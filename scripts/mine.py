import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
# 言葉バンク候補の一文を抽出（原文の部分文字列のまま）
# 使い方: python3 mine.py <theme> [N] [lang]
import json, re, glob, sys, collections, random
D = RAW + "/"
theme = sys.argv[1]; N = int(sys.argv[2]) if len(sys.argv) > 2 else 40; lang = sys.argv[3] if len(sys.argv) > 3 else "jp"
recs = []
for f in glob.glob(D + "*.jsonl"):
    for l in open(f, encoding="utf-8"): recs.append(json.loads(l))
PRO = re.compile(r"当院|施術|ご予約|院長|治療家|整体師|理学療法士|柔道整復師|トレーナー|患者さん|患者様|お客様|クライアント")
FP = re.compile(r"私|わたし|自分|うち|主人|夫|旦那|娘|息子|孫|母|家族|ワタシ|あたし")
T = CFG.get("mine_ja", {})
pat = re.compile(T[theme]) if lang == "jp" else None
EN_T = CFG.get("mine_en", {})
if lang == "en": pat = re.compile(EN_T[theme], re.I)
HIPJ = rx("topic_ja")
EXCL = rx("exclude", flags=re.I)
HIPE = rx("topic_en", flags=re.I)
HIPURL = set(u for u in [r["url"] for r in recs] if any(t in u for t in CFG.get("topic_thread_ids", [])))
cands = []
for r in recs:
    if (r["country"] == "JP") != (lang == "jp"): continue
    t = r["text"]
    if lang == "jp" and PRO.search(t): continue
    if EXCL.search(t): continue
    hipthread = r["url"] in HIPURL
    if lang == "jp" and not (HIPJ.search(t) or hipthread): continue
    if lang == "en" and not HIPE.search(t) and not r["is_reply"]: continue
    sents = re.split(r"(?<=[。！？!?])|\n", t) if lang == "jp" else re.split(r"(?<=[.!?])\s+|\n", t)
    for s in sents:
        s = s.strip()
        if not (14 <= len(s) <= (95 if lang == "jp" else 260)): continue
        if not pat.search(s): continue
        if lang == "jp" and not (FP.search(s) or re.search(r"です|ます|た。|い。|ない|ません", s)): continue
        sc = len(pat.findall(s)) + (2 if r["author_age_hint"] else 0) + (1 if not r["is_reply"] else 0)
        if lang == "jp":
            sc += len(re.findall(T["feel"], s)) * 1.5
        cands.append((sc, r["platform"], r["url"], s))
random.seed(int(sys.argv[4]) if len(sys.argv) > 4 else 1)
random.shuffle(cands)
cands.sort(key=lambda x: -x[0])
seen = set(); out = []
for c in cands:
    k = c[3][:25]
    if k in seen: continue
    seen.add(k); out.append(c)
skip = int(sys.argv[5]) if len(sys.argv) > 5 else 0
for sc, p, u, s in out[skip:skip + N]:
    print("%s|%s|%s" % (p[:10], u.replace("https://", "").replace("detail.chiebukuro.yahoo.co.jp/qa/question_detail/", "cb/").replace("www.reddit.com/r/", "rd/").replace("www.mumsnet.com/talk/", "mn/"), s))
print("TOTAL", len(out), file=sys.stderr)
