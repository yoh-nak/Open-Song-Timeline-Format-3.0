# 全項目・選択値・構造の収録対応表 / Complete coverage map

**OSTF 3.0.0の60件の主サンプルについて、168/168の宣言パラメーターと37/37のenum値の出現を対応付けました。** 14件の条件付き再制約、13件のconst、51の名前付き定義についても、該当する記述位置を示します。これは文書作成時の静的な所在確認であり、動作検証・Schema検証・意味検証の合格報告ではありません。

The 60 main examples contain every one of the **168 declared parameter entries** and **37 enum-value occurrences**, plus witnesses for the 14 conditional overlays, 13 constants and 51 named definitions. This is a static documentation inventory, not validation or execution evidence.

## 1. 数え方と方法 / Counting and method

- 一つの型定義を使う多数の場所は、宣言の数として重複計上しません。枝ごとに宣言された同名フィールドは別の宣言です。`if` / `then` 内で既存フィールドを再制約する14件は、168件と分けて示します。
- enumは7集合に37個の値が現れます。`const`の13箇所はenumと別に集計します。任意の数値・文字列・ベンダーキーの全値、または全条件の直積を列挙する意味ではありません。
- 3.0.0 Schemaのローカル`$ref`、配列要素、プロパティと明示された分岐タグを辿り、実在するサンプルのJSON Pointerを記録しました。既知profileのpayloadはnamespaceと正確なversionが一致する場合だけ、その型の例に数えます。未来版の不透明なdataを、既知版の網羅実績へ混ぜていません。
- 型とフィールドの存在を辿る処理は、数値範囲・参照先・加算・配列順・依存範囲・操作結果を検証しません。プロジェクトコード、validator、CLI、試験、DAW/MIDIは実行していません。
- `.ostf`の正例で禁止ケースのすべてを表すことはできません。禁止・拒否条件は[リファレンス](PARAMETER_REFERENCE.ja.md)、[仕様](FORMAT_SPECIFICATION.ja.md)、[適合条件](CONFORMANCE.md)に記述します。関係が古い例や未知版の例も、構造不正の配布例とは区別します。
- 2件の2.3原典は主サンプルの集計対象外です。[COVERAGE.json](COVERAGE.json)には全寄与ファイル、出現数、各行最大6件の具体的な位置、入力Schemaとサンプルのhashを収録しています。

Each declaration is counted once at its schema definition; repeated usage sites are not new parameters. Branch-specific declarations count separately. Conditional overlays are separate from declarations. Open-ended data domains and cross-products are representative only. Exact version gates prevent future payloads from contributing to known-profile coverage. The machine inventory records presence witnesses, with up to six concrete locations per row and all contributing sample paths.

## 2. 収録数 / Totals

| 対象 / Category | 定義数 / Defined | 位置を記録 / Located |
| --- | ---: | ---: |
| 宣言パラメーター / Declared properties | 168 | 168 |
| 条件付き再制約 / Conditional property overlays | 14 | 14 |
| enumの値の出現 / Enum-value occurrences | 37 | 37 |
| constの出現箇所 / Constant occurrences | 13 | 13 |
| 名前付き定義 / Named definitions | 51 | 51 |
| 分岐規則の出現箇所 / Branch-rule locations | 27 | 27 |

The 27 branch rules are schema rule locations, not a count of all possible logical outcomes. Section7 lists the observed structural forms separately, including both outcomes of all six exact-profile-version gates.

## 3. 全168宣言パラメーター / Every declared parameter

A location such as `/tracks/0/clips/0/notes/0/start` is a JSON Pointer within the linked `.ostf` file. It identifies a field's presence, not a line number or a semantic test result.



### ref

| Parameter / Schema pointer | Example | JSON Pointer |
| --- | --- | --- |
| `type`<br>`#/$defs/ref/properties/type` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/extensions/com.example.generator-state.v1/dependencies/refs/0/type` |
| `id`<br>`#/$defs/ref/properties/id` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/extensions/com.example.generator-state.v1/dependencies/refs/0/id` |

### range

| Parameter / Schema pointer | Example | JSON Pointer |
| --- | --- | --- |
| `start`<br>`#/$defs/range/properties/start` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/extensions/org.ostf.generation-context.v1/data/processes/0/targetRange/start` |
| `duration`<br>`#/$defs/range/properties/duration` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/extensions/org.ostf.generation-context.v1/data/processes/0/targetRange/duration` |

### spelledPitchClass

| Parameter / Schema pointer | Example | JSON Pointer |
| --- | --- | --- |
| `step`<br>`#/$defs/spelledPitchClass/properties/step` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/harmony/chords/0/root/step` |
| `alter`<br>`#/$defs/spelledPitchClass/properties/alter` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/harmony/chords/0/root/alter` |

### song

| Parameter / Schema pointer | Example | JSON Pointer |
| --- | --- | --- |
| `title`<br>`#/$defs/song/properties/title` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/song/title` |
| `primaryMelodyTrackId`<br>`#/$defs/song/properties/primaryMelodyTrackId` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/song/primaryMelodyTrackId` |

### section

| Parameter / Schema pointer | Example | JSON Pointer |
| --- | --- | --- |
| `id`<br>`#/$defs/section/properties/id` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/timeline/sections/0/id` |
| `name`<br>`#/$defs/section/properties/name` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/timeline/sections/0/name` |
| `start`<br>`#/$defs/section/properties/start` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/timeline/sections/0/start` |
| `duration`<br>`#/$defs/section/properties/duration` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/timeline/sections/0/duration` |
| `role`<br>`#/$defs/section/properties/role` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/timeline/sections/0/role` |

### tempo

| Parameter / Schema pointer | Example | JSON Pointer |
| --- | --- | --- |
| `at`<br>`#/$defs/tempo/properties/at` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/timeline/tempoChanges/0/at` |
| `bpm`<br>`#/$defs/tempo/properties/bpm` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/timeline/tempoChanges/0/bpm` |

### meter

| Parameter / Schema pointer | Example | JSON Pointer |
| --- | --- | --- |
| `at`<br>`#/$defs/meter/properties/at` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/timeline/meterChanges/0/at` |
| `numerator`<br>`#/$defs/meter/properties/numerator` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/timeline/meterChanges/0/numerator` |
| `denominator`<br>`#/$defs/meter/properties/denominator` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/timeline/meterChanges/0/denominator` |

### timeline

| Parameter / Schema pointer | Example | JSON Pointer |
| --- | --- | --- |
| `sections`<br>`#/$defs/timeline/properties/sections` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/timeline/sections` |
| `tempoChanges`<br>`#/$defs/timeline/properties/tempoChanges` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/timeline/tempoChanges` |
| `meterChanges`<br>`#/$defs/timeline/properties/meterChanges` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/timeline/meterChanges` |

### chord

| Parameter / Schema pointer | Example | JSON Pointer |
| --- | --- | --- |
| `id`<br>`#/$defs/chord/properties/id` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/harmony/chords/0/id` |
| `start`<br>`#/$defs/chord/properties/start` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/harmony/chords/0/start` |
| `duration`<br>`#/$defs/chord/properties/duration` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/harmony/chords/0/duration` |
| `label`<br>`#/$defs/chord/properties/label` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/harmony/chords/0/label` |
| `root`<br>`#/$defs/chord/properties/root` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/harmony/chords/0/root` |
| `intervals`<br>`#/$defs/chord/properties/intervals` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/harmony/chords/0/intervals` |
| `bass`<br>`#/$defs/chord/properties/bass` | [34_all_core_fields.ostf](../samples/34_all_core_fields.ostf) | `/harmony/chords/0/bass` |

### scale

| Parameter / Schema pointer | Example | JSON Pointer |
| --- | --- | --- |
| `id`<br>`#/$defs/scale/properties/id` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/harmony/scales/0/id` |
| `start`<br>`#/$defs/scale/properties/start` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/harmony/scales/0/start` |
| `duration`<br>`#/$defs/scale/properties/duration` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/harmony/scales/0/duration` |
| `label`<br>`#/$defs/scale/properties/label` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/harmony/scales/0/label` |
| `tonic`<br>`#/$defs/scale/properties/tonic` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/harmony/scales/0/tonic` |
| `intervals`<br>`#/$defs/scale/properties/intervals` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/harmony/scales/0/intervals` |

### harmony

| Parameter / Schema pointer | Example | JSON Pointer |
| --- | --- | --- |
| `chords`<br>`#/$defs/harmony/properties/chords` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/harmony/chords` |
| `scales`<br>`#/$defs/harmony/properties/scales` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/harmony/scales` |

### instrument

| Parameter / Schema pointer | Example | JSON Pointer |
| --- | --- | --- |
| `name`<br>`#/$defs/instrument/properties/name` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/tracks/0/instrument/name` |
| `family`<br>`#/$defs/instrument/properties/family` | [34_all_core_fields.ostf](../samples/34_all_core_fields.ostf) | `/tracks/0/instrument/family` |

### note

| Parameter / Schema pointer | Example | JSON Pointer |
| --- | --- | --- |
| `id`<br>`#/$defs/note/properties/id` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/tracks/0/clips/0/notes/0/id` |
| `start`<br>`#/$defs/note/properties/start` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/tracks/0/clips/0/notes/0/start` |
| `duration`<br>`#/$defs/note/properties/duration` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/tracks/0/clips/0/notes/0/duration` |
| `pitch`<br>`#/$defs/note/properties/pitch` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/tracks/0/clips/0/notes/0/pitch` |
| `soundSlotId`<br>`#/$defs/note/properties/soundSlotId` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/tracks/3/clips/0/notes/0/soundSlotId` |

### clip

| Parameter / Schema pointer | Example | JSON Pointer |
| --- | --- | --- |
| `id`<br>`#/$defs/clip/properties/id` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/tracks/0/clips/0/id` |
| `name`<br>`#/$defs/clip/properties/name` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/tracks/0/clips/0/name` |
| `start`<br>`#/$defs/clip/properties/start` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/tracks/0/clips/0/start` |
| `duration`<br>`#/$defs/clip/properties/duration` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/tracks/0/clips/0/duration` |
| `enabled`<br>`#/$defs/clip/properties/enabled` | [10_enabled_states.ostf](../samples/10_enabled_states.ostf) | `/tracks/0/clips/1/enabled` |
| `notes`<br>`#/$defs/clip/properties/notes` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/tracks/0/clips/0/notes` |

### track

| Parameter / Schema pointer | Example | JSON Pointer |
| --- | --- | --- |
| `id`<br>`#/$defs/track/properties/id` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/tracks/0/id` |
| `name`<br>`#/$defs/track/properties/name` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/tracks/0/name` |
| `role`<br>`#/$defs/track/properties/role` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/tracks/0/role` |
| `instrument`<br>`#/$defs/track/properties/instrument` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/tracks/0/instrument` |
| `enabled`<br>`#/$defs/track/properties/enabled` | [10_enabled_states.ostf](../samples/10_enabled_states.ostf) | `/tracks/1/enabled` |
| `clips`<br>`#/$defs/track/properties/clips` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/tracks/0/clips` |

### soundSlot

| Parameter / Schema pointer | Example | JSON Pointer |
| --- | --- | --- |
| `id`<br>`#/$defs/soundSlot/properties/id` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/soundSlots/0/id` |
| `name`<br>`#/$defs/soundSlot/properties/name` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/soundSlots/0/name` |
| `role`<br>`#/$defs/soundSlot/properties/role` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/soundSlots/0/role` |
| `midiNote`<br>`#/$defs/soundSlot/properties/midiNote` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/soundSlots/0/midiNote` |

### lyricDocument

| Parameter / Schema pointer | Example | JSON Pointer |
| --- | --- | --- |
| `id`<br>`#/$defs/lyricDocument/properties/id` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/lyrics/documents/0/id` |
| `title`<br>`#/$defs/lyricDocument/properties/title` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/lyrics/documents/0/title` |
| `language`<br>`#/$defs/lyricDocument/properties/language` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/lyrics/documents/0/language` |

### lyricPhrase

| Parameter / Schema pointer | Example | JSON Pointer |
| --- | --- | --- |
| `id`<br>`#/$defs/lyricPhrase/properties/id` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/lyrics/phrases/0/id` |
| `documentId`<br>`#/$defs/lyricPhrase/properties/documentId` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/lyrics/phrases/0/documentId` |
| `text`<br>`#/$defs/lyricPhrase/properties/text` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/lyrics/phrases/0/text` |
| `pronunciation`<br>`#/$defs/lyricPhrase/properties/pronunciation` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/lyrics/phrases/0/pronunciation` |
| `start`<br>`#/$defs/lyricPhrase/properties/start` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/lyrics/phrases/0/start` |
| `duration`<br>`#/$defs/lyricPhrase/properties/duration` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/lyrics/phrases/0/duration` |

### lyricUnit

| Parameter / Schema pointer | Example | JSON Pointer |
| --- | --- | --- |
| `id`<br>`#/$defs/lyricUnit/properties/id` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/lyrics/units/0/id` |
| `phraseId`<br>`#/$defs/lyricUnit/properties/phraseId` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/lyrics/units/0/phraseId` |
| `text`<br>`#/$defs/lyricUnit/properties/text` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/lyrics/units/0/text` |
| `pronunciation`<br>`#/$defs/lyricUnit/properties/pronunciation` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/lyrics/units/0/pronunciation` |
| `start`<br>`#/$defs/lyricUnit/properties/start` | [34_all_core_fields.ostf](../samples/34_all_core_fields.ostf) | `/lyrics/units/0/start` |
| `duration`<br>`#/$defs/lyricUnit/properties/duration` | [34_all_core_fields.ostf](../samples/34_all_core_fields.ostf) | `/lyrics/units/0/duration` |

### lyricAlignment

| Parameter / Schema pointer | Example | JSON Pointer |
| --- | --- | --- |
| `id`<br>`#/$defs/lyricAlignment/properties/id` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/lyrics/alignments/0/id` |
| `unitIds`<br>`#/$defs/lyricAlignment/properties/unitIds` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/lyrics/alignments/0/unitIds` |
| `noteIds`<br>`#/$defs/lyricAlignment/properties/noteIds` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/lyrics/alignments/0/noteIds` |

### lyrics

| Parameter / Schema pointer | Example | JSON Pointer |
| --- | --- | --- |
| `documents`<br>`#/$defs/lyrics/properties/documents` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/lyrics/documents` |
| `phrases`<br>`#/$defs/lyrics/properties/phrases` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/lyrics/phrases` |
| `units`<br>`#/$defs/lyrics/properties/units` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/lyrics/units` |
| `alignments`<br>`#/$defs/lyrics/properties/alignments` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/lyrics/alignments` |

### resource

| Parameter / Schema pointer | Example | JSON Pointer |
| --- | --- | --- |
| `id`<br>`#/$defs/resource/properties/id` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/resources/0/id` |
| `kind`<br>`#/$defs/resource/properties/kind` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/resources/0/kind` |
| `uri`<br>`#/$defs/resource/properties/uri` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/resources/0/uri` |
| `name`<br>`#/$defs/resource/properties/name` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/resources/0/name` |
| `sha256`<br>`#/$defs/resource/properties/sha256` | [16_generation_context.ostf](../samples/16_generation_context.ostf) | `/resources/0/sha256` |

### dependencies

| Parameter / Schema pointer | Example | JSON Pointer |
| --- | --- | --- |
| `scope`<br>`#/$defs/dependencies/oneOf/0/properties/scope` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/extensions/org.ostf.appearance.v1/dependencies/scope` |
| `scope`<br>`#/$defs/dependencies/oneOf/1/properties/scope` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/extensions/com.example.generator-state.v1/dependencies/scope` |
| `refs`<br>`#/$defs/dependencies/oneOf/1/properties/refs` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/extensions/com.example.generator-state.v1/dependencies/refs` |

### extension

| Parameter / Schema pointer | Example | JSON Pointer |
| --- | --- | --- |
| `version`<br>`#/$defs/extension/properties/version` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/extensions/com.example.generator-state.v1/version` |
| `status`<br>`#/$defs/extension/properties/status` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/extensions/com.example.generator-state.v1/status` |
| `dependencies`<br>`#/$defs/extension/properties/dependencies` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/extensions/com.example.generator-state.v1/dependencies` |
| `data`<br>`#/$defs/extension/properties/data` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/extensions/com.example.generator-state.v1/data` |

### relativeAssignment

| Parameter / Schema pointer | Example | JSON Pointer |
| --- | --- | --- |
| `noteId`<br>`#/$defs/relativeAssignment/properties/noteId` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/extensions/org.ostf.relative-phrase.v1/data/assignments/0/noteId` |
| `basis`<br>`#/$defs/relativeAssignment/properties/basis` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/extensions/org.ostf.relative-phrase.v1/data/assignments/0/basis` |
| `contextId`<br>`#/$defs/relativeAssignment/properties/contextId` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/extensions/org.ostf.relative-phrase.v1/data/assignments/0/contextId` |
| `anchorPitch`<br>`#/$defs/relativeAssignment/properties/anchorPitch` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/extensions/org.ostf.relative-phrase.v1/data/assignments/0/anchorPitch` |
| `index`<br>`#/$defs/relativeAssignment/properties/index` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/extensions/org.ostf.relative-phrase.v1/data/assignments/0/index` |
| `chromaticOffset`<br>`#/$defs/relativeAssignment/properties/chromaticOffset` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/extensions/org.ostf.relative-phrase.v1/data/assignments/0/chromaticOffset` |

### relativeData

| Parameter / Schema pointer | Example | JSON Pointer |
| --- | --- | --- |
| `assignments`<br>`#/$defs/relativeData/properties/assignments` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/extensions/org.ostf.relative-phrase.v1/data/assignments` |

### generator

| Parameter / Schema pointer | Example | JSON Pointer |
| --- | --- | --- |
| `id`<br>`#/$defs/generator/properties/id` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/extensions/org.ostf.generation-context.v1/data/processes/0/generator/id` |
| `version`<br>`#/$defs/generator/properties/version` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/extensions/org.ostf.generation-context.v1/data/processes/0/generator/version` |

### generationInput

| Parameter / Schema pointer | Example | JSON Pointer |
| --- | --- | --- |
| `role`<br>`#/$defs/generationInput/properties/role` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/extensions/org.ostf.generation-context.v1/data/processes/0/inputs/0/role` |
| `ref`<br>`#/$defs/generationInput/properties/ref` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/extensions/org.ostf.generation-context.v1/data/processes/0/inputs/0/ref` |
| `readRange`<br>`#/$defs/generationInput/properties/readRange` | [16_generation_context.ostf](../samples/16_generation_context.ostf) | `/extensions/org.ostf.generation-context.v1/data/processes/0/inputs/1/readRange` |

### generationProcess

| Parameter / Schema pointer | Example | JSON Pointer |
| --- | --- | --- |
| `id`<br>`#/$defs/generationProcess/properties/id` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/extensions/org.ostf.generation-context.v1/data/processes/0/id` |
| `generator`<br>`#/$defs/generationProcess/properties/generator` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/extensions/org.ostf.generation-context.v1/data/processes/0/generator` |
| `inputs`<br>`#/$defs/generationProcess/properties/inputs` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/extensions/org.ostf.generation-context.v1/data/processes/0/inputs` |
| `outputs`<br>`#/$defs/generationProcess/properties/outputs` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/extensions/org.ostf.generation-context.v1/data/processes/0/outputs` |
| `targetRange`<br>`#/$defs/generationProcess/properties/targetRange` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/extensions/org.ostf.generation-context.v1/data/processes/0/targetRange` |
| `protectedNoteIds`<br>`#/$defs/generationProcess/properties/protectedNoteIds` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/extensions/org.ostf.generation-context.v1/data/processes/0/protectedNoteIds` |
| `vendorExtension`<br>`#/$defs/generationProcess/properties/vendorExtension` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/extensions/org.ostf.generation-context.v1/data/processes/0/vendorExtension` |

### generationData

| Parameter / Schema pointer | Example | JSON Pointer |
| --- | --- | --- |
| `processes`<br>`#/$defs/generationData/properties/processes` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/extensions/org.ostf.generation-context.v1/data/processes` |

### roleDefinition

| Parameter / Schema pointer | Example | JSON Pointer |
| --- | --- | --- |
| `id`<br>`#/$defs/roleDefinition/properties/id` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/extensions/org.ostf.appearance.v1/data/roleDefinitions/0/id` |
| `name`<br>`#/$defs/roleDefinition/properties/name` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/extensions/org.ostf.appearance.v1/data/roleDefinitions/0/name` |
| `baseRole`<br>`#/$defs/roleDefinition/properties/baseRole` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/extensions/org.ostf.appearance.v1/data/roleDefinitions/0/baseRole` |

### objectColor

| Parameter / Schema pointer | Example | JSON Pointer |
| --- | --- | --- |
| `target`<br>`#/$defs/objectColor/properties/target` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/extensions/org.ostf.appearance.v1/data/appearance/objectColors/0/target` |
| `color`<br>`#/$defs/objectColor/properties/color` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/extensions/org.ostf.appearance.v1/data/appearance/objectColors/0/color` |

### appearanceData

| Parameter / Schema pointer | Example | JSON Pointer |
| --- | --- | --- |
| `roleDefinitions`<br>`#/$defs/appearanceData/properties/roleDefinitions` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/extensions/org.ostf.appearance.v1/data/roleDefinitions` |
| `sectionRoleAssignments`<br>`#/$defs/appearanceData/properties/sectionRoleAssignments` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/extensions/org.ostf.appearance.v1/data/sectionRoleAssignments` |
| `appearance`<br>`#/$defs/appearanceData/properties/appearance` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/extensions/org.ostf.appearance.v1/data/appearance` |
| `roleColors`<br>`#/$defs/appearanceData/properties/appearance/properties/roleColors` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/extensions/org.ostf.appearance.v1/data/appearance/roleColors` |
| `customRoleColors`<br>`#/$defs/appearanceData/properties/appearance/properties/customRoleColors` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/extensions/org.ostf.appearance.v1/data/appearance/customRoleColors` |
| `objectColors`<br>`#/$defs/appearanceData/properties/appearance/properties/objectColors` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/extensions/org.ostf.appearance.v1/data/appearance/objectColors` |

### legacyData

| Parameter / Schema pointer | Example | JSON Pointer |
| --- | --- | --- |
| `sourceVersion`<br>`#/$defs/legacyData/properties/sourceVersion` | [45_legacy_import_archive.ostf](../samples/45_legacy_import_archive.ostf) | `/extensions/org.ostf.legacy-import.v1/data/sourceVersion` |
| `sourceSha256`<br>`#/$defs/legacyData/properties/sourceSha256` | [45_legacy_import_archive.ostf](../samples/45_legacy_import_archive.ostf) | `/extensions/org.ostf.legacy-import.v1/data/sourceSha256` |
| `sourceText`<br>`#/$defs/legacyData/properties/sourceText` | [45_legacy_import_archive.ostf](../samples/45_legacy_import_archive.ostf) | `/extensions/org.ostf.legacy-import.v1/data/sourceText` |
| `conversionReport`<br>`#/$defs/legacyData/properties/conversionReport` | [45_legacy_import_archive.ostf](../samples/45_legacy_import_archive.ostf) | `/extensions/org.ostf.legacy-import.v1/data/conversionReport` |

### extensions

| Parameter / Schema pointer | Example | JSON Pointer |
| --- | --- | --- |
| `org.ostf.relative-phrase.v1`<br>`#/$defs/extensions/properties/org.ostf.relative-phrase.v1` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/extensions/org.ostf.relative-phrase.v1` |
| `org.ostf.generation-context.v1`<br>`#/$defs/extensions/properties/org.ostf.generation-context.v1` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/extensions/org.ostf.generation-context.v1` |
| `org.ostf.appearance.v1`<br>`#/$defs/extensions/properties/org.ostf.appearance.v1` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/extensions/org.ostf.appearance.v1` |
| `org.ostf.legacy-import.v1`<br>`#/$defs/extensions/properties/org.ostf.legacy-import.v1` | [45_legacy_import_archive.ostf](../samples/45_legacy_import_archive.ostf) | `/extensions/org.ostf.legacy-import.v1` |
| `org.ostf.phrase-library.v1`<br>`#/$defs/extensions/properties/org.ostf.phrase-library.v1` | [22_phrase_library.ostf](../samples/22_phrase_library.ostf) | `/extensions/org.ostf.phrase-library.v1` |
| `org.ostf.clip-choices.v1`<br>`#/$defs/extensions/properties/org.ostf.clip-choices.v1` | [25_choice_shared_muted.ostf](../samples/25_choice_shared_muted.ostf) | `/extensions/org.ostf.clip-choices.v1` |

### phraseTemplate

| Parameter / Schema pointer | Example | JSON Pointer |
| --- | --- | --- |
| `id`<br>`#/$defs/phraseTemplate/properties/id` | [22_phrase_library.ostf](../samples/22_phrase_library.ostf) | `/extensions/org.ostf.phrase-library.v1/data/templates/0/id` |
| `duration`<br>`#/$defs/phraseTemplate/properties/duration` | [22_phrase_library.ostf](../samples/22_phrase_library.ostf) | `/extensions/org.ostf.phrase-library.v1/data/templates/0/duration` |
| `notes`<br>`#/$defs/phraseTemplate/properties/notes` | [22_phrase_library.ostf](../samples/22_phrase_library.ostf) | `/extensions/org.ostf.phrase-library.v1/data/templates/0/notes` |
| `name`<br>`#/$defs/phraseTemplate/properties/name` | [22_phrase_library.ostf](../samples/22_phrase_library.ostf) | `/extensions/org.ostf.phrase-library.v1/data/templates/0/name` |

### phraseNoteMapping

| Parameter / Schema pointer | Example | JSON Pointer |
| --- | --- | --- |
| `templateNoteId`<br>`#/$defs/phraseNoteMapping/properties/templateNoteId` | [22_phrase_library.ostf](../samples/22_phrase_library.ostf) | `/extensions/org.ostf.phrase-library.v1/data/instances/0/noteMap/0/templateNoteId` |
| `repeatIndex`<br>`#/$defs/phraseNoteMapping/properties/repeatIndex` | [22_phrase_library.ostf](../samples/22_phrase_library.ostf) | `/extensions/org.ostf.phrase-library.v1/data/instances/0/noteMap/0/repeatIndex` |
| `noteId`<br>`#/$defs/phraseNoteMapping/properties/noteId` | [22_phrase_library.ostf](../samples/22_phrase_library.ostf) | `/extensions/org.ostf.phrase-library.v1/data/instances/0/noteMap/0/noteId` |

### phraseInstance

| Parameter / Schema pointer | Example | JSON Pointer |
| --- | --- | --- |
| `id`<br>`#/$defs/phraseInstance/properties/id` | [22_phrase_library.ostf](../samples/22_phrase_library.ostf) | `/extensions/org.ostf.phrase-library.v1/data/instances/0/id` |
| `templateId`<br>`#/$defs/phraseInstance/properties/templateId` | [22_phrase_library.ostf](../samples/22_phrase_library.ostf) | `/extensions/org.ostf.phrase-library.v1/data/instances/0/templateId` |
| `clipId`<br>`#/$defs/phraseInstance/properties/clipId` | [22_phrase_library.ostf](../samples/22_phrase_library.ostf) | `/extensions/org.ostf.phrase-library.v1/data/instances/0/clipId` |
| `repeatCount`<br>`#/$defs/phraseInstance/properties/repeatCount` | [22_phrase_library.ostf](../samples/22_phrase_library.ostf) | `/extensions/org.ostf.phrase-library.v1/data/instances/0/repeatCount` |
| `transpose`<br>`#/$defs/phraseInstance/properties/transpose` | [22_phrase_library.ostf](../samples/22_phrase_library.ostf) | `/extensions/org.ostf.phrase-library.v1/data/instances/0/transpose` |
| `noteMap`<br>`#/$defs/phraseInstance/properties/noteMap` | [22_phrase_library.ostf](../samples/22_phrase_library.ostf) | `/extensions/org.ostf.phrase-library.v1/data/instances/0/noteMap` |

### phraseLibraryData

| Parameter / Schema pointer | Example | JSON Pointer |
| --- | --- | --- |
| `templates`<br>`#/$defs/phraseLibraryData/properties/templates` | [22_phrase_library.ostf](../samples/22_phrase_library.ostf) | `/extensions/org.ostf.phrase-library.v1/data/templates` |
| `instances`<br>`#/$defs/phraseLibraryData/properties/instances` | [22_phrase_library.ostf](../samples/22_phrase_library.ostf) | `/extensions/org.ostf.phrase-library.v1/data/instances` |

### clipCandidate

| Parameter / Schema pointer | Example | JSON Pointer |
| --- | --- | --- |
| `id`<br>`#/$defs/clipCandidate/properties/id` | [25_choice_shared_muted.ostf](../samples/25_choice_shared_muted.ostf) | `/extensions/org.ostf.clip-choices.v1/data/groups/0/candidates/0/id` |
| `clipIds`<br>`#/$defs/clipCandidate/properties/clipIds` | [25_choice_shared_muted.ostf](../samples/25_choice_shared_muted.ostf) | `/extensions/org.ostf.clip-choices.v1/data/groups/0/candidates/0/clipIds` |
| `name`<br>`#/$defs/clipCandidate/properties/name` | [55_choice_empty_candidate.ostf](../samples/55_choice_empty_candidate.ostf) | `/extensions/org.ostf.clip-choices.v1/data/groups/0/candidates/0/name` |

### clipChoiceGroup

| Parameter / Schema pointer | Example | JSON Pointer |
| --- | --- | --- |
| `id`<br>`#/$defs/clipChoiceGroup/properties/id` | [25_choice_shared_muted.ostf](../samples/25_choice_shared_muted.ostf) | `/extensions/org.ostf.clip-choices.v1/data/groups/0/id` |
| `candidates`<br>`#/$defs/clipChoiceGroup/properties/candidates` | [25_choice_shared_muted.ostf](../samples/25_choice_shared_muted.ostf) | `/extensions/org.ostf.clip-choices.v1/data/groups/0/candidates` |
| `selectedCandidateId`<br>`#/$defs/clipChoiceGroup/properties/selectedCandidateId` | [25_choice_shared_muted.ostf](../samples/25_choice_shared_muted.ostf) | `/extensions/org.ostf.clip-choices.v1/data/groups/0/selectedCandidateId` |
| `name`<br>`#/$defs/clipChoiceGroup/properties/name` | [25_choice_shared_muted.ostf](../samples/25_choice_shared_muted.ostf) | `/extensions/org.ostf.clip-choices.v1/data/groups/0/name` |

### clipChoicesData

| Parameter / Schema pointer | Example | JSON Pointer |
| --- | --- | --- |
| `groups`<br>`#/$defs/clipChoicesData/properties/groups` | [25_choice_shared_muted.ostf](../samples/25_choice_shared_muted.ostf) | `/extensions/org.ostf.clip-choices.v1/data/groups` |

### root

| Parameter / Schema pointer | Example | JSON Pointer |
| --- | --- | --- |
| `format`<br>`#/properties/format` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/format` |
| `version`<br>`#/properties/version` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/version` |
| `ppq`<br>`#/properties/ppq` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/ppq` |
| `song`<br>`#/properties/song` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/song` |
| `timeline`<br>`#/properties/timeline` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/timeline` |
| `harmony`<br>`#/properties/harmony` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/harmony` |
| `tracks`<br>`#/properties/tracks` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/tracks` |
| `soundSlots`<br>`#/properties/soundSlots` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/soundSlots` |
| `lyrics`<br>`#/properties/lyrics` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/lyrics` |
| `resources`<br>`#/properties/resources` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/resources` |
| `extensions`<br>`#/properties/extensions` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/extensions` |

## 4. 条件付きの全14項目 / All conditional overlays

| Schema pointer | Example | JSON Pointer |
| --- | --- | --- |
| `#/$defs/relativeAssignment/allOf/0/if/properties/basis` | [13_relative_scale.ostf](../samples/13_relative_scale.ostf) | `/extensions/org.ostf.relative-phrase.v1/data/assignments/0/basis` |
| `#/$defs/relativeAssignment/allOf/0/then/properties/index` | [13_relative_scale.ostf](../samples/13_relative_scale.ostf) | `/extensions/org.ostf.relative-phrase.v1/data/assignments/0/index` |
| `#/$defs/extensions/properties/org.ostf.relative-phrase.v1/allOf/1/if/properties/version` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/extensions/org.ostf.relative-phrase.v1/version` |
| `#/$defs/extensions/properties/org.ostf.relative-phrase.v1/allOf/1/then/properties/data` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/extensions/org.ostf.relative-phrase.v1/data` |
| `#/$defs/extensions/properties/org.ostf.generation-context.v1/allOf/1/if/properties/version` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/extensions/org.ostf.generation-context.v1/version` |
| `#/$defs/extensions/properties/org.ostf.generation-context.v1/allOf/1/then/properties/data` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/extensions/org.ostf.generation-context.v1/data` |
| `#/$defs/extensions/properties/org.ostf.appearance.v1/allOf/1/if/properties/version` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/extensions/org.ostf.appearance.v1/version` |
| `#/$defs/extensions/properties/org.ostf.appearance.v1/allOf/1/then/properties/data` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/extensions/org.ostf.appearance.v1/data` |
| `#/$defs/extensions/properties/org.ostf.legacy-import.v1/allOf/1/if/properties/version` | [45_legacy_import_archive.ostf](../samples/45_legacy_import_archive.ostf) | `/extensions/org.ostf.legacy-import.v1/version` |
| `#/$defs/extensions/properties/org.ostf.legacy-import.v1/allOf/1/then/properties/data` | [45_legacy_import_archive.ostf](../samples/45_legacy_import_archive.ostf) | `/extensions/org.ostf.legacy-import.v1/data` |
| `#/$defs/extensions/properties/org.ostf.phrase-library.v1/allOf/1/if/properties/version` | [22_phrase_library.ostf](../samples/22_phrase_library.ostf) | `/extensions/org.ostf.phrase-library.v1/version` |
| `#/$defs/extensions/properties/org.ostf.phrase-library.v1/allOf/1/then/properties/data` | [22_phrase_library.ostf](../samples/22_phrase_library.ostf) | `/extensions/org.ostf.phrase-library.v1/data` |
| `#/$defs/extensions/properties/org.ostf.clip-choices.v1/allOf/1/if/properties/version` | [25_choice_shared_muted.ostf](../samples/25_choice_shared_muted.ostf) | `/extensions/org.ostf.clip-choices.v1/version` |
| `#/$defs/extensions/properties/org.ostf.clip-choices.v1/allOf/1/then/properties/data` | [25_choice_shared_muted.ostf](../samples/25_choice_shared_muted.ostf) | `/extensions/org.ostf.clip-choices.v1/data` |

## 5. 全enum値とconst / Every enum value and constant

| enum rule | Value | Example and location |
| --- | --- | --- |
| `#/$defs/ref/properties/type/enum` | `"section"` | [38_dependency_scopes.ostf](../samples/38_dependency_scopes.ostf)<br>`/extensions/com.example.object-state.v1/dependencies/refs/0/type` |
| `#/$defs/ref/properties/type/enum` | `"track"` | [38_dependency_scopes.ostf](../samples/38_dependency_scopes.ostf)<br>`/extensions/com.example.object-state.v1/dependencies/refs/1/type` |
| `#/$defs/ref/properties/type/enum` | `"clip"` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf)<br>`/extensions/com.example.generator-state.v1/dependencies/refs/0/type` |
| `#/$defs/ref/properties/type/enum` | `"note"` | [17_appearance.ostf](../samples/17_appearance.ostf)<br>`/extensions/org.ostf.appearance.v1/data/appearance/objectColors/1/target/type` |
| `#/$defs/ref/properties/type/enum` | `"chord"` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf)<br>`/extensions/org.ostf.generation-context.v1/data/processes/0/inputs/0/ref/type` |
| `#/$defs/ref/properties/type/enum` | `"scale"` | [38_dependency_scopes.ostf](../samples/38_dependency_scopes.ostf)<br>`/extensions/com.example.object-state.v1/dependencies/refs/5/type` |
| `#/$defs/ref/properties/type/enum` | `"soundSlot"` | [38_dependency_scopes.ostf](../samples/38_dependency_scopes.ostf)<br>`/extensions/com.example.object-state.v1/dependencies/refs/6/type` |
| `#/$defs/ref/properties/type/enum` | `"lyricDocument"` | [38_dependency_scopes.ostf](../samples/38_dependency_scopes.ostf)<br>`/extensions/com.example.object-state.v1/dependencies/refs/7/type` |
| `#/$defs/ref/properties/type/enum` | `"lyricPhrase"` | [38_dependency_scopes.ostf](../samples/38_dependency_scopes.ostf)<br>`/extensions/com.example.object-state.v1/dependencies/refs/8/type` |
| `#/$defs/ref/properties/type/enum` | `"lyricUnit"` | [38_dependency_scopes.ostf](../samples/38_dependency_scopes.ostf)<br>`/extensions/com.example.object-state.v1/dependencies/refs/9/type` |
| `#/$defs/ref/properties/type/enum` | `"lyricAlignment"` | [38_dependency_scopes.ostf](../samples/38_dependency_scopes.ostf)<br>`/extensions/com.example.object-state.v1/dependencies/refs/10/type` |
| `#/$defs/ref/properties/type/enum` | `"resource"` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf)<br>`/extensions/org.ostf.generation-context.v1/data/processes/0/inputs/2/ref/type` |
| `#/$defs/spelledPitchClass/properties/step/enum` | `"A"` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf)<br>`/harmony/chords/1/root/step` |
| `#/$defs/spelledPitchClass/properties/step/enum` | `"B"` | [35_pitch_class_spellings.ostf](../samples/35_pitch_class_spellings.ostf)<br>`/harmony/chords/5/bass/step` |
| `#/$defs/spelledPitchClass/properties/step/enum` | `"C"` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf)<br>`/harmony/chords/0/root/step` |
| `#/$defs/spelledPitchClass/properties/step/enum` | `"D"` | [13_relative_scale.ostf](../samples/13_relative_scale.ostf)<br>`/harmony/scales/0/tonic/step` |
| `#/$defs/spelledPitchClass/properties/step/enum` | `"E"` | [34_all_core_fields.ostf](../samples/34_all_core_fields.ostf)<br>`/harmony/chords/0/bass/step` |
| `#/$defs/spelledPitchClass/properties/step/enum` | `"F"` | [35_pitch_class_spellings.ostf](../samples/35_pitch_class_spellings.ostf)<br>`/harmony/chords/25/bass/step` |
| `#/$defs/spelledPitchClass/properties/step/enum` | `"G"` | [34_all_core_fields.ostf](../samples/34_all_core_fields.ostf)<br>`/harmony/chords/1/bass/step` |
| `#/$defs/meter/properties/denominator/enum` | `1` | [36_all_meter_denominators.ostf](../samples/36_all_meter_denominators.ostf)<br>`/timeline/meterChanges/0/denominator` |
| `#/$defs/meter/properties/denominator/enum` | `2` | [36_all_meter_denominators.ostf](../samples/36_all_meter_denominators.ostf)<br>`/timeline/meterChanges/1/denominator` |
| `#/$defs/meter/properties/denominator/enum` | `4` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf)<br>`/timeline/meterChanges/0/denominator` |
| `#/$defs/meter/properties/denominator/enum` | `8` | [11_meter_tempo_gaps.ostf](../samples/11_meter_tempo_gaps.ostf)<br>`/timeline/meterChanges/1/denominator` |
| `#/$defs/meter/properties/denominator/enum` | `16` | [36_all_meter_denominators.ostf](../samples/36_all_meter_denominators.ostf)<br>`/timeline/meterChanges/4/denominator` |
| `#/$defs/meter/properties/denominator/enum` | `32` | [36_all_meter_denominators.ostf](../samples/36_all_meter_denominators.ostf)<br>`/timeline/meterChanges/5/denominator` |
| `#/$defs/meter/properties/denominator/enum` | `64` | [36_all_meter_denominators.ostf](../samples/36_all_meter_denominators.ostf)<br>`/timeline/meterChanges/6/denominator` |
| `#/$defs/resource/properties/kind/enum` | `"audio"` | [16_generation_context.ostf](../samples/16_generation_context.ostf)<br>`/resources/0/kind` |
| `#/$defs/resource/properties/kind/enum` | `"midi"` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf)<br>`/resources/0/kind` |
| `#/$defs/resource/properties/kind/enum` | `"text"` | [16_generation_context.ostf](../samples/16_generation_context.ostf)<br>`/resources/1/kind` |
| `#/$defs/resource/properties/kind/enum` | `"other"` | [37_resource_kinds.ostf](../samples/37_resource_kinds.ostf)<br>`/resources/3/kind` |
| `#/$defs/dependencies/oneOf/0/properties/scope/enum` | `"document"` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf)<br>`/extensions/org.ostf.appearance.v1/dependencies/scope` |
| `#/$defs/dependencies/oneOf/0/properties/scope/enum` | `"none"` | [18_opaque_precision.ostf](../samples/18_opaque_precision.ostf)<br>`/extensions/com.example.precision.v1/dependencies/scope` |
| `#/$defs/extension/properties/status/enum` | `"current"` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf)<br>`/extensions/com.example.generator-state.v1/status` |
| `#/$defs/extension/properties/status/enum` | `"stale"` | [14_stale_source.ostf](../samples/14_stale_source.ostf)<br>`/extensions/org.ostf.relative-phrase.v1/status` |
| `#/$defs/extension/properties/status/enum` | `"unverified"` | [15_unverified_source.ostf](../samples/15_unverified_source.ostf)<br>`/extensions/org.ostf.relative-phrase.v1/status` |
| `#/$defs/relativeAssignment/properties/basis/enum` | `"chordTone"` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf)<br>`/extensions/org.ostf.relative-phrase.v1/data/assignments/0/basis` |
| `#/$defs/relativeAssignment/properties/basis/enum` | `"scaleDegree"` | [13_relative_scale.ostf](../samples/13_relative_scale.ostf)<br>`/extensions/org.ostf.relative-phrase.v1/data/assignments/0/basis` |

| const rule | Value | Example and location |
| --- | --- | --- |
| `#/$defs/chord/properties/intervals/contains/const` | `0` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf)<br>`/harmony/chords/0/intervals/0` |
| `#/$defs/scale/properties/intervals/contains/const` | `0` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf)<br>`/harmony/scales/0/intervals/0` |
| `#/$defs/dependencies/oneOf/1/properties/scope/const` | `"objects"` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf)<br>`/extensions/com.example.generator-state.v1/dependencies/scope` |
| `#/$defs/relativeAssignment/allOf/0/if/properties/basis/const` | `"scaleDegree"` | [13_relative_scale.ostf](../samples/13_relative_scale.ostf)<br>`/extensions/org.ostf.relative-phrase.v1/data/assignments/0/basis` |
| `#/$defs/legacyData/properties/sourceVersion/const` | `"2.3.0"` | [45_legacy_import_archive.ostf](../samples/45_legacy_import_archive.ostf)<br>`/extensions/org.ostf.legacy-import.v1/data/sourceVersion` |
| `#/$defs/extensions/properties/org.ostf.relative-phrase.v1/allOf/1/if/properties/version/const` | `"1.0.0-draft.1"` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf)<br>`/extensions/org.ostf.relative-phrase.v1/version` |
| `#/$defs/extensions/properties/org.ostf.generation-context.v1/allOf/1/if/properties/version/const` | `"1.0.0-draft.1"` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf)<br>`/extensions/org.ostf.generation-context.v1/version` |
| `#/$defs/extensions/properties/org.ostf.appearance.v1/allOf/1/if/properties/version/const` | `"1.0.0-draft.1"` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf)<br>`/extensions/org.ostf.appearance.v1/version` |
| `#/$defs/extensions/properties/org.ostf.legacy-import.v1/allOf/1/if/properties/version/const` | `"1.0.0-draft.1"` | [45_legacy_import_archive.ostf](../samples/45_legacy_import_archive.ostf)<br>`/extensions/org.ostf.legacy-import.v1/version` |
| `#/$defs/extensions/properties/org.ostf.phrase-library.v1/allOf/1/if/properties/version/const` | `"1.0.0-draft.1"` | [22_phrase_library.ostf](../samples/22_phrase_library.ostf)<br>`/extensions/org.ostf.phrase-library.v1/version` |
| `#/$defs/extensions/properties/org.ostf.clip-choices.v1/allOf/1/if/properties/version/const` | `"1.0.0-draft.1"` | [25_choice_shared_muted.ostf](../samples/25_choice_shared_muted.ostf)<br>`/extensions/org.ostf.clip-choices.v1/version` |
| `#/properties/format/const` | `"OSTF"` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf)<br>`/format` |
| `#/properties/version/const` | `"3.0.0"` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf)<br>`/version` |

## 6. 全51型定義 / Every named definition

| Definition | Example | JSON Pointer |
| --- | --- | --- |
| `#/$defs/id` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/extensions/com.example.generator-state.v1/dependencies/refs/0/id` |
| `#/$defs/nonnegative` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/extensions/org.ostf.generation-context.v1/data/processes/0/targetRange/start` |
| `#/$defs/positive` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/extensions/org.ostf.generation-context.v1/data/processes/0/targetRange/duration` |
| `#/$defs/signed` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/tracks/0/clips/0/notes/0/start` |
| `#/$defs/pitch` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/extensions/org.ostf.relative-phrase.v1/data/assignments/0/anchorPitch` |
| `#/$defs/ref` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/extensions/com.example.generator-state.v1/dependencies/refs/0` |
| `#/$defs/range` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/extensions/org.ostf.generation-context.v1/data/processes/0/targetRange` |
| `#/$defs/spelledPitchClass` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/harmony/chords/0/root` |
| `#/$defs/song` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/song` |
| `#/$defs/section` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/timeline/sections/0` |
| `#/$defs/tempo` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/timeline/tempoChanges/0` |
| `#/$defs/meter` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/timeline/meterChanges/0` |
| `#/$defs/timeline` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/timeline` |
| `#/$defs/chord` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/harmony/chords/0` |
| `#/$defs/scale` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/harmony/scales/0` |
| `#/$defs/harmony` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/harmony` |
| `#/$defs/instrument` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/tracks/0/instrument` |
| `#/$defs/note` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/tracks/0/clips/0/notes/0` |
| `#/$defs/clip` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/tracks/0/clips/0` |
| `#/$defs/track` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/tracks/0` |
| `#/$defs/soundSlot` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/soundSlots/0` |
| `#/$defs/lyricDocument` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/lyrics/documents/0` |
| `#/$defs/lyricPhrase` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/lyrics/phrases/0` |
| `#/$defs/lyricUnit` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/lyrics/units/0` |
| `#/$defs/lyricAlignment` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/lyrics/alignments/0` |
| `#/$defs/lyrics` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/lyrics` |
| `#/$defs/sha256` | [16_generation_context.ostf](../samples/16_generation_context.ostf) | `/resources/0/sha256` |
| `#/$defs/resource` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/resources/0` |
| `#/$defs/dependencies` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/extensions/com.example.generator-state.v1/dependencies` |
| `#/$defs/extension` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/extensions/com.example.generator-state.v1` |
| `#/$defs/relativeAssignment` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/extensions/org.ostf.relative-phrase.v1/data/assignments/0` |
| `#/$defs/relativeData` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/extensions/org.ostf.relative-phrase.v1/data` |
| `#/$defs/generator` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/extensions/org.ostf.generation-context.v1/data/processes/0/generator` |
| `#/$defs/generationInput` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/extensions/org.ostf.generation-context.v1/data/processes/0/inputs/0` |
| `#/$defs/generationProcess` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/extensions/org.ostf.generation-context.v1/data/processes/0` |
| `#/$defs/generationData` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/extensions/org.ostf.generation-context.v1/data` |
| `#/$defs/color` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/extensions/org.ostf.appearance.v1/data/appearance/customRoleColors/role-verse` |
| `#/$defs/roleDefinition` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/extensions/org.ostf.appearance.v1/data/roleDefinitions/0` |
| `#/$defs/roleColorMap` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/extensions/org.ostf.appearance.v1/data/appearance/roleColors` |
| `#/$defs/customRoleColorMap` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/extensions/org.ostf.appearance.v1/data/appearance/customRoleColors` |
| `#/$defs/objectColor` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/extensions/org.ostf.appearance.v1/data/appearance/objectColors/0` |
| `#/$defs/appearanceData` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/extensions/org.ostf.appearance.v1/data` |
| `#/$defs/legacyData` | [45_legacy_import_archive.ostf](../samples/45_legacy_import_archive.ostf) | `/extensions/org.ostf.legacy-import.v1/data` |
| `#/$defs/extensions` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/extensions` |
| `#/$defs/phraseTemplate` | [22_phrase_library.ostf](../samples/22_phrase_library.ostf) | `/extensions/org.ostf.phrase-library.v1/data/templates/0` |
| `#/$defs/phraseNoteMapping` | [22_phrase_library.ostf](../samples/22_phrase_library.ostf) | `/extensions/org.ostf.phrase-library.v1/data/instances/0/noteMap/0` |
| `#/$defs/phraseInstance` | [22_phrase_library.ostf](../samples/22_phrase_library.ostf) | `/extensions/org.ostf.phrase-library.v1/data/instances/0` |
| `#/$defs/phraseLibraryData` | [22_phrase_library.ostf](../samples/22_phrase_library.ostf) | `/extensions/org.ostf.phrase-library.v1/data` |
| `#/$defs/clipCandidate` | [25_choice_shared_muted.ostf](../samples/25_choice_shared_muted.ostf) | `/extensions/org.ostf.clip-choices.v1/data/groups/0/candidates/0` |
| `#/$defs/clipChoiceGroup` | [25_choice_shared_muted.ostf](../samples/25_choice_shared_muted.ostf) | `/extensions/org.ostf.clip-choices.v1/data/groups/0` |
| `#/$defs/clipChoicesData` | [25_choice_shared_muted.ostf](../samples/25_choice_shared_muted.ostf) | `/extensions/org.ostf.clip-choices.v1/data` |

## 7. 構造の分岐 / Structural forms

The following 39 observations identify applicable shapes and presence/tag combinations. They are not evaluations of every JSON Schema condition. Valid examples cover both note targets, both choice-selection forms, both dependency-object shapes, paired presence/absence of chord structure and lyric timing, both relative bases, and known/unknown versions for every standard namespace.

| Form | Example | JSON Pointer |
| --- | --- | --- |
| `#/$defs/chord/dependentRequired=paired-absent` | [03_harmony_only.ostf](../samples/03_harmony_only.ostf) | `/harmony/chords/1` |
| `#/$defs/chord/dependentRequired=paired-present` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/harmony/chords/0` |
| `#/$defs/clipChoiceGroup/properties/selectedCandidateId/anyOf/0` | [25_choice_shared_muted.ostf](../samples/25_choice_shared_muted.ostf) | `/extensions/org.ostf.clip-choices.v1/data/groups/0/selectedCandidateId` |
| `#/$defs/clipChoiceGroup/properties/selectedCandidateId/anyOf/1` | [26_choice_none.ostf](../samples/26_choice_none.ostf) | `/extensions/org.ostf.clip-choices.v1/data/groups/0/selectedCandidateId` |
| `#/$defs/dependencies/oneOf/0` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/extensions/org.ostf.appearance.v1/dependencies` |
| `#/$defs/dependencies/oneOf/1` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/extensions/com.example.generator-state.v1/dependencies` |
| `#/$defs/extensions/properties/org.ostf.appearance.v1/allOf/0` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/extensions/org.ostf.appearance.v1` |
| `#/$defs/extensions/properties/org.ostf.appearance.v1/allOf/1` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/extensions/org.ostf.appearance.v1` |
| `#/$defs/extensions/properties/org.ostf.appearance.v1/allOf/1/if=false` | [51_opaque_json_values.ostf](../samples/51_opaque_json_values.ostf) | `/extensions/org.ostf.appearance.v1` |
| `#/$defs/extensions/properties/org.ostf.appearance.v1/allOf/1/if=true` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/extensions/org.ostf.appearance.v1` |
| `#/$defs/extensions/properties/org.ostf.clip-choices.v1/allOf/0` | [25_choice_shared_muted.ostf](../samples/25_choice_shared_muted.ostf) | `/extensions/org.ostf.clip-choices.v1` |
| `#/$defs/extensions/properties/org.ostf.clip-choices.v1/allOf/1` | [25_choice_shared_muted.ostf](../samples/25_choice_shared_muted.ostf) | `/extensions/org.ostf.clip-choices.v1` |
| `#/$defs/extensions/properties/org.ostf.clip-choices.v1/allOf/1/if=false` | [29_future_optional_profiles.ostf](../samples/29_future_optional_profiles.ostf) | `/extensions/org.ostf.clip-choices.v1` |
| `#/$defs/extensions/properties/org.ostf.clip-choices.v1/allOf/1/if=true` | [25_choice_shared_muted.ostf](../samples/25_choice_shared_muted.ostf) | `/extensions/org.ostf.clip-choices.v1` |
| `#/$defs/extensions/properties/org.ostf.generation-context.v1/allOf/0` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/extensions/org.ostf.generation-context.v1` |
| `#/$defs/extensions/properties/org.ostf.generation-context.v1/allOf/1` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/extensions/org.ostf.generation-context.v1` |
| `#/$defs/extensions/properties/org.ostf.generation-context.v1/allOf/1/if=false` | [51_opaque_json_values.ostf](../samples/51_opaque_json_values.ostf) | `/extensions/org.ostf.generation-context.v1` |
| `#/$defs/extensions/properties/org.ostf.generation-context.v1/allOf/1/if=true` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/extensions/org.ostf.generation-context.v1` |
| `#/$defs/extensions/properties/org.ostf.legacy-import.v1/allOf/0` | [45_legacy_import_archive.ostf](../samples/45_legacy_import_archive.ostf) | `/extensions/org.ostf.legacy-import.v1` |
| `#/$defs/extensions/properties/org.ostf.legacy-import.v1/allOf/1` | [45_legacy_import_archive.ostf](../samples/45_legacy_import_archive.ostf) | `/extensions/org.ostf.legacy-import.v1` |
| `#/$defs/extensions/properties/org.ostf.legacy-import.v1/allOf/1/if=false` | [51_opaque_json_values.ostf](../samples/51_opaque_json_values.ostf) | `/extensions/org.ostf.legacy-import.v1` |
| `#/$defs/extensions/properties/org.ostf.legacy-import.v1/allOf/1/if=true` | [45_legacy_import_archive.ostf](../samples/45_legacy_import_archive.ostf) | `/extensions/org.ostf.legacy-import.v1` |
| `#/$defs/extensions/properties/org.ostf.phrase-library.v1/allOf/0` | [22_phrase_library.ostf](../samples/22_phrase_library.ostf) | `/extensions/org.ostf.phrase-library.v1` |
| `#/$defs/extensions/properties/org.ostf.phrase-library.v1/allOf/1` | [22_phrase_library.ostf](../samples/22_phrase_library.ostf) | `/extensions/org.ostf.phrase-library.v1` |
| `#/$defs/extensions/properties/org.ostf.phrase-library.v1/allOf/1/if=false` | [29_future_optional_profiles.ostf](../samples/29_future_optional_profiles.ostf) | `/extensions/org.ostf.phrase-library.v1` |
| `#/$defs/extensions/properties/org.ostf.phrase-library.v1/allOf/1/if=true` | [22_phrase_library.ostf](../samples/22_phrase_library.ostf) | `/extensions/org.ostf.phrase-library.v1` |
| `#/$defs/extensions/properties/org.ostf.relative-phrase.v1/allOf/0` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/extensions/org.ostf.relative-phrase.v1` |
| `#/$defs/extensions/properties/org.ostf.relative-phrase.v1/allOf/1` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/extensions/org.ostf.relative-phrase.v1` |
| `#/$defs/extensions/properties/org.ostf.relative-phrase.v1/allOf/1/if=false` | [19_future_profile.ostf](../samples/19_future_profile.ostf) | `/extensions/org.ostf.relative-phrase.v1` |
| `#/$defs/extensions/properties/org.ostf.relative-phrase.v1/allOf/1/if=true` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/extensions/org.ostf.relative-phrase.v1` |
| `#/$defs/lyricPhrase/dependentRequired=paired-absent` | [05_lyrics_only.ostf](../samples/05_lyrics_only.ostf) | `/lyrics/phrases/0` |
| `#/$defs/lyricPhrase/dependentRequired=paired-present` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/lyrics/phrases/0` |
| `#/$defs/lyricUnit/dependentRequired=paired-absent` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/lyrics/units/0` |
| `#/$defs/lyricUnit/dependentRequired=paired-present` | [34_all_core_fields.ostf](../samples/34_all_core_fields.ostf) | `/lyrics/units/0` |
| `#/$defs/note/oneOf/0` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/tracks/0/clips/0/notes/0` |
| `#/$defs/note/oneOf/1` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/tracks/3/clips/0/notes/0` |
| `#/$defs/relativeAssignment/allOf/0` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/extensions/org.ostf.relative-phrase.v1/data/assignments/0` |
| `#/$defs/relativeAssignment/allOf/0/if=false` | [01_four_part_sketch.ostf](../samples/01_four_part_sketch.ostf) | `/extensions/org.ostf.relative-phrase.v1/data/assignments/0` |
| `#/$defs/relativeAssignment/allOf/0/if=true` | [13_relative_scale.ostf](../samples/13_relative_scale.ostf) | `/extensions/org.ostf.relative-phrase.v1/data/assignments/0` |

## 8. 使い方・意味の対応 / Feature navigation

| 目的 / Feature | Examples |
| --- | --- |
| 空・メロディー・和声・歌詞から始める / Incomplete entry points | 02–05 |
| 全Coreフィールド / All Core fields together | [34](../samples/34_all_core_fields.ostf) |
| 音名綴り・全拍子分母・全素材種別 / Spellings, meters, resources | 35–37 |
| 全参照種別・依存scope / Reference kinds and dependency scopes | 38, 41, 43 |
| 連符・弱起・テール・同音重複 / Tuplets, pickups, tails, overlap | 07–09, 21, 24, 60 |
| 有効状態と候補の関係 / Enabled states and choices | 10, 25–29, 55–57 |
| 相対音・状態・再解釈しない読込 / Relative pitch and saved correspondence | 12–15, 39–40, 52 |
| 生成範囲・入力・保護 / Generation input, ranges and protection | 16, 41–42 |
| 表示の全対象と優先順 / Appearance targets and priority | 17, 43–44 |
| 歌詞と複数言語 / Lyrics and languages | 05, 20, 34, 46 |
| templateと実体、置換、解除 / Templates, realization, replacement, detachment | 22–24, 30–33, 53–54, 59 |
| 空文字・省略・空の任意profile / Empty strings, omission, empty profiles | 02, 28, 50, 53, 55 |
| 未知の値・未知profile版 / Opaque values and future versions | 18–19, 29, 51 |
| 原典アーカイブ / Original-source archive | [45](../samples/45_legacy_import_archive.ostf), [58](../samples/58_complete_workflow.ostf) |
| 全6profileの共存 / All six profiles together | [58](../samples/58_complete_workflow.ostf) |
| 複数パートの構成 / Multiple-part arrangement | 01, 60 |

各番号の完全なファイル名と目的は[サンプル索引](../samples/INDEX.md)を参照してください。境界値の例は、その値を普段の作曲へ推奨するものではありません。単独の状態ファイルは、操作を実行した証拠や保護比較の結果を証明しません。

The coverage files describe the frozen release samples. If a schema or sample is edited later, its old inventory/hash is no longer evidence about the edited contents. The included `tools/build_reference.py` regenerates the parameter reference and catalogue from the schema; it does not regenerate this sample-coverage inventory or perform validation.
