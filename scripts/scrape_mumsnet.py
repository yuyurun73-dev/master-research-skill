import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
# Mumsnet スレ（OP=ld+json articleBody, 返信=reply-body-*）を1行1発言で保存
import re, json, sys, time, html, urllib.request
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
OUT = stage("mumsnet.jsonl")
URLS = [l.strip() for l in open(sys.argv[1]) if l.strip()]
def get(u):
    for i in range(3):
        try: return urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": UA}), timeout=40).read().decode("utf-8", "replace")
        except Exception as e: sys.stderr.write("retry %s %s\n" % (u, e)); time.sleep(3)
    return ""
def clean(s):
    s = re.sub(r"<br\s*/?>", "\n", s); s = re.sub(r"</p>\s*<p>", "\n\n", s); s = re.sub(r"<blockquote.*?</blockquote>", "", s, flags=re.S)
    s = re.sub(r"<[^>]+>", "", s); return re.sub(r"\n{3,}", "\n\n", html.unescape(s)).strip()
f = open(OUT, "a", encoding="utf-8"); n = 0
for u in URLS:
    u = u.split("?")[0]
    pages = [get(u)]
    for p in range(2, 6):
        if ("page=%d" % p) not in pages[-1]: break
        pages.append(get(u + "?page=%d" % p)); time.sleep(1)
    h = pages[0]
    if not h: continue
    op, date = "", ""
    for m in re.findall(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', h, re.S):
        try: j = json.loads(m)
        except Exception: continue
        if isinstance(j, dict) and j.get("@type") == "DiscussionForumPosting":
            op = (j.get("headline", "") + "\n\n" + j.get("articleBody", "")).strip(); date = j.get("datePublished", "")[:10]
    if op:
        f.write(json.dumps({"platform": "Mumsnet", "country": "UK", "url": u, "date": date, "text": op, "is_reply": False}, ensure_ascii=False) + "\n"); n += 1
    first = True
    for hp in pages:
        for rid, dt, body in re.findall(r'data-reply-id="(\d+)".*?(\d\d/\d\d/\d{4}) \d\d:\d\d.*?id="reply-body-\1"[^>]*>(.*?)</div>', hp, re.S):
            t = clean(body)
            if first: first = False;
            if len(t) < 40 or (op and t[:80] in op): continue
            d = "%s-%s-%s" % (dt[6:], dt[3:5], dt[:2])
            f.write(json.dumps({"platform": "Mumsnet", "country": "UK", "url": u, "date": d, "text": t, "is_reply": True}, ensure_ascii=False) + "\n"); n += 1
    sys.stderr.write("ok %s\n" % u[-60:]); time.sleep(1.2)
sys.stderr.write("WROTE %d\n" % n)
