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

def resolve_href(h):
    """True if an internal href points at a file that exists on disk."""
    h = h.split('#')[0].split('?')[0]
    if 'sukayipkacaklari.com' in h:
        h = h.split('sukayipkacaklari.com', 1)[1]
    if h in ('', '/'):
        return os.path.isfile('index.html')
    p = h.lstrip('/')
    if p.endswith('/'):
        p += 'index.html'
    return os.path.isfile(p) or os.path.isfile(p + '.html')

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
    ga = ('googletagmanager.com"' in s) and ('G-ETN61F721R' in s)

    # --- i18n: <html lang>, hreflang trio, JSON-LD inLanguage ---
    nf = f.replace(os.sep, '/')
    is_en = nf == 'en/index.html' or nf.startswith('en/')
    want_lang = 'en' if is_en else 'tr'
    mhtml = re.search(r'<html[^>]*\blang="([^"]+)"', s)
    got_lang = mhtml.group(1) if mhtml else None
    lang_ok = got_lang == want_lang
    noindex = bool(re.search(r'<meta[^>]+name="robots"[^>]+content="[^"]*noindex', s))
    href = dict(re.findall(r'<link rel="alternate" hreflang="([^"]+)" href="([^"]+)"', s))
    if noindex:
        hreflang_ok = True
    else:
        hreflang_ok = ({'tr','en','x-default'} <= set(href)
                       and all(resolve_href(href[k]) for k in ('tr','en','x-default')))
    ld_lang_ok = True
    for b in jblocks:
        for m in re.finditer(r'"inLanguage"\s*:\s*"([^"]+)"', b):
            if not m.group(1).lower().startswith(want_lang):
                ld_lang_ok = False

    if left or p.err or jerr or nodim or not ga or not lang_ok or not hreflang_ok or not ld_lang_ok:
        issues+=1
        print(f'✗ {f}')
        if left: print('   unclosed:',left)
        if p.err: print('   ',p.err[:4])
        if jerr: print('   ld+json:',jerr)
        if nodim: print(f'   {len(nodim)} <img> without width/height:',nodim[0][:90])
        if not ga: print('   GA tag (googletagmanager + G-ETN61F721R) missing')
        if not lang_ok: print(f'   <html lang> expected "{want_lang}", got {got_lang!r}')
        if not hreflang_ok: print('   hreflang tr/en/x-default trio missing or target unresolved:', href)
        if not ld_lang_ok: print(f'   JSON-LD inLanguage does not match page language ({want_lang})')

print(f'\n{len(files)} files — {issues} with issues')
