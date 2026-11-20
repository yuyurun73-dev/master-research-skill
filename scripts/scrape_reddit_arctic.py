# Reddit（arctic-shift 公開アーカイブAPI）から、投稿＋コメントの木を大量に取る
# 2026-11-18 作り直し：サーバー側の本文・タイトル検索は大きいサブレで時間切れになるので使わない。
#   日付で遡って全投稿を100件ずつ取り（速い）、手元で config の topic_en で絞る。
# 使い方: RESEARCH_DIR=<作業フォルダ> python3 scrape_reddit_arctic.py [posts|comments|all]（既定 all）
# config.json:
#   reddit_subs:          [[サブレ, null(=悩み専門のサブレ。全部残す) or "filter"(=手元で topic_en に当たる物だけ), 遡るページ数(100件/頁)], ...]
#   reddit_comment_subs:  [[サブレ, 遡るページ数], ...]  雑談・世代・家族系の大きいサブレ。コメントを遡って topic_en に当たる物だけ
#   reddit_min_len (200)  reddit_keep_per_sub (200＝コメントの木を取る上位件数)  reddit_keep_all (true＝残りの候補も本文は全部保存)  reddit_replies (80)  reddit_after ("2015-01-01" など・任意)
# 出力: raw/_stage/reddit.jsonl（投稿＋返信）・raw/_stage/utter_reddit_comments.jsonl（コメント単体）
# 途中で止まっても、取った物は残り、再実行で続きから（同じURLは飛ばす）
# 並行で速く回す: REDDIT_ONLY=SubA,SubB を付けて担当を分けた複数本を同時に起動（3本まで。多いと混雑で遅くなる）
import os, sys, json, re, time, urllib.request, urllib.parse, urllib.error
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *

API = "https://arctic-shift.photon-reddit.com/api/"
OUT = stage("reddit.jsonl")
OUTC = stage("utter_reddit_comments.jsonl")
MODE = sys.argv[1] if len(sys.argv) > 1 else "all"
ONLY = set(x for x in os.environ.get("REDDIT_ONLY", "").split(",") if x)   # 並行で回す時の担当サブレ
SUBS = sorted([tuple(x) for x in CFG.get("reddit_subs", [])], key=lambda t: t[1] is not None)   # 悩み専門サブレ（null）を先に
CSUBS = [tuple(x) for x in CFG.get("reddit_comment_subs", [])]
MINLEN = int(CFG.get("reddit_min_len", 200))
KEEP = int(CFG.get("reddit_keep_per_sub", 200))
NREP = int(CFG.get("reddit_replies", 80))
KEEPALL = CFG.get("reddit_keep_all", True)   # 候補の投稿本文は全部残す（コメントの木は上位 KEEP 件だけ）
AFTER = CFG.get("reddit_after")
TOPIC = rx("topic_en", flags=re.I)
EMO = rx("emo_en", DEFAULT_EMO_EN, re.I)
AGE = rx("age_en", flags=re.I)

def get(path, params, tries=8):
    url = API + path + "?" + urllib.parse.urlencode(params)
    for i in range(tries):
        try:
            r = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "voc-research/0.2"}), timeout=90)
            j = json.loads(r.read().decode("utf-8", "replace"))
            if j.get("error"):
                sys.stderr.write("apierr %s\n" % j["error"]); time.sleep(6 * (i + 1)); continue
            return j.get("data") or []
        except urllib.error.HTTPError as e:
            if e.code == 400: sys.stderr.write("bad request %s\n" % url); return []
            time.sleep(6 * (i + 1))   # 422=混雑「slow down」。待って再試行
        except Exception as e:
            if "nodename" in str(e) or "Network is unreachable" in str(e) or "timed out" in str(e):
                # ネットが切れている（スリープ等）。回数を使わずにつながるまで待つ（最大30分）
                for _ in range(30):
                    time.sleep(60)
                    try: urllib.request.urlopen(API + "posts/search?subreddit=AskDocs&limit=1", timeout=20); break
                    except Exception: pass
                continue
            sys.stderr.write("retry %s\n" % e); time.sleep(6 * (i + 1))
    sys.stderr.write("give up %s\n" % url)
    return None

def flatten(tree, out):
    for node in tree:
        d = node.get("data", {}) if isinstance(node, dict) else {}
        b = d.get("body")
        if b and b not in ("[deleted]", "[removed]") and d.get("author") != "AutoModerator" and len(b) > 40:
            out.append({"body": b.strip(), "score": d.get("score", 0), "created_utc": d.get("created_utc")})
        rep = d.get("replies")
        if isinstance(rep, dict): flatten(rep.get("data", {}).get("children", []), out)
        elif isinstance(rep, list): flatten(rep, out)

def seen_urls(p, key="url"):
    s = set()
    if os.path.exists(p):
        for l in open(p, encoding="utf-8"):
            try: s.add(json.loads(l)[key])
            except Exception: pass
    return s

def day(ts): return time.strftime("%Y-%m-%d", time.gmtime(ts)) if ts else ""

def walk(path, sub, pages, fields):
    before = None
    for p in range(pages):
        params = {"subreddit": sub, "limit": 100, "sort": "desc", "fields": fields}
        if before: params["before"] = before
        if AFTER: params["after"] = AFTER
        d = get(path, params)
        if not d: return
        yield d
        before = int(d[-1]["created_utc"])
        time.sleep(1.0)

def do_posts():
    seen = seen_urls(OUT); f = open(OUT, "a", encoding="utf-8"); total = 0
    for sub, filt, pages in SUBS:
        if not pages or (ONLY and sub not in ONLY): continue
        cands, n = [], 0; t0 = time.time()
        sys.stderr.write("START r/%s %s頁 %s\n" % (sub, pages, "全部" if not filt else "絞る")); sys.stderr.flush()
        for d in walk("posts/search", sub, int(pages), "id,title,selftext,created_utc,num_comments,author,score"):
            for x in d:
                n += 1
                st = (x.get("selftext") or "").strip()
                if len(st) < MINLEN or st in ("[deleted]", "[removed]"): continue
                txt = (x.get("title") or "") + "\n" + st
                if filt and not TOPIC.search(txt): continue
                sc = len(EMO.findall(txt)) + 3 * bool(AGE.search(txt)) + min(len(st), 3000) / 1000 + min(x.get("num_comments", 0), 40) / 10
                cands.append((sc, x))
        cands.sort(key=lambda t: -t[0]); keep = cands[:KEEP]
        sys.stderr.write("SUB r/%s 見た%d 候補%d 残す%d %d秒\n" % (sub, n, len(cands), len(keep), time.time() - t0)); sys.stderr.flush()
        # 上位 KEEP 件はコメントの木つき、残りの候補も本文は全部残す（API を叩かないので速い）
        for rank, (sc, x) in enumerate(cands if KEEPALL else keep):
            url = "https://www.reddit.com/r/%s/comments/%s/" % (sub, x["id"])
            if url in seen: continue
            seen.add(url); reps = []
            if rank < KEEP and x.get("num_comments", 0) > 0:
                tree = get("comments/tree", {"link_id": "t3_" + x["id"], "limit": 500}) or []
                flatten(tree, reps); reps.sort(key=lambda r: -(r["score"] or 0)); time.sleep(1.0)
            reps = reps[:NREP]
            f.write(json.dumps({"url": url, "source": "reddit r/" + sub, "country": "EN", "date": day(x["created_utc"]),
                                "title": x.get("title", ""), "text": x.get("title", "") + "\n\n" + x["selftext"].strip(),
                                "score": round(sc, 2), "replies": [r["body"] for r in reps],
                                "reply_dates": [day(r.get("created_utc")) for r in reps]}, ensure_ascii=False) + "\n")
            f.flush(); total += 1
    sys.stderr.write("POSTS WROTE %d\n" % total)

def do_comments():
    seen = seen_urls(OUTC); f = open(OUTC, "a", encoding="utf-8"); total = 0
    for sub, pages in CSUBS:
        if ONLY and sub not in ONLY: continue
        n = hit = 0
        for d in walk("comments/search", sub, int(pages), "id,body,created_utc,link_id,score"):
            for c in d:
                n += 1
                b = (c.get("body") or "").strip()
                if len(b) < 80 or b in ("[deleted]", "[removed]") or not TOPIC.search(b): continue
                url = "https://www.reddit.com/r/%s/comments/%s/_/%s/" % (sub, (c.get("link_id") or "t3_")[3:], c["id"])
                if url in seen: continue
                seen.add(url); hit += 1; total += 1
                f.write(json.dumps({"platform": "Reddit r/%s (comment)" % sub, "country": "EN", "url": url, "date": day(c.get("created_utc")),
                                    "text": b, "is_reply": True, "likes": c.get("score", 0), "in_topic": True}, ensure_ascii=False) + "\n")
            f.flush()
        sys.stderr.write("COMMENTS r/%s 見た%d 残す%d\n" % (sub, n, hit))
    sys.stderr.write("COMMENTS WROTE %d\n" % total)

if MODE in ("posts", "all"): do_posts()
if MODE in ("comments", "all"): do_comments()
