# master-research（Claude Code スキル）

商品と悩みを渡すと、ペイン・アバター/サブアバター・VoC（ニッチな掲示板・Reddit・海外まで）・競合・UMP/UMS・アングルの種までを1本の流れで掘り切り、生きたリサーチ文書（RESEARCH.md）1つに束ねる全部入りリサーチ。

- 手順：`SKILL.md`（工程0〜14・最低ライン・決まり）
- 原典と雛形：`references/`（講義6本の要点・RESEARCH.md雛形・ニッチな出どころの地図・Engine 1 の指示文）
- 収集と集計：`scripts/`（知恵袋・Ameba・note・はてな・5ch・ガルちゃん・YouTubeコメント・Reddit・Mumsnet・英語掲示板・LINEオープンチャット・App Storeレビュー・FDA → convert → aggregate → mine → build）

## 入れ方
```
git clone https://github.com/yuyurun73-dev/master-research-skill ~/.claude/skills/master-research
```
使う時は `/master-research <商品> <悩み・読み手> [JP|US]`。案件ごとに `references/config-example.json` を写して `config.json` を作り、`RESEARCH_DIR=<作業フォルダ>` を付けてスクリプトを回す。
