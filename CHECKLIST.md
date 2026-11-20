# 統合リサーチスキル チェックリスト（2026-11-18）

依頼：Driveの「2. Research」講義6本のリサーチ手順を土台に、ペイン・アバター・UMP/UMSまで全部入りの1本を作る。既存のリサーチ系スキル・wikiのSOPは全部これに合わせる。追加指示：native-adsは質が高いが、もっとニッチな情報を取れるように。

## A. 原典を読む
- [x] A1 講義6本を書き起こして保存 → `~/llm-wiki/raw/research-course-ecomuniversity/`（txt 6本＋要点スライド3枚。計20,633語）
- [x] A2 6本の要点を日本語化 → `references/lecture-notes.md`（チャットでも報告）
- [x] A3 既存スキルの棚卸し：ump-ums / native-ads / customer-research / research-icp / research-market / competitor-profiling / competitors / product-council → `references/merge-map.md`
- [x] A4 wikiのSOP棚卸し：Zakaria 7本・RMBC II 2本・ネイティブPhase1・Evolve 2本・gap-research 3本・avatar/angle 2本 → `references/merge-map.md`
- [ ] A5 講義の「リサーチ用プロンプト」「テンプレ」の原本 → **未入手**（共有は動画だけ・親フォルダ非共有）。代わりに `references/engine1-prompt.md` を自前で作成

## B. 統合スキル（~/.claude/skills/master-research/）
- [x] B1 SKILL.md：講義の8ステップを背骨に工程0〜14（チェックリスト→Engine1→商品→買い手の道→声の収集→購入者の声→記録→突き合わせ→認知仮説→アバター/サブアバター→競合→UMP/UMS→厳密さ→アングル→メモ→読み直し・納品）
- [x] B2 全工程に「入力／やること／出力／合格」
- [x] B3 既存の良い所の対応表 → `references/merge-map.md`（スキル12・wiki 16・本人メモ11）
- [x] B4 講義03（生きた文書）・05（厳密さ）・06（ピッチ）を工程化 → 工程11・13・「生かし続ける」節・`research-doc-template.md`
- [x] B5 本人ルール反映：VoC原文のまま・研究より強く言わない・報告して止まる・薬機法の注意書きなし・商品開発を提案しない・調べて＝調べるだけ（SKILL.md「決まり」）
- [x] B6 納品物の型：`RESEARCH.md`（正本・16節）＋`CONTEXT.md`（地図）＋`voice-research-template.md`
- [x] B7 description に日本語の呼び出し語（YAML読み込みOK・537字）
- [x] B8（追加指示）ニッチ：`references/niche-sources.md`（日英4区分・32サイトを curl で到達確認）＋ニッチの引き方5つ＋2周目（内輪の言葉で引き直し）を工程4に必須化＋最低ライン「普通は見ない出どころ3種以上」
- [x] B9 収集スクリプトを汎用化して同梱（config.json で案件切替）：知恵袋・Ameba・note・はてな・5ch・ガルちゃん・Mumsnet・Reddit・HealthUnlocked・X＋**新規** YouTubeコメント・FDA不具合報告＋汎用の口 `utter_*.jsonl`

## B2. 追加指示（2026-11-18 2回目）「Redditもっと取れる・海外は多いほど良い」「40代以上の日本人はどこに書く？Facebook？」「40・50代が信頼するメディア→記事型かVSLか・LPの見た目」
- [x] E1 Reddit を作り直し：サーバー検索をやめ、日付で遡って全投稿→手元で絞る（1分≈1,500投稿・失敗0）。保存上限45→150〜200/サブレ、コメントの木500→上位80、雑談・世代系サブレはコメントを遡る
- [x] E2 サブレの自動発見 `discover_subreddits.py`（名前の頭の文字で候補→直近100投稿の当たり→年間の当たり件数で 全部/絞る/コメント/使わない を判定→config案）
- [ ] E3 股関節で実際に大量取得（18サブレ＋コメント13サブレ）→ 件数を報告 ← 実行中
- [x] E4 英語の掲示板の汎用スクリプト `scrape_forum_threads.py`（XenForo・Discourse・その他）。BoneSmart 37投稿・Inspire 10投稿で確認。Patient.info は403で飛ばす
- [x] E5 最低ラインを海外重視に：英語3,000発言以上（日本市場でも）・サブレ10以上・スレ300以上・英語の掲示板2サイト以上
- [x] E6 日本の40代以上の居場所と信頼メディアを総務省 令和6年度の報告書PDFから実測 → `niche-sources.md` §0.5
- [x] E7 Facebook を実測：公開ページもグループも外から中身0 → 本人が手で参加して渡す／明示の許可がある時だけ読むだけ、と明記
- [x] E8 LINEオープンチャットの部屋（名前・説明・人数・最終発言）を取る `scrape_line_openchat.py`（股関節で41部屋・2,136人）
- [x] E9 工程3b「信頼の地図→ファネルの形（記事型/VSL/直PDP）とLPの見た目・語り手」を追加＋情報源の言及件数を集計（MELAO股関節：医師823・家族友人440・整体師402・ネット237・テレビ118）

## C. 既存との整理
- [x] C1 重なる6スキルの description に `/master-research` への案内（ump-ums・native-ads・customer-research・research-icp・research-market・competitor-profiling。全部YAML読み込みOK）。消していない
- [ ] C2 wiki の moc-research-sops への導線 → **未実施**（本人ルール「wikiは頼まれた時だけ書く」）。書くなら1行

## D. 検収
- [x] D1 実データで通し：MELAO股関節の生データで新旧スクリプトの出力を比較 → **変換10媒体すべて同一・集計 完全一致**。新規の作業フォルダで実際に収集→変換→集計→報告書組み立てまで通過（知恵袋3・Ameba11・note8・はてな2・ガルちゃん10スレ・5ch 727発言・Reddit 28スレ・YouTube 112コメント・FDA 30件 → JP 1,003／EN 185発言）
- [x] D2 引用の照合：本物1件＋偽物1件を入れて build.py → 「引用2件／MISS 1件」で偽物だけ検出
- [x] D3 SKILL.md 189行（500行以内）・参照パス 存在20／欠落0（1件は見本内の `*.jsonl` 表記の誤検知）
- [ ] D4 Trustpilot の自動収集 → **やらない**（403のサイトを自動化ブラウザで抜ける作りが権限で拒否。スクリプトは削除し、工程4bは WebFetch か本人の手に変更）
