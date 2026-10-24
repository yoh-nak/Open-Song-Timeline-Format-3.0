#!/usr/bin/env python3
"""Conservative archival migration from declared OSTF 2.3.0 to stable 3.0.0.

Default: recognized title/timeline/appearance only. Interpreting sample-shaped
notes and chord symbols requires --interpret-sample-notes. This converter does
not certify complete 2.3 conformance or complete musical conversion.
Draft 2 remains available as an explicitly selected destination version.
"""
from __future__ import annotations

import argparse
from collections import Counter
from decimal import Decimal
import hashlib
import os
from pathlib import Path
import re
import sys
import tempfile
from typing import Any

from ostf3 import VERSION, DRAFT2_VERSION, dump_strict, load_strict, validate_document

TARGET_VERSION = VERSION
MIGRATION_TARGET_VERSIONS = (VERSION, DRAFT2_VERSION)
PROFILE_VERSION = "1.0.0-draft.1"
ARCHIVE_NAMESPACE = "org.ostf.legacy-import.v1"
OLD_APPEARANCE_NAMESPACE = "org.ostf.section-role-appearance.v1"
APPEARANCE_NAMESPACE = "org.ostf.appearance.v1"
MAX_INTEGER = 9007199254740991
ID_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,127}\Z", re.ASCII)
COLOR_RE = re.compile(r"#[0-9A-Fa-f]{6}\Z", re.ASCII)


class MigrationError(ValueError):
    """The bounded conversion cannot safely produce the requested target."""


class _Ids:
    def __init__(self) -> None:
        self.used: set[str] = set()

    def allocate(self, preferred: Any, fallback: str) -> str:
        if isinstance(preferred, str) and ID_RE.fullmatch(preferred) and preferred not in self.used:
            result = preferred
        else:
            result = fallback
            suffix = 2
            while result in self.used:
                result = f"{fallback}.{suffix}"
                suffix += 1
        self.used.add(result)
        return result


def _warn(report: dict, code: str, path: str, message: str) -> None:
    report["warnings"].append({"code": code, "path": path, "message": message})


def _archive_only(report: dict, path: str, reason: str) -> None:
    report["archivedOnly"].append({"path": path, "reason": reason})


def _require(condition: bool, path: str, message: str) -> None:
    if not condition:
        raise MigrationError(f"{path}: {message}")


def _integer(value: Any, minimum: int = 0, maximum: int = MAX_INTEGER) -> bool:
    return type(value) is int and minimum <= value <= maximum


def _nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and len(value) > 0


def _time_pair(obj: dict, path: str, report: dict) -> tuple[int, int] | None:
    start, duration = obj.get("start"), obj.get("duration")
    if not _integer(start) or not _integer(duration, 1) or start + duration > MAX_INTEGER:
        reason = "No complete bounded integer start/duration pair; timing was not invented."
        _archive_only(report, path, reason)
        _warn(report, "uninterpreted_timing", path, reason)
        return None
    return start, duration


def _extra_fields(obj: dict, known: set[str], path: str, report: dict, *, block: bool) -> bool:
    extra = sorted(set(obj) - known)
    if extra:
        message = "Uninterpreted fields: " + ", ".join(extra)
        if block:
            message += ". Performance object archived only; unknown control semantics were not guessed."
            _archive_only(report, path, message)
        else:
            message += ". These fields remain in the complete source archive."
        _warn(report, "uninterpreted_fields", path, message)
    return bool(extra)


def _mapping(report: dict, source_type: str, path: str, source_id: Any,
             target_type: str, target_id: str) -> None:
    report["idMappings"].append({
        "sourceType": source_type, "sourcePath": path,
        "sourceId": source_id if isinstance(source_id, str) else None,
        "targetType": target_type, "targetId": target_id,
    })
    if isinstance(source_id, str) and source_id != target_id:
        _warn(report, "id_remapped", path + "/id",
              f"ID {source_id!r} became {target_id!r} to satisfy target identity constraints.")


def _original_id_counts(source: dict) -> dict[str, Counter]:
    chords = source["harmony"].get("chords", [])
    clips = []
    for melody in source["melodies"]:
        if isinstance(melody, dict) and isinstance(melody.get("clips"), list):
            clips.extend(melody["clips"])
    groups = {"section": source["timeline"]["sections"],
              "chordClip": chords if isinstance(chords, list) else [], "melodyClip": clips}
    return {kind: Counter(item["id"] for item in objects
                          if isinstance(item, dict) and _nonempty_string(item.get("id")))
            for kind, objects in groups.items()}


def _sorted_events(items: list[dict], path: str, report: dict) -> list[dict]:
    if any(a["start"] > b["start"] for a, b in zip(items, items[1:])):
        _warn(report, "stable_temporal_sort", path,
              "Converted events sorted by start; equal-start order retained.")
    return sorted(items, key=lambda item: item["start"])


def _transfer_timeline(source: dict, ids: _Ids, report: dict,
                       refs: dict[tuple[str, str], dict]) -> dict:
    timeline = source["timeline"]
    for name in ("sections", "tempoChanges", "meterChanges"):
        _require(isinstance(timeline.get(name), list) and bool(timeline[name]),
                 "/timeline/" + name, "requires a nonempty array in this bounded 2.3 source check")
    _extra_fields(timeline, {"sections", "tempoChanges", "meterChanges"}, "/timeline", report, block=False)
    sections = []
    old_ids: set[str] = set()
    previous_end = 0
    for index, item in enumerate(timeline["sections"]):
        path = f"/timeline/sections/{index}"
        _require(isinstance(item, dict), path, "requires an object")
        _require(_nonempty_string(item.get("id")), path + "/id", "requires a nonempty string")
        _require(item["id"] not in old_ids, path + "/id", "duplicate source section ID")
        old_ids.add(item["id"])
        _require(_nonempty_string(item.get("name")), path + "/name", "requires a nonempty string")
        start, duration = item.get("start"), item.get("duration")
        _require(_integer(start) and _integer(duration, 1), path, "requires bounded integer timing")
        _require(start + duration <= MAX_INTEGER, path, "section end exceeds target bound")
        _require(start >= previous_end, path, "source sections are unsorted or overlapping")
        previous_end = start + duration
        new_id = ids.allocate(item["id"], f"import-section-{index + 1:03d}")
        section = {"id": new_id, "name": item["name"], "start": start, "duration": duration}
        if "role" in item:
            _require(isinstance(item["role"], str), path + "/role", "requires a string")
            section["role"] = item["role"]
        _extra_fields(item, {"id", "name", "start", "duration", "role"}, path, report, block=False)
        sections.append(section)
        _mapping(report, "section", path, item["id"], "section", new_id)
        refs[("section", item["id"])] = {"type": "section", "id": new_id}
    converted = {"sections": sections, "tempoChanges": [], "meterChanges": []}
    for name in ("tempoChanges", "meterChanges"):
        previous_at = -1
        for index, item in enumerate(timeline[name]):
            path = f"/timeline/{name}/{index}"
            _require(isinstance(item, dict), path, "requires an object")
            at = item.get("at")
            _require(_integer(at), path + "/at", "requires a bounded integer")
            _require((index != 0 or at == 0) and at > previous_at, path + "/at",
                     "map must begin at zero and have strictly increasing positions")
            previous_at = at
            if name == "tempoChanges":
                bpm = item.get("bpm")
                _require(not isinstance(bpm, bool) and isinstance(bpm, (int, float, Decimal))
                         and 0 < bpm <= 1000, path + "/bpm", "requires target BPM in (0, 1000]")
                converted[name].append({"at": at, "bpm": bpm})
                known = {"at", "bpm"}
            else:
                numerator, denominator = item.get("numerator"), item.get("denominator")
                _require(_integer(numerator, 1, 64), path + "/numerator", "requires integer 1..64")
                _require(type(denominator) is int and denominator in (1, 2, 4, 8, 16, 32, 64),
                         path + "/denominator", "requires a supported integer denominator")
                converted[name].append({"at": at, "numerator": numerator, "denominator": denominator})
                known = {"at", "numerator", "denominator"}
            _extra_fields(item, known, path, report, block=False)
    return converted


def _interpret_music(source: dict, target: dict, ids: _Ids, report: dict,
                     counts: dict[str, Counter], refs: dict[tuple[str, str], dict]) -> None:
    chords = source["harmony"].get("chords", [])
    if not isinstance(chords, list):
        _archive_only(report, "/harmony/chords", "Not an array; no chord payload interpreted.")
        _warn(report, "uninterpreted_chords", "/harmony/chords", "Not an array; source retained.")
        chords = []
    for index, item in enumerate(chords):
        path = f"/harmony/chords/{index}"
        if not isinstance(item, dict):
            _archive_only(report, path, "Not a sample-shaped chord object.")
            continue
        if _extra_fields(item, {"id", "start", "duration", "symbol"}, path, report, block=True):
            continue
        timing = _time_pair(item, path, report)
        if timing is None:
            continue
        if not _nonempty_string(item.get("symbol")):
            _archive_only(report, path, "No nonempty sample symbol string; label was not inferred.")
            _warn(report, "uninterpreted_symbol", path, "A nonempty sample symbol string is required.")
            continue
        new_id = ids.allocate(item.get("id"), f"import-chord-{index + 1:03d}")
        target["harmony"]["chords"].append({
            "id": new_id, "start": timing[0], "duration": timing[1], "label": item["symbol"],
        })
        _mapping(report, "chordClip", path, item.get("id"), "chord", new_id)
        if isinstance(item.get("id"), str) and counts["chordClip"][item["id"]] == 1:
            refs[("chordClip", item["id"])] = {"type": "chord", "id": new_id}
    target["harmony"]["chords"] = _sorted_events(target["harmony"]["chords"], "/harmony/chords", report)

    for ti, item in enumerate(source["melodies"]):
        path = f"/melodies/{ti}"
        if not isinstance(item, dict):
            _archive_only(report, path, "Not a sample-shaped melody object.")
            continue
        if _extra_fields(item, {"id", "name", "clips"}, path, report, block=True):
            continue
        if "clips" in item and not isinstance(item["clips"], list):
            _archive_only(report, path, "clips is not an array; no part interpreted.")
            _warn(report, "uninterpreted_clips", path + "/clips", "Expected a sample clips array.")
            continue
        name = item.get("name")
        if not isinstance(name, str):
            name = f"Imported melody {ti + 1}"
            _warn(report, "generated_display_name", path + "/name", "A display label was generated; no musical meaning inferred.")
        track_id = ids.allocate(item.get("id"), f"import-track-{ti + 1:03d}")
        track = {"id": track_id, "name": name, "clips": []}
        _mapping(report, "melody", path, item.get("id"), "track", track_id)
        for ci, clip in enumerate(item.get("clips", [])):
            cpath = f"{path}/clips/{ci}"
            if not isinstance(clip, dict):
                _archive_only(report, cpath, "Not a sample-shaped clip object.")
                continue
            if _extra_fields(clip, {"id", "name", "start", "duration", "notes"}, cpath, report, block=True):
                continue
            timing = _time_pair(clip, cpath, report)
            if timing is None:
                continue
            if "notes" in clip and not isinstance(clip["notes"], list):
                _archive_only(report, cpath, "notes is not an array; clip was not interpreted.")
                _warn(report, "uninterpreted_notes", cpath + "/notes", "Expected a sample notes array.")
                continue
            clip_id = ids.allocate(clip.get("id"), f"import-clip-{ti + 1:03d}-{ci + 1:03d}")
            new_clip = {"id": clip_id, "start": timing[0], "duration": timing[1], "notes": []}
            if isinstance(clip.get("name"), str):
                new_clip["name"] = clip["name"]
            _mapping(report, "melodyClip", cpath, clip.get("id"), "clip", clip_id)
            if isinstance(clip.get("id"), str) and counts["melodyClip"][clip["id"]] == 1:
                refs[("melodyClip", clip["id"])] = {"type": "clip", "id": clip_id}
            for ni, note in enumerate(clip.get("notes", [])):
                npath = f"{cpath}/notes/{ni}"
                if not isinstance(note, dict):
                    _archive_only(report, npath, "Not a sample-shaped note object.")
                    continue
                if _extra_fields(note, {"id", "pitch", "start", "duration"}, npath, report, block=True):
                    continue
                pitch, start, duration = note.get("pitch"), note.get("start"), note.get("duration")
                valid = (_integer(pitch, 0, 127) and _integer(start, -MAX_INTEGER) and _integer(duration, 1))
                if valid:
                    onset = timing[0] + start
                    valid = 0 <= onset <= MAX_INTEGER and onset + duration <= MAX_INTEGER
                if not valid:
                    reason = "pitch/start/duration fail the explicit sample interpretation or target bounds."
                    _archive_only(report, npath, reason)
                    _warn(report, "uninterpreted_note", npath, reason)
                    continue
                note_id = ids.allocate(note.get("id"), f"import-note-{ti + 1:03d}-{ci + 1:03d}-{ni + 1:03d}")
                new_clip["notes"].append({"id": note_id, "pitch": pitch, "start": start, "duration": duration})
                _mapping(report, "note", npath, note.get("id"), "note", note_id)
            new_clip["notes"] = _sorted_events(new_clip["notes"], cpath + "/notes", report)
            track["clips"].append(new_clip)
        track["clips"] = _sorted_events(track["clips"], path + "/clips", report)
        target["tracks"].append(track)


def _transfer_appearance(source: dict, target: dict, report: dict,
                         refs: dict[tuple[str, str], dict]) -> None:
    if OLD_APPEARANCE_NAMESPACE not in source["extensions"]:
        return
    ext = source["extensions"][OLD_APPEARANCE_NAMESPACE]
    path = "/extensions/" + OLD_APPEARANCE_NAMESPACE
    if not isinstance(ext, dict) or ext.get("version") != "1.0.0" or not isinstance(ext.get("data"), dict):
        _warn(report, "uninterpreted_appearance_version", path,
              "Only known legacy appearance version 1.0.0 is interpreted; original retained.")
        return
    _extra_fields(ext, {"version", "data"}, path, report, block=False)
    old = ext["data"]
    _extra_fields(old, {"roleDefinitions", "sectionRoleAssignments", "appearance"},
                  path + "/data", report, block=False)
    data = {"roleDefinitions": [], "sectionRoleAssignments": {}, "appearance": {
        "roleColors": {}, "customRoleColors": {}, "objectColors": [],
    }}
    role_ids = _Ids()
    role_map: dict[str, str] = {}
    definitions = old.get("roleDefinitions", [])
    if not isinstance(definitions, list):
        _warn(report, "uninterpreted_roles", path + "/data/roleDefinitions", "Expected an array.")
        definitions = []
    role_counts = Counter(role["id"] for role in definitions
                          if isinstance(role, dict) and _nonempty_string(role.get("id")))
    for index, role in enumerate(definitions):
        rpath = f"{path}/data/roleDefinitions/{index}"
        if (not isinstance(role, dict) or not _nonempty_string(role.get("id"))
                or not _nonempty_string(role.get("name")) or role_counts[role["id"]] != 1
                or ("baseRole" in role and not isinstance(role["baseRole"], str))):
            _warn(report, "uninterpreted_role", rpath, "Invalid or ambiguous role definition archived only.")
            continue
        rid = role_ids.allocate(role["id"], f"import-role-{index + 1:03d}")
        new_role = {"id": rid, "name": role["name"]}
        if "baseRole" in role:
            new_role["baseRole"] = role["baseRole"]
        _extra_fields(role, {"id", "name", "baseRole"}, rpath, report, block=False)
        data["roleDefinitions"].append(new_role)
        role_map[role["id"]] = rid
        _mapping(report, "customRole", rpath, role["id"], "appearanceRole", rid)
    assignments = old.get("sectionRoleAssignments", {})
    if not isinstance(assignments, dict):
        _warn(report, "uninterpreted_role_assignments", path, "Expected section-role assignment object.")
        assignments = {}
    for sid, rid in assignments.items():
        ref = refs.get(("section", sid))
        if ref is not None and isinstance(rid, str) and rid in role_map:
            data["sectionRoleAssignments"][ref["id"]] = role_map[rid]
        else:
            _warn(report, "unresolved_role_assignment", path + "/data/sectionRoleAssignments",
                  f"Assignment for source section {sid!r} archived only.")
    appearance = old.get("appearance", {})
    if not isinstance(appearance, dict):
        _warn(report, "uninterpreted_appearance", path, "Expected appearance object.")
        appearance = {}
    _extra_fields(appearance, {"roleColors", "customRoleColors", "objectColors"},
                  path + "/data/appearance", report, block=False)
    for field in ("roleColors", "customRoleColors"):
        colors = appearance.get(field, {})
        if not isinstance(colors, dict):
            _warn(report, "uninterpreted_color_map", path + "/data/appearance/" + field, "Expected object.")
            continue
        for key, color in colors.items():
            mapped = key if field == "roleColors" else role_map.get(key)
            if mapped is not None and isinstance(color, str) and COLOR_RE.fullmatch(color):
                data["appearance"][field][mapped] = color
            else:
                _warn(report, "uninterpreted_color", path + "/data/appearance/" + field,
                      f"Invalid color or unresolved custom role {key!r} archived only.")
    colors = appearance.get("objectColors", [])
    if not isinstance(colors, list):
        _warn(report, "uninterpreted_object_colors", path, "Expected objectColors array.")
        colors = []
    target_counts = Counter((entry.get("targetType"), entry.get("targetId"))
                            for entry in colors if isinstance(entry, dict)
                            and isinstance(entry.get("targetType"), str) and isinstance(entry.get("targetId"), str))
    for index, entry in enumerate(colors):
        cpath = f"{path}/data/appearance/objectColors/{index}"
        if not isinstance(entry, dict):
            _warn(report, "uninterpreted_object_color", cpath, "Expected an object.")
            continue
        _extra_fields(entry, {"targetType", "targetId", "color"}, cpath, report, block=False)
        kind, old_id, color = entry.get("targetType"), entry.get("targetId"), entry.get("color")
        key = (kind, old_id) if isinstance(kind, str) and isinstance(old_id, str) else None
        ref = refs.get(key) if key is not None else None
        if (ref is None or target_counts[key] != 1 or not isinstance(color, str)
                or not COLOR_RE.fullmatch(color)):
            _warn(report, "unresolved_object_color", cpath,
                  "Unconverted/ambiguous target, duplicate target, or invalid color; original retained.")
            continue
        data["appearance"]["objectColors"].append({"target": dict(ref), "color": color})
    target["extensions"][APPEARANCE_NAMESPACE] = {
        "version": PROFILE_VERSION, "status": "current", "dependencies": {"scope": "document"}, "data": data,
    }
    _warn(report, "appearance_precedence_not_certified", path,
          "Known colors/roles were mapped to draft appearance rules; matching every legacy renderer's visual precedence is not certified.")


def migrate_text(source_text: str, *, interpret_sample_notes: bool = False,
                 target_version: str = VERSION) -> dict:
    """Return the selected target with its source and partial-conversion report.

    No files are written. Only explicitly interpreted sample music is activated.
    The target defaults to stable 3.0.0; Draft 2 must be selected explicitly.
    """
    if not isinstance(source_text, str):
        raise MigrationError("migrate_text requires str; use migrate_bytes for UTF-8 bytes")
    _require(isinstance(target_version, str) and target_version in MIGRATION_TARGET_VERSIONS,
             "target_version", "expected stable 3.0.0 or 3.0.0-draft.2")
    try:
        source = load_strict(source_text)
        source_bytes = source_text.encode("utf-8", errors="strict")
    except (ValueError, UnicodeError) as exc:
        raise MigrationError(f"Source strict-wire check failed: {exc}") from exc
    _require(source.get("format") == "OSTF", "/format", "expected OSTF")
    _require(source.get("version") == "2.3.0", "/version", "expected declared version 2.3.0")
    _require(type(source.get("ppq")) is int and source["ppq"] == 960, "/ppq", "expected integer 960")
    for key, kind in (("song", dict), ("timeline", dict), ("harmony", dict),
                      ("melodies", list), ("lyrics", dict), ("extensions", dict)):
        _require(isinstance(source.get(key), kind), "/" + key, "missing or invalid source container")
    report = {
        "conversionMode": "interpret-sample-notes" if interpret_sample_notes else "structure-only",
        "sourceValidation": {"scope": "bounded", "fullOSTF23ConformanceChecked": False,
            "checks": ["strict UTF-8 JSON ingress", "format/version/ppq identity",
                       "required source container kinds", "recognized timeline ordering and target bounds"]},
        "completeMusicMigration": False, "assumptions": [], "archivedOnly": [],
        "warnings": [], "idMappings": [], "counts": {},
    }
    title = source["song"].get("title", "")
    if not isinstance(title, str):
        title = ""
        _warn(report, "uninterpreted_title", "/song/title", "Non-string title retained only in source archive.")
    target = {
        "format": "OSTF", "version": target_version, "ppq": 960, "song": {"title": title},
        "timeline": {}, "harmony": {"chords": [], "scales": []}, "tracks": [], "soundSlots": [],
        "lyrics": {"documents": [], "phrases": [], "units": [], "alignments": []},
        "resources": [], "extensions": {},
    }
    ids = _Ids()
    refs: dict[tuple[str, str], dict] = {}
    target["timeline"] = _transfer_timeline(source, ids, report, refs)
    if interpret_sample_notes:
        report["assumptions"].extend([
            "Explicit opt-in: sample pitch is an integer 12-TET note number with 60=C4.",
            "Explicit opt-in: note.start is clip-local ticks; note.duration is a gate/hold length.",
            "Explicit opt-in: timed harmony.symbol is display label only; no chord structure is inferred.",
            "Only sample-shaped chord/performance objects without extra fields are activated; a different dialect needs an explicit adapter.",
            "Primary melody is not inferred.",
        ])
        _interpret_music(source, target, ids, report, _original_id_counts(source), refs)
        _archive_only(report, "/harmony", "Only timed sample symbols transferred; all other harmony data remains archival.")
    else:
        _archive_only(report, "/harmony", "Opaque harmony not interpreted in structure-only mode.")
        _archive_only(report, "/melodies", "Opaque melody/note content not interpreted in structure-only mode.")
    _archive_only(report, "/lyrics", "Legacy segmentation/pronunciation/alignment semantics were not inferred.")
    _archive_only(report, "/extensions", "Original extensions archival; recognized role/color subset separately transferred.")
    for key in source:
        if key not in {"format", "version", "ppq", "song", "timeline", "harmony", "melodies", "lyrics", "extensions"}:
            _archive_only(report, "/" + key, "Unknown top-level field retained only in source archive.")
    _extra_fields(source["song"], {"title"}, "/song", report, block=False)
    _transfer_appearance(source, target, report, refs)
    appearance = target["extensions"].get(APPEARANCE_NAMESPACE, {}).get("data", {})
    report["counts"] = {
        "sections": len(target["timeline"]["sections"]),
        "tempoChanges": len(target["timeline"]["tempoChanges"]),
        "meterChanges": len(target["timeline"]["meterChanges"]),
        "chords": len(target["harmony"]["chords"]), "tracks": len(target["tracks"]),
        "clips": sum(len(track["clips"]) for track in target["tracks"]),
        "notes": sum(len(clip["notes"]) for track in target["tracks"] for clip in track["clips"]),
        "appearanceTargets": len(appearance.get("appearance", {}).get("objectColors", [])),
        "sectionRoleAssignments": len(appearance.get("sectionRoleAssignments", {})),
    }
    target["extensions"][ARCHIVE_NAMESPACE] = {
        "version": PROFILE_VERSION, "status": "unverified", "dependencies": {"scope": "document"},
        "data": {"sourceVersion": "2.3.0", "sourceSha256": hashlib.sha256(source_bytes).hexdigest(),
                 "sourceText": source_text, "conversionReport": report},
    }
    errors = [issue for issue in validate_document(target) if issue.get("severity") == "error"]
    if errors:
        detail = "; ".join(f"{issue.get('path', '')}: {issue.get('message', issue.get('code', 'error'))}"
                           for issue in errors[:5])
        raise MigrationError("Generated target failed validation: " + detail)
    return target


def migrate_bytes(source_bytes: bytes, *, interpret_sample_notes: bool = False,
                  target_version: str = VERSION) -> dict:
    """Decode strict UTF-8 without newline conversion and migrate the source."""
    if not isinstance(source_bytes, bytes):
        raise MigrationError("migrate_bytes requires bytes")
    try:
        text = source_bytes.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise MigrationError(f"Source is not strict UTF-8: {exc}") from exc
    return migrate_text(text, interpret_sample_notes=interpret_sample_notes,
                        target_version=target_version)


def _write_output(destination: Path, payload: str, *, force: bool) -> None:
    """Publish a complete sibling temporary file, preserving an existing target.

    No-force publication uses an exclusive hard link, so a competing writer's
    file is never replaced. Filesystems without that operation fail safely.
    Force uses atomic replacement. The publication step is the commit point;
    later temporary-name cleanup failure must not report an uncommitted write.
    This does not promise crash/power-loss durability or filesystem transactions.
    """
    encoded = (payload + "\n").encode("utf-8")
    temporary = None
    committed = False
    try:
        with tempfile.NamedTemporaryFile(mode="wb", dir=destination.parent,
                                         prefix=".ostf3-migrate-", delete=False) as handle:
            temporary = Path(handle.name)
            written = handle.write(encoded)
            if written != len(encoded):
                raise OSError('Incomplete temporary-file write; destination was not published.')
        if force:
            os.replace(temporary, destination)
            temporary = None
        else:
            os.link(temporary, destination)
        committed = True
    finally:
        if temporary is not None:
            try:
                temporary.unlink(missing_ok=True)
            except OSError:
                if not committed:
                    raise


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="UTF-8 source declaring OSTF 2.3.0")
    parser.add_argument("output", type=Path, help="new .ostf output path")
    parser.add_argument("--target-version", choices=MIGRATION_TARGET_VERSIONS, default=VERSION,
                        help=f"destination root version (default: {VERSION})")
    parser.add_argument("--interpret-sample-notes", action="store_true",
                        help="explicitly assume the sample pitch/local-start/gate and symbol conventions")
    parser.add_argument("--force", action="store_true", help="replace existing output, never source itself")
    parser.add_argument("--json-report", action="store_true", help="print the embedded report as JSON")
    args = parser.parse_args(argv)
    try:
        same = args.source.resolve() == args.output.resolve()
        if not same and args.source.exists() and args.output.exists():
            same = os.path.samefile(args.source, args.output)
        if same:
            raise MigrationError("Source and output must be different files, including with --force.")
        if args.output.exists() and not args.force:
            raise MigrationError("Output already exists; choose another path or explicitly use --force.")
        document = migrate_bytes(args.source.read_bytes(), interpret_sample_notes=args.interpret_sample_notes,
                                 target_version=args.target_version)
        _write_output(args.output, dump_strict(document, indent=2), force=args.force)
        report = document["extensions"][ARCHIVE_NAMESPACE]["data"]["conversionReport"]
        if args.json_report:
            print(dump_strict(report, indent=2))
        else:
            print(f"Created {args.output} ({report['conversionMode']}; partial migration).")
            print(f"Converted {report['counts']['notes']} notes; complete source text and SHA-256 archived.")
            print("Bounded source checks only; full OSTF 2.3 conformance and complete musical conversion are not claimed.")
            print(f"Inspect embedded conversionReport: {len(report['warnings'])} warnings.")
        return 0
    except (MigrationError, OSError, ValueError) as exc:
        if args.json_report:
            print(dump_strict({"status": "error", "message": str(exc)}, indent=2))
        else:
            print(f"Migration failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
