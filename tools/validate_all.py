# -*- coding: utf-8 -*-
import glob, re, json, os, html.parser
os.chdir(r"C:\Users\muham\Desktop\LEAKEXPERT APPS\leakexpert-site")

class TB(html.parser.HTMLParser):
    VOID={'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
    def __init__(s): super().__init__(); s.st=[]; s.err=[]
    def handle_starttag(s,t,a):
        if t not in s.VOID: s.st.append(t)
    def handle_endtag(s,t):
        if t in s.VOID: return
        if t in s.st:
            while s.st and s.st.pop()!=t: pass
        else: s.err.append(f'stray </{t}>')

files=sorted(f for f in glob.glob('**/*.html',recursive=True) if '.git' not in f and 'assets' not in f)
issues=0
for f in files:
    s=open(f,encoding='utf-8').read()
    p=TB(); p.feed(s)
    left=[x for x in p.st if x not in ('html','body')]
    jblocks=re.findall(r'<script type="application/ld\+json">(.*?)</script>',s,re.S)
    jerr=[]; types=[]
    for b in jblocks:
        try:
            d=json.loads(b)
            for node in (d.get('@graph') or [d]):
                t=node.get('@type'); types.append(t if isinstance(t,str) else '/'.join(t) if t else '?')
                if (isinstance(t,str) and t=='Article') or (isinstance(t,list) and 'Article' in t):
                    for req in ('headline','image','datePublished','publisher'):
                        if req not in node: jerr.append(f'Article missing {req}')
        except Exception as e:
            jerr.append(f'PARSE: {e}')
    # img dims
    imgs=re.findall(r'<img [^>]*>',s)
    nodim=[i for i in imgs if 'width=' not in i or 'height=' not in i]
    ga = 'preconnect" href="https://www.googletagmanager.com"' in s
    if left or p.err or jerr or nodim or not ga:
        issues+=1
        print(f'✗ {f}')
        if left: print('   unclosed:',left)
        if p.err: print('   ',p.err[:4])
        if jerr: print('   ld+json:',jerr)
        if nodim: print(f'   {len(nodim)} <img> without width/height:',nodim[0][:90])
        if not ga: print('   GA preconnect missing')

print(f'\n{len(files)} files — {issues} with issues')
