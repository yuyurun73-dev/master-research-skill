import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
# _stage/*.jsonl（スレッド単位）→ raw/<platform>.jsonl（1行1発言）
# 項目: platform, country, url, date, author_age_hint, text(原文全文), is_reply
import json, re, os, glob, collections, html
D = RAW + "/"
S = STAGE + "/"
HIP_JA = rx("topic_ja")
HIP_EN = rx("topic_en", flags=re.I)
PROMO = rx("promo_ja", DEFAULT_PROMO_JA)
AGE_JA = rx("age_ja")
AGE_EN = rx("age_en", flags=re.I)

def age_hint(t, ja=True):
    m = (AGE_JA if ja else AGE_EN).findall(t)
    return "・".join(list(dict.fromkeys(m))[:4]) if m else ""

def rd(name):
    p = S + name
    if not os.path.exists(p): return []
    out = []
    for l in open(p, encoding="utf-8"):
        try: out.append(json.loads(l))
        except Exception: pass
    return out

out = collections.defaultdict(list)
seen = set()
def add(platform, country, url, date, text, is_reply, ja=True, extra=None):
    text = html.unescape((text or "")).strip()
    if len(text) < 20: return
    key = (url, text[:200])
    if key in seen: return
    seen.add(key)
    rec = {"platform": platform, "country": country, "url": url, "date": date or "", "author_age_hint": age_hint(text, ja), "text": text, "is_reply": is_reply}
    if extra: rec.update(extra)
    out[platform].append(rec)

# 知恵袋：質問が悩みの語(topic_ja)に当たるものだけ。質問＋全回答
for d in rd("chiebukuro.jsonl"):
    q = d.get("question") or d.get("text", "")
    if not HIP_JA.search(q + d.get("title", "")): continue
    add("Yahoo!知恵袋", "JP", d["url"], d.get("date", ""), q, False)
    for r in d.get("replies", []) or []:
        add("Yahoo!知恵袋", "JP", d["url"], d.get("date", ""), r, True)

# ブログ系：宣伝（整体院・治療院等）を除外、悩みの語を含むもの
for name, plat in (("ameba.jsonl", "Amebaブログ"), ("note.jsonl", "note"), ("hatena.jsonl", "はてなブログ")):
    for d in rd(name):
        t = d.get("text", "")
        if not HIP_JA.search(t + d.get("title", "")): continue
        if len(PROMO.findall(t + d.get("title", ""))) >= 2: continue
        add(plat, "JP", d["url"], d.get("date", ""), (d.get("title", "") + "\n\n" + t) if d.get("title") else t, False)

# 5ch：悩みの語を含む書き込みだけ（スレ題が当たれば全レス）
for d in rd("fivech.jsonl"):
    title_hip = bool(HIP_JA.search(d.get("title", "")))
    parts = d.get("text", "").split("\n\n【レス】\n")
    op = parts[0]; reps = d.get("replies", []) or []
    if title_hip or HIP_JA.search(op): add("5ちゃんねる", "JP", d["url"], d.get("date", ""), op, False)
    for r in reps:
        if title_hip or HIP_JA.search(r): add("5ちゃんねる", "JP", d["url"], d.get("date", ""), r, True)

# ガールズちゃんねる：コメントごと。悩みの語を含むコメントのみ
for d in rd("girlschannel.jsonl"):
    for chunk in re.split(r"\n\n(?=\d+\. )", d.get("text", "")):
        m = re.match(r"(\d+)\. (.*)", chunk, re.S)
        if not m: continue
        body = m.group(2).strip()
        if not HIP_JA.search(body): continue
        add("ガールズちゃんねる", "JP", d["url"], d.get("date", ""), body, m.group(1) != "1")

# X：悩みの語を含み、宣伝っぽいもの（PROMO語・URLだらけ・ハッシュタグ3個以上）を除外
for name in ("x_raw.jsonl",):
    for d in rd(name):
        t = d.get("text", "")
        if not HIP_JA.search(t): continue
        if PROMO.search(t) or t.count("#") >= 3 or re.search(r"https?://", t) and len(t) < 80: continue
        add("X", "JP", d["url"], (d.get("time") or "")[:10], t, False)

# Reddit：投稿＋コメント（コメントは悩みの語なしでも返信として保持）
for d in rd("reddit.jsonl"):
    add("Reddit " + d.get("source", "").replace("reddit ", ""), "EN", d["url"], d.get("date", ""), d.get("text", ""), False, ja=False)
    for i, r in enumerate(d.get("replies", []) or []):
        rdts = d.get("reply_dates") or []
        add("Reddit " + d.get("source", "").replace("reddit ", ""), "EN", d["url"], rdts[i] if i < len(rdts) else "", r, True, ja=False)

# その他英語（既に1行1発言形式のもの）
for name in ("mayo.jsonl", "mumsnet.jsonl", "agingcare.jsonl", "webmd.jsonl", "other_en.jsonl"):
    for d in rd(name):
        if "platform" in d:
            add(d["platform"], d.get("country", "EN"), d["url"], d.get("date", ""), d["text"], d.get("is_reply", False), ja=False, extra={k: v for k, v in d.items() if k == "note"})
        else:
            add(d.get("source", name), d.get("country", "US"), d["url"], d.get("date", ""), d.get("text", ""), False, ja=False)
            for r in d.get("replies", []) or []:
                add(d.get("source", name), d.get("country", "US"), d["url"], d.get("date", ""), r, True, ja=False)

# 汎用の口：_stage/utter_<媒体>.jsonl（1行1発言。platform, country, url, date, text, is_reply）
# ニッチな出どころ（YouTubeのコメント・TikTokのコメント・レビュー・Q&Aサイト等）はこの形で置けば乗る。
# in_topic: true の行（その悩みの動画・商品の下のコメント等）は語の絞り込みをしない
for p in sorted(glob.glob(S + "utter_*.jsonl")):
    for d in rd(os.path.basename(p)):
        ja = d.get("country", "JP") == "JP"
        t = d.get("text", "")
        if not d.get("in_topic") and not (HIP_JA if ja else HIP_EN).search(t + d.get("title", "")): continue
        if ja and len(PROMO.findall(t)) >= 2: continue
        add(d.get("platform") or os.path.basename(p)[6:-6], d.get("country", "JP"), d["url"], d.get("date", ""), t, d.get("is_reply", False), ja=ja,
            extra={k: v for k, v in d.items() if k in ("rating", "product", "likes", "title")})

FN = {"Yahoo!知恵袋": "chiebukuro", "Amebaブログ": "ameba", "note": "note", "はてなブログ": "hatena", "5ちゃんねる": "5ch", "ガールズちゃんねる": "girlschannel", "X": "x", "Mayo Clinic Connect": "mayo", "Mumsnet": "mumsnet"}
for f in glob.glob(D + "*.jsonl"): os.remove(f)
grp = collections.defaultdict(list)
for plat, recs in out.items():
    fn = FN.get(plat) or ("reddit" if plat.startswith("Reddit") else re.sub(r"\W+", "_", plat.lower()))
    grp[fn] += recs
for fn, recs in grp.items():
    with open(D + fn + ".jsonl", "w", encoding="utf-8") as f:
        for r in recs: f.write(json.dumps(r, ensure_ascii=False).encode("utf-8", "replace").decode("utf-8") + "\n")  # 壊れた絵文字（片割れのサロゲート）で止まらないように
tot = collections.Counter(); thr = collections.defaultdict(set); age = collections.Counter()
for plat, recs in out.items():
    for r in recs:
        tot[(r["country"], plat)] += 1; thr[(r["country"], plat)].add(r["url"])
        if r["author_age_hint"]: age[r["country"]] += 1
for k in sorted(tot): print(k, "発言", tot[k], "スレ/記事", len(thr[k]))
print("JP 発言計", sum(v for k, v in tot.items() if k[0] == "JP"), "EN 発言計", sum(v for k, v in tot.items() if k[0] != "JP"))
print("年齢・属性ヒントあり", dict(age))
