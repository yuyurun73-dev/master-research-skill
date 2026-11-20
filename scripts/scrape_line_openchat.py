# LINEオープンチャット：検索語ごとに「部屋の名前・説明・人数・最終発言」を取る（会話の中身はアプリで参加しないと見えない）
# 40代以上の日本人はLINE利用率9割超（総務省 令和6年度：40代94.8%・50代94.5%・60代91.1%）。悩みごとの部屋＝生息地とサブアバターの名前がそのまま出る
# 使い方: RESEARCH_DIR=<作業フォルダ> python3 scrape_line_openchat.py <検索語ファイル>
# 出力: raw/_stage/utter_openchat.jsonl（部屋の説明＝管理人が書いた原文。in_topic）／analysis/openchat_rooms.md（人数順の部屋一覧＝本人が手で参加する候補）
import os, sys, re, json, time, html, urllib.request, urllib.parse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
OUT = stage("utter_openchat.jsonl")
QS = [l.strip() for l in open(sys.argv[1], encoding="utf-8") if l.strip() and not l.startswith("#")]
def txt(s): return html.unescape(re.sub(r"<[^>]+>|<!--.*?-->", "", s)).strip()
rooms = {}
for q in QS:
    try:
        h = urllib.request.urlopen(urllib.request.Request("https://openchat.line.me/jp/search?keyword=" + urllib.parse.quote(q), headers={"User-Agent": UA, "Accept-Language": "ja"}), timeout=30).read().decode("utf-8", "replace")
    except Exception as e:
        sys.stderr.write("skip %s %s\n" % (q, e)); continue
    n = 0
    for m in re.finditer(r'<a href="(/jp/cover/[^"?]+)[^"]*" class="list_link">(.*?)</a>', h, re.S):
        b = m.group(2)
        t = re.search(r'<strong class="tit">(.*?)</strong>', b, re.S); d = re.search(r'<span class="desc">(.*?)</span>', b, re.S)
        mem = re.search(r'<span class="member">\D*(\d[\d,]*)', b); tm = re.search(r'<time class="time">(.*?)</time>', b)
        url = "https://openchat.line.me" + m.group(1)
        if url in rooms: continue
        rooms[url] = {"title": txt(t.group(1)) if t else "", "desc": txt(d.group(1)) if d else "", "members": int(mem.group(1).replace(",", "")) if mem else 0, "last": txt(tm.group(1)) if tm else "", "query": q}
        n += 1
    sys.stderr.write("%s +%d\n" % (q, n)); time.sleep(1.5)
with open(OUT, "w", encoding="utf-8") as fo:
    for u, r in rooms.items():
        fo.write(json.dumps({"platform": "LINEオープンチャット（部屋の説明）", "country": "JP", "url": u, "date": "", "title": r["title"],
                             "text": r["title"] + "\n" + r["desc"], "is_reply": False, "likes": r["members"], "in_topic": True}, ensure_ascii=False) + "\n")
md = "| 部屋 | 人数 | 最終発言 | 説明（冒頭） | 見つけた語 |\n|---|---|---|---|---|\n"
for u, r in sorted(rooms.items(), key=lambda t: -t[1]["members"]):
    md += "| [%s](%s) | %d | %s | %s | %s |\n" % (r["title"].replace("|", "／"), u, r["members"], r["last"], r["desc"][:60].replace("|", "／").replace("\n", " "), r["query"])
os.makedirs(os.path.join(RESEARCH_DIR, "analysis"), exist_ok=True)
open(os.path.join(RESEARCH_DIR, "analysis", "openchat_rooms.md"), "w", encoding="utf-8").write(md)
print("部屋", len(rooms), "合計メンバー", sum(r["members"] for r in rooms.values()))
