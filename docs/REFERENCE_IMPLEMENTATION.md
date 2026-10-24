# Python reference implementation

This guide describes the Python reader, validator, event extractor, and editing
helpers in the **OSTF Core 3.0.0** technical distribution. All six supported
optional profiles remain provisional at exact version **1.0.0-draft.1**. The
[format specification](FORMAT_SPECIFICATION.en.md) and
[stable Core schema](../schema/ostf-3.0.0.schema.json) define the format.

The reader accepts exactly `3.0.0-draft.1`, `3.0.0-draft.2`, and `3.0.0`.
It selects the matching bundled schema and profile registry without changing
the input version. The [Draft 1 schema](../schema/ostf-3.0.0-draft.1.schema.json)
and [Draft 2 schema](../schema/ostf-3.0.0-draft.2.schema.json) are retained
unchanged. Other root versions produce `UNSUPPORTED_VERSION`; this differs from
opaque fallback for an unsupported optional profile version.

The stable implementation adds exact stable-version dispatch, general explicit conversion, and a stable migration default while preserving the existing musical contract. This release documentation uses the same five reference source files as preparation revision 1. No project code was imported or executed while preparing this distribution. [LICENSE.md](../LICENSE.md) covers the reference programs under MIT; [release readiness](RELEASE_READINESS.md) records the packaging scope.

The reader uses stored Core notes as the authoritative performance. The separate
[operation module](OPERATIONS.md) explicitly materializes stored templates,
replaces a current template and all linked placements, detaches selected links,
selects clip alternatives, and compares protected notes across snapshots. These
phrase and choice operations accept Draft 2 and stable documents. Neither module
runs a composition algorithm, synthesizes audio, or writes MIDI. Loading never
invokes those editing operations.

`replace_phrase_template` keeps original-map IDs for surviving occurrences and
refuses lyric-reference breakage. `detach_phrase_instances` preserves all Core
data and retains the phrase envelope's previous status. The
[operation guide](OPERATIONS.md) defines complete signatures, atomic rejection
behavior, fixed protection checks, and resource limits. The existing safeguards
are unchanged.

For a first implementation, start with the bilingual [Core-only quickstart](IMPLEMENTER_QUICKSTART.md) and examples 04/03. The [complete manual](COMPLETE_MANUAL.en.md) and [parameter reference](PARAMETER_REFERENCE.en.md) explain the full format. Core-only export capability and the reference validator's broader exact-profile checks are separate claims.

## 1. Installation and usage examples

Use Python 3.10 or later. From the package root, install the declared dependency
in the Python environment you intend to use. These are usage examples, not steps
executed for this release or additional publication prerequisites:

```sh
python -m pip install -r requirements.txt
python ostf3_validate.py --schema-check
python ostf3_validate.py --schema-check --schema-version 3.0.0-draft.1
python ostf3_validate.py --schema-check --schema-version 3.0.0-draft.2
python ostf3_validate.py --json --events samples/01_four_part_sketch.ostf
```

The checked-in [requirements file](../requirements.txt) pins
`jsonschema==4.23.0`. It does not pin every transitive dependency. The recorded
Draft 2 Revision 1 acceptance run used Python 3.12.14 and jsonschema 4.23.0.
That historical environment does not establish that the changed stable code has
run there. The declared minimum Python version is not a claim that every supported
Python version was tested.

Keep `ostf3.py` and its `schema/` directory together. Schema resolution is local.
The reader does not retrieve resource URLs found in a document, and it does not
execute extension payloads.

## 2. The three validation layers

Full validation requires all three layers below.

| Layer | Entry point | What it establishes |
| --- | --- | --- |
| Strict JSON and lexical rules | `load_strict`, then in-memory checks in `validate_document` | UTF-8, one object root, unique object keys, valid Unicode, finite numbers, and retention of integer versus real-number token kinds |
| Document structure | The bundled JSON Schema through `validate_document` | Required fields, allowed properties, types, ranges, and the exact supported profiles' payload structures |
| Document semantics | `validate_document` | Identity, references, timeline order, endpoint arithmetic, known profile relationships, dependency coverage, and archive integrity |

A general JSON Schema validator alone does not establish OSTF conformance. For
example, a general validator may accept `1.0` as an integer because its numeric
value is whole. OSTF integer fields require an integer JSON token. This reference
implementation uses a stricter type checker: only a Python value whose exact
type is `int` satisfies an integer field. `True`, `1.0`, `Decimal("1")`, and a
parsed `1e0` do not.

Duplicate object keys and an original numeric token cannot reliably be recovered
after a permissive parser has discarded them. Use `load_strict` at the input
boundary, rather than parsing with ordinary `json.loads` and then assuming that
`validate_document` can reconstruct the source.

## 3. A complete read, validate, and save example

```python
from pathlib import Path

from ostf3 import (
    DocumentValidationError,
    WireError,
    dump_strict,
    load_strict,
    performance_end,
    realized_events,
    validate_document,
)

source = Path("samples/01_four_part_sketch.ostf")

try:
    document = load_strict(source.read_bytes())
except WireError as exc:
    print(exc.diagnostic())
    raise

diagnostics = validate_document(document)
for diagnostic in diagnostics:
    print(diagnostic)

if any(item["severity"] == "error" for item in diagnostics):
    raise DocumentValidationError(diagnostics)

events = realized_events(document)
end_tick = performance_end(document)
print(f"{len(events)} events; performance end {end_tick} ticks")

# Choose a distinct destination when retaining the input file is required.
Path("sketch-copy.ostf").write_text(
    dump_strict(document) + "\n", encoding="utf-8"
)
```

`load_strict` checks the JSON representation; it does not perform full OSTF
validation. `dump_strict` likewise checks that its input can be written as strict
JSON, not that it is a valid OSTF document. Validate an edited document before
publishing it as conforming OSTF.

Warnings alone do not make a document invalid. Extraction functions validate
their input again and reject documents containing errors, rather than returning
a partial performance.

## 4. Public Python API

All functions below leave input documents unchanged. Functions returning derived
objects return new objects. None writes an input file; file writing in the
example above is an explicit caller operation. Validation reads the bundled
schema and caches the validator internally.

| API | Return value | Relevant failure behavior |
| --- | --- | --- |
| `load_strict(source: bytes \| str)` | A parsed document object | `WireError` for rejected JSON or an explicitly reported reader limit; `TypeError` for an unsupported argument type |
| `dump_strict(value, *, indent=2, sort_keys=False)` | A JSON string | `WireError` for an unsupported JSON value tree; `ValueError` for an invalid indentation argument |
| `validate_document(doc)` | A list of diagnostic dictionaries | Invalid documents normally produce diagnostics; missing dependencies or a damaged installation are tool failures, not document diagnostics |
| `realized_events(doc)` | A sorted list of active Core note events | `DocumentValidationError` if any validation error exists |
| `performance_end(doc)` | The latest active gate end, or `0` | `DocumentValidationError` if any validation error exists |
| `resolve_color(doc, target, default_color="#808080")` | A `#RRGGBB` string | `DocumentValidationError` for an invalid document; `ValueError` for an invalid target or default color |
| `invalidate_extensions(doc, changed_refs=None)` | A deep copy with affected `current` extensions marked `unverified` | `DocumentValidationError` for invalid JSON/schema structure; `TypeError` or `ValueError` for an invalid `changed_refs` argument |
| `get_schema(version=VERSION)` | A deep copy of the selected bundled schema | An unsupported version raises `ValueError`; installation or file-access failures can propagate |
| `schema_self_check(version=VERSION)` | `True` after checking the selected schema and constructing its validator | Raises on an unsupported version, schema, or dependency failure |

`VERSION` is `"3.0.0"`, and `SCHEMA_PATH` points to the stable schema.
`DRAFT1_VERSION` is `"3.0.0-draft.1"`; `DRAFT2_VERSION` is
`"3.0.0-draft.2"`. `SUPPORTED_VERSIONS` and `SCHEMA_PATHS` identify all three
exact alternatives. `get_schema()` and `schema_self_check()` default to stable
through `VERSION`, while explicit old-version arguments retain old selection.
`SUPPORTED_PROFILES_BY_VERSION` is the root-specific registry;
`SUPPORTED_PROFILES` names the stable registry for compatibility. `PROFILE_VERSION`
remains provisional `"1.0.0-draft.1"` for all six supported namespaces. Loading
or validating never upgrades a document.

Version-changing APIs live in the separate operation module:

| API | Version contract |
| --- | --- |
| `convert_version(document, target_version=VERSION)` | Converts among all three roots; defaults to stable 3.0.0 |
| `convert_draft_version(document, target_version)` | Compatibility API; target remains required and both ends must be Draft 1 or Draft 2 |

CLI `convert SOURCE OUTPUT --to-version VERSION` supports all three targets and
requires the option. Legacy `upgrade` targets Draft 2, and `downgrade` targets
Draft 1; both accept draft inputs only and reject stable inputs. Conversion keeps
Core data/events and profile versions, applying conservative status changes for
profiles unknown on either side. It does not silently promote stale claims.

The separate [2.3 migration adapter](MIGRATION_2_3_TO_3_0.md) has keyword
`target_version=VERSION` on both `migrate_bytes` and `migrate_text`, and CLI
`--target-version`. It defaults to stable and accepts Draft 2 as an explicit
alternative; it does not target Draft 1.

These are not catch-all process boundaries. Resource exhaustion and other
runtime or installation failures are not promises of a normal invalid-document
result.

### Exceptions and diagnostics

`WireError` and `DocumentValidationError` both subclass `ValueError`.

- `WireError` exposes `code`, `path`, and `diagnostic()`.
- `DocumentValidationError` exposes the complete `diagnostics` list used to
  reject the operation.

Each diagnostic has four fields:

```json
{
  "severity": "error",
  "code": "REFERENCE_MISSING",
  "path": "/lyrics/alignments/0/noteIds/0",
  "message": "A description of the unresolved reference."
}
```

This is an illustrative diagnostic shape, not a captured error message. `path`
uses JSON Pointer syntax, with the empty string denoting the root. `severity`
is `error` or `warning`. Consumers should use the fields rather than match
English message wording or assume a fixed diagnostic order.

| Category | Representative codes | Interpretation |
| --- | --- | --- |
| JSON input | `WIRE_UTF8`, `WIRE_BOM`, `WIRE_DUPLICATE_KEY`, `WIRE_JSON`, `WIRE_ROOT`, `WIRE_SURROGATE`, `WIRE_NONFINITE` | The wire input violates the accepted JSON representation |
| In-memory JSON values | `WIRE_CYCLE`, `WIRE_OBJECT_KEY`, `WIRE_TYPE`, `WIRE_NUMBER_TOKEN` | A caller supplied an invalid JSON tree or inconsistent retained numeric token |
| Reader limits | `WIRE_NUMBER_RANGE`, `WIRE_DEPTH` | This implementation cannot represent or traverse the input within its runtime limits; this is distinct from a mathematical claim that a finite JSON number is invalid |
| Schema | `SCHEMA_TYPE`, `SCHEMA_REQUIRED`, `SCHEMA_ADDITIONALPROPERTIES`, `SCHEMA_ENUM`, `SCHEMA_OVERSIZED_VALUE` | Document structure or a constrained field is invalid |
| Root-version dispatch | `UNSUPPORTED_VERSION` | The declared Core wire version has no registered validator |
| Core semantics | `DUPLICATE_ID`, `REFERENCE_MISSING`, `REFERENCE_KIND`, `TIME_ORDER`, `TIME_OVERFLOW`, `MAP_ORIGIN`, `SECTION_OVERLAP`, `NEGATIVE_ABSOLUTE_ONSET` | Stored Core relationships or timing violate the selected Core version |
| Supported profile semantics | `RELATIVE_REALIZATION`, `CURRENT_DEPENDENCY_COVERAGE`, `APPEARANCE_ROLE_MISSING`, `VENDOR_EXTENSION_MISSING` | A supported profile's relationship needs attention; severity can depend on status |
| Phrase library | `PHRASE_DUPLICATE_OCCURRENCE`, `PHRASE_CLIP_OWNERSHIP`, `PHRASE_MAP_COVERAGE`, `PHRASE_NOTE_TARGET`, `PHRASE_TIME_RANGE` | Local identities, ownership, mapping, or a saved realization violates the phrase contract |
| Clip choices | `CHOICE_DUPLICATE_GROUP`, `CHOICE_CLIP_OWNERSHIP`, `CHOICE_SELECTION_MISSING`, `CHOICE_ENABLED_MISMATCH` | Choice identities, management scope, selection, or saved enabled state violates the choice contract |
| Opaque fallback | `OPAQUE_EXTENSION` | A namespace or exact profile version is unsupported; its payload remains opaque |
| Legacy archive | `ARCHIVE_HASH_MISMATCH`, `ARCHIVE_DEPENDENCY_SCOPE`, `ARCHIVE_UNVERIFIED` | The supported archive envelope or preserved source fails its archive rules |
| CLI environment | `TOOL_ERROR` | A file or runtime dependency could not be used |

Schema codes normally use `SCHEMA_` followed by the uppercase JSON Schema keyword.
For example, `additionalProperties` produces `SCHEMA_ADDITIONALPROPERTIES`.
`SCHEMA_OVERSIZED_VALUE` is a fallback when the schema library cannot format an
extremely large invalid constrained integer in an error message.

Validation stops before semantic checks when structural errors are present. It
also avoids resolving references through ambiguous duplicate Core IDs. Fixing
one layer can therefore reveal additional diagnostics on a later pass.

## 5. Exact numbers and strict serialization

`load_strict` retains JSON integer tokens as Python integers and real-number
tokens as `JsonReal`, a subclass of `decimal.Decimal`. `JsonReal` carries the
original real-number token in its `json_token` property.

```python
from ostf3 import dump_strict, load_strict

value = load_strict(
    '{"integer":1,"exponent":1e0,"precise":0.123456789012345678901,'
    '"large":1e400,"small":1e-400}'
)

assert type(value["integer"]) is int
assert value["exponent"].json_token == "1e0"
saved = dump_strict(value, indent=None)
```

The values `1e400` and `1e-400` remain finite exact decimals. The reader does not
first convert them to binary64, so binary64 overflow or underflow is not a reason
to reject or silently alter them. They can be preserved in opaque payloads even
when they would be outside a particular Core field's allowed range.

Serialization follows these rules:

- A `JsonReal` is written using its retained real-number token, including an
  exponent spelling such as `1e0`.
- An ordinary finite `Decimal` is written as a real-number token. If necessary,
  `.0` is appended so a numerically integral decimal does not become an integer
  token.
- Integers retain their exact numeric value, including large integers in opaque
  data. Core integer fields are independently restricted by their schema ranges.
- Finite Python floats can be written, but the serializer cannot recover
  precision already lost before they were supplied.
- Object insertion order is retained unless `sort_keys=True`; array order is
  retained. Whitespace and other JSON spelling can change.

Use `dump_strict` for a document loaded by `load_strict`. Ordinary `json.dumps`
does not directly support these decimal values, and converting them to floats
or strings would change their meaning or JSON type. Retention is of JSON values
and numeric token kind, not the original file bytes. The legacy migration
archive has a separate source-text preservation rule.

`JsonReal("1e0")` is also available to callers that deliberately need to create a
real-number token with a chosen spelling. Preserve opaque values without
incidental arithmetic or type coercion. Decimal arithmetic can use a caller's
rounding context and need not retain a `JsonReal`'s original token.

### Numeric and nesting limits

Core tick endpoints and checked time sums must stay within
`0..9007199254740991`; individual signed local positions and other integer
fields have their own schema ranges. All event timing calculations use integers.
The declared PPQ must satisfy the schema and is used directly. The implementation
does not silently normalize a document to the recommended PPQ of 960.

The integer parser avoids Python's usual decimal-string conversion digit limit
without changing global interpreter settings. This is not a promise of
unbounded memory or processing capacity. Decimal construction still has the
runtime's representational limits. A real-number token that exceeds those
limits is rejected with `WIRE_NUMBER_RANGE`; it is never accepted as a rounded,
infinite, or zero substitute.

Nesting is limited by the Python runtime and the recursive parser, traversal,
and serializer. Parsing or traversal can report `WIRE_JSON` or `WIRE_DEPTH` when
the limit is reached. There is no fixed, cross-platform depth limit promised by
this reference implementation. The implementation limits do not add a new numeric
range or nesting rule to the OSTF format itself.

## 6. Stored performance extraction

For each note in an enabled clip on an enabled track, the extractor computes:

```text
onset = clip.start + note.start
gate_end = onset + note.duration
```

Omitted track and clip `enabled` values mean `true`. A note's `duration` is its
gate length. Clip and section placement boundaries do not truncate notes or
restrict their onsets. Valid pickups, tails, and overlapping notes are retained.

Each note produces two events:

```json
{
  "type": "noteOn",
  "tick": 0,
  "noteId": "example-note",
  "trackId": "example-track",
  "clipId": "example-clip",
  "pitch": 60
}
```

The corresponding `noteOff` carries the same identities and target. For an
unpitched note, `soundSlotId` replaces `pitch` in both events. No velocity,
channel, instrument routing, or sound mapping is invented.

Events are sorted by absolute tick, then with `noteOff` before `noteOn`, then by
ASCII `noteId`. Same-pitch overlaps retain their independent note identities.
The extractor does not sort or modify the stored note arrays. These are abstract
OSTF events, not a MIDI byte stream; an exporter must make its own explicit
decisions about a destination's capabilities.

`performance_end` returns the greatest active gate end, or zero when there are no
active notes. It does not return the end of the last clip or section. A valid
harmony-only or lyrics-only document can consequently have a performance end of
zero.

## 7. Exact profile versions and opaque fallback

The implementation recognizes these namespaces only at the exact profile version
`1.0.0-draft.1`, which remains provisional. The first four apply to all three
supported root versions; the final two are interpreted in Draft 2 and stable:

| Namespace | Implemented interpretation |
| --- | --- |
| `org.ostf.relative-phrase.v1` | Validates saved relative assignments against structured harmony and stored Core pitch |
| `org.ostf.generation-context.v1` | Validates generation context, references, ranges, protection references, and dependency declarations |
| `org.ostf.appearance.v1` | Validates appearance data and resolves colors |
| `org.ostf.legacy-import.v1` | Validates the preserved source archive's integrity and envelope rules |
| `org.ostf.phrase-library.v1` | Validates finite template/instance mappings against saved Core notes; never materializes on load |
| `org.ostf.clip-choices.v1` | Validates candidate groups and their correspondence to clip enabled states; never activates on load |

The two new namespaces remain opaque in a Draft 1 document, including at their
known profile version. This keeps Draft 1's structural and semantic interpretation
aligned. Their names are also exposed as `PHRASE_LIBRARY` and `CLIP_CHOICES`.

Phrase validation checks the supplied map entries, their unique occurrence keys,
and their cardinality; it never expands every repeat to establish completeness.
An instance's map must match its entire owned Core clip when current. Clip-choice
validation compares each managed clip's own `enabled` value with the selected
candidate; a parent track's mute is independent. Local identity ambiguity and
ownership conflicts are errors in every status. Unresolved references or saved
realization/state mismatches follow the current-versus-stale severity rule below.

A future version of a familiar namespace is treated like any other unsupported
profile: its common envelope and declared dependencies are checked, its `data`
is preserved as opaque JSON, and an `OPAQUE_EXTENSION` warning is emitted. Its
payload is not validated against the current version's shape, even if its status
is `current`. Stored Core notes remain available for extraction.

Status does not excuse invalid JSON or malformed supported payload structure.
For supported relationship checks, a broken `current` relationship is normally
an error; the corresponding unresolved or mismatched relationship in `stale` or
`unverified` information is a warning. Core references remain errors regardless
of any extension's status.

A current supported profile with direct Core references must declare document-wide
dependencies or list every such reference in its object dependencies. Profile-local
IDs are not Core dependency references. With no Core dependency, `none` is allowed
unless the individual profile requires document scope. A current generation
process referring to a vendor extension requires document-wide dependencies.
Missing coverage is reported as `CURRENT_DEPENDENCY_COVERAGE`, with
status-dependent severity.

The supported legacy archive has an additional rule: it is a preservation
record, not a second current performance model. Its dependencies must be
document-wide, its source-text hash must match, and its status cannot be
`current`. The reader does not replay or musically reinterpret its source text.

## 8. Color resolution

```python
from ostf3 import resolve_color

color = resolve_color(document, {"type": "note", "id": "lead-c4"})
```

For the supplied four-part sketch this note inherits `#A358D1`. The helper first
validates the document and requires the target to resolve to the stated Core
kind. Its precedence follows the supported appearance profile:

| Target | Precedence, from first choice to fallback |
| --- | --- |
| Section | Own object color; assigned custom role color; that role's base-role color; Core section-role color; host default |
| Track or sound slot | Own object color; Core role color; host default |
| Clip | Own object color; resolved parent track color |
| Note | Own object color; resolved parent clip color |
| Other Core object | Own object color; host default |

The default is `#808080` unless supplied by the caller. Color text is returned
without case normalization. A section overlapping a note in time does not
automatically color that note.

Still-resolvable colors in a supported `stale` or `unverified` appearance profile
can be displayed. Missing references are not rebound to other objects. An
unsupported appearance version remains opaque and uses the host default.

## 9. Invalidating dependencies after an edit

Call `invalidate_extensions` after editing Core data and before treating an old
profile relationship as current. Supply the changed Core references when their
scope is known:

```python
from ostf3 import invalidate_extensions, validate_document

# post_edit_document is a structurally valid document edited by the caller.
updated = invalidate_extensions(
    post_edit_document,
    [{"type": "clip", "id": changed_clip_id}],
)
diagnostics = validate_document(updated)
```

The helper accepts a document whose supported relationships may have become
semantically stale after the edit, but its JSON and schema structure must still
be valid. It returns a deep copy and changes affected `current` statuses to
`unverified`. It preserves payloads and existing `stale` or `unverified` statuses.

| Argument or dependency | Behavior |
| --- | --- |
| `changed_refs=None` | Treat any or all Core data as changed; invalidate all current extensions whose scope is not `none` |
| `changed_refs=[]` | Declare that no Core data changed |
| A list of changed Core references | Invalidate matching object dependencies and document-wide dependencies, including relevant parents and descendants |
| A deleted reference whose ancestry is unavailable | Conservatively invalidate all non-`none` current dependencies |
| `dependencies.scope == "none"` | Leave status unchanged |

Use `None` for an edit whose full scope is uncertain, for a broad Core change,
and for root-level time-model edits such as PPQ, tempo-map, or meter-map changes.
Those settings do not have an entity `Ref`; inventing one would understate the
edit's effect.

Container relationships matter. Changing a clip's timing or enabled state can
affect a profile depending on its notes; editing a note can affect a profile
depending on its enclosing clip or track. The helper includes these relationships
conservatively. It may invalidate more information than a fully informed editor
would need to invalidate.

This function does not discover edits, repair a relative phrase, recompute
generation results, or prove that an opaque vendor's dependency declaration is
complete. The caller must supply an accurate change scope and validate the
result. Marking a profile unverified does not fix a broken Core reference or
other Core error.

### Protection comparison and its boundary

The generation-context profile records protected notes and the validator checks
their references. Draft 2 adds `check_protected_notes` and
`check_generation_protection` in the separate operation module. They compare
fixed before-snapshot IDs for target, absolute onset, gate and effective enabled
state at equal PPQ. A real regeneration engine must additionally implement its
generation algorithm, input/output scope and any required provenance checks.
Snapshot comparison does not establish that a particular algorithm ran, or that
tempo in seconds, timbre and acoustic release remained equivalent. See the
[operation guide](OPERATIONS.md) for the exact comparison and failure contract.

## 10. Validation CLI

```sh
python ostf3_validate.py sketch.ostf
python ostf3_validate.py --json --events sketch.ostf
python ostf3_validate.py --schema-check --json sketch.ostf another.ostf
python ostf3_validate.py --warnings-as-errors --json sketch.ostf
python ostf3_validate.py - < sketch.ostf
```

| Argument or flag | Meaning |
| --- | --- |
| One or more file paths | Validate each file independently |
| `-` | Read UTF-8 bytes from standard input; usable at most once |
| `--json` | Write one machine-readable report to standard output |
| `--events` | Include each valid file's sorted active Core events |
| `--schema-check` | Check the bundled schema; can be used without a document |
| `--schema-version VERSION` | Select exactly `3.0.0`, `3.0.0-draft.2`, or `3.0.0-draft.1` for `--schema-check`; defaults to stable 3.0.0 and requires that flag |
| `--warnings-as-errors` | Fail the command when warnings occur, without changing their severity or document validity |

At least one input or `--schema-check` is required. The CLI reads files and writes
its report to standard output; it does not rewrite documents.

The JSON report contains `formatVersion`, `supportedFormatVersions`, a `files`
array, aggregate `valid`, and `commandPassed`. The top-level `formatVersion`
identifies the newest wire version supported by this distribution. Each parsed
file with a string version has its own `formatVersion`, reporting its actual
input version; it is never rewritten to the newest version. Each file record
also has `file`, `valid`, and `diagnostics`. Valid records have `performanceEnd`,
and have `events` when requested. `schemaValid` and `schemaVersion` appear when
`--schema-check` is used. A schema-check tool failure can also produce a
top-level `toolError`.

`valid` and `commandPassed` answer different questions:

- `valid` reports whether the checked documents and, if requested, the schema
  have validity errors. Warnings do not make it false.
- `commandPassed` reports whether the invocation meets the selected command
  policy and completed successfully.

For example, a valid document containing an opaque extension can have
`valid: true` and `commandPassed: false` under `--warnings-as-errors`. Its
`OPAQUE_EXTENSION` diagnostic remains a warning. Without that flag the same
warning does not fail the command.

| Exit code | Meaning |
| --- | --- |
| `0` | Validation passed, and the selected warning policy passed |
| `1` | At least one wire/document validation error, or a warning rejected by `--warnings-as-errors` |
| `2` | Command usage, file I/O, runtime dependency, or schema-check failure |

For multiple inputs, a tool failure takes precedence over a validity/policy
failure. Argument-parser usage failures are printed by the command parser and
need not have the JSON report shape. Files that are invalid do not receive a
partial event extraction.

## 11. Release evidence and sample scope

This package contains authored samples, complete documentation, schemas, and reference source. No runtime, validator, CLI, import, schema-check, test-suite, DAW, MIDI, or clean-extraction execution was performed for its preparation. The [conformance contract](CONFORMANCE.md) describes required behavior without marking it as passed. [Coverage](COVERAGE.md) is a static documentation inventory.

Historical execution reports from Draft 2 Revision 1 remain in earlier development packages and are not evidence for the current stable source. They are not bundled in this release-focused set. The [four-part](../samples/01_four_part_sketch.ostf), [linked-phrase](../samples/31_linked_phrase_before.ostf), and [clip-choice](../samples/25_choice_shared_muted.ostf) examples are authored data, with source relationships recorded in the [catalogue](../samples/catalog.json).

## Implementation sources

- [Reader, validator, extractor, and helpers](../ostf3.py)
- [Validation CLI](../ostf3_validate.py)
- [Explicit operations API](../ostf3_operations.py) and [CLI](../ostf3_edit.py)
- [Operation guide](OPERATIONS.md)
- [Pinned direct dependency](../requirements.txt)
- [Stable 3.0.0 JSON Schema](../schema/ostf-3.0.0.schema.json)
- [Preserved Draft 2 JSON Schema](../schema/ostf-3.0.0-draft.2.schema.json)
- [Preserved Draft 1 JSON Schema](../schema/ostf-3.0.0-draft.1.schema.json)
