# Open Song Timeline Format — OSTF 3.0.0

**Exchange composition structure and the concrete performance currently adopted for multiple musical parts.** An `.ostf` file is UTF-8 JSON. Core notes store a pitch or percussion target, an onset and a gate duration. **Core does not define velocity.**

[日本語](README_JA.md) · [Complete manual](docs/COMPLETE_MANUAL.en.md) · [Parameter reference](docs/PARAMETER_REFERENCE.en.md) · [Specification](docs/FORMAT_SPECIFICATION.en.md) · [Examples](samples/INDEX.md)

## Release contents

- **Stable Core wire version: `3.0.0`.** File extension: `.ostf`.
- **Six optional standard profiles remain provisional at exact version `1.0.0-draft.1`.** Profile maturity is independent of the stable Core root.
- **98 files total:** 60 authored 3.0.0 examples, two original 2.3 migration inputs, bilingual manuals/reference/specification, machine-readable inventories, schemas and reference source.
- **Traceable completeness:** [coverage](docs/COVERAGE.md) maps declared properties and finite enum choices to concrete sample locations. It does not claim to enumerate infinitely many arrangements or arbitrary vendor JSON values.
- **No runtime verification was performed for this distribution.** Project imports, validator/CLI execution, tests, DAW and MIDI playback were not run. The coverage inventory is static documentation, not a passing execution report.

## Where to start

| Goal | Read |
| --- | --- |
| Implement a small exporter | [Core quickstart](docs/IMPLEMENTER_QUICKSTART.md) and [melody example 04](samples/04_melody_only.ostf) |
| Understand all parameter families | [Complete manual](docs/COMPLETE_MANUAL.en.md) |
| Look up types, required fields, bounds and conditions | [Full parameter reference](docs/PARAMETER_REFERENCE.en.md) and [machine catalogue](docs/PARAMETER_CATALOG.json) |
| Implement normative behavior | [Specification](docs/FORMAT_SPECIFICATION.en.md) with the [3.0.0 schema](schema/ostf-3.0.0.schema.json) |
| Find complete song documents | [Sample index](samples/INDEX.md), [catalogue](samples/catalog.json), and [coverage](docs/COVERAGE.md) |
| Materialize phrases, replace templates or select candidates | [Profile supplement](docs/OPTIONAL_PROFILES.md) and [operations](docs/OPERATIONS.md) |
| Use the Python API and CLI | [Reference implementation](docs/REFERENCE_IMPLEMENTATION.md) |
| Import 2.3 data | [Migration guide](docs/MIGRATION_2_3_TO_3_0.md) and [source attribution](docs/SOURCE_ATTRIBUTION.md) |
| Publish the release materials | [Release notes](RELEASE_NOTES.md), [readiness](docs/RELEASE_READINESS.md), and [license](LICENSE.md) |

## Design

Stored Core notes determine the adopted performance. A reader does not regenerate accompaniment from harmony, choose another candidate or play both a template and its already materialized notes. Harmony-only, melody-only, lyrics-only and unfinished documents are supported.

Optional profiles describe relative notes, generation inputs/outputs, appearance, original-source archives, reusable phrases and clip alternatives. Vendor namespaces can preserve proprietary settings without forcing every reader to implement a composition engine. Unsupported metadata is kept opaque; edits must conservatively invalidate claims whose correspondence can no longer be guaranteed.

Instrument names are descriptions and percussion `midiNote` values are optional output hints. The format does not reproduce a plug-in state or complete MIDI device configuration. A DAW adapter must state how it supplies values such as velocity that Core does not define.

## Package layout

| Location | Files | Contents |
| --- | ---: | --- |
| Root | 12 | English/Japanese READMEs, license, changelog, release notes, manifest, dependencies, five Python files |
| `docs/` | 18 | Complete specifications, manuals, references and coverage |
| `schema/` | 3 | Stable Core and preserved Draft 1/2 schemas |
| `tools/` | 1 | Static parameter-reference documentation builder |
| `samples/` recursively | 64 | 60 stable examples, two legacy inputs, index and catalogue |
| **Total** | **98** | No nested ZIP or authoring scratch files |

[PACKAGE_MANIFEST.json](PACKAGE_MANIFEST.json) records the distributed paths, byte lengths and SHA-256 hashes. Its own hash is excluded to avoid circularity. Draft schemas remain bundled for the reference reader; all 60 main examples declare `3.0.0`.

## One browser upload to GitHub

Extract the ZIP, open **Add file → Upload files** in the intended repository, and drag the **contents** of `OSTF_3_0_0_GitHub_Release` into the upload area. Retain the directory structure with README at repository root, review the resulting paths and commit. The package fits GitHub's documented maximum of 100 files in a single browser upload; every file is below its 25 MiB browser limit. [Official upload instructions](https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository), consulted 2026-10-24.

For a GitHub Release, use the suggested tag `v3.0.0`, title `OSTF 3.0.0`, and the prepared body in [RELEASE_NOTES.md](RELEASE_NOTES.md). The ZIP may also be attached as a release asset. Uploading a ZIP into a repository does not automatically extract it. Choose a new 3.0 repository or an intentional destination if keeping 2.3 separate. No upload, tag or publication was performed while authoring this package.

## License

Specification, schemas, documentation and examples: **CC BY 4.0**. Reference programs and executable snippets: **MIT**. [LICENSE.md](LICENSE.md) defines exact scopes and attribution. Product names in the design survey are source references, not OSTF support claims, partnerships or certification.
