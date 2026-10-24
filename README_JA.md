# Open Song Timeline Format — OSTF 3.0.0

**作曲の意図と、現在採用している複数パートの演奏を交換する形式。** `.ostf` はUTF-8のJSONです。音高または打楽器の発音対象、発音位置、ゲートタイムを保存し、Coreにベロシティーは設けません。

[English](README.md) · [全網羅マニュアル](docs/COMPLETE_MANUAL.ja.md) · [パラメーターリファレンス](docs/PARAMETER_REFERENCE.ja.md) · [仕様](docs/FORMAT_SPECIFICATION.ja.md) · [サンプル索引](samples/INDEX.md)

## この配布物

- **Coreの正式版：`3.0.0`。** ファイル拡張子は `.ostf`。
- **標準の任意profile：6種類、各 `1.0.0-draft.1`。** profileの暫定状態とCoreの正式版は独立です。
- **全98ファイル。** 3.0.0の記述例60件、2.3移行元2件、日英のマニュアル・辞典・仕様、機械可読カタログ、Schema、参照コードを含みます。
- **全項目の所在を追跡可能。** [対応表](docs/COVERAGE.md)は、定義されたプロパティ・有限の列挙値とサンプル内のJSON Pointerを結び付けます。無限にある音楽や任意のベンダーJSONを列挙する意味ではありません。
- **動作検証は未実施。** この配布準備ではプロジェクトコード、validator、CLI、試験、DAW/MIDI再生を実行していません。対応表は記述内容の静的な収録確認です。

## 読む順番

| 目的 | 入口 |
| --- | --- |
| 小さなexporterを作る | [最小実装ガイド](docs/IMPLEMENTER_QUICKSTART.md)と[メロディー例04](samples/04_melody_only.ostf) |
| パラメーターの使い方を理解する | [全網羅マニュアル](docs/COMPLETE_MANUAL.ja.md) |
| 型・必須・範囲・列挙・条件を引く | [全網羅リファレンス](docs/PARAMETER_REFERENCE.ja.md)と[機械可読辞典](docs/PARAMETER_CATALOG.json) |
| 規範となる意味を実装する | [仕様本文](docs/FORMAT_SPECIFICATION.ja.md)と[3.0.0 Schema](schema/ostf-3.0.0.schema.json) |
| 機能ごとの完成したJSONを探す | [サンプル索引](samples/INDEX.md)と[サンプルカタログ](samples/catalog.json) |
| フレーズ反復・原型置換・候補選択を扱う | [profile補足](docs/OPTIONAL_PROFILES.md)と[明示操作ガイド](docs/OPERATIONS.md) |
| PythonのAPI・CLIを利用する | [参照実装](docs/REFERENCE_IMPLEMENTATION.md) |
| 2.3の文書を引き継ぐ | [移行ガイド](docs/MIGRATION_2_3_TO_3_0.md)と[原典](docs/SOURCE_ATTRIBUTION.md) |
| リリース内容を公開する | [リリース本文](RELEASE_NOTES.md)、[準備状況](docs/RELEASE_READINESS.md)、[LICENSE](LICENSE.md) |

## 設計の中心

Coreに保存した具体的なノート列が、現在の演奏です。読み込みだけでコードから伴奏を作り直したり、候補を選び直したり、templateと実体ノートを二重に発音したりしません。コードだけ、メロディーだけ、歌詞だけの未完成文書も表現できます。

関係を共有したいアプリは、相対音、生成入力・出力、表示、原典アーカイブ、再利用フレーズ、クリップ候補の任意profileを追加できます。独自アルゴリズムの設定は名前空間付きの拡張へ保存します。未知の内容は意味を推測せず保持し、編集で対応を保証できなくなった情報は `stale` / `unverified` にします。

楽器名は説明情報、`soundSlots[].midiNote` は出力先への任意ヒントです。プラグイン状態やMIDI機器の完全な再現を定義しません。ベロシティーや音源状態を持つDAWへの書出しでは、アダプターが補う方針を別途示します。

## ディレクトリとファイル数

| 範囲 | ファイル数 | 内容 |
| --- | ---: | --- |
| ルート | 12 | README日英、ライセンス、変更履歴、リリース本文、manifest、依存宣言、Python5本 |
| `docs/` | 18 | 仕様・マニュアル・辞典・参照資料・対応表 |
| `schema/` | 3 | 正式3.0.0と旧Draft 1/2 |
| `tools/` | 1 | パラメーター辞典の静的資料生成ツール |
| `samples/` 以下 | 64 | 主例60件、移行元2件、索引とカタログ |
| **合計** | **98** | ZIPの中にZIPや開発時の作業ファイルは含めない |

[PACKAGE_MANIFEST.json](PACKAGE_MANIFEST.json)に全ファイルのパス・サイズ・SHA-256を記録します。manifest自身のhashは自己参照を避けて含めません。旧Draft Schemaは参照readerの互換性のために同梱し、主サンプル60件はすべて3.0.0です。

## GitHubに一度でアップロードする

1. 配布ZIPを展開します。
2. GitHubの対象リポジトリで **Add file → Upload files** を開きます。
3. 展開した `OSTF_3_0_0_GitHub_Release` の**中身**をまとめてドラッグし、ルートのREADMEと各サブディレクトリの配置を確認してコミットします。
4. Releaseを作成するときは、タグの候補を `v3.0.0`、タイトルを `OSTF 3.0.0` とし、[RELEASE_NOTES.md](RELEASE_NOTES.md)の本文を使用できます。必要なら配布ZIPをRelease assetとして添付します。

GitHubのブラウザーuploadは一度に100ファイルまで、各ファイル25 MiBまでです。本配布物は98ファイルで収まります。[GitHub公式案内](https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository)（2026-10-24参照）。ZIPをリポジトリへ置くだけでは、その中のファイルは自動展開されません。既存の2.3を残す場合は、3.0用のリポジトリまたは意図した配置先へアップロードしてください。本資料の作成ではGitHubへのアップロード・タグ作成・公開は行っていません。

## ライセンス

仕様・Schema・説明資料・サンプルは **CC BY 4.0**、参照プログラムと実行コード例は **MIT**。適用範囲、帰属、原典の扱いは[LICENSE.md](LICENSE.md)に記載します。既存製品の名称は設計研究の出典を示し、対応・提携・認証を意味しません。
