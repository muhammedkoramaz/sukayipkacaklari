# -*- coding: utf-8 -*-
"""Add intrinsic width/height to every local <img src="/assets/..."> that lacks them
(CLS / layout-shift fix). Idempotent — re-run after any page regeneration."""
import glob, os, re
from PIL import Image

SITE = r"C:\Users\muham\Desktop\LEAKEXPERT APPS\leakexpert-site"
os.chdir(SITE)

_cache = {}
def dims(src):
    rel = src.lstrip("/")
    if rel in _cache:
        return _cache[rel]
    if not os.path.isfile(rel):
        _cache[rel] = None
        return None
    try:
        with Image.open(rel) as im:
            _cache[rel] = im.size
    except Exception:
        _cache[rel] = None
    return _cache[rel]

IMG_RE = re.compile(r'<img\b[^>]*>')
SRC_RE = re.compile(r'src="(/assets/[^"]+)"')

changed = 0
touched_files = 0
for f in sorted(glob.glob("**/*.html", recursive=True)):
    if ".git" in f or f.startswith("assets" + os.sep):
        continue
    s = open(f, encoding="utf-8").read()
    out = []
    last = 0
    n = 0
    for m in IMG_RE.finditer(s):
        tag = m.group(0)
        if "width=" in tag and "height=" in tag:
            continue
        sm = SRC_RE.search(tag)
        if not sm:
            continue
        d = dims(sm.group(1))
        if not d:
            continue
        w, h = d
        new = tag[:-1].rstrip()
        # insert after src="..."
        ins_at = sm.end()
        new_tag = tag[:sm.end()] + f' width="{w}" height="{h}"' + tag[sm.end():]
        out.append(s[last:m.start()])
        out.append(new_tag)
        last = m.end()
        n += 1
    if n:
        out.append(s[last:])
        open(f, "w", encoding="utf-8", newline="\n").write("".join(out))
        touched_files += 1
        changed += n
        print(f"  {f}: +{n}")

print(f"\n{changed} <img> tags fixed across {touched_files} files")
