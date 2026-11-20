# 対応表：既存のリサーチ資産 → master-research のどの工程に入ったか

「既存のものは全部合わせる」（2026-11-18本人）。1行ずつ、何をどこに取り込んだか。取り込まなかった物は理由つき。
既存スキルは消していない（他のスキル・メモから呼ばれているため）。重なる物の説明文に「全部入りは /master-research」と案内を足した。

## スキル

| 既存 | 取り込んだ中身 | 入った工程 |
|---|---|---|
| ecomuniversity 講義01〜06（今回の原典） | 2エンジン・8ステップ・生きた文書・サブアバター/アングル・厳密さ・ピッチ | 背骨（工程1〜13全体）／`lecture-notes.md` |
| `/native-ads` 工程1 VoC | xarkr の声の指示文・日英の出どころ・下限40件→実績1,899件・逐語照合MISSゼロ・到達不可の理由記録 | 工程4・5／`voice-research-template.md` |
| `/native-ads` 工程1b 実購入者レビュー | Trustpilot★均等・★1〜3・買った理由の件数＞声の量・返品理由 | 工程4b |
| `/native-ads` 工程2 アバター質問票（10章68問・WHY×3） | 根拠の逐語引用・不明は不明・【推論】明示・コピー直結サマリー | 工程8（質問票は `~/.claude/skills/native-ads/references/avatar-questionnaire.md`） |
| native-ads の収集スクリプト群（melao-insole/raw-hip/tools・negirai/raw-miminari） | 知恵袋・Ameba・note・はてな・5ch・ガルちゃん・Mumsnet・Reddit(arctic)・HealthUnlocked・X・変換・集計・抜き出し・組み立て・照合 | `scripts/`（config.json で案件を切り替える形に汎用化。MELAO股関節の生データで元と出力完全一致を確認） |
| `/ump-ums` | 商品のピン留め・試した物10〜20・研究25本・ノーベル賞級の借景・直結/1段・5条件×4テスト・Dr.Dave基準・自己検収・商品開発を提案しない | 工程2（部品の書き出し）・工程10（手順は ump-ums の SKILL.md 3〜10 をそのまま回す）／`scripts/pm.py`・`ab.py` |
| `/customer-research` | 出どころの信頼度の重み・テーマを頻度×強さで並べる・ペルソナの失敗パターン | 工程5・6 |
| `/research-icp` | 生息地マップ（密度H/M/L・発見/信頼/購入の役割）・確信度ラベル（高=独立3出どころ以上）・最低5データ点 | 工程4・6 |
| `/research-market` | 競合と隣接競合の確認・主張に全部出典 | 工程9 |
| `/competitor-profiling` | 競合をURLから深掘りする観点 | 工程9（日本のEC向けには Zakaria 6軸を主に使う） |
| `/product-council` | — | 取り込まない。**商品を選ぶ前段**。商品が決まっていなければ先にそちら |
| 総務省 令和6年度 情報通信メディアの利用時間と情報行動に関する調査 | 年代別のSNS利用率・書き込み率・メディアの信頼度 | 工程3b・`niche-sources.md` §0.5 |
| `/competitors` | — | 取り込まない。比較LP（SEO）を作るスキルでリサーチではない |

## wiki（~/llm-wiki/wiki/ ほか）

| 既存 | 取り込んだ中身 | 入った工程 |
|---|---|---|
| Zakaria `zakaria-market-research-sop` | 広いカテゴリでなく固有の悩みを持つ層で切る | 工程8 |
| Zakaria `zakaria-avatar-research-sop` | アバター文書の章立て（日常・表の症状・隠れたコスト・失敗した解決策・本当の欲求・反論・認知段階） | 工程8 |
| Zakaria `zakaria-competitor-research-sop` | 競合6軸（ファネル・オファー・広告・立ち位置・効いている事・失敗している事） | 工程9 |
| Zakaria `zakaria-similar-product-research-sop` | 似た商品の反論マップ（商品・信頼・結果・個人的事情）と立ち位置の穴 | 工程9 |
| Zakaria `zakaria-research-root-cause-sop` | 見える症状→本人の思う原因→本当の機序→なぜ前のが効かなかったか→知識の穴→敵 | 工程10 |
| `rmbc2-unified-research-document`・`rmbc2-deep-research-prompts` | 認知段階は「同型品の認知」で測る・心理の質問リスト（好奇心・堕落を含む）・複数AIの出力を1本に束ねる・**全部の依頼に1文書を添付** | 工程1（`engine1-prompt.md`）・工程7・工程13（RESEARCH.md） |
| ネイティブ講座 Phase1 `02-phase1-audience-diagnosis` | 6つの診断質問・男女のレンズ・信じやすさ4象限・表の痛みと深夜2時の痛み・感情マップ | 工程7・8 |
| Evolve `evolve-research-sequence` | 12の出どころの順・顧客への電話（本人がやる）・Answer The Public | 工程3・4 |
| Evolve `evolve-avatar-system` | 欲求→洗練度→コアアバター→サブアバター→アングル・倫理則「事実とAIの下調べを二重に確かめる」 | 工程8・11 |
| `avatar-construction`（4層） | 欲求→体験→感情→行動。属性は最後 | 工程8 |
| `angle-types` | 隠れた原因／失敗した試み／正しい人が使う物 | 工程11 |
| `satisfied-vs-unsatisfied-customer` | 買うのは不満顧客だけ・3類型（裏切られた/未着手/諦めた） | 工程8 |
| `importance-satisfaction-matrix`・`gap-research-process` | 重要度高×満足度低の穴を狙う | 工程9 |
| `ums-ump-framework`・`ump-llm-pipeline` | UMP5条件・UMS4条件・良いUMPの3型 | 工程10（ump-ums 経由） |

## 本人のメモ（~/.claude/projects/-Users-u/memory/）

| メモ | 反映した所 |
|---|---|
| report-research-before-production（リサーチ後は報告して止まる） | 工程14：台本・記事・画像に進まない |
| research-means-research-only（調べて＝調べるだけ） | 決まり：本番の設定・文言を変えない |
| localize-faithful-translation・jp-copy-fake-comma-tell・jp-ad-copy-no-ai-tells | 決まり：VoCは句読点ごと原文のまま・訳して言い換えない |
| no-auto-compliance | 決まり：薬機法・景表法の注意書きは付けない。見るのは「研究より強く言っていないか」だけ |
| shortform-research-depth（2本見て型を決めるな） | 工程4の最低ライン |
| browser-login-automation-blocked・no-browser-automation-on-live-accounts | `niche-sources.md` の「やらないこと」 |
| youtube-bot-block-clip-library | `scrape_youtube_comments.py` の上限と停止 |
| x-read-via-fxtwitter・instagram-likes-public-page・tiktok-discover-route | 工程4の取り方（URLが分かっている投稿の数字・動画） |
| large-task-checklist-loop・all-japanese-output | 工程0・報告の形 |
| research-depth-mechanism-ums-tech（melaoレベル＝因果の鎖・効かない理由・技術の中身・第三者レビュー） | 工程2（機器の中身・原典主張の検証）・工程4b（自社レビュー全件と表示の差）・工程10 |
| research-timebox（長すぎると「長くない？」） | 工程5の後に途中経過を1回返す（止まらない） |
| deliverables-html-not-md・show-deliverables-inline | 工程14：本人への報告はチャット本文。md は機械用の作業文書 |
