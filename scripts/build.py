import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
# template.md に件数表・集計表・照合結果を差し込んで voice-research.md を書く
import json, re, glob, collections, subprocess, datetime
D = RAW + "/"
ANA = os.path.join(RESEARCH_DIR, "analysis") + "/"
HERE = os.path.dirname(os.path.abspath(__file__)) + "/"
OUT = os.path.join(RESEARCH_DIR, "voice-research.md")
subprocess.run(["python3", HERE + "aggregate.py"], check=True, capture_output=True)
recs = []
for f in sorted(glob.glob(D + "*.jsonl")):
    for l in open(f, encoding="utf-8"): recs.append(json.loads(l))
# 件数表
cnt = collections.Counter(); thr = collections.defaultdict(set); rep = collections.Counter(); age = collections.Counter()
for r in recs:
    k = (r["country"] if r["country"] == "JP" else "EN(" + r["country"] + ")", r["platform"])
    cnt[k] += 1; thr[k].add(r["url"]); rep[k] += r["is_reply"]; age[k] += bool(r["author_age_hint"])
rows = "| 言語 | 媒体 | 発言数 | うち返信 | スレ/記事数 | 年齢・属性ヒントあり |\n|---|---|---|---|---|---|\n"
tj = te = 0
for k in sorted(cnt, key=lambda k: (k[0] != "JP", -cnt[k])):
    rows += "| %s | %s | %d | %d | %d | %d |\n" % (k[0], k[1], cnt[k], rep[k], len(thr[k]), age[k])
    if k[0] == "JP": tj += cnt[k]
    else: te += cnt[k]
tt = sum(len(v) for v in thr.values())
counts = rows + "\n**合計：日本語 %d 発言／英語 %d 発言（計 %d 発言・%d スレッド/記事）**。日本語の割合は約%d%%。\n" % (tj, te, tj + te, tt, round(100 * tj / max(1, tj + te)))
counts += "\n知恵袋は質問＋回答の全文、5ch はスレのレス全件（悩みの語で絞る）、ブログは本文丸ごと（宣伝記事は除外）、Mumsnet は元投稿＋全返信、Reddit は投稿本文＋上位スレのコメントの木。\n"
agg = open(ANA + "agg.md", encoding="utf-8").read()
parts = re.split(r"(?=^### )", agg, flags=re.M)
emo = "".join(p for p in parts if p.startswith("### 感情マップ"))
rest = "".join(p for p in parts if p.startswith("###") and not p.startswith("### 感情マップ"))
kw = open(ANA + "kw.md", encoding="utf-8").read()
md = open(os.path.join(RESEARCH_DIR, "voice-research.template.md") if os.path.exists(os.path.join(RESEARCH_DIR, "voice-research.template.md")) else HERE + "../references/voice-research-template.md", encoding="utf-8").read()
md = md.replace("<!--COUNTS-->", counts).replace("<!--EMO-->", emo).replace("<!--AGG-->", rest).replace("<!--KW-->", kw)
# 照合
byurl = collections.defaultdict(str)
for r in recs: byurl[r["url"]] += "\n" + r["text"]
n = miss = 0; misses = []
for line in md.split("\n"):
    m = re.search(r"「(.*)」 \[([^\]]*)\]\((https?://[^)]+)\)", line)
    if not m: continue
    q, u = m.group(1), m.group(3); n += 1
    if u not in byurl: miss += 1; misses.append("NOURL " + u + " " + q[:40]); continue
    if q not in byurl[u]: miss += 1; misses.append("MISS " + u + " " + q[:60])
ver = "- 照合方法：本文の `「引用」 [媒体](URL)` 形式の行をすべて抜き出し、生データ（raw/*.jsonl）の同じURLの発言テキストに、その引用が**一字一句そのまま部分文字列として含まれるか**を機械で確認（`scripts/build.py`）。\n"
ver += "- 実行日時：%s\n- **引用 %d 件／MISS %d 件**\n" % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), n, miss)
if misses: ver += "\n```\n" + "\n".join(misses) + "\n```\n"
md = md.replace("<!--VERIFY-->", ver)
open(OUT, "w", encoding="utf-8").write(md)
print("quotes", n, "MISS", miss); print("\n".join(misses))
print("JP", tj, "EN", te)
