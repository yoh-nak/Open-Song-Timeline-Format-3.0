# OSTF 3.0.0

**Core wire version:** `3.0.0`  
**Suggested GitHub tag:** `v3.0.0`  
**Release material prepared:** 2026-10-24  
**Distribution:** 98 files; 60 OSTF 3.0 examples and two OSTF 2.3 migration inputs.

## 日本語

OSTF 3.0.0は、曲構成・和声・歌詞と、現在採用している複数パートの具体的な演奏を交換するための正式Core仕様です。ノートには、音高または打楽器の発音対象、発音位置、ゲートタイムを保存します。Coreにベロシティーは設けません。

### 主な内容

- track → clip → noteによる複数パート、共通PPQの整数tick、安定したIDと型付き参照。
- コード名と構造化和声、スケール、テンポ・拍子変更、歌詞の多対多対応、発音スロット、素材参照。
- 弱起、配置区間外で始まるノート、クリップを越えるゲート、同音重複、track/clipの有効状態を明示的に保持。
- 相対フレーズ、生成文脈、表示、原典アーカイブ、再利用フレーズ、クリップ候補という6つの標準任意profile。
- templateの有限反復・移調、原型置換と全instance更新、リンク解除、候補選択、固定した操作前後データによる保護比較の明示操作。
- Draft 1・Draft 2・正式3.0.0の明示的な版変換と、元データを保持する保守的な2.3移行。

### 全網羅の公開資料

日本語・英語の完全マニュアル、パラメーターリファレンス、規範仕様、JSON Schema、参照コード、サンプル索引、機械可読辞典・対応表を同梱します。主サンプル60件はすべて`.ostf`、root `version`はすべて`3.0.0`です。2.3原典2件は移行入力として別ディレクトリへ分離しています。

168件の宣言パラメーター、14件の条件付き再制約、7組・37値のenum、13箇所のconst、51の名前付き定義をリファレンスへ収録し、すべてにサンプル内の所在を対応付けました。全任意文字列・数値・独自拡張・楽曲組合せの列挙を意味しません。

入口は`README_JA.md`、`docs/COMPLETE_MANUAL.ja.md`、`docs/PARAMETER_REFERENCE.ja.md`、`samples/INDEX.md`です。Core全項目をまとめた例は34、全6profileを併記する例は58です。

### 版と確認範囲

Coreは正式版`3.0.0`です。6つの任意profileは、それぞれ正確な暫定版`1.0.0-draft.1`として提供します。Coreの正式版化はprofileの自動昇格を意味しません。読み込みだけで生成、候補選択、フレーズ再同期を実行せず、保存されたCoreノートを演奏の正本とします。

この配布準備では動作検証を行っていません。静的な項目対応表は、validator・試験・再生・外部製品連携の合格を意味しません。過去のDraft実行結果を正式3.0.0の実績として転用していません。

仕様・Schema・説明資料・サンプルはCC BY 4.0、参照プログラムと実行コード例はMITです。対象範囲と帰属は`LICENSE.md`、原典の固定commitとhashは`docs/SOURCE_ATTRIBUTION.md`、配布ファイル一覧は`PACKAGE_MANIFEST.json`に記載します。

## English

OSTF 3.0.0 is the initial stable Core specification for exchanging song structure, harmony, lyrics and the concrete performance currently adopted across multiple parts. A note stores a pitch or percussion target, onset and gate duration. Core does not define velocity.

### Highlights

- Explicit tracks, clips and notes on a shared integer-tick PPQ timeline, with stable identities and typed references.
- Harmony labels and structured chords/scales, tempo/meter maps, many-to-many lyric alignment, percussion slots and resource references.
- Preserved pickups, late local starts, gate tails, same-pitch overlap and independent track/clip enabled states.
- Six optional standard profiles: relative phrase, generation context, appearance, legacy import, phrase library and clip choices.
- Explicit finite materialization, transposition, whole-template replacement and linked refresh, detachment, candidate selection and fixed before/after protection checks.
- Explicit conversion among Draft 1, Draft 2 and stable roots, plus conservative OSTF 2.3 migration with original-source preservation.

### Complete release materials

The 98-file distribution includes complete Japanese/English manuals, full parameter references, normative specifications, schemas, reference source, a sample index and machine-readable parameter/coverage catalogues. All 60 main examples are `.ostf` files declaring root `3.0.0`; two preserved 2.3 migration inputs are clearly separated.

The reference inventories 168 declared parameters, 14 conditional overlays, seven enum sets with 37 value occurrences, 13 constants and 51 named definitions. Each has sample-location evidence. This is not an enumeration of unlimited numeric/string values, proprietary settings or every arrangement combination.

Start with `README.md`, `docs/COMPLETE_MANUAL.en.md`, `docs/PARAMETER_REFERENCE.en.md` and `samples/INDEX.md`. Example34 combines all Core fields; example58 combines all six profiles.

### Versioning and evidence

Core is stable `3.0.0`. The six optional profiles remain provisional at exact version `1.0.0-draft.1`. Loading does not generate, select alternatives or refresh linked notes. Stored Core notes remain authoritative.

No runtime verification was performed for this release preparation. Static coverage is not a validator, test, playback or interoperability pass. Earlier Draft execution records are not reused as evidence for stable 3.0.0.

Documentation, schemas, supporting data and examples use CC BY 4.0; reference programs and executable snippets use MIT. Exact scopes and attribution are in `LICENSE.md`. Source provenance is in `docs/SOURCE_ATTRIBUTION.md`, and file hashes are in `PACKAGE_MANIFEST.json`.
