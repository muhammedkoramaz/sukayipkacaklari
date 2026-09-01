# -*- coding: utf-8 -*-
import glob, re, os
os.chdir(r"C:\Users\muham\Desktop\LEAKEXPERT APPS\leakexpert-site")

def exists(h):
    h = h.split('#')[0].split('?')[0]
    if h in ('', '/'):
        return True
    p = h.lstrip('/')
    if p.endswith('/'):
        p += 'index.html'
    return os.path.isfile(p) or os.path.isfile(p + '.html')

bad = []
htmls = [f for f in glob.glob('**/*.html', recursive=True) if 'assets' not in f]
for f in sorted(htmls):
    s = open(f, encoding='utf-8').read()
    for h in re.findall(r'href="(/[^"]*)"', s):
        if h.startswith(('/assets/', '/favicon', '/site.webmanifest')):
            continue
        if not exists(h):
            bad.append((f, h))

for f, h in bad:
    print('BROKEN', f, '->', h)
print(f'checked {len(htmls)} files; broken links: {len(bad)}')
