#!/usr/bin/env python3
import sys,re,html,os
for p in sys.argv[1:]:
  a=open(os.path.join(os.environ.get('UMP_CACHE', os.path.join(os.getcwd(),'cache')),p+'.xml')).read()
  t=lambda r: html.unescape(re.sub(r'<[^>]+>','',' '.join(re.findall(r,a,re.S))))
  print('##',p,t(r'<ArticleTitle>(.*?)</ArticleTitle>'),'|',t(r'<ISOAbbreviation>(.*?)</ISOAbbreviation>'))
  for lab,txt in re.findall(r'<AbstractText(?:[^>]*Label="([^"]*)")?[^>]*>(.*?)</AbstractText>',a,re.S):
    if lab.upper() in ('RESULTS','CONCLUSION','CONCLUSIONS','FINDINGS','') : print(f'[{lab}]',html.unescape(re.sub(r'<[^>]+>','',txt))[:1400])
  print()
