import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
# 日本の声の集計①〜⑤＋感情マップ（JP/EN）。1発言につき各項目は最大1回数える。
# 出力: <作業フォルダ>/analysis/agg.md・agg.json・kw.md
import json, re, glob, collections
D = RAW + "/"
ANA = os.path.join(RESEARCH_DIR, "analysis") + "/"; os.makedirs(ANA, exist_ok=True)
recs = []
for f in glob.glob(D + "*.jsonl"):
    for l in open(f, encoding="utf-8"): recs.append(json.loads(l))
JP = [r for r in recs if r["country"] == "JP"]
EN = [r for r in recs if r["country"] != "JP"]
# 宣伝・施術者らしい発言は集計から除く（本人の声に寄せる）
PRO = re.compile(r"当院|当整体|施術|ご予約|院長|治療家|整体師です|理学療法士です|柔道整復師です|トレーナーです|医師です|看護師です|専門家として|私の整体|患者さん(が|を|に|の)")
_c = collections.Counter(r["text"][:60] for r in JP)
JPv = [r for r in JP if not PRO.search(r["text"]) and _c[r["text"][:60]] < 3]

def count(rs, table):
    c = collections.Counter(); ex = {}
    for r in rs:
        t = r["text"]
        for name, pat in table:
            if re.search(pat, t):
                c[name] += 1
                ex.setdefault(name, r["url"])
    return c, ex

LOC = [tuple(x) if isinstance(x, list) else x for x in CFG.get("loc", [])]
SCENE = [tuple(x) if isinstance(x, list) else x for x in CFG.get("scene", [])]
TRIED = [tuple(x) if isinstance(x, list) else x for x in CFG.get("tried", [])]
RESULT_NEG = r"効かな|効果(が)?な|効き目がな|変わらな|改善しな|良くならな|よくならな|治らな|一時的|その場しのぎ|悪化|余計に|かえって|ひどくな|酷くな|気休め|続かな"
RESULT_POS = r"楽にな|らくにな|マシにな|ましにな|良くな|よくな|改善し|和らい|効いた|効果があ|痛みが(消|取れ|とれ|なくな)"
FEAR = [tuple(x) if isinstance(x, list) else x for x in CFG.get("fear", [])]
EMO_JP = [
 ("不安・恐怖", r"不安|怖い|こわい|恐怖|心配"), ("つらさ・消耗", r"辛い|つらい|しんどい|苦痛|疲れ"), ("悲しみ・涙", r"悲し|泣|涙"),
 ("絶望・諦め", r"絶望|諦め|あきらめ|どうしようもな|もう無理|希望がな"), ("苛立ち・怒り", r"イライラ|腹が立|ムカ|悔し|くやし"),
 ("情けなさ・恥", r"情けな|恥ずかし|みっともな|惨め|みじめ"), ("罪悪感・申し訳なさ", r"申し訳|迷惑|負担"),
 ("孤独・理解されない", r"わかってもらえ|分かってもらえ|理解されな|理解してもらえ|誰にも|孤独"), ("焦り", r"焦|あせ"),
 ("落ち込み・うつ", r"落ち込|鬱|うつ|気が滅入|憂鬱"), ("老いの自覚", r"年寄り|老人|おばあさん|ババア|老け|年を取|歳を取|年取"),
]
EMO_EN = [
 ("fear/anxiety", r"scared|afraid|terrified|fear|anxious|anxiety|worried|worry|panic"), ("exhaustion", r"exhaust|tired|worn out|drained|knackered|fatigue"),
 ("sadness/crying", r"\bcry|cried|tears|sad\b|heartbroken"), ("hopelessness", r"hopeless|give up|gave up|no point|can't take|cannot take|at the end of my tether|end of my rope|despair"),
 ("anger/frustration", r"frustrat|angry|furious|fed up|sick of|annoy"), ("shame/embarrassment", r"embarrass|ashamed|humiliat|self.conscious"),
 ("guilt/burden", r"burden|guilt|let (them|everyone|my family) down|feel useless|useless"), ("isolation/dismissed", r"dismiss|nobody (understand|believe)|no one (understand|believe)|not taken seriously|brushed off|fobbed off|alone"),
 ("depression", r"depress|low mood|miserable"), ("feeling old", r"feel (so )?old|old lady|old woman|elderly|80 year old|ninety|pensioner"),
]

def tbl(title, c, ex, n, key="項目"):
    s = "| 順位 | %s | 件数（発言） | 比率 | 例（URL） |\n|---|---|---|---|---|\n" % key
    for i, (k, v) in enumerate(c.most_common(), 1):
        s += "| %d | %s | %d | %.1f%% | %s |\n" % (i, k, v, 100.0 * v / n, ex[k])
    return "### %s（対象 %d 発言）\n\n" % (title, n) + s + "\n"

md = ""
res = {}
c, ex = count(JPv, LOC); md += tbl("① 痛む場所の呼び方（日本）", c, ex, len(JPv), "呼び方"); res["loc"] = c.most_common()
c, ex = count(JPv, SCENE); md += tbl("② 痛む場面（日本）", c, ex, len(JPv), "場面"); res["scene"] = c.most_common()
# ③ 試した物：言及数＋同じ文（。！？改行区切り）に否定/肯定の結果語がある数
sent_split = re.compile(r"[。！？!?\n]")
c3 = collections.Counter(); neg = collections.Counter(); pos = collections.Counter(); ex3 = {}
for r in JPv:
    sents = [s for s in sent_split.split(r["text"]) if s]
    for name, pat in TRIED:
        hit = [s for s in sents if re.search(pat, s)]
        if not hit: continue
        c3[name] += 1; ex3.setdefault(name, r["url"])
        if any(re.search(RESULT_NEG, s) for s in hit): neg[name] += 1
        if any(re.search(RESULT_POS, s) for s in hit): pos[name] += 1
md += "### ③ 試した物とその結果の言葉（日本・対象 %d 発言）\n\n結果の言葉は、その物に触れた**同じ文**の中に「効かない／変わらない／一時的／悪化…」（否定）か「楽になった／マシになった／良くなった…」（肯定）があるかで数えた。\n\n| 順位 | 試した物 | 言及 | 否定の言葉あり | 肯定の言葉あり | 例（URL） |\n|---|---|---|---|---|---|\n" % len(JPv)
for i, (k, v) in enumerate(c3.most_common(), 1):
    md += "| %d | %s | %d | %d | %d | %s |\n" % (i, k, v, neg[k], pos[k], ex3[k])
md += "\n"; res["tried"] = [(k, v, neg[k], pos[k]) for k, v in c3.most_common()]
c, ex = count(JPv, FEAR); md += tbl("④ 怖がっていること（日本）", c, ex, len(JPv), "怖がっていること"); res["fear"] = c.most_common()
# ⑤ 医者に言われた言葉：「…と言われ」「…って言われ」の直前の句（医療の文脈がある文のみ）
SAID = re.compile(r"([^。！？\n]{0,40}?)(?:」|』)?\s*(?:と|って|て)(?:言われ|いわれ|診断され|告げられ)")
MED = re.compile(r"医|先生|ドクター|Dr|病院|整形|クリニック|診察|診断|レントゲン|MRI")
DOC = [tuple(x) for x in CFG.get("doc", [])]   # 医者・専門家に言われたことの分類 [名前, 正規表現]（案件ごとに config へ）
c5 = collections.Counter(); ex5 = {}; raw5 = collections.Counter(); nsaid = 0
SAIDW = re.compile(r"言われ|いわれ|診断|と言う|と言い|って言|説明され|告げられ|だそうです|と言っ")
DOCW = re.compile(r"医者|医師|先生|ドクター|主治医|整形|病院|クリニック|診察|Dr")
for r in JPv:
    got = set()
    for sn in sent_split.split(r["text"]):
        if not (DOCW.search(sn) and SAIDW.search(sn)): continue
        nsaid += 1
        for name, pat in DOC:
            if name not in got and re.search(pat, sn):
                got.add(name); c5[name] += 1; ex5.setdefault(name, r["url"])
md += tbl("⑤ 医者に言われた言葉（日本・「医者／先生／病院」と「言われた／診断」が同じ文にある文を分類）", c5, ex5, len(JPv), "言われた言葉")
md += "（該当する文の総数：%d）\n\n" % nsaid
res["doc"] = c5.most_common()
# 感情マップ
c, ex = count(JPv, EMO_JP); md += tbl("感情マップ（日本）", c, ex, len(JPv), "感情"); res["emo_jp"] = c.most_common()
c, ex = count(EN, EMO_EN); md += tbl("感情マップ（英語圏）", c, ex, len(EN), "感情"); res["emo_en"] = c.most_common()
open(ANA + "agg.md", "w", encoding="utf-8").write(md)
json.dump(res, open(ANA + "agg.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("JP", len(JP), "JP(施術者除外)", len(JPv), "EN", len(EN))
for k in ("loc", "scene", "fear", "doc", "emo_jp", "emo_en"): print(k, res[k][:6])
print("tried", res["tried"][:6])
# キーワード・用語の出現数（発言数）
KW_JP = [tuple(x) if isinstance(x, list) else x for x in CFG.get("kw_jp", [])]
KW_EN = [tuple(x) if isinstance(x, list) else x for x in CFG.get("kw_en", [])]
def kwc(rs, kws, flags=0):
    out = []
    for k in kws:
        p = re.compile(r"\b%s\b" % re.escape(k), re.I) if flags else re.compile(re.escape(k))
        out.append((k, sum(1 for r in rs if p.search(r["text"]))))
    return sorted(out, key=lambda x: -x[1])
kj = kwc(JPv, KW_JP); ke = kwc(EN, KW_EN, 1)
md2 = "| 用語（日本語） | 出現発言数 |\n|---|---|\n" + "".join("| %s | %d |\n" % x for x in kj if x[1] > 0)
md2 += "\n| Term (English) | 出現発言数 |\n|---|---|\n" + "".join("| %s | %d |\n" % x for x in ke if x[1] > 0)
open(ANA + "kw.md", "w", encoding="utf-8").write(md2)
print("KW_JP", kj[:12]); print("KW_EN", ke[:12])

# 情報源の言及（工程3b：この悩みの読み手が何を信じているか）。config の source_ja: [[名前, 正規表現], ...]
SRC = [tuple(x) for x in CFG.get("source_ja", [])]
if SRC:
    c, ex = count(JPv, SRC)
    md3 = tbl("情報源の言及（日本）", c, ex, len(JPv), "情報源")
    open(ANA + "sources.md", "w", encoding="utf-8").write(md3)
    print("source", c.most_common(8))
