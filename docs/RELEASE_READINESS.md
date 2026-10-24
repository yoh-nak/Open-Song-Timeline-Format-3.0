# リリース準備状況 / Release readiness

**判定：OSTF 3.0.0の正式リリース用資料一式を、GitHubに一度でアップロードできる98ファイルの配布セットとして用意しました。** この判定は公開資料の準備状態です。GitHubへのアップロード、タグ作成、Release公開は本作業では行っていません。動作検証を追加の公開条件にはしていません。

**Assessment: the complete formal-release materials are prepared as a 98-file distribution suitable for one GitHub browser upload.** This assesses preparation of the publication package. No GitHub upload, tag or Release was created. No additional runtime verification is imposed as a publication prerequisite.

## 1. 公開対象 / Publication scope

| Item | State |
| --- | --- |
| Core identity | Stable `3.0.0`, extension `.ostf`, UTF-8 JSON |
| Six standard optional profiles | Exact provisional `1.0.0-draft.1`; not promoted by the Core release |
| Normative specification | Japanese and English, with the existing stable Core meanings |
| Complete manuals | Japanese and English, 23 sections per edition |
| Full parameter references | Japanese and English; all 51 named definitions and 168 declared parameter entries |
| Conditional constraints | 14 property overlays,37 enum-value occurrences,13 const locations and27 schema branch-rule locations documented |
| Samples | 60 main 3.0.0 `.ostf` examples plus 2 verbatim 2.3 migration inputs |
| Coverage | All 168 declared entries and37 enum-value occurrences have concrete sample-location witnesses;14overlays,13 constants and51definitions also located |
| Machine data | Parameter catalogue, sample catalogue, full coverage inventory and file manifest |
| Reference programs | Five existing Python sources; documented reader, validator, editor and migrator contracts |
| Schemas | Stable 3.0.0 plus retained Draft 1/Draft 2 schemas |
| Usage terms | Final release notice for CC BY 4.0 documents/schema/data and MIT reference programs |
| Release text | Root `RELEASE_NOTES.md`, suggested title `OSTF 3.0.0` / tag `v3.0.0` |
| File limit | 98 files recursively, within 100; all files below 25 MiB |
| External publication | Not performed |
| Runtime verification | Not performed for this release preparation |

## 2. What “complete” means / 全網羅の意味

The bounded inventory is the actual stable Schema and its six exact supported profile payload schemas, read with the normative prose. There are 168 canonical property declarations and 14 conditional reassertions/overlays. These sum to 182 property occurrences in the schema source. Shared type definitions are counted once; declarations in distinct structural branches remain separate. All declared property entries and all 37 enum values have presence witnesses in the 60 main samples. Both note targets, both selection forms, paired optional values and all six known/unknown profile-version branches are represented.

任意の値を取り得る数値・文字列、ベンダー固有のJSON、全楽曲パターン、全パラメーターの組合せは有限個のファイルで列挙できないため、定義・代表例・境界例で示します。構造不正や拒否される入力は通常の曲サンプルへ混ぜず、リファレンスと適合条件に記述します。これらの範囲を明示した上で、現行の定義項目を全網羅した配布資料としています。

## 3. What was done / 今回の作業

- Reorganized the package around complete manuals, references and examples; supplied bilingual navigation and release text.
- Authored 27 new stable examples, retained 33 unique prior examples with only their root-version token changed, and kept two 2.3 source files byte-for-byte as migration inputs.
- Matched parameter declarations, finite choices and structural forms with sample-file locations using a static documentation inventory.
- Read the newly authored sample relationships and explanatory documents for consistency, retained exact opaque number tokens and recorded source attribution/file metadata.
- Kept the five runtime files and three schemas byte-for-byte identical to stable preparation revision 1. No wire semantics or profile version was changed by this documentation work.
- Consolidated license scopes into `LICENSE.md`; included original-source provenance and prepared a publication-ready release body.

## 4. Evidence boundary / 実施していない確認との区別

プロジェクト本体のimport・実行、CLI/help、validator、Schema適合検査、試験runner、DAW/MIDI再生、展開後の動作検証は行っていません。ファイル数、本文、参照パス、hash、パラメーター出現位置の確認は、資料作成・梱包の静的な作業です。サンプルが操作の実行出力である、全検証に合格した、外部製品と相互運用できた、という意味にはしません。

Earlier Draft 2 Revision 1 execution evidence belongs to its earlier source snapshot and remains in earlier development packages. This curated release omits historical test runners and reports; their counts are not passing claims for stable 3.0.0. The 89 viewpoints in `CONFORMANCE.md` describe expected behavior, not executed successes.

## 5. Remaining publication action / 公開時に行うこと

Unzip the distribution and upload the contents of the package directory into the intended GitHub repository using **Add file → Upload files**. Review the paths and commit. Create the desired GitHub Release/tag and use the prepared `RELEASE_NOTES.md` body; attach the ZIP if desired. The repository destination is intentionally left to the owner, since this work did not create or rename a repository.

[GitHub's current upload documentation](https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository) permits up to 100 files per browser upload and 25 MiB per file (consulted 2026-10-24). This package contains98 files. Uploading the ZIP as a repository file does not extract its contents; uploading it as a Release asset provides the archive for download.

## 6. Future development / 後続の範囲

Automatic chord fitting, partial overrides, time scaling, nested phrases, whole-song scenes, notation and engraving, additional expression and external application adapters are future extensions. They are not missing items in the initial Core scope. No named composition product is claimed to support OSTF. Profile stabilization requires its own exact versioned contract; Core release numbering does not silently change payload interpretation.

See the full [manual](COMPLETE_MANUAL.ja.md), [reference](PARAMETER_REFERENCE.ja.md), [coverage](COVERAGE.md), [source attribution](SOURCE_ATTRIBUTION.md) and [license](../LICENSE.md) for the concrete deliverables.
