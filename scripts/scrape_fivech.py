import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
import re, json, time, sys, os, html, urllib.request

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
DUA = "Monazilla/1.00 (JaneStyle/3.80)"
OUT = stage("fivech.jsonl")
HOST = CFG.get("fivech", {}).get("host", "https://rio2016.5ch.net")
BOARD = CFG.get("fivech", {}).get("board", "body")
PAGES = int(sys.argv[1]) if len(sys.argv) > 1 else 40

KEEP = rx("topic_ja")
DROP = rx("drop")

def get(u, tries=3, raw=False, ua=UA):
    for _ in range(tries):
        try:
            r = urllib.request.Request(u, headers={"User-Agent": ua})
            b = urllib.request.urlopen(r, timeout=30).read()
            return b if raw else b.decode("utf-8", "replace")
        except Exception as e:
            sys.stderr.write("retry %s %s\n" % (u, e)); time.sleep(2)
    return b"" if raw else ""

def clean(s):
    s = re.sub(r'<br\s*/?>', '\n', s, flags=re.I)
    s = re.sub(r'<[^>]+>', '', s)
    s = html.unescape(s)
    s = re.sub(r'https?://\S+', '', s)
    s = re.sub(r'>>\d+', '', s)
    return re.sub(r'\n{3,}', '\n\n', s).strip()

def thread_posts(tid):
    d = get("https://itest.5ch.io/public/newapi/client.php?subdomain=rio2016&board=%s&dat=%s" % (BOARD, tid), ua="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148")
    try: j = json.loads(d)
    except Exception: return "", []
    posts = []
    for c in j.get("comments", []):
        body = clean(c[6] if len(c) > 6 else "")
        if len(body) > 25: posts.append(body)
    if not posts: return "", []
    return posts[0], posts[1:]

seen = set()
if os.path.exists(OUT):
    for l in open(OUT, encoding="utf-8"):
        try: seen.add(json.loads(l)["url"])
        except Exception: pass

cands = []
for p in range(1, PAGES + 1):
    h = get("https://itest.5ch.io/subback/%s/archives/%d" % (BOARD, p))
    if not h: continue
    found = re.findall(r'<a href="https://itest\.5ch\.io/rio2016/test/read\.cgi/%s/(\d+)">\s*(.*?)\s*</a>' % BOARD, h, re.S)
    for tid, title in found:
        title = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', title))).strip()
        if not KEEP.search(title) or DROP.search(title): continue
        cands.append((tid, title))
    sys.stderr.write("PAGE %d -> %d cands so far\n" % (p, len(cands)))
    time.sleep(0.5)

uniq = []
s2 = set()
for tid, title in cands:
    if tid in s2: continue
    s2.add(tid); uniq.append((tid, title))
sys.stderr.write("CANDS %d\n" % len(uniq))

_old="/nonexistent"
if os.path.exists(_old):
    for _l in open(_old,encoding="utf-8"):
        try: seen.add(json.loads(_l)["url"])
        except Exception: pass
f = open(OUT, "a", encoding="utf-8")
w = 0
for tid, title in uniq:
    url = "%s/test/read.cgi/%s/%s/" % (HOST, BOARD, tid)
    if url in seen: continue
    seen.add(url)
    op, reps = thread_posts(tid)
    if not op:
        sys.stderr.write("EMPTY %s %s\n" % (tid, title)); time.sleep(0.6); continue
    f.write(json.dumps({"url": url, "source": "5ch 身体・健康(過去ログ)", "country": "JP",
        "date": "", "query": title, "title": title,
        "text": (op + "\n\n【レス】\n" + "\n---\n".join(reps))[:30000], "replies": reps}, ensure_ascii=False) + "\n")
    f.flush(); w += 1
    sys.stderr.write("ok %s %s (%d)\n" % (tid, title, len(reps) + 1))
    time.sleep(1.0)
sys.stderr.write("WROTE %d\n" % w)
