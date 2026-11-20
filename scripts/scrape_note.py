import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
import json, re, time, sys, urllib.parse, urllib.request, os, html
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/128.0 Safari/537.36"
OUT = stage("note.jsonl")
QUERIES=[l.strip() for l in open(sys.argv[1],encoding="utf-8") if l.strip()]
def get(u):
    for _ in range(3):
        try:
            return urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent":UA,"Accept":"application/json"}), timeout=30).read().decode("utf-8","replace")
        except Exception as e:
            sys.stderr.write("retry %s\n"%e); time.sleep(2)
    return ""
def strip(h):
    h=re.sub(r'<br\s*/?>','\n',h); h=re.sub(r'</p>','\n',h)
    h=re.sub(r'<[^>]+>','',h); return html.unescape(h).strip()
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
    s=get("https://note.com/api/v3/searches?context=note&q=%s&size=20"%urllib.parse.quote(q))
    if not s: continue
    try: contents=json.loads(s)["data"]["notes"]["contents"]
    except Exception as e: sys.stderr.write("parse %s\n"%e); continue
    sys.stderr.write("QUERY %s -> %d\n"%(q,len(contents)))
    for c in contents[:8]:
        key=c.get("key"); un=c.get("user",{}).get("urlname","")
        url="https://note.com/%s/n/%s"%(un,key)
        if url in seen: continue
        seen.add(url)
        d=get("https://note.com/api/v3/notes/%s"%key)
        if not d: continue
        try: nd=json.loads(d)["data"]
        except: continue
        body=strip(nd.get("body") or "")
        if len(body)<200: continue
        f.write(json.dumps({"url":url,"source":"note.com","country":"JP",
            "date":nd.get("publish_at",""),"query":q,"title":nd.get("name",""),
            "text":body[:6000],"replies":[]},ensure_ascii=False)+"\n"); f.flush(); n+=1
        time.sleep(0.6)
    time.sleep(0.6)
sys.stderr.write("WROTE %d\n"%n)
