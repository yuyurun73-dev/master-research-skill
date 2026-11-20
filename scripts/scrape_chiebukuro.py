import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
import re, json, time, sys, urllib.parse, urllib.request, os
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
OUT = stage("chiebukuro.jsonl")
QUERIES = [l.strip() for l in open(sys.argv[1], encoding="utf-8") if l.strip()]
PER = int(sys.argv[2]) if len(sys.argv) > 2 else 10
def get(url, tries=3):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "ja"})
            return urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace")
        except Exception as e:
            sys.stderr.write("retry %s %s\n" % (url, e)); time.sleep(2)
    return ""
def parse_detail(url, query):
    h = get(url)
    if not h: return None
    for m in re.findall(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', h, re.S):
        try: blocks = json.loads(m)
        except Exception: continue
        if not isinstance(blocks, list): blocks = [blocks]
        for b in blocks:
            if b.get("@type") == "QAPage":
                q = b["mainEntity"]
                text = q.get("text") or q.get("name", "")
                if len(q.get("name","")) > len(text): text = q.get("name","")
                replies = []
                aa = q.get("acceptedAnswer")
                if aa: replies.append(aa.get("text", ""))
                for sa in q.get("suggestedAnswer", []) or []:
                    replies.append(sa.get("text", ""))
                replies = [r for r in replies if r]
                full = text + ("\n\n【回答】\n" + "\n---\n".join(replies) if replies else "")
                return {"url": url, "source": "chiebukuro", "country": "JP",
                        "date": q.get("datePublished",""), "title": q.get("name","")[:60],
                        "query": query, "text": full, "question": text, "replies": replies}
    return None
seen = set()
if os.path.exists(OUT):
    for line in open(OUT, encoding="utf-8"):
        try: seen.add(json.loads(line)["url"])
        except Exception: pass
_old="/nonexistent"
if os.path.exists(_old):
    for _l in open(_old,encoding="utf-8"):
        try: seen.add(json.loads(_l)["url"])
        except Exception: pass
f = open(OUT, "a", encoding="utf-8"); n = 0
for q in QUERIES:
    ids = []
    for pg in (1, 2):
        s = get("https://chiebukuro.yahoo.co.jp/search?p=" + urllib.parse.quote(q) + ("&b=%d" % (1 + (pg-1)*10) if pg > 1 else ""))
        for qid in re.findall(r'detail/(q\d+)', s):
            if qid not in ids: ids.append(qid)
        time.sleep(0.5)
    sys.stderr.write("QUERY %s -> %d ids\n" % (q, len(ids)))
    for qid in ids[:PER]:
        url = "https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/" + qid
        if url in seen: continue
        seen.add(url)
        d = parse_detail(url, q)
        if d and len(d["question"]) > 40:
            f.write(json.dumps(d, ensure_ascii=False) + "\n"); f.flush(); n += 1
        time.sleep(0.6)
sys.stderr.write("WROTE %d\n" % n)
