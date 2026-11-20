# VoCリサーチ：股関節の痛み（MELAO® アーチサポートインソール／native-ads 工程1）

- 作成日：2026-11-09
- 対象：日本の50〜75歳の女性（主婦・立ち仕事・介護・パート）／英語圏 women 50+ with hip pain
- 集めたのは**商品ではなく「問題」**。商品レビュー・整体院や治療院の宣伝記事は集計から外した。
- 生データ：`~/app-venture/research/native-ads/melao-insole/raw-hip/*.jsonl`（1行1発言：platform, country, url, date, author_age_hint, text（原文全文）, is_reply）
- 引用はすべて原文のまま（日本語は日本語、英語は英語）。各引用の末尾に `[媒体/国](URL)`。
- 注意：知恵袋・5ch・ガルちゃんの「回答／レス」には年齢・性別不明の人や医療職も混じる。年齢・属性が本文から読めた発言は `author_age_hint` に入れてある（例：50代・主婦・孫・介護）。

## 0. 集めた件数

<!--COUNTS-->

### 到達できなかった／一部だけのソース

| ソース | 状態 | 理由 |
|---|---|---|
| Reddit（ブラウザ・公式JSON） | 不可 | 素のHTTPは403。ブラウザ自動操作は権限で拒否（検知回避扱い）。→ 公開アーカイブAPI（arctic-shift）に切り替えて取得。ただし同APIも大きいサブレ（r/ChronicPain, r/Menopause 等）の検索はサーバー側タイムアウトが続き、取れたのは r/HipDysplasia・r/AskWomenOver40・r/over60 の3つ（計71スレ）。途中で止めた |
| Mayo Clinic Connect | 一部のみ（抜粋9件） | curl は403。承認済みの取得ツールでは読めたが本文を丸ごとファイルに落とせないため、画面に出た部分を逐語で保存した（`mayo.jsonl` の note 欄に明記） |
| HealthUnlocked | 不可 | 本文がブラウザ描画でしか出ない作り（HTMLに本文が無い）。ブラウザ自動操作は不可 |
| Patient.info / BoneSmart / Quora | 不可 | いずれも403 |
| WebMD Forums | 未取得 | 掲示板トップは届くが股関節スレの一覧が取れず、時間内に断念 |
| AgingCare | 未取得 | 届くが検索結果がJS描画で、スレの多くが「親の骨折」の介護相談（本人の股関節痛ではない） |
| Facebookグループ | 不可 | ログイン必須（ログイン自動化は禁止ルール） |
| 教えて!goo | 不可 | サービス終了（前例どおり） |
| 発言小町 | 未実施 | 前例で404。今回は再試行せず |
| Amazon/楽天レビュー | 意図的に除外 | 指示書の「商品レビューは捨てる」に従った |
| X（後半の検索語） | 一部0件 | 1回目の後半8語が取得制限で0件→時間を置いて再実行し回収 |

---

## 1. Verbatim Language Bank（原文のまま）

### 1-A 日本語

#### ① 問題そのものを説明する言葉（場所・場面・痛み方）

- 「のはきずらさ、足の爪がきりにくい、歩行の痛み、日々両足に痛みがあり、最近は少しの時間の買い物も辛く、座ってても常に痛みがあります。」 [Yahoo!知恵袋/JP・42歳](https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q13217564273) ※原文はこの直前の行が「靴下」
- 「症状としては、長い距離を歩けない、階段が手すりなしでは上がれない、台所仕事が辛い、夜、足の痛みで良く眠れない、床に座ったときの立ち上がりが難しいなどです。」 [Yahoo!知恵袋/JP](https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q11295790671)
- 「しゃがむと何かに全体重乗せないと痛すぎて立ち上がれないし、両足の太ももの前側が常に痛い、ふくらはぎも痛くなってきています。」 [Yahoo!知恵袋/JP・50代](https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q14324569644)
- 「そのうち、靴下やズボンを履くのも不自由になり、ついには、右足の付け根がギシギシと錆びついたように動かせなくなって、私はサンパウロの日本病院を受診した。」 [note/JP・50過ぎ](https://note.com/amanda816/n/n383da4aceca9)
- 「恐怖は交差点の青信号の点滅。（これは股関節痛い人あるあるじゃないかな）」 [note/JP・50〜60代](https://note.com/momokuri_san/n/n8fb8b86feb71)
- 「エレベーターがあるかを駅構内図で確認してからでかけるようになっていました」 [note/JP・50〜60代](https://note.com/momokuri_san/n/n8fb8b86feb71)
- 「2週間前から左の股関節が痛く、夜寝ていると寝返りする時に痛み、朝起きる時に痛み、椅子に座っててふと足を動かしたら痛み」 [Yahoo!知恵袋/JP](https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q10310685060)
- 「横向きに足を丸めて寝てもしばらく経つと外側太ももの付け根が痛くなります。」 [Yahoo!知恵袋/JP](https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q11260253156)
- 「立ち上がる時や靴下履くときズキッと痛みます。」 [Yahoo!知恵袋/JP](https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q11251656861)
- 「階段なんか怖すぎるし、しゃがむことは出来るけどそこから支えなしで立つのは本当に無理です。」 [Yahoo!知恵袋/JP](https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q12287479177)
- 「普通に歩き出すことすら怖く感じ、一気に不安が押し寄せました。」 [Amebaブログ/JP](https://ameblo.jp/83chanmegu90/entry-12977712876.html)
- 「入浴介助トイレなどすると仕事が終わると痛い階段の登り降り」 [Yahoo!知恵袋/JP・介護職](https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q13243187788)
- 「かつての自分からは信じられないほど歩けなくなってしまいました。」 [Amebaブログ/JP・変形性股関節症末期](https://ameblo.jp/aozoratomidori1234/entry-12983800781.html)
- 「座ると強い痛みが走る…は特に、周りにもいないし検索にも引っかからないし先生にも首を傾げられ困っています」 [Yahoo!知恵袋/JP](https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q11306163221)
- 「私はもう階段を昇れない」 [note/JP・50〜60代](https://note.com/momokuri_san/n/n8fb8b86feb71)
- 「最近は寝ていて痛みが股関節から足首の方へ痛みが繋がり、歩けなくなる不安が起きます。」 [Yahoo!知恵袋/JP・介護経験](https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q11294765066)

#### ② どう感じているかの言葉

- 「今にも股関節が激痛で泣きそうですというか泣いてます。」 [Yahoo!知恵袋/JP](https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q13307614793)
- 「うまく動けないことにもどかしさを感じたり、痛みを感じることが憂鬱で辛くなります。」 [Yahoo!知恵袋/JP・50歳女性](https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q12274466862)
- 「日に日に悪く痛くなり、憂鬱です。」 [Yahoo!知恵袋/JP・60代](https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q12319630597)
- 「60代も終わりになって来たから仕方ないかもしれないけど、手術が怖いです。」 [Yahoo!知恵袋/JP・60代](https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q12319630597)
- 「異常なしと言われ痛いのに原因すら分からなくて毎日気分が落ち込んでしまいます。」 [Yahoo!知恵袋/JP](https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q12234614402)
- 「歳をとるにつれて歩くのが辛くなっていったりするのかと思うと辛いです。」 [Yahoo!知恵袋/JP・60代の母について](https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q12295114272)
- 「これから、先不安ですし、今は行動が制限されて辛いです。」 [Yahoo!知恵袋/JP](https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q10110797495)
- 「生まれる前からの右足股関節脱臼の体が情けなくてもどかしくてたまらん、もういやや。」 [Amebaブログ/JP](https://ameblo.jp/aozoratomidori1234/entry-12978681190.html)
- 「ほとんどもうこの部屋の中で過ごすしかなく自分の中に希望を見いだせず。」 [Amebaブログ/JP](https://ameblo.jp/aozoratomidori1234/entry-12978681190.html)
- 「辛い、車がね片道10分といえどもう無理なのでね、辛すぎる。」 [Amebaブログ/JP](https://ameblo.jp/aozoratomidori1234/entry-12978681190.html)
- 「だけど、やっぱり怖くて、自分にとって体の中に人工物が入ることがこんなに怖いことだとは思わなかった。」 [5ちゃんねる 変形性股関節症スレ17/JP](https://rio2016.5ch.net/test/read.cgi/body/1548762174/)
- 「手術が怖いのと安全なのはわかるんだけど人工のものが体内に入るのが恐怖でしかない…」 [X/JP](https://x.com/suouasagi/status/922163809707483136)
- 「早いと言われながら、なんとか痛みを我慢し、12年経ちましたが、もう我慢の限界で手術を決めました。」 [Yahoo!知恵袋/JP・45歳](https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q14331742634)
- 「術後の痛みや脱臼、初めて体重を乗せることなど不安で仕方ありません。」 [Yahoo!知恵袋/JP・45歳](https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q14331742634)
- 「人工股関節置換術をすれば、これらの痛みは改善されるかどうか不安でしかありません。」 [Yahoo!知恵袋/JP・50代](https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q14324569644)
- 「情けなくないよ、私も寂しくて、辛くて、苦しくて、一人になれた時に大泣きしてるよ。」 [5ちゃんねる 変形性股関節症雑談スレ/JP](https://rio2016.5ch.net/test/read.cgi/body/1556331153/)
- 「泣きたいけど一人になれる場所ないから泣けないのが辛くて。」 [5ちゃんねる 変形性股関節症雑談スレ/JP](https://rio2016.5ch.net/test/read.cgi/body/1556331153/)
- 「行きたいとこにも行けない生活は辛いですね。」 [5ちゃんねる 変形性股関節症スレ19/JP](https://rio2016.5ch.net/test/read.cgi/body/1596109739/)
- 「そんな説明をぼんやり聞きながら、老いて車椅子に乗る自分の姿を思い浮べた。」 [note/JP・50過ぎ](https://note.com/amanda816/n/n383da4aceca9)
- 「「生まれつき」なんて、50過ぎになって言われても全然ピンと来なかった。今さらそんなのありか、と思った。」 [note/JP・50過ぎ](https://note.com/amanda816/n/n383da4aceca9)

#### ③ 試したこと（と、なぜダメだったか）

- 「整体に通っていますが良くならず」 [Yahoo!知恵袋/JP](https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q14284565819)
- 「１年ほど週二回のリハビリに通いましたが徐々に悪化する方向でした。」 [Yahoo!知恵袋/JP](https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q10298083645)
- 「リハビリしても多分治らない気がするので行ってないです。」 [Yahoo!知恵袋/JP](https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q14264006779)
- 「リハビリも何度かいったが良くならない。」 [Yahoo!知恵袋/JP・介護職](https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q13243187788)
- 「ストレッチをしても、良くなるかどころか痛みがない日ガないくらい痛く」 [Yahoo!知恵袋/JP・50代](https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q14324569644)
- 「ロキソニンも効かなくなってきてしまいました。」 [5ちゃんねる 変形性股関節症スレ16/JP](https://rio2016.5ch.net/test/read.cgi/body/1536036673/)
- 「痛み止めと湿布もらってるけど効かないので、来月MRI予約しました。」 [5ちゃんねる 変形性股関節症スレ19/JP](https://rio2016.5ch.net/test/read.cgi/body/1596109739/)
- 「整形外科行ってレントゲン撮っても異常はなくジクロフェナク貰ったのですが効果ありません。」 [Yahoo!知恵袋/JP](https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q14320894329)
- 「整形外科に行ってレントゲンを撮っても異常はなく、湿布を処方され少しは和らぎますが、しばらくするとまたなります。」 [Yahoo!知恵袋/JP](https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q10306531600)
- 「今までは接骨院とかで週1マッサージとかを受けていましたが､保険適用外のため高いしすぐに痛みが出てくるので､整形外科に行ってみようと思うのですが」 [Yahoo!知恵袋/JP](https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q13303335568)
- 「母が股関節に人工関節入れたんだけど、専門の病院で入院してる人みんな言ってたけど、サプリたくさん飲んだけどまったく効かないって言ってた。」 [ガールズちゃんねる/JP](https://girlschannel.net/topics/3465528/)
- 「手元には整形外科で処方された痛み止め、通常用と強めの2種類。」 [note/JP・50〜60代](https://note.com/momokuri_san/n/n8fb8b86feb71)
- 「勝負の日（仕事で絶対歩けないとダメな日など）に強めのを飲む、、、とだんだん痛みが増していきました。」 [note/JP・50〜60代](https://note.com/momokuri_san/n/n8fb8b86feb71)
- 「このまま整形に通ってるだけでいいのか不安になりました…。」 [Yahoo!知恵袋/JP・60代の母について](https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q12295114272)

#### ④ こうなってほしい・こういう物があれば（願い）

- 「手術後は立ったり座ったり、しゃがんだり、普通にできるようになりますか？」 [Yahoo!知恵袋/JP・50代](https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q14324569644)
- 「車の運転や、自転車、階段の上り下り、足の爪切り、正座や床からの立ち上がりなどできるようになるのでしょうか。」 [Yahoo!知恵袋/JP・45歳](https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q14331742634)
- 「数ヶ月後には痛みが取れて、元通りに回復するのでしょうか。」 [Yahoo!知恵袋/JP・45歳](https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q14331742634)
- 「注射とか、直してくれる飲み薬、あったら何でも教えて下さい^_^」 [Yahoo!知恵袋/JP・60代](https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q12319630597)
- 「股関節の軟骨に効くサプリメント、他こうしたら良かったという事があったら教えて下さい。」 [Yahoo!知恵袋/JP・60代](https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q12319630597)
- 「少しでも楽な無理せず出来る介護の仕事があるといいけど無理ですよね！」 [Yahoo!知恵袋/JP・介護職](https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q13243187788)
- 「歩けなくなったり、安静時にも痛むようになってからでは手遅れですか？」 [Yahoo!知恵袋/JP・80代の母について](https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q12322017487)
- 「それとも、手押し車を買って、歩ける範囲で運動した方がいいですか？」 [Yahoo!知恵袋/JP・80代の母について](https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q12322017487)
- 「健康で家族に迷惑をかけない生活を送りたい為、不快なまま生活したくなく」 [Yahoo!知恵袋/JP](https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q13319886973)

#### ⑤ 医者に言われた言葉（逐語）

- 「レジの立ちっぱなしの仕事は一番良くないので辞めてしまうか」 [Yahoo!知恵袋/JP・50代主婦・レジ勤続5年](https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q12150863512)
- 「医者には1回目行った時に若いのでまだ手術はしない方がいいかもと言われ、上の先生と相談してみます。」 [Yahoo!知恵袋/JP・42歳](https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q13217564273)
- 「痛みが続くようなら手術も視野に入れて下さいと言われました。」 [Yahoo!知恵袋/JP・42歳](https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q13217564273)
- 「あとは自分の意思です。と言われたのですが…手術はやはり抵抗もあります」 [Yahoo!知恵袋/JP・42歳](https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q13217564273)
- 「4段階あるとか医者からは言われず、色々ネットで調べて段階があるんだと知りました。」 [Yahoo!知恵袋/JP・42歳](https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q13217564273)
- 「医師からは「変形性股関節症の人は老化も早いから」と言われてしまって子供の将来とかを思うと申し訳なくなってました。」 [ガールズちゃんねる/JP](https://girlschannel.net/topics/4948253/)
- 「先生も「完全に治そうとしたら手術にはなるね」と言ってるそうで、母は手術には否定的です。」 [Yahoo!知恵袋/JP・60代の母について](https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q12295114272)
- 「当時診て頂いた先生に”癌で例えるなら末期だ”と言われた覚えがあります。」 [Yahoo!知恵袋/JP](https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q12149244507)
- 「診てくださった先生はレントゲンを見て｢骨がボコボコしちゃってるなぁ…20度…うーん｣と言っていたのは聞こえました。」 [Yahoo!知恵袋/JP](https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q13303885163)
- 「手術をしても2年もつかどうか、そしてリハビリもきついとかでお医者様からいわれました。」 [Yahoo!知恵袋/JP](https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q1425502144)
- 「「痛みがそれほどでないなら、年齢的にもう少し先にした方がいい」とおっしゃる先生。」 [Yahoo!知恵袋/JP](https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q10113993745)
- 「医者も、年齢と命に関わるわけではないので、無理に手術は勧めません。」 [Yahoo!知恵袋/JP・80代の母について](https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q12322017487)
- 「医師は、このまま放置すれば、そのうち痛みで歩けなくなる。いつか人工股関節を入れることになるだろう、と不吉な予言のように続けた。」 [note/JP・50過ぎ](https://note.com/amanda816/n/n383da4aceca9)
- 「膝痛いし、しまいには脚の付け根まで痛くなったから医者行ったら、先生優しく詳しく解説してくれたけど、結局は『年齢のせい』だった悲しい。」 [X/JP](https://x.com/KuemieQuemie/status/1961302092804665433)
- 「生まれつきの臼蓋形成不全という股関節の疾患を、長年地元の整形外科に通っていても認識されず変形性股関節症になり」 [X/JP](https://x.com/Happy63romi/status/1905109895638135220)

**「レントゲンは異常なし」系**

- 「数日前に整形外科で股関節のレントゲンを撮ってもらいましたが、臼蓋形成不全ではないし、股関節に異常はないと言われました。」 [Yahoo!知恵袋/JP](https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q14324071024)
- 「股関節が痛くて病院に行ったんですが、レントゲンもMRIも異常なしでした。」 [Yahoo!知恵袋/JP](https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q10309855790)
- 「レントゲン撮ったけど異常なくてむしろ股関節綺麗ですとか言われた。」 [X/JP](https://x.com/sykyk_ykk/status/1201435238896766976)
- 「レントゲンでは腰には異常がなく、若い人の骨みたいだと言われました。」 [5ちゃんねる 変形性股関節症スレ20/JP](https://rio2016.5ch.net/test/read.cgi/body/1655220701/)
- 「一度整形外科でレントゲンを撮った時には、骨に異常はなかったのですが、何が痛みの原因なのかよく分かりません。」 [Yahoo!知恵袋/JP](https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q13330006388)
- 「整形外科に行きレントゲンを撮りましたが異常なしで、おそらく寒さからくる強張りかなって診断ロキソニンと湿布を頂きましたが改善されません。」 [Yahoo!知恵袋/JP](https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q12254752637)

#### ⑥ 人目・家族・仕事（関係のひずみ）

- 「私と一緒に買い物に行っても母は杖をついているために歩きが遅くて、そのあまりにも昔の姿との変化に恥ずかしながら母と一緒に隣を歩くのが恥ずかしいのです。」 [Yahoo!知恵袋/JP・娘から見た母](https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q1485758009)
- 「それでも全然ついて行けなくて、お願いだから気にせずに置いて行ってくれ、と懇願した。」 [note/JP・50過ぎ](https://note.com/amanda816/n/n383da4aceca9)
- 「見栄をはって、というか友人に気を使わせたくなくて無理して同じ速さで歩いたりしてました。」 [note/JP・50〜60代](https://note.com/momokuri_san/n/n8fb8b86feb71)
- 「私はホントに足が痛くて一緒に走れない」 [note/JP・50〜60代](https://note.com/momokuri_san/n/n8fb8b86feb71)
- 「毎日送ったりお迎えに行って抱きついて来てくれてた孫を思い出して涙…涙…ばかり」 [5ちゃんねる 変形性股関節症雑談スレ/JP](https://rio2016.5ch.net/test/read.cgi/body/1556331153/)
- 「入院になって家族に負担かけるのが辛いです。」 [5ちゃんねる 変形性股関節症スレ17/JP](https://rio2016.5ch.net/test/read.cgi/body/1548762174/)
- 「杖つくと手首とかもすぐ痛くなるので杖使ってないんですが、それも軽く見られて悪いのかも。」 [5ちゃんねる 変形性股関節症スレ17/JP](https://rio2016.5ch.net/test/read.cgi/body/1548762174/)
- 「「私は杖なんてつかない、ダサいから」と言ったその人は、杖をつかずからだを大きくうねらせて歩いていた。」 [Amebaブログ/JP](https://ameblo.jp/rao-rl/entry-12975903897.html)
- 「でも５年も勤めて大好きなレジの仕事なので辞めたくなかったのですが」 [Yahoo!知恵袋/JP・50代主婦](https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q12150863512)
- 「母も診断を受けて、痛みのあまりとＤｒの薦めで介護の仕事を辞めました。」 [Yahoo!知恵袋/JP](https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q1227971387)
- 「60になる母が現在介護の仕事をしていますが、とにかく足が痛いらしく仕事が辛いとの事で今日病院へ行ってきました。」 [Yahoo!知恵袋/JP・60歳の母について](https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q11313552891)
- 「仕事、お金、生活を考えると色々難しいけど日々の痛みが段々辛すぎて、自分でもどうしたらいいのか決断できなく日々悩んでます。」 [Yahoo!知恵袋/JP・42歳](https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q13217564273)

### 1-B English

#### ① Describing the problem

- 「I'm a shadow of my former self.」 [Mumsnet/UK・52](https://www.mumsnet.com/talk/am_i_being_unreasonable/4847131-to-want-to-cry-with-hip-pain)
- 「Every day the pain is different - it's like the gift from hell that keeps on giving.」 [Mumsnet/UK・52](https://www.mumsnet.com/talk/am_i_being_unreasonable/4847131-to-want-to-cry-with-hip-pain)
- 「I barely go out and I walk like I've birthed an elephant for the few Stephanie can manage.」 [Mumsnet/UK・52](https://www.mumsnet.com/talk/am_i_being_unreasonable/4847131-to-want-to-cry-with-hip-pain)
- 「Then, upon standing, my hips were so painful I had to hold on to the wardrobe until I had warmed up, as it were.」 [Mumsnet/UK・52](https://www.mumsnet.com/talk/am_i_being_unreasonable/4568429-when-is-it-hip-replacement-time)
- 「I feel ok when I stand and move around, but lying down isn't great and sitting brings me to tears.」 [Mumsnet/UK](https://www.mumsnet.com/talk/general_health/4668015-hips-so-painful-i-cried-at-work)
- 「I feel it in my groin constantly, like a hot tight feeling that won't go.」 [Mumsnet/UK](https://www.mumsnet.com/talk/general_health/4668015-hips-so-painful-i-cried-at-work)
- 「Now that is cleared, I am struggling to sleep at night with hip pain, whatever position I get my self in, it becomes unbearable after an hour or so.」 [Mumsnet/UK・menopause board](https://www.mumsnet.com/talk/menopause/5088053-and-now-hip-pain-please-tell-me-how-you-manage-to-sleep-at-night-as-my-gp-cant)
- 「I tried physio, yoga, exercise but every year it got worse until the new normal was to not reach my toes, tie laces, trouble walking/sleeping ….」 [Mumsnet/UK](https://www.mumsnet.com/talk/am_i_being_unreasonable/4568429-when-is-it-hip-replacement-time)
- 「I'm quite shocked at how rapidly my health and mobility has gone downhill.」 [Mumsnet/UK・early 50s](https://www.mumsnet.com/talk/am_i_being_unreasonable/5278170-to-wonder-whats-normal-re-pain-or-health-issues-over-50)
- 「It wakes me up at night, and has left me wanting to cry.」 [Mumsnet/UK](https://www.mumsnet.com/talk/general_health/2371118-Hip-joint-degeneration-pain-how-to-cope)
- 「Even my husband lightly resting his hand on my waist used to 'drag' my hips back and make me want to kill him」 [Mumsnet/UK](https://www.mumsnet.com/talk/general_health/4226786-Hip-pain-that-is-worse-at-night-help)
- 「I could walk I just had to walk slow and use a wall to make sure it didn’t give out.」 [Mayo Clinic Connect/US](https://connect.mayoclinic.org/discussion/complex-hip-pain-with-no-answers/)
- 「It hurt the minute I laid down and woke me up often as it became worse throughout the night.」 [Mayo Clinic Connect/US](https://connect.mayoclinic.org/discussion/hip-pain-when-laying-down/)
- 「The pain became unbearable, to the point where I was wandering around the house at 3 am, crying because my right leg felt like it was on fire.」 [Reddit r/HipDysplasia/英語圏・46](https://www.reddit.com/r/HipDysplasia/comments/1hiud84/)

#### ② How it makes them feel

- 「My life is awful - everything has changed - I feel so sorry for the teenage DD who has to see me like」 [Mumsnet/UK・52](https://www.mumsnet.com/talk/am_i_being_unreasonable/4847131-to-want-to-cry-with-hip-pain)
- 「By age 46 (present day) I was feeling extremely defeated and depressed.」 [Reddit r/HipDysplasia/英語圏・46](https://www.reddit.com/r/HipDysplasia/comments/1hiud84/)
- 「I wasn't in crippling pain, but I also just felt like my whole life had become about my stupid hips and I was suddenly angry and miserable.」 [Reddit r/HipDysplasia/英語圏・46](https://www.reddit.com/r/HipDysplasia/comments/1hiud84/)
- 「I cried in his office as he told me there was nothing I could do at this point besides have a total hip replacement.」 [Reddit r/HipDysplasia/英語圏](https://www.reddit.com/r/HipDysplasia/comments/1ku0r7o/)
- 「I’m so scared all the time and in so much pain and I don’t know what to do.」 [Reddit r/HipDysplasia/英語圏](https://www.reddit.com/r/HipDysplasia/comments/1sr9s4f/)
- 「The surgeon said this is more complex at my age and even described me as “geriatric” for the procedure, which honestly scared me.」 [Reddit r/HipDysplasia/英語圏](https://www.reddit.com/r/HipDysplasia/comments/1te5thr/)
- 「I am scared to get the injection done again even though I am in terrible pain every day.」 [Reddit r/HipDysplasia/英語圏](https://www.reddit.com/r/HipDysplasia/comments/14flfdl/)
- 「She spends her life taking extremely strong painkillers and crying it's so awful」 [Mumsnet/UK](https://www.mumsnet.com/talk/am_i_being_unreasonable/4783793-to-expect-to-be-able-to-have-a-hip-operation-done-on-the-nhs)
- 「Honestly the impact this has had on my mental health has been awful and my husband has had to carry the load of everything for over a month now.」 [Mumsnet/UK](https://www.mumsnet.com/talk/chronic_pain/4745746-back-hip-pain-causing-depression)
- 「It doesn't help that my family isn't particularly interested or sympathetic, but then that might be down to me hating to make a big fuss about stuff.」 [Mumsnet/UK](https://www.mumsnet.com/talk/general_health/2371118-Hip-joint-degeneration-pain-how-to-cope)
- 「Many of my friends and family say do the op, but I'm worried that things will be worse rather than better.」 [Mumsnet/UK](https://www.mumsnet.com/talk/general_health/5111138-how-do-you-decide-when-you-absolutely-must-have-hip-replacement-surgery)
- 「It crushed me that a doctor would be so angry.」 [Mayo Clinic Connect/US](https://connect.mayoclinic.org/discussion/complex-hip-pain-with-no-answers/)

#### ③ What they've tried

- 「I have tried ibuprofen and voltarol gel and nothing helps.」 [Mumsnet/UK](https://www.mumsnet.com/talk/general_health/4226786-Hip-pain-that-is-worse-at-night-help)
- 「I did have injections - one steroid which did nothing - and two hyaluronic injections (the first helped for a couple of months - the second did nothing) before my replacement.」 [Mumsnet/UK](https://www.mumsnet.com/talk/chronic_pain/5155838-osteoarthritis-diagnosis-and-pain-control)
- 「My recent experience was private physio that made the pain worse then NHS physio that was better but made diagnosis without x-ray or scan.」 [Mumsnet/UK](https://www.mumsnet.com/talk/menopause/5088053-and-now-hip-pain-please-tell-me-how-you-manage-to-sleep-at-night-as-my-gp-cant)
- 「Yoga didn't help me much, it aggreviated my discomfort.」 [Mumsnet/UK](https://www.mumsnet.com/talk/menopause/5088053-and-now-hip-pain-please-tell-me-how-you-manage-to-sleep-at-night-as-my-gp-cant)
- 「My GP also diagnosed bursitis but the exercises my physio has given me only seem to be making the pain worse.」 [Mumsnet/UK](https://www.mumsnet.com/talk/general_health/4226786-Hip-pain-that-is-worse-at-night-help)
- 「In the three years previously I had spent way more than that on physio and chiropractic that helped but didn't solve the problem.」 [Mumsnet/UK](https://www.mumsnet.com/talk/general_health/5247006-nhs-hip-assessment-phone-call-what-to-expect-hip-replacement-qs-too)
- 「I have tried different mattresses, I am using a knee pillow, sometimes replaced by a proper pillow, have tried to sleep on both right and left side, facing up (my back hurts), on my tummy (ditto)」 [Mumsnet/UK](https://www.mumsnet.com/talk/menopause/5088053-and-now-hip-pain-please-tell-me-how-you-manage-to-sleep-at-night-as-my-gp-cant)
- 「I took 1600 mgs per day of Ibuprofen. No relief at all.」 [Mayo Clinic Connect/US](https://connect.mayoclinic.org/discussion/cortisone-injection-for-trochanteric-bursitis/)
- 「Cortisone shot - £200 all ish -can’t remember the exact prices.」 [Mumsnet/UK](https://www.mumsnet.com/talk/chronic_pain/4745746-back-hip-pain-causing-depression)

#### ④ What they wish existed / want back

- 「I don't actively want to have surgery, I just want my life back.」 [Mumsnet/UK](https://www.mumsnet.com/talk/general_health/5247006-nhs-hip-assessment-phone-call-what-to-expect-hip-replacement-qs-too)
- 「I'm pretty miserable with a huge decrease of quality of life these last few months - I just want my life back, but it's hard to know who to listen to.」 [Mumsnet/UK](https://www.mumsnet.com/talk/general_health/5247006-nhs-hip-assessment-phone-call-what-to-expect-hip-replacement-qs-too)
- 「I just want to feel good again and know I need to get fit.」 [Mumsnet/UK](https://www.mumsnet.com/talk/_chat/5515935-help-me-stop-hurting)
- 「I wish I'd gone for the op about 4 years earlier than I did.」 [Mumsnet/UK](https://www.mumsnet.com/talk/am_i_being_unreasonable/4568429-when-is-it-hip-replacement-time)
- 「I feel like I could manage if there were a standing desk to use at intervals, but it's not likely.」 [Mumsnet/UK](https://www.mumsnet.com/talk/general_health/4668015-hips-so-painful-i-cried-at-work)
- 「Just as DC are flying the nest, doing more of those was how I saw my life going in the future years.」 [Mumsnet/UK・turned 50](https://www.mumsnet.com/talk/general_health/5348818-osteoarthritis-in-the-hip-what-do-i-need-to-know)
- 「I did all the advised things, diet, exercise, no alcohol, good sleep」 [Mumsnet/UK・early 50s](https://www.mumsnet.com/talk/am_i_being_unreasonable/5278170-to-wonder-whats-normal-re-pain-or-health-issues-over-50)

#### ⑤ What doctors said (verbatim as reported)

- 「I did go to my GP who barely looked at me, dismissed me when I tried to tell him my symptoms were not just my hip and he put it down to wear and tear from carrying DD, gave me naproxen and Cocodamol, three months worth and sent me on my merry way, limping to the car.」 [Mumsnet/UK](https://www.mumsnet.com/talk/chronic_pain/4745746-back-hip-pain-causing-depression)
- 「Because I didn't jump off the chair in pain when he moved my leg, I'm OK.」 [Mumsnet/UK](https://www.mumsnet.com/talk/chronic_pain/4745746-back-hip-pain-causing-depression)
- 「Waiting list for a replacement is a year at least but the consultants say to manage it with steroid injections.」 [Mumsnet/UK・52](https://www.mumsnet.com/talk/am_i_being_unreasonable/4847131-to-want-to-cry-with-hip-pain)
- 「Oh wait - there's a 10 month waiting list.」 [Mumsnet/UK・52](https://www.mumsnet.com/talk/am_i_being_unreasonable/4847131-to-want-to-cry-with-hip-pain)
- 「Been 2 months, GP prescribed ibruprofen and told me it would go away, but nope.」 [Mumsnet/UK](https://www.mumsnet.com/talk/general_health/4043897-hip-pain)
- 「My GP was very nice, but had little advice other than not to overdo things, to keep as active as I can, and to take NSAIDs when it hurts.」 [Mumsnet/UK](https://www.mumsnet.com/talk/general_health/2371118-Hip-joint-degeneration-pain-how-to-cope)
- 「I'm in need of a hip replacement due to osteoarthritis although the surgeon I saw said I was too young and it needs to be managed with steroids (I'm 51).」 [Mumsnet/UK・51](https://www.mumsnet.com/talk/chronic_pain/4747090-osteoarthritis-stiffness)
- 「GP told me you had to have had physio and injections before you can get the replacement, is that correct?」 [Mumsnet/UK](https://www.mumsnet.com/talk/general_health/5247006-nhs-hip-assessment-phone-call-what-to-expect-hip-replacement-qs-too)
- 「I had X rays done back then and was told I would need hip replacement surgery in 1 to 5 years time.」 [Mumsnet/UK](https://www.mumsnet.com/talk/general_health/5111138-how-do-you-decide-when-you-absolutely-must-have-hip-replacement-surgery)
- 「Also I thought I had Piriformis syndrome for years and tried so much to correct it, I then got told it was greater trochanteric pain syndrome!」 [Mumsnet/UK](https://www.mumsnet.com/talk/am_i_being_unreasonable/4010422-To-be-sick-of-being-in-undiagnosed-pain-all-the-time)
- 「that doctor didn’t even examine me and told me I had bursitis and needed physical therapy」 [Mayo Clinic Connect/US](https://connect.mayoclinic.org/discussion/complex-hip-pain-with-no-answers/)
- 「Poor tissue strength is what I'm being told.」 [Mayo Clinic Connect/US・73歳女性](https://connect.mayoclinic.org/discussion/hip-revision-on-73-year-old-female/)

---

## 2. Emotional State Map（感情マップ）

数え方：1発言に感情語が1つでもあれば1件（施術者・宣伝・同一テンプレ回答は除外）。下の表は件数順＝頻度順。

<!--EMO-->

**読み取り（日本）**
1. **不安・恐怖**が最多。中身は「この先歩けなくなる」「人工股関節にするしかないのか」「手術が怖い」の3つにほぼ集約される。痛みそのものより「この先」が怖い。
2. **つらさ・消耗**。「辛い」は1文に2回重ねる書き方が多い（「辛くて辛くて」「辛すぎる」）。
3. **罪悪感・申し訳なさ**が3位に来るのが日本側の特徴。家族・職場・孫・夫への「迷惑」「負担」。英語圏ではこの層は薄く、代わりに**怒り・不満（frustration, fed up）**と**「医者に流された」（dismissed, fobbed off）**が上位。
4. **悲しみ・涙**と**落ち込み・うつ**。「一人になれる場所がないから泣けない」という、泣く場所すらない形の悲しみが5chに繰り返し出る。
5. **絶望・諦め**と**老いの自覚**（「年のせい」「年寄り」）は件数は少ないが、一番深いところにある。

---

## 3. Psychological Patterns（心のパターン）

### なぜこの問題が起きていると思っているか
- **「年のせい」「生まれつき」**：日本側はこの2つに分かれる。60代以上は「年齢的に仕方ない」と自分で言う（「60代も終わりになって来たから仕方ないかもしれないけど」）。50代前後で臼蓋形成不全と言われた人は「生まれつき」と言われて混乱する（「50過ぎになって言われても全然ピンと来なかった」）。
- **「使いすぎ・立ちすぎ」**：レジ・介護・立ち仕事の人は、仕事が原因だと思っている（医者からも「立ちっぱなしは一番良くない」）。
- **「軟骨がすり減った・骨が変形した」**：画像で説明を受けた人はこの物語で理解している。逆に**「異常なし」と言われた人には原因の物語がない**。ここが最も不安の強い層（「痛いのに原因すら分からなくて」）。
- 英語圏は **wear and tear / menopause / hypermobility** を原因に挙げる人が多い。

### 誰・何を責めているか
- **医者（日本は静かに、英語圏ははっきり）**：日本は「首を傾げられ」「4段階あるとか医者からは言われず」「長年地元の整形外科に通っていても認識されず」と、説明されなかったことを責める。英語圏は「barely looked at me」「dismissed me」「didn't even examine me」と診察の態度を責める。
- **制度**：英国は NHS の待機リスト（「a year at least」「10 month waiting list」）。日本は「保険適用外のため高い」。
- **自分の体**：「生まれる前からの右足股関節脱臼の体が情けなくて」。体を自分から切り離して責める言い方。
- **親**：臼蓋形成不全の人の一部は「幼少期に親が整形外科に連れていってくれていたら」と書く。

### 何を試して、本人は「なぜダメだった」と思っているか
- **整形外科の湿布と痛み止め**：「少しは和らぎますが、しばらくするとまたなる」。その場しのぎで、原因に触れていないと感じている。痛み止めは「お守り→毎日→強いのを勝負の日に」と段階的に増えていく。
- **リハビリ・ストレッチ・筋トレ**：「1年通ったが悪化する方向」「ストレッチをしても良くなるどころか」。やっているのに良くならない→「多分治らない気がするので行ってない」と離脱する。
- **整体・接骨院・マッサージ**：「良くならず」「保険適用外で高いしすぐ痛みが出る」。
- **注射（ヒアルロン酸・ステロイド）**：英語圏は「did nothing」「helped for a couple of months」。日本は件数が少なく、効かなかった報告は「ステロイドもヒアルロン酸もまったく効かなくなった」。
- **寝具・枕**（英語圏に多い）：マットレス・トッパー・膝枕を全部試しても夜の痛みが残る。
- 共通の理屈：**「その場は楽になるが、戻る」＝原因が残っている**と本人たちは感じている。

### 小さな希望の火
- 「手術後は普通にできるようになりますか？」＝**元の生活（しゃがむ・爪切り・階段・正座）に戻れるか**が一番の関心。
- 「手術の前に、まだできることがあるなら」：60代以上と、手術を「早い」と言われた40〜50代は、**手術以外の手**を探し続けている（「注射とか、直してくれる飲み薬、あったら何でも教えて下さい」）。
- 英語圏：「I just want my life back」。手術そのものは望んでいない。

---

## 4. Keyword & Jargon List（用語と出現数）

<!--KW-->

**コピーで信頼の合図になる、本人たちの言い回し（日本）**：股関節／脚の付け根／足の付け根／お尻の横／太ももの外側／臼蓋形成不全（「屋根が浅い」「受け皿が浅い」）／変形性股関節症（前期・初期・進行期・末期）／人工股関節（「人工物が体に入る」）／骨切り／杖／手すり／エレベーター／青信号の点滅／靴下が履けない／爪切り／あぐらがかけない／正座／寝返り／横向きで寝られない／立ち上がり／歩き始め／湿布と痛み止め／ロキソニン／ヒアルロン酸／リハビリ／整体・接骨院／レントゲンは異常なし／年のせい・年齢的なもの／様子見／我慢の限界

**English**：hip OA, bone on bone, bursitis, GTPS, gluteal tendinopathy, dysplasia, PAO, labral tear, groin pain, side sleeping, knee pillow, mattress topper, limp, walking stick/cane, cortisone/steroid injection, physio, GP, consultant, NHS waiting list, wear and tear, menopause/HRT, "I just want my life back", "shadow of my former self"

---

## 5. The Sentence They'd Never Say Out Loud（口に出せない一文）

- **日本語**：「このまま歩けなくなって、家族の“お荷物”になる日が来るのが一番怖い。でも『年のせい』で片づけられるのも、人工股関節にするのも、本当は嫌なんです。」
- **English**："I'm terrified I'm turning into the old woman everyone has to slow down for — and I don't want surgery, I just want someone to tell me why this is happening and that it's not too late."

（この一文は引用ではなく、集めた発言から組み立てた要約。根拠：④怖がっていること「歩けなくなる・進行」、感情マップ「罪悪感・申し訳なさ」、⑤「年のせい」「手術しかない」、英語「I just want my life back」）

---

## 6. 日本の声の集計（件数）

数え方：日本の発言のうち、施術者・宣伝・同一テンプレ回答を除いたものが対象。1発言の中で同じ項目は1回だけ数える。比率は対象発言数に対する割合。

注意：日本の発言の約6割は5chの「変形性股関節症」スレ（診断済み・手術を考えている人が多い）なので、集計は「すでに診断を受けた人」寄り。「脱臼」「お風呂」などが多いのは術後の話が混じるため。

<!--AGG-->

**集計から読めること**
- ① 呼び方は「股関節」が圧倒的。次に「腰」「お尻」「骨盤」が一緒に語られる＝**股関節だけの問題と思っていない**人が多い。「脚の付け根／足の付け根」は医療用語を使わない層の言い方。
- ② 場面は「歩く」が最多、次が「座る・座った後」「立ち上がり」「夜中に目が覚める・眠れない」。靴下・爪切り・あぐらは件数は少ないが**具体的で一読で映像が浮かぶ**（コピー向き）。
- ③ 試した物は「人工股関節手術」「整形外科」「リハビリ」「痛み止め」「ストレッチ」「筋トレ・体操」が上位。**痛み止めは否定の言葉（効かない・一時的）が肯定の約2.5倍**。筋トレ・体操は肯定の言葉が多いが、知恵袋の回答者による助言（「筋力をつければ良くなる」型）が多く混じっていて、本人の体験と分けきれていない。
- ④ 怖がっていることは「進行・悪化」が最多。「脱臼」は人工股関節の術前術後スレ由来。続いて「お金・費用」「転倒・骨折」「一生このまま」「反対側も悪くなる」「老後・将来」「家族に迷惑・負担」。
- ⑤ 医者の言葉（医者＋「言われた」が同じ文にあるもの）は「変形している」「臼蓋形成不全」「異常なし」「手術しかない」「人工関節」「湿布と痛み止め」「筋力をつけなさい」の順。**「年のせい」系は医者の台詞としては約10件しかないが、日本の発言全体では約300件に出てくる**＝医者に言われたというより、本人や家族が自分で「年のせい」と言って片づけている。

---

## 7. 照合結果（本文の引用 → 生データ）

<!--VERIFY-->
