import { chromium } from '/Users/u/app-venture/research/x-ingest/node_modules/playwright/index.mjs';
import fs from 'node:fs';
// 使い方: RESEARCH_DIR=<作業フォルダ> node scrape_healthunlocked.mjs <英語の検索語ファイル（1行1語）>
const OUT = (process.env.RESEARCH_DIR || process.cwd()) + '/raw/_stage/utter_healthunlocked.jsonl';
const QUERIES = fs.readFileSync(process.argv[2], 'utf8').split('\n').map(s => s.trim()).filter(Boolean);
const b = await chromium.launch({ headless: true });
const ctx = await b.newContext({ userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36', viewport: { width: 1280, height: 2200 } });
const page = await ctx.newPage();
const seen = new Set(fs.existsSync(OUT) ? fs.readFileSync(OUT, 'utf8').split('\n').filter(Boolean).map(l => JSON.parse(l).url) : []);
const ws = fs.createWriteStream(OUT, { flags: 'a' });

const links = new Set();
for (const q of QUERIES) {
  try {
    await page.goto('https://healthunlocked.com/search/posts?query=' + encodeURIComponent(q), { waitUntil: 'domcontentloaded', timeout: 45000 });
    await page.waitForTimeout(3500);
    for (let i = 0; i < 6; i++) { await page.mouse.wheel(0, 2200); await page.waitForTimeout(1200); }
    const hrefs = await page.$$eval('a[href*="/posts/"]', as => as.map(a => a.getAttribute('href')));
    let n = 0;
    for (const h of hrefs) { if (!h) continue; const u = h.startsWith('http') ? h : 'https://healthunlocked.com' + h; if (!links.has(u)) { links.add(u); n++; } }
    console.log(`[${q}] +${n} (total ${links.size})`);
  } catch (e) { console.log('SEARCHFAIL', q, e.message); }
}

let w = 0;
for (const u of links) {
  if (seen.has(u)) continue; seen.add(u);
  try {
    await page.goto(u, { waitUntil: 'domcontentloaded', timeout: 45000 });
    await page.waitForTimeout(2500);
    for (let i = 0; i < 5; i++) { await page.mouse.wheel(0, 2500); await page.waitForTimeout(800); }
    const d = await page.evaluate(() => {
      const title = document.querySelector('h1')?.innerText ?? '';
      const t = document.querySelector('time');
      const main = (document.querySelector('main') || document.body).innerText;
      return { title, date: t ? (t.getAttribute('datetime') || t.innerText) : '', main };
    });
    if (!d.title || d.main.length < 300) { continue; }
    ws.write(JSON.stringify({ url: u, source: 'healthunlocked', platform: 'HealthUnlocked', country: 'UK/EN', date: d.date, author: '', likes: '', title: d.title, text: d.main.slice(0, 20000), replies: [] }) + '\n');
    w++; if (w % 20 === 0) console.log('wrote', w);
  } catch (e) { console.log('FAIL', u, e.message); }
}
console.log('WROTE', w); ws.end(); await b.close();
