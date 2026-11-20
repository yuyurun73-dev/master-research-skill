# App Store（公開の検索API・レビューのRSS）で、競合アプリの一覧とレビューを取る（アプリのリサーチ用・工程4b/9）
# 使い方:
#   RESEARCH_DIR=<作業フォルダ> python3 scrape_appstore.py search <検索語ファイル> <国コード,カンマ区切り 例 us,gb,jp>
#     → raw/_stage/appstore_apps.jsonl と analysis/apps_<国>.md（評価数の多い順・価格・ジャンル・説明の冒頭）
#   RESEARCH_DIR=<作業フォルダ> python3 scrape_appstore.py reviews <国> <trackId,...> [ページ数=10]
#     → reviews/appstore-<国>-<trackId>.jsonl（1行1レビュー：rating, title, text, version, date, url）。最新順と役立つ順の両方、最大 各500件
# どちらも認証不要の公開エンドポイント（itunes.apple.com）。間を空けて叩く
import os, sys, json, time, urllib.request, urllib.parse, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *

def g(u):
    for i in range(4):
        try: return json.loads(urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"}), timeout=30).read())
        except Exception as e: sys.stderr.write("retry %s %s\n" % (u, e)); time.sleep(3 * (i + 1))
    return {}

mode = sys.argv[1]
if mode == "search":
    terms = [l.strip() for l in open(sys.argv[2], encoding="utf-8") if l.strip() and not l.startswith("#")]
    out = stage("appstore_apps.jsonl"); apps = {}
    if os.path.exists(out):
        for l in open(out, encoding="utf-8"):
            a = json.loads(l); apps[(a["country"], a["trackId"])] = a
    for cc in sys.argv[3].split(","):
        for t in terms:
            j = g("https://itunes.apple.com/search?" + urllib.parse.urlencode({"term": t, "entity": "software", "country": cc, "limit": 50}))
            for rank, a in enumerate(j.get("results", [])):
                k = (cc, a["trackId"])
                rec = apps.get(k) or {"country": cc, "trackId": a["trackId"], "name": a.get("trackName"), "seller": a.get("sellerName"),
                    "rating": round(a.get("averageUserRating") or 0, 2), "ratings": a.get("userRatingCount") or 0, "price": a.get("formattedPrice"),
                    "genre": a.get("primaryGenreName"), "released": (a.get("releaseDate") or "")[:10], "updated": (a.get("currentVersionReleaseDate") or "")[:10],
                    "url": a.get("trackViewUrl", "").split("?")[0], "desc": (a.get("description") or "")[:1500], "terms": []}
                rec["terms"] = sorted(set(rec["terms"]) | {"%s#%d" % (t, rank + 1)})
                apps[k] = rec
            time.sleep(1.5)
    with open(out, "w", encoding="utf-8") as f:
        for a in apps.values(): f.write(json.dumps(a, ensure_ascii=False) + "\n")
    os.makedirs(os.path.join(RESEARCH_DIR, "analysis"), exist_ok=True)
    for cc in sys.argv[3].split(","):
        rows = sorted([a for a in apps.values() if a["country"] == cc], key=lambda a: -a["ratings"])
        md = "| アプリ | 開発 | 評価 | 評価数 | 価格 | ジャンル | 公開 | 更新 | 当たった検索語(順位) |\n|---|---|---|---|---|---|---|---|---|\n"
        for a in rows[:80]:
            md += "| [%s](%s) | %s | %s | %d | %s | %s | %s | %s | %s |\n" % (a["name"].replace("|", "／"), a["url"], (a["seller"] or "").replace("|", "／"), a["rating"], a["ratings"], a["price"], a["genre"], a["released"], a["updated"], " ".join(a["terms"][:4]))
        open(os.path.join(RESEARCH_DIR, "analysis", "apps_%s.md" % cc), "w", encoding="utf-8").write(md)
        print(cc, "アプリ", len(rows))
elif mode == "reviews":
    cc = sys.argv[2]; ids = sys.argv[3].split(","); pages = int(sys.argv[4]) if len(sys.argv) > 4 else 10
    d = os.path.join(RESEARCH_DIR, "reviews"); os.makedirs(d, exist_ok=True)
    for tid in ids:
        seen = set(); rows = []
        for sort in ("mostrecent", "mosthelpful"):
            for p in range(1, pages + 1):
                j = g("https://itunes.apple.com/%s/rss/customerreviews/page=%d/id=%s/sortby=%s/json" % (cc, p, tid, sort))
                es = (j.get("feed") or {}).get("entry") or []
                if isinstance(es, dict): es = [es]
                es = [e for e in es if "im:rating" in e]
                if not es: break
                for e in es:
                    rid = e["id"]["label"]
                    if rid in seen: continue
                    seen.add(rid)
                    rows.append({"source": "appstore", "country": cc, "trackId": tid, "rating": int(e["im:rating"]["label"]), "title": e["title"]["label"],
                                 "text": e["content"]["label"], "version": e.get("im:version", {}).get("label", ""), "date": e.get("updated", {}).get("label", "")[:10],
                                 "url": "https://apps.apple.com/%s/app/id%s?see-all=reviews#%s" % (cc, tid, rid)})
                time.sleep(1)
        with open(os.path.join(d, "appstore-%s-%s.jsonl" % (cc, tid)), "w", encoding="utf-8") as f:
            for r in rows: f.write(json.dumps(r, ensure_ascii=False) + "\n")
        print(cc, tid, "レビュー", len(rows), dict(sorted(collections.Counter(r["rating"] for r in rows).items())))
