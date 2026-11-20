# YouTube：検索上位の動画のコメントを取る（体験談・解説動画の下は濃い声が溜まる）
# 使い方: RESEARCH_DIR=<作業フォルダ> python3 scrape_youtube_comments.py <検索語ファイル> [1語あたりの動画数=5] [1動画あたりのコメント上限=300]
# 出力: raw/_stage/utter_youtube.jsonl（1行1コメント・in_topic=true）
# 注意: 連続で回すとYouTubeにbot判定される。動画は多くて合計40本まで・語ごとに間を空ける
import os, sys, json, subprocess, time, tempfile, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *

OUT = stage("utter_youtube.jsonl")
QUERIES = [l.strip() for l in open(sys.argv[1], encoding="utf-8") if l.strip() and not l.startswith("#")]
PER = int(sys.argv[2]) if len(sys.argv) > 2 else 5
MAXC = int(sys.argv[3]) if len(sys.argv) > 3 else 300
COUNTRY = os.environ.get("COUNTRY", "JP")
seen = set()
if os.path.exists(OUT):
    for l in open(OUT, encoding="utf-8"):
        try: seen.add(json.loads(l)["cid"])
        except Exception: pass
n_new = 0
with open(OUT, "a", encoding="utf-8") as fo:
    for q in QUERIES:
        with tempfile.TemporaryDirectory() as td:
            cmd = ["yt-dlp", "ytsearch%d:%s" % (PER, q), "--skip-download", "--write-comments", "--no-warnings", "-q",
                   "--extractor-args", "youtube:max_comments=%d,all,50;comment_sort=top" % MAXC,
                   "--sleep-requests", "1", "-o", os.path.join(td, "%(id)s.%(ext)s")]
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=900)
            if r.returncode != 0 and "Sign in to confirm" in (r.stderr or ""):
                sys.exit("YouTubeにbot判定された。ここで止める（時間を置く）。")
            for p in glob.glob(os.path.join(td, "*.info.json")):
                info = json.load(open(p, encoding="utf-8"))
                url = "https://www.youtube.com/watch?v=" + info["id"]
                for c in info.get("comments") or []:
                    if c.get("id") in seen or not c.get("text"): continue
                    seen.add(c["id"])
                    ts = c.get("timestamp")
                    fo.write(json.dumps({"platform": "YouTubeコメント", "country": COUNTRY, "url": url + "&lc=" + c["id"], "cid": c["id"],
                        "date": time.strftime("%Y-%m-%d", time.gmtime(ts)) if ts else "", "text": c["text"], "is_reply": c.get("parent") != "root",
                        "likes": c.get("like_count", 0), "title": info.get("title", ""), "in_topic": True, "query": q}, ensure_ascii=False) + "\n")
                    n_new += 1
        sys.stderr.write("%s → 累計 %d\n" % (q, n_new)); time.sleep(5)
print("新規コメント", n_new)
