# OSTF 3.0.0 — Complete authoring and implementation manual

This manual explains every defined parameter family, its musical purpose, and the workflow around it. The wire version is **`3.0.0`**. The six bundled optional profiles retain the exact provisional version **`1.0.0-draft.1`**. A stable Core version does not make those profiles stable.

Read the [parameter reference](PARAMETER_REFERENCE.en.md) for every declaration, type, requiredness, bound, enum, conditional rule, and Schema location. The [machine catalog](PARAMETER_CATALOG.json) makes that inventory accessible to tools. The [coverage report](COVERAGE.md) connects declarations and finite choices to the [sample collection](../samples/INDEX.md). The [format specification](FORMAT_SPECIFICATION.en.md) and [JSON Schema](../schema/ostf-3.0.0.schema.json) are the normative sources; this manual explains them without adding fields or new conformance requirements. [日本語版](COMPLETE_MANUAL.ja.md).

The release examples and commands are authored documentation. Runtime, DAW, MIDI, and interoperability verification were not performed for this release preparation. Field coverage is a documentation inventory, not a statement that every program behavior has passed a test.

## 1. What a file communicates

OSTF stores a composition in a form that another application can understand even when it cannot reproduce the original generator. A file can hold song sections, chords and scales, explicit instrument-part notes, lyrics, source references, and optional relationships such as reusable phrases or alternative clip sets.

The adopted note performance is stored in **`tracks → clips → notes`**. Every note states its target, onset, and gate. Core has no velocity, MIDI channel, controller, pitch bend, synthesizer state, audio-track playback, or score-engraving model. A host may choose sounds and playback dynamics, but those choices are not portable Core parameters.

Three kinds of information coexist:

| Layer | Authoring responsibility | Reader responsibility |
| --- | --- | --- |
| Core | Save the concrete finite notes currently adopted by the author | Read the saved music directly |
| Standard optional profile | Save an explicitly versioned relationship, together with its status and dependencies | Interpret only supported exact versions |
| Vendor extension | Save settings or data whose meaning belongs to the producer | Preserve unknown values without inventing their meaning |

Loading does not generate notes, re-roll randomness, apply candidate selection, refresh a phrase, or reinterpret a source archive. If a generator changes a phrase, the writer updates the adopted Core notes through an explicit operation. Optional data must not cause a second copy of those notes to play.

Harmony-only, melody-only, lyrics-only, and empty sketches are legitimate documents. A chord-only file states harmonic intent; it does not claim that accompaniment notes already exist. Start with samples [02](../samples/02_empty_sketch.ostf), [03](../samples/03_harmony_only.ostf), [04](../samples/04_melody_only.ostf), and [05](../samples/05_lyrics_only.ostf).

## 2. Start with the eleven root members

Every `.ostf` file contains one UTF-8 JSON object with these members. Containers remain present even when their arrays or objects are empty.

| Member | Authoring instruction |
| --- | --- |
| `format` | Write the exact string `OSTF`. |
| `version` | Write `3.0.0` for a new stable Core document. |
| `ppq` | Choose one integer tick resolution for the whole document: 1–960000; 960 is recommended. |
| `song` | Supply at least `title`. |
| `timeline` | Supply `sections`, `tempoChanges`, and `meterChanges`. |
| `harmony` | Supply `chords` and `scales`. |
| `tracks` | Supply the ordered array of performed parts, possibly empty. |
| `soundSlots` | Supply percussion target definitions, possibly empty. |
| `lyrics` | Supply `documents`, `phrases`, `units`, and `alignments`. |
| `resources` | Supply source/material references, possibly empty. |
| `extensions` | Supply a namespace-to-envelope object, possibly `{}`. |

Here is a complete empty sketch, with a title intentionally left blank:

```json
{
  "format": "OSTF",
  "version": "3.0.0",
  "ppq": 960,
  "song": { "title": "" },
  "timeline": {
    "sections": [],
    "tempoChanges": [{ "at": 0, "bpm": 120 }],
    "meterChanges": [{ "at": 0, "numerator": 4, "denominator": 4 }]
  },
  "harmony": { "chords": [], "scales": [] },
  "tracks": [],
  "soundSlots": [],
  "lyrics": { "documents": [], "phrases": [], "units": [], "alignments": [] },
  "resources": [],
  "extensions": {}
}
```

Core objects are closed. Put additional settings inside a namespaced extension instead of adding undeclared fields to notes or tracks. An optional field can be omitted; that does not generally permit `null`. `selectedCandidateId` is an explicit exception that allows `null`.

## 3. Numbers, identity, and references

### 3.1 Integer representation and exact values

Strict input rejects a UTF-8 byte-order mark, invalid UTF-8, duplicate object keys, unpaired Unicode surrogates, `NaN`, `Infinity`, non-finite numbers, and non-whitespace content after the one root object. A permissive parser can erase evidence of duplicate keys or number-token form, so enforce these rules before that information is lost.

An integer field must use a JSON integer token: `1` is permitted; `1.0`, `1e0`, and `true` are not integer-field representations. General JSON Schema software may treat a mathematically whole real number as an integer, so this lexical rule needs attention at the parser boundary.

The common tick limit is `MAX = 9007199254740991`. Nonnegative positions range from 0 to MAX; positive durations from 1 to MAX; signed note-local positions from −MAX to MAX. Individual fields such as pitch, PPQ, meter, and transpose have smaller limits. Check calculated ends and sums as well as individual operands.

Opaque extension values are not limited to binary64 precision. Finite decimal numbers such as `1e400`, `1e-400`, and high-precision fractional values can be retained as JSON values. A writer claiming lossless unknown-data preservation must retain numeric value and integer-versus-real token category. Whitespace and object-key spelling/order preservation is a separate promise. Sample [18](../samples/18_opaque_precision.ostf) illustrates precision; [21](../samples/21_integer_boundary.ostf) illustrates integer limits.

### 3.2 Core IDs and local IDs

All Core `id` values share one document-wide namespace across all object kinds. They are 1–128 ASCII characters, matching `^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$`. Use identities that remain stable when an object moves or its name changes. Assign new IDs to independent copies.

Profile-local template IDs, template-note IDs, instance IDs, process IDs, custom-role IDs, group IDs, and candidate IDs use their declared local scopes. A local note ID inside a template does not register another Core note. Do not recursively index arbitrary vendor `data` as Core objects.

### 3.3 Typed references and ranges

A `Ref` has `type` and `id`. The complete `type` vocabulary is `section`, `track`, `clip`, `note`, `chord`, `scale`, `soundSlot`, `lyricDocument`, `lyricPhrase`, `lyricUnit`, `lyricAlignment`, and `resource`. The referenced ID must identify that exact kind. A matching string under a different kind does not satisfy the reference.

A global `Range` has `start` and `duration`, both in document ticks. Its start is nonnegative, its duration positive, and their sum must not exceed MAX. `readRange` and `targetRange` use this same definition. Samples [41](../samples/41_generation_all_ref_types.ostf) and [43](../samples/43_appearance_all_targets.ostf) show all typed target kinds.

## 4. Song information and the timeline

| Object/member | Required? | Meaning and use |
| --- | --- | --- |
| `song.title` | Yes | Display title; an empty string is valid. |
| `song.primaryMelodyTrackId` | No | Existing Core track selected as the main melody. It does not create another part. |
| `sections[].id` | Yes | Core identity of a song section. |
| `sections[].name` | Yes | Nonempty display name, such as “Verse 1.” |
| `sections[].start`, `duration` | Yes | Global placement and positive span. |
| `sections[].role` | No | Open string for musical/form role; it is not a fixed enum. |
| `tempoChanges[].at` | Yes | Global tick at which the next tempo begins. |
| `tempoChanges[].bpm` | Yes | Finite quarter notes per minute, greater than 0 and at most 1000. |
| `meterChanges[].at` | Yes | Exact global tick of the meter change. |
| `meterChanges[].numerator` | Yes | Integer 1–64. |
| `meterChanges[].denominator` | Yes | One of 1, 2, 4, 8, 16, 32, 64. |

Sections are ordered by start and do not overlap; gaps and an empty section list are allowed. Notes may cross section boundaries. Tempo and meter maps each begin at tick 0 and thereafter strictly increase in `at`. A host must not move a map change to an inferred bar boundary.

Tempo always measures quarter notes, including in 6/8 or another compound meter. For a constant-tempo segment, `seconds = ticks × 60 / ppq / bpm`. Split a note's time calculation at tempo changes. Meter changes do not alter tick resolution. Bar numbering, including pickup numbering, belongs to presentation.

At PPQ 960 an eighth-note grid is 480 ticks, a sixteenth-note grid 240, and one third of a quarter note 320. Seven equal divisions of a quarter cannot be exact at that PPQ; sample [07](../samples/07_septuplets.ostf) uses a suitable resolution. A gate of 432 on a 480-tick grid is an example of 90% articulation, not a format default. See [11](../samples/11_meter_tempo_gaps.ostf), [36](../samples/36_all_meter_denominators.ostf), [48](../samples/48_ppq_minimum.ostf), and [49](../samples/49_ppq_maximum.ostf).

## 5. Harmony: labels, spelling, and intervals

`harmony.chords` and `harmony.scales` are independently ordered by nondecreasing start. Contexts may overlap. A relationship selects a context by ID instead of relying on which array entry happens to come first.

| Structure/member | Required? | Meaning |
| --- | --- | --- |
| Spelled pitch class `step` | Yes | One of A, B, C, D, E, F, G. |
| Spelled pitch class `alter` | Yes | Integer −2…2; no octave is included. |
| Chord `id`, `start`, `duration` | Yes | Core identity and global span. |
| Chord `label` | Yes | Nonempty display text. A label-only chord is valid. |
| Chord `root`, `intervals` | Paired optional | Supply both or neither. The root is a spelled pitch class. Intervals are nonempty, distinct, strictly increasing integer semitone distances 0…35, including 0. |
| Chord `bass` | No | Spelled bass pitch class; does not generate a bass note. |
| Scale `id`, `start`, `duration` | Yes | Core identity and global span. |
| Scale `label` | No | Display text. |
| Scale `tonic` | Yes | Spelled pitch class. |
| Scale `intervals` | Yes | Nonempty, distinct, strictly increasing integers 0…11, including 0. |

Natural pitch classes are C=0, D=2, E=4, F=5, G=7, A=9, B=11. Add `alter` and normalize modulo 12. Preserve the spelling: C sharp and D flat need not be rewritten into each other.

A chord interval of 14 conveys an extension above the root and must not be reduced to 2. The interval list is harmonic structure, not a performed voicing. Core notes can contain passing tones or dissonances outside these lists. Harmony does not constrain all notes and does not automatically produce accompaniment.

Samples [03](../samples/03_harmony_only.ostf), [34](../samples/34_all_core_fields.ostf), and [35](../samples/35_pitch_class_spellings.ostf) cover label-only and structured harmony. Relative-note examples [12](../samples/12_relative_chord.ostf), [13](../samples/13_relative_scale.ostf), [39](../samples/39_relative_objects.ostf), and [40](../samples/40_relative_interval_limits.ostf) add optional relationships.

## 6. Tracks, clips, and notes

### 6.1 All performance parameters

| Object/member | Required? | Authoring instruction |
| --- | --- | --- |
| Track `id`, `name` | Yes | Stable Core ID and display name. |
| Track `role` | No | Open musical-function string, such as a host's melody or bass role. |
| Track `instrument` | No | Object requiring `name` and optionally `family`; describes an instrument without loading a plug-in. |
| Track `enabled` | No | Boolean; omission means true. |
| Track `clips` | Yes | Array ordered by nondecreasing clip start. |
| Clip `id` | Yes | Stable Core ID. |
| Clip `name` | No | Display name. |
| Clip `start` | Yes | Nonnegative global tick. |
| Clip `duration` | Yes | Positive placement/editing span. |
| Clip `enabled` | No | Boolean; omission means true. |
| Clip `notes` | Yes | Array ordered by nondecreasing local start. |
| Note `id` | Yes | Stable Core ID, distinct for each occurrence. |
| Note `start` | Yes | Signed offset from the clip start. |
| Note `duration` | Yes | Positive gate/hold duration in ticks. |
| Note `pitch` | Exactly one target | Integer 0…127; C4=60, A4=69, reference tuning A4=440 Hz. |
| Note `soundSlotId` | Exactly one target | Existing percussion sound-slot ID. |

`pitch` and `soundSlotId` are mutually exclusive and cannot both be absent. An instrument's `name` and `family`, and all Core `role` fields, are descriptions rather than standardized sound routing. Arpeggiation is a playing method, not an instrument identity.

### 6.2 Placement span and gate are different

For every note:

```text
absolute onset = clip.start + note.start
absolute gate end = absolute onset + note.duration
```

Absolute onset must be nonnegative; both sums must remain at or below MAX. Also check `clip.start + clip.duration`. A negative local start can represent a pickup if the clip is placed late enough. A note can start after the clip's placement span or finish beyond it. A clip/section boundary does not crop the note.

For a clip starting at tick 120 with duration 960, a local note at −120 for 240 ticks plays from 0 to 240. Another at 720 for 480 plays from 840 to 1320, after the clip span ends at 1080. These are deliberate timing relationships, not malformed placement.

Gate measures how long a note is held. It is not audio release time, reverb duration, or a notated tied value. Two notes of the same pitch can overlap and retain independent identities. Do not merge them on import. Samples [08](../samples/08_pickups_tails.ostf), [09](../samples/09_same_pitch_overlap.ostf), and [24](../samples/24_phrase_late_overlap.ostf) illustrate these cases.

### 6.3 Enabled state and event order

A note contributes to the adopted active performance only when both its track and its clip are enabled. Disabled content is still retained and validated. There is no Core per-note mute or solo field. An exporter translates its adopted solo/mute result into the available Core states or adopted note arrays.

Track array order is display order. Clips and notes allow equal starts and preserve equal-start array order. Event extraction has a separate deterministic order: absolute tick, then all `noteOff` events before all `noteOn` events, then lexicographic `noteId` within the same tick and event kind. Each event carries `noteId`, `trackId`, `clipId`, and the note's target.

Performance end is the maximum enabled note gate end, or zero when there are no active notes. It is not the last section or clip end. Stop/seek behavior and a destination's ability to handle overlapping equal pitches belong to the host. Samples [10](../samples/10_enabled_states.ostf) and [47](../samples/47_pitch_boundaries.ostf) cover states and pitch limits.

## 7. Percussion and referenced resources

| Object/member | Required? | Meaning |
| --- | --- | --- |
| Sound slot `id`, `name` | Yes | Identity and display label of an unpitched target. |
| Sound slot `role` | No | Open role string; repeated roles are allowed. |
| Sound slot `midiNote` | No | Integer 0…127 mapping hint for an output. |
| Resource `id` | Yes | Core identity. |
| Resource `kind` | Yes | `audio`, `midi`, `text`, or `other`. |
| Resource `uri` | Yes | Nonempty reference string. |
| Resource `name` | No | Display name. |
| Resource `sha256` | No | Exactly 64 lowercase hexadecimal characters. |

Two sound slots can have the same role or MIDI-note hint and still be independent. `midiNote` does not assert General MIDI conformance. Assigning an actual sound is a host decision; an unmapped slot remains meaningful stored data. A pitched 808 line uses `pitch` notes if semitone pitch is the intended meaning. See [06](../samples/06_percussion_slots.ostf) and [23](../samples/23_phrase_percussion.ostf).

A resource is referenced material, potentially a generation input. Its presence does not start an audio track or authorize automatic fetching or execution. A missing file does not invalidate the stored note structure. Resolving relative URIs and checking resource hashes are explicit host operations. Sample [37](../samples/37_resource_kinds.ostf) covers all four resource kinds.

## 8. Lyrics and many-to-many alignment

| Object/member | Required? | Meaning |
| --- | --- | --- |
| Document `id` | Yes | Core identity of one lyric document. |
| Document `title`, `language` | No | Auxiliary strings for display and language. |
| Phrase `id`, `documentId`, `text` | Yes | Phrase identity, parent lyric document, and displayed phrase text. |
| Phrase `pronunciation` | No | Pronunciation annotation. |
| Phrase `start`, `duration` | Paired optional | Both present or both absent; global timeline timing. |
| Unit `id`, `phraseId`, `text` | Yes | Unit identity, parent phrase, and displayed unit text. |
| Unit `pronunciation` | No | Pronunciation annotation independent of display text. |
| Unit `start`, `duration` | Paired optional | Both present or both absent; global timing. |
| Alignment `id` | Yes | Core identity of the relation. |
| Alignment `unitIds`, `noteIds` | Yes | Ordered, nonempty, duplicate-free lists of existing lyric-unit and Core-note IDs. |

Phrase text remains the displayed phrase; concatenating unit text need not reproduce it. Language-specific segmentation and phoneme alphabets are not standardized here. Timed units use global positions even when their notes use clip-local positions.

An alignment can connect one unit to several notes, several units to one note, or several of each. This accommodates melisma and other grouping without inventing duplicated words or notes. Alignment does not create notes or imply a singing-synthesis voice. Untimed lyrics remain valid. See [05](../samples/05_lyrics_only.ostf), [20](../samples/20_lyric_alignment.ostf), and [46](../samples/46_lyrics_multilingual.ostf).

## 9. Extension envelopes and safe editing

### 9.1 Namespace and every envelope member

An extension key uses reverse-domain-style grammar `^[a-z][a-z0-9-]*(?:\.[a-z][a-z0-9-]*){2,}$`. It has at least three components. This naming convention is not proof of authorship.

| Member | Meaning |
| --- | --- |
| `version` | Nonempty exact profile version string. |
| `status` | `current`, `stale`, or `unverified`. |
| `dependencies` | One of the three shapes below. |
| `data` | Any JSON value for an unknown profile; the declared data shape for an exact supported profile. |

All four envelope members are required and extra envelope members are forbidden. Arbitrary vendor fields go inside `data`.

| Dependency form | Use |
| --- | --- |
| `{"scope":"document"}` | The relation depends on the document or cannot be safely narrowed. |
| `{"scope":"none"}` | No dependency on current Core objects. |
| `{"scope":"objects","refs":[...]}` | Explicit nonempty, duplicate-free typed references. |

For a current supported profile, object scope must include every direct Core reference in its data. Local profile IDs are not Core refs. Dependency meaning includes ancestry: moving a clip changes its notes' global times, and muting a parent changes effective note state. Prefer document scope when the needed dependency set is uncertain.

### 9.2 Status is a relationship claim

`current` means the producer declares correspondence with the current saved document. `stale` means a relevant change is known to have broken it. `unverified` means correspondence has not been established or cannot be checked by the current editor. None of these switches playback away from Core, and `current` does not certify that an unknown generator was reproduced.

A current dependency ref must resolve. Missing refs in stale/unverified extension relationships are retained with warnings; broken Core refs remain errors. A known payload with malformed structure is an error in every status. Status relaxes correspondence checks, not JSON or the supported data schema.

After a relevant edit, either update an understood relationship and adopted Core content together, or set the relation stale/unverified. Preserve unknown `data` intact and express uncertainty through the envelope. The reference invalidator uses `unverified`; an editor that knows a relationship is broken may use `stale` under the format contract. Status changes alone are not recursive musical edits.

### 9.3 Unknown versions and preservation

Dispatch by both namespace and exact version. A future version of a familiar namespace remains opaque; do not apply the older payload schema to it. The envelope and declared dependencies still have meaning. A Core reader can use saved notes without knowing any profile, while a reference validator that explicitly supports a profile checks that profile's known structure. These are different capability statements.

Samples [14](../samples/14_stale_source.ostf), [15](../samples/15_unverified_source.ostf), [19](../samples/19_future_profile.ostf), [38](../samples/38_dependency_scopes.ostf), [51](../samples/51_opaque_json_values.ostf), and [52](../samples/52_stale_missing_references.ostf) explain this lifecycle.

## 10. Relative-note profile

Namespace: **`org.ostf.relative-phrase.v1`**. `data.assignments` is required and may be empty. Each assignment has all six members below.

| Member | Meaning |
| --- | --- |
| `noteId` | Pitched Core note; each target occurs at most once in the assignments. |
| `basis` | `chordTone` or `scaleDegree`. |
| `contextId` | Chord ID for chordTone; scale ID for scaleDegree. |
| `anchorPitch` | Actual octave-specific root/tonic pitch, integer 0…127. |
| `index` | One-based index in the context's ordered interval array; structural maximum 36 for chordTone, 12 for scaleDegree. |
| `chromaticOffset` | Integer semitone adjustment −24…24. |

For current data, the index must also fit the actual interval array, the anchor pitch class must match the root/tonic, and `anchorPitch + intervals[index − 1] + chromaticOffset` must equal the saved Core pitch in 0…127. A chord-based context must supply structured `root` and `intervals`.

The index is an array position, not a chord-symbol interval label. A pickup can refer to a context outside its onset span. Stale or unverified correspondence is retained as a warning; no pitch is overwritten on load. Optimal register, voice leading, chord-aware fitting, and input-note rank interpretation are not part of this version. Samples 12, 13, 39, and 40 provide complete files.

## 11. Generation-context profile

Namespace: **`org.ostf.generation-context.v1`**. `data.processes` is required and may be empty.

| Structure/member | Required? | Meaning |
| --- | --- | --- |
| Process `id` | Yes | Unique local process identity. |
| Process `generator` | Yes | Object with nonempty `id` and `version`; identifies the generating engine. |
| Process `inputs` | Yes | Array of source records; may be empty or contain several sources. |
| Input `role` | Yes | Nonempty source-purpose string. |
| Input `ref` | Yes | Typed Core reference. |
| Input `readRange` | No | Global range read from the source. |
| Process `outputs` | Yes | Nonempty array of typed Core refs. |
| Process `targetRange` | No | Global range requested for editing. |
| Process `protectedNoteIds` | Yes | Duplicate-free Core-note IDs; empty is allowed. |
| Process `vendorExtension` | No | Namespace of another extension in the same document. |

For current data, inputs, outputs, protected notes, and a referenced vendor extension must exist. A `vendorExtension` reference requires document dependency; self-reference to generation-context is an error in every status. A missing vendor reference or non-document scope is retained with a warning for stale/unverified data.

Read range, requested target range, and complete produced-note span can differ because of pickups and tails. Multiple inputs must remain distinct. Values such as seed, complexity, style strength, and humanize are not standardized cross-engine parameters: place them in vendor data and identify the engine/version.

Protection constrains an operation to preserve note identity, target, absolute onset, gate, and effective enabled state. A saved list alone cannot prove a historical operation obeyed it; before/after comparison is necessary for that claim. Samples [16](../samples/16_generation_context.ostf), [41](../samples/41_generation_all_ref_types.ostf), and [42](../samples/42_generation_protected_range.ostf) cover sources and protection.

## 12. Appearance profile

Namespace: **`org.ostf.appearance.v1`**. Required `data` members are `roleDefinitions`, `sectionRoleAssignments`, and `appearance`.

| Structure/member | Meaning |
| --- | --- |
| `roleDefinitions[].id` | Unique profile-local role ID. |
| `roleDefinitions[].name` | Required nonempty display name. |
| `roleDefinitions[].baseRole` | Optional open string used for fallback role color. |
| `sectionRoleAssignments` | Map from Core section IDs to local role IDs. |
| `appearance.roleColors` | Required map from arbitrary role strings to colors. |
| `appearance.customRoleColors` | Required map from custom-role IDs to colors. |
| `appearance.objectColors` | Required array of `target` typed ref plus `color`. |

Empty maps and arrays are permitted. Color strings use exactly `#RRGGBB`, with either case for hexadecimal letters. Duplicate typed targets in `objectColors` are invalid. Current assignments and references must resolve.

| Target | First available color wins, left to right |
| --- | --- |
| Section | Own color → assigned custom-role color → custom role's base-role color → Core section-role color → host default |
| Track or sound slot | Own color → Core role color → host default |
| Clip | Own color → resolved parent-track color |
| Note | Own color → resolved parent-clip color |
| Other Core kind | Own color → host default |

A section's temporal overlap never implicitly colors its notes. Resolvable stale/unverified colors can still be displayed; missing targets must not be redirected. Appearance does not change performance. This namespace is distinct from the old 2.3 `org.ostf.section-role-appearance.v1`. See [17](../samples/17_appearance.ostf), [43](../samples/43_appearance_all_targets.ostf), and [44](../samples/44_appearance_inheritance.ostf).

## 13. Reusable phrase-library profile

Namespace: **`org.ostf.phrase-library.v1`**. Required `data.templates` and `data.instances` may both be empty.

| Structure/member | Meaning |
| --- | --- |
| Template `id` | Local unique template identity. |
| Template `name` | Optional display string. |
| Template `duration` | Positive repeat period in document ticks. |
| Template `notes` | Required array using the Core-note field shape; note IDs are local to that template. |
| Instance `id` | Local unique instance identity. |
| Instance `templateId` | Source template's local ID. |
| Instance `clipId` | Owned Core clip. |
| Instance `repeatCount` | Integer 1…MAX. |
| Instance `transpose` | Integer −127…127 semitones. |
| Instance `noteMap` | Required occurrence-map array. |
| Mapping `templateNoteId` | Source note's local ID. |
| Mapping `repeatIndex` | Zero-based repeat index, integer 0…MAX; for current data it is below repeatCount. |
| Mapping `noteId` | Realized Core-note ID. |

Template notes do not play. A current instance must correspond exactly to one existing Core clip, whose entire note array is covered by the map. The equations are:

```text
clip.duration = template.duration × repeatCount
note.start = repeatIndex × template.duration + templateNote.start
note.duration = templateNote.duration
pitched note.pitch = templateNote.pitch + transpose
unpitched note.soundSlotId = templateNote.soundSlotId
```

One template can have many instances; one clip has at most one instance owner. Each `(repeatIndex, templateNoteId)` maps once, and mapped Core-note IDs are unique across the library. Template IDs and instance IDs have separate local scopes; source note IDs are unique within a template.

Signed starts, late starts, repeat overlap, pickups, and tails remain intact. Transposition does not change a sound-slot identity. Any calculated pitch or time outside Core limits is rejected instead of clamped. An empty template can have an empty realization, but the clip span must still fit the time limit. Cardinality and supplied-map uniqueness establish coverage without expanding every possible repetition during validation.

Structural ambiguity and conflicting ownership are always errors. Missing links and realization mismatches are errors when current and warnings when stale/unverified. One envelope status covers the entire library. A manually added unmapped note in an owned clip means the current exact-realization relation no longer holds; detach or explicitly revise the relationship. Document dependency is recommended; direct object dependencies include slots, clips, and mapped Core notes, not local IDs.

Read samples [22](../samples/22_phrase_library.ostf)–24, [30](../samples/30_template_before_materialization.ostf)–33, [53](../samples/53_phrase_empty_template.ostf), [54](../samples/54_phrase_objects_dependencies.ostf), and [59](../samples/59_phrase_transpose_limits.ostf). This profile does not define nested templates, probability, time scaling, chord fitting, or per-note overrides.

## 14. Clip-choice profile

Namespace: **`org.ostf.clip-choices.v1`**. `data.groups` is required and may be empty.

| Structure/member | Meaning |
| --- | --- |
| Group `id` | Local unique group identity. |
| Group `name` | Optional display string. |
| Group `candidates` | Required nonempty array. |
| Group `selectedCandidateId` | Required local candidate ID or explicit `null`. |
| Candidate `id` | Local identity unique within its group. |
| Candidate `name` | Optional display string. |
| Candidate `clipIds` | Required ordered, duplicate-free list of Core clips; may be empty. |

A group's managed set is the union of its candidate clip lists. Shared clips inside one group are allowed; management by two groups is forbidden. When current, a managed clip's own `enabled` flag equals membership in the selected candidate. A null selection disables all managed clips. An empty candidate represents a named silent option and is distinct in metadata from no selection.

Track mute remains independent. A selected clip can be silent under a disabled track. Unmanaged clips remain untouched. Current references and selection must resolve; stale/unverified mismatches remain warnings, while duplicate IDs and ownership ambiguity remain errors. Every candidate clip, including unselected ones, counts toward dependencies.

The profile selects already materialized performance clips. Harmony, sections, lyrics, routing, and transport are not switched by it. Loading does not apply selection or repair flags. See [25](../samples/25_choice_shared_muted.ostf), [26](../samples/26_choice_none.ostf), [55](../samples/55_choice_empty_candidate.ostf), [56](../samples/56_choice_disjoint_groups.ostf), and [57](../samples/57_choice_objects_dependencies.ostf).

## 15. Legacy-source archive profile

Namespace: **`org.ostf.legacy-import.v1`**. This profile preserves source evidence rather than an alternative performance. It requires document dependency and cannot claim `current`.

| Required `data` member | Meaning |
| --- | --- |
| `sourceVersion` | Exact `2.3.0`. |
| `sourceSha256` | SHA-256 of the original UTF-8 source bytes, 64 lowercase hexadecimal characters. |
| `sourceText` | Complete nonempty original text; UTF-8 re-encoding must recreate the hashed bytes. |
| `conversionReport` | JSON object describing the conversion; the wire profile does not impose a universal nested report schema. |

Keep original line endings, numeric spellings, escapes, and other source text in the decoded string. JSON escaping of that string in a new file does not change its contents. Do not update the archive to pretend that later Core edits were present in the source. The converter normally sets `unverified`; `stale` remains an allowed non-current archive state under the declared rules. Sample [45](../samples/45_legacy_import_archive.ostf) and the separately labeled [legacy 2.3 inputs](../samples/legacy_2_3/) illustrate the distinction.

## 16. Explicit editing operations

All editing APIs return copies, validate before and after, and leave caller documents, replacement objects, and ID lists unchanged. Failure exposes no partially edited result. These contracts describe the supplied implementation; they do not state that commands were run during this preparation. Full details and diagnostic codes are in [OPERATIONS.md](OPERATIONS.md).

| API | Inputs and result |
| --- | --- |
| `convert_version(document, target_version=VERSION)` | Converts among Draft 1, Draft 2, and stable roots; default target `3.0.0`. |
| `convert_draft_version(document, target_version)` | Compatibility API with required target; both endpoints must be draft roots. |
| `materialize_phrase(document, template_id, *, instance_id, track_id, clip_id, start, repeat_count=1, transpose=0, enabled=True, max_notes=100000)` | Adds a new Core clip and linked instance from a current phrase library. |
| `activate_candidate(document, group_id, candidate_id, *, protected_note_ids=())` | Applies one group's candidate or `None`, retaining track mute and unmanaged clips. |
| `replace_phrase_template(document, template_id, replacement, *, protected_note_ids=(), max_notes=100000)` | Replaces a complete template and refreshes every linked instance atomically. |
| `detach_phrase_instances(document, instance_ids, *, protected_note_ids=())` | Removes selected instance records while preserving all Core objects and templates. |
| `check_protected_notes(before, after, note_ids)` | Compares the fixed note set between valid equal-PPQ documents. |
| `check_generation_protection(before, after, process_id)` | Takes the fixed protection set from before's current generation process. |

Phrase and choice editing requires Draft 2 or stable Core plus the exact supported profile. Materialization and replacement require a current phrase library. Detachment accepts current/stale/unverified libraries that remain structurally valid. Candidate activation may accept any of those states, but all necessary references must resolve and the whole choice profile must validate current afterward; it does not repair other groups as a side effect.

### 16.1 Materialization and replacement

New reference-operation note IDs are `note.` followed by SHA-256 of UTF-8 compact JSON `[instanceId, repeatIndex, templateNoteId]`, without spaces. This is an operation policy, not a requirement that all valid Core IDs use hashes. Core notes are sorted by local start, repeat index, then source-array index; maps are ordered by repeat index and source-array index.

Replacement consumes one complete template object with the same template ID. Surviving occurrence keys keep their original mapped Core IDs, including custom IDs. Renaming a source note is removal plus addition. Original IDs, including removed ones, remain reserved during the transaction; collisions reject it. If removing a Core note would break a lyric alignment, the operation fails with `OPERATION_REFERENCED_NOTE_REMOVAL` instead of deleting lyric data.

`max_notes=100000` is an explicit reference-operation resource limit, not the format's repeat or note limit. For replacement it bounds the total resulting notes across all affected instances before expansion. One invalid instance rejects the entire update. Empty templates do not enumerate huge empty repetition loops. Exact no-op replacement preserves order/status; name-only change preserves Core and map order while applying the metadata/dependency update.

### 16.2 Detachment and protection

Detachment removes only selected instance links. It retains Core notes, IDs, times, lyrics, mute states, order, templates, and the phrase envelope's prior status and dependencies. Empty API input is a validated no-op; duplicate or missing instance IDs reject the entire request. Detaching the last mismatch does not automatically promote a stale library.

Protection compares existence, target, absolute onset, gate, and effective enabled state, including inactive notes. A parent change is allowed if those properties remain the same. Different PPQ produces `PROTECTION_PPQ_MISMATCH`; elapsed seconds, tempo, timbre, and acoustic release are not protected by this tick-based comparator. Removing the protection list from the after snapshot cannot evade a before-based generation check.

Nontrivial edits conservatively invalidate other dependent current profiles. No-op operations do not manufacture unrelated invalidations. See samples 30–33 for authored before/after relationships and [58](../samples/58_complete_workflow.ostf) for combined features.

## 17. Reference reader and support levels

Use Python 3.10 or later with the supplied `requirements.txt` when using the reference implementation. Keep the Python modules with the bundled `schema/` directory. Schemas are resolved locally. The [implementation guide](REFERENCE_IMPLEMENTATION.md) gives complete return shapes, diagnostics, and serializer behavior.

| API | Purpose and important parameters |
| --- | --- |
| `load_strict(source)` | Accept bytes or text; preserve exact number category; enforce strict JSON ingress. It is not full OSTF validation. |
| `dump_strict(value, *, indent=2, sort_keys=False)` | Serialize supported strict JSON values; `indent=None` is compact. It does not by itself establish OSTF validity. |
| `validate_document(doc)` | Return diagnostics for wire/in-memory structure, selected schema, and semantics. |
| `realized_events(doc)` | Return sorted active Core events after validation. |
| `performance_end(doc)` | Return latest active gate end, or 0, after validation. |
| `resolve_color(doc, target, default_color="#808080")` | Resolve a typed Core target's display color. |
| `invalidate_extensions(doc, changed_refs=None)` | Return a copy marking affected current claims unverified; include changed typed refs when known, or conservatively omit the set. |
| `get_schema(version=VERSION)` | Return a copy of the exact bundled schema; default stable. |
| `schema_self_check(version=VERSION)` | Check a selected bundled schema when explicitly invoked. |

`VERSION` is `3.0.0`; `DRAFT1_VERSION` and `DRAFT2_VERSION` identify the two retained drafts. `SUPPORTED_VERSIONS`, `SCHEMA_PATHS`, and `SUPPORTED_PROFILES_BY_VERSION` describe dispatch. `PROFILE_VERSION` remains `1.0.0-draft.1`. `JsonReal` retains exact real-number tokens; use the strict writer for documents read by the strict reader.

A diagnostic contains `severity`, `code`, `path`, and `message`. Paths are JSON Pointers; an empty path denotes the root. Use codes and fields rather than comparing English message wording or assuming a fixed order. Warnings do not automatically invalidate a document. `WireError`, `DocumentValidationError`, `OperationError`, and `MigrationError` distinguish different failure boundaries; installation/resource failures are not ordinary musical-format diagnostics.

Declare capabilities separately: Core export, Core reading/playback, lossless editing of unknown data, each profile's interpretation, each explicit editing operation, and proprietary regeneration. A Core-only exporter does not need to create all profiles. The supplied validator checks every exact profile it supports, so it can reject known malformed profile data even though another Core-only consumer has a narrower capability claim.

## 18. Complete command-line option map

All CLIs and editor subcommands also accept the standard `-h` / `--help` option to display argument help. These are documented usage options, not commands executed for this release.

Commands below are usage documentation. They were not executed for this package.

### Validator

`python ostf3_validate.py [files ...] [options]`

| Argument/option | Meaning |
| --- | --- |
| `files` | Zero or more paths as allowed by the selected action; `-` denotes standard input. |
| `--json` | Machine-readable diagnostic report. |
| `--events` | Include sorted active Core events. |
| `--warnings-as-errors` | Fail the command on warnings without changing their stored severity. |
| `--schema-check` | Explicitly check a bundled Schema. |
| `--schema-version` | Exact supported root for schema-check; stable is the default. |

### Editor

Mutating subcommands take `SOURCE OUTPUT`; common options are `--force` to replace an existing distinct output and `--json` for a machine-readable receipt. `--force` never permits overwriting an input alias.

| Subcommand | Specific options |
| --- | --- |
| `convert` | Required `--to-version` with `3.0.0-draft.1`, `3.0.0-draft.2`, or `3.0.0`. |
| `upgrade`, `downgrade` | Draft-only compatibility commands; upgrade targets Draft 2, downgrade Draft 1. |
| `materialize` | Required `--template`, `--instance`, `--track`, `--clip`, `--start`; optional `--repeat` (1), `--transpose` (0), `--disabled`, `--max-notes` (100000). |
| `choose` | Required `--group` and exactly one of `--candidate` or `--none`; repeatable `--protect-note`, optional `--protect-process`. |
| `replace-template` | Required `--template`, `--replacement` JSON file; optional `--max-notes`, repeatable `--protect-note`, `--protect-process`. |
| `detach` | Required repeatable `--instance`; repeatable `--protect-note`, optional `--protect-process`. |
| `check-protection` | Positional `BEFORE AFTER`, exactly one of `--process` or repeatable `--note`; optional `--json`; no output file. |

```sh
python ostf3_edit.py convert old-draft.ostf stable.ostf --to-version 3.0.0 --json
python ostf3_edit.py materialize samples/30_template_before_materialization.ostf placed.ostf --template pickup-template --instance placed-1 --track target-track --clip placed-clip --start 120 --repeat 2 --json
python ostf3_edit.py choose samples/25_choice_shared_muted.ostf chosen.ostf --group main-choice --candidate choice-b --json
```

For replacement, the separate JSON input is one complete template, not an OSTF document and not a patch. `--protect-process` takes protection from the input snapshot's current generation process. CLI editing exit codes are 0 success, 1 document/operation/protection rejection, and 2 argument/I/O/runtime errors.

Output writing stages and closes the complete content before publication. Without force it creates the destination exclusively; with force it atomically replaces a distinct destination. Failure before publication leaves the destination unchanged. Inputs, including a replacement-template input, are protected against direct, symbolic-link, and hard-link aliases. There is no partial-write fallback when required atomic publication is unavailable; power-loss durability and rollback after successful publication are not promised.

## 19. Root-version conversion and OSTF 2.3 migration

Draft-to-stable conversion preserves Core content and profile versions. When an extension is unknown to either side, a current claim becomes unverified if its dependency scope is not none. Existing stale/unverified states are not promoted. If previously opaque data becomes known, it must satisfy the target profile structure; conversion does not guess repairs. Phrase-library and clip-choices remain opaque in Draft 1, which understands only the original four profiles. Conversion is explicit and never occurs during reading.

OSTF 2.3 uses a separate bounded migration adapter. Its default mode transfers recognized title, timeline, and mapped appearance, while preserving the complete source. It does not infer music from opaque 2.3 data. Opting into sample conventions interprets the documented sample-shaped pitch/start/duration fields and chord symbols, with an explicit report of assumptions.

| API/option | Meaning |
| --- | --- |
| `migrate_bytes(source_bytes, *, interpret_sample_notes=False, target_version=VERSION)` | Preferred when starting from a file; avoids accidental newline normalization. Returns a new document. |
| `migrate_text(source_text, *, interpret_sample_notes=False, target_version=VERSION)` | Migrates already available exact source text. Returns a new document. |
| CLI `SOURCE OUTPUT` | Distinct source and target `.ostf` files. |
| `--target-version` | `3.0.0` by default, or explicitly `3.0.0-draft.2`; Draft 1 is not a target. |
| `--interpret-sample-notes` | Explicitly apply the narrow published sample conventions. |
| `--force` | Replace an existing output while protecting the source and its aliases. |
| `--json-report` | Print the embedded conversion report; failures use a JSON error object in this mode. |

```sh
python ostf3_migrate.py samples/legacy_2_3/54_full_feature.ostf imported.ostf --json-report
python ostf3_migrate.py samples/legacy_2_3/54_full_feature.ostf interpreted.ostf --interpret-sample-notes --json-report
```

The reference adapter's report includes `conversionMode`; `sourceValidation.scope`, `fullOSTF23ConformanceChecked`, and `checks`; `completeMusicMigration`; `assumptions`; `archivedOnly`; `warnings`; `idMappings`; and `counts`. These are implementation report fields inside an open report object, not new fixed Core parameters. The adapter states bounded source checks and `completeMusicMigration: false`.

Additional unknown music attributes may affect mute, transposition, dynamics, or another behavior. The narrow adapter archives such objects without activating them. It does not parse chord labels into structured roots/intervals, reconstruct arbitrary lyrics, or infer phrase templates and choices. ID collisions are remapped deterministically, while ambiguous references are not guessed. Migration exit codes are 0 success, 1 conversion/file error, and 2 usage error. Read [MIGRATION_2_3_TO_3_0.md](MIGRATION_2_3_TO_3_0.md) and [SOURCE_ATTRIBUTION.md](SOURCE_ATTRIBUTION.md) for the reviewed source and exact limits.

## 20. Practical authoring workflows

### Chord progression to multiple parts

Write the harmonic plan in `harmony`, then save every adopted bass, chord, melody, and percussion note in separate tracks. Use meaningful roles and instrument descriptions without relying on them for playback routing. A generator can add relative assignments and generation context when it knows those relationships. Preserve proprietary controls in its own namespace. Another application can edit the notes even if it knows none of that generator's algorithms. Sample [01](../samples/01_four_part_sketch.ostf) demonstrates a multitrack sketch.

### Repeated phrase with a later manual edit

Save a template and materialized linked instances. An explicit replacement refreshes all linked instances while preserving surviving identities. If one placement should remain independently edited, detach that instance first; its Core notes remain. Do not leave a known mismatched library marked current. Samples 31–33 show the authored stages.

### Alternative arrangements without hidden playback rules

Store all candidate clips in Core and record their own enabled flags. Add a clip-choice group to explain which set is selected. Switching candidates explicitly updates those flags. The host's parent track mute remains a separate decision. Keep alternative harmony or whole-song scenes in separately defined future/vendor metadata instead of implying this profile switches them.

### Reliable round-trip editing

Use strict input, retain unknown values with sufficient numeric precision, keep IDs and array order, apply the intended Core edit, and invalidate relationships whose dependencies changed. Save with the same root version unless the user explicitly requests conversion. An exporter may make a bounded Core export without preserving every private setting, but should describe that capability clearly rather than call it lossless round-trip support.

## 21. Sample navigation and coverage limits

All numbered main examples use `.ostf` and root `3.0.0`. The two files in `samples/legacy_2_3/` are explicitly labeled 2.3 migration inputs. The [catalog](../samples/catalog.json) records sample purposes and provenance.

| Topic | Examples |
| --- | --- |
| Complete sketch and unfinished layers | 01–05, 34, 60 |
| Percussion, timing, gates, overlap, mute, meter | 06–11, 21, 35–37, 47–50 |
| Relative relationships and their states | 12–15, 39–40, 52 |
| Generation sources and protection | 16, 41–42 |
| Appearance and all Core target kinds | 17, 43–44 |
| Unknown data, exact numbers, dependency scopes | 18–19, 38, 51 |
| Lyrics and source archive | 20, 45–46; separately labeled legacy inputs |
| Phrase and choice basics | 22–26 |
| Optional-profile stale/empty/future forms | 27–29 |
| Materialization, replacement, detachment | 30–33 |
| Empty and object-scoped libraries, transpose limits | 53–54, 59 |
| Silent candidate, independent groups, object dependencies | 55–57 |
| Combined composition relationships | 58 |

“Complete coverage” here means all currently declared parameter positions, finite enum choices, and documented structural alternatives can be traced in the reference and coverage inventory. Arbitrary strings, numeric combinations, all possible music, and unbounded vendor JSON cannot be exhaustively enumerated in a finite sample set. A field appearing in a sample is not runtime proof of every semantic condition.

## 22. Common authoring mistakes

| Mistake | Correct interpretation |
| --- | --- |
| Adding note `velocity` to Core | Core is closed; use a separately specified extension if needed. |
| Saving only a loop recipe for an adopted performance | Save finite realized notes; an optional template relationship can accompany them. |
| Cropping notes to clip or section boundaries | Respect note onset and gate independently of placement spans. |
| Treating `midiNote` as sound-slot identity | Slot ID is identity; the number is an optional output hint. |
| Using track mute to satisfy candidate flags | Candidate correspondence checks each clip's own enabled state. |
| Treating `stale` as permission for malformed payloads | Known structure is checked in every status. |
| Reinterpreting a future profile using an older schema | Dispatch exact version and keep unsupported payload opaque. |
| Guessing a missing Core reference from a similar name | IDs and kinds must resolve exactly; names do not establish identity. |
| Assuming `current` proves past generation or protection | It is a saved declaration; historical claims require evidence. |
| Renaming root 2.3 to 3.0.0 | Use the bounded migration adapter and review its report. |
| Calling a field sweep an interoperability pass | Coverage is static documentation; real application exchange is a separate claim. |

## 23. Publication and future work

The initial release scope is stable Core, the six existing provisional profiles, the documented explicit operations, and conservative 2.3 migration. Chord-aware fitting, time scaling, partial overrides, whole-song scenes, notation, additional expression, and application-specific adapters are future work, not unstated completion requirements for this release.

Use [RELEASE_READINESS.md](RELEASE_READINESS.md) for the package's stated release scope and verification status, [CONFORMANCE.md](CONFORMANCE.md) for conformance requirements, and [LICENSE.md](../LICENSE.md) for the applicable project terms. Independently authored songs and applications are not assigned project licenses merely by using the OSTF format.
