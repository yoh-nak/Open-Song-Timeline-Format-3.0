#!/usr/bin/env python3
"""Validate local OSTF files. Exit 0: valid; 1: invalid/policy; 2: tool/I/O error."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from ostf3 import SUPPORTED_VERSIONS, VERSION, WireError, load_strict, performance_end, realized_events, schema_self_check, validate_document


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="*", help="OSTF paths, or - for standard input")
    parser.add_argument("--json", action="store_true", help="Machine-readable JSON diagnostics")
    parser.add_argument("--events", action="store_true", help="Include sorted active core note events")
    parser.add_argument("--warnings-as-errors", action="store_true", help="Fail the command on warnings, without changing diagnostic severity")
    parser.add_argument("--schema-check", action="store_true", help="Check the bundled JSON Schema")
    parser.add_argument("--schema-version", choices=SUPPORTED_VERSIONS, help=f"Exact schema version for --schema-check (default: {VERSION})")
    args = parser.parse_args(argv)
    if not args.files and not args.schema_check:
        parser.error("provide a file or --schema-check")
    if args.files.count("-") > 1:
        parser.error("standard input may be used only once")
    if args.schema_version is not None and not args.schema_check:
        parser.error("--schema-version requires --schema-check")
    report = {"formatVersion": VERSION, "supportedFormatVersions": list(SUPPORTED_VERSIONS), "files": [], "valid": True}
    exit_code = 0
    if args.schema_check:
        report["schemaVersion"] = args.schema_version or VERSION
        try:
            schema_self_check(report["schemaVersion"])
            report["schemaValid"] = True
        except Exception as exc:
            report["schemaValid"] = False
            report["toolError"] = str(exc)
            report["valid"] = False
            exit_code = 2
    for filename in args.files:
        record = {"file": filename, "valid": False, "diagnostics": []}
        try:
            content = sys.stdin.buffer.read() if filename == "-" else Path(filename).read_bytes()
            document = load_strict(content)
            if isinstance(document.get("version"), str):
                record["formatVersion"] = document["version"]
            record["diagnostics"] = validate_document(document)
            record["valid"] = not any(d["severity"] == "error" for d in record["diagnostics"])
            if record["valid"]:
                record["performanceEnd"] = performance_end(document)
                if args.events:
                    record["events"] = realized_events(document)
            if not record["valid"] or (args.warnings_as_errors and record["diagnostics"]):
                exit_code = max(exit_code, 1)
        except WireError as exc:
            record["diagnostics"].append(exc.diagnostic())
            exit_code = max(exit_code, 1)
        except (OSError, RuntimeError) as exc:
            record["diagnostics"].append({"severity": "error", "code": "TOOL_ERROR", "path": "", "message": str(exc)})
            exit_code = 2
        report["files"].append(record)
    report["valid"] = report["valid"] and all(item["valid"] for item in report["files"])
    report["commandPassed"] = exit_code == 0
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        if "schemaValid" in report:
            print(f"Schema {report['schemaVersion']}: " + ("valid" if report["schemaValid"] else "invalid"))
        if "toolError" in report:
            print(report["toolError"], file=sys.stderr)
        for record in report["files"]:
            print(f"{record['file']}: {'VALID' if record['valid'] else 'INVALID'}")
            for item in record["diagnostics"]:
                print(f"  {item['severity'].upper()} {item['code']} {item['path'] or '/'}: {item['message']}")
            if "performanceEnd" in record:
                print(f"  Performance end: {record['performanceEnd']} ticks")
            if args.events and "events" in record:
                print(json.dumps(record["events"], ensure_ascii=False, indent=2))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
