# Explicit composition operations for OSTF 3.0.0

This guide covers `ostf3_operations.py` and `ostf3_edit.py` for **stable Core 3.0.0**, retaining Draft 1 and Draft 2 compatibility. Phrase materialization, candidate selection, template replacement, and detachment accept both Draft 2 and stable documents. All six optional profiles retain provisional version `1.0.0-draft.1`; stable Core does not promote their versions or change their meanings. The wire contract is in the [specification](FORMAT_SPECIFICATION.en.md); the [profile guide](OPTIONAL_PROFILES.md) explains the musical relationships. Core event extraction always uses stored notes, including when profiles are omitted or stale.

The examples below document API and command syntax. The changed stable code and authored stable examples were not executed for this preparation. Historical Draft 2 Revision 1 results do not validate this update, and additional runtime verification is not a release condition.

| Intent | Operation | Phrase status required |
| --- | --- | --- |
| Add a new placement | `materialize_phrase` | Current |
| Replace one source template and update all its placements | `replace_phrase_template` | Entire phrase profile current |
| Keep existing notes but remove selected links | `detach_phrase_instances` | Current, stale, or unverified; document valid |

Ordinary reading performs none of these operations. Updating a current linked
phrase is an explicit transaction; detachment can preserve a manual edit without
claiming it still matches its source.

## 1. Shared operation contract

Every editing API accepts an already decoded document, validates it, works on a copy and validates the result. The caller's document, replacement template, and supplied ID lists are never changed. A failure returns no partial document. The CLI writes only after the entire operation and any requested protection comparison succeed.

All commands use the strict reader/writer, preserving unknown extension payloads, finite decimal values and number-token distinctions. They fetch no resources and execute no generator. `OperationError` provides `.code`, `.message` (also `str(error)`) and `.diagnostics`. Invalid documents raise `DocumentValidationError` with `.diagnostics`.

Known profiles may be `current`, `stale` or `unverified`. Structural or intrinsic identity defects are always errors. A stale relationship is not silently repaired by ordinary reading. An operation that reasserts `current` must validate the **whole profile**, including other instances or groups.

CLI output paths must differ from every input, including hard links and symbolic links. For `replace-template`, both SOURCE and the replacement JSON are protected inputs. An existing output requires `--force`; force never authorizes overwriting an input. The output writer creates the destination atomically. Exit codes are 0 for success, 1 for document/operation/protection rejection, and 2 for argument, I/O or runtime errors. `--json` emits a machine-readable report; no output file is written for `check-protection`.

The complete payload is staged before publication. Validation, operation,
protection, staging, or publication failure before commit leaves the final
destination unchanged. Publication is exclusive without force and replacement is
atomic with force. A filesystem lacking the required atomic publication fails
without a non-atomic fallback. This guarantee ends at publication; it does not
promise rollback after commit or power-loss durability.

## 2. Convert among supported root versions

```python
from ostf3_operations import convert_version, convert_draft_version

stable = convert_version(draft1)  # target_version defaults to VERSION == "3.0.0"
draft2 = convert_version(stable, "3.0.0-draft.2")
draft1_again = convert_version(stable, "3.0.0-draft.1")

# Compatibility API: target is required; both ends must be draft roots.
legacy_draft2 = convert_draft_version(draft1, "3.0.0-draft.2")
```

```sh
python ostf3_edit.py convert before.ostf stable.ostf --to-version 3.0.0 --json
python ostf3_edit.py convert stable.ostf draft2.ostf --to-version 3.0.0-draft.2 --json
python ostf3_edit.py upgrade draft1.ostf legacy-draft2.ostf --json
python ostf3_edit.py downgrade draft2.ostf legacy-draft1.ostf --json
```

`convert_version(document, target_version=VERSION)` accepts exactly
`3.0.0-draft.1`, `3.0.0-draft.2`, and `3.0.0` as source and target roots. Its
default target is stable 3.0.0. The CLI `convert` requires `--to-version` and
accepts those same three values. A no-op conversion returns a validated copy.
Core musical content and events are unchanged, and loading never changes the root.

`convert_draft_version(document, target_version)` retains its required target
argument and rejects a stable source or target. Legacy CLI `upgrade` targets
Draft 2; `downgrade` targets Draft 1. Both aliases accept draft inputs only.
`upgrade` does not mean “convert to the newest release.” Use `convert` for stable
3.0.0, including a conversion from stable to either draft.

For an extension whose exact namespace/version is unknown to either side, a
`current` claim with dependencies other than `none` becomes `unverified`. Payloads
and profile versions are preserved. Draft 1 understands the original four
profiles; Draft 2 and stable understand the same six. A current known relationship
can remain current only when both sides understand it and validation succeeds.
Stale or unverified claims are not automatically promoted. A formerly opaque
payload becoming known must pass the target structure; invalid payloads are
rejected without guessed repair or deletion.

Passing a phrase or choice payload through Draft 1 preserves its data but does
not restore its earlier `current` status on the way back. A capable editor must
recheck the relationships explicitly. Conversion among these three roots is
separate from migration from OSTF 2.3.

## 3. Materialize a finite phrase instance

```python
from ostf3_operations import materialize_phrase
result = materialize_phrase(
    document, "pickup-template",
    instance_id="placed-1", track_id="target-track", clip_id="placed-clip",
    start=120, repeat_count=2, transpose=0, enabled=True,
    max_notes=100000,
)
```

```sh
python ostf3_edit.py materialize samples/30_template_before_materialization.ostf placed.ostf --template pickup-template --instance placed-1 --track target-track --clip placed-clip --start 120 --repeat 2 --json
```

Requirements:

- Exact Draft 2 or stable 3.0.0 root and a `current` `org.ostf.phrase-library.v1` profile at the supported provisional version.
- A template and target track already exist. The new instance ID and new Core clip ID do not collide with existing objects in their respective scopes.
- `start` is a nonnegative tick, `repeat_count` is a positive integer, `transpose` is an integer from -127 through 127, and `enabled` is a boolean.
- Every computed pitch, local start, absolute onset and gate endpoint fits Core limits. Pitch is never clamped and notes are never truncated to the template period.

The operation adds one clip and one instance. Its placement duration is `template.duration * repeat_count`. For repeat index `r`, note start is `r * template.duration + templateNote.start`; gate duration is unchanged. Pitched targets receive the semitone transposition; percussion sound-slot identity stays unchanged. Track enabled state stays unchanged.

This subsection uses retained Draft 2 sample 30, which remains a supported input;
the same operation also accepts stable 3.0.0 documents. The sample template has two notes: pitch 60 at -120 for 240 ticks and pitch 64 at 720 for 480 ticks, with period 960. Placing two repeats at tick 120 produces:

| Repeat | Pitch | Absolute onset | Gate end |
| --- | ---: | ---: | ---: |
| 0 | 60 | 0 | 240 |
| 0 | 64 | 840 | 1320 |
| 1 | 60 | 960 | 1200 |
| 1 | 64 | 1800 | 2280 |

The clip span ends at 2040, while its final note ends at 2280. This tail is retained. Repeat overlap is allowed. A placement at tick 0 would put the pickup before the song origin and is rejected.

Each generated note ID is `note.` followed by the lowercase SHA-256 of the UTF-8 compact JSON array `[instanceId, repeatIndex, templateNoteId]`, using no spaces. This is the reference operation's identity policy; valid files may use any permitted unique Core IDs. A detected collision rejects the operation. Notes are sorted by local start, then repeat index, then template array order. `noteMap` is ordered by repeat index and template array order; its wire interpretation is order-independent.

`max_notes` is a reference-operation resource bound, not the format's maximum repeat count. The count is checked before allocation. An empty template does not loop over empty repetitions. Callers may choose a different explicit bound. Oversized finite requests fail before partial output is exposed.

The phrase profile's dependencies become document-scoped to include the new objects. Affected other profiles are conservatively invalidated. The complete phrase profile is certified current only after validation. Existing instances are never rebuilt by this command. Revision 1 provides the separate replacement and detachment operations in Sections 6 and 7. Automatic synchronization on load, time scaling, per-note overrides, and chord-aware fitting remain outside these operations.

## 4. Activate a set of alternative clips

```python
from ostf3_operations import activate_candidate
result = activate_candidate(
    document, "main-choice", "choice-b", protected_note_ids=()
)
silent = activate_candidate(document, "main-choice", None)
```

```sh
python ostf3_edit.py choose samples/25_choice_shared_muted.ostf chosen.ostf --group main-choice --candidate choice-b --json
python ostf3_edit.py choose samples/25_choice_shared_muted.ostf silent.ostf --group main-choice --none --json
```

The managed set is the union of every candidate's `clipIds` in the requested group. Selected clips get their own `enabled=true`; other managed clips get `enabled=false`. A null selection disables every managed clip. Parent tracks retain their own enabled state. Unmanaged clips retain their data. Shared clips within one group are permitted; ownership by two groups is invalid.

The sample keeps `bass-common` selected in both alternatives. Its parent track remains muted. `pad-a` and `pad-b` change selection, while `unmanaged-clip` is untouched. An empty candidate represents intentional silence and remains distinct from a null selection in the metadata.

Input choice status may be current, stale or unverified, but structural defects are rejected and every needed managed Core reference must resolve. After applying only the requested group, the whole profile must validate as current. If another group's mismatch remains, the operation fails without applying that group's choice as a side effect.

Changed Core clip states invalidate dependent profiles. If the selected candidate ID changes but both candidates have the same set of clips, profile metadata has still changed and non-`none` dependencies are conservatively invalidated. Repeating an already-current selection without changes preserves unrelated statuses.

Optional `protected_note_ids` is fixed by the caller before the operation. Any change to a protected note's musical snapshot rejects the operation. From the CLI, repeat `--protect-note NOTE_ID`, or use `--protect-process PROCESS_ID` to use the input document's current generation-context process. These guards run before output is written.

This operation selects **performance clips**. It does not switch chords, scales, tempo, lyric documents, song sections, plugin routing or transport state.

## 5. Compare protected notes across snapshots

```python
from ostf3_operations import check_protected_notes, check_generation_protection
report = check_protected_notes(before, after, ["melody-note-1"])
report = check_generation_protection(before, after, "process-1")
```

```sh
python ostf3_edit.py check-protection before.ostf after.ostf --note melody-note-1 --json
python ostf3_edit.py check-protection before.ostf after.ostf --process process-1 --json
```

Both documents must be valid and have the same PPQ. A PPQ mismatch returns `valid=false`, code `PROTECTION_PPQ_MISMATCH`, and an empty `checkedNoteIds`; unequal tick coordinates are not compared. The caller-supplied list must contain unique permitted IDs. Empty input is valid but explicitly checks zero IDs.

For each fixed protected ID, compare:

| Property | Compared value |
| --- | --- |
| Existence | The ID identifies a Core note in both snapshots. |
| Target | Pitch or sound-slot identity. |
| Start | Absolute onset, `clip.start + note.start`. |
| Gate | `note.duration`. |
| Effective enabled | Parent track enabled AND clip enabled, with omitted values meaning true. |

Inactive notes are also compared. A note may move to another parent or change local coordinates while retaining the same absolute onset, target, gate and effective enabled state. Such a move passes this defined protection contract. The comparator does not require byte-identical parent containers.

The returned object contains `valid`, `checkedNoteIds` and `diagnostics`. The generation wrapper additionally reports `processId` and `protectionSource="before"`. It requires the **before** document's exact known generation profile to be current and obtains protected IDs only from that snapshot. Removing the list or process in the after document cannot evade comparison.

This is a bounded before/after property comparison. It does not prove that a generator ran, establish trusted provenance, compare tempo in seconds, preserve timbre, compare acoustic release, or enforce a process's entire input/output range. A workflow needing those guarantees must define and implement additional checks. Snapshot comparison does not retroactively make an arbitrary generation-context history trustworthy.

## 6. Replace a template and refresh all linked placements

```python
from pathlib import Path
from ostf3 import load_strict
from ostf3_operations import replace_phrase_template

document = load_strict(Path("samples/31_linked_phrase_before.ostf").read_bytes())
replacement = load_strict(Path("replacement-template.json").read_bytes())
result = replace_phrase_template(
    document, "editable-template", replacement,
    protected_note_ids=(), max_notes=100000,
)
```

```sh
python ostf3_edit.py replace-template samples/31_linked_phrase_before.ostf updated.ostf --template editable-template --replacement replacement-template.json --json
```

`replacement-template.json` is one **complete template object**, not a whole OSTF
document and not a field patch. It must pass the existing template schema, and its
`id` must exactly match `editable-template`. A different ID is not an implicit
rename. Missing required members, duplicate local note IDs, undeclared fields,
invalid integer tokens, or missing referenced sound slots are rejected.

To obtain the replacement object from retained Draft 2 after-sample 32, the
preparation step below selects only its template object, which has the same
provisional profile shape. It does not copy or upgrade that sample's root. It refuses to
overwrite an existing preparation file:

```python
from pathlib import Path
from ostf3 import load_strict, dump_strict

example = load_strict(Path("samples/32_replaced_phrase_after.ostf").read_bytes())
templates = example["extensions"]["org.ostf.phrase-library.v1"]["data"]["templates"]
replacement = next(item for item in templates if item["id"] == "editable-template")
with Path("replacement-template.json").open("x", encoding="utf-8") as destination:
    destination.write(dump_strict(replacement) + "\n")
```

### Preconditions and the transaction boundary

The root must be exactly Draft 2 or stable 3.0.0, the phrase profile must have the
exact supported provisional version, and the **entire phrase profile must be current**. A valid stale document
is insufficient for replacement. Requiring current correspondence prevents an
operation from overwriting manual changes hidden behind an outdated map.

The operation updates the one template and every instance referencing it as one
transaction. It preserves each instance's ID, template ID, clip ID, repeat count,
and transpose. It preserves the parent track and the clip's ID, global start,
name, and own enabled value, as well as track mute. The clip duration and notes
follow the replacement's duration and notes using the unchanged phrase equations.
Other templates, instances, and Core clips remain as stored.

Any invalid pitch, placement span, local start, absolute onset, or gate end in any
affected instance rejects the entire update. There is no successful first
placement followed by a failed second placement in the returned document.

The resource count is:

```text
total output notes = len(replacement.notes) * sum(affected instance repeatCount)
```

`max_notes` bounds that whole output, including retained notes, before expansion.
It is not a limit on newly added notes alone or on each instance separately. The
default 100000 is an operation resource limit; the wire format has not acquired
that limit. Empty templates do not enumerate huge empty repetition loops.

### Surviving note identity

| Occurrence in the replacement | ID treatment |
| --- | --- |
| Same `(repeatIndex, templateNoteId)` as before | Keep its original mapped Core note ID exactly |
| New occurrence key | Derive the reference `note.` plus SHA-256 ID |
| Removed occurrence key | Remove that Core note, subject to lyric and protection checks |
| Source-note ID changed, with otherwise identical pitch/time | Treat as removal plus addition |

An existing custom ID is authoritative. A writer must not replace it with the hash
that the reference materializer would have generated. Source note ordering, pitch,
and timing are not identity keys.

For new occurrences, all original Core IDs remain reserved for the transaction,
including IDs of notes being removed. Newly allocated IDs are reserved too. A
collision is rejected rather than overwriting an object or giving a different
occurrence a deleted identity.

Refreshed notes are sorted by local start, repeat index, then source array index;
maps by repeat index and source array index. Pickups, tails, starts after the
period, and overlaps are retained with no trimming.

### Lyrics and protection

A removed note referenced by a Core lyric alignment causes
`OPERATION_REFERENCED_NOTE_REMOVAL`. Diagnostics identify the alignment/reference.
The operation never silently drops a lyric unit, alignment, or note reference.
An alignment to a surviving note retains the same ID. This preserves attachment;
it does not promise that the note's pitch, onset, or gate stayed unchanged.

Pass a fixed `protected_note_ids` list or tuple to protect those musical fields.
The before/after comparison in Section 5 runs before returning a result. From the
CLI, repeat `--protect-note ID`, or use `--protect-process ID` to obtain IDs only
from the source document's current generation record. These are explicit guards;
after-state changes cannot redefine their checked set.

If a lyric-attached placement should keep its existing notes while other linked
placements change, detach that instance first. Detachment preserves those Core
notes and their lyric references. It does not silently rewrite the lyric model
to make deletion possible.

### Status, no-ops, and metadata changes

Other extension payloads are preserved. Changed clips and removed note IDs are
passed to conservative dependency invalidation. When removed ancestry can no
longer be determined, invalidation can be broader than the directly edited
objects. A profile-only change also conservatively marks other non-`none` current
claims unverified.

For a nontrivial successful replacement, phrase dependencies become document-wide
and the whole phrase profile must validate as current. Existing unrelated stale
relations are not silently repaired. Unknown numeric values and token categories
remain intact.

An identical validated template returns a no-op copy, preserving statuses,
dependencies, and order; requested protection is still checked. If only `name`
changes while `duration` and `notes` are identical, Core and the existing note-map
order are preserved. The metadata change still causes the conservative status
updates just described. It is distinct from an identical-template no-op.

Both SOURCE and `--replacement` paths are protected inputs, even when `--force`
is present. Failures before publication leave the final destination unchanged,
under the shared writer boundary in Section 1. The input documents and caller's
replacement object remain unchanged on both success and failure.

## 7. Detach instance links while keeping the music

```python
from ostf3_operations import detach_phrase_instances

independent = detach_phrase_instances(
    document, ["linked-instance-a"], protected_note_ids=(),
)
```

```sh
python ostf3_edit.py detach samples/31_linked_phrase_before.ostf detached.ostf --instance linked-instance-a --json
```

Repeat `--instance ID` to detach several instances atomically. The Python argument
is a list or tuple of distinct valid instance IDs. Every requested instance must
exist. A mixed valid/missing request is rejected without removing any link. An
empty API list returns a validated no-op copy; requested protection still applies.

Detachment requires a valid Draft 2 or stable 3.0.0 document and the exact
supported provisional phrase profile, but that profile may be current, stale, or unverified. It removes only
the selected instance records. It retains every template and every Core object:
note IDs, notes, clips, timing, lyric alignments, harmony, array order, clip enabled
states, and track mute are unchanged. An edited realization need not be regenerated
to remove its stale link.

Other non-`none` current extension claims are conservatively invalidated for this
profile edit. The phrase envelope retains its **original status and dependencies**.
Removing the last inconsistency does not promote stale or unverified to current,
and declared dependencies are not automatically narrowed. A later editor must
explicitly verify correspondence before asserting current status. Detachment is
not a shortcut around the replacement operation's current-profile precondition.

The result and fixed protection set are validated before exposure. `--protect-note`
and `--protect-process` are available with the same before-only selection rules as
replacement. Missing or invalid protection requests still fail even though a
successful detach would not change Core music.

## 8. Historical evidence and remaining limits

Stable Core retains the musical semantics and explicit operations of Draft 2
Revision 1 and the release scope recorded in Revision 2. This version-alignment
update changes root dispatch, conversion entry points, and defaults. It adds no
automatic linked refresh on load, time scaling, harmony fitting, probabilistic
generation, or per-instance override layer. It does not implement a generator,
MIDI/DAW adapter, routing engine, audio comparison, or full-song scene recall.

The [consolidated conformance criteria](CONFORMANCE.md) retain 89 viewpoints. No new execution or passing result is claimed. Earlier development reports are not included in this curated release and cannot establish the stable code's behavior.

Examples [01](../samples/01_four_part_sketch.ostf), [31](../samples/31_linked_phrase_before.ostf), and [25](../samples/25_choice_shared_muted.ostf) are authored root-version copies; the [catalogue](../samples/catalog.json) records their provenance. Samples 31–33 illustrate before, replacement, and detachment states; they are not an assertion that a tool was run for this release. A specified condition, an authored example, and an executed passing test remain distinct forms of evidence.
