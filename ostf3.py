"""OSTF 3.0.0 and Draft 1/2 reader, validator, and core event extractor.

No document URI is fetched and no extension code is executed. Validation does
not mutate its input. Use load_strict/dump_strict for precision-preserving JSON;
ordinary json.loads cannot preserve the lexical integer/real distinction.
"""

from __future__ import annotations

from collections.abc import Iterator
from copy import deepcopy
from decimal import Decimal, InvalidOperation
from functools import lru_cache
from hashlib import sha256
import json
import math
from pathlib import Path
import re
from typing import Any

MAX = 9007199254740991
DRAFT1_VERSION = "3.0.0-draft.1"
DRAFT2_VERSION = "3.0.0-draft.2"
VERSION = "3.0.0"
SUPPORTED_VERSIONS = (DRAFT1_VERSION, DRAFT2_VERSION, VERSION)
PROFILE_VERSION = "1.0.0-draft.1"
SCHEMA_PATHS = {
    version: Path(__file__).resolve().parent / "schema" / f"ostf-{version}.schema.json"
    for version in SUPPORTED_VERSIONS
}
SCHEMA_PATH = SCHEMA_PATHS[VERSION]
RELATIVE = "org.ostf.relative-phrase.v1"
GENERATION = "org.ostf.generation-context.v1"
APPEARANCE = "org.ostf.appearance.v1"
LEGACY = "org.ostf.legacy-import.v1"
PHRASE_LIBRARY = "org.ostf.phrase-library.v1"
CLIP_CHOICES = "org.ostf.clip-choices.v1"
SUPPORTED_PROFILES_BY_VERSION = {
    DRAFT1_VERSION: {key: PROFILE_VERSION for key in (RELATIVE, GENERATION, APPEARANCE, LEGACY)},
    DRAFT2_VERSION: {key: PROFILE_VERSION for key in (RELATIVE, GENERATION, APPEARANCE, LEGACY, PHRASE_LIBRARY, CLIP_CHOICES)},
    VERSION: {key: PROFILE_VERSION for key in (RELATIVE, GENERATION, APPEARANCE, LEGACY, PHRASE_LIBRARY, CLIP_CHOICES)},
}
SUPPORTED_PROFILES = SUPPORTED_PROFILES_BY_VERSION[VERSION]
Diagnostic = dict[str, str]
_NUMBER_PATTERN = re.compile(r"-?(?:0|[1-9][0-9]*)(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\Z")


class WireError(ValueError):
    """Malformed/forbidden JSON, or an explicitly reported reader limitation."""

    def __init__(self, message: str, code: str = "WIRE_INVALID", path: str = ""):
        super().__init__(message)
        self.code, self.path = code, path

    def diagnostic(self) -> Diagnostic:
        return _diagnostic("error", self.code, self.path, str(self))


class DocumentValidationError(ValueError):
    """Semantic extraction requested on an invalid OSTF document."""

    def __init__(self, diagnostics: list[Diagnostic]):
        self.diagnostics = diagnostics
        count = sum(item["severity"] == "error" for item in diagnostics)
        super().__init__(f"Invalid OSTF document: {count} error(s)")


class JsonReal(Decimal):
    """Exact decimal value retaining the source JSON real-number token.

    Decimal('1e0') alone prints as '1'; retaining the original token avoids
    incorrectly turning an opaque real token into an integer when saving.
    """

    def __new__(cls, token: str) -> JsonReal:
        if not isinstance(token, str) or not _NUMBER_PATTERN.fullmatch(token) or not any(c in token for c in ".eE"):
            raise ValueError("JsonReal requires a JSON real-number token")
        value = super().__new__(cls, token)
        value._json_token = token
        return value

    @property
    def json_token(self) -> str:
        return self._json_token

    def __reduce__(self):
        return JsonReal, (self.json_token,)

    def __deepcopy__(self, memo):
        return JsonReal(self.json_token)


def _diagnostic(severity: str, code: str, path: str, message: str) -> Diagnostic:
    return {"severity": severity, "code": code, "path": path, "message": message}


def _ptr(parent: str, child: str | int) -> str:
    return parent + "/" + str(child).replace("~", "~0").replace("/", "~1")


def _json_issues(value: Any) -> list[Diagnostic]:
    """Inspect JSON-compatible values without altering numbers or opaque data."""
    result: list[Diagnostic] = []
    active: set[int] = set()

    def visit(node: Any, path: str) -> None:
        if isinstance(node, str):
            if any(0xD800 <= ord(char) <= 0xDFFF for char in node):
                result.append(_diagnostic("error", "WIRE_SURROGATE", path, "Unpaired Unicode surrogate is forbidden."))
        elif node is None or type(node) in (bool, int):
            return
        elif type(node) is float:
            if not math.isfinite(node):
                result.append(_diagnostic("error", "WIRE_NONFINITE", path, "JSON numbers must be finite."))
        elif isinstance(node, Decimal):
            if not node.is_finite():
                result.append(_diagnostic("error", "WIRE_NONFINITE", path, "JSON numbers must be finite."))
            elif isinstance(node, JsonReal):
                token = node.json_token
                try:
                    good = bool(_NUMBER_PATTERN.fullmatch(token)) and any(c in token for c in ".eE") and Decimal(token) == node
                except (InvalidOperation, ValueError, TypeError):
                    good = False
                if not good:
                    result.append(_diagnostic("error", "WIRE_NUMBER_TOKEN", path, "Stored numeric token does not match its value or token kind."))
        elif isinstance(node, (dict, list)):
            if id(node) in active:
                result.append(_diagnostic("error", "WIRE_CYCLE", path, "Cyclic data cannot be JSON."))
                return
            active.add(id(node))
            if isinstance(node, dict):
                for key, child in node.items():
                    if not isinstance(key, str):
                        result.append(_diagnostic("error", "WIRE_OBJECT_KEY", path, "JSON object keys must be strings."))
                        continue
                    visit(key, _ptr(path, key))
                    visit(child, _ptr(path, key))
            else:
                for index, child in enumerate(node):
                    visit(child, _ptr(path, index))
            active.remove(id(node))
        else:
            result.append(_diagnostic("error", "WIRE_TYPE", path, f"Unsupported JSON value type: {type(node).__name__}."))

    try:
        visit(value, "")
    except RecursionError:
        result.append(_diagnostic("error", "WIRE_DEPTH", "", "Nesting exceeds this reference reader's recursion limit."))
    return result


def _parse_integer(token: str) -> int:
    # Avoid Python's decimal-string conversion limit without changing global
    # interpreter settings. All core integers are range-checked afterwards.
    negative = token.startswith("-")
    digits = token[1:] if negative else token
    value = 0
    for start in range(0, len(digits), 1000):
        part = digits[start:start + 1000]
        value = value * (10 ** len(part)) + int(part)
    return -value if negative else value


def load_strict(source: bytes | str) -> dict[str, Any]:
    """Decode strict UTF-8 JSON into an object, preserving exact numeric values.

    NaN/Infinity and invalid Unicode are rejected. Real tokens use JsonReal;
    1e400 and 1e-400 remain finite and are not converted to binary64. Numbers
    exceeding Python Decimal's representational limits raise WIRE_NUMBER_RANGE,
    a reader limitation rather than a claim of mathematical JSON invalidity.
    """
    if isinstance(source, bytes):
        try:
            source = source.decode("utf-8", errors="strict")
        except UnicodeDecodeError as exc:
            raise WireError("Input is not valid UTF-8.", "WIRE_UTF8") from exc
    elif not isinstance(source, str):
        raise TypeError("load_strict expects bytes or str")
    if source.startswith("\ufeff"):
        raise WireError("A UTF-8 BOM is forbidden.", "WIRE_BOM")

    def pairs(items):
        value = {}
        for key, child in items:
            if key in value:
                raise WireError(f"Duplicate object key: {key!r}.", "WIRE_DUPLICATE_KEY")
            value[key] = child
        return value

    def invalid_constant(token):
        raise WireError(f"Non-finite JSON token {token!r} is forbidden.", "WIRE_NONFINITE")

    def exact_real(token):
        try:
            value = JsonReal(token)
            if not value.is_finite():
                raise InvalidOperation
            return value
        except (InvalidOperation, OverflowError) as exc:
            raise WireError("Number exceeds this reader's exact Decimal representation; no rounded value was accepted.", "WIRE_NUMBER_RANGE") from exc

    try:
        value = json.loads(source, object_pairs_hook=pairs, parse_int=_parse_integer,
                           parse_float=exact_real, parse_constant=invalid_constant)
    except WireError:
        raise
    except (json.JSONDecodeError, ValueError, RecursionError) as exc:
        raise WireError(f"Invalid or too deeply nested JSON: {exc}", "WIRE_JSON") from exc
    if not isinstance(value, dict):
        raise WireError("JSON root must be an object.", "WIRE_ROOT")
    issues = _json_issues(value)
    if issues:
        first = issues[0]
        raise WireError(first["message"], first["code"], first["path"])
    return value


def dump_strict(value: Any, *, indent: int | None = 2, sort_keys: bool = False) -> str:
    """Write exact JSON values and preserve integer/real token distinction.

    load_strict's real tokens are written verbatim. Plain Decimal inputs are
    treated as real tokens, even if numerically integral. This function cannot
    undo precision already lost before a caller supplied a Python float.
    """
    if indent is not None and (type(indent) is not int or indent < 0):
        raise ValueError("indent must be a nonnegative integer or None")
    issues = _json_issues(value)
    if issues:
        first = issues[0]
        raise WireError(first["message"], first["code"], first["path"])

    def render(node: Any, depth: int) -> str:
        if node is None:
            return "null"
        if type(node) is bool:
            return "true" if node else "false"
        if isinstance(node, str):
            return json.dumps(node, ensure_ascii=False)
        if isinstance(node, JsonReal):
            return node.json_token
        if isinstance(node, Decimal):
            text = str(node)
            return text if any(c in text for c in ".eE") else text + ".0"
        if type(node) is int:
            try:
                return str(node)
            except ValueError:
                return str(Decimal(node))
        if type(node) is float:
            return json.dumps(node, allow_nan=False)
        is_object = isinstance(node, dict)
        left, right = ("{", "}") if is_object else ("[", "]")
        if not node:
            return left + right
        if is_object:
            keys = sorted(node) if sort_keys else node
            colon = ":" if indent is None else ": "
            entries = [json.dumps(key, ensure_ascii=False) + colon + render(node[key], depth + 1) for key in keys]
        else:
            entries = [render(item, depth + 1) for item in node]
        if indent is None:
            return left + ",".join(entries) + right
        padding = " " * (indent * (depth + 1))
        return left + "\n" + padding + (",\n" + padding).join(entries) + "\n" + " " * (indent * depth) + right

    return render(value, 0)


@lru_cache(maxsize=len(SUPPORTED_VERSIONS))
def _schema(version: str = VERSION) -> dict:
    if version not in SCHEMA_PATHS:
        raise ValueError("Unsupported OSTF root version")
    return json.loads(SCHEMA_PATHS[version].read_text(encoding="utf-8"))


def get_schema(version: str = VERSION) -> dict:
    """Return a copy of the schema for one exact supported wire version."""
    return deepcopy(_schema(version))


@lru_cache(maxsize=len(SUPPORTED_VERSIONS))
def _validator(version: str = VERSION):
    try:
        from jsonschema import Draft202012Validator, validators
        from referencing import Registry
        from referencing.exceptions import NoSuchResource
    except ImportError as exc:
        raise RuntimeError("Install requirements.txt before validation.") from exc

    def no_remote(uri):
        raise NoSuchResource(ref=uri)

    Draft202012Validator.check_schema(_schema(version))
    checker = Draft202012Validator.TYPE_CHECKER.redefine(
        "integer", lambda _, value: type(value) is int
    ).redefine(
        "number", lambda _, value: type(value) in (int, float) or isinstance(value, Decimal)
    )
    validator_class = validators.extend(Draft202012Validator, type_checker=checker)
    return validator_class(_schema(version), registry=Registry(retrieve=no_remote))


def schema_self_check(version: str = VERSION) -> bool:
    """Check the bundled schema for an exact supported wire version."""
    _validator(version)
    return True


def _entities(doc: dict) -> Iterator[tuple[str, dict, str]]:
    for kind, items, base in (
        ("section", doc["timeline"]["sections"], "/timeline/sections"),
        ("chord", doc["harmony"]["chords"], "/harmony/chords"),
        ("scale", doc["harmony"]["scales"], "/harmony/scales"),
        ("soundSlot", doc["soundSlots"], "/soundSlots"),
        ("lyricDocument", doc["lyrics"]["documents"], "/lyrics/documents"),
        ("lyricPhrase", doc["lyrics"]["phrases"], "/lyrics/phrases"),
        ("lyricUnit", doc["lyrics"]["units"], "/lyrics/units"),
        ("lyricAlignment", doc["lyrics"]["alignments"], "/lyrics/alignments"),
        ("resource", doc["resources"], "/resources"),
    ):
        for index, item in enumerate(items):
            yield kind, item, _ptr(base, index)
    for ti, track in enumerate(doc["tracks"]):
        tp = _ptr("/tracks", ti)
        yield "track", track, tp
        for ci, clip in enumerate(track["clips"]):
            cp = _ptr(tp + "/clips", ci)
            yield "clip", clip, cp
            for ni, note in enumerate(clip["notes"]):
                yield "note", note, _ptr(cp + "/notes", ni)


def validate_document(doc: Any) -> list[Diagnostic]:
    """Return errors/warnings without mutation; paths are JSON Pointers.

    Structural errors stop semantic validation to avoid misleading cascades.
    Unknown profile versions get only common-envelope and dependency checks.
    An already parsed Python float cannot prove its source lexical token;
    integer fields therefore reject all floats, including numerically whole ones.
    """
    diagnostics = _json_issues(doc)
    if diagnostics:
        return diagnostics
    version = doc.get("version", VERSION) if isinstance(doc, dict) else VERSION
    if not isinstance(version, str) or version not in SUPPORTED_VERSIONS:
        return [_diagnostic("error", "UNSUPPORTED_VERSION", "/version", "No validator is registered for the declared OSTF root version.")]
    try:
        errors = sorted(_validator(version).iter_errors(doc), key=lambda e: (tuple(str(p) for p in e.absolute_path), e.message))
    except ValueError as exc:
        # jsonschema formats invalid numeric instances in diagnostics; Python
        # may refuse to render an integer with >4300 decimal digits. Such
        # integers remain legal opaque data, but an invalid constrained field
        # still gets a diagnostic instead of crashing the validator.
        if "integer string conversion" not in str(exc):
            raise
        return [_diagnostic("error", "SCHEMA_OVERSIZED_VALUE", "", "A constrained schema field has an oversized integer; the validator could not format its full value.")]
    for error in errors:
        path = ""
        for part in error.absolute_path:
            path = _ptr(path, part)
        diagnostics.append(_diagnostic("error", "SCHEMA_" + str(error.validator).upper(), path, error.message))
    if diagnostics:
        return diagnostics

    def add(code, path, message, severity="error"):
        diagnostics.append(_diagnostic(severity, code, path, message))

    entities: dict[str, tuple[str, dict, str]] = {}
    for kind, item, path in _entities(doc):
        ident = item["id"]
        if ident in entities:
            add("DUPLICATE_ID", path + "/id", f"ID {ident!r} already occurs at {entities[ident][2]}.")
        else:
            entities[ident] = kind, item, path
        if kind != "note" and "start" in item and "duration" in item and item["start"] + item["duration"] > MAX:
            add("TIME_OVERFLOW", path, "start + duration exceeds MAX.")
    if any(item["code"] == "DUPLICATE_ID" for item in diagnostics):
        return diagnostics  # Never resolve an ambiguous duplicate ID.

    def ref(ident, kind, path, severity="error"):
        found = entities.get(ident)
        if found is None:
            add("REFERENCE_MISSING", path, f"No {kind} with ID {ident!r} exists.", severity)
            return None
        if found[0] != kind:
            add("REFERENCE_KIND", path, f"ID {ident!r} refers to {found[0]}, not {kind}.", severity)
            return None
        return found[1]

    def check_ref(item, path, severity="error"):
        return ref(item["id"], item["type"], path, severity)

    def sorted_times(items, field, path, strict=False):
        for index in range(1, len(items)):
            previous, current = items[index - 1][field], items[index][field]
            if current < previous or (strict and current == previous):
                add("TIME_ORDER", _ptr(path, index) + "/" + field, "Times must be " + ("strictly increasing." if strict else "nondecreasing."))

    for name in ("tempoChanges", "meterChanges"):
        values = doc["timeline"][name]
        path = "/timeline/" + name
        if values[0]["at"] != 0:
            add("MAP_ORIGIN", path + "/0/at", "First entry must begin at tick 0.")
        sorted_times(values, "at", path, strict=True)
    sections = doc["timeline"]["sections"]
    sorted_times(sections, "start", "/timeline/sections")
    last_end = -1
    for index, section in sorted(enumerate(sections), key=lambda pair: pair[1]["start"]):
        if section["start"] < last_end:
            add("SECTION_OVERLAP", f"/timeline/sections/{index}", "Section placement spans must not overlap.")
        last_end = max(last_end, section["start"] + section["duration"])
    for name in ("chords", "scales"):
        values = doc["harmony"][name]
        sorted_times(values, "start", "/harmony/" + name)
        for index, context in enumerate(values):
            intervals = context.get("intervals")
            if intervals is not None and any(right <= left for left, right in zip(intervals, intervals[1:])):
                add("INTERVAL_ORDER", f"/harmony/{name}/{index}/intervals", "Intervals must be strictly ascending.")

    for ti, track in enumerate(doc["tracks"]):
        tp = f"/tracks/{ti}"
        sorted_times(track["clips"], "start", tp + "/clips")
        for ci, clip in enumerate(track["clips"]):
            cp = f"{tp}/clips/{ci}"
            sorted_times(clip["notes"], "start", cp + "/notes")
            for ni, note in enumerate(clip["notes"]):
                np = f"{cp}/notes/{ni}"
                onset = clip["start"] + note["start"]
                off = onset + note["duration"]
                if onset < 0:
                    add("NEGATIVE_ABSOLUTE_ONSET", np + "/start", "clip.start + note.start must be nonnegative.")
                if onset > MAX or off > MAX:
                    add("TIME_OVERFLOW", np, "Absolute onset or gate end exceeds MAX.")
                if "soundSlotId" in note:
                    ref(note["soundSlotId"], "soundSlot", np + "/soundSlotId")
    if "primaryMelodyTrackId" in doc["song"]:
        ref(doc["song"]["primaryMelodyTrackId"], "track", "/song/primaryMelodyTrackId")
    for index, phrase in enumerate(doc["lyrics"]["phrases"]):
        ref(phrase["documentId"], "lyricDocument", f"/lyrics/phrases/{index}/documentId")
    for index, unit in enumerate(doc["lyrics"]["units"]):
        ref(unit["phraseId"], "lyricPhrase", f"/lyrics/units/{index}/phraseId")
    for ai, alignment in enumerate(doc["lyrics"]["alignments"]):
        for field, kind in (("unitIds", "lyricUnit"), ("noteIds", "note")):
            for index, ident in enumerate(alignment[field]):
                ref(ident, kind, f"/lyrics/alignments/{ai}/{field}/{index}")

    extensions = doc["extensions"]
    supported_profiles = SUPPORTED_PROFILES_BY_VERSION[version]
    for namespace, envelope in extensions.items():
        ep = _ptr("/extensions", namespace)
        severity = "error" if envelope["status"] == "current" else "warning"
        dependency = envelope["dependencies"]
        if dependency["scope"] == "objects":
            for index, target in enumerate(dependency["refs"]):
                check_ref(target, ep + f"/dependencies/refs/{index}", severity)
        if namespace not in supported_profiles or envelope["version"] != supported_profiles[namespace]:
            add("OPAQUE_EXTENSION", ep, "Unsupported namespace/version; payload retained without interpretation.", "warning")
            continue
        data, dp = envelope["data"], ep + "/data"
        direct_refs: set[tuple[str, str]] = set()

        def pref(ident, kind, path):
            direct_refs.add((kind, ident))
            return ref(ident, kind, path, severity)

        def ptarget(target, path):
            return pref(target["id"], target["type"], path)

        if namespace == RELATIVE:
            assigned: set[str] = set()
            for index, assignment in enumerate(data["assignments"]):
                ap = dp + f"/assignments/{index}"
                if assignment["noteId"] in assigned:
                    add("DUPLICATE_ASSIGNMENT", ap + "/noteId", "A note may have only one assignment in this profile.")
                assigned.add(assignment["noteId"])
                note = pref(assignment["noteId"], "note", ap + "/noteId")
                kind = "chord" if assignment["basis"] == "chordTone" else "scale"
                context = pref(assignment["contextId"], kind, ap + "/contextId")
                if note is not None and "pitch" not in note:
                    add("RELATIVE_UNPITCHED", ap + "/noteId", "Relative assignment requires a pitched note.", severity)
                if context is None:
                    continue
                if "intervals" not in context:
                    add("RELATIVE_UNSTRUCTURED", ap + "/contextId", "Chord-tone assignment needs structured harmony; labels are not parsed.", severity)
                    continue
                pc = context["root" if kind == "chord" else "tonic"]
                natural = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}[pc["step"]]
                if assignment["anchorPitch"] % 12 != (natural + pc["alter"]) % 12:
                    add("RELATIVE_ANCHOR", ap + "/anchorPitch", "Anchor pitch class differs from context root or tonic.", severity)
                if assignment["index"] > len(context["intervals"]):
                    add("RELATIVE_INDEX", ap + "/index", "Index exceeds the context's interval list.", severity)
                    continue
                expected = assignment["anchorPitch"] + context["intervals"][assignment["index"] - 1] + assignment["chromaticOffset"]
                if not 0 <= expected <= 127:
                    add("RELATIVE_PITCH_RANGE", ap, "Resolved pitch is outside 0..127.", severity)
                elif note is not None and "pitch" in note and note["pitch"] != expected:
                    add("RELATIVE_REALIZATION", ap, f"Stored pitch {note['pitch']} differs from declared realized pitch {expected}.", severity)
        elif namespace == GENERATION:
            process_ids: set[str] = set()
            for index, process in enumerate(data["processes"]):
                pp = dp + f"/processes/{index}"
                if process["id"] in process_ids:
                    add("DUPLICATE_PROCESS_ID", pp + "/id", "Process IDs must be unique in this profile.")
                process_ids.add(process["id"])
                for ii, item in enumerate(process["inputs"]):
                    ip = pp + f"/inputs/{ii}"
                    ptarget(item["ref"], ip + "/ref")
                    if "readRange" in item and item["readRange"]["start"] + item["readRange"]["duration"] > MAX:
                        add("TIME_OVERFLOW", ip + "/readRange", "Range end exceeds MAX.")
                for oi, target in enumerate(process["outputs"]):
                    ptarget(target, pp + f"/outputs/{oi}")
                for ni, ident in enumerate(process["protectedNoteIds"]):
                    pref(ident, "note", pp + f"/protectedNoteIds/{ni}")
                if "targetRange" in process and process["targetRange"]["start"] + process["targetRange"]["duration"] > MAX:
                    add("TIME_OVERFLOW", pp + "/targetRange", "Range end exceeds MAX.")
                if "vendorExtension" in process:
                    vendor = process["vendorExtension"]
                    if vendor == namespace:
                        add("VENDOR_SELF_REFERENCE", pp + "/vendorExtension", "A generation profile cannot refer to itself.")
                    elif vendor not in extensions:
                        add("VENDOR_EXTENSION_MISSING", pp + "/vendorExtension", "Referenced vendor extension is missing.", severity)
                    if dependency["scope"] != "document":
                        add("CURRENT_DEPENDENCY_COVERAGE", ep + "/dependencies", "A process with vendorExtension requires document-scoped dependencies.", severity)
        elif namespace == APPEARANCE:
            role_ids: set[str] = set()
            for index, role in enumerate(data["roleDefinitions"]):
                if role["id"] in role_ids:
                    add("DUPLICATE_ROLE_ID", dp + f"/roleDefinitions/{index}/id", "Role IDs must be unique in this profile.")
                role_ids.add(role["id"])
            for section_id, role_id in data["sectionRoleAssignments"].items():
                path = _ptr(dp + "/sectionRoleAssignments", section_id)
                pref(section_id, "section", path)
                if role_id not in role_ids:
                    add("APPEARANCE_ROLE_MISSING", path, f"Custom role {role_id!r} is not defined.", severity)
            for role_id in data["appearance"]["customRoleColors"]:
                if role_id not in role_ids:
                    add("APPEARANCE_ROLE_MISSING", _ptr(dp + "/appearance/customRoleColors", role_id), f"Custom role {role_id!r} is not defined.", severity)
            targets: set[tuple[str, str]] = set()
            for index, item in enumerate(data["appearance"]["objectColors"]):
                path = dp + f"/appearance/objectColors/{index}/target"
                key = item["target"]["type"], item["target"]["id"]
                if key in targets:
                    add("DUPLICATE_COLOR_TARGET", path, "Object color targets must be unique.")
                targets.add(key)
                ptarget(item["target"], path)
        elif namespace == PHRASE_LIBRARY:
            templates: dict[str, dict | None] = {}
            local_notes: dict[str, dict[str, dict | None]] = {}
            for ti, template in enumerate(data["templates"]):
                tp = dp + f"/templates/{ti}"
                ident = template["id"]
                if ident in templates:
                    add("PHRASE_DUPLICATE_TEMPLATE", tp + "/id", "Template IDs must be unique within the phrase library.")
                    templates[ident] = None
                else:
                    templates[ident] = template
                indexed_notes: dict[str, dict | None] = {}
                sorted_times(template["notes"], "start", tp + "/notes")
                for ni, source_note in enumerate(template["notes"]):
                    np = tp + f"/notes/{ni}"
                    source_id = source_note["id"]
                    if source_id in indexed_notes:
                        add("PHRASE_DUPLICATE_TEMPLATE_NOTE", np + "/id", "Note IDs must be unique within each template.")
                        indexed_notes[source_id] = None
                    else:
                        indexed_notes[source_id] = source_note
                    if "soundSlotId" in source_note:
                        pref(source_note["soundSlotId"], "soundSlot", np + "/soundSlotId")
                local_notes[ident] = indexed_notes

            instance_ids: set[str] = set()
            owned_clips: set[str] = set()
            owned_notes: set[str] = set()
            for ii, instance in enumerate(data["instances"]):
                ip = dp + f"/instances/{ii}"
                if instance["id"] in instance_ids:
                    add("PHRASE_DUPLICATE_INSTANCE", ip + "/id", "Instance IDs must be unique within the phrase library.")
                instance_ids.add(instance["id"])
                if instance["clipId"] in owned_clips:
                    add("PHRASE_CLIP_OWNERSHIP", ip + "/clipId", "A Core clip can be owned by only one phrase instance.")
                owned_clips.add(instance["clipId"])
                clip = pref(instance["clipId"], "clip", ip + "/clipId")
                template = templates.get(instance["templateId"])
                if instance["templateId"] not in templates:
                    add("PHRASE_TEMPLATE_MISSING", ip + "/templateId", "Referenced local template does not exist.", severity)
                clip_note_ids = {note["id"] for note in clip["notes"]} if clip is not None else set()
                mapped_ids: set[str] = set()
                occurrences: set[tuple[int, str]] = set()

                if template is not None:
                    span = template["duration"] * instance["repeatCount"]
                    if span > MAX:
                        add("PHRASE_TIME_RANGE", ip + "/repeatCount", "Computed repeated clip duration exceeds MAX.", severity)
                    if clip is not None and clip["duration"] != span:
                        add("PHRASE_CLIP_DURATION", ip + "/clipId", "Core clip duration differs from template duration multiplied by repeatCount.", severity)
                    expected_count = len(template["notes"]) * instance["repeatCount"]
                    if len(instance["noteMap"]) != expected_count:
                        add("PHRASE_MAP_COVERAGE", ip + "/noteMap", "Map cardinality differs from template notes multiplied by repeatCount.", severity)

                # Never enumerate the Cartesian product of notes and repeats.
                # Valid keys, uniqueness, and cardinality establish completeness.
                for mi, mapping in enumerate(instance["noteMap"]):
                    mp = ip + f"/noteMap/{mi}"
                    occurrence = mapping["repeatIndex"], mapping["templateNoteId"]
                    if occurrence in occurrences:
                        add("PHRASE_DUPLICATE_OCCURRENCE", mp, "Each repeat/template-note occurrence can be mapped only once.")
                    occurrences.add(occurrence)
                    mapped_id = mapping["noteId"]
                    if mapped_id in owned_notes:
                        add("PHRASE_NOTE_OWNERSHIP", mp + "/noteId", "Each Core note can appear in only one phrase mapping.")
                    owned_notes.add(mapped_id)
                    mapped_ids.add(mapped_id)
                    note = pref(mapped_id, "note", mp + "/noteId")
                    if mapping["repeatIndex"] >= instance["repeatCount"]:
                        add("PHRASE_REPEAT_INDEX", mp + "/repeatIndex", "repeatIndex must be smaller than repeatCount.", severity)
                    if clip is not None and mapped_id not in clip_note_ids:
                        add("PHRASE_NOTE_CLIP", mp + "/noteId", "Mapped note does not belong to the instance's clip.", severity)
                    if template is None:
                        continue
                    source_notes = local_notes[instance["templateId"]]
                    if mapping["templateNoteId"] not in source_notes:
                        add("PHRASE_TEMPLATE_NOTE_MISSING", mp + "/templateNoteId", "Referenced note does not exist in the local template.", severity)
                        continue
                    source_note = source_notes[mapping["templateNoteId"]]
                    if source_note is None:
                        continue  # An intrinsic duplicate already made this ID ambiguous.
                    expected_start = mapping["repeatIndex"] * template["duration"] + source_note["start"]
                    if not -MAX <= expected_start <= MAX:
                        add("PHRASE_TIME_RANGE", mp, "Computed local note start is outside the signed Core range.", severity)
                    if clip is not None:
                        expected_onset = clip["start"] + expected_start
                        expected_off = expected_onset + source_note["duration"]
                        if expected_onset < 0 or expected_onset > MAX or expected_off > MAX:
                            add("PHRASE_TIME_RANGE", mp, "Computed absolute onset or gate end is outside Core limits.", severity)
                    if note is not None:
                        if note["start"] != expected_start:
                            add("PHRASE_NOTE_START", mp + "/noteId", "Core note start differs from the mapped occurrence.", severity)
                        if note["duration"] != source_note["duration"]:
                            add("PHRASE_NOTE_DURATION", mp + "/noteId", "Core note gate differs from its template note.", severity)
                    if "pitch" in source_note:
                        expected_pitch = source_note["pitch"] + instance["transpose"]
                        if not 0 <= expected_pitch <= 127:
                            add("PHRASE_PITCH_RANGE", mp, "Transposed template pitch is outside 0..127.", severity)
                        if note is not None and note.get("pitch") != expected_pitch:
                            add("PHRASE_NOTE_TARGET", mp + "/noteId", "Core pitch differs from the transposed template pitch.", severity)
                    elif note is not None and note.get("soundSlotId") != source_note["soundSlotId"]:
                        add("PHRASE_NOTE_TARGET", mp + "/noteId", "Core sound slot differs from the template sound slot.", severity)
                if clip is not None and mapped_ids != clip_note_ids:
                    add("PHRASE_CLIP_COVERAGE", ip + "/noteMap", "Map must cover all and only the notes in its owned Core clip.", severity)
        elif namespace == CLIP_CHOICES:
            group_ids: set[str] = set()
            managed_by: dict[str, int] = {}
            for gi, group in enumerate(data["groups"]):
                gp = dp + f"/groups/{gi}"
                if group["id"] in group_ids:
                    add("CHOICE_DUPLICATE_GROUP", gp + "/id", "Group IDs must be unique within clip choices.")
                group_ids.add(group["id"])
                candidates: dict[str, dict | None] = {}
                managed: dict[str, dict | None] = {}
                for ci, candidate in enumerate(group["candidates"]):
                    cp = gp + f"/candidates/{ci}"
                    candidate_id = candidate["id"]
                    if candidate_id in candidates:
                        add("CHOICE_DUPLICATE_CANDIDATE", cp + "/id", "Candidate IDs must be unique within each group.")
                        candidates[candidate_id] = None
                    else:
                        candidates[candidate_id] = candidate
                    for ri, clip_id in enumerate(candidate["clipIds"]):
                        rp = cp + f"/clipIds/{ri}"
                        managed[clip_id] = pref(clip_id, "clip", rp)
                        if clip_id in managed_by and managed_by[clip_id] != gi:
                            add("CHOICE_CLIP_OWNERSHIP", rp, "A clip cannot be managed by more than one choice group.")
                        else:
                            managed_by[clip_id] = gi
                selected_id = group["selectedCandidateId"]
                if selected_id is not None and selected_id not in candidates:
                    add("CHOICE_SELECTION_MISSING", gp + "/selectedCandidateId", "Selected candidate does not exist in this group.", severity)
                    continue
                if selected_id is not None and candidates[selected_id] is None:
                    continue  # Do not resolve a duplicate candidate ID by array order.
                selected = set(candidates[selected_id]["clipIds"]) if selected_id is not None else set()
                for clip_id, clip in managed.items():
                    if clip is not None and clip.get("enabled", True) != (clip_id in selected):
                        add("CHOICE_ENABLED_MISMATCH", gp + "/selectedCandidateId", f"Core clip {clip_id!r} enabled state differs from the selected candidate.", severity)
        elif namespace == LEGACY:
            digest = sha256(data["sourceText"].encode("utf-8")).hexdigest()
            if digest != data["sourceSha256"]:
                add("ARCHIVE_HASH_MISMATCH", dp + "/sourceSha256", "SHA-256 does not match UTF-8 sourceText bytes.")
            if dependency["scope"] != "document":
                add("ARCHIVE_DEPENDENCY_SCOPE", ep + "/dependencies", "The legacy archive must declare document-scoped dependencies.")
            if envelope["status"] == "current":
                add("ARCHIVE_UNVERIFIED", ep + "/status", "A legacy archive does not assert complete migration; retain unverified or stale status.")

        if direct_refs and dependency["scope"] != "document":
            declared = {(target["type"], target["id"]) for target in dependency.get("refs", [])}
            missing = sorted(direct_refs - declared)
            if missing:
                labels = ", ".join(kind + ":" + ident for kind, ident in missing)
                add("CURRENT_DEPENDENCY_COVERAGE", ep + "/dependencies", f"Dependencies omit direct profile references: {labels}.", severity)
    return diagnostics


def _require_valid(doc: dict) -> None:
    diagnostics = validate_document(doc)
    if any(item["severity"] == "error" for item in diagnostics):
        raise DocumentValidationError(diagnostics)


def _active_notes(doc: dict) -> Iterator[tuple[dict, dict, dict, int, int]]:
    for track in doc["tracks"]:
        if not track.get("enabled", True):
            continue
        for clip in track["clips"]:
            if not clip.get("enabled", True):
                continue
            for note in clip["notes"]:
                onset = clip["start"] + note["start"]
                yield track, clip, note, onset, onset + note["duration"]


def realized_events(doc: dict) -> list[dict]:
    """Extract only active stored core notes; never regenerate or truncate.

    Events contain type, tick, noteId, trackId, clipId, and pitch OR soundSlotId.
    Both on and off events carry the target. No velocity/routing is invented.
    """
    _require_valid(doc)
    result = []
    for track, clip, note, onset, off in _active_notes(doc):
        target = {"pitch": note["pitch"]} if "pitch" in note else {"soundSlotId": note["soundSlotId"]}
        common = {"noteId": note["id"], "trackId": track["id"], "clipId": clip["id"], **target}
        result.append({"type": "noteOn", "tick": onset, **common})
        result.append({"type": "noteOff", "tick": off, **common})
    return sorted(result, key=lambda item: (item["tick"], 0 if item["type"] == "noteOff" else 1, item["noteId"]))


def performance_end(doc: dict) -> int:
    """Latest active gate end or zero; placement spans do not mask events."""
    _require_valid(doc)
    return max((off for _, _, _, _, off in _active_notes(doc)), default=0)


def resolve_color(doc: dict, target: dict, default_color: str = "#808080") -> str:
    """Resolve the exact supported appearance profile's specified precedence.

    A future profile is opaque and uses the host default. Stale/unverified known
    profiles can display still-resolvable colors; no missing target is rebound.
    Invalid documents raise DocumentValidationError; an invalid target argument
    raises ValueError. Neither the document nor the color text is modified.
    """
    _require_valid(doc)
    by_key = {(kind, item["id"]): item for kind, item, _ in _entities(doc)}
    if not isinstance(target, dict) or set(target) != {"type", "id"} or not isinstance(target["type"], str) or not isinstance(target["id"], str):
        raise ValueError("target must be a Ref with type and id")
    key = (target["type"], target["id"])
    if key not in by_key:
        raise ValueError("target must resolve to the correct core kind")
    if not isinstance(default_color, str) or not re.fullmatch(r"#[0-9A-Fa-f]{6}", default_color):
        raise ValueError("default_color must be #RRGGBB")
    envelope = doc["extensions"].get(APPEARANCE)
    if not envelope or envelope["version"] != PROFILE_VERSION:
        return default_color
    data = envelope["data"]
    appearance = data["appearance"]
    object_colors = {(item["target"]["type"], item["target"]["id"]): item["color"] for item in appearance["objectColors"]}
    roles = {role["id"]: role for role in data["roleDefinitions"]}
    parents = {}
    for track in doc["tracks"]:
        for clip in track["clips"]:
            parents[("clip", clip["id"])] = ("track", track["id"])
            for note in clip["notes"]:
                parents[("note", note["id"])] = ("clip", clip["id"])

    def resolve(object_key):
        if object_key in object_colors:
            return object_colors[object_key]
        kind, ident = object_key
        item = by_key[object_key]
        if kind == "section":
            role_id = data["sectionRoleAssignments"].get(ident)
            if role_id in roles:
                if role_id in appearance["customRoleColors"]:
                    return appearance["customRoleColors"][role_id]
                base = roles[role_id].get("baseRole")
                if base in appearance["roleColors"]:
                    return appearance["roleColors"][base]
            if item.get("role") in appearance["roleColors"]:
                return appearance["roleColors"][item["role"]]
        elif kind in ("track", "soundSlot"):
            if item.get("role") in appearance["roleColors"]:
                return appearance["roleColors"][item["role"]]
        elif kind in ("clip", "note"):
            return resolve(parents[object_key])
        return default_color

    return resolve(key)


def invalidate_extensions(doc: dict, changed_refs: list[dict] | None = None) -> dict:
    """Return a copy with affected current extensions marked unverified.

    Call after a core edit, providing the changed core Ref objects; None means
    any/all core changes and [] means no core changes. This conservative helper
    does not claim to repair known profiles. Existing stale/unverified status
    and all data payloads remain untouched. Object dependencies include parent
    timing/enabled changes and container-content edits. If a deleted target's
    ancestry cannot be determined, all non-none dependencies are invalidated.
    A post-edit document may contain temporarily stale semantic references,
    but its JSON/schema structure must be valid.
    """
    wire = _json_issues(doc)
    if wire:
        raise DocumentValidationError(wire)
    version = doc.get("version", VERSION) if isinstance(doc, dict) else VERSION
    if not isinstance(version, str) or version not in SUPPORTED_VERSIONS:
        raise DocumentValidationError(validate_document(doc))
    try:
        structure_valid = _validator(version).is_valid(doc)
    except ValueError as exc:
        # Keep this helper's invalid-input contract when jsonschema cannot
        # format a very large constrained integer in its error message.
        if "integer string conversion" not in str(exc):
            raise
        raise DocumentValidationError(validate_document(doc)) from exc
    if not structure_valid:
        raise DocumentValidationError(validate_document(doc))
    known_keys = {(kind, item["id"]) for kind, item, _ in _entities(doc)}
    parents: dict[tuple[str, str], set[tuple[str, str]]] = {}
    descendants: dict[tuple[str, str], set[tuple[str, str]]] = {}
    for track in doc["tracks"]:
        tk = ("track", track["id"])
        for clip in track["clips"]:
            ck = ("clip", clip["id"])
            parents[ck] = {tk}
            descendants.setdefault(tk, set()).add(ck)
            for note in clip["notes"]:
                nk = ("note", note["id"])
                parents[nk] = {tk, ck}
                descendants.setdefault(tk, set()).add(nk)
                descendants.setdefault(ck, set()).add(nk)
    # Lyric containers have no inherited timing, but content edits may affect
    # an extension that depends on a document/phrase as a whole.
    for phrase in doc["lyrics"]["phrases"]:
        pk, dk = ("lyricPhrase", phrase["id"]), ("lyricDocument", phrase["documentId"])
        parents[pk] = {dk}
        descendants.setdefault(dk, set()).add(pk)
    for unit in doc["lyrics"]["units"]:
        uk, pk = ("lyricUnit", unit["id"]), ("lyricPhrase", unit["phraseId"])
        parents[uk] = {pk} | parents.get(pk, set())
        for parent in parents[uk]:
            descendants.setdefault(parent, set()).add(uk)
    changed = set()
    all_changed = changed_refs is None
    if changed_refs is not None:
        if not isinstance(changed_refs, list):
            raise TypeError("changed_refs must be a list of Ref objects or None")
        allowed_kinds = set(_schema(version)["$defs"]["ref"]["properties"]["type"]["enum"])
        for target in changed_refs:
            if not isinstance(target, dict) or set(target) != {"type", "id"} or not isinstance(target["type"], str) or target["type"] not in allowed_kinds or not isinstance(target["id"], str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,127}", target["id"]):
                raise ValueError("changed_refs contains an invalid Ref")
            key = (target["type"], target["id"])
            if key not in known_keys:
                all_changed = True
            changed.add(key)
            changed.update(parents.get(key, set()))
            changed.update(descendants.get(key, set()))
    result = deepcopy(doc)
    for envelope in result["extensions"].values():
        if envelope["status"] != "current":
            continue
        dependency = envelope["dependencies"]
        if dependency["scope"] == "none":
            continue
        if all_changed or (changed and dependency["scope"] == "document"):
            envelope["status"] = "unverified"
        elif dependency["scope"] == "objects" and any((target["type"], target["id"]) in changed for target in dependency["refs"]):
            envelope["status"] = "unverified"
    return result
