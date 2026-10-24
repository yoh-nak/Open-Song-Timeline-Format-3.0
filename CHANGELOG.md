# Changelog

## 3.0.0 — formal release distribution

Prepared 2026-10-24. Core wire version is `3.0.0`; this package does not publish a GitHub tag or Release automatically.

### Composition format

- Explicit tracks, clips and notes share one integer-tick timeline. Notes specify pitch or percussion slot, onset and gate; Core has no velocity.
- Song structure, tempo/meter maps, structured or label-only harmony, scale context, lyrics/alignment and source-resource references have defined Core contracts.
- Six standard optional profiles remain at exact provisional version `1.0.0-draft.1`: relative phrase, generation context, appearance, legacy import, phrase library and clip choices.
- Stored notes and enabled states are authoritative. Loading does not generate, synchronize templates or activate a candidate.
- Strict JSON, global Core identity, typed references, numerical bounds, pickups, tails, overlap, unknown-data retention and status invalidation are specified.

### Reference implementation carried forward

- Preserved three-root reader dispatch for Draft 1, Draft 2 and stable 3.0.0.
- Explicit root conversion, phrase materialization, whole-template replacement and linked refresh, detachment, clip selection and protected snapshot comparison.
- Conservative 2.3 migration defaults to 3.0.0, with explicit Draft 2 output available; source text/hash and conversion assumptions are preserved.
- Five runtime files and all three schemas are byte-identical to preparation revision 1. This packaging update changes documentation and example inventory, not their code or wire semantics.

### Complete publication materials

- Added complete Japanese/English manuals and references, a machine parameter catalogue, full static property/enum/branch coverage mapping and a source attribution document.
- Consolidated 60 stable `.ostf` examples and two preserved 2.3 migration inputs, with provenance and thematic navigation.
- Prepared final README, license scope, release notes and per-file manifest within 98 files.
- Applied the prepared CC BY 4.0 documentation/data and MIT reference-code scope in the release license notice.
- Omitted duplicated historical samples, development test runners and historical execution reports from this release-focused set. Earlier packages retain them.

### Evidence and scope

No project runtime verification was performed for this distribution. Static field coverage is documentation evidence, not an execution result. Earlier Draft 2 Revision 1 results do not establish a pass for stable 3.0.0. External product support and DAW/MIDI interoperability are not claimed.

### Deferred extensions

Automatic chord fitting, partial instance overrides, time scaling, nested templates, whole-song scenes, notation/engraving, expression profiles and external adapters remain future work. They are not prerequisites for this initial Core release.
