# Reddit のサブレを自動で探して「濃さ」を測る（工程4の生息地マップ・reddit_subs を決める材料）
# 使い方: RESEARCH_DIR=<作業フォルダ> python3 discover_subreddits.py <語幹 例: hip arthrit bursit menopaus chronicpain ...> [--also Sub1,Sub2] [--max-pages 100]
#   出た案は目で見て、名前が似ているだけの無関係なサブレ（hip→hiphop・hippos 等）を消してから config に貼る
#   語幹＝サブレ名の頭の文字（大文字小文字は区別しない）。悩み・病名・体の部位・世代（over40, AskOldPeople）・家族（caregiver）で広めに
#   --also で WebSearch や Engine 1 で見つけたサブレ名を足す
# やること: 候補ごとに直近100投稿を取り、topic_en に当たる割合＝密度を測る
# 出力: analysis/reddit_subs.md（濃い順の表）と、config.json に貼れる reddit_subs / reddit_comment_subs の案
import os, sys, json, re, time, urllib.request, urllib.parse, urllib.error
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *

API = "https://arctic-shift.photon-reddit.com/api/"
TOPIC = rx("topic_en", flags=re.I)
args = sys.argv[1:]; also = []; MAXP = 100   # 巨大サブレ1つで遡る上限（100頁＝1万投稿≒7分）
if "--max-pages" in args:
    i = args.index("--max-pages"); MAXP = int(args[i + 1]); args = args[:i] + args[i + 2:]
if "--also" in args:
    i = args.index("--also"); also = [s for s in args[i + 1].split(",") if s]; args = args[:i] + args[i + 2:]

def get(path, params, tries=6):
    url = API + path + "?" + urllib.parse.urlencode(params)
    for i in range(tries):
        try:
            j = json.loads(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "voc-research/0.2"}), timeout=90).read())
            return j.get("data") or []
        except urllib.error.HTTPError as e:
            if e.code == 400: return []
            time.sleep(5 * (i + 1))
        except Exception: time.sleep(5 * (i + 1))
    return []

cands = {}
for stem in args:
    for x in get("subreddits/search", {"subreddit_prefix": stem, "limit": 40}):
        if x.get("over18"): continue
        k = x["display_name"]
        if k.lower() in {c.lower() for c in cands}: continue   # 大文字小文字違いの同じサブレ
        cands[k] = x.get("subscribers") or 0
    time.sleep(1)
for s in also:
    if s.lower() not in {c.lower() for c in cands}: cands[s] = 0
rows = []
for name, subs in sorted(cands.items(), key=lambda t: -t[1]):
    if subs and subs < 300 and name not in also: continue   # 小さすぎる・空のサブレは飛ばす
    d = get("posts/search", {"subreddit": name, "limit": 100, "sort": "desc", "fields": "title,selftext,created_utc"})
    if not d: continue
    hit = sum(1 for x in d if TOPIC.search((x.get("title") or "") + " " + (x.get("selftext") or "")))
    longp = sum(1 for x in d if len(x.get("selftext") or "") >= 200)
    span = (d[0]["created_utc"] - d[-1]["created_utc"]) / 86400 if len(d) > 1 else 0
    rows.append((name, subs, hit, len(d), longp, round(span, 1)))
    sys.stderr.write("%s 登録%s 当たり%d/%d\n" % (name, subs, hit, len(d))); time.sleep(1)
# 判定は割合でなく「1年あたりの当たり件数」。巨大サブレは割合が低くても量で勝つ
def judge(hit, n, span):
    per_year = hit / max(span, 0.05) * 365
    per_page_days = max(span, 0.05)                      # 100投稿で何日分か
    pages5y = int(min(MAXP * 2, max(5, 5 * 365 / per_page_days)))  # 5年分（上限は --max-pages の2倍）
    if n and hit / n >= 0.5: return "H", per_year, "投稿を全部（null）", [None, pages5y]
    if per_year >= 100 and hit >= 2: return "M", per_year, "投稿を遡って手元で絞る（filter）", ["filter", min(MAXP, max(20, int(3000 / max(hit, 1))))]
    if hit >= 2: return "L", per_year, "コメントを遡る", [None, 60]
    return "-", per_year, "使わない", None
rows.sort(key=lambda r: -judge(r[2], r[3], r[5])[1])
md = "| サブレ | 登録者 | 直近100投稿の当たり | 長文 | 100投稿の期間(日) | 当たり/年(推定) | 密度 | 使い方 |\n|---|---|---|---|---|---|---|---|\n"
posts, comments = [], []
for name, subs, hit, n, longp, span in rows:
    dens, py, use, cfg = judge(hit, n, span)
    if dens in ("H", "M"): posts.append([name, cfg[0], cfg[1]])
    elif dens == "L": comments.append([name, cfg[1]])
    md += "| r/%s | %s | %d/%d | %d | %s | %d | %s | %s |\n" % (name, subs, hit, n, longp, span, py, dens, use)
os.makedirs(os.path.join(RESEARCH_DIR, "analysis"), exist_ok=True)
open(os.path.join(RESEARCH_DIR, "analysis", "reddit_subs.md"), "w", encoding="utf-8").write(md)
print(md)
print(json.dumps({"reddit_subs": posts, "reddit_comment_subs": comments}, ensure_ascii=False))
