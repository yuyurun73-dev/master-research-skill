import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
import re, json, time, sys, os, html, urllib.parse, urllib.request
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/128.0 Safari/537.36"
OUT = stage("ameba.jsonl")
QUERIES=[l.strip() for l in open(sys.argv[1],encoding="utf-8") if l.strip()]
def get(u):
    for _ in range(3):
        try:
            return urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":UA,"Accept-Language":"ja"}),timeout=30).read().decode("utf-8","replace")
        except Exception as e:
            sys.stderr.write("retry %s\n"%e); time.sleep(2)
    return ""
def body_of(h):
    m=re.search(r'<div[^>]*class="[^"]*skin-entryBody[^"]*"[^>]*>(.*?)</div>\s*(?:<div|</article)', h, re.S)
    if not m:
        m=re.search(r'id="entryBody"[^>]*>(.*?)</div>', h, re.S)
    if not m:
        m=re.search(r'<div class="articleText">(.*?)</div>', h, re.S)
    t = m.group(1) if m else ""
    t=re.sub(r'<script.*?</script>','',t,flags=re.S)
    t=re.sub(r'<br\s*/?>','\n',t); t=re.sub(r'</(p|div)>','\n',t)
    t=re.sub(r'<[^>]+>','',t)
    return re.sub(r'\n{3,}','\n\n',html.unescape(t)).strip()
def title_of(h):
    m=re.search(r'<title>(.*?)</title>',h,re.S)
    return html.unescape(re.sub(r'<[^>]+>','',m.group(1))).strip() if m else ""
def date_of(h):
    m=re.search(r'"datePublished"\s*:\s*"([^"]+)"',h) or re.search(r'<time[^>]*datetime="([^"]+)"',h)
    return m.group(1) if m else ""
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
    for pg in ["", "&p=2", "&p=3"]:
        s=get("https://search.ameba.jp/search/entry/%s.html?"%urllib.parse.quote(q)+pg.lstrip("&"))
        for x in re.findall(r'href="(https?://ameblo\.jp/[^"/]+/entry-\d+\.html)"', s):
            if x not in urls: urls.append(x)
        time.sleep(0.5)
    sys.stderr.write("QUERY %s -> %d\n"%(q,len(urls)))
    for u in urls[:12]:
        if u in seen: continue
        seen.add(u)
        h=get(u)
        if not h: continue
        b=body_of(h)
        if len(b)<250: continue
        f.write(json.dumps({"url":u,"source":"Ameba blog","country":"JP","date":date_of(h),
            "query":q,"title":title_of(h),"text":b[:7000],"replies":[]},ensure_ascii=False)+"\n"); f.flush(); n+=1
        time.sleep(0.6)
sys.stderr.write("WROTE %d\n"%n)
