# Conservative migration from OSTF 2.3

This document describes `ostf3_migrate.py`, which defaults to **OSTF 3.0.0** and
also supports an explicitly selected **3.0.0-draft.2** target. It creates a new
document and archives the entire original source. It does **not** claim complete
OSTF 2.3 conformance checking, complete musical conversion, or verified
compatibility with an existing OSTF application.

The stable update changes the default output root, not the conservative
interpretation policy. Appearance and legacy archive profiles remain provisional
`1.0.0-draft.1`. The converter does not infer reusable templates or candidate
groups from legacy data. Existing Draft 1 or Draft 2 documents use the separate
`convert_version` operation to reach stable 3.0.0; the legacy
`convert_draft_version` remains restricted to the two draft roots. Reading a
file never upgrades it.

This guide specifies the adapter contract. No execution of the stable code was performed for this release preparation. Additional runtime verification is not a release condition. [LICENSE.md](../LICENSE.md) states the program and data terms; [source attribution](SOURCE_ATTRIBUTION.md) identifies the two bundled legacy source examples. Archived third-party inputs retain their applicable rights and are not relicensed merely by conversion.

The source baseline reviewed for this adapter is the upstream repository at
commit `90fce246de28a1b265fb6b25cc2866c70036fda6`, specifically its
[format specification](https://github.com/yoh-nak/Open-Song-Timeline-Format-2.3/blob/90fce246de28a1b265fb6b25cc2866c70036fda6/docs/FORMAT_SPECIFICATION.md),
[candidate schema](https://github.com/yoh-nak/Open-Song-Timeline-Format-2.3/blob/90fce246de28a1b265fb6b25cc2866c70036fda6/schema/ostf-2.3-standalone-candidate.schema.json),
and sample files. The converter does not retrieve these URLs at runtime.

## Why conversion is partial

The published 2.3 profile standardizes its envelope, selected timeline fields,
identities, and role/color references. Much of the nested Harmony, Melody, and
Lyrics content is opaque. Example files carry `pitch`, `start`, `duration`, and
`symbol`, but passing the 2.3 profile does not establish the complete musical
meaning of all additional fields.

The converter separates recognized structural data, explicitly interpreted sample
music, and an exact historical archive. The archive is **not** another playback
authority: readers must not play it, automatically reimport it, or regenerate from
it on load.

## Commands

Use Python 3.10 or later and install this package's requirements first.

```sh
python ostf3_migrate.py old_song.ostf new_song.ostf
python ostf3_migrate.py old_song.ostf interpreted_song.ostf --interpret-sample-notes
python ostf3_migrate.py old_song.ostf report_song.ostf --json-report
python ostf3_migrate.py old_song.ostf draft2_song.ostf --target-version 3.0.0-draft.2
```

`--target-version` accepts exactly `3.0.0` and `3.0.0-draft.2`, defaulting to
`3.0.0`. Draft 1 is not an output target of this adapter. Selecting a target does
not relabel its provisional profile versions or alter source interpretation.

The existing output is never overwritten by default. `--force` explicitly permits
replacing an output. The source and output must still be different files, including
resolved symlinks and existing hard links; `--force` does not authorize replacing
the source. The converter never downloads a referenced resource.

The writer prepares and closes a complete temporary file in the output directory
before publishing it. Without `--force`, an exclusive hard-link operation creates
the destination only if it is absent; with `--force`, an atomic replacement
publishes the completed file. Validation, staging, or publication failure before
commit leaves the final destination unchanged. A filesystem that cannot perform the required
publication operation fails instead of using a partial-write fallback. This
contract does not promise power-loss durability or rollback after successful
publication if a later report cannot be displayed.

Success exits with code 0, conversion/file errors with code 1, and argument usage
errors with code 2. Success means that the reported **partial target conversion**
passed validation for the selected target root, not that the source passed a
complete 2.3 test suite. This describes a successful invocation's contract; it is
not evidence that this stable update has been run.

`--json-report` prints the embedded conversion report to stdout. A failed run prints
a JSON error object in this mode. The report is also stored in the output `.ostf`.

## Default mode: structure only

Without `--interpret-sample-notes`, the converter transfers:

- A string `song.title`, if available; otherwise an empty target title.
- Section names, roles, starts, durations, and identities.
- Recognized tempo and meter maps at 960 PPQ.
- Valid recognized custom section roles, role colors, and object colors whose
  targets have actually been transferred.

The new harmony arrays, tracks, sound slots, lyric collections, and resource list
remain empty. No opaque musical or lyric interpretation is guessed. In particular,
the first legacy melody is not automatically declared the primary melody.

A structure-only output may intentionally have no playable notes. All original
musical content still exists in its original-source archive.

## Explicit sample interpretation

The `--interpret-sample-notes` option records and applies these assumptions:

| Source | Interpretation |
|---|---|
| Timed `harmony.chords[].symbol` | Display label only; no chord parsing |
| Sample-shaped `melodies[]` | Pitched part transferred to a Core track |
| Clip `start` | Global tick position |
| Clip `duration` | Placement/editing span |
| Note `pitch` | Integer 12-TET semitone number; 60 = C4 |
| Note `start` | Tick offset relative to the containing clip |
| Note `duration` | Positive integer gate/hold length |

No root, interval formula, scale, bass line, or accompaniment is generated from a
chord symbol. The symbol is retained as display text.

This is a narrow adapter for the documented example shape. Its recognized
chord and performance fields are:

- Chord: `id`, `start`, `duration`, `symbol`.
- Melody: `id`, `name`, `clips`.
- Clip: `id`, `name`, `start`, `duration`, `notes`.
- Note: `id`, `pitch`, `start`, `duration`.

If a chord or performance object has any additional fields, it is **archived without
activation**, and those fields are listed in the report. This deliberately avoids
guessing whether an unknown field controls mute, transposition, velocity, relative
pitch, or another behavior. Even a label-only chord is not activated when additional
source fields could change its harmonic meaning. An extra field on a melody
excludes that part; an extra field on a clip excludes that clip; an extra field on
a note excludes that note. A future explicit adapter may support another source
dialect.

Untimed clips, null timing, half-specified time pairs, malformed notes, and JSON
real tokens where integers are needed are not repaired with invented defaults.
Their source paths and reasons are recorded. Optional source IDs are generated or
remapped where necessary. Missing/non-string display names may receive a generic
display label; this does not infer a musical role or instrument.

Negative clip-local note starts and tails are allowed when the resulting global
onset and gate end are within the target Core bounds. Notes are not cropped to clip
boundaries, and same-pitch overlaps are not shortened or merged. Converted events
are stably sorted by start, retaining equal-start order. Required temporal
reordering is reported.

## IDs and known appearance metadata

Legacy IDs may be scoped by object kind, whereas target Core IDs are globally
unique. A valid unused Core-compatible ID is retained. Otherwise the converter
assigns a deterministic ID and records its source kind/path/ID and target kind/ID.
Colors are resolved through their **legacy kind and legacy ID**, then redirected
to the corresponding new typed reference.

Source section IDs must be nonempty and unique in this bounded converter. If an
opaque source has duplicate chord-clip or melody-clip IDs, no ambiguous color
reference is guessed. Their converted objects can have distinct new IDs, but the
unresolvable old reference remains only in the source archive with a report.

Only version `1.0.0` of `org.ostf.section-role-appearance.v1` is interpreted. It is
mapped to the **new** `org.ostf.appearance.v1`, version `1.0.0-draft.1`; the old
namespace is not redefined.

| Legacy target | Target Core kind |
|---|---|
| `section` | Converted `section` |
| `chordClip` | Converted label-only `chord`, with explicit music opt-in |
| `melodyClip` | Converted `clip`, with explicit music opt-in |

Custom-role IDs are profile-local and separately remapped when needed. Duplicate
role definitions, duplicate color targets, malformed colors, unresolved targets,
and unknown appearance versions are reported and retained in the original source.
No color is redirected to a convenient but different object.

The transferred appearance subset is marked `current` with document dependency.
The supported appearance profile's precedence applies to that subset. The converter does not
certify identical visual results across all legacy applications or their precedence
rules; the embedded report explicitly records this limitation.

## Exact original-source preservation

The output contains the following archive envelope:

```text
extensions["org.ostf.legacy-import.v1"]
  version: "1.0.0-draft.1"
  status: "unverified"
  dependencies: { scope: "document" }
  data:
    sourceVersion: "2.3.0"
    sourceSha256: SHA-256 of original UTF-8 bytes
    sourceText: complete decoded original text
    conversionReport: structured JSON object
```

The CLI reads raw bytes and decodes strict UTF-8 without newline conversion.
Re-encoding `sourceText` as UTF-8 reconstructs the original bytes, including CRLF,
indentation, original key order, escapes, and original numeric spelling. Escaping
the entire text as a string inside the new JSON does not change that string's
content.

All original lyrics, unknown fields, music, and extensions are included, whether or
not they were interpreted. High-precision original numeric tokens are preserved in
that text. The shared strict loader/dumper also preserves real numeric token kinds
and precision for transferred recognized values such as BPM.

This archive is historical evidence. Editing the new arrangement must not rewrite
it to pretend it was the original source of the revised music. Archive preservation
does not automatically create active lyric/note references or complete semantic
compatibility.

## Validation and report

Source validation is explicitly **bounded**:

- Shared strict JSON ingress: UTF-8, BOM, duplicate keys, invalid Unicode, and
  non-finite values.
- Declared `format: OSTF`, `version: 2.3.0`, and lexical integer `ppq: 960`.
- Expected source container kinds.
- Nonempty recognized 2.3 timeline collections, ordering, and target bounds.

It does not run the entire published 2.3 conformance suite or certify opaque music,
lyrics, unknown references, or legacy generator behavior. Unsupported source
timeline values are refused rather than silently clamped. The generated target is
validated before it is returned or written; target errors abort conversion.

The report fields are:

| Field | Meaning |
|---|---|
| `conversionMode` | `structure-only` or `interpret-sample-notes` |
| `sourceValidation.scope` | Always `bounded` |
| `sourceValidation.fullOSTF23ConformanceChecked` | Always `false` |
| `sourceValidation.checks` | Checks performed |
| `completeMusicMigration` | Always `false` |
| `assumptions` | Explicit sample conventions; empty in default mode |
| `archivedOnly` | Source paths and reasons not fully activated |
| `warnings` | Diagnostic objects with `code`, `path`, `message` |
| `idMappings` | Source/target identity records |
| `counts` | Counts of transferred sections/maps/chords/tracks/clips/notes/colors/assignments |

The report's `path` values identify source locations for review; no referenced
source is fetched or executed.

## Python API

```python
from ostf3_migrate import ARCHIVE_NAMESPACE, migrate_bytes, migrate_text

stable = migrate_bytes(original_bytes)
interpreted = migrate_text(original_text, interpret_sample_notes=True)
draft2 = migrate_bytes(original_bytes, target_version="3.0.0-draft.2")
report = interpreted["extensions"][ARCHIVE_NAMESPACE]["data"]["conversionReport"]
```

Both functions accept keyword-only `interpret_sample_notes=False` and
`target_version=VERSION`, where `VERSION` is `"3.0.0"`. The only accepted targets
are stable 3.0.0 and Draft 2. They return a dictionary and write no files.
`MigrationError` indicates an unsupported target or a bounded conversion that
could not complete. When starting from a file, prefer
`migrate_bytes(path.read_bytes())` to avoid newline normalization introduced by a
different text reader.

## Limits

The converter preserves the original source bytes and the explicitly transferred
subset. It does not promise complete preservation of **active** playback/editing
semantics, automatic lyric reconstruction, reversible musical downgrade after
editing, external device interoperability, or identical sound/appearance. No
Ableton Live, Max for Live, or other third-party application execution is implied
by target validation.
