# Engine 1：AIの下調べ（裏で回す・出てきた物は全部「リード」）

講義02「2つのエンジンを同時に回す」の Engine 1。速く・広く・自動。**事実としては一度も信じない**（Engine 2＝手で掘った物で確かめてから使う）。
回し方：下の [ ] を埋めて `<作業フォルダ>/engine1/prompt.md` に保存し、ChatGPT Deep Research に投げて**待たずに工程2へ進む**。

```
cd ~/app-venture/research/native-ads/chatgpt && node ask.mjs <作業フォルダ>/engine1/prompt.md <作業フォルダ>/engine1/chatgpt.md
```
（ブラウザの窓が1つ開く・最長40分。ログインが切れていたら `node login.mjs` を本人に1回だけ頼む）

---

```
I'm doing deep market research for [PRODUCT + PDP URL], sold in [JAPAN / US] to people with [PAIN / DESIRE].
Read the product page first. Then research the MARKET, not the brand. Return everything with a source URL per claim.
Treat "product aware" as awareness of SIMILAR products in this category, not of our brand.

1. PRODUCT FACTS
- Every component / ingredient / material / feature of this product. For each: what it does in the body or in use, regulatory status (FDA / 機能性表示 / 医療機器 class) and for what use, the 2-3 strongest studies (author, year, journal, n, result in the study's own wording).

2. AWARENESS & SOPHISTICATION
- Where the bulk of this market sits on Schwartz's 5 awareness stages (with signals: search trends, social chatter, competitor ad style).
- Sophistication stage 1-5: which claims and mechanisms have competitors already used? List them by brand.

3. PSYCHOGRAPHICS (answer each)
- Who is the customer, in emotional state + belief terms (not demographics). Hopes, dreams, victories, failures.
- What outside forces do THEY believe stopped them? Prejudices? Core beliefs in 1-3 sentences.
- Existing solutions they use (list with brand names and prices in this country). What they like / dislike. Horror stories. Do they believe existing solutions work? Why not?
- CURIOSITY: anyone who tried to solve this in a very unique way? Old (pre-1960) or forgotten solutions? A conspiratorial story about why old solutions failed?
- CORRUPTION: a belief that this problem used to not exist or was less bad? Recently worsened by outside forces (modern life, food, screens, work)? What forces?

4. SUB-AVATARS
- 5-8 distinct sub-groups inside this market, each defined by an emotional state + belief + situation (e.g. "diabetic men skeptical of doctors"), with: why this product helps THEM specifically, and evidence they exist (links to threads / reviews / studies).

5. COMPETITORS
- Top 10 competitors in this country (+5 in the US if Japan): offer, price, guarantee, funnel (ad → page → checkout), their mechanism / "why us" story, their longest-running ads, and what customers complain about (1-3 star reviews, Reddit, 知恵袋).

6. VOICE
- 30+ verbatim quotes from real people about the PROBLEM (not products), half from niche communities (condition-specific forums, subreddits, 知恵袋, ガールズちゃんねる, blogs, YouTube comments), in the original language, each with URL. Prioritize rock-bottom moments, things they've never said out loud, what doctors told them, what they tried and why it failed.

7. COUNTER-EVIDENCE
- The strongest evidence AGAINST this product's approach working. Studies with null results. Skeptic communities. What critics say.

Format: headings 1-7. Every claim has a URL. Mark anything you inferred (not sourced) as [INFERRED].
```

---

## 返ってきた後（工程6で使う）

- 文書の頭に **「Engine 1＝リード。全部未確認」** と書く
- 各主張を Engine 2（手で掘った物）と突き合わせて 3色に分ける：**確認済み**（自分で一次資料を開いて同じことを確かめた）／**未確認**（まだ見ていない）／**誤り・作り話**（出典が無い・出典と言っていることが違う）。誤りは赤で残し、二度と使わない
- Engine 1 にしか出てこない競合・サブアバター・出どころは、工程3〜5に戻って手で確かめる（＝Engine 1 の仕事は「見落としの発見」）
