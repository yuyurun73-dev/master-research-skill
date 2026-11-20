import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
import re, json, time, sys, os, html, urllib.parse, urllib.request
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/128.0 Safari/537.36"
OUT = stage("girlschannel.jsonl")
QUERIES=[l.strip() for l in open(sys.argv[1],encoding="utf-8") if l.strip()]
KEEP = rx("topic_ja")
def get(u):
    for _ in range(3):
        try: return urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":UA,"Accept-Language":"ja"}),timeout=30).read().decode("utf-8","replace")
        except Exception as e: sys.stderr.write("retry %s %s\n"%(u,e)); time.sleep(2)
    return ""
def clean(t):
    t=re.sub(r'<br\s*/?>','\n',t); t=re.sub(r'<[^>]+>','',t); t=html.unescape(t)
    return re.sub(r'[ \t]+\n','\n',re.sub(r'\n{3,}','\n\n',t)).strip()
def comments(h):
    out=[]
    for m in re.finditer(r'<li class="comment-item" id="comment(\d+)">.*?<div class="body lv\d">(.*?)</div>', h, re.S):
        b=clean(m.group(2))
        if b: out.append((int(m.group(1)), b))
    return out
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
    ids=[]
    for pg in ("", "&page=2"):
        s=get("https://girlschannel.net/topics/search/?q=%s%s"%(urllib.parse.quote(q),pg))
        for t in re.findall(r'href="/topics/(\d+)/"', s):
            if t not in ids: ids.append(t)
        time.sleep(0.5)
    sys.stderr.write("QUERY %s -> %d\n"%(q,len(ids)))
    for tid in ids[:10]:
        url="https://girlschannel.net/topics/%s/"%tid
        if url in seen: continue
        seen.add(url)
        h=get(url)
        if not h: continue
        tm=re.search(r'<title>(.*?)\s*\|',h); title=html.unescape(tm.group(1)) if tm else ""
        if not KEEP.search(title): sys.stderr.write("skip %s\n"%title); continue
        dm=re.search(r'class="datetime">([^<]+)<',h); date=dm.group(1) if dm else ""
        cs=comments(h)
        for p in (2,3,4):
            if 'href="/topics/%s/%d/"'%(tid,p) not in h: break
            h2=get("https://girlschannel.net/topics/%s/%d/"%(tid,p)); time.sleep(0.5)
            cs+=comments(h2)
        if len(cs)<3: continue
        text="\n\n".join("%d. %s"%(i,b) for i,b in cs)
        f.write(json.dumps({"url":url,"source":"girlschannel","country":"JP","date":date,"query":q,"title":title,
            "text":text[:30000],"n_comments":len(cs)},ensure_ascii=False)+"\n"); f.flush(); n+=1
        sys.stderr.write("ok %s (%d)\n"%(title,len(cs)))
        time.sleep(0.7)
sys.stderr.write("WROTE %d\n"%n)
