# OSTF 3.0.0 implementer quickstart

This is an informative guide for a first implementation. It introduces no new
fields, defaults, conformance levels or requirements. The
[Japanese specification](FORMAT_SPECIFICATION.ja.md),
[English specification](FORMAT_SPECIFICATION.en.md), and
[3.0.0 schema](../schema/ostf-3.0.0.schema.json) define the contract.
Release terms are specified in [LICENSE.md](../LICENSE.md).

## 日本語

### 1. 最初に実装する範囲を決める

初回は、任意profileを使わず、具体的なノートをCoreへ書き出す機能から
始められます。既存ファイルの読込、編集、生成設定の再現は、それぞれ別の
対応範囲として案内します。

| 能力 | 実装する内容 | 対応表明で分けること |
| --- | --- | --- |
| Core exporter | 自分のアプリの曲情報と採用した演奏から、有効なCore文書を作る | 書き出す音楽層・対象とroot版。任意profileは省略可能 |
| Core player | 保存されたノート、PPQ、テンポ、track/clipの有効状態から演奏イベントを得る | 読み込むroot版、音高・打楽器の出力範囲、出力先で補う値や変換上の制約 |
| 情報を保持するeditor | 既存の情報とIDを保持して編集し、依存する拡張の同期状態を扱う | 未知情報の保持と、理解して編集できるprofileを区別 |
| Validator | 厳密JSON入力、構造、時間計算、ID・参照などの適合性を判定する | 検査するroot版・profile版・層を明示。Schemaだけの成功と全体適合を区別 |

例えば「3.0.0 Coreの音高付きノートを書き出す」は具体的な対応表明です。
それだけで旧Draftの読込、未知情報を保持した往復編集、他社の生成処理の再現
まで対応したことにはなりません。参照ツールが旧2版を扱えることは、すべての
新規exporterに旧版変換の実装を要求するものでもありません。

### 2. 最小文書でも必要な11のrootキー

| キー | 最初の実装で用意する内容 |
| --- | --- |
| `format` | 正確な文字列 `"OSTF"` |
| `version` | 正確な文字列 `"3.0.0"` |
| `ppq` | 四分音符当たりのtick数。整数1〜960000。推奨960 |
| `song` | `title` を持つオブジェクト。未命名なら空文字列でよい |
| `timeline` | `sections`、`tempoChanges`、`meterChanges` の3配列 |
| `harmony` | `chords`、`scales` の2配列 |
| `tracks` | track配列。演奏未作成なら空配列 |
| `soundSlots` | 打楽器などの発音対象の配列。使わなければ空配列 |
| `lyrics` | `documents`、`phrases`、`units`、`alignments` の4配列 |
| `resources` | 素材参照の配列。使わなければ空配列 |
| `extensions` | 拡張オブジェクト。Coreだけなら `{}` |

コードだけ、メロディーだけ、歌詞だけの途中状態も扱えます。使わない配列は
空のまま残します。ただし、`tempoChanges` と `meterChanges` は、それぞれ
`at: 0` の要素を持つ必要があります。変更点は厳密な昇順にします。BPMは
拍子にかかわらず四分音符毎分であり、読み手は宣言されたPPQを使います。

ファイルはBOMなしのUTF-8 JSONオブジェクト一つです。整数項目には `1` の
ような整数tokenを使い、`1.0`、`1e0`、真偽値を整数の代用にしません。
Coreのオブジェクトへ未定義の項目を追加せず、必要な独自情報は拡張へ記録します。
厳密入力の詳細は仕様第2章を参照してください。

### 3. ノートを保存する最小の形

| オブジェクト | 必須項目 |
| --- | --- |
| Track | `id`、`name`、`clips` |
| Clip | `id`、`start`、`duration`、`notes` |
| Note | `id`、`start`、`duration` と、`pitch` または `soundSlotId` の一方だけ |

音高は0〜127の整数半音番号で、60=C4です。`soundSlotId` を使うノートには、
実在するsound slotへの参照が必要です。Coreノートにvelocityはありません。

Core IDは全種別を通じて文書内で一意にします。音高や配列番号を同一性の判定に
使わず、独立した複製には新しいIDを与えます。track/clipの `enabled` は省略時
trueです。無効な配置も保存し、構造・参照・時間の規則を満たす必要があります。

時間は次の式で読み取れます。

```text
onset   = clip.start + note.start
gateEnd = onset + note.duration
MAX     = 9007199254740991
```

clipの開始は非負、noteの開始はclipからの符号付きtickです。`duration` は
正の整数です。個別値の範囲に加え、clipの配置終端、ノートの絶対onsetと
ゲート終端も上限内に収め、絶対onsetを負にしません。

clipの `duration` は配置・編集のための区間であり、ノートを切る位置では
ありません。弱起、区間後から始まる音、末尾を越える音、同音重複をそのまま
保持します。track内のclipsとclip内のnotesは `start` の非減少順にし、
同じstartでは配列順を保ちます。track配列自体は表示順です。

playerはtrackとclipの両方が有効なノートだけを演奏します。イベントを並べる
場合はtick順、同tickではnoteOffの後にnoteOn、同種の同tickではnoteIdの
辞書順です。実効演奏の終端は有効ノートの最大gateEndで、該当ノートがなければ0です。

### 4. まず読む二つの例

[04_melody_only.ostf](../samples/04_melody_only.ostf) は、
和声や歌詞、任意profileを持たない1track・1clipのメロディー例です。
PPQは960、clip.startは0、clip.durationは1920です。

| ノート | pitch | 開始tick | ゲートtick | 算術上のgateEnd |
| --- | ---: | ---: | ---: | ---: |
| `melody-c` | 60 | 0 | 432 | 432 |
| `melody-e` | 64 | 480 | 432 | 912 |
| `melody-g` | 67 | 960 | 432 | 1392 |
| `melody-a` | 69 | 1440 | 432 | 1872 |

この例の480tick間隔は8分音符のグリッドで、432tickのゲートはその90%です。
**90%はこの例の選択であり、OSTF共通の既定値ではありません。** 保存されるのは
比率ではなく実際の整数tickです。最後のゲートは1872で終わり、clipの配置区間は
1920まであります。表の値はファイルの記述と算術の説明であり、実行結果ではありません。

[03_harmony_only.ostf](../samples/03_harmony_only.ostf) は、
構造化したCコードとlabelだけのコードを持つ、和声先行の例です。`tracks` は
空なので、**保存されたノート演奏はありません**。読み手がコード名から伴奏を
自動的に発音する指示ではありません。生成機能が伴奏を作った場合は、その採用結果を
別途Coreノートへ保存します。

この2例は旧04・03のroot版だけを変更した記述例です。今回のコードによる変換、
検証器、再生の実行結果ではありません。由来は[サンプル索引](../samples/INDEX.md)と
[正式版例のカタログ](../samples/catalog.json)に記載しています。

### 5. 任意profileを後から加えるとき

root版とprofile版は独立しています。現行Coreは `3.0.0`、同梱の6つの任意
profileはそれぞれ正確な `1.0.0-draft.1` です。profileの `current` は保存文書
との対応状態であり、規格が正式版かどうかを表しません。

Core playerは保存済みノートを使い、読込時にフレーズを再展開したり、候補を
選び直したり、独自生成器を実行したりしません。素材のURIも読込だけでは取得・実行しません。

editorが未知の拡張を保持するときは、envelopeとpayloadを残し、関係する編集後の
同期状態を仕様どおりに扱います。無損失を表明する場合は、未知の大きな整数、
精密な十進数、整数／実数tokenの区別まで保持する必要があります。通常のbinary64へ
読み込んで保存し直すだけで、その保持を保証することはできません。

**同梱の参照validatorは「Coreだけを検査するモード」ではありません。** root版に
対応する既知profile集合を使い、その正確な版のdataがあれば構造と意味も検査します。
未知の名前空間や版には共通envelope・依存参照の規則を適用し、payloadは推測しません。
既知profileの構造不正は `stale`／`unverified` でもエラーです。Schemaの成功だけで
参照や時間計算を含む全適合を表明しないでください。詳しい境界は
[参照実装ガイド](REFERENCE_IMPLEMENTATION.md)と仕様第9章にあります。

## English

### 1. Choose the first capability

A first implementation can export explicit Core notes with no optional profiles.
Declare reading, writing, preservation-aware editing and generator reproduction
separately.

| Capability | Implementation responsibility | Declare separately |
| --- | --- | --- |
| Core exporter | Create a valid Core document from the application's own content and adopted performance | Root version and musical content/targets exported; optional profiles may be absent |
| Core player | Derive events from stored notes, declared PPQ, tempo and track/clip enabled states | Root versions, pitched/percussion output, supplied output values and conversion limitations |
| Preserving editor | Retain existing information and identities while handling dependent extension status after edits | Unknown-data preservation versus profiles understood and edited |
| Validator | Check strict input, structure, time arithmetic, identities and references | Exact roots/profiles and validation layers; schema success alone is not full conformance |

For example, “OSTF 3.0.0 Core export of pitched notes” states a useful bounded
capability. It does not claim historical Draft import, lossless round-trip editing
or reproduction of another application's generator. The reference tools' support
for older roots does not require every new exporter to implement draft conversion.

### 2. The eleven required root members

| Member | Initial content |
| --- | --- |
| `format` | Exact string `"OSTF"` |
| `version` | Exact string `"3.0.0"` |
| `ppq` | Integer ticks per quarter note, 1–960000; 960 is recommended |
| `song` | Object with `title`; an empty title is allowed |
| `timeline` | Arrays `sections`, `tempoChanges`, `meterChanges` |
| `harmony` | Arrays `chords`, `scales` |
| `tracks` | Track array, empty if no performance has been written |
| `soundSlots` | Sound-target array, empty when unused |
| `lyrics` | Arrays `documents`, `phrases`, `units`, `alignments` |
| `resources` | Resource array, empty when unused |
| `extensions` | Extension object; use `{}` for a Core-only document |

Harmony-only, melody-only and lyrics-only work is permitted. Keep unused arrays
empty, but supply an entry at `at: 0` in both tempo and meter maps. Subsequent map
positions strictly increase. BPM always means quarter notes per minute; honor the
declared PPQ independently of meter.

Write one UTF-8 JSON object without a BOM. Integer fields use integer tokens such
as `1`, not `1.0`, `1e0` or booleans. Core objects are closed; proprietary fields
belong in extensions. See specification Section 2 for the full strict-input rules.

### 3. A minimal note hierarchy

| Object | Required members |
| --- | --- |
| Track | `id`, `name`, `clips` |
| Clip | `id`, `start`, `duration`, `notes` |
| Note | `id`, `start`, `duration`, and exactly one of `pitch` or `soundSlotId` |

Pitch is an integer semitone number from 0 through 127, with 60=C4. A
`soundSlotId` must resolve to an existing sound slot. Core notes have no velocity.
Core IDs are unique across all kinds in a document; independent copies need new
IDs. Pitch and array position are not identities. Track and clip `enabled`
default semantically to true when absent. Disabled placements still retain valid
structure, timing and references.

```text
onset   = clip.start + note.start
gateEnd = onset + note.duration
MAX     = 9007199254740991
```

Clip start is nonnegative, note start is a signed clip-local offset, and duration
is a positive integer. Check field bounds and computed placement/note endpoints;
absolute onset cannot be negative, and endpoints cannot exceed MAX.

Clip duration describes a placement span, not a note cutoff. Preserve pickups,
late starts, tails and independent same-pitch overlaps. Clips within a track and
notes within a clip use nondecreasing start order, retaining order at equal
starts. Track order is display order.

A player uses a note only when both its track and clip are enabled. Event order
is tick first, noteOff before noteOn at the same tick, then lexicographic noteId
for the same tick and kind. Performance end is the largest active gateEnd, or 0
when there are no active notes.

### 4. Two starting examples

[04_melody_only.ostf](../samples/04_melody_only.ostf) contains one
track, one clip and four pitched notes, without harmony, lyrics or profiles. PPQ
is 960; the clip starts at 0 and has a placement duration of 1920.

| Note | Pitch | Start ticks | Gate ticks | Arithmetic gateEnd |
| --- | ---: | ---: | ---: | ---: |
| `melody-c` | 60 | 0 | 432 | 432 |
| `melody-e` | 64 | 480 | 432 | 912 |
| `melody-g` | 67 | 960 | 432 | 1392 |
| `melody-a` | 69 | 1440 | 432 | 1872 |

The 480-tick grid is an eighth note here, and the 432-tick gate is 90% of that
grid. **This is a choice in this example, not an OSTF default.** The document
stores actual integer ticks, not a gate percentage. The final gate ends at 1872
while the placement span ends at 1920. These are descriptions of the stored data
and arithmetic, not execution observations.

[03_harmony_only.ostf](../samples/03_harmony_only.ostf) contains a
structured C chord and a label-only chord, with `tracks: []`. It contains no
stored note performance and does not instruct a player to generate accompaniment
from the harmony. A generator can explicitly create accompaniment and store the
adopted result as Core notes.

These examples copy historical examples 04 and 03 with only the root version
changed. They are authored examples, not executed conversion, validation or
playback results. Provenance is in the [sample index](../samples/INDEX.md) and
[stable catalogue](../samples/catalog.json).

### 5. Add optional meaning deliberately

Root and profile versions are independent: current Core is `3.0.0`, while the
six bundled optional profiles remain exact provisional `1.0.0-draft.1` versions.
`current` describes correspondence with the saved document, not specification
maturity.

A Core player uses stored notes without rematerializing phrases, reselecting
candidates or executing a generator on load. Loading also does not fetch or
execute resource URIs.

An editor preserving unknown extensions retains their envelopes and payloads,
then handles synchronization status after relevant edits as the specification
requires. A lossless claim includes large integers, precise decimal values and
integer/real token categories. Ordinary binary64 parsing and reserialization
alone cannot establish that preservation.

**The bundled reference validator is not a Core-only validation mode.** It selects
the known profile set for the root and checks the exact supported profiles'
structures and semantics when present. For unknown namespaces or versions it
checks the common envelope and dependencies without guessing payload meaning.
A malformed known structure remains an error even when stale or unverified.
Schema success alone does not establish full reference and time-arithmetic
conformance. See the [implementation guide](REFERENCE_IMPLEMENTATION.md) and
specification Section 9.

## Evidence status / 実行記録との区別

This guide and its new examples were prepared by static reading and authoring.
No project code, validator, CLI, Schema self-check, test or DAW was run for this
revision. The retained 213-case / 89-criterion report applies to Draft 2 Revision 1,
not to the stable implementation or these new examples. This task adds no runtime
verification requirement to the release decision.

このガイドと新しい記述例は静的な読解・作成によるものです。今回、実装コード、
検証器、CLI、Schema自己検査、試験、DAWは実行していません。過去の213件・89観点の
レポートはDraft 2 Revision 1の記録であり、正式版の実装や新しい記述例の実行結果では
ありません。追加の動作検証を今回のリリース判定条件にしていません。
