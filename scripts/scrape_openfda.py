# openFDA 医療機器の有害事象（MAUDE）から、同型の器具で起きた不具合・苦情の文章を取る
# 「なぜ他の器具は効かなかった・ダメだったか」を第三者の公的記録で返すための材料（器具・家電系の商品で使う）
# 使い方: RESEARCH_DIR=<作業フォルダ> python3 scrape_openfda.py "<検索式>" [件数=200]
#   検索式の例: 'device.generic_name:"tens"'  'device.brand_name:"theragun"'  'device.generic_name:insole'
# 出力: raw/_stage/utter_openfda.jsonl（1報告1行・country=US・in_topic=true）
import os, sys, json, time, urllib.parse, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *

OUT = stage("utter_openfda.jsonl")
Q = sys.argv[1]; N = int(sys.argv[2]) if len(sys.argv) > 2 else 200
seen = set()
if os.path.exists(OUT):
    for l in open(OUT, encoding="utf-8"):
        try: seen.add(json.loads(l)["url"])
        except Exception: pass
got = 0
with open(OUT, "a", encoding="utf-8") as fo:
    for skip in range(0, N, 100):
        u = "https://api.fda.gov/device/event.json?" + urllib.parse.urlencode({"search": Q, "limit": min(100, N - skip), "skip": skip})
        try:
            j = json.loads(urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "research/0.1"}), timeout=60).read())
        except Exception as e:
            sys.stderr.write("stop %s\n" % e); break
        for r in j.get("results", []):
            key = r.get("mdr_report_key") or r.get("report_number")
            url = "https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfmaude/detail.cfm?mdrfoi__id=%s" % key
            if url in seen: continue
            seen.add(url)
            txt = "\n".join(t.get("text", "") for t in r.get("mdr_text", []) if t.get("text"))
            if len(txt) < 40: continue
            dev = (r.get("device") or [{}])[0]
            fo.write(json.dumps({"platform": "FDA MAUDE", "country": "US", "url": url, "date": r.get("date_received", ""),
                                 "text": txt, "is_reply": False, "in_topic": True,
                                 "product": "%s / %s" % (dev.get("brand_name", ""), dev.get("generic_name", "")),
                                 "event_type": r.get("event_type", "")}, ensure_ascii=False) + "\n")
            got += 1
        time.sleep(1)
print("新規報告", got)
