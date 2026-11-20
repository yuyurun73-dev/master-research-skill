import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
import re, json, time, sys, os, html, urllib.parse, urllib.request
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/128.0 Safari/537.36"
OUT = stage("hatena.jsonl")
QUERIES=[l.strip() for l in open(sys.argv[1],encoding="utf-8") if l.strip()]
BLOG=re.compile(r'https?://(?:[a-z0-9-]+\.(?:hatenablog\.com|hatenablog\.jp|hateblo\.jp|hatenadiary\.com|hatenadiary\.jp|hatenadiary\.org)/entry/[^"#?\s<>()]+|anond\.hatelabo\.jp/\d+)')
def get(u):
    for _ in range(3):
        try: return urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":UA,"Accept-Language":"ja"}),timeout=30).read().decode("utf-8","replace")
        except Exception as e: sys.stderr.write("retry %s %s\n"%(u,e)); time.sleep(2)
    return ""
def clean(t):
    t=re.sub(r'<(script|style).*?</\1>','',t,flags=re.S)
    t=re.sub(r'<br\s*/?>','\n',t); t=re.sub(r'</(p|div|h\d|li)>','\n',t); t=re.sub(r'<[^>]+>','',t)
    return re.sub(r'\n{3,}','\n\n',html.unescape(t)).strip()
seen=set()
if os.path.exists(OUT):
    for l in open(OUT,encoding="utf-8"):
        try: seen.add(json.loads(l)["url"])
        except: pass
_old="/nonexistent"
if os.path.exists(_old):
    for _l in open(_old,encoding="utf-8"):
        try: seen.add(json.loads(_l)["url"])
        except Exception: pass
f=open(OUT,"a",encoding="utf-8"); n=0
for q in QUERIES:
    urls=[]
    for tgt in ("text","title"):
        s=get("https://b.hatena.ne.jp/q/%s?target=%s&sort=recent"%(urllib.parse.quote(q),tgt))+get("https://b.hatena.ne.jp/q/%s?target=%s&sort=popular"%(urllib.parse.quote(q),tgt))
        for u in BLOG.findall(s):
            if u not in urls: urls.append(u)
        time.sleep(0.5)
    sys.stderr.write("QUERY %s -> %d\n"%(q,len(urls)))
    for u in urls[:12]:
        if u in seen: continue
        seen.add(u)
        h=get(u); time.sleep(0.6)
        if not h: continue
        m=re.search(r'<div class="entry-content[^"]*"[^>]*>(.*?)<(?:div class="entry-footer|footer)', h, re.S) or re.search(r'<div class="section">(.*?)</div>\s*<p class="sectionfooter',h,re.S)
        if not m: continue
        body=clean(m.group(1))
        if len(body)<300: continue
        tm=re.search(r'<title>(.*?)</title>',h,re.S); title=html.unescape(tm.group(1)).strip() if tm else ""
        dm=re.search(r'<time[^>]*datetime="([^"]+)"',h); date=dm.group(1) if dm else ""
        f.write(json.dumps({"url":u,"source":"hatena","country":"JP","date":date,"query":q,"title":title,"text":body[:8000]},ensure_ascii=False)+"\n"); f.flush(); n+=1
sys.stderr.write("WROTE %d\n"%n)
