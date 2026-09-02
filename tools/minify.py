#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/minify.py — el yazımı CSS/JS kaynaklarından *.min.* üretir.

Saf statik site olduğu için build adımı yok; minify çıktıları REPO'ya commit edilir.
HTML dosyaları /assets/css/site.min.css, fonts.min.css ve /assets/js/site.min.js'e
referans verir. Kaynağı (site.css / fonts.css / site.js) elle düzenle, sonra bunu çalıştır.

Tipik akış:  py tools/minify.py  ->  py tools/validate_all.py  ->  git commit

Konservatif:
  - CSS: yorumları siler, boşlukları sıkıştırır, yalnızca { } : ; , çevresini kırpar.
    calc()/clamp() içindeki +/- korunur (aralarındaki boşluk CSS'de zorunlu).
  - JS: yalnızca /* ... */ bloklarını ve satır başı/sonu boşluklarını siler,
    satır sonlarını KORUR (ASI güvenli). site.js ES5, regex-literali/`//` yorumu yok.
Bağımlılık yok.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JOBS = [
    ("assets/css/site.css",  "assets/css/site.min.css",  "css"),
    ("assets/css/fonts.css", "assets/css/fonts.min.css", "css"),
    ("assets/js/site.js",    "assets/js/site.min.js",    "js"),
]


def minify_css(s: str) -> str:
    s = re.sub(r"/\*.*?\*/", "", s, flags=re.S)          # yorumlar
    s = re.sub(r"\s+", " ", s)                            # tüm boşluk -> tek boşluk
    s = re.sub(r"\s*([{}:;,])\s*", r"\1", s)              # sadece bu belirteçlerin çevresini kırp
    s = re.sub(r";}", "}", s)                             # gereksiz son ;
    s = re.sub(r"\}\s*", "}", s)
    return s.strip()


def minify_js(s: str) -> str:
    s = re.sub(r"/\*.*?\*/", "", s, flags=re.S)           # /* blok */ yorumlar
    s = "\n".join(line.strip() for line in s.split("\n"))  # satır başı/sonu boşluk
    s = re.sub(r"\n{2,}", "\n", s)                         # boş satırları tek satıra
    return s.strip() + "\n"


def main() -> int:
    changed = 0
    for src_rel, out_rel, kind in JOBS:
        src = ROOT / src_rel
        out = ROOT / out_rel
        raw = src.read_text(encoding="utf-8")
        mini = minify_css(raw) if kind == "css" else minify_js(raw)
        old = out.read_text(encoding="utf-8") if out.exists() else None
        out.write_text(mini, encoding="utf-8", newline="")
        pct = 100 - round(len(mini) / max(len(raw), 1) * 100)
        tag = "=" if old == mini else "*"
        if old != mini:
            changed += 1
        print(f"  {tag} {out_rel:30s} {len(raw):>6d} -> {len(mini):>6d} bytes  (-{pct}%)")
    print(f"{'updated' if changed else 'no changes'} ({changed} file(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
