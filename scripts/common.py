# master-research の収集・集計スクリプト共通部品
# 作業フォルダ（RESEARCH_DIR、無ければカレント）の config.json を読む。
# config.json の項目（正規表現は文字列で書く）:
#   topic_ja / topic_en   : この痛み・悩みの語（発言を残す条件）
#   age_ja / age_en       : 読み手の年齢層・立場のヒント語
#   promo_ja              : 宣伝・施術者の発言を除く語（省略時は既定）
#   drop                  : 5ch等で明らかに無関係なスレを落とす語
#   emo_en                : Reddit で感情の濃い投稿を優先する語（省略時は既定）
#   reddit_subs           : [[sub, タイトル絞り込み語 or null, 最大ページ数(100件/頁)], ...]
#   fivech                : {"host": "https://xxx.5ch.net", "board": "body"}
import json, os, re, sys

RESEARCH_DIR = os.path.abspath(os.environ.get("RESEARCH_DIR", os.getcwd()))
RAW = os.path.join(RESEARCH_DIR, "raw")          # 1行1発言（convert.py の出力）
STAGE = os.path.join(RAW, "_stage")              # スレッド単位の生データ（各スクレイパーの出力）
os.makedirs(STAGE, exist_ok=True)

DEFAULT_PROMO_JA = r"院長|整体院|治療院|接骨院|整骨院|鍼灸院|当院|ご予約|予約受付|LINE予約|LINE登録|ご来院|施術|お問い合わせ|初回限定|体験レッスン|パーソナルトレーニング|トレーナーの|サロン|セラピスト|理学療法士の|柔道整復師|カウンセリング|公式LINE|\bPR\b|アフィリエイト|楽天ROOM|クーポン|整体師|療術|リラクゼーション|ストレッチ専門|ピラティススタジオ|クリニック院|当クリニック|医師監修|無料相談"
DEFAULT_EMO_EN = (r"cry|cried|tears|scared|terrified|afraid|fear|depress|hopeless|give up|gave up|can't take|cant take|"
                  r"burden|ashamed|embarrass|miss (my|being)|feel (old|useless|like)|husband|wife|my kids|nobody|no one|"
                  r"dismiss|told me|years|ruin|exhaust|frustrat|desperate|anxious|anxiety|worst|hate")

def load_cfg():
    p = os.path.join(RESEARCH_DIR, "config.json")
    if not os.path.exists(p):
        sys.exit("config.json が無い: %s （references/config-example.json を写して埋める）" % p)
    return json.load(open(p, encoding="utf-8"))

CFG = load_cfg()

def rx(key, default=None, flags=0):
    v = CFG.get(key) or default
    if not v:
        return re.compile(r"(?!x)x")  # 何にも当たらない
    return re.compile(v, flags)

def stage(name):
    return os.path.join(STAGE, name)
