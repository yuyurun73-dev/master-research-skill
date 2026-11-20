// 使い方: node scrape_x_slow.mjs <検索語のJSON配列ファイル> $RESEARCH_DIR/raw/_stage/x_raw.jsonl
// （プロフィールは x-ingest のもの＝Xにログイン済み。同じプロフィールで2本同時に起動しない）
// x-ingest/scrape.mjs のレート制限対応版。0件が続いたら長めに待って同じ検索語を再試行する。
import { chromium } from '/Users/u/app-venture/research/x-ingest/node_modules/playwright/index.mjs';
import fs from 'node:fs';
const [, , qfile, out] = process.argv;
const queries = JSON.parse(fs.readFileSync(qfile, 'utf8'));
const ctx = await chromium.launchPersistentContext('/Users/u/app-venture/research/x-ingest/profile', { headless: true, viewport: { width: 1200, height: 1600 } });
const page = ctx.pages()[0] ?? await ctx.newPage();
const seen = new Set(fs.existsSync(out) ? fs.readFileSync(out, 'utf8').split('\n').filter(Boolean).map(l => JSON.parse(l).url) : []);
const ws = fs.createWriteStream(out, { flags: 'a' });
async function harvest(query) {
  const arts = await page.$$eval('article[data-testid="tweet"]', els => els.map(a => {
    const t = a.querySelector('[data-testid="tweetText"]')?.innerText ?? '';
    const link = [...a.querySelectorAll('a[href*="/status/"]')].map(x => x.getAttribute('href')).find(h => /^\/[^/]+\/status\/\d+$/.test(h)) ?? '';
    const user = link.split('/')[1] ?? '';
    const num = sel => { const e = a.querySelector(sel); return e ? (e.getAttribute('aria-label') ?? e.innerText) : ''; };
    const likes = num('[data-testid="like"]'), reposts = num('[data-testid="retweet"]');
    const time = a.querySelector('time')?.getAttribute('datetime') ?? '';
    return { t, link, user, likes, reposts, time };
  }));
  let n = 0, total = arts.length;
  for (const a of arts) {
    if (!a.link || !a.t || a.t.length < 30) continue;
    const url = 'https://x.com' + a.link; if (seen.has(url)) continue; seen.add(url);
    ws.write(JSON.stringify({ query, url, platform: 'X', country: /[ぁ-んァ-ヶ一-龠]/.test(a.t) ? 'JP' : 'EN', user: a.user, author: a.user, date: a.time, time: a.time, likes: a.likes, reposts: a.reposts, text: a.t }) + '\n'); n++;
  }
  return { n, total };
}
let consecutiveEmpty = 0;
for (const q of queries) {
  for (let attempt = 0; attempt < 3; attempt++) {
    await page.goto('https://x.com/search?q=' + encodeURIComponent(q) + '&src=typed_query&f=live', { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(6000);
    let got = 0, tot = 0;
    for (let i = 0; i < 10; i++) { const r = await harvest(q); got += r.n; tot += r.total; await page.mouse.wheel(0, 1800); await page.waitForTimeout(2200 + Math.random() * 1200); }
    console.log(`[${q}] +${got} (articles seen ${tot}) attempt${attempt}`);
    if (tot > 0) { consecutiveEmpty = 0; break; }
    consecutiveEmpty++;
    const wait = 60000 * (attempt + 1);
    console.log(`  empty -> backoff ${wait}ms`);
    await page.waitForTimeout(wait);
  }
  await page.waitForTimeout(8000);
}
ws.end(); await ctx.close();
