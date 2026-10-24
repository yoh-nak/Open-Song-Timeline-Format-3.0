# Source attribution / 出典・由来

## OSTF 2.3 baseline

- Repository: <https://github.com/yoh-nak/Open-Song-Timeline-Format-2.3>
- Owner identity used for attribution: **yoh-nak**
- Pinned commit: `90fce246de28a1b265fb6b25cc2866c70036fda6`
- Tree: `9cc6d590068d9229030c530e3af4d3d450fd2fd4`
- Baseline retrieval date: **2026-10-24**

The following inventory preserves the reviewed source metadata. It does not assert that every listed file is bundled. This package includes the exact source files `samples/54_full_feature.ostf` and `samples/29_lyrics_alignment.ostf` under `samples/legacy_2_3/`; both retain their **2.3.0** version and original bytes. These are migration inputs, not 3.0 examples. The other entries document the design/migration baseline.

| Source path at pinned commit | Bytes | SHA-256 |
| --- | ---: | --- |
| `README.md` | 953 | `2badb5399e259c060d304667a150473461dbdac402152b9d39181e0d5706699f` |
| `docs/FORMAT_SPECIFICATION.md` | 9211 | `7f2715ec0a0108c79965c05f8ac1315678d401a88d4181c3d798bf4bcd29fb48` |
| `docs/PARAMETER_REFERENCE.md` | 7557 | `278139a541dfcaa1cf7e00a3316ee4991ebc16cd847f349a3f1808c57d7af547` |
| `docs/COMPLETE_MANUAL.md` | 5480 | `cdefbebccb835e8007c9dffcc8e897ec2f32178023b51751dabd90bd7ee5a46a` |
| `docs/RELEASE_NOTES.md` | 534 | `2cbcce56ad78509462c3f52a4f512a8cc77dfa8edcf45a26b082d3e96ac9bd38` |
| `schema/ostf-2.3-standalone-candidate.schema.json` | 9472 | `62b9a9b4105d6e6fb5371f8703b7d86494b070c390f60de12471110dbc69f5b8` |
| `samples/54_full_feature.ostf` | 2895 | `cf8a24d487c7f09b390f946839cb08d08be7d566428dda12ec556326240bca64` |
| `samples/23_melody_multi_clip.ostf` | 1907 | `2c7a1503c6b747428fb2c4f25356af345fa3c9ffe1c11ec23eaa90e395c5cd69` |
| `samples/11_meter_changes.ostf` | 1105 | `4f8ce6394b9d7adbe8d2e73192119b91c55ca1f799bab2001e9954ca93f0d93f` |
| `samples/29_lyrics_alignment.ostf` | 1239 | `34887f5b5910a19a24ec61af202fb10d5ecba9f6c57a784b148144bb3039b188` |
| `samples/22_melody_one_clip.ostf` | 1170 | `4af033c92fc9893608a18d4013730dd63d8ede989bd1b195eae5de56e12a4a11` |

## New 3.0 distribution

The stable Core source baseline is the OSTF 3.0.0 preparation revision 1 assembled in this work. The five reference Python files and three schema files are retained byte-for-byte. This formal distribution reorganizes and expands documentation, the field catalogue, static coverage evidence and musical examples. [PACKAGE_MANIFEST.json](../PACKAGE_MANIFEST.json) records the actual distributed bytes and SHA-256 values; it excludes its own hash to avoid a circular definition.

Samples 01–33 are authored root-version copies of the earlier unique examples, retaining data and opaque numeric tokens. Their root changes from the earlier Draft to `3.0.0`; filenames 27–29 remove the old draft label. Samples 34–60 are newly authored for field, enum and feature coverage. The [sample catalogue](../samples/catalog.json) records individual provenance. A root-version copy is not a claim that `convert_version` was run: an actual conversion can additionally change affected extension status. Before/after samples illustrate stored states without claiming runtime generation in this release.

The [design decisions](DESIGN_DECISIONS.md) cite official product information used as precedents. Product names identify those sources. The survey is neither exhaustive over all software on the Internet nor a representation that those products support OSTF.

## Release and license references

- Material scopes and standard licenses: [LICENSE.md](../LICENSE.md).
- GitHub browser upload documentation: <https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository> (consulted 2026-10-24; up to 100 files per upload and 25 MiB per file).
- CC BY 4.0 legal terms: <https://creativecommons.org/licenses/by/4.0/legalcode.en>.
- MIT standard terms: <https://opensource.org/license/mit>.

License notices in this package cover the owner's rights in the identified project material. They do not replace third-party rights or automatically change rights in externally archived sources.
