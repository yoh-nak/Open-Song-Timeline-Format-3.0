# OSTF 3.0.0 design decisions

Status: design rationale for stable Core `3.0.0` and provisional optional profiles, 24 October 2026. The normative rules are in the specification and schema. Draft 1's Core is retained. The product-to-format mappings below are design inferences, not claims that any named product exports OSTF or implements the proposed profiles.

## 1. Share the chosen composition and preserve its optional meaning

A receiver must be able to recover the chosen finite arrangement without possessing the original composition algorithm. Core therefore stores explicit notes. A capable application can additionally preserve relative meaning, generation inputs, and vendor settings.

This separates three practical capabilities:

| Capability | Minimum information |
| --- | --- |
| Show and export the chosen notes | Core tracks, clips, notes, timing, and targets |
| Explain or edit supported composition relationships | Core plus the corresponding versioned standard profile |
| Reproduce an application's generation behavior | Its supported algorithm, settings, version, inputs, and execution environment |

The first capability does not imply the third. A seed or a parameter named `complexity` alone does not specify an algorithm. Draft 1 therefore gives those settings a vendor namespace instead of pretending that equally named controls are interchangeable.

## 2. Use composition methods as design checks

The survey covers contrasting methods, rather than claiming a complete inventory of every composition application on the internet. Each row links to the publisher's own material. The mapping and boundary columns are proposals made for OSTF.

| Precedent and documented method | OSTF mapping | Boundary kept explicit |
| --- | --- | --- |
| [Scaler 3](https://scalermusic.com/products/scaler-3/): a chord track, multiple composition lanes, Motions, and scenes | Separate harmony and performance tracks; relative relationships; optional sets of alternative performance clips | Motion algorithms and whole-song scene state remain application-specific; clip choices do not switch harmony |
| [InstaComposer 3](https://www.waproduction.com/plugins/view/instacomposer-3): multiple roles, scenes within song sections, procedural controls, and note editing | Open track roles, timeline sections, concrete chosen notes, versioned generator records | Track/scene counts and probability or complexity control meanings are not copied into Core |
| [LANDR Composer](https://www.landr.com/plugins/landr-composer/): chord, bass, melody, and arpeggio generation with piano-roll editing | Common track/clip/note model; accompaniment is stored explicitly | A chord label does not cause an OSTF reader to invent accompaniment |
| [RapidComposer](https://musicdevelopments.com/workingwithphrasest.html): reusable phrases with chord- and scale-relative notes and variations | Relative meaning beside realized pitches; finite templates, instances and occurrence maps; explicit linked updates and detachment | Chord fitting, voicing optimization and a per-instance override layer need additional rules |
| [Mixed In Key Captain Melody](https://mixedinkey.com/captain-epic-tutorials/captain-melody-epic-guide/): an idea region can update selected aspects while locked notes remain | Generation inputs, output references, target range and protected IDs; explicit before/after note comparison | Snapshot comparison checks defined note properties; it does not establish generation history or full acoustic equivalence |
| [Unison MIDI Wizard](https://unison.audio/midi-wizard/): imported chord progressions can guide melodies and linked bass generation | Typed, potentially multiple inputs and explicit outputs; separate musical roles | Importing a source does not imply that the source's complete instrument or effect state is portable |
| [Synfire Figure](https://docs.cognitone.com/synfire/G3/EN/parameters/Figure.html): parametric symbols and segments are rendered against harmony | Keep the rendered notes and preserve the parametric representation in an understood extension | The small relative-pitch profile is not a universal replacement for a parametric rendering algorithm |
| [Hookpad Aria](https://www.hooktheory.com/hookpad/aria): chords can follow a melody, a melody can follow chords, or both can be generated | Chord-only and melody-only files are valid; generation inputs need not be one-way | Harmony is contextual information, not a mandatory prerequisite for every note |
| [Magenta Studio](https://magenta.withgoogle.com/studio): continuation, interpolation, groove, and drum generation use selected clips | Multiple typed inputs, input read ranges, and finite stored results | Reading a file does not rerun stochastic generation or infer missing model parameters |
| [AIVA](https://www.aiva.ai/): audio or MIDI influences can guide generation and generated tracks can be edited | Resource references plus explicit generated notes | A resource URI does not authorize fetching it and is not an audio playback instruction |
| [ChordPulse](https://www.chordpulse.com/guide/play-menu.html): accompaniment layers depend on style and the chord cycle can be repeated independently | Harmony spans and performance placement are separate; chosen repetitions are materialized | A clip boundary is not an implicit repeat, phase reset, or note cutoff |
| [Dorico duration model](https://www.steinberg.help/r/dorico-se/6.2/en/dorico/topics/key_editor/key_editor_notes_duration_played_notated_c.html): played and notated durations are distinct | Core duration is the gate; future notation metadata can describe score duration | A shorter gate is not automatically a shorter written note |

The software descriptions are used only to identify observable workflow concepts. Product quality claims, internal model details, and promises of equivalent rendering are not inferred from marketing material.

## 3. Keep the core small without losing timing

### No velocity in Core

This is a deliberate scope decision for a composition interchange format. It is not based on an assumption that composition products never control dynamics. For example, the official InstaComposer and Unison descriptions include velocity-related controls. A transfer of those products' complete performance data would need an explicitly defined additional representation and a disclosed conversion policy.

Start and gate duration remain exact integer ticks within the declared PPQ. This retains rhythmic placement, anticipation, sustain, and overlap without requiring a full instrument-control stream. Omitting velocity does not make the timestamp coarse or equate the gate to the score's written duration.

### A clip is a placement span

An editor needs a useful region to select, move, or repeat. A note can begin before that region or continue after it. Core separates the region's span from the note's actual onset and gate end. The author chooses a finite arrangement and stores the resulting notes. Exporters must not silently clamp, merge, or regenerate them.

### Declared PPQ

960 is convenient for many rhythms but cannot divide a quarter note exactly into seven integer ticks. A PPQ of 6720 gives seven 960-tick parts. A receiver uses the declared PPQ; a resampler reports rounding if the destination cannot represent the same timing.

### Independent percussion identity

Two kick sounds may have the same role or output note hint but still be different composition targets. A sound slot's ID is authoritative. The optional `midiNote` is only a mapping hint. Pitched bass sounds remain ordinary pitched notes.

## 4. Make interpretation and synchronization explicit

An extension envelope says which version it uses, whether its claims are current, and what it depends on. Known exact versions can be checked. Unknown versions stay opaque even if their namespace is familiar. This prevents a later profile's data from being forced through an earlier interpretation.

For a supported relative assignment, `current` means the declared relation and realized pitch agree. A stale or unverified relation can be retained with warnings while the stored Core performance remains usable. Structural corruption of a known profile is still an error. Appearance metadata can continue to show resolvable colors without rebinding missing IDs to similar names.

If an unsupported extension depends on an edited note, clip, track, or the whole document, a writer cannot truthfully keep asserting that it is synchronized. The reference editing helper conservatively changes affected `current` claims to `unverified` and preserves the payload.

This also explains the use of global IDs and typed references. A label change, track reorder, or coincidental matching string must not reconnect unrelated music. Numeric precision is part of this preservation obligation: opaque settings must not be rounded or change JSON token kind during a save.

## 5. Preserve incomplete work

A musical document may contain only harmony, only a melody, or only lyrics. Every required container exists, but musical arrays can be empty. Tempo and meter still have explicit values at tick zero. The format supports working ideas without manufacturing the missing parts.

Harmony records can retain a display label before structural interpretation is known. A label-only chord is displayable but is not sufficient for a `current` chord-tone calculation. Declared harmonic contexts may overlap and are selected by ID. Notes are not constrained to belong to a chord or scale.

Lyrics have documents, phrases, units, and explicit many-to-many note alignments. A whole phrase remains meaningful even when its syllable segmentation or pitch allocation is unfinished.

## 6. Migrate 2.3 conservatively

The reviewed [2.3 specification](https://github.com/yoh-nak/Open-Song-Timeline-Format-2.3/blob/90fce246de28a1b265fb6b25cc2866c70036fda6/docs/FORMAT_SPECIFICATION.md) and [parameter reference](https://github.com/yoh-nak/Open-Song-Timeline-Format-2.3/blob/90fce246de28a1b265fb6b25cc2866c70036fda6/docs/PARAMETER_REFERENCE.md) leave much inner harmony, melody, and lyric data opaque. A sample establishes a practical convention, but cannot alone make every 2.3 producer's musical semantics identical.

The migration tool therefore has a structure-only default and an explicit sample-convention mode. Unknown musical fields prevent the affected sample object from becoming active. The original UTF-8 source and its hash stay in an archive with a detailed conversion report. A successful target validation is not a claim of complete source conformance or complete musical conversion.

## 7. Bound the first reusable-phrase and choice contracts

Draft 2 introduces two optional profiles after separating the concepts that can be shared precisely from those requiring a rendering engine. `org.ostf.phrase-library.v1` stores a finite note template, a positive period, semitone transposition, finite repeats and a complete map to Core notes. `org.ostf.clip-choices.v1` stores alternatives as sets of existing Core clips and an explicit selected candidate.

A phrase template can contain pickups, notes after its period and tails. Period means repeat spacing, not a constraint that cuts off notes. One instance owns an entire Core clip, with every occurrence mapped exactly once. This restriction makes the initial relationship testable. Individual edits can leave the relationship stale or detach it; there is no ambiguous combination of linked data and hidden overrides.

Explicit materialization creates new Core notes. Ordinary loading does not. Existing instances are not silently rebuilt. An editor without the profile still obtains the same stored performance. Validation checks saved maps in time proportional to their supplied data, without expanding a potentially huge repeat count.

Revision 1 defines an explicit transaction that replaces a current template and refreshes every linked instance. The wire relationship already contains all information needed for this operation, so the schema and profile version remain unchanged. Existing occurrence maps preserve surviving Core IDs, even when another writer chose them. Renaming a template note is removal plus addition, not identity inferred from pitch or array position.

Core lyric references make deletion consequential. If a note slated for removal is still aligned to a lyric unit, the entire update is refused. The editor must explicitly adjust that alignment or detach a placement that should keep its current notes. This keeps vocal text from disappearing as a side effect of editing a backing motif. Protection checks additionally enforce the fixed before-snapshot set chosen for an operation.

Detachment removes only the selected relationship records. Core content, lyric links and IDs remain unchanged, including manually edited notes behind a stale relationship. The envelope retains its prior status rather than promoting all remaining relationships to current. This supplies a precise independent-edit path without inventing an override layer.

Choice groups manage their union of clips. A selected candidate controls each managed clip's own enabled flag; it does not override the parent track's mute. Clips may be shared by alternatives inside one group, while cross-group ownership is forbidden. These rules give silent candidates, common bass lines and multiple-part alternatives deterministic meanings without adding an entire transport or scene engine.

The phrase and choice profiles are independently optional and may coexist. When a selection changes clip states, another dependent profile is conservatively marked unverified. A more capable editor may revalidate and reassert current state; the reference operation does not claim that all unrelated semantic layers were regenerated.

Protection comparison uses the before snapshot to fix the protected ID list and compares target, absolute onset, gate and effective enabled state. This avoids losing protection by deleting the after list. It is a useful editing check, not proof that a particular generator ran or that playback in seconds and sound are identical.

## 8. Decisions still requiring interoperability evidence

| Topic | Initial 3.0 position | Evidence needed for a broader contract |
| --- | --- | --- |
| Reusable phrase templates and instances | Exact finite repetition/transposition, complete occurrence maps, explicit all-instance updates and detachment | An override layer, chord-aware fitting and round trips in independent implementations |
| Scenes and alternative candidates | Selected sets of performance clips with explicit activation | Harmony, tempo, lyric and section alternatives; whole-document switching and conflict rules |
| Input-note ordinal patterns | Not equated with chord or scale degree | Definitions of input ordering, missing notes, duplicate pitches, and octave behavior |
| Score notation | Gate timing plus lyric alignment | Written duration, ties, voices, spelling, tuplets, and their relationship to played timing |
| Detailed percussion mapping | Stable slots and optional hints | Mapping identity, articulations, choke behavior, and fallback requirements |
| Additional expression | No velocity in Core | A bounded optional representation with clear fallback and loss reporting |
| Adoption and compatibility | Reference source package; current stable changes unexecuted | Independent exporters/readers and actual application round trips establish broader interoperability; publication terms are tracked separately |

The first useful adopter should be able to export explicit Core notes. More capable adopters can add well-defined relationships without making every basic reader implement a composition engine.

## 9. Close the initial release scope

The documented Core, six optional profile namespaces and existing explicit operations form the initial feature boundary. Numerical bounds and field meanings stay as specified. Further generation, overrides, notation, expression and external adapters are later extensions, not initial release conditions.

The stable package implements the identifier work identified in Revision 2: an exact stable schema and root dispatch, continued Draft 1/Draft 2 reading, continued Draft 2 editing, stable editing support, explicit conversion across the three roots and a stable migration default with an explicit Draft 2 option. The old draft-conversion aliases keep their original endpoints. There is no implicit upgrade on load.

Optional profile versions remain `1.0.0-draft.1`. A stable Core can coexist with provisional optional editing metadata because every reader can use the stored performance independently. Promoting a profile later requires an exact versioned contract; it does not authorize bulk replacement of unknown versions.

The [release assessment](RELEASE_READINESS.md) describes the complete formal distribution, and [LICENSE.md](../LICENSE.md) assigns the documented release scopes. No runtime verification was performed for this packaging work; historical results are not claimed for the stable code. Product surveys describe design precedents, not product endorsement, OSTF support, or a claim to have inventoried every composition tool on the Internet.
