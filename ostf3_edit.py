#!/usr/bin/env python3
"""Perform explicit OSTF version conversion, phrase editing or clip selection."""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import sys

from ostf3 import VERSION, DRAFT1_VERSION, DRAFT2_VERSION, SUPPORTED_VERSIONS, DocumentValidationError, WireError, load_strict, dump_strict, validate_document, performance_end
from ostf3_migrate import _write_output
from ostf3_operations import OperationError, convert_version, convert_draft_version, materialize_phrase, activate_candidate, check_protected_notes, check_generation_protection, replace_phrase_template, detach_phrase_instances


def _output_arguments(parser):
    parser.add_argument('source', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('--force', action='store_true', help='replace the output, never an input alias')
    parser.add_argument('--json', action='store_true', help='emit a machine-readable operation receipt')


def _destination(source: Path, output: Path, force: bool):
    same = source.resolve() == output.resolve()
    if not same and source.exists() and output.exists():
        same = os.path.samefile(source, output)
    if same:
        raise OperationError('OPERATION_INPUT_OVERWRITE', 'Input and output must be different files, including with --force.')
    if output.exists() and not force:
        raise OperationError('OPERATION_OUTPUT_EXISTS', 'Output exists; choose another path or explicitly use --force.')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    p = sub.add_parser('convert', help='Explicitly convert between stable 3.0.0, Draft 1, and Draft 2.')
    _output_arguments(p)
    p.add_argument('--to-version', required=True, choices=SUPPORTED_VERSIONS,
                   help='exact destination root version')
    for name, description in [('upgrade', 'Legacy Draft 1/2 alias: convert to Draft 2.'), ('downgrade', 'Legacy Draft 1/2 alias: convert to Draft 1, retaining new profiles as opaque data.')]:
        _output_arguments(sub.add_parser(name, help=description))
    p = sub.add_parser('materialize', help='Add a new phrase instance and Core clip.')
    _output_arguments(p)
    p.add_argument('--template', required=True)
    p.add_argument('--instance', required=True)
    p.add_argument('--track', required=True)
    p.add_argument('--clip', required=True)
    p.add_argument('--start', required=True, type=int)
    p.add_argument('--repeat', default=1, type=int)
    p.add_argument('--transpose', default=0, type=int)
    p.add_argument('--disabled', action='store_true')
    p.add_argument('--max-notes', default=100000, type=int, help='explicit expansion resource limit')
    p = sub.add_parser('choose', help='Apply one clip candidate, keeping parent track mutes.')
    _output_arguments(p)
    p.add_argument('--group', required=True)
    choice = p.add_mutually_exclusive_group(required=True)
    choice.add_argument('--candidate')
    choice.add_argument('--none', action='store_true', help='disable all clips managed by the group')
    p.add_argument('--protect-note', action='append', default=[], metavar='NOTE_ID')
    p.add_argument('--protect-process', help='also enforce the input snapshot process protection list')
    p = sub.add_parser('replace-template', help='Replace one current phrase template and refresh all of its instances.')
    _output_arguments(p)
    p.add_argument('--template', required=True)
    p.add_argument('--replacement', required=True, type=Path, help='strict JSON file containing one complete replacement template')
    p.add_argument('--max-notes', default=100000, type=int, help='total output note limit across all refreshed instances')
    p.add_argument('--protect-note', action='append', default=[], metavar='NOTE_ID')
    p.add_argument('--protect-process', help='also enforce the input snapshot process protection list')
    p = sub.add_parser('detach', help='Remove selected phrase-instance links while preserving every Core object.')
    _output_arguments(p)
    p.add_argument('--instance', action='append', required=True, help='instance ID; repeat this option')
    p.add_argument('--protect-note', action='append', default=[], metavar='NOTE_ID')
    p.add_argument('--protect-process', help='also enforce the input snapshot process protection list')
    p = sub.add_parser('check-protection', help='Compare protected notes across two snapshots; write no file.')
    p.add_argument('before', type=Path)
    p.add_argument('after', type=Path)
    protection = p.add_mutually_exclusive_group(required=True)
    protection.add_argument('--process', help='take the protection list only from before')
    protection.add_argument('--note', action='append', help='fixed protected note ID; repeat this option')
    p.add_argument('--json', action='store_true')
    args = parser.parse_args(argv)
    try:
        if args.command == 'check-protection':
            before, after = load_strict(args.before.read_bytes()), load_strict(args.after.read_bytes())
            report = check_generation_protection(before, after, args.process) if args.process is not None else check_protected_notes(before, after, args.note)
            report['commandPassed'] = report['valid']
            if args.json:
                print(dump_strict(report))
            else:
                print(('PASS' if report['valid'] else 'FAIL') + ': checked ' + str(len(report['checkedNoteIds'])) + ' protected note IDs.')
                for diagnostic in report['diagnostics']:
                    print(diagnostic['code'] + ': ' + diagnostic['message'])
            return 0 if report['valid'] else 1
        _destination(args.source, args.output, args.force)
        if args.command == 'replace-template':
            _destination(args.replacement, args.output, args.force)
        before = load_strict(args.source.read_bytes())
        if args.command == 'convert':
            result = convert_version(before, args.to_version)
        elif args.command in ('upgrade', 'downgrade'):
            result = convert_draft_version(before, DRAFT2_VERSION if args.command == 'upgrade' else DRAFT1_VERSION)
        elif args.command == 'materialize':
            result = materialize_phrase(before, args.template, instance_id=args.instance, track_id=args.track,
                clip_id=args.clip, start=args.start, repeat_count=args.repeat, transpose=args.transpose,
                enabled=not args.disabled, max_notes=args.max_notes)
        elif args.command == 'choose':
            result = activate_candidate(before, args.group, None if args.none else args.candidate,
                                        protected_note_ids=args.protect_note)
        elif args.command == 'replace-template':
            template = load_strict(args.replacement.read_bytes())
            result = replace_phrase_template(before, args.template, template,
                protected_note_ids=args.protect_note, max_notes=args.max_notes)
        else:
            result = detach_phrase_instances(before, args.instance, protected_note_ids=args.protect_note)
        if getattr(args, 'protect_process', None) is not None:
            guard = check_generation_protection(before, result, args.protect_process)
            if not guard['valid']:
                raise OperationError('OPERATION_PROTECTION_VIOLATION',
                    'The edit violates the input process protection list.', guard['diagnostics'])
        _write_output(args.output, dump_strict(result), force=args.force)
        report = {'commandPassed': True, 'operation': args.command, 'output': str(args.output),
                  'inputVersion': before['version'], 'outputVersion': result['version'],
                  'performanceEnd': performance_end(result), 'diagnostics': validate_document(result)}
        if args.json:
            print(dump_strict(report))
        else:
            print('Created ' + str(args.output) + ' (' + result['version'] + ').')
            print('Operation: ' + args.command + '; performance end: ' + str(report['performanceEnd']) + ' ticks.')
            for diagnostic in report['diagnostics']:
                print(diagnostic['severity'].upper() + ' ' + diagnostic['code'] + ': ' + diagnostic['message'])
        return 0
    except DocumentValidationError as exc:
        error = {'code': 'DOCUMENT_INVALID', 'message': str(exc), 'diagnostics': exc.diagnostics}
        status = 1
    except OperationError as exc:
        error = {'code': exc.code, 'message': str(exc), 'diagnostics': exc.diagnostics}
        status = 1
    except WireError as exc:
        error = {'code': exc.code, 'message': str(exc), 'diagnostics': [exc.diagnostic()]}
        status = 1
    except (OSError, RuntimeError) as exc:
        error = {'code': 'TOOL_ERROR', 'message': str(exc), 'diagnostics': []}
        status = 2
    if args.json:
        print(dump_strict({'commandPassed': False, 'error': error}))
    else:
        print(error['code'] + ': ' + error['message'], file=sys.stderr)
    return status


if __name__ == '__main__':
    raise SystemExit(main())
