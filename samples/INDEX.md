# OSTF3.0 サンプル索引 / Sample index

**60件のOSTF3.0記述例と、移行入力専用のOSTF2.3原典2件**を収録します。サンプルファイルの拡張子はすべて`.ostf`です。

The collection contains **60 authored OSTF3.0 examples and two verbatim OSTF2.3 migration inputs**. Every sample has the `.ostf` extension.

## 読み始める順番 / Where to start

最小構成は[02](02_empty_sketch.ostf)、単旋律は[04](04_melody_only.ostf)、和声のみは[03](03_harmony_only.ostf)、複数パートは[01](01_four_part_sketch.ostf)です。全Core項目を一つで見るには[34](34_all_core_fields.ostf)、全6profileの共存は[58](58_complete_workflow.ostf)、Coreだけの曲構成は[60](60_song_form_arrangement.ostf)を参照してください。

Start with02 for empty content,04 for a melody,03 for harmony only, and01 for multiple parts. Example34 presents every named Core field,58 combines the six standard profiles, and60 shows a complete Core-only arrangement.

- [完全マニュアル / Complete manual](../docs/COMPLETE_MANUAL.ja.md) · [English](../docs/COMPLETE_MANUAL.en.md)
- [全パラメーター / Parameter reference](../docs/PARAMETER_REFERENCE.ja.md) · [English](../docs/PARAMETER_REFERENCE.en.md)
- [収録範囲の対応表 / Coverage mapping](../docs/COVERAGE.md) · [Machine-readable catalogue](catalog.json)
- [規範仕様 / Normative specification](../docs/FORMAT_SPECIFICATION.ja.md) · [English](../docs/FORMAT_SPECIFICATION.en.md)

## 作成条件と「全網羅」の範囲 / Authoring and coverage scope

主サンプル01〜60はすべてroot `version: "3.0.0"`です。理解対象として記述する標準profileは`1.0.0-draft.1`のままです。19・29・51は未来版をopaqueとして扱う例です。未知のベンダーdataや将来版の意味を規範化していません。

01〜33は既存の一意なサンプルのroot version文字列だけを変更し、34〜60は配布用に新しく記述しました。01〜33は`convert_version`の実行結果ではありません。32・33などの前後状態も独立した記述例であり、この配布作業で編集操作を実行した結果ではありません。出典と各ファイルのhashはcatalog.jsonに記録しています。

All main examples use root3.0.0. Known standard profiles retain version1.0.0-draft.1;19,29 and51 intentionally demonstrate opaque future versions. Examples01–33 change only the prior source root-version token. Examples34–60 are newly authored data. No converter, migrator, editor, validator, test suite, DAW or playback was run for this collection.

全網羅は、現行仕様が定義するパラメーター、有限の列挙選択値、主要な構造分岐をサンプルへ対応付けることを意味します。任意の文字列・数値・ベンダーキーや全パラメーターの組合せを列挙する主張ではありません。`docs/COVERAGE.json`は記述範囲の静的な索引で、実行検証の合格報告ではありません。

Coverage means mapping the currently declared parameters, finite enum alternatives and principal structural variants to examples. It does not enumerate unbounded strings, numbers, vendor keys, or every cross-product of options. Static coverage is an inventory, not a passing execution result.

## 全60サンプル / All60 main examples

| # | `.ostf` | 説明 / Purpose |
| --- | --- | --- |
| 01 | [01_four_part_sketch.ostf](01_four_part_sketch.ostf) | 4パート、和声、歌詞、相対音、生成・表示情報を含む作曲スケッチ。<br>Four parts with harmony, lyrics, relative notes, generation context and appearance. |
| 02 | [02_empty_sketch.ostf](02_empty_sketch.ostf) | まだノートや和声のない作曲途中の最小文書。<br>An unfinished document with empty musical collections. |
| 03 | [03_harmony_only.ostf](03_harmony_only.ostf) | 構造化コードとラベルだけのコード。和声から暗黙に発音しない。<br>Structured and label-only chords without implicit accompaniment. |
| 04 | [04_melody_only.ostf](04_melody_only.ostf) | 和声や拡張を必要としない4音の単旋律。<br>Four explicit melodic notes without harmony or extensions. |
| 05 | [05_lyrics_only.ostf](05_lyrics_only.ostf) | 音楽より先に作る歌詞、表示本文と分割単位の独立性。<br>Lyrics before music; display text and editorial segmentation are independent. |
| 06 | [06_percussion_slots.ostf](06_percussion_slots.ostf) | 同じ役割・MIDIヒントを持つ別スロット、未割当スロット。<br>Distinct percussion slots may share role and MIDI hint; unmapped slots are retained. |
| 07 | [07_septuplets.ostf](07_septuplets.ostf) | 7連符を丸めず記録するPPQと整数tick。<br>A PPQ that represents seven equal subdivisions exactly. |
| 08 | [08_pickups_tails.ostf](08_pickups_tails.ostf) | 負のローカル開始、配置区間外の開始、クリップを越えるゲート。<br>Pickups, starts beyond a clip span, and gates extending beyond it. |
| 09 | [09_same_pitch_overlap.ostf](09_same_pitch_overlap.ostf) | 同音・同時刻・重複クリップの独立したノートIDとゲート。<br>Independent note identities and gates through same-pitch and clip overlaps. |
| 10 | [10_enabled_states.ostf](10_enabled_states.ostf) | trackとclip双方のenabled。無効な内容も保存する。<br>Track and clip enabled states; disabled music stays in the document. |
| 11 | [11_meter_tempo_gaps.ostf](11_meter_tempo_gaps.ostf) | テンポ・拍子変更とセクション間の空白。<br>Tempo and meter changes, and gaps between sections. |
| 12 | [12_relative_chord.ostf](12_relative_chord.ostf) | コード文脈区間外でも明示参照を保つ相対音。<br>Chord-relative meaning may refer outside the context time span. |
| 13 | [13_relative_scale.ostf](13_relative_scale.ostf) | 宣言されたintervals内の位置と半音補正による相対音。<br>Scale-relative indexes and chromatic offsets. |
| 14 | [14_stale_source.ostf](14_stale_source.ostf) | 古くなった関係をstaleとして残し、Core音高を保持する。<br>Stale relative data preserves the stored Core pitch. |
| 15 | [15_unverified_source.ostf](15_unverified_source.ostf) | 未確認の関係をunverifiedとして残す。<br>Unverified relative data does not overwrite realized notes. |
| 16 | [16_generation_context.ostf](16_generation_context.ostf) | 音声・和声・テキスト等の複数入力と生成の由来。<br>Multiple audio, harmony and text inputs as generation provenance. |
| 17 | [17_appearance.ostf](17_appearance.ostf) | 明示色、カスタム役割色、定義済みの色継承。<br>Explicit object colors, custom role colors and defined inheritance. |
| 18 | [18_opaque_precision.ostf](18_opaque_precision.ostf) | 未知payloadの高精度数値と整数・実数token種別。<br>Exact opaque numbers and integer versus real token kinds. |
| 19 | [19_future_profile.ostf](19_future_profile.ostf) | 既知名前空間でも未知のprofile版はopaqueとして保存する。<br>An unknown version of a known profile remains opaque. |
| 20 | [20_lyric_alignment.ostf](20_lyric_alignment.ostf) | 歌詞本文・読み・分割と多対多のノート割り付け。<br>Display, pronunciation, segmentation and many-to-many lyric alignment. |
| 21 | [21_integer_boundary.ostf](21_integer_boundary.ostf) | 整数上限MAXちょうどで終わる発音。<br>An exact integer endpoint at MAX. |
| 22 | [22_phrase_library.ostf](22_phrase_library.ostf) | 弱起・テール・移調を含む有限反復と明示的noteMap。<br>Finite repetition, transpose, pickups, tails and explicit note mappings. |
| 23 | [23_phrase_percussion.ostf](23_phrase_percussion.ostf) | 打楽器スロットは移調しない。template-local IDの独立性。<br>Percussion slots ignore transposition; template-local IDs are independent. |
| 24 | [24_phrase_late_overlap.ostf](24_phrase_late_overlap.ostf) | 反復周期後の開始と同音ゲートの重なり。<br>Late template starts and overlapping same-pitch gates across repetitions. |
| 25 | [25_choice_shared_muted.ostf](25_choice_shared_muted.ostf) | 共有clipを持つ候補、親trackの独立したミュート、未管理clip。<br>Shared clips, independent parent mute and unmanaged music. |
| 26 | [26_choice_none.ostf](26_choice_none.ostf) | nullによる明示的な候補未選択。<br>An explicit null selection disables the managed set. |
| 27 | [27_stale_optional_profiles.ostf](27_stale_optional_profiles.ostf) | 古いphrase・未確認choice関係がCore演奏を書き換えない。<br>Stale phrase and unverified choice relationships preserve Core performance. |
| 28 | [28_empty_optional_profiles.ostf](28_empty_optional_profiles.ostf) | Core依存を持たない空のphrase・choice profile。<br>Empty phrase and choice profiles with no Core dependency. |
| 29 | [29_future_optional_profiles.ostf](29_future_optional_profiles.ostf) | phrase・choiceの未知バージョンをそのまま保持する。<br>Future phrase and choice profile versions remain opaque. |
| 30 | [30_template_before_materialization.ostf](30_template_before_materialization.ostf) | templateだけの保存ではclipや発音を生成しない。<br>A stored template does not materialize or sound on load. |
| 31 | [31_linked_phrase_before.ostf](31_linked_phrase_before.ostf) | リンク中の配置、独自Core ID、歌詞参照、無効な親track。<br>Linked placements with custom Core IDs, lyric references and a muted parent. |
| 32 | [32_replaced_phrase_after.ostf](32_replaced_phrase_after.ostf) | 原型置換後を独立に記述した例。存続IDと新規発生を分ける。<br>An independently authored replacement state preserving surviving occurrence IDs. |
| 33 | [33_detached_manual_after.ostf](33_detached_manual_after.ostf) | 手編集済み配置のリンクだけを解除した記述例。<br>An authored detached state retaining manually edited Core notes and lyrics. |
| 34 | [34_all_core_fields.ostf](34_all_core_fields.ostf) | 全Coreパラメーターを一つに集めた例。<br>Every named Core parameter appears in one document. |
| 35 | [35_pitch_class_spellings.ostf](35_pitch_class_spellings.ostf) | 音名A〜Gと変化量−2〜2の35通り。<br>All seven pitch-class steps and all five alterations, in 35 spellings. |
| 36 | [36_all_meter_denominators.ostf](36_all_meter_denominators.ostf) | 拍子分母1・2・4・8・16・32・64の全選択値。<br>Every supported meter denominator. |
| 37 | [37_resource_kinds.ostf](37_resource_kinds.ostf) | audio・midi・text・otherの全素材種別。<br>All four resource kinds, with an optional SHA-256 annotation. |
| 38 | [38_dependency_scopes.ostf](38_dependency_scopes.ostf) | 依存scopeの3形式と12種の型付き参照。<br>All three dependency scopes and every typed reference kind. |
| 39 | [39_relative_objects.ostf](39_relative_objects.ostf) | 両basisと直接参照すべてを列挙したobjects依存。<br>Both relative bases with complete object dependency declarations. |
| 40 | [40_relative_interval_limits.ostf](40_relative_interval_limits.ostf) | intervals件数、index上限、半音補正±24の例。<br>Declared interval-count limits, index limits and ±24 chromatic offsets. |
| 41 | [41_generation_all_ref_types.ostf](41_generation_all_ref_types.ostf) | 生成の入力・出力に使える12種の型付き参照。<br>All twelve typed references in generation inputs and outputs. |
| 42 | [42_generation_protected_range.ostf](42_generation_protected_range.ostf) | 読み取り範囲、生成要求範囲、保護ノート、vendor設定の関係。<br>Read range, target range, protected notes and engine-specific settings. |
| 43 | [43_appearance_all_targets.ostf](43_appearance_all_targets.ostf) | 表示profileの全フィールドと12種の対象色。<br>All appearance fields and all twelve object-color target kinds. |
| 44 | [44_appearance_inheritance.ostf](44_appearance_inheritance.ostf) | セクション色の5段階とtrack→clip→noteの継承。<br>The five section-color fallback levels and track/clip/note inheritance. |
| 45 | [45_legacy_import_archive.ostf](45_legacy_import_archive.ostf) | 2.3原文、SHA-256、移行報告を持つ原典アーカイブ。<br>Legacy source text, its UTF-8 SHA-256 and an explicit conversion-report object. |
| 46 | [46_lyrics_multilingual.ostf](46_lyrics_multilingual.ostf) | 複数言語の歌詞文書を同じノートへ独立に関連付ける。<br>Independent lyric documents in two languages aligned to the same notes. |
| 47 | [47_pitch_boundaries.ostf](47_pitch_boundaries.ostf) | pitchとmidiNoteヒントの0・127境界。<br>The pitch and optional MIDI-hint endpoints0 and127. |
| 48 | [48_ppq_minimum.ostf](48_ppq_minimum.ostf) | PPQ最小値1、1tickゲート、テンポ上限1000。<br>Minimum PPQ1, one-tick gates and maximum BPM1000. |
| 49 | [49_ppq_maximum.ostf](49_ppq_maximum.ostf) | PPQ上限960000、拍子分子64、正の小数テンポ。<br>Maximum PPQ960000, numerator64 and a positive fractional tempo. |
| 50 | [50_optional_empty_strings.ostf](50_optional_empty_strings.ostf) | 空文字を許すフィールドと、空の標準任意profile。<br>Allowed empty strings and empty standard optional profiles. |
| 51 | [51_opaque_json_values.ostf](51_opaque_json_values.ostf) | 未知dataに許されるJSON値の全種別と高精度token。<br>Every JSON value kind in opaque data, including precise numeric tokens. |
| 52 | [52_stale_missing_references.ostf](52_stale_missing_references.ostf) | 既知profileの欠落した過去の参照をstale／unverifiedで保持する。<br>Missing historical profile references retained as stale or unverified. |
| 53 | [53_phrase_empty_template.ostf](53_phrase_empty_template.ostf) | 空templateをMAX回反復してもノートは0件。<br>An empty template with MAX repetitions still has zero occurrences. |
| 54 | [54_phrase_objects_dependencies.ostf](54_phrase_objects_dependencies.ostf) | phraseのsoundSlot・clip・mapped noteをobjects依存へ列挙する。<br>Every directly referenced sound slot, clip and mapped note in phrase dependencies. |
| 55 | [55_choice_empty_candidate.ostf](55_choice_empty_candidate.ostf) | 空clipIdsの名前付き候補を選ぶ。nullとは異なる編集上の意図。<br>Selecting a named empty candidate preserves an editorial intention distinct from null. |
| 56 | [56_choice_disjoint_groups.ostf](56_choice_disjoint_groups.ostf) | 管理clipが重ならない2つの候補group。candidate IDはgroup内ローカル。<br>Two groups own disjoint clip sets; candidate IDs are local to each group. |
| 57 | [57_choice_objects_dependencies.ostf](57_choice_objects_dependencies.ostf) | 未選択を含むすべての候補clipを依存宣言する。<br>Choice dependencies include selected and unselected candidate clips. |
| 58 | [58_complete_workflow.ostf](58_complete_workflow.ostf) | 全6標準profileが一つのCore文書で共存する例。<br>All six standard profiles coexist with one explicit Core performance. |
| 59 | [59_phrase_transpose_limits.ostf](59_phrase_transpose_limits.ostf) | 移調量±127と、結果pitchが0〜127に収まる組。<br>Both transpose endpoints with resulting pitches inside0–127. |
| 60 | [60_song_form_arrangement.ostf](60_song_form_arrangement.ostf) | イントロ・ヴァース・コーラス・アウトロを持つ6小節のCore編曲。<br>A six-bar four-part Core arrangement with intro, verse, chorus and outro. |

## 読み方の補足 / Reading notes

### 関係が古い例・未知の例 / Stale and unknown relationships

14・15・27・33・52はstaleまたはunverifiedの関係を明示して保存する例です。18・19・29・38・51はopaqueなデータの保持を説明します。これは関係の警告があり得ることを意図したもので、既知profileの構造不正やCore自体の参照不正を許可するものではありません。45・58のlegacy archiveは仕様に従いunverifiedです。

Examples14,15,27,33 and52 intentionally retain outdated or unverified relationships.18,19,29,38 and51 illustrate opaque preservation. Relationship warnings are intentional; invalid known structures and invalid Core references remain errors. Legacy archives in45 and58 are unverified as required by the specification.

### 数値・時間の例 / Numbers and time

18と51の高精度数値は、一般的なJSON処理系で丸めて保存すると意味が変わる可能性があります。整数tokenと実数tokenの種別も保持します。21・40・47〜49・53・59は境界や型を説明する例で、通常の作曲に推奨する値の組合せではありません。クリップ末尾やセクション末尾は音のゲートを切りません。

Preserve exact numeric values and integer/real token kinds in18 and51. The large or extreme values in21,40,47–49,53 and59 illustrate limits, not normal composing recommendations. Placement spans do not truncate note gates.

### 保護と編集 / Protection and editing

42は保護IDと生成範囲、31〜33は原型置換・リンク解除の前後関係を示します。保護を守ったという判定には操作前後の二つの文書を使う定義済み比較が必要です。生成工程を保存しただけで実行や履歴を証明したことにはなりません。[操作ガイド](../docs/OPERATIONS.md)を参照してください。

Example42 describes protection and ranges;31–33 describe replacement and detachment states. Actual protection claims require the defined comparison of before and after documents. A stored process description is not proof of execution or history.

### 素材・発音 / Resources and sound

resource URIはすべて参照情報で、読み込みだけで外部取得・コード実行・音声再生を指示しません。soundSlotのmidiNoteは出力先のヒントで、GM対応や音色の一致を保証しません。サンプルにはCore velocityを追加していません。

Resource URIs are inert references. A sound-slot MIDI hint neither declares GM conformance nor guarantees timbre. These examples add no Core velocity parameter.

## OSTF2.3移行入力 / Legacy migration inputs

| File | Use | Upstream SHA-256 |
| --- | --- | --- |
| [legacy_2_3/54_full_feature.ostf](legacy_2_3/54_full_feature.ostf) | 2.3原文の移行入力 / Verbatim2.3 input | `cf8a24d487c7f09b390f946839cb08d08be7d566428dda12ec556326240bca64` |
| [legacy_2_3/29_lyrics_alignment.ostf](legacy_2_3/29_lyrics_alignment.ostf) | 2.3原文の移行入力 / Verbatim2.3 input | `34887f5b5910a19a24ec61af202fb10d5ecba9f6c57a784b148144bb3039b188` |

この2件だけはroot `version: "2.3.0"`です。3.0読者の入力例とは分けて扱ってください。出典は[yoh-nak/Open-Song-Timeline-Format-2.3](https://github.com/yoh-nak/Open-Song-Timeline-Format-2.3)、固定commit `90fce246de28a1b265fb6b25cc2866c70036fda6`です。[出典情報](../docs/SOURCE_ATTRIBUTION.md)と[移行ガイド](../docs/MIGRATION_2_3_TO_3_0.md)を参照してください。

Only these two files use root2.3.0. They are migration inputs, not3.0 reader examples. Their exact source bytes and provenance are preserved. A version-token edit alone is not a2.3-to3.0 migration.

## 個別の補足 / Per-example details

### 34 — 34_all_core_fields.ostf

bass単独のlabel-onlyコードも含む。resourceは実行・取得指示ではない。

Includes a label-only chord with an independent bass spelling. Resources are inert references.

### 35 — 35_pitch_class_spellings.ostf

異名同音でも綴りを保持する。35コードを自動伴奏として鳴らす指定ではない。

Enharmonically equal pitch classes retain their spelling; these chord declarations do not sound automatically.

### 36 — 36_all_meter_denominators.ostf

変更位置は保存値そのもの。小節境界への移動やPPQの再定義はしない。

Change positions are literal; they do not redefine PPQ or imply snapping to bar boundaries.

### 37 — 37_resource_kinds.ostf

textのhashはUTF-8の「OSTF example」とLFのバイト列を指す例示。素材ファイルは同梱しない。

The text digest describes UTF-8 bytes of "OSTF example" followed by LF. No external media is bundled or fetched.

### 38 — 38_dependency_scopes.ostf

独自名前空間のdataはopaque。currentは作成者の整合性宣言で、実行・検証の証明ではない。

Vendor data is opaque. Current is the author declaration, not proof that a generator ran or was verified.

### 40 — 40_relative_interval_limits.ostf

音高は順に0+35+24=59、24+11−24=11、24+0−24=0。境界値を説明する記述例。

The authored pitches are 59, 11 and 0 from the stated formulas; this is a boundary illustration, not a test result.

### 41 — 41_generation_all_ref_types.ostf

一般的な編集・生成文脈の記述例。工程が実行されたという記録ではない。

An authored process description, not a claim that these editing or generation steps were executed.

### 42 — 42_generation_protected_range.ostf

保護は操作前後の比較が必要。seedやcomplexityに全エンジン共通の意味は与えない。

Protection requires before/after comparison. Seed and complexity are engine-specific, with no universal behavior.

### 43 — 43_appearance_all_targets.ostf

大文字・小文字を混ぜた#RRGGBBも表す。役割名は閉じたenumではなく文字列。

Mixed-case #RRGGBB is included. Role names are open strings, not a closed enumeration.

### 44 — 44_appearance_inheritance.ostf

section-0〜4は順に明示色、custom色、baseRole色、Core role色、ホスト既定色。note-inheritはclip色を継承。

Sections0–4 illustrate explicit, custom, base-role, Core-role and host-default colors; note-inherit uses its clip color.

### 45 — 45_legacy_import_archive.ostf

同梱legacy_2_3/54_full_feature.ostfの原文を格納。移行器を実行した出力ではなく、Coreへの意味変換は主張しない。

Embeds the exact bundled legacy54 source. This is not migrator output and does not claim a musical conversion.

### 46 — 46_lyrics_multilingual.ostf

言語タグから自動翻訳や歌声合成を要求しない。割り付け順序は配列のまま保持する。

Language strings do not request translation or vocal synthesis. Alignment order is preserved.

### 47 — 47_pitch_boundaries.ostf

0と127が音楽的に常用されるとは主張しない。音源割当はホスト側で行う。

Endpoints are illustrative, not typical orchestration advice. Sound assignment belongs to the host.

### 49 — 49_ppq_maximum.ostf

bpmには0より大きい値が必要で、最小の正の実数は規定しない。これは境界と型の記述例。

BPM must be positive; the format does not define a least positive real value. This illustrates types and boundaries.

### 50 — 50_optional_empty_strings.ostf

section.name、chord.label、resource.uriなどは空にしない。legacy以外の5profileには空のレコード配列・対応表とscope:noneを示す。

Nonempty-string fields remain nonempty. The five non-legacy profiles illustrate empty record collections and mappings with scope:none.

### 51 — 51_opaque_json_values.ostf

巨大整数、高精度小数、負の実数ゼロ、微小な実数を保持する。generation・appearance・legacyの未知版2.0.0もopaqueとして表す。

Preserves a large integer, exact decimal, negative real zero and tiny real. Unknown version2.0.0 of generation, appearance and legacy profiles is opaque.

### 52 — 52_stale_missing_references.ostf

参照不一致の警告を意図した例。Coreの4音は有効な参照を保つ。statusによって既知の構造不正やCore参照不正を許す例ではない。

Designed to illustrate relationship warnings. The four Core notes retain valid references; status does not excuse invalid known structure or Core references.

### 53 — 53_phrase_empty_template.ostf

長さは1×MAX=MAX。反復の直積を列挙する必要はなく、配置末尾を演奏終端と見なさない。

The placement span is1×MAX. No Cartesian expansion is needed, and the placement end is not a performance end.

### 54 — 54_phrase_objects_dependencies.ostf

template IDやtemplate-local note ID自体はCore依存参照へ追加しない。

Template IDs and template-local note IDs are not Core dependency references.

### 55 — 55_choice_empty_candidate.ostf

管理下のclipはすべてfalse。親trackミュートと未管理clipはそのまま。

All managed clips are disabled. Parent mute and unmanaged content remain unchanged.

### 56 — 56_choice_disjoint_groups.ostf

両groupにaとbというIDを使える。同じCore clipを異なるgroupに所属させない。

Both groups may use IDs a and b; a Core clip must not be managed by different groups.

### 57 — 57_choice_objects_dependencies.ostf

選択中のclipだけでは依存が不足する。未管理clipはこのprofileの直接依存に含めない。

Declaring only selected clips is insufficient. The unmanaged clip is not a direct dependency of this profile.

### 58 — 58_complete_workflow.ostf

相対・phrase・choiceのcurrent宣言は同じCoreを参照する。legacyはunverifiedの原典保管で、Coreは新規の記述。

Current relative, phrase and choice declarations describe the same Core. The legacy archive is unverified; Core music is independently authored.

### 59 — 59_phrase_transpose_limits.ostf

0+127=127、127−127=0。source note IDは異なるtemplateで同じlocalを使える。

0+127=127 and127−127=0. Different templates may reuse the local source-note ID.

### 60 — 60_song_form_arrangement.ostf

最終ゲートはセクション・clipの末尾を越える。すべてのパートはCoreノートとして明示し、拡張は使わない。

The final gate extends beyond the section and clip spans. Every part is explicitly stored in Core; no extensions are needed.

