# OSTF 3.0.0 Complete Parameter Reference

This dictionary covers Core `3.0.0` and the exact provisional version `1.0.0-draft.1` of all six bundled optional profiles. It lists every definition, declared field, finite choice, branch and structural constraint. See the [complete manual](COMPLETE_MANUAL.en.md) for usage, the [specification](FORMAT_SPECIFICATION.en.md) for normative meaning, and the [sample index](../samples/INDEX.md) for complete files.

**Inventory scope:** 168 canonical parameter declarations, 14 conditional property overlays, 51 named definitions, 7 enum sets (37 value occurrences). Same-named branch-local fields are separate declarations; reuses of one definition are not counted again. Completeness does not mean enumerating every possible string, number, vendor JSON value or musical combination.

Exact schema JSON Pointers, expanded instance paths and original constraints are provided in [PARAMETER_CATALOG.json](PARAMETER_CATALOG.json); [COVERAGE.md](COVERAGE.md) maps these to samples. This is a static documentation inventory, not runtime verification or a conformance pass result.

## Reading conventions and common rules

- Required means that the member must exist. Optional does not imply nullable. The explicit standard null case is an unselected `selectedCandidateId`.
- `additionalProperties: false` forbids undeclared keys. Put additional information in extensions rather than adding fields such as Core `velocity`.
- `default` is a schema annotation and inserts nothing. The specification gives omitted track/clip `enabled` the semantic value `true`.
- `minimum`/`maximum` are inclusive; `exclusiveMinimum` excludes its endpoint. `uniqueItems` disallows duplicate array values.
- Integer fields require JSON integer tokens. `1.0`, `1e0` and `true` are not valid integer-field representations.
- `oneOf` matches exactly one alternative, `anyOf` at least one, and `allOf` every listed rule. `if` tests a condition; `then` applies its consequent.
- Profile interpretation is selected by exact namespace and version. Preserve unknown-version `data` in the common envelope without applying an older payload schema.
- Instance-path `[*]` means an array element or dynamic object key. Listing a path does not assert that a conditional branch is active.

Schema SHA-256: `a2d828c928ab6654a925f845359614f274bf5b3e948f2d5ff0dc5020a121b263`.

Source: [ostf-3.0.0.schema.json](../schema/ostf-3.0.0.schema.json).

## Definition index

- [root](#def-root) — Complete document; all eleven root members are required.
- [id](#def-id) — ID lexical form; Core-wide and profile-local uniqueness are separate semantic rules.
- [nonnegative](#def-nonnegative) — Nonnegative integer ticks or occurrence indices.
- [positive](#def-positive) — Positive integer ticks or counts.
- [signed](#def-signed) — Signed integer, used for note-local start positions.
- [pitch](#def-pitch) — Semitone pitch number; 60 is C4 and 69 is A4.
- [ref](#def-ref) — Typed Core reference; both kind and ID must match.
- [range](#def-range) — Range on the global tick timeline; the computed endpoint is also bounded.
- [spelledPitchClass](#def-spelledpitchclass) — Spelled pitch class without octave; enharmonic spelling is retained.
- [song](#def-song) — Song title and primary-melody designation; an unnamed song may have an empty title.
- [section](#def-section) — Song-structure section; gaps are allowed but sections do not overlap.
- [tempo](#def-tempo) — Tempo from this tick onward, always measured in quarter notes per minute.
- [meter](#def-meter) — Meter from this tick onward; a reader does not move it to an inferred bar boundary.
- [timeline](#def-timeline) — Section, tempo-change and meter-change arrays.
- [chord](#def-chord) — Harmonic meaning; a label-only chord is allowed and does not generate a performed voicing.
- [scale](#def-scale) — Scale meaning; it does not restrict the pitches permitted in Core notes.
- [harmony](#def-harmony) — Chord and scale arrays; adopted performances are stored separately as Core notes.
- [instrument](#def-instrument) — Instrument description, not a plug-in-state or sound-engine contract.
- [note](#def-note) — Target, local onset and gate duration; Core and phrase templates share this shape but have different ID scopes.
- [clip](#def-clip) — Placement/editing unit within a track; duration does not truncate its notes.
- [track](#def-track) — Performance part with name, role, instrument description and clips; array order is display order.
- [soundSlot](#def-soundslot) — Percussion target; its ID establishes identity, not its MIDI hint or role.
- [lyricDocument](#def-lyricdocument) — Lyric-document identity and auxiliary metadata.
- [lyricPhrase](#def-lyricphrase) — Displayed lyric phrase; it need not equal the concatenation of its units.
- [lyricUnit](#def-lyricunit) — Lyric unit used for segmentation and note alignment.
- [lyricAlignment](#def-lyricalignment) — Ordered many-to-many association between lyric units and Core notes.
- [lyrics](#def-lyrics) — Four arrays for lyric documents, phrases, units and alignments.
- [sha256](#def-sha256) — SHA-256 digest as 64 lowercase hexadecimal digits.
- [resource](#def-resource) — Reference to source material; loading does not fetch, execute or play it.
- [dependencies](#def-dependencies) — Core dependency scope; two oneOf shapes represent three scope values.
- [extension](#def-extension) — Closed common envelope for every known or unknown extension.
- [relativeAssignment](#def-relativeassignment) — Relationship between one pitched Core note and a chord or scale interval.
- [relativeData](#def-relativedata) — Relative-pitch assignments; they do not rewrite Core on load.
- [generator](#def-generator) — Generator identifier and version; not a guarantee of algorithm reproduction.
- [generationInput](#def-generationinput) — One input role, Core reference and optional context-read range.
- [generationProcess](#def-generationprocess) — Record of generation inputs, outputs and protected-note relationships.
- [generationData](#def-generationdata) — Records of generation processes.
- [color](#def-color) — RGB color: # followed by six uppercase or lowercase hexadecimal digits.
- [roleDefinition](#def-roledefinition) — Custom section-role definition for presentation.
- [roleColorMap](#def-rolecolormap) — Dictionary from open role strings to RGB colors.
- [customRoleColorMap](#def-customrolecolormap) — Dictionary from declared custom-role IDs to RGB colors.
- [objectColor](#def-objectcolor) — Object-specific color for a typed Core reference.
- [appearanceData](#def-appearancedata) — Custom roles, section assignments and presentation colors; no performance effect.
- [legacyData](#def-legacydata) — Archive of 2.3 source text, its SHA-256 and a conversion report; not a command to restore Core.
- [extensions](#def-extensions) — Namespace-keyed extension dictionary; exact namespace and version select the payload structure.
- [phraseTemplate](#def-phrasetemplate) — Reusable concrete source notes; duration is the repeat period.
- [phraseNoteMapping](#def-phrasenotemapping) — Mapping from source-note identity and repetition index to a realized Core note.
- [phraseInstance](#def-phraseinstance) — Complete correspondence between a template and one Core clip.
- [phraseLibraryData](#def-phraselibrarydata) — Concrete phrase templates and already realized instances; never expanded on load.
- [clipCandidate](#def-clipcandidate) — Candidate-local identity and the Core clips enabled for that choice.
- [clipChoiceGroup](#def-clipchoicegroup) — Candidate group and saved selection, corresponding to stored Core enabled states.
- [clipChoicesData](#def-clipchoicesdata) — Array of independent clip-choice groups.

<a id="def-root"></a>

## root

Complete document; all eleven root members are required.

Schema: `#`

`"object"`; closed object.

Structural instance locations:

- `$`

| Parameter / Schema Pointer | Presence | Type and structural constraints | Meaning |
| --- | --- | --- | --- |
| `format`<br>`#/properties/format` | required | const=`"OSTF"` | Exact format identifier OSTF. |
| `version`<br>`#/properties/version` | required | const=`"3.0.0"` | Exact Core wire version 3.0.0. |
| `ppq`<br>`#/properties/ppq` | required | `"integer"`; minimum=`1`; maximum=`960000` | Integer ticks per quarter note; 960 is recommended but the declared value governs. |
| `song`<br>`#/properties/song` | required | [song](#def-song); `"object"`; closed object | Song metadata. |
| `timeline`<br>`#/properties/timeline` | required | [timeline](#def-timeline); `"object"`; closed object | Sections, tempo and meter maps. |
| `harmony`<br>`#/properties/harmony` | required | [harmony](#def-harmony); `"object"`; closed object | Chord and scale meaning. |
| `tracks`<br>`#/properties/tracks` | required | `"array"`; items: [track](#def-track); `"object"`; closed object | Performance tracks; preserve display order. |
| `soundSlots`<br>`#/properties/soundSlots` | required | `"array"`; items: [soundSlot](#def-soundslot); `"object"`; closed object | Percussion-target definitions. |
| `lyrics`<br>`#/properties/lyrics` | required | [lyrics](#def-lyrics); `"object"`; closed object | Lyrics and their note alignments. |
| `resources`<br>`#/properties/resources` | required | `"array"`; items: [resource](#def-resource); `"object"`; closed object | Referenced source material; never fetched automatically. |
| `extensions`<br>`#/properties/extensions` | required | [extensions](#def-extensions); `"object"`; additionalProperties: [extension](#def-extension); `"object"`; closed object; propertyNames=`{"pattern":"^[a-z][a-z0-9-]*(?:\\.[a-z][a-z0-9-]*){2,}$","not":{"pattern":"[\\r\\n\\u2028\\u2029]"}}` | Namespace dictionary of standard profiles and vendor data. |

<a id="def-id"></a>

## id

ID lexical form; Core-wide and profile-local uniqueness are separate semantic rules.

Schema: `#/$defs/id`

`"string"`; pattern=`"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$"`; not=`{"pattern":"[\\r\\n\\u2028\\u2029]"}`.

Structural instance locations:

- `$.extensions["org.ostf.appearance.v1"].data.appearance.customRoleColors.<key>`
- `$.extensions["org.ostf.appearance.v1"].data.appearance.objectColors[*].target.id`
- `$.extensions["org.ostf.appearance.v1"].data.roleDefinitions[*].id`
- `$.extensions["org.ostf.appearance.v1"].data.sectionRoleAssignments.<key>`
- `$.extensions["org.ostf.appearance.v1"].data.sectionRoleAssignments[*]`
- `$.extensions["org.ostf.appearance.v1"].dependencies.refs[*].id`
- `$.extensions["org.ostf.clip-choices.v1"].data.groups[*].candidates[*].clipIds[*]`
- `$.extensions["org.ostf.clip-choices.v1"].data.groups[*].candidates[*].id`
- `$.extensions["org.ostf.clip-choices.v1"].data.groups[*].id`
- `$.extensions["org.ostf.clip-choices.v1"].data.groups[*].selectedCandidateId`
- `$.extensions["org.ostf.clip-choices.v1"].dependencies.refs[*].id`
- `$.extensions["org.ostf.generation-context.v1"].data.processes[*].id`
- `$.extensions["org.ostf.generation-context.v1"].data.processes[*].inputs[*].ref.id`
- `$.extensions["org.ostf.generation-context.v1"].data.processes[*].outputs[*].id`
- `$.extensions["org.ostf.generation-context.v1"].data.processes[*].protectedNoteIds[*]`
- `$.extensions["org.ostf.generation-context.v1"].dependencies.refs[*].id`
- `$.extensions["org.ostf.legacy-import.v1"].dependencies.refs[*].id`
- `$.extensions["org.ostf.phrase-library.v1"].data.instances[*].clipId`
- `$.extensions["org.ostf.phrase-library.v1"].data.instances[*].id`
- `$.extensions["org.ostf.phrase-library.v1"].data.instances[*].noteMap[*].noteId`
- `$.extensions["org.ostf.phrase-library.v1"].data.instances[*].noteMap[*].templateNoteId`
- `$.extensions["org.ostf.phrase-library.v1"].data.instances[*].templateId`
- `$.extensions["org.ostf.phrase-library.v1"].data.templates[*].id`
- `$.extensions["org.ostf.phrase-library.v1"].data.templates[*].notes[*].id`
- `$.extensions["org.ostf.phrase-library.v1"].data.templates[*].notes[*].soundSlotId`
- `$.extensions["org.ostf.phrase-library.v1"].dependencies.refs[*].id`
- `$.extensions["org.ostf.relative-phrase.v1"].data.assignments[*].contextId`
- `$.extensions["org.ostf.relative-phrase.v1"].data.assignments[*].noteId`
- `$.extensions["org.ostf.relative-phrase.v1"].dependencies.refs[*].id`
- `$.extensions[*].dependencies.refs[*].id`
- `$.harmony.chords[*].id`
- `$.harmony.scales[*].id`
- `$.lyrics.alignments[*].id`
- `$.lyrics.alignments[*].noteIds[*]`
- `$.lyrics.alignments[*].unitIds[*]`
- `$.lyrics.documents[*].id`
- `$.lyrics.phrases[*].documentId`
- `$.lyrics.phrases[*].id`
- `$.lyrics.units[*].id`
- `$.lyrics.units[*].phraseId`
- `$.resources[*].id`
- `$.song.primaryMelodyTrackId`
- `$.soundSlots[*].id`
- `$.timeline.sections[*].id`
- `$.tracks[*].clips[*].id`
- `$.tracks[*].clips[*].notes[*].id`
- `$.tracks[*].clips[*].notes[*].soundSlotId`
- `$.tracks[*].id`

Structural/conditional rules (verbatim schema fragments):

```json
{
  "not": {
    "pattern": "[\\r\\n\\u2028\\u2029]"
  }
}
```

<a id="def-nonnegative"></a>

## nonnegative

Nonnegative integer ticks or occurrence indices.

Schema: `#/$defs/nonnegative`

`"integer"`; minimum=`0`; maximum=`9007199254740991`.

Structural instance locations:

- `$.extensions["org.ostf.generation-context.v1"].data.processes[*].inputs[*].readRange.start`
- `$.extensions["org.ostf.generation-context.v1"].data.processes[*].targetRange.start`
- `$.extensions["org.ostf.phrase-library.v1"].data.instances[*].noteMap[*].repeatIndex`
- `$.harmony.chords[*].start`
- `$.harmony.scales[*].start`
- `$.lyrics.phrases[*].start`
- `$.lyrics.units[*].start`
- `$.timeline.meterChanges[*].at`
- `$.timeline.sections[*].start`
- `$.timeline.tempoChanges[*].at`
- `$.tracks[*].clips[*].start`

<a id="def-positive"></a>

## positive

Positive integer ticks or counts.

Schema: `#/$defs/positive`

`"integer"`; minimum=`1`; maximum=`9007199254740991`.

Structural instance locations:

- `$.extensions["org.ostf.generation-context.v1"].data.processes[*].inputs[*].readRange.duration`
- `$.extensions["org.ostf.generation-context.v1"].data.processes[*].targetRange.duration`
- `$.extensions["org.ostf.phrase-library.v1"].data.instances[*].repeatCount`
- `$.extensions["org.ostf.phrase-library.v1"].data.templates[*].duration`
- `$.extensions["org.ostf.phrase-library.v1"].data.templates[*].notes[*].duration`
- `$.harmony.chords[*].duration`
- `$.harmony.scales[*].duration`
- `$.lyrics.phrases[*].duration`
- `$.lyrics.units[*].duration`
- `$.timeline.sections[*].duration`
- `$.tracks[*].clips[*].duration`
- `$.tracks[*].clips[*].notes[*].duration`

<a id="def-signed"></a>

## signed

Signed integer, used for note-local start positions.

Schema: `#/$defs/signed`

`"integer"`; minimum=`-9007199254740991`; maximum=`9007199254740991`.

Structural instance locations:

- `$.extensions["org.ostf.phrase-library.v1"].data.templates[*].notes[*].start`
- `$.tracks[*].clips[*].notes[*].start`

<a id="def-pitch"></a>

## pitch

Semitone pitch number; 60 is C4 and 69 is A4.

Schema: `#/$defs/pitch`

`"integer"`; minimum=`0`; maximum=`127`.

Structural instance locations:

- `$.extensions["org.ostf.phrase-library.v1"].data.templates[*].notes[*].pitch`
- `$.extensions["org.ostf.relative-phrase.v1"].data.assignments[*].anchorPitch`
- `$.soundSlots[*].midiNote`
- `$.tracks[*].clips[*].notes[*].pitch`

<a id="def-ref"></a>

## ref

Typed Core reference; both kind and ID must match.

Schema: `#/$defs/ref`

`"object"`; closed object.

Structural instance locations:

- `$.extensions["org.ostf.appearance.v1"].data.appearance.objectColors[*].target`
- `$.extensions["org.ostf.appearance.v1"].dependencies.refs[*]`
- `$.extensions["org.ostf.clip-choices.v1"].dependencies.refs[*]`
- `$.extensions["org.ostf.generation-context.v1"].data.processes[*].inputs[*].ref`
- `$.extensions["org.ostf.generation-context.v1"].data.processes[*].outputs[*]`
- `$.extensions["org.ostf.generation-context.v1"].dependencies.refs[*]`
- `$.extensions["org.ostf.legacy-import.v1"].dependencies.refs[*]`
- `$.extensions["org.ostf.phrase-library.v1"].dependencies.refs[*]`
- `$.extensions["org.ostf.relative-phrase.v1"].dependencies.refs[*]`
- `$.extensions[*].dependencies.refs[*]`

| Parameter / Schema Pointer | Presence | Type and structural constraints | Meaning |
| --- | --- | --- | --- |
| `type`<br>`#/$defs/ref/properties/type` | required | enum=`["section","track","clip","note","chord","scale","soundSlot","lyricDocument","lyricPhrase","lyricUnit","lyricAlignment","resource"]` | Kind of the referenced Core object. |
| `id`<br>`#/$defs/ref/properties/id` | required | [id](#def-id); `"string"`; pattern=`"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$"`; not=`{"pattern":"[\\r\\n\\u2028\\u2029]"}` | Core ID of the kind selected by type. |

<a id="def-range"></a>

## range

Range on the global tick timeline; the computed endpoint is also bounded.

Schema: `#/$defs/range`

`"object"`; closed object.

Structural instance locations:

- `$.extensions["org.ostf.generation-context.v1"].data.processes[*].inputs[*].readRange`
- `$.extensions["org.ostf.generation-context.v1"].data.processes[*].targetRange`

| Parameter / Schema Pointer | Presence | Type and structural constraints | Meaning |
| --- | --- | --- | --- |
| `start`<br>`#/$defs/range/properties/start` | required | [nonnegative](#def-nonnegative); `"integer"`; minimum=`0`; maximum=`9007199254740991` | Start tick; the coordinate system depends on the record type. |
| `duration`<br>`#/$defs/range/properties/duration` | required | [positive](#def-positive); `"integer"`; minimum=`1`; maximum=`9007199254740991` | Positive tick length; computed endpoints have semantic bounds too. |

<a id="def-spelledpitchclass"></a>

## spelledPitchClass

Spelled pitch class without octave; enharmonic spelling is retained.

Schema: `#/$defs/spelledPitchClass`

`"object"`; closed object.

Structural instance locations:

- `$.harmony.chords[*].bass`
- `$.harmony.chords[*].root`
- `$.harmony.scales[*].tonic`

| Parameter / Schema Pointer | Presence | Type and structural constraints | Meaning |
| --- | --- | --- | --- |
| `step`<br>`#/$defs/spelledPitchClass/properties/step` | required | enum=`["A","B","C","D","E","F","G"]` | Natural-note letter A through G. |
| `alter`<br>`#/$defs/spelledPitchClass/properties/alter` | required | `"integer"`; minimum=`-2`; maximum=`2` | Chromatic alteration in semitones, from -2 through 2. |

<a id="def-song"></a>

## song

Song title and primary-melody designation; an unnamed song may have an empty title.

Schema: `#/$defs/song`

`"object"`; closed object.

Structural instance locations:

- `$.song`

| Parameter / Schema Pointer | Presence | Type and structural constraints | Meaning |
| --- | --- | --- | --- |
| `title`<br>`#/$defs/song/properties/title` | required | `"string"` | Display title. |
| `primaryMelodyTrackId`<br>`#/$defs/song/properties/primaryMelodyTrackId` | optional | [id](#def-id); `"string"`; pattern=`"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$"`; not=`{"pattern":"[\\r\\n\\u2028\\u2029]"}` | Existing Core track designated as the primary melody. |

<a id="def-section"></a>

## section

Song-structure section; gaps are allowed but sections do not overlap.

Schema: `#/$defs/section`

`"object"`; closed object.

Structural instance locations:

- `$.timeline.sections[*]`

| Parameter / Schema Pointer | Presence | Type and structural constraints | Meaning |
| --- | --- | --- | --- |
| `id`<br>`#/$defs/section/properties/id` | required | [id](#def-id); `"string"`; pattern=`"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$"`; not=`{"pattern":"[\\r\\n\\u2028\\u2029]"}` | Record ID; see the type description for its uniqueness scope. |
| `name`<br>`#/$defs/section/properties/name` | required | `"string"`; minLength=`1` | Display name; not a substitute for identity. |
| `start`<br>`#/$defs/section/properties/start` | required | [nonnegative](#def-nonnegative); `"integer"`; minimum=`0`; maximum=`9007199254740991` | Global start tick of the section. |
| `duration`<br>`#/$defs/section/properties/duration` | required | [positive](#def-positive); `"integer"`; minimum=`1`; maximum=`9007199254740991` | Section span; its endpoint does not cut notes. |
| `role`<br>`#/$defs/section/properties/role` | optional | `"string"` | Open string describing function or role; not a fixed enumeration. |

<a id="def-tempo"></a>

## tempo

Tempo from this tick onward, always measured in quarter notes per minute.

Schema: `#/$defs/tempo`

`"object"`; closed object.

Structural instance locations:

- `$.timeline.tempoChanges[*]`

| Parameter / Schema Pointer | Presence | Type and structural constraints | Meaning |
| --- | --- | --- | --- |
| `at`<br>`#/$defs/tempo/properties/at` | required | [nonnegative](#def-nonnegative); `"integer"`; minimum=`0`; maximum=`9007199254740991` | Global change tick; each change map begins at 0 and increases strictly. |
| `bpm`<br>`#/$defs/tempo/properties/bpm` | required | `"number"`; exclusiveMinimum=`0`; maximum=`1000` | Finite quarter notes per minute, greater than 0 and at most 1000. |

<a id="def-meter"></a>

## meter

Meter from this tick onward; a reader does not move it to an inferred bar boundary.

Schema: `#/$defs/meter`

`"object"`; closed object.

Structural instance locations:

- `$.timeline.meterChanges[*]`

| Parameter / Schema Pointer | Presence | Type and structural constraints | Meaning |
| --- | --- | --- | --- |
| `at`<br>`#/$defs/meter/properties/at` | required | [nonnegative](#def-nonnegative); `"integer"`; minimum=`0`; maximum=`9007199254740991` | Global change tick; each change map begins at 0 and increases strictly. |
| `numerator`<br>`#/$defs/meter/properties/numerator` | required | `"integer"`; minimum=`1`; maximum=`64` | Meter numerator. |
| `denominator`<br>`#/$defs/meter/properties/denominator` | required | `"integer"`; enum=`[1,2,4,8,16,32,64]` | Meter denominator; only the enumerated powers of two. |

<a id="def-timeline"></a>

## timeline

Section, tempo-change and meter-change arrays.

Schema: `#/$defs/timeline`

`"object"`; closed object.

Structural instance locations:

- `$.timeline`

| Parameter / Schema Pointer | Presence | Type and structural constraints | Meaning |
| --- | --- | --- | --- |
| `sections`<br>`#/$defs/timeline/properties/sections` | required | `"array"`; items: [section](#def-section); `"object"`; closed object | Nonoverlapping sections ordered by start; empty arrays and gaps are allowed. |
| `tempoChanges`<br>`#/$defs/timeline/properties/tempoChanges` | required | `"array"`; minItems=`1`; items: [tempo](#def-tempo); `"object"`; closed object | Piecewise-constant tempo map beginning at tick 0. |
| `meterChanges`<br>`#/$defs/timeline/properties/meterChanges` | required | `"array"`; minItems=`1`; items: [meter](#def-meter); `"object"`; closed object | Meter-change map beginning at tick 0. |

<a id="def-chord"></a>

## chord

Harmonic meaning; a label-only chord is allowed and does not generate a performed voicing.

Schema: `#/$defs/chord`

`"object"`; closed object; dependentRequired (structural rules below).

Structural instance locations:

- `$.harmony.chords[*]`

| Parameter / Schema Pointer | Presence | Type and structural constraints | Meaning |
| --- | --- | --- | --- |
| `id`<br>`#/$defs/chord/properties/id` | required | [id](#def-id); `"string"`; pattern=`"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$"`; not=`{"pattern":"[\\r\\n\\u2028\\u2029]"}` | Record ID; see the type description for its uniqueness scope. |
| `start`<br>`#/$defs/chord/properties/start` | required | [nonnegative](#def-nonnegative); `"integer"`; minimum=`0`; maximum=`9007199254740991` | Start tick; the coordinate system depends on the record type. |
| `duration`<br>`#/$defs/chord/properties/duration` | required | [positive](#def-positive); `"integer"`; minimum=`1`; maximum=`9007199254740991` | Positive tick length; computed endpoints have semantic bounds too. |
| `label`<br>`#/$defs/chord/properties/label` | required | `"string"`; minLength=`1` | Required nonempty chord label; label-only harmony is allowed. |
| `root`<br>`#/$defs/chord/properties/root` | optional; required when intervals is present | [spelledPitchClass](#def-spelledpitchclass); `"object"`; closed object | Spelled root; present together with intervals. |
| `intervals`<br>`#/$defs/chord/properties/intervals` | optional; required when root is present | `"array"`; minItems=`1`; maxItems=`36`; uniqueItems=`true`; items: `"integer"`; minimum=`0`; maximum=`35`; contains=`{"const":0}` | Semitone distances from root or tonic; include 0, strictly increasing and duplicate-free. |
| `bass`<br>`#/$defs/chord/properties/bass` | optional | [spelledPitchClass](#def-spelledpitchclass); `"object"`; closed object | Optional spelled bass pitch class; does not generate a bass note. |

Structural/conditional rules (verbatim schema fragments):

```json
{
  "dependentRequired": {
    "root": [
      "intervals"
    ],
    "intervals": [
      "root"
    ]
  }
}
```

<a id="def-scale"></a>

## scale

Scale meaning; it does not restrict the pitches permitted in Core notes.

Schema: `#/$defs/scale`

`"object"`; closed object.

Structural instance locations:

- `$.harmony.scales[*]`

| Parameter / Schema Pointer | Presence | Type and structural constraints | Meaning |
| --- | --- | --- | --- |
| `id`<br>`#/$defs/scale/properties/id` | required | [id](#def-id); `"string"`; pattern=`"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$"`; not=`{"pattern":"[\\r\\n\\u2028\\u2029]"}` | Record ID; see the type description for its uniqueness scope. |
| `start`<br>`#/$defs/scale/properties/start` | required | [nonnegative](#def-nonnegative); `"integer"`; minimum=`0`; maximum=`9007199254740991` | Start tick; the coordinate system depends on the record type. |
| `duration`<br>`#/$defs/scale/properties/duration` | required | [positive](#def-positive); `"integer"`; minimum=`1`; maximum=`9007199254740991` | Positive tick length; computed endpoints have semantic bounds too. |
| `label`<br>`#/$defs/scale/properties/label` | optional | `"string"` | Optional scale label. |
| `tonic`<br>`#/$defs/scale/properties/tonic` | required | [spelledPitchClass](#def-spelledpitchclass); `"object"`; closed object | Spelled tonic. |
| `intervals`<br>`#/$defs/scale/properties/intervals` | required | `"array"`; minItems=`1`; maxItems=`12`; uniqueItems=`true`; items: `"integer"`; minimum=`0`; maximum=`11`; contains=`{"const":0}` | Semitone distances from root or tonic; include 0, strictly increasing and duplicate-free. |

<a id="def-harmony"></a>

## harmony

Chord and scale arrays; adopted performances are stored separately as Core notes.

Schema: `#/$defs/harmony`

`"object"`; closed object.

Structural instance locations:

- `$.harmony`

| Parameter / Schema Pointer | Presence | Type and structural constraints | Meaning |
| --- | --- | --- | --- |
| `chords`<br>`#/$defs/harmony/properties/chords` | required | `"array"`; items: [chord](#def-chord); `"object"`; closed object; dependentRequired (structural rules below) | Chord contexts ordered by start; overlap is allowed. |
| `scales`<br>`#/$defs/harmony/properties/scales` | required | `"array"`; items: [scale](#def-scale); `"object"`; closed object | Scale contexts ordered by start; overlap is allowed. |

<a id="def-instrument"></a>

## instrument

Instrument description, not a plug-in-state or sound-engine contract.

Schema: `#/$defs/instrument`

`"object"`; closed object.

Structural instance locations:

- `$.tracks[*].instrument`

| Parameter / Schema Pointer | Presence | Type and structural constraints | Meaning |
| --- | --- | --- | --- |
| `name`<br>`#/$defs/instrument/properties/name` | required | `"string"` | Display name; not a substitute for identity. |
| `family`<br>`#/$defs/instrument/properties/family` | optional | `"string"` | Optional open description of an instrument family. |

<a id="def-note"></a>

## note

Target, local onset and gate duration; Core and phrase templates share this shape but have different ID scopes.

Schema: `#/$defs/note`

`"object"`; closed object; oneOf (structural rules below).

Structural instance locations:

- `$.extensions["org.ostf.phrase-library.v1"].data.templates[*].notes[*]`
- `$.tracks[*].clips[*].notes[*]`

| Parameter / Schema Pointer | Presence | Type and structural constraints | Meaning |
| --- | --- | --- | --- |
| `id`<br>`#/$defs/note/properties/id` | required | [id](#def-id); `"string"`; pattern=`"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$"`; not=`{"pattern":"[\\r\\n\\u2028\\u2029]"}` | Core notes are unique document-wide; source-note IDs are local to one template. |
| `start`<br>`#/$defs/note/properties/start` | required | [signed](#def-signed); `"integer"`; minimum=`-9007199254740991`; maximum=`9007199254740991` | Signed tick offset from the parent clip or template start. |
| `duration`<br>`#/$defs/note/properties/duration` | required | [positive](#def-positive); `"integer"`; minimum=`1`; maximum=`9007199254740991` | Gate length; distinct from synthesizer release tails and notated duration. |
| `pitch`<br>`#/$defs/note/properties/pitch` | exactly one of pitch/soundSlotId required | [pitch](#def-pitch); `"integer"`; minimum=`0`; maximum=`127` | Semitone number 0–127; 60=C4; mutually exclusive with soundSlotId. |
| `soundSlotId`<br>`#/$defs/note/properties/soundSlotId` | exactly one of pitch/soundSlotId required | [id](#def-id); `"string"`; pattern=`"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$"`; not=`{"pattern":"[\\r\\n\\u2028\\u2029]"}` | ID of a Core soundSlot; mutually exclusive with pitch. |

Structural/conditional rules (verbatim schema fragments):

```json
{
  "oneOf": [
    {
      "required": [
        "pitch"
      ],
      "not": {
        "required": [
          "soundSlotId"
        ]
      }
    },
    {
      "required": [
        "soundSlotId"
      ],
      "not": {
        "required": [
          "pitch"
        ]
      }
    }
  ]
}
```

<a id="def-clip"></a>

## clip

Placement/editing unit within a track; duration does not truncate its notes.

Schema: `#/$defs/clip`

`"object"`; closed object.

Structural instance locations:

- `$.tracks[*].clips[*]`

| Parameter / Schema Pointer | Presence | Type and structural constraints | Meaning |
| --- | --- | --- | --- |
| `id`<br>`#/$defs/clip/properties/id` | required | [id](#def-id); `"string"`; pattern=`"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$"`; not=`{"pattern":"[\\r\\n\\u2028\\u2029]"}` | Record ID; see the type description for its uniqueness scope. |
| `name`<br>`#/$defs/clip/properties/name` | optional | `"string"` | Display name; not a substitute for identity. |
| `start`<br>`#/$defs/clip/properties/start` | required | [nonnegative](#def-nonnegative); `"integer"`; minimum=`0`; maximum=`9007199254740991` | Global placement start tick. |
| `duration`<br>`#/$defs/clip/properties/duration` | required | [positive](#def-positive); `"integer"`; minimum=`1`; maximum=`9007199254740991` | Placement/edit reference span; does not truncate pickups or tails. |
| `enabled`<br>`#/$defs/clip/properties/enabled` | optional | `"boolean"`; default=`true` | Semantically true when absent; notes are active only when both track and clip are enabled. |
| `notes`<br>`#/$defs/clip/properties/notes` | required | `"array"`; items: [note](#def-note); `"object"`; closed object; oneOf (structural rules below) | Concrete notes in nondecreasing onset order; retain array order at equal starts. |

<a id="def-track"></a>

## track

Performance part with name, role, instrument description and clips; array order is display order.

Schema: `#/$defs/track`

`"object"`; closed object.

Structural instance locations:

- `$.tracks[*]`

| Parameter / Schema Pointer | Presence | Type and structural constraints | Meaning |
| --- | --- | --- | --- |
| `id`<br>`#/$defs/track/properties/id` | required | [id](#def-id); `"string"`; pattern=`"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$"`; not=`{"pattern":"[\\r\\n\\u2028\\u2029]"}` | Record ID; see the type description for its uniqueness scope. |
| `name`<br>`#/$defs/track/properties/name` | required | `"string"` | Display name; not a substitute for identity. |
| `role`<br>`#/$defs/track/properties/role` | optional | `"string"` | Open string describing function or role; not a fixed enumeration. |
| `instrument`<br>`#/$defs/track/properties/instrument` | optional | [instrument](#def-instrument); `"object"`; closed object | Optional instrument-description object. |
| `enabled`<br>`#/$defs/track/properties/enabled` | optional | `"boolean"`; default=`true` | Semantically true when absent; notes are active only when both track and clip are enabled. |
| `clips`<br>`#/$defs/track/properties/clips` | required | `"array"`; items: [clip](#def-clip); `"object"`; closed object | Clips ordered by start; overlap and equal starts are allowed. |

<a id="def-soundslot"></a>

## soundSlot

Percussion target; its ID establishes identity, not its MIDI hint or role.

Schema: `#/$defs/soundSlot`

`"object"`; closed object.

Structural instance locations:

- `$.soundSlots[*]`

| Parameter / Schema Pointer | Presence | Type and structural constraints | Meaning |
| --- | --- | --- | --- |
| `id`<br>`#/$defs/soundSlot/properties/id` | required | [id](#def-id); `"string"`; pattern=`"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$"`; not=`{"pattern":"[\\r\\n\\u2028\\u2029]"}` | Record ID; see the type description for its uniqueness scope. |
| `name`<br>`#/$defs/soundSlot/properties/name` | required | `"string"` | Display name; not a substitute for identity. |
| `role`<br>`#/$defs/soundSlot/properties/role` | optional | `"string"` | Open string describing function or role; not a fixed enumeration. |
| `midiNote`<br>`#/$defs/soundSlot/properties/midiNote` | optional | [pitch](#def-pitch); `"integer"`; minimum=`0`; maximum=`127` | Optional output-mapping hint; does not assert GM conformance or identity. |

<a id="def-lyricdocument"></a>

## lyricDocument

Lyric-document identity and auxiliary metadata.

Schema: `#/$defs/lyricDocument`

`"object"`; closed object.

Structural instance locations:

- `$.lyrics.documents[*]`

| Parameter / Schema Pointer | Presence | Type and structural constraints | Meaning |
| --- | --- | --- | --- |
| `id`<br>`#/$defs/lyricDocument/properties/id` | required | [id](#def-id); `"string"`; pattern=`"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$"`; not=`{"pattern":"[\\r\\n\\u2028\\u2029]"}` | Record ID; see the type description for its uniqueness scope. |
| `title`<br>`#/$defs/lyricDocument/properties/title` | optional | `"string"` | Display title. |
| `language`<br>`#/$defs/lyricDocument/properties/language` | optional | `"string"` | Auxiliary language string without a mandated code format. |

<a id="def-lyricphrase"></a>

## lyricPhrase

Displayed lyric phrase; it need not equal the concatenation of its units.

Schema: `#/$defs/lyricPhrase`

`"object"`; closed object; dependentRequired (structural rules below).

Structural instance locations:

- `$.lyrics.phrases[*]`

| Parameter / Schema Pointer | Presence | Type and structural constraints | Meaning |
| --- | --- | --- | --- |
| `id`<br>`#/$defs/lyricPhrase/properties/id` | required | [id](#def-id); `"string"`; pattern=`"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$"`; not=`{"pattern":"[\\r\\n\\u2028\\u2029]"}` | Record ID; see the type description for its uniqueness scope. |
| `documentId`<br>`#/$defs/lyricPhrase/properties/documentId` | required | [id](#def-id); `"string"`; pattern=`"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$"`; not=`{"pattern":"[\\r\\n\\u2028\\u2029]"}` | Parent Core lyricDocument ID. |
| `text`<br>`#/$defs/lyricPhrase/properties/text` | required | `"string"` | Display text; pronunciation is a separate annotation. |
| `pronunciation`<br>`#/$defs/lyricPhrase/properties/pronunciation` | optional | `"string"` | Pronunciation annotation; no phoneme alphabet or singing engine is standardized. |
| `start`<br>`#/$defs/lyricPhrase/properties/start` | optional; required when duration is present | [nonnegative](#def-nonnegative); `"integer"`; minimum=`0`; maximum=`9007199254740991` | Optional global start tick, supplied together with duration. |
| `duration`<br>`#/$defs/lyricPhrase/properties/duration` | optional; required when start is present | [positive](#def-positive); `"integer"`; minimum=`1`; maximum=`9007199254740991` | Optional timed span, supplied together with start. |

Structural/conditional rules (verbatim schema fragments):

```json
{
  "dependentRequired": {
    "start": [
      "duration"
    ],
    "duration": [
      "start"
    ]
  }
}
```

<a id="def-lyricunit"></a>

## lyricUnit

Lyric unit used for segmentation and note alignment.

Schema: `#/$defs/lyricUnit`

`"object"`; closed object; dependentRequired (structural rules below).

Structural instance locations:

- `$.lyrics.units[*]`

| Parameter / Schema Pointer | Presence | Type and structural constraints | Meaning |
| --- | --- | --- | --- |
| `id`<br>`#/$defs/lyricUnit/properties/id` | required | [id](#def-id); `"string"`; pattern=`"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$"`; not=`{"pattern":"[\\r\\n\\u2028\\u2029]"}` | Record ID; see the type description for its uniqueness scope. |
| `phraseId`<br>`#/$defs/lyricUnit/properties/phraseId` | required | [id](#def-id); `"string"`; pattern=`"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$"`; not=`{"pattern":"[\\r\\n\\u2028\\u2029]"}` | Parent Core lyricPhrase ID. |
| `text`<br>`#/$defs/lyricUnit/properties/text` | required | `"string"` | Display text; pronunciation is a separate annotation. |
| `pronunciation`<br>`#/$defs/lyricUnit/properties/pronunciation` | optional | `"string"` | Pronunciation annotation; no phoneme alphabet or singing engine is standardized. |
| `start`<br>`#/$defs/lyricUnit/properties/start` | optional; required when duration is present | [nonnegative](#def-nonnegative); `"integer"`; minimum=`0`; maximum=`9007199254740991` | Optional global start tick, supplied together with duration. |
| `duration`<br>`#/$defs/lyricUnit/properties/duration` | optional; required when start is present | [positive](#def-positive); `"integer"`; minimum=`1`; maximum=`9007199254740991` | Optional timed span, supplied together with start. |

Structural/conditional rules (verbatim schema fragments):

```json
{
  "dependentRequired": {
    "start": [
      "duration"
    ],
    "duration": [
      "start"
    ]
  }
}
```

<a id="def-lyricalignment"></a>

## lyricAlignment

Ordered many-to-many association between lyric units and Core notes.

Schema: `#/$defs/lyricAlignment`

`"object"`; closed object.

Structural instance locations:

- `$.lyrics.alignments[*]`

| Parameter / Schema Pointer | Presence | Type and structural constraints | Meaning |
| --- | --- | --- | --- |
| `id`<br>`#/$defs/lyricAlignment/properties/id` | required | [id](#def-id); `"string"`; pattern=`"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$"`; not=`{"pattern":"[\\r\\n\\u2028\\u2029]"}` | Record ID; see the type description for its uniqueness scope. |
| `unitIds`<br>`#/$defs/lyricAlignment/properties/unitIds` | required | `"array"`; minItems=`1`; uniqueItems=`true`; items: [id](#def-id); `"string"`; pattern=`"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$"`; not=`{"pattern":"[\\r\\n\\u2028\\u2029]"}` | Nonempty duplicate-free ordered Core lyricUnit IDs. |
| `noteIds`<br>`#/$defs/lyricAlignment/properties/noteIds` | required | `"array"`; minItems=`1`; uniqueItems=`true`; items: [id](#def-id); `"string"`; pattern=`"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$"`; not=`{"pattern":"[\\r\\n\\u2028\\u2029]"}` | Nonempty duplicate-free ordered Core note IDs. |

<a id="def-lyrics"></a>

## lyrics

Four arrays for lyric documents, phrases, units and alignments.

Schema: `#/$defs/lyrics`

`"object"`; closed object.

Structural instance locations:

- `$.lyrics`

| Parameter / Schema Pointer | Presence | Type and structural constraints | Meaning |
| --- | --- | --- | --- |
| `documents`<br>`#/$defs/lyrics/properties/documents` | required | `"array"`; items: [lyricDocument](#def-lyricdocument); `"object"`; closed object | Lyric-document array. |
| `phrases`<br>`#/$defs/lyrics/properties/phrases` | required | `"array"`; items: [lyricPhrase](#def-lyricphrase); `"object"`; closed object; dependentRequired (structural rules below) | Lyric-phrase array. |
| `units`<br>`#/$defs/lyrics/properties/units` | required | `"array"`; items: [lyricUnit](#def-lyricunit); `"object"`; closed object; dependentRequired (structural rules below) | Lyric-unit array. |
| `alignments`<br>`#/$defs/lyrics/properties/alignments` | required | `"array"`; items: [lyricAlignment](#def-lyricalignment); `"object"`; closed object | Lyric-unit/note alignment array. |

<a id="def-sha256"></a>

## sha256

SHA-256 digest as 64 lowercase hexadecimal digits.

Schema: `#/$defs/sha256`

`"string"`; pattern=`"^[0-9a-f]{64}$"`; not=`{"pattern":"[\\r\\n\\u2028\\u2029]"}`.

Structural instance locations:

- `$.extensions["org.ostf.legacy-import.v1"].data.sourceSha256`
- `$.resources[*].sha256`

Structural/conditional rules (verbatim schema fragments):

```json
{
  "not": {
    "pattern": "[\\r\\n\\u2028\\u2029]"
  }
}
```

<a id="def-resource"></a>

## resource

Reference to source material; loading does not fetch, execute or play it.

Schema: `#/$defs/resource`

`"object"`; closed object.

Structural instance locations:

- `$.resources[*]`

| Parameter / Schema Pointer | Presence | Type and structural constraints | Meaning |
| --- | --- | --- | --- |
| `id`<br>`#/$defs/resource/properties/id` | required | [id](#def-id); `"string"`; pattern=`"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$"`; not=`{"pattern":"[\\r\\n\\u2028\\u2029]"}` | Record ID; see the type description for its uniqueness scope. |
| `kind`<br>`#/$defs/resource/properties/kind` | required | enum=`["audio","midi","text","other"]` | Kind of referenced material; not a playback operation. |
| `uri`<br>`#/$defs/resource/properties/uri` | required | `"string"`; minLength=`1` | Nonempty reference string; not resolved or fetched on load. |
| `name`<br>`#/$defs/resource/properties/name` | optional | `"string"` | Display name; not a substitute for identity. |
| `sha256`<br>`#/$defs/resource/properties/sha256` | optional | [sha256](#def-sha256); `"string"`; pattern=`"^[0-9a-f]{64}$"`; not=`{"pattern":"[\\r\\n\\u2028\\u2029]"}` | Optional digest of referenced material; comparison is an explicit operation. |

<a id="def-dependencies"></a>

## dependencies

Core dependency scope; two oneOf shapes represent three scope values.

Schema: `#/$defs/dependencies`

oneOf (structural rules below).

Structural instance locations:

- `$.extensions["org.ostf.appearance.v1"].dependencies`
- `$.extensions["org.ostf.clip-choices.v1"].dependencies`
- `$.extensions["org.ostf.generation-context.v1"].dependencies`
- `$.extensions["org.ostf.legacy-import.v1"].dependencies`
- `$.extensions["org.ostf.phrase-library.v1"].dependencies`
- `$.extensions["org.ostf.relative-phrase.v1"].dependencies`
- `$.extensions[*].dependencies`

| Parameter / Schema Pointer | Presence | Type and structural constraints | Meaning |
| --- | --- | --- | --- |
| `scope`<br>`#/$defs/dependencies/oneOf/0/properties/scope` | required | enum=`["document","none"]` | document means whole Core; none means no Core dependency; objects means explicit refs. |
| `scope`<br>`#/$defs/dependencies/oneOf/1/properties/scope` | required | const=`"objects"` | document means whole Core; none means no Core dependency; objects means explicit refs. |
| `refs`<br>`#/$defs/dependencies/oneOf/1/properties/refs` | required | `"array"`; minItems=`1`; uniqueItems=`true`; items: [ref](#def-ref); `"object"`; closed object | Nonempty duplicate-free typed references, required for objects scope. |

Structural/conditional rules (verbatim schema fragments):

```json
{
  "oneOf": [
    {
      "type": "object",
      "properties": {
        "scope": {
          "enum": [
            "document",
            "none"
          ]
        }
      },
      "required": [
        "scope"
      ],
      "additionalProperties": false
    },
    {
      "type": "object",
      "properties": {
        "scope": {
          "const": "objects"
        },
        "refs": {
          "type": "array",
          "items": {
            "$ref": "#/$defs/ref"
          },
          "minItems": 1,
          "uniqueItems": true
        }
      },
      "required": [
        "scope",
        "refs"
      ],
      "additionalProperties": false
    }
  ]
}
```

<a id="def-extension"></a>

## extension

Closed common envelope for every known or unknown extension.

Schema: `#/$defs/extension`

`"object"`; closed object.

Structural instance locations:

- `$.extensions["org.ostf.appearance.v1"]`
- `$.extensions["org.ostf.clip-choices.v1"]`
- `$.extensions["org.ostf.generation-context.v1"]`
- `$.extensions["org.ostf.legacy-import.v1"]`
- `$.extensions["org.ostf.phrase-library.v1"]`
- `$.extensions["org.ostf.relative-phrase.v1"]`
- `$.extensions[*]`

| Parameter / Schema Pointer | Presence | Type and structural constraints | Meaning |
| --- | --- | --- | --- |
| `version`<br>`#/$defs/extension/properties/version` | required | `"string"`; minLength=`1` | Version of this object; root, profile and generator versions are distinct identifiers. |
| `status`<br>`#/$defs/extension/properties/status` | required | enum=`["current","stale","unverified"]` | Relationship status against this document, not specification maturity or playback on/off. |
| `dependencies`<br>`#/$defs/extension/properties/dependencies` | required | [dependencies](#def-dependencies); oneOf (structural rules below) | Core dependency declaration, including effects inherited from parent movement or disabling. |
| `data`<br>`#/$defs/extension/properties/data` | required | Any JSON value | Any JSON for unknown profiles; exact known versions use the corresponding payload schema. |

<a id="def-relativeassignment"></a>

## relativeAssignment

Relationship between one pitched Core note and a chord or scale interval.

Schema: `#/$defs/relativeAssignment`

`"object"`; closed object; allOf (structural rules below).

Structural instance locations:

- `$.extensions["org.ostf.relative-phrase.v1"].data.assignments[*]`

| Parameter / Schema Pointer | Presence | Type and structural constraints | Meaning |
| --- | --- | --- | --- |
| `noteId`<br>`#/$defs/relativeAssignment/properties/noteId` | required | [id](#def-id); `"string"`; pattern=`"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$"`; not=`{"pattern":"[\\r\\n\\u2028\\u2029]"}` | Target Core note ID. |
| `basis`<br>`#/$defs/relativeAssignment/properties/basis` | required | enum=`["chordTone","scaleDegree"]` | chordTone selects a chord interval; scaleDegree selects a scale interval. |
| `contextId`<br>`#/$defs/relativeAssignment/properties/contextId` | required | [id](#def-id); `"string"`; pattern=`"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$"`; not=`{"pattern":"[\\r\\n\\u2028\\u2029]"}` | Core chord or scale ID selected according to basis. |
| `anchorPitch`<br>`#/$defs/relativeAssignment/properties/anchorPitch` | required | [pitch](#def-pitch); `"integer"`; minimum=`0`; maximum=`127` | Actual octave-specific root or tonic pitch. |
| `index`<br>`#/$defs/relativeAssignment/properties/index` | required | `"integer"`; minimum=`1`; maximum=`36` | One-based position within intervals, not a chord-symbol degree label. |
| `chromaticOffset`<br>`#/$defs/relativeAssignment/properties/chromaticOffset` | required | `"integer"`; minimum=`-24`; maximum=`24` | Semitone adjustment added to the selected interval. |

Structural/conditional rules (verbatim schema fragments):

```json
{
  "allOf": [
    {
      "if": {
        "properties": {
          "basis": {
            "const": "scaleDegree"
          }
        },
        "required": [
          "basis"
        ]
      },
      "then": {
        "properties": {
          "index": {
            "maximum": 12
          }
        }
      }
    }
  ]
}
```

<a id="def-relativedata"></a>

## relativeData

Relative-pitch assignments; they do not rewrite Core on load.

Schema: `#/$defs/relativeData`

`"object"`; closed object.

Structural instance locations:

- `$.extensions["org.ostf.relative-phrase.v1"].data`

| Parameter / Schema Pointer | Presence | Type and structural constraints | Meaning |
| --- | --- | --- | --- |
| `assignments`<br>`#/$defs/relativeData/properties/assignments` | required | `"array"`; items: [relativeAssignment](#def-relativeassignment); `"object"`; closed object; allOf (structural rules below) | At most one assignment for each pitched Core note. |

<a id="def-generator"></a>

## generator

Generator identifier and version; not a guarantee of algorithm reproduction.

Schema: `#/$defs/generator`

`"object"`; closed object.

Structural instance locations:

- `$.extensions["org.ostf.generation-context.v1"].data.processes[*].generator`

| Parameter / Schema Pointer | Presence | Type and structural constraints | Meaning |
| --- | --- | --- | --- |
| `id`<br>`#/$defs/generator/properties/id` | required | `"string"`; minLength=`1` | Nonempty generator identifier; the Core ID lexical restriction does not apply. |
| `version`<br>`#/$defs/generator/properties/version` | required | `"string"`; minLength=`1` | Version of this object; root, profile and generator versions are distinct identifiers. |

<a id="def-generationinput"></a>

## generationInput

One input role, Core reference and optional context-read range.

Schema: `#/$defs/generationInput`

`"object"`; closed object.

Structural instance locations:

- `$.extensions["org.ostf.generation-context.v1"].data.processes[*].inputs[*]`

| Parameter / Schema Pointer | Presence | Type and structural constraints | Meaning |
| --- | --- | --- | --- |
| `role`<br>`#/$defs/generationInput/properties/role` | required | `"string"`; minLength=`1` | Open string describing function or role; not a fixed enumeration. |
| `ref`<br>`#/$defs/generationInput/properties/ref` | required | [ref](#def-ref); `"object"`; closed object | Typed reference to a Core object. |
| `readRange`<br>`#/$defs/generationInput/properties/readRange` | optional | [range](#def-range); `"object"`; closed object | Global context-read range, distinct from the output span. |

<a id="def-generationprocess"></a>

## generationProcess

Record of generation inputs, outputs and protected-note relationships.

Schema: `#/$defs/generationProcess`

`"object"`; closed object.

Structural instance locations:

- `$.extensions["org.ostf.generation-context.v1"].data.processes[*]`

| Parameter / Schema Pointer | Presence | Type and structural constraints | Meaning |
| --- | --- | --- | --- |
| `id`<br>`#/$defs/generationProcess/properties/id` | required | [id](#def-id); `"string"`; pattern=`"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$"`; not=`{"pattern":"[\\r\\n\\u2028\\u2029]"}` | Process ID unique within this generation-context extension. |
| `generator`<br>`#/$defs/generationProcess/properties/generator` | required | [generator](#def-generator); `"object"`; closed object | Generator identifier/version object. |
| `inputs`<br>`#/$defs/generationProcess/properties/inputs` | required | `"array"`; items: [generationInput](#def-generationinput); `"object"`; closed object | Input records with roles; empty or multiple inputs are allowed. |
| `outputs`<br>`#/$defs/generationProcess/properties/outputs` | required | `"array"`; minItems=`1`; items: [ref](#def-ref); `"object"`; closed object | Nonempty typed references to Core outputs. |
| `targetRange`<br>`#/$defs/generationProcess/properties/targetRange` | optional | [range](#def-range); `"object"`; closed object | Requested global modification range; does not truncate pickups or tails. |
| `protectedNoteIds`<br>`#/$defs/generationProcess/properties/protectedNoteIds` | required | `"array"`; uniqueItems=`true`; items: [id](#def-id); `"string"`; pattern=`"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$"`; not=`{"pattern":"[\\r\\n\\u2028\\u2029]"}` | Duplicate-free Core note IDs; the comparison set is fixed before the operation. |
| `vendorExtension`<br>`#/$defs/generationProcess/properties/vendorExtension` | optional | `"string"`; minLength=`1` | Another extension namespace in this document; current data requires document scope. |

<a id="def-generationdata"></a>

## generationData

Records of generation processes.

Schema: `#/$defs/generationData`

`"object"`; closed object.

Structural instance locations:

- `$.extensions["org.ostf.generation-context.v1"].data`

| Parameter / Schema Pointer | Presence | Type and structural constraints | Meaning |
| --- | --- | --- | --- |
| `processes`<br>`#/$defs/generationData/properties/processes` | required | `"array"`; items: [generationProcess](#def-generationprocess); `"object"`; closed object | Generation-process records. |

<a id="def-color"></a>

## color

RGB color: # followed by six uppercase or lowercase hexadecimal digits.

Schema: `#/$defs/color`

`"string"`; pattern=`"^#[0-9A-Fa-f]{6}$"`; not=`{"pattern":"[\\r\\n\\u2028\\u2029]"}`.

Structural instance locations:

- `$.extensions["org.ostf.appearance.v1"].data.appearance.customRoleColors[*]`
- `$.extensions["org.ostf.appearance.v1"].data.appearance.objectColors[*].color`
- `$.extensions["org.ostf.appearance.v1"].data.appearance.roleColors[*]`

Structural/conditional rules (verbatim schema fragments):

```json
{
  "not": {
    "pattern": "[\\r\\n\\u2028\\u2029]"
  }
}
```

<a id="def-roledefinition"></a>

## roleDefinition

Custom section-role definition for presentation.

Schema: `#/$defs/roleDefinition`

`"object"`; closed object.

Structural instance locations:

- `$.extensions["org.ostf.appearance.v1"].data.roleDefinitions[*]`

| Parameter / Schema Pointer | Presence | Type and structural constraints | Meaning |
| --- | --- | --- | --- |
| `id`<br>`#/$defs/roleDefinition/properties/id` | required | [id](#def-id); `"string"`; pattern=`"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$"`; not=`{"pattern":"[\\r\\n\\u2028\\u2029]"}` | Custom-role ID unique within the appearance profile. |
| `name`<br>`#/$defs/roleDefinition/properties/name` | required | `"string"`; minLength=`1` | Display name; not a substitute for identity. |
| `baseRole`<br>`#/$defs/roleDefinition/properties/baseRole` | optional | `"string"` | Optional base-role string. |

<a id="def-rolecolormap"></a>

## roleColorMap

Dictionary from open role strings to RGB colors.

Schema: `#/$defs/roleColorMap`

`"object"`; additionalProperties: [color](#def-color); `"string"`; pattern=`"^#[0-9A-Fa-f]{6}$"`; not=`{"pattern":"[\\r\\n\\u2028\\u2029]"}`.

Structural instance locations:

- `$.extensions["org.ostf.appearance.v1"].data.appearance.roleColors`

Structural/conditional rules (verbatim schema fragments):

```json
{
  "additionalProperties": {
    "$ref": "#/$defs/color"
  }
}
```

<a id="def-customrolecolormap"></a>

## customRoleColorMap

Dictionary from declared custom-role IDs to RGB colors.

Schema: `#/$defs/customRoleColorMap`

`"object"`; additionalProperties: [color](#def-color); `"string"`; pattern=`"^#[0-9A-Fa-f]{6}$"`; not=`{"pattern":"[\\r\\n\\u2028\\u2029]"}`; propertyNames=`{"$ref":"#/$defs/id"}`.

Structural instance locations:

- `$.extensions["org.ostf.appearance.v1"].data.appearance.customRoleColors`

Structural/conditional rules (verbatim schema fragments):

```json
{
  "propertyNames": {
    "$ref": "#/$defs/id"
  },
  "additionalProperties": {
    "$ref": "#/$defs/color"
  }
}
```

<a id="def-objectcolor"></a>

## objectColor

Object-specific color for a typed Core reference.

Schema: `#/$defs/objectColor`

`"object"`; closed object.

Structural instance locations:

- `$.extensions["org.ostf.appearance.v1"].data.appearance.objectColors[*]`

| Parameter / Schema Pointer | Presence | Type and structural constraints | Meaning |
| --- | --- | --- | --- |
| `target`<br>`#/$defs/objectColor/properties/target` | required | [ref](#def-ref); `"object"`; closed object | Typed Core target receiving the color. |
| `color`<br>`#/$defs/objectColor/properties/color` | required | [color](#def-color); `"string"`; pattern=`"^#[0-9A-Fa-f]{6}$"`; not=`{"pattern":"[\\r\\n\\u2028\\u2029]"}` | Object-specific RGB color. |

<a id="def-appearancedata"></a>

## appearanceData

Custom roles, section assignments and presentation colors; no performance effect.

Schema: `#/$defs/appearanceData`

`"object"`; closed object.

Structural instance locations:

- `$.extensions["org.ostf.appearance.v1"].data`

| Parameter / Schema Pointer | Presence | Type and structural constraints | Meaning |
| --- | --- | --- | --- |
| `roleDefinitions`<br>`#/$defs/appearanceData/properties/roleDefinitions` | required | `"array"`; items: [roleDefinition](#def-roledefinition); `"object"`; closed object | Custom-role definitions. |
| `sectionRoleAssignments`<br>`#/$defs/appearanceData/properties/sectionRoleAssignments` | required | `"object"`; additionalProperties: [id](#def-id); `"string"`; pattern=`"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$"`; not=`{"pattern":"[\\r\\n\\u2028\\u2029]"}`; propertyNames=`{"$ref":"#/$defs/id"}` | Map from Core section IDs to custom-role IDs. |
| `appearance`<br>`#/$defs/appearanceData/properties/appearance` | required | `"object"`; closed object | Colors by role, custom role and individual target. |
| `roleColors`<br>`#/$defs/appearanceData/properties/appearance/properties/roleColors` | required | [roleColorMap](#def-rolecolormap); `"object"`; additionalProperties: [color](#def-color); `"string"`; pattern=`"^#[0-9A-Fa-f]{6}$"`; not=`{"pattern":"[\\r\\n\\u2028\\u2029]"}` | Color dictionary keyed by open role strings. |
| `customRoleColors`<br>`#/$defs/appearanceData/properties/appearance/properties/customRoleColors` | required | [customRoleColorMap](#def-customrolecolormap); `"object"`; additionalProperties: [color](#def-color); `"string"`; pattern=`"^#[0-9A-Fa-f]{6}$"`; not=`{"pattern":"[\\r\\n\\u2028\\u2029]"}`; propertyNames=`{"$ref":"#/$defs/id"}` | Color dictionary keyed by declared custom-role IDs. |
| `objectColors`<br>`#/$defs/appearanceData/properties/appearance/properties/objectColors` | required | `"array"`; items: [objectColor](#def-objectcolor); `"object"`; closed object | Object-specific color records. |

Inline object `#/$defs/appearanceData/properties/appearance`:

```json
{
  "type": "object",
  "required": [
    "roleColors",
    "customRoleColors",
    "objectColors"
  ],
  "additionalProperties": false
}
```

<a id="def-legacydata"></a>

## legacyData

Archive of 2.3 source text, its SHA-256 and a conversion report; not a command to restore Core.

Schema: `#/$defs/legacyData`

`"object"`; closed object.

Structural instance locations:

- `$.extensions["org.ostf.legacy-import.v1"].data`

| Parameter / Schema Pointer | Presence | Type and structural constraints | Meaning |
| --- | --- | --- | --- |
| `sourceVersion`<br>`#/$defs/legacyData/properties/sourceVersion` | required | const=`"2.3.0"` | Archived source version, exactly 2.3.0. |
| `sourceSha256`<br>`#/$defs/legacyData/properties/sourceSha256` | required | [sha256](#def-sha256); `"string"`; pattern=`"^[0-9a-f]{64}$"`; not=`{"pattern":"[\\r\\n\\u2028\\u2029]"}` | SHA-256 of sourceText encoded as UTF-8. |
| `sourceText`<br>`#/$defs/legacyData/properties/sourceText` | required | `"string"`; minLength=`1` | Complete original 2.3 JSON text, retaining source whitespace and strings. |
| `conversionReport`<br>`#/$defs/legacyData/properties/conversionReport` | required | `"object"` | Migration mapping/loss report; this profile does not fix its internal members. |

<a id="def-extensions"></a>

## extensions

Namespace-keyed extension dictionary; exact namespace and version select the payload structure.

Schema: `#/$defs/extensions`

`"object"`; additionalProperties: [extension](#def-extension); `"object"`; closed object; propertyNames=`{"pattern":"^[a-z][a-z0-9-]*(?:\\.[a-z][a-z0-9-]*){2,}$","not":{"pattern":"[\\r\\n\\u2028\\u2029]"}}`.

Structural instance locations:

- `$.extensions`

| Parameter / Schema Pointer | Presence | Type and structural constraints | Meaning |
| --- | --- | --- | --- |
| `org.ostf.relative-phrase.v1`<br>`#/$defs/extensions/properties/org.ostf.relative-phrase.v1` | optional | allOf (structural rules below) | Optional profile at this namespace; the known payload version is exactly 1.0.0-draft.1. |
| `org.ostf.generation-context.v1`<br>`#/$defs/extensions/properties/org.ostf.generation-context.v1` | optional | allOf (structural rules below) | Optional profile at this namespace; the known payload version is exactly 1.0.0-draft.1. |
| `org.ostf.appearance.v1`<br>`#/$defs/extensions/properties/org.ostf.appearance.v1` | optional | allOf (structural rules below) | Optional profile at this namespace; the known payload version is exactly 1.0.0-draft.1. |
| `org.ostf.legacy-import.v1`<br>`#/$defs/extensions/properties/org.ostf.legacy-import.v1` | optional | allOf (structural rules below) | Optional profile at this namespace; the known payload version is exactly 1.0.0-draft.1. |
| `org.ostf.phrase-library.v1`<br>`#/$defs/extensions/properties/org.ostf.phrase-library.v1` | optional | allOf (structural rules below) | Optional profile at this namespace; the known payload version is exactly 1.0.0-draft.1. |
| `org.ostf.clip-choices.v1`<br>`#/$defs/extensions/properties/org.ostf.clip-choices.v1` | optional | allOf (structural rules below) | Optional profile at this namespace; the known payload version is exactly 1.0.0-draft.1. |

Structural/conditional rules (verbatim schema fragments):

```json
{
  "propertyNames": {
    "pattern": "^[a-z][a-z0-9-]*(?:\\.[a-z][a-z0-9-]*){2,}$",
    "not": {
      "pattern": "[\\r\\n\\u2028\\u2029]"
    }
  },
  "additionalProperties": {
    "$ref": "#/$defs/extension"
  }
}
```

Property-local branch `#/$defs/extensions/properties/org.ostf.relative-phrase.v1`:

```json
{
  "allOf": [
    {
      "$ref": "#/$defs/extension"
    },
    {
      "if": {
        "properties": {
          "version": {
            "const": "1.0.0-draft.1"
          }
        },
        "required": [
          "version"
        ]
      },
      "then": {
        "properties": {
          "data": {
            "$ref": "#/$defs/relativeData"
          }
        }
      }
    }
  ]
}
```

Property-local branch `#/$defs/extensions/properties/org.ostf.generation-context.v1`:

```json
{
  "allOf": [
    {
      "$ref": "#/$defs/extension"
    },
    {
      "if": {
        "properties": {
          "version": {
            "const": "1.0.0-draft.1"
          }
        },
        "required": [
          "version"
        ]
      },
      "then": {
        "properties": {
          "data": {
            "$ref": "#/$defs/generationData"
          }
        }
      }
    }
  ]
}
```

Property-local branch `#/$defs/extensions/properties/org.ostf.appearance.v1`:

```json
{
  "allOf": [
    {
      "$ref": "#/$defs/extension"
    },
    {
      "if": {
        "properties": {
          "version": {
            "const": "1.0.0-draft.1"
          }
        },
        "required": [
          "version"
        ]
      },
      "then": {
        "properties": {
          "data": {
            "$ref": "#/$defs/appearanceData"
          }
        }
      }
    }
  ]
}
```

Property-local branch `#/$defs/extensions/properties/org.ostf.legacy-import.v1`:

```json
{
  "allOf": [
    {
      "$ref": "#/$defs/extension"
    },
    {
      "if": {
        "properties": {
          "version": {
            "const": "1.0.0-draft.1"
          }
        },
        "required": [
          "version"
        ]
      },
      "then": {
        "properties": {
          "data": {
            "$ref": "#/$defs/legacyData"
          }
        }
      }
    }
  ]
}
```

Property-local branch `#/$defs/extensions/properties/org.ostf.phrase-library.v1`:

```json
{
  "allOf": [
    {
      "$ref": "#/$defs/extension"
    },
    {
      "if": {
        "properties": {
          "version": {
            "const": "1.0.0-draft.1"
          }
        },
        "required": [
          "version"
        ]
      },
      "then": {
        "properties": {
          "data": {
            "$ref": "#/$defs/phraseLibraryData"
          }
        }
      }
    }
  ]
}
```

Property-local branch `#/$defs/extensions/properties/org.ostf.clip-choices.v1`:

```json
{
  "allOf": [
    {
      "$ref": "#/$defs/extension"
    },
    {
      "if": {
        "properties": {
          "version": {
            "const": "1.0.0-draft.1"
          }
        },
        "required": [
          "version"
        ]
      },
      "then": {
        "properties": {
          "data": {
            "$ref": "#/$defs/clipChoicesData"
          }
        }
      }
    }
  ]
}
```

Inline object `#/$defs/extensions/properties/org.ostf.relative-phrase.v1/allOf/1/if`:

```json
{
  "required": [
    "version"
  ]
}
```

Inline object `#/$defs/extensions/properties/org.ostf.relative-phrase.v1/allOf/1/then`:

```json
{}
```

Inline object `#/$defs/extensions/properties/org.ostf.generation-context.v1/allOf/1/if`:

```json
{
  "required": [
    "version"
  ]
}
```

Inline object `#/$defs/extensions/properties/org.ostf.generation-context.v1/allOf/1/then`:

```json
{}
```

Inline object `#/$defs/extensions/properties/org.ostf.appearance.v1/allOf/1/if`:

```json
{
  "required": [
    "version"
  ]
}
```

Inline object `#/$defs/extensions/properties/org.ostf.appearance.v1/allOf/1/then`:

```json
{}
```

Inline object `#/$defs/extensions/properties/org.ostf.legacy-import.v1/allOf/1/if`:

```json
{
  "required": [
    "version"
  ]
}
```

Inline object `#/$defs/extensions/properties/org.ostf.legacy-import.v1/allOf/1/then`:

```json
{}
```

Inline object `#/$defs/extensions/properties/org.ostf.phrase-library.v1/allOf/1/if`:

```json
{
  "required": [
    "version"
  ]
}
```

Inline object `#/$defs/extensions/properties/org.ostf.phrase-library.v1/allOf/1/then`:

```json
{}
```

Inline object `#/$defs/extensions/properties/org.ostf.clip-choices.v1/allOf/1/if`:

```json
{
  "required": [
    "version"
  ]
}
```

Inline object `#/$defs/extensions/properties/org.ostf.clip-choices.v1/allOf/1/then`:

```json
{}
```

<a id="def-phrasetemplate"></a>

## phraseTemplate

Reusable concrete source notes; duration is the repeat period.

Schema: `#/$defs/phraseTemplate`

`"object"`; closed object.

Structural instance locations:

- `$.extensions["org.ostf.phrase-library.v1"].data.templates[*]`

| Parameter / Schema Pointer | Presence | Type and structural constraints | Meaning |
| --- | --- | --- | --- |
| `id`<br>`#/$defs/phraseTemplate/properties/id` | required | [id](#def-id); `"string"`; pattern=`"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$"`; not=`{"pattern":"[\\r\\n\\u2028\\u2029]"}` | Template ID unique within this library, not a Core ID. |
| `duration`<br>`#/$defs/phraseTemplate/properties/duration` | required | [positive](#def-positive); `"integer"`; minimum=`1`; maximum=`9007199254740991` | Positive repeat period in ticks; does not truncate note gates. |
| `notes`<br>`#/$defs/phraseTemplate/properties/notes` | required | `"array"`; items: [note](#def-note); `"object"`; closed object; oneOf (structural rules below) | Concrete notes in nondecreasing onset order; retain array order at equal starts. |
| `name`<br>`#/$defs/phraseTemplate/properties/name` | optional | `"string"` | Display name; not a substitute for identity. |

<a id="def-phrasenotemapping"></a>

## phraseNoteMapping

Mapping from source-note identity and repetition index to a realized Core note.

Schema: `#/$defs/phraseNoteMapping`

`"object"`; closed object.

Structural instance locations:

- `$.extensions["org.ostf.phrase-library.v1"].data.instances[*].noteMap[*]`

| Parameter / Schema Pointer | Presence | Type and structural constraints | Meaning |
| --- | --- | --- | --- |
| `templateNoteId`<br>`#/$defs/phraseNoteMapping/properties/templateNoteId` | required | [id](#def-id); `"string"`; pattern=`"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$"`; not=`{"pattern":"[\\r\\n\\u2028\\u2029]"}` | Source-note ID local to the referenced template. |
| `repeatIndex`<br>`#/$defs/phraseNoteMapping/properties/repeatIndex` | required | [nonnegative](#def-nonnegative); `"integer"`; minimum=`0`; maximum=`9007199254740991` | Zero-based repetition index; below repeatCount for current data. |
| `noteId`<br>`#/$defs/phraseNoteMapping/properties/noteId` | required | [id](#def-id); `"string"`; pattern=`"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$"`; not=`{"pattern":"[\\r\\n\\u2028\\u2029]"}` | Target Core note ID. |

<a id="def-phraseinstance"></a>

## phraseInstance

Complete correspondence between a template and one Core clip.

Schema: `#/$defs/phraseInstance`

`"object"`; closed object.

Structural instance locations:

- `$.extensions["org.ostf.phrase-library.v1"].data.instances[*]`

| Parameter / Schema Pointer | Presence | Type and structural constraints | Meaning |
| --- | --- | --- | --- |
| `id`<br>`#/$defs/phraseInstance/properties/id` | required | [id](#def-id); `"string"`; pattern=`"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$"`; not=`{"pattern":"[\\r\\n\\u2028\\u2029]"}` | Instance ID unique within this library. |
| `templateId`<br>`#/$defs/phraseInstance/properties/templateId` | required | [id](#def-id); `"string"`; pattern=`"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$"`; not=`{"pattern":"[\\r\\n\\u2028\\u2029]"}` | Template ID within this phrase library, not a Core ID. |
| `clipId`<br>`#/$defs/phraseInstance/properties/clipId` | required | [id](#def-id); `"string"`; pattern=`"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$"`; not=`{"pattern":"[\\r\\n\\u2028\\u2029]"}` | ID of the corresponding Core clip. |
| `repeatCount`<br>`#/$defs/phraseInstance/properties/repeatCount` | required | [positive](#def-positive); `"integer"`; minimum=`1`; maximum=`9007199254740991` | Finite repeat count, positive even for an empty template. |
| `transpose`<br>`#/$defs/phraseInstance/properties/transpose` | required | `"integer"`; minimum=`-127`; maximum=`127` | Semitone transposition for pitched notes; percussion slots are unchanged. |
| `noteMap`<br>`#/$defs/phraseInstance/properties/noteMap` | required | `"array"`; items: [phraseNoteMapping](#def-phrasenotemapping); `"object"`; closed object | Complete one-to-one mapping of source-note/repetition occurrences and clip notes. |

<a id="def-phraselibrarydata"></a>

## phraseLibraryData

Concrete phrase templates and already realized instances; never expanded on load.

Schema: `#/$defs/phraseLibraryData`

`"object"`; closed object.

Structural instance locations:

- `$.extensions["org.ostf.phrase-library.v1"].data`

| Parameter / Schema Pointer | Presence | Type and structural constraints | Meaning |
| --- | --- | --- | --- |
| `templates`<br>`#/$defs/phraseLibraryData/properties/templates` | required | `"array"`; items: [phraseTemplate](#def-phrasetemplate); `"object"`; closed object | Reusable concrete phrase templates. |
| `instances`<br>`#/$defs/phraseLibraryData/properties/instances` | required | `"array"`; items: [phraseInstance](#def-phraseinstance); `"object"`; closed object | Correspondences to already realized Core clips. |

<a id="def-clipcandidate"></a>

## clipCandidate

Candidate-local identity and the Core clips enabled for that choice.

Schema: `#/$defs/clipCandidate`

`"object"`; closed object.

Structural instance locations:

- `$.extensions["org.ostf.clip-choices.v1"].data.groups[*].candidates[*]`

| Parameter / Schema Pointer | Presence | Type and structural constraints | Meaning |
| --- | --- | --- | --- |
| `id`<br>`#/$defs/clipCandidate/properties/id` | required | [id](#def-id); `"string"`; pattern=`"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$"`; not=`{"pattern":"[\\r\\n\\u2028\\u2029]"}` | Candidate ID unique within its group. |
| `clipIds`<br>`#/$defs/clipCandidate/properties/clipIds` | required | `"array"`; uniqueItems=`true`; items: [id](#def-id); `"string"`; pattern=`"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$"`; not=`{"pattern":"[\\r\\n\\u2028\\u2029]"}` | Duplicate-free Core clip IDs used by the candidate; an empty candidate is allowed. |
| `name`<br>`#/$defs/clipCandidate/properties/name` | optional | `"string"` | Display name; not a substitute for identity. |

<a id="def-clipchoicegroup"></a>

## clipChoiceGroup

Candidate group and saved selection, corresponding to stored Core enabled states.

Schema: `#/$defs/clipChoiceGroup`

`"object"`; closed object.

Structural instance locations:

- `$.extensions["org.ostf.clip-choices.v1"].data.groups[*]`

| Parameter / Schema Pointer | Presence | Type and structural constraints | Meaning |
| --- | --- | --- | --- |
| `id`<br>`#/$defs/clipChoiceGroup/properties/id` | required | [id](#def-id); `"string"`; pattern=`"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$"`; not=`{"pattern":"[\\r\\n\\u2028\\u2029]"}` | Group ID unique within this clip-choices extension. |
| `candidates`<br>`#/$defs/clipChoiceGroup/properties/candidates` | required | `"array"`; minItems=`1`; items: [clipCandidate](#def-clipcandidate); `"object"`; closed object | One or more candidates. |
| `selectedCandidateId`<br>`#/$defs/clipChoiceGroup/properties/selectedCandidateId` | required | anyOf (structural rules below) | Selected local candidate ID, or null for no selection; the member is required. |
| `name`<br>`#/$defs/clipChoiceGroup/properties/name` | optional | `"string"` | Display name; not a substitute for identity. |

Property-local branch `#/$defs/clipChoiceGroup/properties/selectedCandidateId`:

```json
{
  "anyOf": [
    {
      "$ref": "#/$defs/id"
    },
    {
      "type": "null"
    }
  ]
}
```

<a id="def-clipchoicesdata"></a>

## clipChoicesData

Array of independent clip-choice groups.

Schema: `#/$defs/clipChoicesData`

`"object"`; closed object.

Structural instance locations:

- `$.extensions["org.ostf.clip-choices.v1"].data`

| Parameter / Schema Pointer | Presence | Type and structural constraints | Meaning |
| --- | --- | --- | --- |
| `groups`<br>`#/$defs/clipChoicesData/properties/groups` | required | `"array"`; items: [clipChoiceGroup](#def-clipchoicegroup); `"object"`; closed object | Choice groups; managed clip sets do not overlap across groups. |

## Complete conditional property overlays

These clauses test or further constrain already declared fields. They are not counted again as new parameters.

| Schema Pointer | Constraint |
| --- | --- |
| `#/$defs/relativeAssignment/allOf/0/if/properties/basis` | `{"const":"scaleDegree"}` |
| `#/$defs/relativeAssignment/allOf/0/then/properties/index` | `{"maximum":12}` |
| `#/$defs/extensions/properties/org.ostf.relative-phrase.v1/allOf/1/if/properties/version` | `{"const":"1.0.0-draft.1"}` |
| `#/$defs/extensions/properties/org.ostf.relative-phrase.v1/allOf/1/then/properties/data` | `{"$ref":"#/$defs/relativeData"}` |
| `#/$defs/extensions/properties/org.ostf.generation-context.v1/allOf/1/if/properties/version` | `{"const":"1.0.0-draft.1"}` |
| `#/$defs/extensions/properties/org.ostf.generation-context.v1/allOf/1/then/properties/data` | `{"$ref":"#/$defs/generationData"}` |
| `#/$defs/extensions/properties/org.ostf.appearance.v1/allOf/1/if/properties/version` | `{"const":"1.0.0-draft.1"}` |
| `#/$defs/extensions/properties/org.ostf.appearance.v1/allOf/1/then/properties/data` | `{"$ref":"#/$defs/appearanceData"}` |
| `#/$defs/extensions/properties/org.ostf.legacy-import.v1/allOf/1/if/properties/version` | `{"const":"1.0.0-draft.1"}` |
| `#/$defs/extensions/properties/org.ostf.legacy-import.v1/allOf/1/then/properties/data` | `{"$ref":"#/$defs/legacyData"}` |
| `#/$defs/extensions/properties/org.ostf.phrase-library.v1/allOf/1/if/properties/version` | `{"const":"1.0.0-draft.1"}` |
| `#/$defs/extensions/properties/org.ostf.phrase-library.v1/allOf/1/then/properties/data` | `{"$ref":"#/$defs/phraseLibraryData"}` |
| `#/$defs/extensions/properties/org.ostf.clip-choices.v1/allOf/1/if/properties/version` | `{"const":"1.0.0-draft.1"}` |
| `#/$defs/extensions/properties/org.ostf.clip-choices.v1/allOf/1/then/properties/data` | `{"$ref":"#/$defs/clipChoicesData"}` |

## Complete enum and constant index

| Schema Pointer | Values |
| --- | --- |
| `#/$defs/ref/properties/type/enum` | `["section","track","clip","note","chord","scale","soundSlot","lyricDocument","lyricPhrase","lyricUnit","lyricAlignment","resource"]` |
| `#/$defs/spelledPitchClass/properties/step/enum` | `["A","B","C","D","E","F","G"]` |
| `#/$defs/meter/properties/denominator/enum` | `[1,2,4,8,16,32,64]` |
| `#/$defs/resource/properties/kind/enum` | `["audio","midi","text","other"]` |
| `#/$defs/dependencies/oneOf/0/properties/scope/enum` | `["document","none"]` |
| `#/$defs/extension/properties/status/enum` | `["current","stale","unverified"]` |
| `#/$defs/relativeAssignment/properties/basis/enum` | `["chordTone","scaleDegree"]` |
| `#/$defs/chord/properties/intervals/contains/const` | `[0]` |
| `#/$defs/scale/properties/intervals/contains/const` | `[0]` |
| `#/$defs/dependencies/oneOf/1/properties/scope/const` | `["objects"]` |
| `#/$defs/relativeAssignment/allOf/0/if/properties/basis/const` | `["scaleDegree"]` |
| `#/$defs/legacyData/properties/sourceVersion/const` | `["2.3.0"]` |
| `#/$defs/extensions/properties/org.ostf.relative-phrase.v1/allOf/1/if/properties/version/const` | `["1.0.0-draft.1"]` |
| `#/$defs/extensions/properties/org.ostf.generation-context.v1/allOf/1/if/properties/version/const` | `["1.0.0-draft.1"]` |
| `#/$defs/extensions/properties/org.ostf.appearance.v1/allOf/1/if/properties/version/const` | `["1.0.0-draft.1"]` |
| `#/$defs/extensions/properties/org.ostf.legacy-import.v1/allOf/1/if/properties/version/const` | `["1.0.0-draft.1"]` |
| `#/$defs/extensions/properties/org.ostf.phrase-library.v1/allOf/1/if/properties/version/const` | `["1.0.0-draft.1"]` |
| `#/$defs/extensions/properties/org.ostf.clip-choices.v1/allOf/1/if/properties/version/const` | `["1.0.0-draft.1"]` |
| `#/properties/format/const` | `["OSTF"]` |
| `#/properties/version/const` | `["3.0.0"]` |

## Semantic requirements beyond schema shape

This table indexes normative requirements. Shape matching alone does not establish ordering, references, calculated results or operation correctness.

| Specification section | Additional semantic requirements |
| --- | --- |
| [2](FORMAT_SPECIFICATION.en.md) | Strict UTF-8; no BOM, duplicate keys, nonfinite values or unpaired surrogates; integer fields require integer tokens. |
| [2.3 / 9.3](FORMAT_SPECIFICATION.en.md) | Preserve opaque numeric precision and integer/real token category; never apply a known payload schema to an unknown version. |
| [3.1 / 3.4 / 6.3](FORMAT_SPECIFICATION.en.md) | Computed sums/products and endpoints, not only operands, must fit MAX; absolute onsets are nonnegative. |
| [3.2 / 3.3](FORMAT_SPECIFICATION.en.md) | Core-wide unique IDs, correct reference kinds, and distinct local profile identity scopes. |
| [4.2](FORMAT_SPECIFICATION.en.md) | Sections are start-ordered and nonoverlapping; tempo and meter maps begin at 0 and increase strictly. |
| [5](FORMAT_SPECIFICATION.en.md) | Harmony arrays are start-ordered; intervals strictly increase; labels, bass and scales do not generate notes. |
| [6](FORMAT_SPECIFICATION.en.md) | Ordered clips/notes, retained equal-start order and pickups/tails/overlaps; clip duration is not a truncation mask. |
| [6.4](FORMAT_SPECIFICATION.en.md) | Effective enabled is track AND clip; off precedes on at a shared tick, then note IDs order equal event kinds. |
| [7](FORMAT_SPECIFICATION.en.md) | MIDI hints do not replace sound-slot identity; loading does not fetch or execute resources. |
| [8](FORMAT_SPECIFICATION.en.md) | Typed lyric/document/note references, global lyric timing, and ordered many-to-many alignments. |
| [9](FORMAT_SPECIFICATION.en.md) | Current references must resolve; stale/unverified status does not excuse malformed known payloads. |
| [9.2](FORMAT_SPECIFICATION.en.md) | Dependencies cover all direct Core references of current known profiles and effects inherited from parents. |
| [10.1](FORMAT_SPECIFICATION.en.md) | Check relative-pitch equation, anchor pitch class, actual context bounds and unique target note IDs. |
| [10.2](FORMAT_SPECIFICATION.en.md) | Process IDs are locally unique; current vendorExtension targets another existing extension and requires document scope. |
| [10.3](FORMAT_SPECIFICATION.en.md) | Resolve appearance role/color references and apply the specification’s presentation precedence. |
| [10.4](FORMAT_SPECIFICATION.en.md) | Complete phrase correspondence, clip ownership, source/mapping uniqueness, repetition equations, transposition and bounds. |
| [10.5](FORMAT_SPECIFICATION.en.md) | Local candidate IDs, disjoint managed clips across groups, and agreement between selection and Core enabled flags. |
| [10.6 / 10.7](FORMAT_SPECIFICATION.en.md) | Generation, choice, template replacement and detachment are explicit operations; no execution on load; protection is fixed from before. |
| [11](FORMAT_SPECIFICATION.en.md) | 2.3 migration is not a version-string edit; preserve source text, its hash and the conversion report. |

## Related material and regeneration

- [Complete manual](COMPLETE_MANUAL.en.md)
- [Normative specification](FORMAT_SPECIFICATION.en.md)
- [Explicit operations and CLI/API parameters](OPERATIONS.md)
- [2.3 migration](MIGRATION_2_3_TO_3_0.md)
- [Machine-readable parameter catalog](PARAMETER_CATALOG.json)
- [Sample coverage](COVERAGE.md)

Regenerate this reference and catalog from the package root with the documentation command below. It does not validate or play OSTF documents.

```sh
python3 tools/build_reference.py
```
