# 海外（日本も可）の掲示板のスレを、URLのリストから投稿ごとに取る汎用スクリプト
# 対応：XenForo（BoneSmart など・ページ送りも追う）／Discourse（/t/ のURL・公開JSON）／その他（本文らしい段落を原文のまま）
# スレURLの集め方：WebSearch「site:bonesmart.org <悩み語>」「site:agingcare.com <悩み語>」「site:patient.info/forums <悩み語>」など
# 使い方: RESEARCH_DIR=<作業フォルダ> COUNTRY=EN python3 scrape_forum_threads.py <URLファイル（1行1URL）> [XenForoの最大ページ=10]
# 出力: raw/_stage/utter_forum.jsonl（1行1投稿。platform=サイト名。topic_en/topic_ja で絞られる）
# 403で拒むサイトは飛ばして記録するだけ（抜けにいかない）
import os, sys, re, json, time, html, urllib.request, urllib.parse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
OUT = stage("utter_forum.jsonl")
URLS = [l.strip() for l in open(sys.argv[1], encoding="utf-8") if l.strip() and not l.startswith("#")]
MAXP = int(sys.argv[2]) if len(sys.argv) > 2 else 10
COUNTRY = os.environ.get("COUNTRY", "EN")

def get(u):
    for i in range(3):
        try:
            r = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": UA, "Accept-Language": "en,ja"}), timeout=30)
            return r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            if e.code in (401, 403, 404, 410): sys.stderr.write("skip %s %s\n" % (e.code, u)); return ""
            time.sleep(3 * (i + 1))
        except Exception as e:
            sys.stderr.write("retry %s %s\n" % (u, e)); time.sleep(3 * (i + 1))
    return ""

def clean(t):
    t = re.sub(r"<(script|style|blockquote)[^>]*>.*?</\1>", " ", t, flags=re.S | re.I)   # 引用（他人の発言の再掲）は外す
    t = re.sub(r"<br\s*/?>|</p>|</div>|</li>", "\n", t, flags=re.I)
    t = re.sub(r"<[^>]+>", "", t); t = html.unescape(t)
    return re.sub(r"\n{3,}", "\n\n", re.sub(r"[ \t\r]+", " ", t)).strip()

def site(u): return urllib.parse.urlparse(u).netloc.replace("www.", "")

def xenforo(u, h):
    posts = []; base = re.sub(r"/page-\d+.*$|#.*$", "", u).rstrip("/") + "/"
    p = 1
    while True:
        for m in re.finditer(r'<article[^>]*class="message[^"]*"[^>]*?data-content="post-(\d+)".*?<div class="bbWrapper">(.*?)</div>\s*(?:<div class="js-selectToQuote|</article>|<div class="message-lastEdit|<aside)', h, re.S):
            t = clean(m.group(2))
            if t: posts.append((base + "post-" + m.group(1), t))
        p += 1
        if p > MAXP or ('/page-%d"' % p) not in h: break
        time.sleep(1.2); h = get(base + "page-%d" % p)
        if not h: break
    return posts

def discourse(u):
    m = re.search(r"(https?://[^/]+/t/[^/]+/\d+)", u)
    if not m: return []
    j = get(m.group(1) + ".json")
    try: j = json.loads(j)
    except Exception: return []
    return [(m.group(1) + "/" + str(p["post_number"]), clean(p.get("cooked", ""))) for p in j.get("post_stream", {}).get("posts", [])]

def generic(u, h):
    body = re.sub(r"<(header|footer|nav|aside|form)[^>]*>.*?</\1>", " ", h, flags=re.S | re.I)
    blocks = [clean(b) for b in re.findall(r"<p[^>]*>(.*?)</p>", body, re.S | re.I)]
    blocks = [b for b in blocks if len(b) >= 60 and not re.search(r"cookie|privacy|terms of|sign up|log in|subscribe", b, re.I)]
    return [(u + "#p%d" % i, b) for i, b in enumerate(blocks)]

seen = set()
if os.path.exists(OUT):
    for l in open(OUT, encoding="utf-8"):
        try: seen.add(json.loads(l)["url"])
        except Exception: pass
tot = 0
with open(OUT, "a", encoding="utf-8") as fo:
    for u in URLS:
        if "/t/" in u: posts = discourse(u); kind = "discourse"
        else:
            h = get(u)
            if not h: continue
            if 'data-template="thread_view"' in h or "bbWrapper" in h: posts = xenforo(u, h); kind = "xenforo"
            else: posts = generic(u, h); kind = "generic"
        n = 0
        for i, (pu, t) in enumerate(posts):
            if pu in seen or len(t) < 40: continue
            seen.add(pu); n += 1; tot += 1
            fo.write(json.dumps({"platform": site(u), "country": COUNTRY, "url": pu, "thread": u, "date": "", "text": t, "is_reply": i > 0}, ensure_ascii=False) + "\n")
        sys.stderr.write("%s %s +%d\n" % (kind, u, n)); time.sleep(1.5)
print("新規投稿", tot)
