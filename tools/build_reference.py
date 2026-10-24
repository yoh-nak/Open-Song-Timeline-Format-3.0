#!/usr/bin/env python3
"""Build bilingual documentation/catalog from schema text; never validate OSTF data.

This is a documentation-authoring tool. It imports no OSTF project module and
does not execute the reader, editor, schema validator or test suite.
"""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'schema' / 'ostf-3.0.0.schema.json'
DOCS = ROOT / 'docs'

DEFINITIONS = {
    'root': ('文書全体。11個のrootキーはすべて必須。', 'Complete document; all eleven root members are required.'),
    'id': ('IDの字句形式。Core全体での一意性と、profile内の局所IDの一意性は別の意味規則。', 'ID lexical form; Core-wide and profile-local uniqueness are separate semantic rules.'),
    'nonnegative': ('非負の整数tick・回数添字。', 'Nonnegative integer ticks or occurrence indices.'),
    'positive': ('正の整数tick・回数。', 'Positive integer ticks or counts.'),
    'signed': ('符号付き整数。ノートの局所開始位置に使用。', 'Signed integer, used for note-local start positions.'),
    'pitch': ('半音単位の音高番号。60=C4、69=A4。', 'Semitone pitch number; 60 is C4 and 69 is A4.'),
    'ref': ('Coreオブジェクトへの型付き参照。typeとidの両方が一致する必要がある。', 'Typed Core reference; both kind and ID must match.'),
    'range': ('曲全体のtick座標による区間。終了位置の加算にも上限を適用する。', 'Range on the global tick timeline; the computed endpoint is also bounded.'),
    'spelledPitchClass': ('綴りを持つ音名。オクターブを含まず、異名同音の綴りを保持する。', 'Spelled pitch class without octave; enharmonic spelling is retained.'),
    'song': ('曲名と主旋律の指定。未命名の曲には空のtitleを使用できる。', 'Song title and primary-melody designation; an unnamed song may have an empty title.'),
    'section': ('曲構成の区間。隙間は許すが区間同士は重ならない。', 'Song-structure section; gaps are allowed but sections do not overlap.'),
    'tempo': ('そのtick以後のテンポ。BPMは拍子によらず四分音符毎分。', 'Tempo from this tick onward, always measured in quarter notes per minute.'),
    'meter': ('そのtick以後の拍子。変更点を暗黙の小節境界へ移動しない。', 'Meter from this tick onward; a reader does not move it to an inferred bar boundary.'),
    'timeline': ('曲構成、テンポ変更、拍子変更の配列。', 'Section, tempo-change and meter-change arrays.'),
    'chord': ('和音の意味情報。labelだけでも有効で、演奏ボイシングを生成しない。', 'Harmonic meaning; a label-only chord is allowed and does not generate a performed voicing.'),
    'scale': ('音階の意味情報。Coreノートの使用可能音を制限しない。', 'Scale meaning; it does not restrict the pitches permitted in Core notes.'),
    'harmony': ('和音と音階の配列。演奏はCoreノートとして別に保存する。', 'Chord and scale arrays; adopted performances are stored separately as Core notes.'),
    'instrument': ('楽器の表示情報。プラグイン状態や音源を指定する契約ではない。', 'Instrument description, not a plug-in-state or sound-engine contract.'),
    'note': ('発音対象、局所開始位置、ゲート長。Coreとphrase templateで同じ構造を使うがID範囲は異なる。', 'Target, local onset and gate duration; Core and phrase templates share this shape but have different ID scopes.'),
    'clip': ('トラック上の配置・編集単位。durationはノートを切るマスクではない。', 'Placement/editing unit within a track; duration does not truncate its notes.'),
    'track': ('名前、役割、楽器説明、クリップを持つ演奏パート。配列順は表示順。', 'Performance part with name, role, instrument description and clips; array order is display order.'),
    'soundSlot': ('打楽器の発音先。IDが同一性を持ち、MIDI番号やroleは同一性ではない。', 'Percussion target; its ID establishes identity, not its MIDI hint or role.'),
    'lyricDocument': ('歌詞文書の識別と補助情報。', 'Lyric-document identity and auxiliary metadata.'),
    'lyricPhrase': ('表示用の歌詞フレーズ。分割単位の連結と同じ文字列である必要はない。', 'Displayed lyric phrase; it need not equal the concatenation of its units.'),
    'lyricUnit': ('歌詞の分割・対応づけの単位。', 'Lyric unit used for segmentation and note alignment.'),
    'lyricAlignment': ('歌詞単位とCoreノートの順序付き多対多対応。', 'Ordered many-to-many association between lyric units and Core notes.'),
    'lyrics': ('歌詞文書、フレーズ、単位、対応の四配列。', 'Four arrays for lyric documents, phrases, units and alignments.'),
    'sha256': ('小文字16進数64桁のSHA-256値。', 'SHA-256 digest as 64 lowercase hexadecimal digits.'),
    'resource': ('生成素材などへの参照。読込時の取得・実行・音声再生指示ではない。', 'Reference to source material; loading does not fetch, execute or play it.'),
    'dependencies': ('拡張が依存するCoreの範囲。二つのoneOf構造で三種類のscopeを表す。', 'Core dependency scope; two oneOf shapes represent three scope values.'),
    'extension': ('既知・未知のすべての拡張に共通する閉じたenvelope。', 'Closed common envelope for every known or unknown extension.'),
    'relativeAssignment': ('Coreの有音高ノートと、和音・音階の構成音との対応。', 'Relationship between one pitched Core note and a chord or scale interval.'),
    'relativeData': ('相対音高の対応一覧。読込時にCoreを書き換えない。', 'Relative-pitch assignments; they do not rewrite Core on load.'),
    'generator': ('生成器の識別子と版。アルゴリズムの再現を保証するものではない。', 'Generator identifier and version; not a guarantee of algorithm reproduction.'),
    'generationInput': ('一つの入力役割、Core参照、任意の読取範囲。', 'One input role, Core reference and optional context-read range.'),
    'generationProcess': ('生成入力・出力・保護ノートなどの関係記録。', 'Record of generation inputs, outputs and protected-note relationships.'),
    'generationData': ('複数の生成工程の記録。', 'Records of generation processes.'),
    'color': ('RGB色。#に続く大文字または小文字の16進数6桁。', 'RGB color: # followed by six uppercase or lowercase hexadecimal digits.'),
    'roleDefinition': ('表示用の独自セクション役割の定義。', 'Custom section-role definition for presentation.'),
    'roleColorMap': ('任意のrole文字列からRGB色への辞書。', 'Dictionary from open role strings to RGB colors.'),
    'customRoleColorMap': ('定義済み独自role IDからRGB色への辞書。', 'Dictionary from declared custom-role IDs to RGB colors.'),
    'objectColor': ('型付きCore参照に対する個別色。', 'Object-specific color for a typed Core reference.'),
    'appearanceData': ('独自役割、セクションへの割当、色の表示情報。演奏には影響しない。', 'Custom roles, section assignments and presentation colors; no performance effect.'),
    'legacyData': ('2.3原文とSHA-256、移行記録の保存。Coreを書き戻す指示ではない。', 'Archive of 2.3 source text, its SHA-256 and a conversion report; not a command to restore Core.'),
    'extensions': ('namespaceをキーに持つ拡張辞書。正確なnamespaceと版でpayload構造を選ぶ。', 'Namespace-keyed extension dictionary; exact namespace and version select the payload structure.'),
    'phraseTemplate': ('再利用する具体的ノート列。durationは反復周期。', 'Reusable concrete source notes; duration is the repeat period.'),
    'phraseNoteMapping': ('source noteと反復番号から、実体化済みCoreノートへの対応。', 'Mapping from source-note identity and repetition index to a realized Core note.'),
    'phraseInstance': ('templateと一つのCore clipの完全対応。', 'Complete correspondence between a template and one Core clip.'),
    'phraseLibraryData': ('具体的phrase templatesと実体化済みinstances。読込時に展開しない。', 'Concrete phrase templates and already realized instances; never expanded on load.'),
    'clipCandidate': ('候補の局所IDと、その候補で有効にするCore clips。', 'Candidate-local identity and the Core clips enabled for that choice.'),
    'clipChoiceGroup': ('候補群と保存済み選択。Coreのenabled状態との一致を記録する。', 'Candidate group and saved selection, corresponding to stored Core enabled states.'),
    'clipChoicesData': ('独立したクリップ選択グループの配列。', 'Array of independent clip-choice groups.'),
}

# Names shared by several records have their common meaning here; contextual
# meanings and identity scopes are supplied by the precise overrides below.
COMMON = {
 'id': ('このレコードのID。適用される一意性の範囲は型の説明を参照。', 'Record ID; see the type description for its uniqueness scope.'),
 'name': ('表示名。IDの代用にはしない。', 'Display name; not a substitute for identity.'),
 'title': ('表示用の題名。', 'Display title.'),
 'start': ('開始tick。座標系はこの型の説明を参照。', 'Start tick; the coordinate system depends on the record type.'),
 'duration': ('正の長さtick。終了位置の加算にも意味上の上限がある。', 'Positive tick length; computed endpoints have semantic bounds too.'),
 'role': ('用途・役割を表す文字列。固定enumではない。', 'Open string describing function or role; not a fixed enumeration.'),
 'enabled': ('省略時は意味上true。trackとclipが両方trueのときのみノートが有効。', 'Semantically true when absent; notes are active only when both track and clip are enabled.'),
 'pitch': ('0〜127の半音番号。60=C4。soundSlotIdとの二者択一。', 'Semitone number 0–127; 60=C4; mutually exclusive with soundSlotId.'),
 'soundSlotId': ('Core soundSlotのID。pitchとの二者択一。', 'ID of a Core soundSlot; mutually exclusive with pitch.'),
 'notes': ('開始位置順の具体的ノート配列。同時刻では配列順を保持。', 'Concrete notes in nondecreasing onset order; retain array order at equal starts.'),
 'version': ('この対象の版。root版・profile版・生成器版は別の識別子。', 'Version of this object; root, profile and generator versions are distinct identifiers.'),
 'intervals': ('根音または主音からの半音差。0を含み、厳密昇順・重複なし。', 'Semitone distances from root or tonic; include 0, strictly increasing and duplicate-free.'),
 'text': ('表示文字列。発音表記はpronunciationに分離する。', 'Display text; pronunciation is a separate annotation.'),
 'pronunciation': ('発音の補助文字列。音素体系や歌唱エンジンは規定しない。', 'Pronunciation annotation; no phoneme alphabet or singing engine is standardized.'),
 'at': ('曲全体の変更tick。各変更配列は0から始まり厳密昇順。', 'Global change tick; each change map begins at 0 and increases strictly.'),
 'color': ('個別RGB色。', 'Object-specific RGB color.'),
 'ref': ('型付きCore参照。', 'Typed reference to a Core object.'),
 'noteId': ('対応先CoreノートのID。', 'Target Core note ID.'),
 'templateId': ('同じphrase-library内のtemplate ID。Core IDではない。', 'Template ID within this phrase library, not a Core ID.'),
 'clipId': ('対応するCore clipのID。', 'ID of the corresponding Core clip.'),
}

SPECIFIC = {
 ('root','format'): ('形式識別子。正確にOSTF。', 'Exact format identifier OSTF.'),
 ('root','version'): ('Core wire版。正確に3.0.0。', 'Exact Core wire version 3.0.0.'),
 ('root','ppq'): ('四分音符あたりの整数tick数。推奨960だが宣言値を使用する。', 'Integer ticks per quarter note; 960 is recommended but the declared value governs.'),
 ('root','song'): ('曲情報。', 'Song metadata.'),
 ('root','timeline'): ('セクション・テンポ・拍子。', 'Sections, tempo and meter maps.'),
 ('root','harmony'): ('和音・音階の意味情報。', 'Chord and scale meaning.'),
 ('root','tracks'): ('表示順を保持する演奏トラック配列。', 'Performance tracks; preserve display order.'),
 ('root','soundSlots'): ('打楽器の発音先一覧。', 'Percussion-target definitions.'),
 ('root','lyrics'): ('歌詞とノートへの対応。', 'Lyrics and their note alignments.'),
 ('root','resources'): ('参照素材の一覧。自動取得しない。', 'Referenced source material; never fetched automatically.'),
 ('root','extensions'): ('標準profileと独自データのnamespace辞書。', 'Namespace dictionary of standard profiles and vendor data.'),
 ('ref','type'): ('参照先のCoreオブジェクト種別。', 'Kind of the referenced Core object.'),
 ('ref','id'): ('typeで指定した種別のCore ID。', 'Core ID of the kind selected by type.'),
 ('spelledPitchClass','step'): ('自然音の文字名A〜G。', 'Natural-note letter A through G.'),
 ('spelledPitchClass','alter'): ('半音単位の変化量。-2から2。', 'Chromatic alteration in semitones, from -2 through 2.'),
 ('song','primaryMelodyTrackId'): ('主旋律として指定する既存Core trackのID。', 'Existing Core track designated as the primary melody.'),
 ('section','start'): ('曲全体のセクション開始tick。', 'Global start tick of the section.'),
 ('section','duration'): ('セクションの区間長。区間端でノートを切らない。', 'Section span; its endpoint does not cut notes.'),
 ('tempo','bpm'): ('四分音符毎分。0より大きく1000以下の有限数。', 'Finite quarter notes per minute, greater than 0 and at most 1000.'),
 ('meter','numerator'): ('拍子の分子。', 'Meter numerator.'),
 ('meter','denominator'): ('拍子の分母。列挙された2の累乗だけを使用。', 'Meter denominator; only the enumerated powers of two.'),
 ('timeline','sections'): ('非重複・開始位置順の構成区間。空・隙間を許す。', 'Nonoverlapping sections ordered by start; empty arrays and gaps are allowed.'),
 ('timeline','tempoChanges'): ('tick 0から始まるテンポの区分一定変更列。', 'Piecewise-constant tempo map beginning at tick 0.'),
 ('timeline','meterChanges'): ('tick 0から始まる拍子変更列。', 'Meter-change map beginning at tick 0.'),
 ('chord','label'): ('必須の空でない表示コード名。非構造的な文字列だけでも有効。', 'Required nonempty chord label; label-only harmony is allowed.'),
 ('chord','root'): ('綴りを保持する根音。intervalsと同時に指定。', 'Spelled root; present together with intervals.'),
 ('chord','bass'): ('任意の綴り付きベース音名。低音ノートを生成しない。', 'Optional spelled bass pitch class; does not generate a bass note.'),
 ('scale','label'): ('任意の表示用音階名。', 'Optional scale label.'),
 ('scale','tonic'): ('綴りを保持する主音。', 'Spelled tonic.'),
 ('harmony','chords'): ('開始位置順の和音区間。重なりを許す。', 'Chord contexts ordered by start; overlap is allowed.'),
 ('harmony','scales'): ('開始位置順の音階区間。重なりを許す。', 'Scale contexts ordered by start; overlap is allowed.'),
 ('instrument','family'): ('任意の楽器群の説明。固定分類ではない。', 'Optional open description of an instrument family.'),
 ('note','id'): ('Coreでは文書全体で一意。template内ではそのtemplateだけで一意。', 'Core notes are unique document-wide; source-note IDs are local to one template.'),
 ('note','start'): ('親clipまたはtemplateの開始に対する符号付きtick。', 'Signed tick offset from the parent clip or template start.'),
 ('note','duration'): ('発音を保持するゲート長。音源のrelease尾部や記譜音価ではない。', 'Gate length; distinct from synthesizer release tails and notated duration.'),
 ('clip','start'): ('曲全体の配置開始tick。', 'Global placement start tick.'),
 ('clip','duration'): ('配置・編集用の参照区間長。pickup・tailを切らない。', 'Placement/edit reference span; does not truncate pickups or tails.'),
 ('track','instrument'): ('任意の楽器表示情報。', 'Optional instrument-description object.'),
 ('track','clips'): ('開始位置順のclip配列。重なり・同時開始を許す。', 'Clips ordered by start; overlap and equal starts are allowed.'),
 ('soundSlot','midiNote'): ('出力変換の任意のヒント。GM準拠・同一性の宣言ではない。', 'Optional output-mapping hint; does not assert GM conformance or identity.'),
 ('lyricDocument','language'): ('補助的な言語文字列。形式は固定しない。', 'Auxiliary language string without a mandated code format.'),
 ('lyricPhrase','documentId'): ('所属するCore lyricDocumentのID。', 'Parent Core lyricDocument ID.'),
 ('lyricUnit','phraseId'): ('所属するCore lyricPhraseのID。', 'Parent Core lyricPhrase ID.'),
 ('lyricPhrase','start'): ('任意のグローバル開始tick。durationと同時に指定。', 'Optional global start tick, supplied together with duration.'),
 ('lyricUnit','start'): ('任意のグローバル開始tick。durationと同時に指定。', 'Optional global start tick, supplied together with duration.'),
 ('lyricPhrase','duration'): ('任意の区間長。startと同時に指定。', 'Optional timed span, supplied together with start.'),
 ('lyricUnit','duration'): ('任意の区間長。startと同時に指定。', 'Optional timed span, supplied together with start.'),
 ('lyricAlignment','unitIds'): ('空でなく重複のない、順序付きCore lyricUnit ID列。', 'Nonempty duplicate-free ordered Core lyricUnit IDs.'),
 ('lyricAlignment','noteIds'): ('空でなく重複のない、順序付きCore note ID列。', 'Nonempty duplicate-free ordered Core note IDs.'),
 ('lyrics','documents'): ('歌詞文書配列。', 'Lyric-document array.'),
 ('lyrics','phrases'): ('歌詞フレーズ配列。', 'Lyric-phrase array.'),
 ('lyrics','units'): ('歌詞単位配列。', 'Lyric-unit array.'),
 ('lyrics','alignments'): ('歌詞単位とノートの対応配列。', 'Lyric-unit/note alignment array.'),
 ('resource','kind'): ('参照素材の種別。再生動作は指定しない。', 'Kind of referenced material; not a playback operation.'),
 ('resource','uri'): ('空でない参照文字列。読込時には解決・取得しない。', 'Nonempty reference string; not resolved or fetched on load.'),
 ('resource','sha256'): ('参照素材に対する任意のSHA-256。照合は明示的操作。', 'Optional digest of referenced material; comparison is an explicit operation.'),
 ('dependencies','scope'): ('document=Core全体、none=Core依存なし、objects=明示参照。', 'document means whole Core; none means no Core dependency; objects means explicit refs.'),
 ('dependencies','refs'): ('objects時に必須の空でない、重複なし型付き参照列。', 'Nonempty duplicate-free typed references, required for objects scope.'),
 ('extension','status'): ('現在文書との関係の状態。規格の成熟度や再生のon/offではない。', 'Relationship status against this document, not specification maturity or playback on/off.'),
 ('extension','dependencies'): ('Coreへの依存宣言。親の移動・無効化による影響も含む。', 'Core dependency declaration, including effects inherited from parent movement or disabling.'),
 ('extension','data'): ('未知profileでは任意JSON。既知の正確な版では各payload構造に従う。', 'Any JSON for unknown profiles; exact known versions use the corresponding payload schema.'),
 ('relativeAssignment','basis'): ('chordToneは和音構成音、scaleDegreeは音階構成音。', 'chordTone selects a chord interval; scaleDegree selects a scale interval.'),
 ('relativeAssignment','contextId'): ('basisに応じたCore chordまたはscaleのID。', 'Core chord or scale ID selected according to basis.'),
 ('relativeAssignment','anchorPitch'): ('オクターブを含む実際の根音・主音番号。', 'Actual octave-specific root or tonic pitch.'),
 ('relativeAssignment','index'): ('intervals配列内の1始まり位置。コード名称の度数番号ではない。', 'One-based position within intervals, not a chord-symbol degree label.'),
 ('relativeAssignment','chromaticOffset'): ('選んだ構成音への半音単位の補正。', 'Semitone adjustment added to the selected interval.'),
 ('relativeData','assignments'): ('Core有音高ノートごとに最大1件の対応。', 'At most one assignment for each pitched Core note.'),
 ('generator','id'): ('空でない生成器識別文字列。Core IDの字句制限は適用しない。', 'Nonempty generator identifier; the Core ID lexical restriction does not apply.'),
 ('generationInput','readRange'): ('生成時に読んだグローバル範囲。出力区間とは別。', 'Global context-read range, distinct from the output span.'),
 ('generationProcess','id'): ('このgeneration-context内で一意な工程ID。', 'Process ID unique within this generation-context extension.'),
 ('generationProcess','generator'): ('生成器の識別・版情報。', 'Generator identifier/version object.'),
 ('generationProcess','inputs'): ('空も複数も許す、役割付きの入力列。', 'Input records with roles; empty or multiple inputs are allowed.'),
 ('generationProcess','outputs'): ('空でない型付きCore出力参照列。', 'Nonempty typed references to Core outputs.'),
 ('generationProcess','targetRange'): ('変更を要求したグローバル範囲。pickupやtailを切らない。', 'Requested global modification range; does not truncate pickups or tails.'),
 ('generationProcess','protectedNoteIds'): ('重複なしCore note ID列。操作前に比較対象を固定する。', 'Duplicate-free Core note IDs; the comparison set is fixed before the operation.'),
 ('generationProcess','vendorExtension'): ('同一文書内の別拡張namespace。current時はdocument依存が必須。', 'Another extension namespace in this document; current data requires document scope.'),
 ('generationData','processes'): ('工程記録配列。', 'Generation-process records.'),
 ('roleDefinition','id'): ('appearance profile内で一意な独自role ID。', 'Custom-role ID unique within the appearance profile.'),
 ('roleDefinition','baseRole'): ('任意の基本role文字列。', 'Optional base-role string.'),
 ('objectColor','target'): ('色を指定するCore対象の型付き参照。', 'Typed Core target receiving the color.'),
 ('appearanceData','roleDefinitions'): ('独自roleの定義配列。', 'Custom-role definitions.'),
 ('appearanceData','sectionRoleAssignments'): ('Core section IDをキー、独自role IDを値とする辞書。', 'Map from Core section IDs to custom-role IDs.'),
 ('appearanceData','appearance'): ('role・独自role・対象別の色指定。', 'Colors by role, custom role and individual target.'),
 ('appearanceData','roleColors'): ('任意のrole文字列に対応する色辞書。', 'Color dictionary keyed by open role strings.'),
 ('appearanceData','customRoleColors'): ('定義した独自role IDに対応する色辞書。', 'Color dictionary keyed by declared custom-role IDs.'),
 ('appearanceData','objectColors'): ('対象別の色指定配列。', 'Object-specific color records.'),
 ('legacyData','sourceVersion'): ('保存した原文の版。正確に2.3.0。', 'Archived source version, exactly 2.3.0.'),
 ('legacyData','sourceSha256'): ('sourceTextのUTF-8バイト列に対するSHA-256。', 'SHA-256 of sourceText encoded as UTF-8.'),
 ('legacyData','sourceText'): ('元の2.3 JSON全文。空白と文字列を含む原文を保存。', 'Complete original 2.3 JSON text, retaining source whitespace and strings.'),
 ('legacyData','conversionReport'): ('移行の対応・損失等の記録。内部項目はこのprofileでは固定しない。', 'Migration mapping/loss report; this profile does not fix its internal members.'),
 ('phraseTemplate','id'): ('このlibrary内で一意なtemplate ID。Core IDではない。', 'Template ID unique within this library, not a Core ID.'),
 ('phraseTemplate','duration'): ('正の反復周期tick。ノートのゲートを切らない。', 'Positive repeat period in ticks; does not truncate note gates.'),
 ('phraseNoteMapping','templateNoteId'): ('参照template内のsource note ID。', 'Source-note ID local to the referenced template.'),
 ('phraseNoteMapping','repeatIndex'): ('0始まりの反復番号。current時はrepeatCount未満。', 'Zero-based repetition index; below repeatCount for current data.'),
 ('phraseInstance','id'): ('このlibrary内で一意なinstance ID。', 'Instance ID unique within this library.'),
 ('phraseInstance','repeatCount'): ('有限の反復回数。空templateでも正整数。', 'Finite repeat count, positive even for an empty template.'),
 ('phraseInstance','transpose'): ('有音高ノートの半音移調量。打楽器slotは変更しない。', 'Semitone transposition for pitched notes; percussion slots are unchanged.'),
 ('phraseInstance','noteMap'): ('全source note×反復と全clip noteを一対一に結ぶ対応。', 'Complete one-to-one mapping of source-note/repetition occurrences and clip notes.'),
 ('phraseLibraryData','templates'): ('再利用する具体的phrase配列。', 'Reusable concrete phrase templates.'),
 ('phraseLibraryData','instances'): ('実体化済みCore clipsへの対応配列。', 'Correspondences to already realized Core clips.'),
 ('clipCandidate','id'): ('所属group内で一意なcandidate ID。', 'Candidate ID unique within its group.'),
 ('clipCandidate','clipIds'): ('候補が使う重複なしCore clip ID列。空候補も許す。', 'Duplicate-free Core clip IDs used by the candidate; an empty candidate is allowed.'),
 ('clipChoiceGroup','id'): ('このclip-choices内で一意なgroup ID。', 'Group ID unique within this clip-choices extension.'),
 ('clipChoiceGroup','candidates'): ('1件以上の候補。', 'One or more candidates.'),
 ('clipChoiceGroup','selectedCandidateId'): ('選択した局所candidate ID、または未選択を表すnull。省略不可。', 'Selected local candidate ID, or null for no selection; the member is required.'),
 ('clipChoicesData','groups'): ('選択グループ配列。別group間のclip管理範囲は重ねない。', 'Choice groups; managed clip sets do not overlap across groups.'),
}

MAP_KEYS = ('$defs', 'properties', 'patternProperties', 'dependentSchemas')
SINGLE_KEYS = ('items', 'contains', 'additionalProperties', 'propertyNames', 'not', 'if', 'then', 'else', 'unevaluatedProperties')
ARRAY_KEYS = ('allOf', 'anyOf', 'oneOf', 'prefixItems')
BRANCH_KEYS = ('oneOf', 'anyOf', 'allOf', 'if', 'then', 'else', 'dependentRequired', 'dependentSchemas')


def esc(token):
    return token.replace('~', '~0').replace('/', '~1')


def schema_nodes(node, pointer='#'):
    yield pointer, node
    if not isinstance(node, dict):
        return
    for key in MAP_KEYS:
        for name, child in node.get(key, {}).items():
            yield from schema_nodes(child, pointer + '/' + key + '/' + esc(name))
    for key in SINGLE_KEYS:
        if key in node and isinstance(node[key], (dict, bool)):
            yield from schema_nodes(node[key], pointer + '/' + key)
    for key in ARRAY_KEYS:
        for i, child in enumerate(node.get(key, [])):
            yield from schema_nodes(child, pointer + '/' + key + '/' + str(i))


def owner(pointer):
    parts = pointer.split('/')
    return parts[2] if len(parts) > 2 and parts[1] == '$defs' else 'root'


def description(pointer, name):
    kind = owner(pointer)
    if kind == 'extensions':
        return ('このnamespaceの任意profile。既知payloadを解釈する版は1.0.0-draft.1。',
                'Optional profile at this namespace; the known payload version is exactly 1.0.0-draft.1.')
    return SPECIFIC.get((kind, name), COMMON.get(name, ('型と制約は下記の定義に従う。', 'Follow the type and constraints specified below.')))


def compact(value):
    return json.dumps(value, ensure_ascii=False, separators=(',', ':'))


def code(value):
    return '`' + compact(value).replace('|', '\\|') + '`'


def effective(schema, node):
    result = dict(node)
    seen = set()
    while '$ref' in result and result['$ref'] not in seen:
        ref = result.pop('$ref')
        seen.add(ref)
        target = schema
        for token in ref[2:].split('/'):
            target = target[token.replace('~1', '/').replace('~0', '~')]
        result = {**target, **result}
    return result


def summarize(schema, node, lang=0):
    if isinstance(node, bool):
        return str(node).lower()
    if not node:
        return '任意のJSON値' if lang == 0 else 'Any JSON value'
    resolved = effective(schema, node)
    parts = []
    if '$ref' in node:
        name = node['$ref'].rsplit('/', 1)[-1]
        parts.append('[' + name + '](#def-' + name.lower() + ')')
    if 'type' in resolved:
        parts.append(code(resolved['type']))
    for key in ('const', 'enum', 'minimum', 'exclusiveMinimum', 'maximum', 'exclusiveMaximum',
                'minLength', 'maxLength', 'pattern', 'minItems', 'maxItems', 'uniqueItems',
                'minContains', 'maxContains', 'default'):
        if key in resolved:
            parts.append(key + '=' + code(resolved[key]))
    if 'items' in resolved:
        parts.append('items: ' + summarize(schema, resolved['items'], lang))
    if 'contains' in resolved:
        parts.append('contains=' + code(resolved['contains']))
    if resolved.get('additionalProperties') is False:
        parts.append('追加キー禁止' if lang == 0 else 'closed object')
    elif isinstance(resolved.get('additionalProperties'), dict):
        parts.append('additionalProperties: ' + summarize(schema, resolved['additionalProperties'], lang))
    if 'propertyNames' in resolved:
        parts.append('propertyNames=' + code(resolved['propertyNames']))
    if 'not' in resolved:
        parts.append('not=' + code(resolved['not']))
    for key in ('oneOf', 'anyOf', 'allOf', 'dependentRequired'):
        if key in resolved:
            parts.append(key + ('（下記構造規則）' if lang == 0 else ' (structural rules below)'))
    return '; '.join(parts) or ('下記構造規則を参照' if lang == 0 else 'See structural rules below')


def path_add(path, name):
    if name.replace('_', '').isalnum() and not name[0].isdigit():
        return path + '.' + name
    return path + '[' + compact(name) + ']'


def instance_locations(schema):
    locations = {}
    def walk(node, pointer, path, stack=()):
        locations.setdefault(pointer, set()).add(path)
        if not isinstance(node, dict):
            return
        if '$ref' in node:
            ref = node['$ref']
            if ref not in stack:
                target = schema
                for token in ref[2:].split('/'):
                    target = target[token.replace('~1', '/').replace('~0', '~')]
                walk(target, ref, path, stack + (ref,))
        for name, child in node.get('properties', {}).items():
            walk(child, pointer + '/properties/' + esc(name), path_add(path, name), stack)
        if isinstance(node.get('items'), dict):
            walk(node['items'], pointer + '/items', path + '[*]', stack)
        if isinstance(node.get('additionalProperties'), dict):
            walk(node['additionalProperties'], pointer + '/additionalProperties', path + '[*]', stack)
        if isinstance(node.get('propertyNames'), dict):
            walk(node['propertyNames'], pointer + '/propertyNames', path + '.<key>', stack)
        if isinstance(node.get('contains'), dict):
            walk(node['contains'], pointer + '/contains', path + '[*]', stack)
        for key in ('oneOf', 'anyOf', 'allOf'):
            for i, child in enumerate(node.get(key, [])):
                walk(child, pointer + '/' + key + '/' + str(i), path, stack)
        for key in ('if', 'then', 'else', 'not'):
            if isinstance(node.get(key), dict):
                walk(node[key], pointer + '/' + key, path, stack)
    walk(schema, '#', '$')
    return {key: sorted(value) for key, value in locations.items()}


def required_text(parent, field, lang):
    if field in parent.get('required', []):
        base = '必須' if lang == 0 else 'required'
    else:
        base = '任意' if lang == 0 else 'optional'
    dependencies = [key for key, values in parent.get('dependentRequired', {}).items() if field in values]
    if dependencies:
        base += ('；' + '、'.join(dependencies) + 'がある場合は必須') if lang == 0 else ('; required when ' + ', '.join(dependencies) + ' is present')
    if field in ('pitch', 'soundSlotId') and 'oneOf' in parent:
        base = 'pitch/soundSlotIdの一方だけ必須' if lang == 0 else 'exactly one of pitch/soundSlotId required'
    return base


SEMANTIC_ROWS = [
 ('2', 'UTF-8、BOM禁止、重複キー・非有限値・孤立surrogate禁止。整数は整数tokenで保存。', 'Strict UTF-8; no BOM, duplicate keys, nonfinite values or unpaired surrogates; integer fields require integer tokens.'),
 ('2.3 / 9.3', '未知dataの数値精度とinteger/real token区別を保持。未知のprofile版は既知payload schemaで検査しない。', 'Preserve opaque numeric precision and integer/real token category; never apply a known payload schema to an unknown version.'),
 ('3.1 / 3.4 / 6.3', '開始・長さだけでなく加算・乗算したendpointもMAX以内。絶対開始は非負。', 'Computed sums/products and endpoints, not only operands, must fit MAX; absolute onsets are nonnegative.'),
 ('3.2 / 3.3', 'Core ID全体の一意性、参照先の種別、一意性が局所のprofile IDとの区別。', 'Core-wide unique IDs, correct reference kinds, and distinct local profile identity scopes.'),
 ('4.2', 'sectionsは開始順・非重複。テンポと拍子は0開始・厳密昇順。', 'Sections are start-ordered and nonoverlapping; tempo and meter maps begin at 0 and increase strictly.'),
 ('5', 'harmonyは開始順。intervalsは厳密昇順。label、bass、scaleからノートを生成しない。', 'Harmony arrays are start-ordered; intervals strictly increase; labels, bass and scales do not generate notes.'),
 ('6', 'clipとnoteの開始順、同時刻での配列順、pickup・tail・重複音の保持。clip長は切断マスクではない。', 'Ordered clips/notes, retained equal-start order and pickups/tails/overlaps; clip duration is not a truncation mask.'),
 ('6.4', '実効enabledはtrack AND clip。同tickでoffがonより前、同種はnote ID辞書順。', 'Effective enabled is track AND clip; off precedes on at a shared tick, then note IDs order equal event kinds.'),
 ('7', 'soundSlotの同一性をMIDI番号で置き換えない。resourceを読込時に取得・実行しない。', 'MIDI hints do not replace sound-slot identity; loading does not fetch or execute resources.'),
 ('8', '歌詞の文書・フレーズ・ノート参照、グローバル時刻、順序付き多対多の対応。', 'Typed lyric/document/note references, global lyric timing, and ordered many-to-many alignments.'),
 ('9', 'currentの参照は解決が必要。stale/unverifiedでも既知payloadの構造不正はエラー。', 'Current references must resolve; stale/unverified status does not excuse malformed known payloads.'),
 ('9.2', '既知current profileの全Core直接参照を依存に含める。親から継承する影響も考慮。', 'Dependencies cover all direct Core references of current known profiles and effects inherited from parents.'),
 ('10.1', '相対式、anchorの音名一致、実配列内のindex、重複noteId禁止を確認。', 'Check relative-pitch equation, anchor pitch class, actual context bounds and unique target note IDs.'),
 ('10.2', '生成工程IDは局所一意。vendorExtensionは自身以外の実在拡張を指し、current時はdocument依存。', 'Process IDs are locally unique; current vendorExtension targets another existing extension and requires document scope.'),
 ('10.3', 'appearanceのrole割当と色参照を解決し、競合する割当を意味規則に従って扱う。', 'Resolve appearance role/color references and apply the specification’s presentation precedence.'),
 ('10.4', 'phraseの完全対応、clip所有、source IDs・noteMapの一意性、反復式・移調・範囲。', 'Complete phrase correspondence, clip ownership, source/mapping uniqueness, repetition equations, transposition and bounds.'),
 ('10.5', 'candidateの局所ID、group間の管理clip非重複、選択IDとCore enabledの一致。', 'Local candidate IDs, disjoint managed clips across groups, and agreement between selection and Core enabled flags.'),
 ('10.6 / 10.7', '生成・選択・template置換・detachは明示的操作。読込時に実行しない。保護対象はbeforeから固定。', 'Generation, choice, template replacement and detachment are explicit operations; no execution on load; protection is fixed from before.'),
 ('11', '2.3移行は版文字列置換ではない。sourceText、hash、移行記録を保持する。', '2.3 migration is not a version-string edit; preserve source text, its hash and the conversion report.'),
]


def main():
    raw = SOURCE.read_bytes()
    schema = json.loads(raw)
    nodes = list(schema_nodes(schema))
    by_pointer = dict(nodes)
    locations = instance_locations(schema)
    parameters = []
    overlays = []
    for pointer, node in nodes:
        if not isinstance(node, dict) or '/properties/' not in pointer:
            continue
        parent_pointer, name = pointer.rsplit('/properties/', 1)
        if '/' in name:
            continue
        parent = by_pointer[parent_pointer]
        desc = description(pointer, name)
        entry = {
            'schema_pointer': pointer, 'name': name,
            'context': owner(pointer), 'parent_schema_pointer': parent_pointer,
            'instance_paths': locations.get(pointer, []),
            'required_in_parent': name in parent.get('required', []),
            'requiredness_ja': required_text(parent, name, 0),
            'requiredness_en': required_text(parent, name, 1),
            'description_ja': desc[0], 'description_en': desc[1],
            'schema': node, 'effective_constraints': effective(schema, node),
        }
        is_overlay = any('/' + key + '/' in pointer for key in ('if', 'then', 'else', 'not'))
        (overlays if is_overlay else parameters).append(entry)
    enum_sets = []
    constants = []
    branches = []
    for pointer, node in nodes:
        if not isinstance(node, dict):
            continue
        for keyword, output in (('enum', enum_sets), ('const', constants)):
            if keyword in node:
                output.append({'schema_pointer': pointer + '/' + keyword,
                               'node_schema_pointer': pointer,
                               'instance_paths': locations.get(pointer, []),
                               'values': node[keyword] if keyword == 'enum' else [node[keyword]]})
        for keyword in BRANCH_KEYS:
            if keyword in node:
                value = node[keyword]
                branches.append({'schema_pointer': pointer + '/' + keyword,
                                 'keyword': keyword, 'node_schema_pointer': pointer,
                                 'instance_paths': locations.get(pointer, []),
                                 'value': value})
    counts = {
        'canonical_parameter_declarations': len(parameters),
        'conditional_property_overlays': len(overlays),
        'total_property_occurrences': len(parameters) + len(overlays),
        'named_definitions': len(schema['$defs']),
        'enum_sets': len(enum_sets),
        'enum_alternatives': sum(len(e['values']) for e in enum_sets),
        'const_occurrences': len(constants),
        'branch_rule_occurrences': len(branches),
        'schema_nodes': len(nodes),
    }
    catalog = {
        'catalog_version': '1.0.0', 'ostf_version': '3.0.0',
        'source_schema': '../schema/ostf-3.0.0.schema.json',
        'source_schema_id': schema['$id'], 'source_schema_dialect': schema['$schema'],
        'source_sha256': hashlib.sha256(raw).hexdigest(),
        'purpose': 'Static documentation inventory, not validator output or runtime evidence.',
        'counting_rule': 'Canonical declarations are each properties entry outside if/then/else/not overlays. Branch-local declarations count separately. Conditional overlays remain fully listed. Instance paths use [*] for array elements or dynamic object members; conditions remain in schema fragments.',
        'path_interpretation': 'Paths enumerate structural locations, not proof that a branch is active in a particular document. Known payload paths require exact namespace/version dispatch. A wildcard under extensions means any namespace, including known ones whose common envelopes still apply.',
        'counts': counts, 'parameters': parameters, 'conditional_property_overlays': overlays,
        'enum_sets': enum_sets, 'constants': constants, 'branches': branches,
        'definitions': [
            {'name': name, 'schema_pointer': '#/$defs/' + esc(name),
             'instance_paths': locations.get('#/$defs/' + esc(name), []),
             'description_ja': DEFINITIONS[name][0], 'description_en': DEFINITIONS[name][1],
             'schema': definition}
            for name, definition in schema['$defs'].items()
        ],
        'schema_nodes': [{'schema_pointer': p, 'instance_paths': locations.get(p, []), 'schema': n} for p, n in nodes],
    }
    (DOCS / 'PARAMETER_CATALOG.json').write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    for lang, suffix in enumerate(('ja', 'en')):
        title = 'OSTF 3.0.0 全パラメーターリファレンス' if lang == 0 else 'OSTF 3.0.0 Complete Parameter Reference'
        lines = ['# ' + title, '']
        if lang == 0:
            lines += [
                'Core `3.0.0` と、同梱する6種類の任意profileの正確な版 `1.0.0-draft.1` を対象とします。'
                'この文書はSchemaの全定義・宣言フィールド・選択値・分岐・制約を参照する辞典です。'
                '使い方は[全網羅マニュアル](COMPLETE_MANUAL.ja.md)、規範的な意味は[仕様本文](FORMAT_SPECIFICATION.ja.md)、'
                '具体的なファイルは[サンプル索引](../samples/INDEX.md)を参照してください。', '',
                '**列挙した項目の範囲**：宣言パラメーター ' + str(counts['canonical_parameter_declarations']) + '件、条件による再制約 '
                + str(counts['conditional_property_overlays']) + '件、名前付き定義51件、enum ' + str(counts['enum_sets'])
                + '組（値の出現数' + str(counts['enum_alternatives']) + '）。枝ごとの同名フィールドは別宣言として数えます。'
                '同じ定義を使う複数の場所は、その定義を重複計上しません。任意文字列・数値・ベンダーJSONの全組合せを有限個の例で列挙する意味ではありません。', '',
                '各項目の正確なSchema JSON Pointer、展開したinstance path、原文の制約は'
                '[PARAMETER_CATALOG.json](PARAMETER_CATALOG.json)に収録しています。'
                'サンプルとの対応は[COVERAGE.md](COVERAGE.md)を参照してください。これは文書作成用の静的な棚卸しであり、実行検証や適合性の合格結果ではありません。', '',
                '## 読み方と共通規則', '',
                '- 「必須」はキーが必要という意味です。任意でも`null`が許されるとは限りません。標準の明示的nullは`selectedCandidateId`の未選択です。',
                '- `additionalProperties: false`は未宣言キーの禁止です。Coreの`velocity`などを追加せず、必要な情報は拡張へ置きます。',
                '- `default`はSchema注釈であり、自動挿入しません。track/clipの`enabled`だけは仕様上、省略を`true`として解釈します。',
                '- `minimum`/`maximum`は両端を含み、`exclusiveMinimum`はその値を除きます。`uniqueItems`は配列要素の重複禁止です。',
                '- 整数フィールドにはJSON整数tokenを使います。`1.0`、`1e0`、`true`は整数フィールドの正しい記述ではありません。',
                '- `oneOf`は一つだけ、`anyOf`は少なくとも一つ、`allOf`はすべての規則に一致します。`if`は条件検査、`then`は条件成立時の追加制約です。',
                '- 任意profileの解釈はnamespaceと正確な版で決めます。未知版の`data`は共通envelope内で保持し、旧版payload規則を適用しません。',
                '- instance pathの`[*]`は配列要素または動的な辞書キーを表します。パスの列挙だけで条件分岐の成立を意味しません。', '',
            ]
        else:
            lines += [
                'This dictionary covers Core `3.0.0` and the exact provisional version `1.0.0-draft.1` of all six bundled optional profiles. '
                'It lists every definition, declared field, finite choice, branch and structural constraint. See the '
                '[complete manual](COMPLETE_MANUAL.en.md) for usage, the [specification](FORMAT_SPECIFICATION.en.md) for normative meaning, '
                'and the [sample index](../samples/INDEX.md) for complete files.', '',
                '**Inventory scope:** ' + str(counts['canonical_parameter_declarations']) + ' canonical parameter declarations, '
                + str(counts['conditional_property_overlays']) + ' conditional property overlays, 51 named definitions, '
                + str(counts['enum_sets']) + ' enum sets (' + str(counts['enum_alternatives']) + ' value occurrences). '
                'Same-named branch-local fields are separate declarations; reuses of one definition are not counted again. '
                'Completeness does not mean enumerating every possible string, number, vendor JSON value or musical combination.', '',
                'Exact schema JSON Pointers, expanded instance paths and original constraints are provided in '
                '[PARAMETER_CATALOG.json](PARAMETER_CATALOG.json); [COVERAGE.md](COVERAGE.md) maps these to samples. '
                'This is a static documentation inventory, not runtime verification or a conformance pass result.', '',
                '## Reading conventions and common rules', '',
                '- Required means that the member must exist. Optional does not imply nullable. The explicit standard null case is an unselected `selectedCandidateId`.',
                '- `additionalProperties: false` forbids undeclared keys. Put additional information in extensions rather than adding fields such as Core `velocity`.',
                '- `default` is a schema annotation and inserts nothing. The specification gives omitted track/clip `enabled` the semantic value `true`.',
                '- `minimum`/`maximum` are inclusive; `exclusiveMinimum` excludes its endpoint. `uniqueItems` disallows duplicate array values.',
                '- Integer fields require JSON integer tokens. `1.0`, `1e0` and `true` are not valid integer-field representations.',
                '- `oneOf` matches exactly one alternative, `anyOf` at least one, and `allOf` every listed rule. `if` tests a condition; `then` applies its consequent.',
                '- Profile interpretation is selected by exact namespace and version. Preserve unknown-version `data` in the common envelope without applying an older payload schema.',
                '- Instance-path `[*]` means an array element or dynamic object key. Listing a path does not assert that a conditional branch is active.', '',
            ]
        lines += [('Schema SHA-256: `' + hashlib.sha256(raw).hexdigest() + '`.'), '',
                  ('出典: ' if lang == 0 else 'Source: ') + '[ostf-3.0.0.schema.json](../schema/ostf-3.0.0.schema.json).', '',
                  ('## 型・オブジェクト索引' if lang == 0 else '## Definition index'), '']
        for name in ['root', *schema['$defs']]:
            lines.append('- [' + name + '](#def-' + name.lower() + ') — ' + DEFINITIONS[name][lang])
        lines.append('')
        for name, definition in [('root', schema), *schema['$defs'].items()]:
            pointer = '#' if name == 'root' else '#/$defs/' + esc(name)
            lines += ['<a id="def-' + name.lower() + '"></a>', '', '## ' + name, '', DEFINITIONS[name][lang], '',
                      'Schema: `' + pointer + '`', '', summarize(schema, definition, lang) + '.', '']
            paths = locations.get(pointer, [])
            if paths:
                lines += [('使用箇所（構造上のパス）:' if lang == 0 else 'Structural instance locations:'), '']
                lines += ['- `' + path + '`' for path in paths]
                lines.append('')
            # Include inline object properties and branch declarations belonging
            # to this named definition, without folding away their branch scope.
            owned = [entry for entry in parameters if entry['context'] == name]
            if name == 'root':
                owned = [entry for entry in owned if entry['parent_schema_pointer'] == '#']
            if owned:
                lines += [('| パラメーター / Schema Pointer | 必須性 | 型・構造制約 | 意味 |' if lang == 0 else '| Parameter / Schema Pointer | Presence | Type and structural constraints | Meaning |'),
                          '| --- | --- | --- | --- |']
                for entry in owned:
                    field = '`' + entry['name'] + '`<br>`' + entry['schema_pointer'] + '`'
                    lines.append('| ' + field + ' | ' + entry['requiredness_ja' if lang == 0 else 'requiredness_en']
                                 + ' | ' + summarize(schema, entry['schema'], lang)
                                 + ' | ' + entry['description_ja' if lang == 0 else 'description_en'] + ' |')
                lines.append('')
            rules = {key: value for key, value in definition.items()
                     if key in BRANCH_KEYS or key in ('propertyNames', 'patternProperties', 'not')
                     or (key == 'additionalProperties' and isinstance(value, dict))}
            # Nested inline objects have their own required/closed rules.
            inline_rules = []
            for p, n in nodes:
                if p.startswith(pointer + '/properties/') and owner(p) == name and isinstance(n, dict):
                    if 'properties' in n and not any('/' + key + '/' in p for key in ('if', 'then', 'else', 'not')):
                        inline_rules.append((p, {k: v for k, v in n.items() if k != 'properties'}))
            if rules:
                lines += [('構造・分岐規則（Schema原文）:' if lang == 0 else 'Structural/conditional rules (verbatim schema fragments):'), '',
                          '```json', json.dumps(rules, ensure_ascii=False, indent=2), '```', '']
            # Branches can be attached to a property rather than its named
            # object definition (selectedCandidateId and each profile wrapper).
            # Print their complete fragments as well; do not merely promise a
            # rule "below" without reproducing those alternatives.
            nested_branch_roots = []
            for p, n in nodes:
                if not p.startswith(pointer + '/properties/') or owner(p) != name or not isinstance(n, dict):
                    continue
                branch_fragment = {k: v for k, v in n.items() if k in BRANCH_KEYS}
                if not branch_fragment or any(p.startswith(previous + '/') for previous in nested_branch_roots):
                    continue
                nested_branch_roots.append(p)
                lines += [('フィールド内の分岐 ' if lang == 0 else 'Property-local branch ') + '`' + p + '`:', '',
                          '```json', json.dumps(branch_fragment, ensure_ascii=False, indent=2), '```', '']
            for p, fragment in inline_rules:
                lines += [('内側のオブジェクト ' if lang == 0 else 'Inline object ') + '`' + p + '`:', '',
                          '```json', json.dumps(fragment, ensure_ascii=False, indent=2), '```', '']
        lines += [('## 条件付きフィールド再制約の全一覧' if lang == 0 else '## Complete conditional property overlays'), '',
                  ('既に宣言されたフィールドを条件判断・条件成立後の制約として使う箇所です。新しいパラメーターとして二重計上しません。' if lang == 0 else 'These clauses test or further constrain already declared fields. They are not counted again as new parameters.'), '',
                  '| Schema Pointer | ' + ('制約' if lang == 0 else 'Constraint') + ' |', '| --- | --- |']
        for entry in overlays:
            lines.append('| `' + entry['schema_pointer'] + '` | ' + code(entry['schema']) + ' |')
        lines += ['', ('## 全enum・定数索引' if lang == 0 else '## Complete enum and constant index'), '',
                  '| Schema Pointer | ' + ('値' if lang == 0 else 'Values') + ' |', '| --- | --- |']
        for entry in enum_sets + constants:
            lines.append('| `' + entry['schema_pointer'] + '` | ' + code(entry['values']) + ' |')
        lines += ['', ('## Schemaだけでは完結しない意味規則' if lang == 0 else '## Semantic requirements beyond schema shape'), '',
                  ('下表は規範仕様への索引です。配列順、参照、計算結果、操作の正しさをSchemaの構造一致だけで証明したとは扱いません。' if lang == 0 else 'This table indexes normative requirements. Shape matching alone does not establish ordering, references, calculated results or operation correctness.'), '',
                  '| ' + ('仕様節' if lang == 0 else 'Specification section') + ' | ' + ('追加で必要な意味規則' if lang == 0 else 'Additional semantic requirements') + ' |', '| --- | --- |']
        for section, ja, en in SEMANTIC_ROWS:
            lines.append('| [' + section + '](FORMAT_SPECIFICATION.' + suffix + '.md) | ' + (ja if lang == 0 else en) + ' |')
        lines += ['', ('## 関連資料と再生成' if lang == 0 else '## Related material and regeneration'), '',
                  '- [Complete manual](COMPLETE_MANUAL.' + suffix + '.md)',
                  '- [Normative specification](FORMAT_SPECIFICATION.' + suffix + '.md)',
                  '- [Explicit operations and CLI/API parameters](OPERATIONS.md)',
                  '- [2.3 migration](MIGRATION_2_3_TO_3_0.md)',
                  '- [Machine-readable parameter catalog](PARAMETER_CATALOG.json)',
                  '- [Sample coverage](COVERAGE.md)', '',
                  ('この文書とカタログは配布物のrootで次の文書生成コマンドから再生成できます。OSTFファイルの検証・再生は行いません。' if lang == 0 else 'Regenerate this reference and catalog from the package root with the documentation command below. It does not validate or play OSTF documents.'), '',
                  '```sh', 'python3 tools/build_reference.py', '```', '']
        (DOCS / ('PARAMETER_REFERENCE.' + suffix + '.md')).write_text('\n'.join(lines), encoding='utf-8')
    print(json.dumps({'documentation_inventory': counts, 'runtime_verification_performed': False}, ensure_ascii=False))


if __name__ == '__main__':
    main()
