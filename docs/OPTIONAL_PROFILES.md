# Provisional phrase and choice profiles for Core 3.0.0

This guide accompanies the integrated
[English specification](FORMAT_SPECIFICATION.en.md),
[Japanese specification](FORMAT_SPECIFICATION.ja.md), and
[stable Core schema](../schema/ostf-3.0.0.schema.json). It explains phrase-library
and clip-choices, introduced in Draft 2 and retained unchanged in stable Core
documents, together with their explicit editing and comparison APIs. The
[reference implementation guide](REFERENCE_IMPLEMENTATION.md) covers the reader.

All six optional profiles remain **provisional `1.0.0-draft.1`**. Stable Core
does not promote their versions or change their interpretation. The
[Draft 2 schema](../schema/ostf-3.0.0-draft.2.schema.json) and Draft 1 schema are
retained unchanged. Existing materialization, selection, whole-template
replacement/all-instance refresh, and detachment operate on Draft 2 and 3.0.0
documents. The [operation guide](OPERATIONS.md) gives exact signatures and CLI
arguments, including three-root conversion and the restricted legacy aliases.

Core remains the performance authority: the concrete notes in `tracks`, with
stored track and clip enabled states. Templates and candidate declarations do
not play a second performance. There is no Core velocity, automatic generation
on load, or automatic candidate activation.

The authored stable [linked-phrase](../samples/31_linked_phrase_before.ostf) and
[clip-choice](../samples/25_choice_shared_muted.ostf) examples change only their
predecessors' root versions. This stable preparation performs no runtime
verification and adds none as a release prerequisite. Old execution evidence
does not validate the changed stable code.

## 1. Versions and compatibility

| Document root version | Known original profiles | New phrase-library and clip-choices profiles |
|---|---|---|
| `3.0.0-draft.1` | Interpret their exact supported versions | Preserve as opaque extensions |
| `3.0.0-draft.2` | Same original versions and meanings | Interpret exact version `1.0.0-draft.1` |
| `3.0.0` | Same original versions and meanings | Same provisional version and meaning as Draft 2 |

The original relative, generation, appearance, and legacy-import profile versions
remain provisional `1.0.0-draft.1`. Phrase-library and clip-choices remain at that
same provisional version. Advancing the document root does not advance profile
versions. A profile's `current` status describes correspondence with the document,
not a stable specification release.

An unknown version of a known namespace remains opaque in Draft 2 and stable
documents alike. The common extension envelope still applies. A payload must not be
forced through a known data schema merely because its namespace is familiar.
Conversely, structural errors in an exact known version remain errors even when
the status is stale.

The reader does not upgrade documents on load. Explicit root-version conversion
keeps Core events unchanged, updates the root version, and conservatively adjusts
affected extension statuses. It can fail if opaque data becomes known at the
target root and violates that known schema. This is separate from conservative
[OSTF 2.3 migration](MIGRATION_2_3_TO_3_0.md).

## 2. Phrase library

Namespace: `org.ostf.phrase-library.v1`.

The profile stores reusable concrete source notes and their complete correspondence
to already materialized Core clips. A template can have several instances. An
instance owns one clip, and each occurrence has one mapped Core note ID.

### 2.1 Records and identity scopes

| Record | Required fields | Optional fields | Identity scope |
|---|---|---|---|
| Data | `templates`, `instances` | None | Not an entity |
| Template | `id`, `duration`, `notes` | `name` | Template IDs unique in this profile |
| Template note | `id`, `start`, `duration`, exactly one of `pitch`/`soundSlotId` | None | Note IDs unique within that template |
| Instance | `id`, `templateId`, `clipId`, `repeatCount`, `transpose`, `noteMap` | None | Instance IDs unique in this profile |
| Mapping | `templateNoteId`, `repeatIndex`, `noteId` | None | One key per `(repeatIndex, templateNoteId)` in its instance |

All IDs use the established ASCII ID syntax. Local template and instance IDs have
separate scopes and are not Core references. Template notes must not be added to
the Core identity index. Only their `soundSlotId`, the instance's `clipId`, and
mapped `noteId` values directly reference Core.

`duration` on a template is its positive integer **repeat period**, in the
document's PPQ. Template notes use signed local starts and positive gate durations.
They are sorted by nondecreasing start. A template may be empty. Its duration does
not clip its notes.

`repeatCount` is an integer from 1 through `MAX`; `transpose` is an integer from
-127 through 127; `repeatIndex` is a zero-based integer. In a current instance,
every index must be below `repeatCount`.

### 2.2 One example with a pickup and final tail

The following is one complete extension envelope. It is an excerpt from a
document, not a standalone `.ostf` root. A matching Core clip is shown below it.
The names used for Core notes are deliberately readable; the format accepts any
valid unique IDs, while the reference materializer uses the deterministic hashed
IDs described in Section 4.

```json
{
  "version": "1.0.0-draft.1",
  "status": "current",
  "dependencies": { "scope": "document" },
  "data": {
    "templates": [
      {
        "id": "short-phrase",
        "name": "Pickup and tail",
        "duration": 960,
        "notes": [
          { "id": "pickup", "pitch": 60, "start": -120, "duration": 240 },
          { "id": "tail", "pitch": 67, "start": 840, "duration": 240 }
        ]
      }
    ],
    "instances": [
      {
        "id": "phrase-a",
        "templateId": "short-phrase",
        "clipId": "clip-a",
        "repeatCount": 2,
        "transpose": 2,
        "noteMap": [
          { "templateNoteId": "pickup", "repeatIndex": 0, "noteId": "pickup-0" },
          { "templateNoteId": "tail", "repeatIndex": 0, "noteId": "tail-0" },
          { "templateNoteId": "pickup", "repeatIndex": 1, "noteId": "pickup-1" },
          { "templateNoteId": "tail", "repeatIndex": 1, "noteId": "tail-1" }
        ]
      }
    ]
  }
}
```

This clip belongs in a Core track:

```json
{
  "id": "clip-a",
  "start": 960,
  "duration": 1920,
  "enabled": true,
  "notes": [
    { "id": "pickup-0", "pitch": 62, "start": -120, "duration": 240 },
    { "id": "tail-0", "pitch": 69, "start": 840, "duration": 240 },
    { "id": "pickup-1", "pitch": 62, "start": 840, "duration": 240 },
    { "id": "tail-1", "pitch": 69, "start": 1800, "duration": 240 }
  ]
}
```

| Occurrence | Absolute onset | Absolute gate end |
|---|---:|---:|
| First pickup | 840 | 1080 |
| First tail | 1800 | 2040 |
| Second pickup | 1800 | 2040 |
| Second tail | 2760 | 3000 |

The clip reference span ends at `960 + 1920 = 2880`, but the final gate ends at
3000. The pickup is valid because its absolute onset is nonnegative. With this
template and `clip.start: 0`, the first pickup would be invalid; no rule silently
omits it. Each repetition includes every source note, even if the note begins
before or after that repetition's reference period.

### 2.3 Exact correspondence

For each occurrence, the current profile asserts:

```text
clip.duration = template.duration * repeatCount
Core note.start = repeatIndex * template.duration + source note.start
Core note.duration = source note.duration
Core pitch = source pitch + transpose
Core soundSlotId = source soundSlotId
```

Transposition applies to pitched notes only. It does not alter a percussion slot,
its output hint, or its role. Pitches must remain in 0–127; they are not wrapped
or clamped. Products, local positions, and global note endpoints must satisfy the
Core limits.

The mapping must cover every source-note/repetition pair exactly once and every
note in the target clip exactly once. A mapped note must belong to that clip.
Additional unmapped embellishments make the exact current correspondence false.
An author can use another template, explicitly update the correspondence, or mark
the profile stale; there is no hidden override mechanism in this version.

Template-note identity and repetition index remain independent of pitch, timing,
and array position. A stored mapping preserves the Core identity across a change
that keeps the same occurrence. Revision 1 provides explicit whole-template
replacement and refresh of all linked instances, using the original map to retain
surviving Core IDs. It also provides detachment for independent editing. Neither
operation runs automatically on load.

### 2.4 What schema checks, and what semantics checks

For example, the actual `phraseNoteMapping` definition in the canonical schema is:

```json
{
  "type": "object",
  "properties": {
    "templateNoteId": { "$ref": "#/$defs/id" },
    "repeatIndex": { "$ref": "#/$defs/nonnegative" },
    "noteId": { "$ref": "#/$defs/id" }
  },
  "required": ["templateNoteId", "repeatIndex", "noteId"],
  "additionalProperties": false
}
```

The local references in this excerpt resolve within the complete canonical schema;
the excerpt is not a separate schema document. Its shape check cannot establish
the referenced template, clip membership, complete occurrence coverage, or the
correspondence equations. Those require semantic validation.

A validator need not generate all expected occurrences. It can compare
`len(template.notes) * repeatCount` with the actual map length, then check each
supplied key, uniqueness, parent membership, and arithmetic. Valid keys plus
uniqueness and equal cardinality establish complete coverage. This keeps a huge
declared repeat count from causing implicit expansion during validation.

### 2.5 Status and dependencies

The entire envelope has one status. A mismatch in one instance cannot be hidden
by claiming that only that instance is stale while the envelope remains current.

| Condition | Current | Stale or unverified |
|---|---|---|
| Missing template, Core clip, note, or sound-slot reference | Error | Warning; retain data |
| Missing or excessive occurrence/clip-note coverage | Error | Warning; retain data |
| Target, timing, duration, pitch, or computed-range mismatch | Error | Warning; retain data |
| Duplicate template/instance ID, duplicate local note ID, duplicate occurrence, reused mapped Core note ID, or competing clip ownership | Error | Error |
| Known structural error or invalid Core data | Error | Error |

All referenced template sound slots, instance clips, and mapped Core notes count
toward dependency coverage. Document scope is a straightforward choice. A library
without Core dependencies may use `none`. Relative-note assignments and generation
records remain separate: if they are also current, their relationships must agree
with the same adopted Core notes.

## 3. Clip choices

Namespace: `org.ostf.clip-choices.v1`.

A candidate names clips already stored in Core. A group defines mutually exclusive
choices among candidate clip sets; a set may span bass, melody, accompaniment, and
percussion tracks. It does not create clips or relocate them.

```json
{
  "version": "1.0.0-draft.1",
  "status": "current",
  "dependencies": { "scope": "document" },
  "data": {
    "groups": [
      {
        "id": "chorus-arrangement",
        "name": "Chorus alternatives",
        "selectedCandidateId": "a",
        "candidates": [
          { "id": "a", "clipIds": ["bass-a", "keys-a", "drums-shared"] },
          { "id": "b", "clipIds": ["bass-b", "keys-b", "drums-shared"] },
          { "id": "silence", "clipIds": [] }
        ]
      }
    ]
  }
}
```

For this current selection, the clips named `bass-a`, `keys-a`, and `drums-shared`
have their own enabled flag true; `bass-b` and `keys-b` have it false. The shared
drum clip is one Core clip and plays once. Selecting `b` changes the managed clip
flags as a group. Selecting the named empty candidate or selecting `null` disables
the entire managed set; the former records a named choice, whereas the latter
records that no candidate is selected.

### 3.1 Ownership and parent mute

The managed set is derived from the union of every candidate's clip list. There is
no second managed-set field to keep synchronized. All references count, including
unselected candidates.

Group IDs are unique within the profile. Candidate IDs are unique within one
group and may be reused in another group. A candidate clip list preserves order
and contains no duplicates. A clip may be shared by candidates in one group but
cannot be controlled by two groups. These identity and ownership conflicts fail
in every status.

Current consistency compares each clip's **own** enabled flag, defaulting to true.
It does not compare the track-and-clip effective flag. Muting a parent track
therefore does not hide an incorrectly enabled unselected candidate, and choosing
a candidate does not unmute a track. Static clips outside the managed set remain
unchanged. Distinct clips may overlap in time, including their pickups and tails;
time overlap alone does not imply competing ownership.

The selected ID must name a candidate in the same group or be explicit null. The
schema uses the following member definition:

```json
{
  "selectedCandidateId": {
    "anyOf": [
      { "$ref": "#/$defs/id" },
      { "type": "null" }
    ]
  }
}
```

This is an excerpt from the group's `properties`. Group membership, reference
resolution, and enabled-state agreement are semantic checks, not consequences of
this type declaration.

Missing local selections, missing Core clips, and enabled-state mismatches are
current errors and stale/unverified warnings. A reader preserves the actual Core
flags rather than applying a stale declaration on load.

### 3.2 Boundary of a choice

This is a performance-clip choice profile, not a whole-song scene format. It does
not switch harmony, song sections, lyric documents, routing, sound devices, or
transport state. In particular, Core harmony has no enabled field. Storing two
chord progressions does not make this profile select one of them.

Alternatives that need exclusive multi-part switching belong in one group. Two
groups controlling distinct clips may coexist even on the same track or time
range; whether that layering is musically desired is not inferred by the format.

## 4. Explicit operation APIs

The operations are provided by `ostf3_operations.py`. They return new documents
or comparison results and never mutate caller inputs. Document operations
validate before and after, refuse unsupported versions, and produce no partial
document on failure. Invalid documents raise `DocumentValidationError`;
`OperationError` exposes an operation error code and message. Unknown payload
values, real-number token categories, precision, and array order survive copying
and strict serialization.

### 4.1 Explicit root-version conversion

```python
convert_version(document, target_version=VERSION)
convert_draft_version(document, target_version)
```

`convert_version` supports source and target roots `3.0.0-draft.1`,
`3.0.0-draft.2`, and `3.0.0`, with stable `VERSION = "3.0.0"` as its default
target. Core content and events stay identical. The operation changes the root
and marks a current extension unverified if it is unknown to either side and
depends on more than `none`. Profiles understood on both sides keep their
meanings and versions. Stale or unverified claims are not promoted. Moving an
opaque payload into a known schema can cause atomic rejection; no guessed repair
occurs.

The compatibility API `convert_draft_version` still requires a target and permits
only Draft 1 or Draft 2 on both sides. CLI
`convert SOURCE OUTPUT --to-version VERSION` supports all three roots and requires
the target option. Legacy
`upgrade` still targets Draft 2 and `downgrade` still targets Draft 1; both reject
stable inputs. Stable conversion uses `convert`, not a redefined legacy alias.

### 4.2 Materialize a new phrase instance

```python
materialize_phrase(
    doc, template_id,
    instance_id=instance_id,
    track_id=track_id,
    clip_id=clip_id,
    start=start,
    repeat_count=1,
    transpose=0,
    enabled=True,
    max_notes=100000,
)
```

This operation requires Draft 2 or stable 3.0.0 and an exact current phrase-library profile. It
adds a new Core clip and instance under an existing track. It refuses existing
clip IDs, instance IDs, and any Core ID collision. A count above `max_notes` is
rejected before occurrence expansion. This limit belongs to the reference
operation, not to the wire format.

The reference note ID is `note.` plus the lowercase SHA-256 of UTF-8 compact JSON
`[instance_id, repeatIndex, templateNoteId]`. Existing collisions are rejected.
The Core note array is sorted by `(start, repeatIndex, template array index)`;
the map array by `(repeatIndex, template array index)`. An empty template can
create an empty clip. Parent track mute is preserved.

Affected other extensions are conservatively invalidated. The complete updated
phrase profile must validate before it is marked current. This creation operation
does not overwrite or refresh an existing instance, fit notes to harmony, or
change source templates. Revision 1 uses a separate explicit replacement operation
for existing linked placements, described in Section 4.5.

### 4.3 Activate a candidate atomically

```python
activate_candidate(doc, group_id, candidate_id, protected_note_ids=())
```

This operation requires Draft 2 or stable 3.0.0 and the exact supported choice profile. Pass
`None` to select no candidate. A structurally valid known choice profile may
start current, stale, or unverified, but required managed references must resolve.
The operation changes only the chosen group's selected ID and managed clip enabled
flags, apart from necessary extension-status updates. Parent mute and unmanaged
objects are preserved.

The whole choice profile must validate as current afterward. If another group is
still inconsistent, the operation fails; it does not silently activate that other
group to repair it. Repeating an already-current identical selection MUST NOT
invalidate unrelated extensions. If supplied, the protected ID list is fixed
before activation and checked after it. A failed check yields no partially edited
document.

### 4.4 File writes

The editing CLI follows the conservative migration tool's write policy. Existing
destinations require `--force`, and input files may not be replaced through their
own path, a hard link, or a symbolic link. Replacement protects both the source
document and its separate template JSON file. Complete output is staged before
publication; a validation, operation, protection, staging, or publication failure
before commit leaves the final destination unchanged. The API itself writes no
files. See the operation guide or CLI help for exact command arguments.

### 4.5 Replace a template and refresh all its instances

```python
replace_phrase_template(
    document, template_id, replacement,
    protected_note_ids=(), max_notes=100000,
)
```

This operation requires a valid Draft 2 or stable 3.0.0 document and an exact
supported phrase profile whose whole status is current. It refuses to overwrite a stale
realization. `replacement` is a complete template under the existing schema, with
the same ID as the existing target, not a partial patch or a rename request.

The template and all its linked instances update atomically. Instance identity,
clip identity, repeat count, transpose, global placement, clip name, and clip and
track enabled states are preserved. Clip duration and note values are recomputed
with the existing equations. Unrelated templates, instances, and Core clips remain
as stored.

For each surviving `(repeatIndex, templateNoteId)`, use the Core ID from the
original valid note map, including custom IDs produced by other writers. Only new
occurrences receive the deterministic reference hash ID. All original Core IDs,
including removed IDs, remain reserved during this transaction. Source-note
renaming is removal plus addition; matching pitch or timing is not an identity
substitute.

`max_notes` limits total resulting notes across every affected instance, before
expansion. Empty templates do not require iterating empty repetitions. An invalid
pitch or timing in one instance rejects the entire update. The output uses the
same stable note/map ordering as materialization and preserves pickups, tails,
late starts, and overlaps.

Deleting a note still referenced by Core lyrics fails with
`OPERATION_REFERENCED_NOTE_REMOVAL`. The operation does not silently remove lyric
units, alignments, or references. References to surviving notes retain their IDs;
optional fixed protection additionally checks musical fields before/after.

Other extension payloads remain intact, with conservative status invalidation.
Deletion can broaden invalidation because a removed object's ancestry is no
longer available. A nontrivial profile-only change also invalidates other
non-`none` current claims. The updated phrase profile uses document dependencies
and must validate completely before the result is returned; supplied protection
must also pass.

An identical validated replacement preserves dependencies, statuses, and ordering
as a no-op copy; requested protection still runs. If only `name` changes while
duration and notes stay identical, Core and existing note-map order are preserved,
but metadata-related status updates still occur. These behaviors require no new
profile field or schema.

### 4.6 Detach links without changing Core

```python
detach_phrase_instances(document, instance_ids, protected_note_ids=())
```

The ID list or tuple must be duplicate-free and every selected instance must
exist. A mixed existing/missing request fails atomically. An empty list is a
validated no-op copy with requested protection checked.

The exact known phrase profile may be current, stale, or unverified, provided the
input document is valid and has a Draft 2 or stable 3.0.0 root. Remove only selected instance records. Preserve all
templates and all Core data, including notes, IDs, timing, lyrics, harmony, array
order, clip enabled flags, and parent mute. This makes it possible to keep a manual
edit when its relationship to the source has become stale.

Other non-`none` current extension claims are conservatively invalidated for the
profile edit, but the phrase profile retains its original status and dependencies.
Removing a mismatch does not certify remaining relationships as current. A stale
detach therefore does not automatically satisfy replacement's current-profile
precondition. No Core objects or lyric references are deleted, and fixed
protection is checked before a result is returned.

## 5. Protection compares fixed snapshots

### 5.1 Direct comparison

```python
check_protected_notes(before, after, note_ids)
```

The supplied ID list is fixed and duplicate-free. Both documents must validate.
The result contains `valid`, `checkedNoteIds`, and `diagnostics`. The checked
set is visible even when it is empty.

For every identified note, including inactive notes, compare:

| Field or relationship | Protection rule |
|---|---|
| Note identity | The same note ID must exist before and after |
| Target | Pitch or sound-slot identity must remain the same |
| Absolute onset | Compare `clip.start + note.start` |
| Gate | Duration and resulting absolute gate end must remain the same |
| Effective enabled state | Compare track enabled AND clip enabled, with defaults |
| PPQ | Must be identical; otherwise report `PROTECTION_PPQ_MISMATCH` and `valid: false` |

A replacement note with a new ID is not the same protected note, even if it has
the same pitch and timing. Two sound slots with the same MIDI output hint are
still distinct targets.

Conversely, a parent clip can move while the note's local start changes by the
opposite amount. If global onset, gate, target, identity, and effective enabled
remain identical, the defined protection is preserved. Parent track/clip identity
and local-coordinate representation are not themselves protected fields.

Inactive notes are not skipped: changing their pitch or gate is a protected edit
even while they remain silent. Effective enabled state is the comparison target;
individual parent flags may differ while their combined effective state remains
the same.

### 5.2 Generation-record comparison

```python
check_generation_protection(before, after, process_id)
```

The source list comes only from the specified process in **before's** exact
supported, current generation-context profile. The process must be uniquely
identified. The operation then delegates to the fixed-ID comparison.

Editing or deleting the after-document's process or protection list cannot make
a protected note disappear from the check. Taking the list from after would allow
a destructive edit to redefine what was protected and is therefore not the
contract.

### 5.3 What a successful comparison establishes

It establishes equality of the specified fields in two supplied, valid snapshots.
It does not prove that a generator ran, that an engine used a particular seed, or
that the snapshots describe a true historical operation.

The contract is in musical ticks. A tempo change can alter elapsed seconds while
these fields still match; tempo is not compared as part of note protection. A
different track instrument, routing, resource content, synthesizer release,
sound-slot mapping, or external effect can change audio without changing the
protected fields. No timbre or audio equivalence is claimed.

## 6. Intentional exclusions and next decisions

The retained explicit operations provide replacement and linked refresh. They do
not synchronize on load. It does not define nested templates, time scaling,
probabilistic playback, harmonic fitting, a per-instance override layer, or a
common interpretation of proprietary generator settings. Relative-pitch meaning
and generation provenance remain separate profiles.

It does not define full-song scene recall, harmony or lyric candidate selection,
real-time launch quantization, routing, audio tracks, MIDI rendering, or DAW/device
execution. Candidate clips must already be materialized and valid in Core.

The inherited 2.3 converter still performs bounded source checks, preserves exact
original source, and requires explicit sample-note interpretation. It defaults
to stable 3.0.0, with an explicitly selectable Draft 2 target. The ability to
represent a phrase or lyric relationship does not justify inventing that
relationship from an opaque legacy payload.

The [consolidated conformance contract](CONFORMANCE.md) includes all 89 retained viewpoints. The [sample catalogue](../samples/catalog.json) and [coverage map](COVERAGE.md) identify authored examples. Criteria and coverage counts are not runtime passes, and format/API documentation does not imply external application interoperability. No runtime verification was performed while creating this distribution.
