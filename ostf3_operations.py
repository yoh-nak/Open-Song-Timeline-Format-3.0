"""Explicit, non-mutating composition operations for OSTF 3.0.0 and Draft 2.

Readers never call this module. Operations do not run a generator or fetch a
resource. They return a completely validated copy or raise without changing the
caller's document. Core notes remain the authority for the chosen performance.
"""
from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
import json
import re
from typing import Any

from ostf3 import (
    MAX, VERSION, DRAFT1_VERSION, DRAFT2_VERSION, PROFILE_VERSION, PHRASE_LIBRARY, CLIP_CHOICES,
    GENERATION, SUPPORTED_VERSIONS, SUPPORTED_PROFILES_BY_VERSION, DocumentValidationError,
    validate_document, invalidate_extensions, _entities,
)

_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,127}\Z")


class OperationError(ValueError):
    """Unsupported or unsafe operation, with a machine-readable reason."""

    def __init__(self, code: str, message: str, diagnostics: list[dict] | None = None):
        super().__init__(message)
        self.code = code
        self.message = message
        self.diagnostics = diagnostics or []


def _require_valid(document: Any) -> None:
    diagnostics = validate_document(document)
    if any(d['severity'] == 'error' for d in diagnostics):
        raise DocumentValidationError(diagnostics)


def _require(condition: bool, code: str, message: str) -> None:
    if not condition:
        raise OperationError(code, message)


def _identifier(value: Any, label: str) -> None:
    _require(isinstance(value, str) and _ID.fullmatch(value) is not None,
             'OPERATION_ID', label + ' must use the OSTF ID grammar.')


def _integer(value: Any, minimum: int, maximum: int, label: str) -> None:
    _require(type(value) is int and minimum <= value <= maximum,
             'OPERATION_INTEGER', label + ' must be an integer in the permitted range.')


def _profile(document: dict, namespace: str, *, current: bool = False) -> dict:
    envelope = document['extensions'].get(namespace)
    supported = SUPPORTED_PROFILES_BY_VERSION.get(document['version'], {})
    _require(namespace in supported, 'OPERATION_UNSUPPORTED_PROFILE',
             'This document version does not interpret the requested profile.')
    _require(envelope is not None and envelope['version'] == supported[namespace],
             'OPERATION_UNSUPPORTED_PROFILE', 'The exact supported profile version is required.')
    if current:
        _require(envelope['status'] == 'current', 'OPERATION_PROFILE_NOT_CURRENT',
                 'This operation requires a current profile; stale data is not regenerated implicitly.')
    return envelope


def _core_index(document: dict) -> dict[str, tuple[str, dict]]:
    return {item['id']: (kind, item) for kind, item, _ in _entities(document)}


def _convert_version(document: dict, target_version: str,
                     allowed_versions: tuple[str, ...]) -> dict:
    """Shared conversion behavior with an explicit source/target version set."""
    _require_valid(document)
    _require(document['version'] in allowed_versions
             and isinstance(target_version, str) and target_version in allowed_versions,
             'OPERATION_VERSION',
             'Source and target must both be one of: ' + ', '.join(allowed_versions) + '.')
    result = deepcopy(document)
    if document['version'] == target_version:
        return result
    before_profiles = SUPPORTED_PROFILES_BY_VERSION[document['version']]
    after_profiles = SUPPORTED_PROFILES_BY_VERSION[target_version]
    for namespace, envelope in result['extensions'].items():
        supported_before = before_profiles.get(namespace) == envelope['version']
        supported_after = after_profiles.get(namespace) == envelope['version']
        if not (supported_before and supported_after):
            if envelope['status'] == 'current' and envelope['dependencies']['scope'] != 'none':
                envelope['status'] = 'unverified'
    result['version'] = target_version
    _require_valid(result)
    return result


def convert_version(document: dict, target_version: str = VERSION) -> dict:
    """Explicitly convert between stable 3.0.0, Draft 1, and Draft 2.

    Core meanings and profile versions are retained. Current extensions with
    non-none dependencies become unverified unless their exact profile version
    is understood on both sides. A newly understood payload must satisfy the
    target schema; conversion never repairs or discards malformed opaque data.
    The input is unchanged, and an identical root version returns a valid copy.
    """
    return _convert_version(document, target_version, SUPPORTED_VERSIONS)


def convert_draft_version(document: dict, target_version: str) -> dict:
    """Legacy conversion restricted to Draft 1 and Draft 2 on both sides.

    target_version remains required. Use convert_version for any conversion
    whose source or destination is stable 3.0.0.
    """
    return _convert_version(document, target_version, (DRAFT1_VERSION, DRAFT2_VERSION))


def materialize_phrase(document: dict, template_id: str, *, instance_id: str,
                       track_id: str, clip_id: str, start: int,
                       repeat_count: int = 1, transpose: int = 0,
                       enabled: bool = True, max_notes: int = 100000) -> dict:
    """Add a new clip and exact phrase instance; never overwrite existing music.

    max_notes is a reference-operation resource limit, not a format limit. IDs
    derive from immutable occurrence identity, not pitch, timing or array order.
    Existing instance refresh, time scaling and individual overrides are outside
    this operation. The caller may explicitly edit or detach those relationships.
    """
    _require_valid(document)
    _require(document['version'] in (DRAFT2_VERSION, VERSION), 'OPERATION_VERSION',
             'Materialization requires Draft 2 or stable 3.0.0.')
    envelope = _profile(document, PHRASE_LIBRARY, current=True)
    for value, label in ((template_id, 'template_id'), (instance_id, 'instance_id'),
                         (track_id, 'track_id'), (clip_id, 'clip_id')):
        _identifier(value, label)
    _integer(start, 0, MAX, 'start')
    _integer(repeat_count, 1, MAX, 'repeat_count')
    _integer(transpose, -127, 127, 'transpose')
    _integer(max_notes, 0, MAX, 'max_notes')
    _require(type(enabled) is bool, 'OPERATION_BOOLEAN', 'enabled must be a boolean.')
    template = next((t for t in envelope['data']['templates'] if t['id'] == template_id), None)
    _require(template is not None, 'OPERATION_TEMPLATE_MISSING', 'No template with the requested ID exists.')
    _require(not any(i['id'] == instance_id for i in envelope['data']['instances']),
             'OPERATION_INSTANCE_EXISTS', 'The instance ID already exists; no instance was replaced.')
    core = _core_index(document)
    _require(track_id in core and core[track_id][0] == 'track', 'OPERATION_TRACK_MISSING',
             'track_id must identify an existing Core track.')
    _require(clip_id not in core, 'OPERATION_ID_COLLISION', 'clip_id already belongs to a Core object.')
    count = len(template['notes']) * repeat_count
    _require(count <= max_notes, 'OPERATION_NOTE_LIMIT',
             'The requested expansion exceeds max_notes; no notes were allocated.')
    span = template['duration'] * repeat_count
    _require(span <= MAX and start + span <= MAX, 'OPERATION_TIME_RANGE',
             'The materialized placement span exceeds Core time bounds.')
    rows, mapping = [], []
    reserved = set(core)
    reserved.add(clip_id)
    # Empty phrases can have large finite repeat counts without looping over
    # empty repetitions. Nonempty expansions were bounded before this loop.
    repetitions = range(repeat_count) if template['notes'] else ()
    for repeat_index in repetitions:
        for source_index, source in enumerate(template['notes']):
            identity = json.dumps([instance_id, repeat_index, source['id']],
                                  ensure_ascii=False, separators=(',', ':'))
            note_id = 'note.' + sha256(identity.encode('utf-8')).hexdigest()
            _require(note_id not in reserved, 'OPERATION_ID_COLLISION',
                     'A generated occurrence ID collides with an existing Core ID.')
            reserved.add(note_id)
            local_start = repeat_index * template['duration'] + source['start']
            onset = start + local_start
            _require(-MAX <= local_start <= MAX and 0 <= onset <= MAX
                     and onset + source['duration'] <= MAX,
                     'OPERATION_TIME_RANGE', 'A generated note has an invalid onset or gate endpoint.')
            note = {'id': note_id, 'start': local_start, 'duration': source['duration']}
            if 'pitch' in source:
                pitch = source['pitch'] + transpose
                _require(0 <= pitch <= 127, 'OPERATION_PITCH_RANGE',
                         'Transposition produces a pitch outside 0..127; no clamping was applied.')
                note['pitch'] = pitch
            else:
                note['soundSlotId'] = source['soundSlotId']
            rows.append((local_start, repeat_index, source_index, note))
            mapping.append({'templateNoteId': source['id'], 'repeatIndex': repeat_index, 'noteId': note_id})
    rows.sort(key=lambda row: row[:3])
    clip = {'id': clip_id, 'start': start, 'duration': span, 'enabled': enabled,
            'notes': [row[3] for row in rows]}
    result = deepcopy(document)
    track = next(t for t in result['tracks'] if t['id'] == track_id)
    track['clips'].append(clip)
    track['clips'].sort(key=lambda c: c['start'])  # stable at equal starts
    updated = result['extensions'][PHRASE_LIBRARY]
    updated['data']['instances'].append({'id': instance_id, 'templateId': template_id,
        'clipId': clip_id, 'repeatCount': repeat_count, 'transpose': transpose, 'noteMap': mapping})
    # This profile now refers to newly created Core objects. Document scope
    # explicitly covers the new complete map without leaving old dependencies.
    updated['dependencies'] = {'scope': 'document'}
    result = invalidate_extensions(result, [{'type': 'track', 'id': track_id}])
    result['extensions'][PHRASE_LIBRARY]['status'] = 'current'
    _require_valid(result)  # certify every instance, not only the new one
    return result


def _note_snapshots(document: dict) -> dict[str, dict]:
    result = {}
    for track in document['tracks']:
        for clip in track['clips']:
            for note in clip['notes']:
                target = {'pitch': note['pitch']} if 'pitch' in note else {'soundSlotId': note['soundSlotId']}
                result[note['id']] = {'target': target, 'onset': clip['start'] + note['start'],
                    'duration': note['duration'],
                    'enabled': track.get('enabled', True) and clip.get('enabled', True)}
    return result


def check_protected_notes(before: dict, after: dict, note_ids: list[str] | tuple[str, ...]) -> dict:
    """Compare fixed protected IDs across valid snapshots at the same PPQ.

    Checks inactive as well as active notes. Tempo, acoustic release, sound
    matching, and the provenance of the two snapshots are not checked.
    """
    _require_valid(before)
    _require_valid(after)
    _require(isinstance(note_ids, (list, tuple)), 'OPERATION_PROTECTION_IDS',
             'note_ids must be a list or tuple of distinct Core note IDs.')
    for note_id in note_ids:
        _identifier(note_id, 'protected note ID')
    _require(len(set(note_ids)) == len(note_ids), 'OPERATION_PROTECTION_IDS',
             'Protected note IDs must be duplicate-free.')
    diagnostics = []
    def add(code, path, message):
        diagnostics.append({'severity': 'error', 'code': code, 'path': path, 'message': message})
    if before['ppq'] != after['ppq']:
        add('PROTECTION_PPQ_MISMATCH', '/ppq',
            'This comparison requires equal PPQ; unequal tick coordinates were not compared.')
        return {'valid': False, 'checkedNoteIds': [], 'diagnostics': diagnostics}
    old, new = _note_snapshots(before), _note_snapshots(after)
    for note_id in note_ids:
        if note_id not in old:
            add('PROTECTION_MISSING_BEFORE', '', 'Protected note ' + note_id + ' does not exist in before.')
        if note_id not in new:
            add('PROTECTION_MISSING_AFTER', '', 'Protected note ' + note_id + ' does not exist in after.')
        if note_id not in old or note_id not in new:
            continue
        for key in ('target', 'onset', 'duration', 'enabled'):
            if old[note_id][key] != new[note_id][key]:
                add('PROTECTION_' + key.upper() + '_CHANGED', '',
                    'Protected note ' + note_id + ' changed ' + key + '.')
    return {'valid': not diagnostics, 'checkedNoteIds': list(note_ids), 'diagnostics': diagnostics}


def check_generation_protection(before: dict, after: dict, process_id: str) -> dict:
    """Use only before's current process declaration to choose protected IDs."""
    _require_valid(before)
    _identifier(process_id, 'process_id')
    envelope = _profile(before, GENERATION, current=True)
    process = next((p for p in envelope['data']['processes'] if p['id'] == process_id), None)
    _require(process is not None, 'OPERATION_PROCESS_MISSING', 'The process does not exist in before.')
    result = check_protected_notes(before, after, process['protectedNoteIds'])
    result['processId'] = process_id
    result['protectionSource'] = 'before'
    return result


def activate_candidate(document: dict, group_id: str, candidate_id: str | None, *,
                       protected_note_ids: list[str] | tuple[str, ...] = ()) -> dict:
    """Explicitly choose one managed clip set without changing parent mutes.

    Only the requested group's clip states are applied. If other groups cannot
    be certified current, validation fails; their choices are never applied as
    a side effect. Protected IDs are fixed by the caller before this operation.
    """
    _require_valid(document)
    _require(document['version'] in (DRAFT2_VERSION, VERSION), 'OPERATION_VERSION',
             'Candidate activation requires Draft 2 or stable 3.0.0.')
    envelope = _profile(document, CLIP_CHOICES)
    _identifier(group_id, 'group_id')
    if candidate_id is not None:
        _identifier(candidate_id, 'candidate_id')
    group = next((g for g in envelope['data']['groups'] if g['id'] == group_id), None)
    _require(group is not None, 'OPERATION_GROUP_MISSING', 'No choice group with the requested ID exists.')
    candidate = next((c for c in group['candidates'] if c['id'] == candidate_id), None)
    _require(candidate_id is None or candidate is not None, 'OPERATION_CANDIDATE_MISSING',
             'The requested candidate does not exist in this group.')
    selected = set(candidate['clipIds']) if candidate is not None else set()
    managed = {ident for c in group['candidates'] for ident in c['clipIds']}
    core = _core_index(document)
    for ident in managed:
        _require(ident in core and core[ident][0] == 'clip', 'OPERATION_CLIP_MISSING',
                 'Every managed clip must resolve before a choice can be applied.')
    result = deepcopy(document)
    result_index = _core_index(result)
    changed = []
    for ident in sorted(managed):
        clip = result_index[ident][1]
        wanted = ident in selected
        if clip.get('enabled', True) != wanted:
            clip['enabled'] = wanted
            changed.append({'type': 'clip', 'id': ident})
    target = next(g for g in result['extensions'][CLIP_CHOICES]['data']['groups'] if g['id'] == group_id)
    metadata_changed = target['selectedCandidateId'] != candidate_id
    target['selectedCandidateId'] = candidate_id
    if changed:
        result = invalidate_extensions(result, changed)
    elif metadata_changed:
        # Different labels may choose identical clip sets. The profile edit can
        # still be relevant to another extension even though Core is unchanged.
        result = invalidate_extensions(result, None)
    result['extensions'][CLIP_CHOICES]['status'] = 'current'
    _require_valid(result)
    protection = check_protected_notes(document, result, protected_note_ids)
    if not protection['valid']:
        raise OperationError('OPERATION_PROTECTION_VIOLATION',
                             'Candidate activation changes a protected note.', protection['diagnostics'])
    return result


def _enforce_protection(before: dict, after: dict, note_ids, message: str) -> None:
    protection = check_protected_notes(before, after, note_ids)
    if not protection['valid']:
        raise OperationError('OPERATION_PROTECTION_VIOLATION', message,
                             protection['diagnostics'])


def replace_phrase_template(document: dict, template_id: str, replacement: dict, *,
                            protected_note_ids: list[str] | tuple[str, ...] = (),
                            max_notes: int = 100000) -> dict:
    """Replace one current template and refresh every linked placement atomically.

    Surviving occurrence keys retain their existing Core IDs, including IDs
    assigned by other writers. New occurrences use the reference materializer's
    deterministic identity policy. Removing a lyrically referenced note is
    refused. Detach a placement first when it should keep independent edits.

    The Draft 2 editing contract also applies to stable 3.0.0; no new wire
    fields are introduced.
    max_notes bounds the total resulting notes across all linked placements,
    before expansion. An identical validated replacement is a no-op copy.
    """
    _require_valid(document)
    _require(document['version'] in (DRAFT2_VERSION, VERSION), 'OPERATION_VERSION',
             'Template replacement requires Draft 2 or stable 3.0.0.')
    envelope = _profile(document, PHRASE_LIBRARY, current=True)
    _identifier(template_id, 'template_id')
    _integer(max_notes, 0, MAX, 'max_notes')
    template_index = next((i for i, item in enumerate(envelope['data']['templates'])
                           if item['id'] == template_id), None)
    _require(template_index is not None, 'OPERATION_TEMPLATE_MISSING',
             'No template with the requested ID exists.')
    _require(isinstance(replacement, dict) and replacement.get('id') == template_id,
             'OPERATION_TEMPLATE_ID',
             'replacement must be a complete template with the existing template ID.')

    # Check strict types and the full existing template schema before comparing
    # values: Python equality alone would equate an integer and 1.0 or True.
    result = deepcopy(document)
    updated = result['extensions'][PHRASE_LIBRARY]
    updated['data']['templates'][template_index] = deepcopy(replacement)
    updated['status'] = 'unverified'
    _require_valid(result)
    template = updated['data']['templates'][template_index]
    core = _core_index(document)
    for source in template['notes']:
        if 'soundSlotId' in source:
            ident = source['soundSlotId']
            _require(ident in core and core[ident][0] == 'soundSlot',
                     'OPERATION_SOUND_SLOT_MISSING',
                     'Every replacement template sound slot must resolve.')
    original = envelope['data']['templates'][template_index]
    if template == original:
        result = deepcopy(document)
        _enforce_protection(document, result, protected_note_ids,
                            'The fixed protection list could not be satisfied.')
        return result

    instances = [item for item in updated['data']['instances']
                 if item['templateId'] == template_id]
    total = sum(len(template['notes']) * item['repeatCount'] for item in instances)
    _require(total <= max_notes, 'OPERATION_NOTE_LIMIT',
             'The complete template update exceeds max_notes; no notes were expanded.')
    reserved = set(core)  # Keep removed IDs reserved for this whole transaction.
    result_core = _core_index(result)
    removed_ids, changed_refs = set(), []
    pattern_changed = (template['duration'] != original['duration']
                       or template['notes'] != original['notes'])
    for instance in instances if pattern_changed else ():
        clip = result_core[instance['clipId']][1]
        span = template['duration'] * instance['repeatCount']
        _require(span <= MAX and clip['start'] + span <= MAX,
                 'OPERATION_TIME_RANGE', 'A refreshed clip span exceeds Core time bounds.')
        old_map = {(item['repeatIndex'], item['templateNoteId']): item['noteId']
                   for item in instance['noteMap']}
        old_ids = {note['id'] for note in clip['notes']}
        rows, mappings = [], []
        repetitions = range(instance['repeatCount']) if template['notes'] else ()
        for repeat_index in repetitions:
            for source_index, source in enumerate(template['notes']):
                key = repeat_index, source['id']
                if key in old_map:
                    note_id = old_map[key]
                else:
                    identity = json.dumps([instance['id'], repeat_index, source['id']],
                                          ensure_ascii=False, separators=(',', ':'))
                    note_id = 'note.' + sha256(identity.encode('utf-8')).hexdigest()
                    _require(note_id not in reserved, 'OPERATION_ID_COLLISION',
                             'A new occurrence ID collides with an original or newly allocated Core ID.')
                    reserved.add(note_id)
                local_start = repeat_index * template['duration'] + source['start']
                onset = clip['start'] + local_start
                _require(-MAX <= local_start <= MAX and 0 <= onset <= MAX
                         and onset + source['duration'] <= MAX,
                         'OPERATION_TIME_RANGE', 'A refreshed note has an invalid onset or gate endpoint.')
                note = {'id': note_id, 'start': local_start, 'duration': source['duration']}
                if 'pitch' in source:
                    pitch = source['pitch'] + instance['transpose']
                    _require(0 <= pitch <= 127, 'OPERATION_PITCH_RANGE',
                             'A refreshed instance pitch is outside 0..127; the whole update was refused.')
                    note['pitch'] = pitch
                else:
                    note['soundSlotId'] = source['soundSlotId']
                rows.append((local_start, repeat_index, source_index, note))
                mappings.append({'templateNoteId': source['id'], 'repeatIndex': repeat_index,
                                 'noteId': note_id})
        rows.sort(key=lambda row: row[:3])
        notes = [row[3] for row in rows]
        removed_ids.update(old_ids - {note['id'] for note in notes})
        if clip['duration'] != span or clip['notes'] != notes:
            changed_refs.append({'type': 'clip', 'id': clip['id']})
            clip['duration'], clip['notes'] = span, notes
        instance['noteMap'] = mappings

    dangling = []
    for ai, alignment in enumerate(document['lyrics']['alignments']):
        for ni, note_id in enumerate(alignment['noteIds']):
            if note_id in removed_ids:
                dangling.append({'severity': 'error', 'code': 'LYRIC_NOTE_REMOVAL',
                    'path': '/lyrics/alignments/' + str(ai) + '/noteIds/' + str(ni),
                    'message': 'Alignment ' + alignment['id'] + ' still refers to removed note ' + note_id + '.'})
    if dangling:
        raise OperationError('OPERATION_REFERENCED_NOTE_REMOVAL',
                             'The update would remove a Core note referenced by lyrics; no alignment was changed.',
                             dangling)

    updated['dependencies'] = {'scope': 'document'}
    changed_refs.extend({'type': 'note', 'id': ident} for ident in sorted(removed_ids))
    # Deleted ancestry may be unknown, so the existing invalidation helper is
    # deliberately conservative. Metadata-only changes follow the same rule as
    # a choice whose candidate ID changes without changing its clip set.
    result = invalidate_extensions(result, changed_refs if changed_refs else None)
    result['extensions'][PHRASE_LIBRARY]['status'] = 'current'
    _require_valid(result)
    _enforce_protection(document, result, protected_note_ids,
                        'Template replacement changes a protected note.')
    return result


def detach_phrase_instances(document: dict, instance_ids: list[str] | tuple[str, ...], *,
                            protected_note_ids: list[str] | tuple[str, ...] = ()) -> dict:
    """Remove selected phrase links while preserving all Core music and IDs.

    Known stale/unverified links may be detached without regenerating their
    manually edited notes. The phrase profile retains its original status and
    dependencies. Templates remain reusable; this operation deletes no notes.
    """
    _require_valid(document)
    _require(document['version'] in (DRAFT2_VERSION, VERSION), 'OPERATION_VERSION',
             'Phrase detachment requires Draft 2 or stable 3.0.0.')
    envelope = _profile(document, PHRASE_LIBRARY)
    _require(isinstance(instance_ids, (list, tuple)), 'OPERATION_INSTANCE_IDS',
             'instance_ids must be a list or tuple of distinct instance IDs.')
    for ident in instance_ids:
        _identifier(ident, 'instance ID')
    _require(len(instance_ids) == len(set(instance_ids)), 'OPERATION_INSTANCE_IDS',
             'Instance IDs must be duplicate-free.')
    requested = set(instance_ids)
    existing = {item['id'] for item in envelope['data']['instances']}
    _require(requested <= existing, 'OPERATION_INSTANCE_MISSING',
             'Every requested instance must exist; no partial detachment was performed.')
    result = deepcopy(document)
    if requested:
        own = result['extensions'][PHRASE_LIBRARY]
        own['data']['instances'] = [item for item in own['data']['instances']
                                   if item['id'] not in requested]
        result = invalidate_extensions(result, None)
        result['extensions'][PHRASE_LIBRARY]['status'] = envelope['status']
    _require_valid(result)
    _enforce_protection(document, result, protected_note_ids,
                        'The fixed protection list could not be satisfied after detachment.')
    return result
