#!/usr/bin/env python3
# usage: pm.py "<query>" [n]  -> prints PMID | year | journal | title + abstract head; caches xml
import sys,urllib.request,urllib.parse,re,os,html,json
q=sys.argv[1]; n=int(sys.argv[2]) if len(sys.argv)>2 else 8
B='https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
def get(u): return urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'research-script'}),timeout=60).read().decode()
ids=json.loads(get(B+'esearch.fcgi?db=pubmed&retmode=json&sort=relevance&retmax=%d&term=%s'%(n,urllib.parse.quote(q))))['esearchresult']['idlist']
if not ids: print('NO HITS'); sys.exit()
x=get(B+'efetch.fcgi?db=pubmed&retmode=xml&id='+','.join(ids))
d=os.environ.get('UMP_CACHE', os.path.join(os.getcwd(),'cache')); os.makedirs(d,exist_ok=True)
for art in re.findall(r'<PubmedArticle>.*?</PubmedArticle>',x,re.S):
  pmid=re.search(r'<PMID[^>]*>(\d+)',art).group(1)
  open(os.path.join(d,pmid+'.xml'),'w').write(art)
  t=lambda p: html.unescape(re.sub(r'<[^>]+>','',' '.join(re.findall(p,art,re.S))))
  title=t(r'<ArticleTitle>(.*?)</ArticleTitle>'); j=t(r'<ISOAbbreviation>(.*?)</ISOAbbreviation>')
  y=(re.findall(r'<PubDate>.*?<Year>(\d+)',art,re.S) or ['?'])[0]
  au=(re.findall(r'<LastName>(.*?)</LastName>',art) or ['?'])[0]
  ab=t(r'<AbstractText[^>]*>(.*?)</AbstractText>')
  print(f'## {pmid} | {au} {y} | {j}\n{title}\n{ab[:900]}\n')
