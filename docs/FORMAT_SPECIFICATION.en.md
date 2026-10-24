# OSTF 3.0.0 — Format Specification

Specification work began on 24 October 2026. Core wire version: `3.0.0`.
Status: initial stable Core specification, with six provisional optional profiles
at their existing exact version `1.0.0-draft.1`.

**This is the stable Core 3.0.0 specification; the optional profiles remain provisional.** [LICENSE.md](../LICENSE.md) defines the release terms and [release readiness](RELEASE_READINESS.md) records the distribution scope. No runtime verification was performed while preparing this package. Earlier Draft results are not passing evidence for 3.0.0.

This is the English implementer edition of the
[Japanese specification](FORMAT_SPECIFICATION.ja.md). Its structural definitions
are provided by the [3.0.0 JSON Schema](../schema/ostf-3.0.0.schema.json). The
[Draft 1 schema](../schema/ostf-3.0.0-draft.1.schema.json) and
[Draft 2 schema](../schema/ostf-3.0.0-draft.2.schema.json) are retained unchanged.
Read the prose and schema together: JSON Schema alone does not express every
wire-format, ordering, identity, timing, or reference requirement.

OSTF 3.0 exchanges song structure, harmony, lyrics, and the performance currently
adopted by the author. A performance note contains a pitch or percussion target,
an onset position, and a gate duration. **Core does not define velocity.**

The requirements below are normative for Core 3.0.0 and for implementations
claiming the exact provisional profile or operation support described here.
Existing Core fields, limits, and performance meanings are the initial stable
baseline. A profile's `current` status describes correspondence with a saved
document, not the maturity of its specification. Later profile versions must not
be silently interpreted as the same version. Conformance concerns structure,
time, references, and supported optional profiles; it does not certify musical
quality, identical timbre, or operation in an existing product.

3.0.0 retains the musical meanings of Draft 2 Revision 2 and adds a stable root
and schema. Reusable concrete phrases, performance-clip choices, whole-template
replacement with refresh of all linked instances, detachment, and protection
comparisons remain explicit operations. Reading performs no automatic generation
or synchronization. The reference implementation retains both draft roots, adds
explicit conversion among all three roots, and defaults 2.3 migration to 3.0.0.

The [four-part example 01](../samples/01_four_part_sketch.ostf), [linked-phrase example 31](../samples/31_linked_phrase_before.ostf), and [clip-choice example 25](../samples/25_choice_shared_muted.ostf) are among 60 complete 3.0.0 examples. Two additional legacy source files are explicitly separated under `samples/legacy_2_3`. The [sample index](../samples/INDEX.md), [catalogue](../samples/catalog.json), and [coverage inventory](COVERAGE.md) identify their scope and provenance. Authored examples are not executed conversion outputs or passing tests.

**MUST** and **MUST NOT** indicate requirements. **SHOULD** indicates a recommended choice from which an implementation may depart for a justified reason. A required field must be present; an optional field may be absent. Optional does not imply that `null` is accepted. The schema defines permitted value types.

First implementers can start with the bilingual [quickstart](IMPLEMENTER_QUICKSTART.md), [complete manual](COMPLETE_MANUAL.en.md), and [parameter reference](PARAMETER_REFERENCE.en.md). [Melody example 04](../samples/04_melody_only.ostf) and [harmony example 03](../samples/03_harmony_only.ostf) use Core without optional profiles. These informative guides do not add fields or change normative requirements.

## 1. Scope and three layers

| Layer | Content | Reader behavior |
|---|---|---|
| Core | Song information, timeline, harmony, adopted notes, lyrics, percussion targets, and resource references | Interpret the current song content |
| Standard optional profiles | Relative-note relationships, generation inputs, protected notes, appearance, reusable phrases, and clip choices | Interpret additional meaning when the profile and version are supported |
| Vendor extensions | Algorithm-specific settings, presets, models, and other proprietary information | Preserve unsupported data without guessing its meaning |

Core MUST contain the concrete notes of the finite arrangement currently adopted
by the author. When relative phrases, repetition, transposition, or probabilistic
choices affect that performance, their adopted results MUST be reflected in Core.
A reader MUST NOT run generation automatically on load, reroll a saved random
choice, or play both a candidate representation and its adopted Core notes.

Incomplete documents are valid. A document may contain only harmony, only a
melody, or only lyrics, while still supplying the required empty containers and
timeline maps. Completion of all musical layers is not required. A document with
no notes must not be represented as containing a completed note performance.

Core excludes velocity, MIDI CC, pitch bend, instrument and effect state, audio
track playback, indefinitely running generation, and complete score engraving.
Future features may be considered as optional profiles that preserve Core meaning.

## 2. File and top-level structure

### 2.1 Strict JSON input

The file extension is `.ostf`. A file MUST contain one UTF-8 JSON object. A reader
MUST reject a byte-order mark, invalid UTF-8, duplicate keys within an object,
unpaired Unicode surrogates, `NaN`, `Infinity`, mathematically non-finite numbers,
and additional non-whitespace content after the root object.

Fields specified as Core integers MUST use JSON integer tokens. `1` is valid;
`1.0`, `1e0`, and `true` are not valid representations of an integer field.
Implementations MUST check this input rule in addition to ordinary JSON Schema
integer validation. Supported profile fields defined as integers likewise retain
their declared integer requirements.

### 2.2 Required root members

| Member | Type and meaning |
|---|---|
| `format` | Exact string `OSTF` |
| `version` | Exact string `3.0.0` |
| `ppq` | Integer ticks per quarter note, from 1 through 960000 |
| `song` | Song information object |
| `timeline` | Object containing `sections`, `tempoChanges`, and `meterChanges` |
| `harmony` | Object containing `chords` and `scales` |
| `tracks` | Array of tracks |
| `soundSlots` | Array of percussion targets |
| `lyrics` | Object containing `documents`, `phrases`, `units`, and `alignments` |
| `resources` | Array of resource references, such as generation source material |
| `extensions` | Object of namespaced extension envelopes |

The reference reader dispatches on the exact root version, supporting
`3.0.0-draft.1`, `3.0.0-draft.2`, and `3.0.0` with their respective schemas and
profile sets. Other root versions are unsupported and are rejected. Reading MUST
NOT rewrite the version. Draft 1 interprets only relative, generation, appearance,
and legacy-import. Draft 2 and 3.0.0 interpret those four plus phrase-library and
clip-choices, with identical profile meanings. The latter two remain opaque in a
Draft 1 document even when their shape is recognizable. All six profile versions
remain provisional `1.0.0-draft.1`, independently of stable Core status. Schema
retrieval and the schema-check option default to 3.0.0; each older schema remains
explicitly selectable.

Core objects are closed: an implementation MUST NOT accept undeclared members as
Core fields. Additional information belongs in `extensions`. For example, a
misspelled `duration` or an undeclared `velocity` on a note is an error, not an
implicitly supported field.

Arrays may generally be empty. `tempoChanges` and `meterChanges` are exceptions:
each MUST contain an entry at tick 0. Object key order has no meaning. Array order
MUST be preserved, subject to the specific temporal ordering requirements below.

### 2.3 Numeric preservation

A finite decimal JSON value MUST NOT be rejected as malformed solely because its
conversion to binary64 overflows or underflows. For example, opaque extension
values `1e400` and `1e-400` are finite decimal values. Their numeric value and their
real-token category must be preserved. Core integers remain subject to the
field-specific bounds and the common limit in Section 3.

If an input exceeds a reference implementation's numeric representation limits,
that condition must be reported as an implementation support limit, not as a JSON
grammar violation.

A reader/writer claiming lossless preservation of unknown extensions MUST also
preserve the precision of numbers in JSON values it does not understand. It MUST
NOT silently change an integer token into a real token or vice versa. Parsing all
numbers into ordinary floating-point values and printing them again is not, by
itself, a lossless strategy. Preserve original numeric tokens or sufficient
precision and verify the result of writing them back. Byte-for-byte preservation
of JSON whitespace and object key order is a separate requirement.

## 3. Time, identity, and references

### 3.1 One timebase

All Core objects and standard profiles in this specification use the document's `ppq`.
The recommended value is 960, but readers MUST honor the declared value. There is
no per-track PPQ and no implicit multiplier.

The common absolute integer limit is:

```text
MAX = 9007199254740991
```

Time positions, durations, and computed end positions MUST remain within their
specified bounds. Unsigned positions are at least 0. Durations are at least 1.
Signed note-local positions range from `-MAX` through `MAX`; their resulting
absolute positions are checked separately.

A meter change does not alter the meaning of a tick. An implementation converting
to another PPQ MUST disclose any timing loss caused by rounding. At PPQ 960, a
quarter note cannot be divided into seven equal integer tick durations; a suitable
PPQ such as 6720 can represent that division exactly.

### 3.2 Stable IDs

A Core `id` is an ASCII string of 1 to 128 characters. It begins with a letter or
digit and then contains only letters, digits, `.`, `_`, `:`, or `-`:

```text
^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$
```

IDs MUST be unique across **all Core object kinds in one document**. Display names,
array indices, and track positions are not identities. Moving an object SHOULD
retain its ID. An independent copy MUST have a distinct ID. IDs local to an
extension use the uniqueness scope defined by that profile; they do not become
Core IDs merely because they have the same spelling.

### 3.3 Typed references

A `Ref` has exactly `type` and `id`. Its `type` is one of:

```text
section, track, clip, note, chord, scale, soundSlot,
lyricDocument, lyricPhrase, lyricUnit, lyricAlignment, resource
```

A Core reference MUST resolve to the correct object kind. Finding the same string
under a different kind does not satisfy the reference. An implementation MUST NOT
recursively scan opaque extension `data` and register coincidental `id` members as
Core objects.

### 3.4 Ranges

Where a `Range` is used, it has exactly `start` and `duration` on the global song
timeline. `start` is a nonnegative integer, `duration` is a positive integer, and
`start + duration` MUST be at most `MAX`. Checking the two operands separately is
not sufficient.

## 4. Song information and timeline

### 4.1 `song`

`title` is a required string. It may be empty for an unnamed song.
`primaryMelodyTrackId` is optional and, when present, MUST identify an existing
track. It designates the primary melody; it does not produce an additional
performance event.

### 4.2 `timeline`

| Array | Required members of each element | Optional members |
|---|---|---|
| `sections` | `id`, nonempty `name`, `start`, `duration` | `role` |
| `tempoChanges` | `at`, `bpm` | None |
| `meterChanges` | `at`, `numerator`, `denominator` | None |

Sections MUST be ordered by start and MUST NOT overlap. Gaps and an empty section
array are allowed. `role` is an open string rather than a fixed enumeration of
song-section categories. Sections need not cover every note and MUST NOT truncate
notes at their boundaries.

`tempoChanges` MUST begin with `at: 0`, and subsequent `at` values MUST strictly
increase. `bpm` is a finite number greater than 0 and at most 1000. It always means
**quarter notes per minute**, independent of meter. Each value remains constant
until the next tempo change. Continuous tempo curves are not defined in 3.0.0.

`meterChanges` follows the same tick-0 and strictly increasing position rules.
`numerator` is an integer from 1 through 64. `denominator` is one of `1`, `2`, `4`,
`8`, `16`, `32`, or `64`. A reader MUST NOT move a declared change to an inferred
bar boundary.

For a constant-tempo segment, elapsed seconds are:

```text
seconds = ticks * 60 / ppq / bpm
```

A note crossing tempo changes must be converted to time segment by segment.
Displayed bar numbers, including whether an anacrusis is called bar 0, are
presentation conventions separate from the tick coordinate system.

## 5. Harmony

`harmony` requires the arrays `chords` and `scales`. Both may be empty. Each array
MUST be in nondecreasing `start` order; overlapping harmonic contexts are allowed.
If several contexts are available, a relative-note assignment selects its context
by ID, not by incidental array order.

### 5.1 Spelled pitch classes

A spelled pitch class contains `step` and `alter`. `step` is one of `A` through
`G`; `alter` is an integer from -2 through 2. Natural pitch classes are `C=0`,
`D=2`, `E=4`, `F=5`, `G=7`, `A=9`, and `B=11`. Add `alter` and normalize modulo 12.

The spelling MUST be retained: `{ "step": "C", "alter": 1 }` and
`{ "step": "D", "alter": -1 }` have the same pitch class but different spellings.
This object contains no octave.

### 5.2 Chords

A chord requires `id`, `start`, `duration`, and a nonempty `label`. `root`,
`intervals`, and `bass` are optional. However, `root` and `intervals` MUST either
both be present or both be absent.

`root` and `bass` are spelled pitch classes. `intervals` is a nonempty array of
integer semitone distances from the root, from 0 through 35. It MUST contain 0,
MUST be strictly increasing, and MUST contain no duplicates. An extension such as
14 MUST NOT be automatically reduced to 2. These intervals declare a harmonic
interpretation, not a performed voicing.

A label-only chord is valid. A reader's private parsing of that label is not
portable structured information shared with other readers. Specifying `bass` does
not generate a bass track.

### 5.3 Scales

A scale requires `id`, `start`, `duration`, `tonic`, and `intervals`. `label` is
optional. `tonic` is a spelled pitch class. `intervals` is a nonempty, strictly
increasing array of distinct integers from 0 through 11 and MUST contain 0.

Chords and scales do not restrict which pitches may occur in Core notes. Passing
tones, dissonances, and intermediate editing states are not format errors. A
reader MUST NOT generate performance events from `harmony` alone.

## 6. Tracks, clips, and notes

### 6.1 Tracks

A track requires `id`, `name`, and `clips`. Optional members are `role`,
`instrument`, and `enabled`. `instrument`, when present, requires a string `name`
and may contain a string `family`. `enabled` defaults semantically to `true` when
absent; the schema's default annotation does not itself insert a field.

Melody, bass, accompaniment, and percussion use the same track structure. `role`
describes a musical function, and `instrument` describes an instrument. Neither
executes an instrument plug-in. A playing method such as arpeggiation is not the
same concept as an instrument name. Track array order is the display order and
MUST be retained.

### 6.2 Clips

A clip requires `id`, `start`, `duration`, and `notes`. `name` and `enabled` are
optional. `start` is a nonnegative global tick position. `duration` is the length
of a placement/editing reference span. `enabled` defaults semantically to `true`.

Clips in a track MUST be in nondecreasing `start` order. Equal starts and overlap
are allowed. A clip's reference span is **not a playback truncation mask**.

### 6.3 Notes

A note requires `id`, `start`, `duration`, and exactly one of `pitch` or
`soundSlotId`. Specifying both targets or neither target is invalid.

| Member | Rule |
|---|---|
| `pitch` | Integer semitone number from 0 through 127; 60 is C4 and 69 is A4; reference tuning uses A4 = 440 Hz |
| `soundSlotId` | Reference to an existing percussion sound slot |
| `start` | Signed integer tick offset relative to the clip's reference start |
| `duration` | Positive integer ticks for which the note is held, up to its gate end |
| `id` | Document-wide unique note identity |

Notes in a clip MUST be in nondecreasing local `start` order. Equal-start notes
retain their array order. Compute absolute positions as follows:

```text
onset   = clip.start + note.start
gateEnd = onset + note.duration
```

`onset` MUST be nonnegative. Both `onset` and `gateEnd` MUST be at most `MAX`.
Implementations MUST check the sums, not just the individual field values.

Negative local starts, starts after the clip's reference span, gates extending
beyond that span, and overlapping notes of the same pitch are valid. Each note
remains a separate identity. Readers MUST NOT merge or shorten these notes on
load. Negative absolute song positions are not allowed; an anacrusis can instead
be represented by placing the first section later on the timeline.

`duration` is not the time until a synthesizer's release or reverberation becomes
silent. It is also distinct from notated duration. Notated values, ties, voices,
and detailed articulations are subjects for future optional profiles.

### 6.4 Enabled performance and deterministic events

A note produces events only when both its track and its clip are enabled.
Disabled tracks and clips MUST still be preserved and structurally validated.

Produce a `noteOn` at `onset` and a `noteOff` at `gateEnd`. Both events carry the
same `noteId`, `trackId`, and `clipId`. Sort events first by tick. At a shared tick,
all `noteOff` events precede all `noteOn` events. Events with the same tick and
event kind are ordered lexicographically by `noteId`.

The performance end is the maximum `gateEnd` of enabled notes, or 0 if there are
none. Section and clip ends alone do not determine when note playback ends.
Transport stop and seek behavior belongs to the host.

An exporter with solo states or per-note mute MUST materialize the adopted
performance through Core `enabled` states or the adopted note arrays. If an output
device cannot independently render overlapping notes of the same pitch, that is
an output conversion constraint; it does not authorize rewriting the stored notes.

## 7. Percussion targets and resource references

### 7.1 `soundSlots`

A sound slot requires `id` and `name`. `role` and `midiNote` are optional.
`midiNote` is an integer from 0 through 127 and is only a mapping hint for a
particular output. It is not the slot's identity and does not declare General MIDI
conformance.

Two slots may both have role `kick` or the same `midiNote` and still remain
independent. They MUST NOT be merged for that reason. A reader without a suitable
sound mapping preserves and displays the events and lets the host assign sounds.
Timbre equivalence is not guaranteed. A pitched 808 bass is represented with
pitched notes.

### 7.2 `resources`

A resource requires `id`, `kind`, and `uri`. `kind` is `audio`, `midi`, `text`, or
`other`. `uri` is a nonempty string. Optional members are `name` and `sha256`, where
`sha256` is exactly 64 lowercase hexadecimal characters.

A resource is a reference to material, such as generation input; it is not an
audio-track playback instruction. Loading a document MUST NOT fetch or execute a
referenced resource. An unavailable resource does not by itself invalidate the
stored note structure. Resolving a relative URI against a base location and
checking the actual resource against its hash belong to an explicit resource
operation.

## 8. Lyrics

`lyrics` requires four arrays: `documents`, `phrases`, `units`, and `alignments`.
Each may be empty.

| Element | Required members | Optional members |
|---|---|---|
| Lyric document | `id` | `title`, `language` |
| Lyric phrase | `id`, `documentId`, `text` | `pronunciation`, `start`, `duration` |
| Lyric unit | `id`, `phraseId`, `text` | `pronunciation`, `start`, `duration` |
| Lyric alignment | `id`, `unitIds`, `noteIds` | None |

`documentId` and `phraseId` MUST resolve to the correct kinds. `text` is display
text; `pronunciation` is a string annotation for pronunciation. This definition
does not standardize language-specific segmentation, phoneme alphabets, or a
singing-synthesis engine. `language` is an auxiliary string.

A phrase's `text` is its displayed text. Units are annotations for segmentation
and assignment. Concatenating unit texts need not exactly reproduce the phrase
text. A pronunciation spelling that differs from display spelling is preserved.

If a phrase or unit has timing, it MUST specify both `start` and `duration` on the
global song timeline. Start is nonnegative, duration is positive, and the computed
end MUST not exceed `MAX`.

Both `unitIds` and `noteIds` in an alignment MUST be nonempty. Each list MUST be
duplicate-free and ordered, and every ID MUST resolve to its declared kind. An
alignment can associate multiple units with multiple notes. It can represent one
syllable extended across several notes or several units associated with one note
without forcing either case into a one-to-one model. An alignment does not
generate notes.

## 9. Common extension contract

### 9.1 Namespaces and envelopes

Extension keys use reverse-domain-style namespaces such as
`org.ostf.relative-phrase.v1`. The grammar is:

```text
^[a-z][a-z0-9-]*(?:\.[a-z][a-z0-9-]*){2,}$
```

There must be at least three dot-separated components, each beginning with a
lowercase ASCII letter. A namespace is an identity convention, not authentication
of the author.

Every extension has exactly four required outer members:

| Member | Meaning |
|---|---|
| `version` | Nonempty version string |
| `status` | `current`, `stale`, or `unverified` |
| `dependencies` | Dependency declaration described below |
| `data` | Arbitrary JSON value, constrained further only for a supported profile version |

The envelope is closed. Vendor-specific outer members MUST NOT be added.

### 9.2 Status and dependencies

| Status | Meaning |
|---|---|
| `current` | The producer declares that the recorded relationship matches the current document |
| `stale` | A relevant change is known to have broken the previous relationship |
| `unverified` | The relationship has not been checked, or the current editor cannot check it |

Status does not switch the Core performance. A `current` declaration is not proof
that a validator has reproduced an unknown generation engine.

`dependencies` has exactly one of these forms:

```json
{ "scope": "document" }
```

```json
{ "scope": "none" }
```

```json
{ "scope": "objects", "refs": [{ "type": "note", "id": "note-example" }] }
```

For `objects`, `refs` MUST be nonempty and duplicate-free. `none` declares no
dependency on current Core objects. A `current` dependency reference MUST resolve
to the correct kind. Missing counterparts for `stale` or `unverified` extensions
are preserved with warnings. This relaxation MUST NOT be applied to broken Core
references.

For a `current` known profile that contains direct Core references, use
`scope: document` or include **every direct Core reference in its data** in
`objects.refs`. This includes relative-note targets and contexts, generation
inputs and outputs, protected notes, and appearance targets. Extension-local IDs
are not Core dependencies. If there are no Core dependencies, `scope: none` is
permitted unless the individual profile requires document scope.

Dependency meaning includes relationships inherited through the Core hierarchy,
not just the referenced object's direct JSON members. Moving a parent clip changes
its note's absolute onset; disabling a parent changes the note's effective enabled
state. An implementation unable to enumerate the necessary dependencies must use
document scope.

After a relevant edit, an editor MUST either update the relationships it
understands and the adopted notes, or change the status to `stale` or `unverified`.
It MUST preserve unknown `data` without speculative modifications and use the
outer status to express uncertainty. Merely recording a new status is not another
musical edit that recursively invalidates extension statuses again.

### 9.3 Exact-version dispatch and fallback

Unknown namespaces and unknown versions of known namespaces are preservable by a
Core reader. The common envelope rules still apply. A reader MUST NOT validate a
future version's `data` against an older known data schema and reject it for that
reason. Profile interpretation is selected by the namespace **and exact supported
version**, not by namespace alone.

Conversely, malformed data for an exact known version is an error even if the
extension is `stale` or `unverified`. Those statuses relax correspondence and
reference checks; they do not relax a known data structure.

## 10. Standard optional profiles

The following five profiles and the legacy source archive in Section 11 are
bundled at provisional version `1.0.0-draft.1`. Relative phrases, generation
context, appearance, and legacy-import retain their Draft 1 meanings; phrase
library and clip choices retain their Draft 2 meanings. Stable Core does not
change these profile versions or make them stable. An implementation claiming
support follows the exact version's rules. A reader that understands none of
them can still read the adopted performance from Core. Their data objects and
nested records are closed according to the schema.

### 10.1 Relative phrases

Namespace: `org.ostf.relative-phrase.v1`.

`data` requires an `assignments` array. Each assignment requires:

| Member | Rule |
|---|---|
| `noteId` | A pitched Core note; each target note appears at most once in the array |
| `basis` | `chordTone` or `scaleDegree` |
| `contextId` | Chord or scale ID, according to `basis` |
| `anchorPitch` | Integer 0–127: an actual octave-specific root or tonic pitch |
| `index` | One-based position in the context's ordered `intervals` array |
| `chromaticOffset` | Integer semitone adjustment from -24 through 24 |

The structural maximum for `index` is 36 for `chordTone` and 12 for
`scaleDegree`. For a `current` assignment, it MUST also be within the actual
context array. This index is a position in that array, not a chord-symbol label
such as “5th.”

A `current` chord-based assignment requires a chord with `root` and `intervals`.
The pitch class of `anchorPitch` MUST match the context's root or tonic. The
following result MUST be within 0–127 and MUST equal the target Core note's pitch:

```text
pitch = anchorPitch + intervals[index - 1] + chromaticOffset
```

An explicitly referenced pickup note is not invalid merely because its onset is
outside the context's time span.

For `stale` or `unverified` data, reference and pitch mismatches are retained as
warnings. A reader MUST NOT overwrite Core pitches from outdated relative
information on load.

This profile version does not imply an optimal register after reharmonization,
voice-leading rules, selection by input-note rank, or complex Figure
interpretation. Those are separate profiles or generator behavior.

### 10.2 Generation context

Namespace: `org.ostf.generation-context.v1`.

`data` requires a `processes` array. Each process requires `id`, `generator`,
`inputs`, `outputs`, and `protectedNoteIds`. `targetRange` and `vendorExtension`
are optional. Process IDs are unique within this extension.

`generator` contains a nonempty `id` and a nonempty `version`. Each input contains
a nonempty string `role`, a typed `ref`, and optionally a `readRange`. Inputs may
be empty or contain multiple distinct sources; they must not be collapsed into a
single presumed source. `outputs` is a nonempty array of typed references.
`protectedNoteIds` is a duplicate-free array of Core note IDs.

For `current` data, all inputs, outputs, and protected notes MUST resolve to the
correct kinds. Unresolved references in `stale` or `unverified` data are retained
with warnings.

`readRange` and `targetRange` use the global `Range` definition. `readRange`
describes the context read. `targetRange` describes the range requested for
modification. Neither is automatically the complete output span: pickups and
extended gates may lie outside it.

For `current` data, `vendorExtension`, when present, MUST reference another
existing extension in the same document and requires
`dependencies.scope: document`. A reference to this generation-context extension
itself is an error regardless of status. For `stale` or `unverified` data, a
missing referenced extension or non-document dependency scope is retained with a
warning.

An application claiming support for protected notes and executing a generation
operation MUST preserve each protected note's ID, pitch or sound target, global
onset, gate, and effective enabled state during that operation. Moving its parent
clip without changing local note values, disabling its parent, or deleting the
note also changes protected content. A validator can check references in a saved
document; without before-and-after data it cannot establish that an earlier
generation operation respected protection.

Settings such as `seed`, `complexity`, or `humanize` do not have universal,
engine-independent behavior. Store proprietary settings in vendor extensions.
This profile records generation context; it is not an instruction to execute
generation on load.

### 10.3 Appearance and section roles

Namespace: `org.ostf.appearance.v1`.

`data` requires `roleDefinitions`, `sectionRoleAssignments`, and `appearance`.
Each role definition has an extension-local unique `id`, a nonempty `name`, and
optionally a string `baseRole`. `sectionRoleAssignments` maps Core section IDs to
custom-role IDs.

`appearance` requires all three members below, even when they are empty:

| Member | Meaning |
|---|---|
| `roleColors` | Map from role strings to colors |
| `customRoleColors` | Map from custom-role IDs to colors |
| `objectColors` | Array of objects containing a typed `target` and `color` |

Colors have the exact `#RRGGBB` form; hexadecimal letters may be upper- or
lowercase. Multiple `objectColors` entries for the same typed target are invalid.
For `current` data, target references and custom roles MUST resolve.

Resolve color using the first available choice in the applicable row:

| Object kind | Priority, highest to lowest |
|---|---|
| Section | Its own object color; assigned custom role's custom color; role color for that custom role's `baseRole`; role color for Core `section.role`; host default |
| Track or sound slot | Its own object color; role color for its Core `role`; host default |
| Clip | Its own object color; its parent track's resolved color |
| Note | Its own object color; its parent clip's resolved color |
| Any other Core target | Its own object color; host default |

A reader MUST NOT infer colors from a section merely because it overlaps an
object in time. Resolvable color references in `stale` or `unverified` data may be
displayed, but unresolved references MUST NOT be redirected to different objects.
Appearance metadata does not create or modify performance events.

This namespace is distinct from OSTF 2.3's
`org.ostf.section-role-appearance.v1`. An implementation MUST NOT silently redefine
the old namespace's target kinds or meaning.

### 10.4 Phrase library

Namespace: `org.ostf.phrase-library.v1`. Profile version: `1.0.0-draft.1`.
Interpret this profile in Draft 2 and 3.0.0 documents.

`data` has exactly the required arrays `templates` and `instances`; both may be
empty. Every ID uses the grammar in Section 3. The records are closed objects.

A template requires `id`, `duration`, and `notes`; `name` is an optional display
string. Template IDs are unique within `templates`. `duration` is positive integer
ticks in the document timebase and defines the **repeat period**.

Template notes use the Core Note field shape: `id`, `start`, `duration`, and
exactly one of `pitch` or `soundSlotId`. However, their IDs are local to that
template, unique within it, and MUST NOT be registered as Core note IDs. Notes
are ordered by nondecreasing `start`. Signed starts, pickups, starts after the
period, and gates beyond the period are allowed. Template notes do not play by
themselves. A template's `soundSlotId` is a direct Core reference.

An instance requires exactly these members:

| Member | Rule |
|---|---|
| `id` | Local ID unique within `instances` |
| `templateId` | Local template ID in this profile |
| `clipId` | Core clip ID |
| `repeatCount` | Integer from 1 through `MAX` |
| `transpose` | Integer semitone offset from -127 through 127 |
| `noteMap` | Array of occurrence mappings |

A mapping contains exactly `templateNoteId`, `repeatIndex`, and `noteId`.
`templateNoteId` identifies a note in the referenced template; `repeatIndex` is an
integer from 0 through `MAX`; `noteId` identifies a Core note. Mapping array order
has no semantic effect. Template IDs and instance IDs have separate local scopes.

One instance owns one Core clip. Two instances MUST NOT name the same `clipId`.
One template may have many instances. Duplicate template IDs, instance IDs, note
IDs within one template, occurrence keys `(repeatIndex, templateNoteId)` within
an instance, mapped Core note IDs anywhere in this profile, and clip ownership
conflicts are intrinsic errors in every status.

For `current` data, each template reference MUST resolve and every `repeatIndex`
MUST be less than `repeatCount`. The map must cover exactly the product of the
template's notes and repetitions, with one occurrence for every pair. Mapped
Core notes MUST belong to the instance's clip; the map MUST cover all of that
clip's notes and no others. Unmapped manual additions to the same clip are not
consistent with a `current` exact realization.

The correspondence equations are:

```text
clip.duration = template.duration * repeatCount
note.start = repeatIndex * template.duration + templateNote.start
note.duration = templateNote.duration
pitched note.pitch = templateNote.pitch + transpose
unpitched note.soundSlotId = templateNote.soundSlotId
```

Transposition does not affect sound slots. Calculated pitch MUST be in 0–127.
`clip.start` supplies global placement, and Core equations determine absolute
onset and gate end. Computed clip duration, local starts, and global endpoints
must fit Core bounds. No first-repetition pickup or final tail is omitted or
truncated. Each occurrence retains a separate Core note identity.

Validation MUST NOT generate all expected occurrences. Integer cardinality,
validity of each supplied mapping key, and uniqueness establish complete coverage
without expanding the Cartesian product. An explicit materialization operation
may have a separate implementation resource limit; that is not a wire-format
repeat limit.

Missing references or templates, incomplete or excessive coverage, wrong mapped
parents, and target, time, duration, computed-pitch, or range mismatches are errors
for `current` and warnings for `stale` or `unverified`. Known structural errors,
intrinsic identity ambiguity, and invalid Core content remain errors. One outer
status applies to the entire library and all its instances.

Direct dependency coverage includes every referenced sound slot, clip, and mapped
Core note, not local IDs. Document scope is recommended. A library with no Core
dependency may use `none`. Loading MUST NOT materialize or refresh instances.
Nested templates, time scaling, probability, harmony fitting, and overrides are
outside this profile version. Relative and generation relationships remain
separate profiles; when both are current, both must agree with the same Core.

### 10.5 Clip choices

Namespace: `org.ostf.clip-choices.v1`. Profile version: `1.0.0-draft.1`.
Interpret this profile in Draft 2 and 3.0.0 documents.

`data` has exactly a required `groups` array, which may be empty. A group requires
`id`, `candidates`, and `selectedCandidateId`; `name` is optional. Group IDs are
unique across groups, and `candidates` is nonempty. A candidate requires `id` and
`clipIds`; `name` is optional. Candidate IDs are local and unique within their
group. Names are display strings; local IDs do not become Core IDs.

`clipIds` is an ordered, duplicate-free array of Core clip IDs. An empty array
represents a silent candidate. `selectedCandidateId` is a candidate ID in that
group or `null`; null explicitly selects no candidate.

The managed set of a group is the union of all its candidates' clip IDs. A clip
may occur in several candidates of one group, but MUST NOT be managed by two
different groups. Duplicate group IDs, duplicate candidate IDs within a group,
duplicate IDs within one candidate's clip list, and conflicting ownership are
errors in every status.

For `current` data, the selected candidate, when nonnull, and every candidate's
Core clip references MUST resolve. Each managed clip's own `enabled` value,
defaulting to true when absent, MUST equal its membership in the selected
candidate. With a null selection, all managed clips MUST be disabled.

Compare the **clip's own enabled flag**, not the effective track-and-clip enabled
state. `track.enabled` is independent and MUST NOT be changed by candidate
activation. A selected clip can therefore remain silent because its parent track
is muted. Unmanaged clips are unaffected. Distinct clips may overlap in time as
Core allows; group ownership is not inferred from time ranges or song sections.

A missing local selection or Core clip reference and a mismatch with clip enabled
states are current errors and stale/unverified warnings. All candidate clip
references, including unselected clips, count toward dependency coverage. A reader
MUST NOT apply a selection or repair Core enabled flags on load.

This profile selects combinations of **already materialized performance clips**.
It does not select harmony, sections, lyric documents, routing, or transport
scenes. It does not add an enabled state to Core harmony or claim a whole-song
scene model.

### 10.6 Explicit operations and snapshot protection

The [operation guide](OPERATIONS.md), [phrase and choice profile guide](OPTIONAL_PROFILES.md), and
[reference implementation guide](REFERENCE_IMPLEMENTATION.md) describe the
operation APIs. Operations return copies, do not mutate caller inputs, and
validate before and after. A failed operation returns no partially edited
document. Replacement templates and supplied ID lists are also caller-owned and
MUST NOT be mutated. Unsupported root, namespace, and profile versions are not interpreted
speculatively. Unknown payload values and numeric token distinctions survive
copying and strict serialization.

`convert_version(document, target_version=VERSION)` defaults to
`VERSION = "3.0.0"` and explicitly converts among all three exact supported roots.
It preserves Core content and events, changing the root version and necessary
extension statuses only. A current extension unknown to either side is marked
unverified when its dependency scope is not `none`. Profiles understood on both
sides keep their meanings and versions; stale or unverified claims are not
promoted automatically. Conversion can fail when formerly opaque data becomes
known and violates its structural schema. Reading does not perform this operation.

The compatibility API `convert_draft_version(document, target_version)` retains
its required target argument and restricts both source and target to Draft 1 or
Draft 2. CLI `convert SOURCE OUTPUT --to-version VERSION` supports all three
roots and requires the target option. Legacy `upgrade` targets Draft 2 and legacy
`downgrade` targets Draft 1, accepting only draft inputs. Use `convert` for any
conversion involving stable 3.0.0.

`materialize_phrase` requires a Draft 2 or 3.0.0 document and an exact known,
current phrase profile. It adds a new clip and instance and never overwrites an existing clip,
instance, or Core ID. It rejects a template-note count times repetition count
above `max_notes` before expansion; the reference default of 100000 is an explicit
implementation resource limit. The reference operation derives each note ID as
`note.` followed by the SHA-256 of UTF-8 compact JSON
`[instance_id, repeatIndex, templateNoteId]`; any existing ID collision is rejected.
Notes are sorted by `(start, repeatIndex, template array index)`, and mappings by
`(repeatIndex, template array index)`. Empty templates can create empty clips.
The parent track's enabled state is unchanged. Affected other extensions are
invalidated; the entire updated phrase profile is certified current only after
validation. This creation operation does not rebuild existing instances. Revision 1
defines a separate explicit replacement operation below; automatic propagation on
load remains prohibited.

`activate_candidate` requires Draft 2 or 3.0.0 and the exact supported clip-choice profile.
It updates the selected ID and all managed clip enabled flags in one operation.
It may accept a structurally valid current, stale, or unverified
choice profile, but required managed references must resolve. It does not repair
other groups. If all groups cannot validate as current afterward, the entire
operation fails. Repeating an already-current identical selection MUST NOT
invalidate unrelated extensions. An optional fixed `protected_note_ids` list is
checked afterward; a mismatch does not yield a partially applied result.

`check_protected_notes` compares a fixed, duplicate-free supplied note ID list
between valid before and after documents. It includes inactive notes and compares
identity presence, pitch or sound-slot identity, global onset, duration/gate end,
and effective enabled state. Local coordinate representation and parent identity
need not be identical. Different PPQ yields `PROTECTION_PPQ_MISMATCH` and an invalid
comparison. An empty supplied list is visibly reported as `checkedNoteIds: []`.

`check_generation_protection` fixes the protected ID list from one process in
before's exact supported, current generation profile, then delegates to the
comparison. Removing or altering after's process or protection list cannot remove
protection from this check. The result establishes only equality of the defined
snapshot fields, not actual engine execution or historical truth. Tempo changes
that alter elapsed seconds, timbre, and audio results are outside this musical-tick
protection contract.

### 10.7 Template replacement and detachment — Revision 1

These are explicit editing operations over the existing phrase-library format.
They introduce no profile fields or changed wire meanings. Both require the exact
Draft 2 or 3.0.0 root and supported phrase-library version. They validate before and after,
leave all caller-owned inputs unchanged, and expose no partial result on failure.
The optional `protected_note_ids` is a fixed, duplicate-free list or tuple selected
before the operation. A failed comparison raises
`OPERATION_PROTECTION_VIOLATION` before a result is exposed.

#### Replace one template and refresh every linked instance

`replace_phrase_template(document, template_id, replacement, *, protected_note_ids=(), max_notes=100000)`
requires a valid document whose **entire phrase profile is current**. It must not
overwrite a manual edit hidden in a stale realization. The target template must
exist. `replacement` is a complete template object under the existing schema, with
the same ID as `template_id`; it is not a patch or an implicit rename. Invalid
structure, duplicate local note IDs, and unresolved sound slots are rejected.

The operation replaces that template and refreshes all instances referencing it
in one transaction. It retains every instance's ID, template ID, clip ID, repeat
count, and transpose, and retains the parent track and each Core clip's ID, start,
name, and own enabled state. Track enabled state is also retained. Clip duration,
notes, and mapping are recomputed with the unchanged phrase equations. Unrelated
templates, instances, and Core clips remain as stored.

For a surviving `(repeatIndex, templateNoteId)` key, the Core note ID comes from
the **original valid map**, including custom non-hash IDs assigned by another
writer. Only new occurrences use the reference materializer's deterministic hash
policy. Reserve all original Core IDs, including those removed in this transaction,
and all newly allocated IDs. A collision rejects the whole operation. Renaming a
source note is removal plus addition; identical pitch or timing does not establish
identity.

Refresh sorts Core notes by `(local start, repeatIndex, source array index)` and
mappings by `(repeatIndex, source array index)`. Pickups, tails, late starts, and
overlaps remain. Before expansion, bound the **total resulting notes across every
affected instance** by `max_notes`. The default 100000 is an operation resource
limit, not a wire maximum. Empty templates must not enumerate huge empty repeat
loops. An invalid pitch, span, local start, or absolute endpoint in any affected
instance rejects the entire operation.

If a Core lyric alignment still references a removed note, fail with
`OPERATION_REFERENCED_NOTE_REMOVAL` and diagnostics identifying the reference.
Never silently delete a lyric unit, alignment, or reference. References to surviving
notes retain their IDs. Retained identity does not itself freeze pitch or gate;
the supplied protection set checks those properties where required.

Other extension payloads are preserved. Core edits trigger conservative
invalidation using changed clip and removed note references. Removal can broaden
invalidation when deleted ancestry cannot be determined; invalidation is not
limited to the immediately edited objects. A nontrivial profile-only edit also
conservatively marks other non-`none` current claims unverified. The updated phrase
profile uses document dependencies and is certified current only after complete
post-validation. Protection must also pass before returning the result.

An identical validated replacement is a no-op copy, including status,
dependencies, and array order; requested protection is still checked. If duration
and notes are identical and only the template name changes, preserve Core and
the existing note-map order while applying the metadata/status/dependency update.
Loading never performs this synchronization, and unrelated stale relationships
are not silently repaired.

#### Detach selected instance relationships

`detach_phrase_instances(document, instance_ids, *, protected_note_ids=())`
removes only the selected instance records. The ID list or tuple must be
duplicate-free and every requested instance must exist. A mixed existing/missing
request fails atomically. An empty list returns a validated no-op copy, with
requested protection still checked.

The input phrase profile may be current, stale, or unverified, but the whole
document must remain valid under its structural and Core requirements. Every
template and every Core object remains unchanged, including notes and IDs, clips,
timing, lyric alignments, harmony, array order, clip enabled states, and track mute.
A manually edited clip with a stale link can therefore be detached without
regenerating it.

This profile edit conservatively invalidates other non-`none` current extension
claims, but preserves the phrase envelope's **original status**. Removing the last
mismatch does not promote stale or unverified to current. Existing phrase
dependencies are retained; over-declaration is allowed. Validate the resulting
whole document and the fixed protection list before returning it. The operation
does not repair unrelated relationships or delete Core notes or lyric references.

#### File-input protection

For `replace-template`, both the source document and the `--replacement` template
JSON file are protected inputs. Existing output requires `--force`, which never
permits overwriting either input through its path, hard link, or symbolic link.
The replacement file is one strict UTF-8 JSON object. `detach` uses the same atomic
output policy. CLI `--protect-process` obtains its IDs only from before's current
generation process. Complete output is staged before publication. Validation,
operation, protection, staging, or publication failure before commit leaves the
final destination unchanged. If the required atomic publication is unavailable,
the writer fails rather than using a non-atomic fallback. This does not promise
rollback of failures after publication.

## 11. Migration from OSTF 2.3

The published 2.3 profile does not fully standardize all nested pitch and lyric
alignment semantics. Changing the version string therefore does not convert a
document to 3.0. The source baseline and the bounded converter are documented in
the [migration guide](MIGRATION_2_3_TO_3_0.md), with links to the upstream
specification and schema at the reviewed commit.

### 11.1 Default migration and source archive

The supplied converter transfers recognized, correctly interpretable title and
timeline structure. It MUST NOT assume general meanings for opaque performance,
parse arbitrary chord labels into structure, or infer lyric references. It records
reasons for material that cannot be transferred into valid target structures.
The converter defaults to root version `3.0.0`. Its API keyword
`target_version=VERSION` and CLI `--target-version` also accept an explicit
`3.0.0-draft.2` target; Draft 1 is not a target of this 2.3 adapter. Its conservative
source interpretation policy is unchanged. It does not infer reusable templates or
candidate groups from legacy material.

The complete original source is stored as UTF-8 text in the archive profile:

```text
namespace: org.ostf.legacy-import.v1
version:   1.0.0-draft.1
status:    unverified
dependencies: { scope: document }
data:
  sourceVersion: 2.3.0
  sourceSha256: SHA-256 of the original UTF-8 bytes
  sourceText: complete original source text
  conversionReport: JSON object
```

These four data fields are required. `sourceSha256` uses 64 lowercase hexadecimal
characters. The report records transferred material, uninterpreted material,
assumptions, warnings, and ID mappings. Re-encoding `sourceText` as UTF-8 MUST
reproduce the original bytes for which the hash was computed, including original
line endings and numeric spelling.

The archive is historical source evidence, **not another playback authority**.
It MUST NOT be automatically updated to match subsequent 3.0 edits or played on
load. Source preservation and complete migration of musical meaning are distinct
claims.

### 11.2 Explicit sample-convention interpretation

Only explicit selection of `interpret-sample-notes` authorizes the adapter to
interpret sample `pitch` values as integer pitches with C4 = 60, note `start` as
clip-relative ticks, and note `duration` as a gate. Mapping sample `symbol` to a
display-only chord `label` is likewise an explicit reported assumption.

If unknown attributes could change mute, transposition, dynamics, or other
meaning, an object MUST NOT be silently activated as a successfully converted
performance or chord. The explicit adapter uses the strict sample shapes described
in the migration guide, archives unsupported objects, and records the reason.
Explicit adapters for identified application dialects may be added later.

Cross-kind legacy ID collisions are deterministically remapped to globally unique
Core IDs. Ambiguous source references MUST NOT be guessed or redirected.

### 11.3 Appearance and limits

Known legacy roles and colors may be transferred to the new appearance profile
where target ID correspondence is established. If a corresponding clip or other
object was not transferred, its color MUST NOT be assigned to a different object.
Unconverted information remains in the original source and report. Identical
appearance may be claimed only after checking the legacy precedence rules as well
as the color values.

3.0.0 does not guarantee a completely reversible 3.0-to-2.3 conversion. New 3.0
performance has one authoritative representation in `tracks`. The supplied
converter performs bounded source checks and validates its generated target; this
is not complete 2.3 conformance testing or a claim of complete semantic migration.
The ability to represent lyric relationships and chord labels in 3.0 does not
establish the meaning of arbitrary opaque 2.3 data.

## 12. Worked timing and relative-note example

The complete JSON example in the
[Japanese specification, Section 12](FORMAT_SPECIFICATION.ja.md#12-最小構成を拡張した記述例)
has PPQ 960, a clip beginning at 0 with duration 3840, and the following notes:

| Pitch | Local start | Gate duration | Absolute gate end |
|---|---:|---:|---:|
| C4, 60 | 0 | 720 | 720 |
| E4, 64 | 960 | 720 | 1680 |
| G4, 67 | 1920 | 2400 | 4320 |

The final gate ends at tick 4320 although the clip's reference span ends at 3840.
The E4 assignment uses a C anchor of 60 and the second element, 4, of the declared
chord intervals: `60 + 4 + 0 = 64`.

A reader without the relative-phrase profile still reads pitches 60, 64, and 67
and their timing directly from Core. The profile contributes no additional notes.
The [four-part sample](../samples/01_four_part_sketch.ostf) and
[sample index](../samples/INDEX.md) provide additional complete files.

## 13. Verification and conformance claims

The original 39 acceptance conditions remain in the [Japanese specification, Section 13](FORMAT_SPECIFICATION.ja.md#13-適合試験の基準). Together with D201–D230 and R101–R120, the [consolidated conformance table](CONFORMANCE.md) records 89 acceptance viewpoints. These describe required behavior and do not claim executed passes. Earlier Draft 2 Revision 1 reports remain in earlier development packages; test runners and historical execution reports are not included in this curated release.

No runtime verification was performed for this release preparation, and additional runtime verification is not a publication prerequisite. The [sample catalogue](../samples/catalog.json) contains authored examples. [Coverage](COVERAGE.md) records field and enumerated-value presence, not runtime or semantic validation.

Keep these verification layers distinct:

1. **Strict input:** UTF-8 and JSON ingestion, forbidden representations, integer
   token form, and unknown numeric precision.
2. **Structure:** Core schema and exact known profile data schemas.
3. **Semantics:** time sums and ordering, global IDs, typed references, profile
   correspondence, and dependency coverage.
4. **Adopted performance:** deterministic event lists and performance end against
   independently specified expected results.
5. **Migration:** conservative default behavior, opt-in assumptions, exact source
   reconstruction, ID mapping, and handling of ambiguity.
6. **Explicit operations:** root-version conversion without changed Core events,
   phrase materialization, atomic candidate activation, and fixed before/after
   protection comparisons against independently specified expectations.

JSON Schema success alone is not success at every layer. Optional-profile editing
behavior is required only of implementations that claim to perform that behavior.
Testing regeneration with protected notes requires before-and-after data. Actual
interchange between external applications is a separate interoperability test and
must be reported separately from format verification.

## 14. Support declarations and implementation sequence

An implementation should describe Core reading, Core writing, editing that
preserves unknown information, display/editing of each profile, and proprietary
regeneration separately. A single undifferentiated “OSTF support” claim is
insufficient to communicate these capabilities.

### Initial release scope

The initial 3.0 scope consists of stable Core, the existing six provisional
profile namespaces at `1.0.0-draft.1`, current explicit operations, and conservative
migration.
Optional profiles and editing behavior apply only to implementations claiming
that support. Chord-aware fitting, partial overrides, time scaling, whole-song
scenes, notation models, additional expression, and external adapters are deferred
and are not completion conditions for the initial stable Core distribution.

Existing types, required fields, and numeric bounds form the initial baseline.
A later incompatible change must identify its effect on previously valid files
or meaning and use an appropriate version. The [license notice](../LICENSE.md) defines the release scopes. [Source attribution](SOURCE_ATTRIBUTION.md) records upstream 2.3 materials and their preserved provenance.

### Implementation and verification units

The units below explain implementation support and required behavior, not new
execution evidence. This stable preparation adds no runtime verification
requirement to its publication decision; earlier results remain historical records.

The implementation and verification units are:

1. Strict JSON input, Core schema, and timing/identity/reference validation.
2. A Core event extractor with independent expected-event tests.
3. Root-version dispatch and preservation of the original relative, generation,
   appearance, and legacy archive profile definitions.
4. Conservative 2.3 migration separated from explicit sample interpretation.
5. Phrase-library and clip-choice validation, explicit operations, and snapshot
   protection checks with independent expectations.
6. Revision 1 replacement across all linked instances with surviving identity,
   lyric integrity, fixed protection, atomic failure, and Core-preserving detachment.
7. Explicit conversion among the three supported roots with unchanged Core
   content, while retaining the restricted legacy draft conversion API. Identify
   the version covered by every schema, authored example, and historical result;
   do not count this unexecuted update as part of an earlier passing run.

Verification reports must identify commands actually run, the environment,
versions tested, positive and negative results, and unsupported scope. Unexecuted
tests MUST NOT be counted as passing.

### Deferred extensions and maintenance policy

| Topic | Initial release treatment | Later work |
|---|---|---|
| Source phrases and placement instances | Existing concrete templates, transposition, and repeats, plus explicit whole-template replacement/all-instance refresh and detachment | Automatic resynchronization, partial overrides, time scaling, and repeat phase |
| Candidates and whole-song scenes | Multi-part Core-clip choices reflected in clip enabled states | Harmony, lyrics, structure, routing, and real-time scene launch |
| Note protection | Fixed before/after identity, target, absolute ticks, gate, and effective enabled state | Integration with generators and protection of seconds, timbre, or audio |
| Input-note rank selection | Not included in the current relative profile | Distinguish pitch order and input order from harmonic degree |
| Notation and performance | Gate duration and lyric alignment defined | Notated values, ties, voices, enharmonic spelling, and tuplets |
| Detailed percussion | Slot IDs, roles, and output hints | Instrument-specific maps, choke behavior, and articulations |
| Expression | No Core velocity | Whether and how an optional profile should cover expression |
| Multiple harmonic contexts | Overlap and explicit context IDs allowed | Lanes, display precedence, and local contexts |
| Numeric limits | Existing bounds adopted as the initial baseline | Revisit in a later version with explicit compatibility consequences |
| External products | No support is presumed | Actual adapters and interoperability tests |

The goal is to let a small generator participate by writing adopted notes,
while allowing a more capable implementation to add compositional relationships
on the same foundation.

## 15. Design references

The source-backed rationale is listed in the
[Japanese specification, Section 15](FORMAT_SPECIFICATION.ja.md#15-設計判断の根拠).
It covers relative phrases versus realized notes, pickup and tail preservation,
protected regeneration, input-note rank versus harmonic degree, independent chord
and accompaniment cycles, percussion mapping, gate versus notation duration,
melody-first workflows, and multiple generation inputs.

Those references inform the design. They do not claim that any named product
implements OSTF or has been tested with this package.

## 16. Change record

Draft 1 places the authoritative adopted performance in `tracks` and defines
pitch or percussion target, onset, and gate duration. It defines declared PPQ,
notes crossing placement boundaries, same-pitch overlaps, stable IDs, structured
harmony, and many-to-many lyric alignment. It introduces extension status and
dependencies, three standard optional profiles, and conservative migration with
original-source preservation.

Draft 2 retains those Core semantics and adds phrase-library and clip-choice
profiles. It defines finite repetition and transposition of concrete templates,
complete Core-note correspondence, candidate selection reflected in `clip.enabled`,
explicit materialization and selection, and fixed before/after protection checks.
Root-version dispatch and explicit conversion preserve the original profile
versions. The conservative 2.3 converter advances its output root version to
Draft 2. Automatic regeneration, whole-song scenes, and audio or MIDI engine
execution are not introduced.

Draft 2 Revision 1 retains the wire version and both schemas while adding
`replace_phrase_template` and `detach_phrase_instances`. Replacement refreshes all
linked instances of a current template in one transaction, retains existing Core
IDs for surviving occurrences, and checks Core lyric references to removed notes
and supplied protection. Detachment removes relationships while preserving Core,
lyrics, identities, mute states, array order, and the phrase envelope's original
status. Both operations leave caller inputs unchanged and expose no partial result
on failure. Automatic synchronization, time scaling, harmony fitting, and an
override layer are not added.

Draft 2 Revision 2 closes the initial feature scope, separates later extensions,
and records public-draft readiness and remaining stable-release tasks. It aligns
the languages on strict integers in supported profiles and non-invalidation for
an identical current candidate selection. Code, schemas, samples, and historical
execution results are retained; no additional runtime verification is performed.

3.0.0 adds the stable Core root and schema while retaining both historical
schemas unchanged. All six provisional profile versions and meanings, and all
existing editing safeguards, are preserved. Phrase and choice operations accept
Draft 2 and stable documents. `convert_version` supports all three roots; the
legacy `convert_draft_version`, `upgrade`, and `downgrade` remain draft-only.
2.3 migration and default schema selection now target 3.0.0. The formal distribution organizes 60 stable examples and two legacy inputs, complete manuals, parameter references, coverage and license notices. This documentation work does not change the established Core/schema/reference-code semantics. No runtime verification was performed. [LICENSE.md](../LICENSE.md) states the release terms.

Subsequent changes must identify whether they affect Core, profiles, migration, or
verification. Incompatible changes require an appropriate version change.

