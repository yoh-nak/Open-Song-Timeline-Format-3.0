# Conformance contract / 適合条件

This is a consolidated statement of **89 retained conformance viewpoints**, not an execution report. The original Core/wire/migration criteria, Draft 2 additions, and Revision 1 operation criteria keep their identifiers for traceability. The two former development-baseline entries D201/R101 are expressed as baseline-preservation viewpoints here; obsolete test totals are not prerequisites for the stable release. The normative [specifications](FORMAT_SPECIFICATION.en.md) and [Schema](../schema/ostf-3.0.0.schema.json) determine the actual format contract.

本書の89件は、実装が備えるべき挙動を整理した観点数です。実行ケース数や合格数ではありません。今回、プロジェクトのimport、CLI、validator、Schema検査、試験、DAW/MIDI再生、展開後実行は行っていません。以前のDraft 2 Revision 1の実行記録を3.0.0の結果として転用しません。過去のrunner・fixture・実行reportは以前の開発配布物に残し、この98ファイルの正式配布セットには含めません。

## 1. Declare support precisely / 対応範囲を示す

| Capability | Meaning |
| --- | --- |
| Core exporter | Write the supported Core layers, complete required containers, explicit notes and valid references; optional profiles may be absent |
| Core reader/player | Interpret stored notes and enabled states without generation, profile-driven rewriting or candidate auto-selection |
| Preserving editor | Preserve unknown values and exact numeric values/token categories; invalidate affected current claims after edits |
| Exact profile implementation | State namespace and exact version; enforce its structure, semantics and dependency rules |
| Explicit operations | State which operations are offered; enforce their preconditions, atomic result contract and protection policy |
| Validator | State root versions, exact profiles and checked layers; Schema alone does not prove complete conformance |

Stable Core is `3.0.0`. All six bundled optional profiles remain provisional `1.0.0-draft.1`. Supporting Core does not require implementing every profile or operation. The reference validator does check exact profiles it recognizes; a malformed known profile is not ignored merely because its status is stale.

## 2. Core, strict input and migration — 39 viewpoints

| ID | 入力または操作 | 期待結果 |
| --- | --- | --- |
| C01 | 空のtracks、harmony、lyricsと正しいtempo・meter | 有効な未完成文書 |
| C02 | コードなしのメロディー | 有効 |
| C03 | ノートなしの歌詞と空のalignments | 有効 |
| C04 | 同一IDをtrackとnoteに使用 | Core参照の前にID重複エラー |
| C05 | primaryMelodyTrackIdがclipを指す | 種別違いエラー |
| C06 | PPQ 6720、四分音符内の7音を960tick間隔で配置 | 丸めず有効 |
| C07 | PPQ 0または宣言と違う暗黙960換算 | 不正または実装不適合 |
| C08 | clip.start=960、note.start=−120 | onset=840として保持 |
| C09 | clip.start=0、note.start=−120 | 負の絶対開始エラー |
| C10 | 最後のゲートがclip末尾を越える | 短縮せず保持 |
| C11 | 同じ音高の二音が重なる | 別IDのまま両方保持 |
| C12 | 同tickで前音が終わり次音が始まる | noteOffを先に出す |
| C13 | enabled=falseのtrackまたはclip | 保存・検証し、発音しない |
| C14 | クリップの基準区間より後にノートが開始 | 絶対時刻が有効なら保持 |
| C15 | 各値は範囲内だが終端の加算がMAXを超える | 終端範囲エラー |
| C16 | Coreノートにvelocityを直接追加 | 未定義Core項目としてエラー |
| C17 | pitchとsoundSlotIdを同時指定、または両方なし | 構造エラー |
| C18 | 非GMのmidiNoteを持つ二種類のkick | 独立スロットとして保持 |
| C19 | 一音節を複数ノートへ割り付ける | 参照が正しければ有効 |
| C20 | labelだけのコードを通常表示する | 有効。構造化コードと誤認しない |
| C21 | labelだけのコードをcurrentなchordToneの基準にする | 必要な構造不足エラー |
| C22 | current相対指定の計算結果とnote.pitchが違う | 対応不一致エラー |
| C23 | 同じ不一致をstaleまたはunverifiedとして保持 | 警告。ノートを書き換えない |
| C24 | current既知profileで依存参照を記載し忘れる | dependenciesの不足エラー |
| C25 | 未知の名前空間または既知名前空間の未来版 | 共通外側を検証し、dataは未対応として保持 |
| C26 | staleだが既知profileの必須フィールドが欠ける | 構造エラー |
| C27 | 異なる二つの入力を持つ生成記録 | 入力を一つに潰さない |
| C28 | 存在しないprotectedNoteIdをcurrentで参照 | 参照エラー |
| C29 | 同じ表示対象へ二つのobjectColorsを指定 | 重複対象エラー |
| C30 | 未知拡張を含む文書を関連編集する | dataを保持し、未確認のcurrentを残さない |
| C31 | ランダム生成済みノートを読み直す | 再抽選しない |
| W01 | 重複JSONキー、BOM、不正UTF-8 | 入力時に拒否 |
| W02 | NaN、Infinity、非有限の数値 | 入力時に拒否 |
| W03 | 整数フィールドへ1.0、1e0、true | 入力または型検証で拒否 |
| W04 | 未知dataに高精度の数値 | 無損失を表明する書き手は丸めない |
| M01 | 2.3を標準モードで変換 | 内部ノートの意味を推測しない |
| M02 | サンプル規約解釈を明示して変換 | 適用した仮定を報告する |
| M03 | 原典アーカイブからsourceTextを取り出す | 元UTF-8バイト列とSHA256が一致する |
| M04 | 旧IDの衝突と曖昧な色参照 | 既知参照だけ変換し、曖昧なものを報告する |

## 3. Phrase, choices, protection and conversion — 30 viewpoints

| ID | Input or operation | Required result |
| --- | --- | --- |
| D201 | Supported Draft 1 source documents and preserved schema | Preserve their declared root on read, Core event meaning and opaque values. Historical check counts are not a new acceptance requirement or result |
| D202 | Draft-specific profile dispatch and an unsupported root version | Draft 1 treats the new namespaces as opaque; Draft 2 checks exact supported versions; reject an unsupported root version |
| D203 | Explicit Draft 1 to Draft 2 conversion and the reverse | Preserve Core events and unknown values; change only root version and required conservative statuses; reject newly recognized malformed payloads |
| D204 | A finite repeated/transposed template with a complete note map | Verify every stored onset, gate and target against independent expected values; never emit the template itself |
| D205 | Duplicate template, template-note or instance identity | Reject intrinsic ambiguity in every status; local IDs do not become Core identities |
| D206 | Missing, duplicate, extra, foreign or multiply owned mapped notes/clips | Require exact occurrence and clip-note coverage for current data; reject duplicate ownership in every status |
| D207 | Bounds, integer token kinds and computed phrase arithmetic | Reject invalid fields or current mismatches, including products and sums; do not clamp or wrap pitches |
| D208 | Pickups, tails, starts after the repeat period and same-pitch overlap | Retain the exact separate notes and gates, including across repeat and clip boundaries |
| D209 | Percussion template with a nonzero transpose and slot references | Preserve slot identity independently of transpose and output hints; validate direct slot references |
| D210 | Stale/unverified phrase correspondence and malformed known structure | Keep correspondence mismatches as warnings without changing Core; structural and intrinsic identity errors remain errors |
| D211 | New profile dependencies, including inactive choices and template slots | Cover every direct Core reference or use document scope; dependency-free empty metadata may use none |
| D212 | Shared clips among candidates, empty candidates and explicit null selection | Compare against the selected candidate's membership; common clips play once; null or silence disables the managed set |
| D213 | Selected/nonselected clip flags under a muted parent track | Validate clip.enabled independently from track.enabled; parent mute never hides an incorrect choice state |
| D214 | Duplicate choice identities or clip ownership across groups | Reject intrinsic ambiguity in every status; permit shared clips within one group |
| D215 | A stale choice whose declaration disagrees with Core | Warn and keep the stored Core events; loading does not select or repair candidates |
| D216 | Explicit phrase materialization | Return a copy with deterministic collision-checked IDs, specified note/map ordering and exact performance |
| D217 | Template times repeatCount exceeds max_notes | Reject before occurrence expansion; disclose this as a reference-operation limit, not a wire maximum |
| D218 | Invalid or conflicting materialization request | Refuse existing IDs, clips/instances, unsafe endpoints and unusable source profiles atomically |
| D219 | Materialization or selection changes Core dependencies | Invalidate other affected current claims, retain unrelated/stale data and preserve opaque numeric values/token kinds |
| D220 | Explicit candidate activation with stale groups or missing refs | Require all managed refs and complete resulting choice-profile consistency; fail atomically rather than repair unrelated groups |
| D221 | Candidate activation under parent mute or repetition of an already-current identical selection | Preserve parent mute and unmanaged objects; repeating that identical selection preserves unrelated claims. A different candidate ID with the same clip set can still invalidate dependencies on metadata |
| D222 | Candidate activation with protected note IDs | Apply the fixed protection set before/after; reject a changed effective-enabled state without partial output |
| D223 | Protected note identity or pitch/slot target changed | Fail even when a replacement has the same audible pitch/timing or a slot shares the same output hint |
| D224 | Protected absolute onset or gate changed, including parent moves | Fail changed musical coordinates; permit compensating local/parent moves that preserve the absolute coordinates |
| D225 | Protected inactive notes and changed parents/enabled flags | Check inactive notes too; compare effective enabled and musical fields rather than parent IDs or individual mute flags |
| D226 | Protection comparison with PPQ change, tempo change, empty/invalid lists or invalid documents | Refuse PPQ mismatch; do not treat tempo as a tick-field change; disclose an empty checked set; reject invalid comparison inputs |
| D227 | Generation protection with its after-list/process removed or edited | Take IDs only from the before document's exact supported current process; after edits cannot remove protection |
| D228 | Editing CLI output replacement and input path aliases | Require force for an existing destination; never overwrite an input through its own path, hard link or symbolic link |
| D229 | Editing operation with unsupported root/profile versions | Refuse interpretation and produce no partial document; do not treat a familiar namespace as supported by itself |
| D230 | Unknown finite numbers through conversion and successful/failed edits | Preserve exact values, integer/real token category and opaque array order; never mutate caller inputs |

## 4. Replacement and detachment — 20 viewpoints

| ID | Input or operation | Required result |
| --- | --- | --- |
| R101 | The established Draft 2 behavior and schema baseline | Preserve earlier musical behavior and exact retained Draft schemas while explicitly identifying the stable root. Historical counts and development artifact inventories are not claims for this release |
| R102 | Replace a template used by multiple instances with different repetitions and transpositions | Refresh every matching placement in one transaction and match independently authored after notes, maps and events |
| R103 | Surviving occurrence keys use custom existing Core IDs and lyric alignments | Keep their exact Core IDs, instance settings, clip metadata, parent state and lyric references |
| R104 | New or renamed source-note occurrences and ID collisions | Derive new IDs from occurrence identity; treat a rename as removal plus addition; reserve every original ID, including removed ones |
| R105 | Unrelated templates, placements, Core objects and both caller inputs | Preserve unrelated content and input objects; successful results are independent copies |
| R106 | Missing/mismatched template IDs or malformed replacement structure, local identities or slots | Reject the complete replacement atomically; validate integer token kinds before recognizing a no-op |
| R107 | Output count across all affected instances, exact limit and huge empty repetitions | Reject an excessive total before expansion; accept the exact limit and avoid enumerating empty repeats |
| R108 | A single affected instance produces an invalid pitch, note endpoint or clip span | Reject the entire operation, including when the failing placement is inactive |
| R109 | A removed Core note is referenced by a lyric alignment | Raise the dedicated referenced-note-removal refusal with useful diagnostics; preserve notes and lyrics in the original input |
| R110 | Fixed protected IDs during replacement, including a removed or inactive protected note | Reject changed protected snapshot fields before exposing a result; unchanged protected objects remain permitted |
| R111 | Core-changing or nontrivial metadata-only replacement | Conservatively invalidate affected other current claims while preserving payloads, numeric precision/token kinds and none/stale states |
| R112 | An identical validated replacement, including a noncanonical valid map order | Return a copy preserving dependencies, statuses and ordering; do not silently normalize the stored map |
| R113 | Detach one or several selected instance records | Remove only those records; retain templates, every Core object, ordering, lyrics and the original phrase dependencies/status |
| R114 | Detach a stale or unverified instance whose Core clip was edited manually | Retain the manual performance exactly and do not promote the phrase status after the link disappears |
| R115 | Duplicate, malformed or mixed existing/missing detach requests, or an empty request | Reject invalid requests atomically; an empty valid request is a copy without invalidation |
| R116 | Detachment changes metadata while other extensions contain opaque precise numbers | Invalidate other non-none current claims conservatively, preserve all payloads/token kinds, and enforce the fixed protection list |
| R117 | CLI replacement JSON input and output aliases of either source file | Use strict UTF-8 JSON; reject direct, hard-linked or symbolic output aliases of both OSTF source and replacement template |
| R118 | CLI creation, unrelated existing output and failed writes | Require force to replace an unrelated destination; validation, operation, protection, staging or publication failure before commit does not change either input or the final destination. Publication is the commit point; later output/cleanup failures and power-loss durability are outside this guarantee |
| R119 | CLI protected notes and before-process protection for replacement/detachment | Apply the input snapshot protection set; no output is exposed on violation and metadata invalidation cannot remove protection |
| R120 | Either new operation receives an unsupported root/profile version; replacement receives an outdated library | Refuse unsupported interpretation and stale/unverified replacement; detachment may preserve a supported outdated library |

## 5. Evidence and limits / 証拠の区別

The [coverage inventory](COVERAGE.md) locates declared fields and finite enum values in the examples. It is a static documentation inventory, not schema validation, cross-reference checking, operation execution, audio comparison, or product interoperability evidence. A valid musical example cannot demonstrate every rejection condition; the tables above and the full reference describe prohibited cases without distributing malformed files as ordinary songs.

An error prevents conformance at the checked layer. A warning such as stale correspondence or unknown metadata is not itself a format error. The CLI `--warnings-as-errors` option changes command success policy, not diagnostic severity; the reference CLI reports `valid` and `commandPassed` separately. See [reference implementation](REFERENCE_IMPLEMENTATION.md).

These conditions do not certify a composer, external DAW, plug-in, generator, identical instrument sound, or reproduction of a proprietary model. [Release readiness](RELEASE_READINESS.md) describes what has been prepared for publication.
