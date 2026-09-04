# Blog Bölümü + 8 Yeni Makale — Uygulama Planı

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** LeakExpert sitesinin `/rehber/` bölümünü `/blog/` olarak taşımak, hub kartlarına ve makalelere görsel eklemek, ve rakip kapsamındaki 8 eksik konuda TR+EN özgün makale yayımlamak.

**Architecture:** Saf statik site; sayfalar Python jeneratörlerle üretilir (`tools/gen_*.py`), build adımı yok, çıktı repoya commit edilir. `gen_rehber.py` → `gen_blog.py` olarak yeniden adlandırılır; `ARTICLES` listesine 8 dict eklenir; hub kartı şablonu `<img>` alır. Bölüm yolu iki jeneratörün paylaştığı `UI` sözlüklerinde ve 20 el-HTML'de `/blog/` + "Blog" olur. `sitemap.xml`'i `gen_projects.py` üretir. Eski yollar nginx 301 ile `/blog/`'a yönlenir.

**Tech Stack:** Python 3.10 (`py` launcher, `PYTHONUTF8=1`), elle yazılmış HTML/CSS/JS, nginx (Coolify `static` buildpack), git. Görsel işleme: Pillow veya `cwebp` (WebP dönüştürme).

**Spec:** `docs/superpowers/specs/2026-09-04-blog-bolumu-ve-8-makale-design.md`

## Global Constraints

Her task'ın gereksinimleri örtük olarak bu bölümü içerir. Değerler `PROJECT.md` §7 ve spec §1'den birebir:

- **Cihaz/marka adı yok.** Jenerik yaz: "taşınabilir ultrasonik debimetre", "basınç veri loggerı", "elektromanyetik hat dedektörü", "yer radarı (GPR)". (Keller, SEBA, Sitelab, Aktek vb. hiçbiri geçmez.)
- **Ana sayfada / örneklerde şehir adı yok.** Örnekler "bir belediyede…" der.
- **"anında onarılan" / "onarım bekleyen"** ifadeleri hiçbir sayfada geçmez.
- **Kurumsal müşteri yorumu / referans metni yok.**
- Header'da **"Keşif talebi" butonu yok**; CTA "görüşme / uzaktan görüntülü görüşme talebi" çerçevesinde — saha ziyareti değil.
- **Bölgesel / Kayseri konumlandırması yok** — Türkiye geneli. Şehir iniş sayfası yapma. `areaServed` = yalnızca Türkiye.
- **Ev / bina / konut içi kaçak tespiti yok.** Kapsam yalnızca belediye + sanayi (OSB) dağıtım şebekeleri.
- Terim **"proje"**, "vaka" değil.
- Tema yalnızca açık (light). Marka mavisi `#2563eb`.
- **TR + EN tam parite.** Slug'lar Türkçe kalır ve değişmez. Eşleşme: `EN yol = "/en" + TR yol`.
- HTML daima `.min` CSS/JS'e referans verir (`site.min.css`, `fonts.min.css`, `site.min.js`).
- Her `<img>` gerçek `width`/`height` taşır (`tools/add_img_dims.py` ekler).
- Makale JSON-LD zorunlu alanları: `headline`, `image`, `datePublished`, `publisher`.
- Yeni makale `datePublished` = **`2026-09-04`**.
- Kanonik host non-www: `https://sukayipkacaklari.com`.
- **Doğrulama zinciri (her jeneratör çalıştırmasından sonra):** `py tools/gen_blog.py` → `py tools/gen_projects.py` → `py tools/add_img_dims.py` → (CSS/JS değiştiyse `py tools/minify.py`) → `py tools/validate_all.py` (0 issue) → `py tools/linkcheck.py` (0 broken).
- Windows: komutları `py -3` ile ve `PYTHONUTF8=1` ortamıyla çalıştır.
- Commit mesajı sonu:
  `Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>` + `Claude-Session: https://claude.ai/code/session_01N4UGLRXRLoyY3UiYUaCnet`

---

## Dosya Yapısı

| Dosya | Sorumluluk | İşlem |
|---|---|---|
| `tools/gen_rehber.py` → `tools/gen_blog.py` | Blog hub + makale üretimi (TR+EN) | `git mv` + içerik |
| `tools/gen_projects.py` | Paylaşılan header/footer/`UI` + `sitemap.xml` üretimi | Modify |
| `rehber/` → `blog/` · `en/rehber/` → `en/blog/` | Üretilen çıktı dizinleri | `git mv` |
| `assets/css/site.css` + `site.min.css` | `.card--media` / `.card__img` kart stili | Modify + minify |
| `assets/blog/*.webp` | Yeni makale hero görselleri | Create |
| `index.html`, `platform.html`, `hizmetler.html`, `referanslar.html`, `hakkimizda.html`, `sss.html`, `iletisim.html`, `gizlilik.html`, `tesekkurler.html`, `404.html` (+ `en/` karşılıkları) | Menü + footer "Blog" linki | Modify ×20 |
| `nginx.conf` | `/rehber/` → `/blog/` 301 kuralı | Modify |
| `.htaccess` | Apache 301 yedeği | Modify |
| `llms.txt` | Bölüm başlığı + link listesi | Modify |
| `sitemap.xml` | Jeneratör çıktısı (elle düzenlenmez) | Regen |
| `PROJECT.md` | §5 sayfa tablosu, §6 jeneratör adı, §8 changelog | Modify |

---

## Task 1: Hero görsellerini hazırla ve onaylat

**Files:**
- Create: `assets/blog/sifir-basinc-testi-nedir.webp`, `assets/blog/boru-hatti-tespiti-nedir.webp`, `assets/blog/sebeke-haritalama-cbs.webp`, `assets/blog/kacak-onarimi-ve-dogrulama.webp` (Drive'dan kürasyon)
- Reference (mevcut, kopyalama yok): `assets/photos/debi-olcum.webp`, `assets/photos/basinc-logger.webp`, `assets/photos/gece-operasyon.webp`, `assets/photos/basinc-test.webp`, `assets/photos/gunduz-dinleme.webp`, `assets/photos/gece-dinleme-hero.webp`, `assets/photos/dma-tasarim.webp`, `assets/photos/depo-cikis.webp`

**Interfaces:**
- Produces: 12 makale için `hero` asset yolu tablosu (Task 4 ve Task 5–12 bu yolları kullanır):

  | slug | hero |
  |---|---|
  | su-kacagi-nasil-anlasilir | `/assets/photos/gunduz-dinleme.webp` |
  | akustik-su-kacagi-tespiti-nedir | `/assets/photos/gece-dinleme-hero.webp` |
  | dma-nedir | `/assets/photos/dma-tasarim.webp` |
  | su-kaybi-dusurme-yol-haritasi | `/assets/photos/depo-cikis.webp` |
  | debi-olcumu-nedir | `/assets/photos/debi-olcum.webp` |
  | basinc-yonetimi-nedir | `/assets/photos/basinc-logger.webp` |
  | adim-testi-nedir | `/assets/photos/gece-operasyon.webp` |
  | sifir-basinc-testi-nedir | `/assets/blog/sifir-basinc-testi-nedir.webp` |
  | hidrolik-modelleme-nedir | `/assets/photos/basinc-test.webp` |
  | boru-hatti-tespiti-nedir | `/assets/blog/boru-hatti-tespiti-nedir.webp` |
  | sebeke-haritalama-cbs | `/assets/blog/sebeke-haritalama-cbs.webp` |
  | kacak-onarimi-ve-dogrulama | `/assets/blog/kacak-onarimi-ve-dogrulama.webp` |

- [ ] **Step 1: Mevcut foto envanterini doğrula**

Run: `py -c "import os; print('\n'.join(sorted(os.listdir(r'assets/photos'))))"`
Beklenen: yukarıdaki `assets/photos/*.webp` 8 dosyanın hepsi listede. Eksik varsa Drive'dan ikame seç (Step 3).

- [ ] **Step 2: Drive'dan aday fotoğrafları listele**

Run (aday havuzu):
```
py -c "import glob; [print(p) for p in glob.glob(r'G:/Drive\'ım/SKK/YAPILAN İŞLER/**/FOTOĞRAFLAR/**/*.jp*g', recursive=True)][:200]"
```
4 eksik konu için (`sifir-basinc-testi-nedir` = vana/hat izolasyonu; `boru-hatti-tespiti-nedir` = saha, işaretleme/dedektör; `sebeke-haritalama-cbs` = harita/ekran/GPS; `kacak-onarimi-ve-dogrulama` = kazı/onarım noktası) her birine 2–3 aday seç. Adayları `Read` ile görüntüle; kişi yüzü, araç plakası, kurum tabelası/logo içerenleri ele veya kırpılacak diye işaretle.

- [ ] **Step 3: Adayları WebP'ye dönüştür**

Her seçili aday için (`cwebp` yoksa Pillow):
```
py -c "from PIL import Image; im=Image.open(SRC).convert('RGB'); w=1600; im=im.resize((w,round(im.height*w/im.width))); im.save('assets/blog/SLUG.webp','WEBP',quality=80,method=6)"
```
Yüz/plaka/tabela varsa `im.crop(...)` ile çıkar. Çıktı genişliği 1600px, kalite 80.

- [ ] **Step 4: Önizleme galerisi (Artifact) yayınla ve kullanıcı onayı al**

12 hero görselini (mevcut 8 + yeni 4) tek sayfada, slug etiketli, 16:9 kırpımla gösteren bir HTML Artifact yaz ve yayınla. Kullanıcıya sor: "Bu hero eşleşmelerini onaylıyor musun? Değiştirmek istediğin var mı?"
**DUR — kullanıcı onayı olmadan Task 2'ye geçme.** Kullanıcı bir görseli reddederse Step 2–3'ü o slug için tekrarla.

- [ ] **Step 5: Commit**

```bash
git add assets/blog/
git commit -m "assets: blog makaleleri için 4 hero görsel (Drive kürasyon)"
```

---

## Task 2: Görselli kart CSS'i

**Files:**
- Modify: `assets/css/site.css` (kart bloğunun sonuna ekle — mevcut `.card` kuralını bul)
- Modify (üretilmiş): `assets/css/site.min.css` — `minify.py` üretir, elle dokunma

**Interfaces:**
- Produces: `.card--media` (görselli kart varyantı) ve `.card__img` sınıfları; Task 4'ün kart şablonu bunları kullanır.

- [ ] **Step 1: Mevcut `.card` kurallarını oku**

Run: `py -c "import re,io; s=open('assets/css/site.css',encoding='utf-8').read(); [print(m.group(0)[:400]) for m in re.finditer(r'\.card[^{]*\{[^}]*\}', s)]"`
`.card`, `.card__ix`, `.cards--3` kurallarının mevcut değerlerini not et (padding, border-radius, renk tokenları).

- [ ] **Step 2: `site.css`'e görsel kart kurallarını ekle**

`.card` bloğunun hemen ardına (mevcut token adlarını ve `--radius` / renk değişkenlerini koruyarak):
```css
.card--media{padding:0;overflow:hidden;display:flex;flex-direction:column}
.card--media .card__img{display:block;width:100%;aspect-ratio:16/9;object-fit:cover;background:var(--c-surface-2,#eef2f7)}
.card--media>*:not(.card__img){padding-inline:var(--card-pad,20px)}
.card--media>.card__img+*{padding-top:16px}
.card--media>*:last-child{padding-bottom:var(--card-pad,20px)}
.card--media .card__ix{position:absolute;top:12px;left:12px;background:#fff;border-radius:8px;padding:2px 8px}
.card--media{position:relative}
```
(Step 1'de bulunan gerçek değişken adlarıyla `var(--card-pad,…)` / `var(--c-surface-2,…)` uyarla; token yoksa sabit değeri bırak.)

- [ ] **Step 3: Minify et**

Run: `py tools/minify.py`
Beklenen çıktı: `* assets/css/site.min.css ... bytes` (`*` = değişti).

- [ ] **Step 4: Doğrula**

Run: `py tools/validate_all.py`
Beklenen: `54 files — 0 with issues` (CSS değişikliği HTML'i bozmaz; sayı değişmedi).

- [ ] **Step 5: Commit**

```bash
git add assets/css/site.css assets/css/site.min.css
git commit -m "css: görselli blog kartı (.card--media / .card__img)"
```

---

## Task 3: `/rehber/` → `/blog/` atomik taşıma

Bu task tek commit'te bitmeli — ara durumda `validate_all.py` hreflang hedefleri diskte çözülemez.

**Files:**
- Rename: `git mv rehber blog`, `git mv en/rehber en/blog`, `git mv tools/gen_rehber.py tools/gen_blog.py`
- Modify: `tools/gen_blog.py` (yol sabitleri + `UI` + fonksiyon adları), `tools/gen_projects.py` (satır 49, 63, 89, 103 `UI` menü/footer; satır 1002–1004 sitemap)
- Modify: `nginx.conf`, `.htaccess`, `llms.txt`, `PROJECT.md`
- Modify ×20: kök `index.html`, `platform.html`, `hizmetler.html`, `referanslar.html`, `hakkimizda.html`, `sss.html`, `iletisim.html`, `gizlilik.html`, `tesekkurler.html`, `404.html` + `en/` karşılıkları

**Interfaces:**
- Consumes: —
- Produces: `/blog/` ve `/en/blog/` yolları; `gen_blog.py` içinde `build_blog_index()` (eski `build_rehber_index`), `BLOG_INDEX_ITEMS` (eski `REHBER_INDEX_ITEMS`). Task 4–12 bu adları kullanır.

- [ ] **Step 1: Dizinleri ve jeneratörü taşı**

```bash
git mv rehber blog
git mv en/rehber en/blog
git mv tools/gen_rehber.py tools/gen_blog.py
```

- [ ] **Step 2: `gen_blog.py` içinde yol ve ad değişimi**

`tools/gen_blog.py` içinde:
- Tüm `"/rehber/"` → `"/blog/"`, `f"/rehber/{...}"` → `f"/blog/{...}"`, `"rehber/index.html"` → `"blog/index.html"`, `"en/rehber/..."` → `"en/blog/..."`.
- `def build_rehber_index` → `def build_blog_index`; `__main__` içindeki çağrı da.
- `REHBER_INDEX_ITEMS` → `BLOG_INDEX_ITEMS`.
- `UI["tr"]`: `"guide": "Rehber"` → `"Blog"`, `"guide_eyebrow": "Rehber"` → `"Blog"`, `menu` içindeki `("/rehber/", "Rehber")` → `("/blog/", "Blog")`, `ftr_corp` içindeki `("/rehber/", "Rehber")` → `("/blog/", "Blog")`.
- `UI["en"]`: karşılık gelen `"guide"`/`"guide_eyebrow"` → `"Blog"`, `menu` & `ftr_corp` `("/rehber/", "Guide")` → `("/blog/", "Blog")`.
- `hub_title` / `hub_desc` / `hub_h1` / `hub_lede` / `hub_name` içinde "Rehber"/"rehber" geçen ibareleri "Blog"/"blog" yap (ör. TR `hub_h1: "Su kayıp-kaçak rehberi."` → `"Su kayıp-kaçak blogu."`; `hub_name` → `"Su kayıp-kaçak blogu"`; EN eşdeğerleri).

- [ ] **Step 3: `gen_projects.py` paylaşılan chrome + sitemap**

`tools/gen_projects.py`:
- Satır 49 & 63 (`UI["tr"]`): `("/rehber/", "Rehber")` → `("/blog/", "Blog")`.
- Satır 89 & 103 (`UI["en"]`): `("/rehber/", "Guide")` → `("/blog/", "Blog")`.
- Satır 1002: `u("/rehber/", "monthly", "0.8")` → `u("/blog/", "monthly", "0.8")`.
- Satır 1003–1004: slug tuple'ı `/blog/` yaz ve 8 yeni slug'ı **şimdilik EKLEME** (Task 5–12 ekler):
  ```python
  u("/blog/", "monthly", "0.8")
  for _rs in ("su-kacagi-nasil-anlasilir", "akustik-su-kacagi-tespiti-nedir", "dma-nedir", "su-kaybi-dusurme-yol-haritasi"):
      u(f"/blog/{_rs}.html", "yearly", "0.7")
  ```

- [ ] **Step 4: 20 el-HTML'de menü + footer**

Her dosyada (kök 10 + `en/` 10):
- `<nav class="nav">` içindeki `<a href="/rehber/">Rehber</a>` → `<a href="/blog/">Blog</a>` (EN dosyalarında etiket zaten "Guide" → "Blog"). `aria-current` yalnızca ilgili sayfadaysa korunur (bu 20 sayfanın hiçbiri blog değil, yani `aria-current` yok).
- Footer "Kurumsal"/"Company" listesindeki `<li><a href="/rehber/">Rehber</a></li>` → `<li><a href="/blog/">Blog</a></li>` (EN: "Guide" → "Blog").

Run (kontrol): `py -c "import glob; [print(f) for f in glob.glob('**/*.html',recursive=True) if 'rehber' in open(f,encoding='utf-8').read() and 'blog' not in f]"`
Beklenen: boş çıktı.

- [ ] **Step 5: `nginx.conf` 301 kuralı**

`location ~* \.(xml|txt)$ { ... }` bloğundan sonra, `location ^~ /en/` bloğundan **önce** ekle:
```nginx
    # eski /rehber/ yolları -> /blog/ (kalıcı)
    location ~ ^/(en/)?rehber(/.*)?$ {
        return 301 /$1blog$2;
    }
```

- [ ] **Step 6: `.htaccess` 301 yedeği**

`ErrorDocument 404 /404.html` satırından sonra ekle:
```apache
RedirectMatch 301 ^/(en/)?rehber(/.*)?$ /$1blog$2
```

- [ ] **Step 7: `llms.txt`**

- `## Rehber (kavramsal içerik)` → `## Blog`
- Tüm `https://sukayipkacaklari.com/rehber/...` → `.../blog/...` (5 TR link + `## Blog` altındaki hub linki)
- EN satırındaki `[Guide](https://sukayipkacaklari.com/en/rehber/)` → `[Blog](https://sukayipkacaklari.com/en/blog/)`

- [ ] **Step 8: `PROJECT.md`**

- §5 tablosu: `/rehber/` satırı → `/blog/` "Blog hub"; `/rehber/*.html (4)` → `/blog/*.html (12)`; başlık satırı "TR 25 + EN 25" → "TR 33 + EN 33"; toplam 50 → 66.
- §5 EN parite paragrafı: `/en/rehber/` → `/en/blog/`.
- §6 tablosu: `tools/gen_rehber.py` → `tools/gen_blog.py`; açıklamada "4'er makale" → "12'şer makale".
- §6 nginx notu: `/en/` 404 satırının yanına "eski `/rehber/` → `/blog/` 301 kuralı da `custom_nginx_configuration` PATCH gerektirir" cümlesi.
- §8'e yeni satır: `| **F** (2026-09-04) | /rehber/ → /blog/ taşındı (301'li), hub+makale kartları görselli, 8 yeni makale (debi ölçümü, basınç yönetimi, adım testi, sıfır basınç testi, hidrolik modelleme, boru hattı tespiti, şebeke haritalama/CBS, kaçak onarımı) TR+EN |`

- [ ] **Step 9: Yeniden üret**

```bash
py tools/gen_blog.py && py tools/gen_projects.py && py tools/add_img_dims.py
```
Beklenen: `blog/index.html`, `blog/*.html` (4), `en/blog/...` yazıldı; `rehber/` ve `en/rehber/` dizinleri boş/yok.

- [ ] **Step 10: Doğrula**

```bash
py tools/validate_all.py
py tools/linkcheck.py
```
Beklenen: `validate_all` → `0 with issues`; `linkcheck` → 0 kırık link. Dosya sayısı hâlâ 54.
Ek kontrol: `py -c "import glob; print([f for f in glob.glob('**/*.html',recursive=True) if '/rehber/' in open(f,encoding='utf-8').read()])"` → `[]`.

- [ ] **Step 11: Commit**

```bash
git add -A
git commit -m "refactor: /rehber/ -> /blog/ taşındı (301'li), etiket 'Blog'"
```

---

## Task 4: Görselli kart şablonu + 4 mevcut makaleye hero

**Files:**
- Modify: `tools/gen_blog.py` — `build_article` (hero `<figure>`), `build_blog_index` (kart şablonu), `article_schema` (opsiyonel `image`/`date` parametresi), `ARTICLES` (4 dict'e `hero`+`hero_alt`+`hero_alt_en`), `BLOG_INDEX_ITEMS` (kartlara görsel için 4. alan)

**Interfaces:**
- Consumes: Task 1 hero tablosu; Task 2 `.card--media` / `.card__img`.
- Produces: `article_schema(headline, desc, url, section, ld_lang, image=None, date="2026-09-04")` imzası; `ARTICLES` dict'lerinde `hero` (str, `/assets/...` yolu), `hero_alt`, `hero_alt_en` alanları; `BLOG_INDEX_ITEMS` girişleri `(slug, tr_title, tr_desc, en_title, en_desc, hero)` 6'lı tuple. Task 5–12 bu şekli izler.

- [ ] **Step 1: `article_schema`'ya görsel/ tarih parametresi**

`tools/gen_blog.py` `article_schema`:
```python
def article_schema(headline, desc, url, section, ld_lang, image=None, date="2026-09-04"):
    img = f"https://sukayipkacaklari.com{image}" if image else "https://sukayipkacaklari.com/assets/img/og-cover.png"
    return ('<script type="application/ld+json">\n{\n'
            '  "@context": "https://schema.org",\n'
            '  "@type": "Article",\n'
            f'  "headline": "{headline}",\n'
            f'  "description": "{desc}",\n'
            f'  "mainEntityOfPage": {{ "@type": "WebPage", "@id": "{url}" }},\n'
            f'  "articleSection": "{section}",\n'
            f'  "inLanguage": "{ld_lang}",\n'
            '  "author": { "@type": "Organization", "name": "LeakExpert", "url": "https://sukayipkacaklari.com/" },\n'
            '  "publisher": { "@type": "Organization", "name": "LeakExpert", "url": "https://sukayipkacaklari.com/",\n'
            '    "logo": { "@type": "ImageObject", "url": "https://sukayipkacaklari.com/assets/img/icon.png" } },\n'
            f'  "image": "{img}",\n'
            f'  "datePublished": "{date}", "dateModified": "{date}"\n'
            '}\n</script>')
```
Mevcut 4 makalenin `date`'i 2026-09-01 kalsın diye: `ARTICLES` dict'lerine `date="2026-09-01"` ekle, `build_article` çağrısında `a.get("date","2026-09-04")` geçir.

- [ ] **Step 2: `build_article`'a hero `<figure>`**

`build_article` içinde, `schema` listesindeki `article_schema(...)` çağrısına `image=a.get("hero"), date=a.get("date","2026-09-04")` ekle. `<section class="phead">` bloğunun kapanışından sonra, `<section class="section">` gövdesinden önce:
```python
    hero_html = ""
    if a.get("hero"):
        hero_html = f"""
  <div class="wrap mw-900">
    <figure class="article-hero"><img src="{a['hero']}" alt="{L(a, 'hero_alt', lang)}" loading="eager"></figure>
  </div>"""
```
ve `body` f-string'inde `<section class="phead">…</section>` ile `<section class="section">` arasına `{hero_html}` yerleştir.

- [ ] **Step 3: Hub kart şablonunu görselli yap**

`build_blog_index` içinde `items` artık 4'lü değil; `BLOG_INDEX_ITEMS` 6'lı tuple (`s, tt, dt, ten, den, hero`). `items` kavrayışını ve `cards` kavrayışını güncelle:
```python
    items = [(s, (ten if lang == "en" else tt), (den if lang == "en" else dt), hero)
             for s, tt, dt, ten, den, hero in BLOG_INDEX_ITEMS]
    ...
    cards = "\n".join(
        f'        <a class="card card--media rv" href="{rel_href(lang, "/blog/" + s + ".html")}">'
        f'<img class="card__img" src="{hero}" alt="" loading="lazy" decoding="async">'
        f'<span class="card__ix">{i+1:02d}</span>'
        f'<h3>{t}</h3><p>{d}</p></a>'
        for i, (s, t, d, hero) in enumerate(items))
```
`item_list` (JSON-LD) kavrayışı `for i, (s, t, d, hero) in enumerate(items)` olacak şekilde 4'lü unpack'e güncelle.

- [ ] **Step 4: 4 mevcut makaleye `hero` alanları**

`ARTICLES` içindeki 4 dict'e ekle (Task 1 tablosundan):
- `su-kacagi-nasil-anlasilir`: `hero="/assets/photos/gunduz-dinleme.webp"`, `hero_alt="Gündüz saha dinleme çalışması"`, `hero_alt_en="Daytime field listening survey"`, `date="2026-09-01"`
- `akustik-su-kacagi-tespiti-nedir`: `hero="/assets/photos/gece-dinleme-hero.webp"`, `hero_alt="Gece akustik dinleme"`, `hero_alt_en="Night-time acoustic listening"`, `date="2026-09-01"`
- `dma-nedir`: `hero="/assets/photos/dma-tasarim.webp"`, `hero_alt="DMA sınır ve sayaç tasarımı"`, `hero_alt_en="DMA boundary and meter design"`, `date="2026-09-01"`
- `su-kaybi-dusurme-yol-haritasi`: `hero="/assets/photos/depo-cikis.webp"`, `hero_alt="Depo çıkışı debi ölçüm noktası"`, `hero_alt_en="Reservoir outlet flow metering point"`, `date="2026-09-01"`

`BLOG_INDEX_ITEMS`'daki 4 satıra 6. alan olarak aynı hero yollarını ekle.

- [ ] **Step 5: `site.css`'e `.article-hero`**

`assets/css/site.css`'e:
```css
.article-hero{margin:0 0 8px;border-radius:var(--radius,12px);overflow:hidden}
.article-hero img{display:block;width:100%;aspect-ratio:16/9;object-fit:cover}
```
Sonra `py tools/minify.py`.

- [ ] **Step 6: Yeniden üret + doğrula**

```bash
py tools/gen_blog.py && py tools/gen_projects.py && py tools/add_img_dims.py && py tools/minify.py
py tools/validate_all.py && py tools/linkcheck.py
```
Beklenen: 0 issue, 0 kırık link. `blog/index.html` içinde `card--media` ve `card__img` var; `blog/dma-nedir.html` içinde `<figure class="article-hero">` var ve `<img>`'de `width`/`height` var (add_img_dims ekledi).

- [ ] **Step 7: Commit**

```bash
git add -A
git commit -m "blog: görselli hub kartları + 4 makaleye hero görsel"
```

---

## Task 5–12: 8 yeni makale (her biri bir task)

Her makale task'ı **aynı iskeleti** izler. Ortak talimat (her task'a uygula):

**Files (her makale task'ı):**
- Modify: `tools/gen_blog.py` — `ARTICLES` listesine 1 dict; `BLOG_INDEX_ITEMS` listesine 1 satır (doğru sırada — aşağıdaki "Hub sırası")
- Modify: `tools/gen_projects.py` — satır ~1003 `for _rs in (...)` tuple'ına slug ekle (doğru sırada)

**Interfaces (her makale task'ı):**
- Consumes: Task 4 `ARTICLES` dict şekli (`slug, h1, title, desc, lede, card_desc, hero, hero_alt, hero_alt_en, h1_en, title_en, desc_en, lede_en, card_desc_en, body, body_en`) ve `BLOG_INDEX_ITEMS` 6'lı tuple şekli.
- Produces: `/blog/<slug>.html` + `/en/blog/<slug>.html`.

**Ortak adımlar:**

- [ ] **Step 1: `ARTICLES`'a dict ekle** — metadata (title/desc/lede) aşağıdaki makale brief'inden; `body` / `body_en` bir `<div class="prose">` içinde brief'teki `<h2>` başlıklarıyla, her biri altında 1–3 `<p>`. Uzunluk ~600–900 kelime. Global Constraints'e birebir uy. İç linkler brief'te verilen slug'lara: `<a href="/blog/<slug>.html">` (EN gövdede `/en/blog/...`, `/en/hizmetler.html` vb.). Kapanış `<h2>`'si + `<ul>` ile `/hizmetler.html`, `/projeler/`, `/sss.html` linkleri (EN'de `/en/` önekli).
- [ ] **Step 2: `BLOG_INDEX_ITEMS`'a satır ekle** — `("<slug>", "<kart başlığı TR>", "<kart açıklaması TR ≤95 krk>", "<kart başlığı EN>", "<kart açıklaması EN ≤95 krk>", "<hero yolu>")`, "Hub sırası"ndaki konuma yerleştir.
- [ ] **Step 3: `gen_projects.py` sitemap slug tuple'ına `<slug>` ekle** — "Hub sırası"ndaki konuma.
- [ ] **Step 4: Üret + doğrula** —
  ```bash
  py tools/gen_blog.py && py tools/gen_projects.py && py tools/add_img_dims.py
  py tools/validate_all.py && py tools/linkcheck.py
  ```
  Beklenen: `56 files — 0 with issues` (Task 5'te ilk artıştan sonra sayı her task'ta +2), 0 kırık link. `sitemap.xml` içinde yeni `/blog/<slug>.html` + `/en/blog/<slug>.html`, hreflang üçlüsüyle.
- [ ] **Step 5: Commit** — `git add -A && git commit -m "blog: <slug> makalesi (TR+EN)"`

**Hub sırası** (`BLOG_INDEX_ITEMS` ve sitemap tuple bu sırada olsun; 01–12):
1. su-kacagi-nasil-anlasilir *(mevcut)*
2. **debi-olcumu-nedir** (Task 5)
3. **basinc-yonetimi-nedir** (Task 6)
4. akustik-su-kacagi-tespiti-nedir *(mevcut)*
5. dma-nedir *(mevcut)*
6. **adim-testi-nedir** (Task 7)
7. **sifir-basinc-testi-nedir** (Task 8)
8. **hidrolik-modelleme-nedir** (Task 9)
9. **boru-hatti-tespiti-nedir** (Task 10)
10. **sebeke-haritalama-cbs** (Task 11)
11. **kacak-onarimi-ve-dogrulama** (Task 12)
12. su-kaybi-dusurme-yol-haritasi *(mevcut)*

> `build_blog_index` kartları `BLOG_INDEX_ITEMS` sırasına göre 01–12 numaralandırır; listeyi yukarıdaki sırada tut. `ARTICLES` sırası önemsiz (makale sayfalarını üretir), ama okunurluk için aynı sırada tutulması önerilir.

---

### Task 5: `debi-olcumu-nedir`

**Metadata:**
- `slug="debi-olcumu-nedir"`
- `h1="Debi ölçümü nedir, şebekede nasıl yapılır?"`
- `title="Debi Ölçümü Nedir? Şebekede Debi Nasıl Ölçülür | LeakExpert"`
- `desc="Şebekede debi ölçümünün amacı, taşınabilir ultrasonik/elektromanyetik debimetre ile geçici ölçüm, kalıcı bölge sayacı, gece minimum debi ve doğruluğu etkileyen etkenler."` (≤160 krk)
- `lede="Kaybı yönetmek için önce <strong>ne kadar su aktığını</strong> bilmek gerekir. Debi ölçümü, bir hattan veya bölgeden birim zamanda geçen su hacmini ölçer; su kayıp-kaçak çalışmasının ilk sayısal adımıdır."`
- `card_desc="Taşınabilir ve kalıcı debimetreler, ölçüm noktası seçimi ve gece minimum debi."`
- `hero="/assets/photos/debi-olcum.webp"`, `hero_alt="Hat üzerinde taşınabilir ultrasonik debimetre kurulumu"`, `hero_alt_en="Portable ultrasonic flow meter clamped on a main"`
- EN: `h1_en="What is flow measurement, and how is it done in a network?"`, `title_en="What Is Flow Measurement? How Flow Is Measured in a Network | LeakExpert"`, `desc_en="The purpose of network flow measurement, temporary measurement with a portable ultrasonic/electromagnetic flow meter, permanent zone meters, minimum night flow and what affects accuracy."`, `lede_en="To manage loss you first need to know <strong>how much water is flowing</strong>. Flow measurement quantifies the volume passing a main or a zone per unit time; it is the first numerical step of any water-loss programme."`, `card_desc_en="Portable and permanent flow meters, choosing the measuring point, minimum night flow."`

**Gövde `<h2>` başlıkları (her biri 1–3 `<p>`):**
1. Debi neden ölçülür? — kayıp tespitinin sayısal temeli, DMA giriş/çıkış dengesi, tüketim profili
2. Taşınabilir ölçüm: kelepçeli ultrasonik debimetre — hızlı kurulum, hatta kesinti yok, geçici kampanya; düz boru şartı (giriş/çıkışta düz uzunluk), boru dolu olmalı
3. Kalıcı ölçüm: bölge (DMA) sayacı — elektromanyetik sayaç + veri kaydı/telemetri, sürekli izleme
4. Ölçüm noktası nasıl seçilir? — depo çıkışı, bölge sınır vanası, düz hat, türbülanstan uzak, erişim
5. Gece minimum debisi — 03:00–05:00 arası en düşük akış; sabit abonede artış = yeni fiziki kaçak (bkz. `dma-nedir`, `adim-testi-nedir`)
6. Doğruluğu ne etkiler? — boru iç çapı/malzeme girişi, hava/kısmi dolu boru, sensör teması, kalibrasyon
7. Ölçümden sonuca — veriler LeakExpert platformuna işlenir, kayıp bölgeleri önceliklendirilir

**İç linkler:** `dma-nedir`, `adim-testi-nedir`, `/hizmetler.html`, `/projeler/`, `/sss.html`
**Kaçın:** cihaz markası, "ev sayacı"/konut içi, saha ziyareti CTA'sı.

---

### Task 6: `basinc-yonetimi-nedir`

**Metadata:**
- `slug="basinc-yonetimi-nedir"`
- `h1="Basınç yönetimi ve basınç bölgeleri (PMA)"`
- `title="Basınç Yönetimi Nedir? Basınç Bölgeleri ve PMA | LeakExpert"`
- `desc="Şebekede yüksek ve dalgalı basıncın kaçak ve patlaklarla ilişkisi, basınç bölgesi (PMA) kurulumu, basınç düşürücü vana ve sabit/zaman/akış kontrollü ayar."`
- `lede="Şebekedeki her fazla metre basınç, hem yeni patlak riskini hem de mevcut kaçakların debisini artırır. <strong>Basınç yönetimi</strong>, şebekeyi gerektiği kadar — ne fazla, ne eksik — basınçta tutma işidir."`
- `card_desc="Basınç–kaçak ilişkisi, basınç bölgesi (PMA) ve basınç düşürücü vana ayarı."`
- `hero="/assets/photos/basinc-logger.webp"`, `hero_alt="Hat üzerinde basınç veri loggerı"`, `hero_alt_en="Pressure data logger on a main"`
- EN: `h1_en="Pressure management and pressure zones (PMA)"`, `title_en="What Is Pressure Management? Pressure Zones and PMA | LeakExpert"`, `desc_en="How high and fluctuating pressure drives leaks and bursts, setting up a pressure managed area (PMA), pressure reducing valves and fixed/time/flow-modulated control."`, `lede_en="Every extra metre of pressure in a network raises both the risk of new bursts and the flow rate of existing leaks. <strong>Pressure management</strong> is the work of keeping the network at just the pressure it needs — no more, no less."`, `card_desc_en="The pressure–leak link, pressure managed areas (PMA) and pressure reducing valve control."`

**Gövde `<h2>`:**
1. Basınç ile kaçak arasındaki ilişki — kaçak debisi basınçla artar (N1 üssü kavramı, sızıntılarda ~1); patlak sıklığı yüksek/dalgalı basınçla artar
2. Basınç bölgesi (PMA) nedir? — kot ve besleme yönünden benzer, sınırları kapalı, tek noktadan beslenen alan; DMA ile ilişkisi (bkz. `dma-nedir`)
3. Basınç düşürücü vana — bölge girişine konur, çıkış basıncını hedefe indirir
4. Ayar tipleri — sabit çıkış; zaman kontrollü (gece daha düşük); akış kontrollü (talep düştükçe basınç düşer)
5. Hedef basınç nasıl belirlenir? — en kritik (en yüksek kot / en uzak) abonede minimum servis basıncı korunarak
6. Kazanç nasıl ölçülür? — öncesi/sonrası gece minimum debi ve patlak sayısı; kalıcı loggerla izleme
7. Tasarımın doğrulanması — saha ölçümleri hidrolik modele işlenir (bkz. `hidrolik-modelleme-nedir`)

**İç linkler:** `dma-nedir`, `su-kaybi-dusurme-yol-haritasi`, `hidrolik-modelleme-nedir`, `/hizmetler.html`, `/sss.html`
**Kaçın:** vana markası/modeli, konut içi tesisat basıncı.

---

### Task 7: `adim-testi-nedir`

**Metadata:**
- `slug="adim-testi-nedir"`
- `h1="Adım (step) testi ile kaçak bölgeleme"`
- `title="Adım (Step) Testi Nedir? Gece Kademeli Vana Kapatma | LeakExpert"`
- `desc="Adım testi, bir DMA içinde gece vanaları kademeli kapatarak debi düşüşlerinden kaybın hangi alt hatta yoğunlaştığını bulur. Hazırlık, uygulama, yorumlama ve riskler."`
- `lede="Bir bölgede kayıp olduğunu bilmek yetmez; <strong>hangi sokakta</strong> olduğunu daraltmak gerekir. Adım testi, gece boyunca vanaları sırayla kapatıp her adımda debinin ne kadar düştüğüne bakarak kaybı alt hatlara böler."`
- `card_desc="Gece vanaları kademeli kapatıp debi düşüşünden kaybı alt hatlara daraltma."`
- `hero="/assets/photos/gece-operasyon.webp"`, `hero_alt="Gece saha operasyonu"`, `hero_alt_en="Night-time field operation"`
- EN: `h1_en="Step testing to narrow down leakage"`, `title_en="What Is a Step Test? Night-time Stepped Valve Closing | LeakExpert"`, `desc_en="A step test closes valves in sequence at night within a DMA and reads the flow drops to find which sub-section holds the loss. Preparation, execution, interpretation and risks."`, `lede_en="Knowing a zone has loss is not enough; you need to narrow down <strong>which street</strong> it is on. A step test closes valves one by one through the night and watches how much flow drops at each step, splitting the loss between sub-sections."`, `card_desc_en="Closing valves in steps at night and reading the flow drop to narrow the loss."`

**Gövde `<h2>`:**
1. Amaç — DMA içinde kaybı sokak/alt hat düzeyine indirmek; akustik taramadan önce alan daraltma (bkz. `akustik-su-kacagi-tespiti-nedir`)
2. Ön hazırlık — güncel şebeke haritası, vana listesi ve sırası, sağlam vanaların teyidi, gece penceresi (düşük tüketim), abonelere bilgilendirme
3. Uygulama — giriş debisi sürekli kaydedilirken vanalar sondan başa doğru tek tek kapatılır; her kapatmadan sonra debi sabitlenene kadar beklenir
4. Debi basamaklarının okunması — bir adımda büyük düşüş = o alt hatta yüksek kayıp; küçük düşüş = temiz
5. Yorumlama ve sonraki adım — yüksek kayıplı alt hatlar akustik ekibe öncelik listesi olarak verilir
6. Riskler ve önlemler — basınç dalgalanması ve bulanıklık, yangın suyu erişimi, vananın açık kalması; kapatmalar yavaş yapılır, test sonunda tüm vanalar açılır ve teyit edilir

**İç linkler:** `dma-nedir`, `debi-olcumu-nedir`, `akustik-su-kacagi-tespiti-nedir`, `/hizmetler.html`, `/projeler/`
**Kaçın:** "anında onarım", konut içi.

---

### Task 8: `sifir-basinc-testi-nedir`

**Metadata:**
- `slug="sifir-basinc-testi-nedir"`
- `h1="Sıfır basınç testi nedir?"`
- `title="Sıfır Basınç Testi Nedir? Hat İzolasyon Kontrolü | LeakExpert"`
- `desc="Sıfır basınç testi, izole edilen bir hat bölümünde basıncı sıfıra indirip basıncın geri gelip gelmediğine bakarak o bölümde kaçak olup olmadığını doğrular. Uygulama adımları ve güvenlik."`
- `lede="Bazen bir hat bölümünden şüphelenilir ama kesin karar verilemez. <strong>Sıfır basınç testi</strong>, o bölümü izole edip basıncını sıfıra düşürür: basınç yavaşça geri geliyorsa içeride hâlâ su besleyen bir yol — çoğu zaman bir kaçak — vardır."`
- `card_desc="Bir hat bölümünü izole edip basıncı sıfıra indirerek kaçak var/yok kararı."`
- `hero="/assets/blog/sifir-basinc-testi-nedir.webp"`, `hero_alt="Vana odasında hat izolasyonu"`, `hero_alt_en="Line isolation at a valve chamber"`
- EN: `h1_en="What is a zero-pressure test?"`, `title_en="What Is a Zero-Pressure Test? Line Isolation Check | LeakExpert"`, `desc_en="A zero-pressure test isolates a section of main, drops its pressure to zero and watches whether pressure returns, confirming whether that section leaks. Steps and safety."`, `lede_en="Sometimes a section of main is suspected but cannot be ruled in or out. A <strong>zero-pressure test</strong> isolates that section and drops its pressure to zero: if pressure creeps back, something is still feeding water in — usually a leak."`, `card_desc_en="Isolating a section and dropping pressure to zero to decide leak or no leak."`

**Gövde `<h2>`:**
1. Ne zaman uygulanır? — adım testi veya akustik sonrası şüpheli kalan bölüm; kısa, tanımlı bir hat parçası (bkz. `adim-testi-nedir`)
2. Bölümü izole etme — sınır vanaları kapatılır ve sızdırmazlığı teyit edilir; test bölümüne bir basınç kaydedici bağlanır
3. Basıncı sıfıra indirme — hidrant veya tahliye noktasından kontrollü boşaltma; basınç sıfıra iner
4. Gözlem — tahliye kapatılır; basınç sabit sıfırda kalıyorsa bölüm sağlam, yavaşça yükseliyorsa besleyen bir yol (kaçak veya sızdıran vana) var
5. Sonucun yorumu — vana sızıntısı mı gerçek kaçak mı ayrımı; kaçaksa akustik ile nokta tespiti (bkz. `akustik-su-kacagi-tespiti-nedir`)
6. Güvenlik ve su kalitesi — negatif basınç ve geri emilim riski, test sonrası hattın basınçlandırılması ve gerekiyorsa dezenfeksiyon/ yıkama, abone bilgilendirmesi

**İç linkler:** `adim-testi-nedir`, `akustik-su-kacagi-tespiti-nedir`, `/hizmetler.html`, `/sss.html`
**Kaçın:** cihaz markası, konut içi tesisat testi, "anında onarım".

---

### Task 9: `hidrolik-modelleme-nedir`

**Metadata:**
- `slug="hidrolik-modelleme-nedir"`
- `h1="Hidrolik modelleme ve saha kalibrasyonu"`
- `title="Hidrolik Modelleme Nedir? Şebeke Modeli ve Saha Kalibrasyonu | LeakExpert"`
- `desc="Hidrolik model, içme suyu şebekesinin bilgisayar benzetimidir. Model girdileri, saha basınç-debi ölçümleriyle kalibrasyon, kayıp ve basınç yönetimi senaryoları ve modelin sınırları."`
- `lede="Bir şehir şebekesinde \"şu vanayı kısarsam uçtaki basınç ne olur?\" sorusunu sahada denemek pahalıdır. <strong>Hidrolik model</strong>, şebekenin borularını, kotlarını ve tüketimini bilgisayarda kurup bu soruları önceden yanıtlar."`
- `card_desc="Şebekenin bilgisayar benzetimi: girdi verisi, saha kalibrasyonu ve senaryolar."`
- `hero="/assets/photos/basinc-test.webp"`, `hero_alt="Sahada basınç ölçümü"`, `hero_alt_en="Field pressure measurement"`
- EN: `h1_en="Hydraulic modelling and field calibration"`, `title_en="What Is Hydraulic Modelling? Network Model and Field Calibration | LeakExpert"`, `desc_en="A hydraulic model is a computer simulation of a drinking-water network. Model inputs, calibration against field pressure and flow measurements, loss and pressure-management scenarios, and the model's limits."`, `lede_en="Testing \"what happens to end-of-line pressure if I throttle this valve?\" in the field is expensive. A <strong>hydraulic model</strong> builds the network's pipes, elevations and demand in software and answers those questions in advance."`, `card_desc_en="A computer simulation of the network: input data, field calibration and scenarios."`

**Gövde `<h2>`:**
1. Model nedir, ne işe yarar? — boru ağı + talep + sınır koşullarının benzetimi; basınç yönetimi tasarımı, yeni yatırım, kayıp senaryoları
2. Girdi verileri — boru güzergâhı, çap, malzeme, pürüzlülük; düğüm kotları; abone/bölge tüketimi; depo seviyeleri, pompa eğrileri (harita/CBS'ten — bkz. `sebeke-haritalama-cbs`)
3. Talep dağıtımı — toplam üretimin düğümlere abone/kayıt oranına göre paylaştırılması; günlük tüketim profili
4. Saha kalibrasyonu — birkaç noktada eşzamanlı basınç ve debi ölçümü; model çıktısı ölçümle örtüşene kadar pürüzlülük/talep düzeltmesi (bkz. `debi-olcumu-nedir`)
5. Senaryolar — basınç düşürücü vana hedefi, bölge sınırlarının değişmesi, yangın debisi, kayıp azaltmanın gece debisine etkisi
6. Modelin sınırları — girdi verisi kadar iyidir; eski/eksik CBS, bilinmeyen kapalı vanalar, kayıt dışı bağlantılar sonucu bozar; model periyodik güncellenir

**İç linkler:** `basinc-yonetimi-nedir`, `dma-nedir`, `sebeke-haritalama-cbs`, `debi-olcumu-nedir`, `/hizmetler.html`
**Kaçın:** yazılım ürün adı, konut içi.

---

### Task 10: `boru-hatti-tespiti-nedir`

**Metadata:**
- `slug="boru-hatti-tespiti-nedir"`
- `h1="Boru hattı güzergâhı ve derinlik tespiti"`
- `title="Boru Hattı Tespiti Nedir? Güzergâh ve Derinlik Belirleme | LeakExpert"`
- `desc="Gömülü içme suyu hatlarının güzergâhı ve derinliği nasıl belirlenir: metal hatlarda elektromanyetik hat dedektörü, plastik hatlarda dâhili prob, sinyal teli ve yer radarı (GPR)."`
- `lede="Kaçağı bulmadan, onarmadan veya haritalamadan önce çoğu zaman ilk soru şudur: <strong>boru tam olarak nerede ve ne kadar derinde?</strong> Hat tespiti, gömülü hattı kazmadan yüzeyden işaretleme işidir."`
- `card_desc="Metal ve plastik gömülü hatların güzergâh ve derinliğini kazısız belirleme."`
- `hero="/assets/blog/boru-hatti-tespiti-nedir.webp"`, `hero_alt="Saha ekibi hat güzergâhını işaretliyor"`, `hero_alt_en="Field crew marking a pipe route"`
- EN: `h1_en="Locating a pipe route and depth"`, `title_en="What Is Pipe Locating? Determining Route and Depth | LeakExpert"`, `desc_en="How the route and depth of buried drinking-water mains are found: electromagnetic pipe locators on metal mains, and internal probes, tracer wire and ground penetrating radar (GPR) on plastic mains."`, `lede_en="Before finding a leak, repairing it or mapping it, the first question is often: <strong>exactly where is the pipe, and how deep?</strong> Pipe locating is marking a buried main from the surface without digging."`, `card_desc_en="Finding the route and depth of buried metal and plastic mains without excavation."`

**Gövde `<h2>`:**
1. Neden gerekir? — onarım kazısı, yeni bağlantı, hasar önleme, CBS'e işleme (bkz. `sebeke-haritalama-cbs`), model girdisi
2. Metal hatlar: elektromanyetik hat dedektörü — vericiyle hatta sinyal bindirilir, alıcı yüzeyden güzergâhı ve derinliği okur; doğrudan bağlantı veya kelepçe
3. Plastik (PE/PVC) hatlar — iletken olmadığı için: hat içine itilen problu kablo, döşemede bırakılan sinyal teli, ya da yer radarı (GPR)
4. Yer radarı (GPR) — zemine radar dalgası gönderip yansımalardan gömülü nesneleri görüntüler; her zemin/derinlikte aynı sonucu vermez
5. İşaretleme ve derinlik — güzergâh sprey/kazık ile işaretlenir, derinlik noktasal ölçülür, koordinatlar kaydedilir
6. Doğruluğun sınırları — paralel metal borular, yoğun altyapı, ıslak killi zemin sinyali bozar; derinlik tahmini yaklaşık kabul edilir, kritik kazıda el çukuru açılır

**İç linkler:** `sebeke-haritalama-cbs`, `hidrolik-modelleme-nedir`, `/hizmetler.html`, `/projeler/`
**Kaçın:** dedektör markası, "kablo/elektrik kaçağı" (kapsam su hattı), konut içi.

---

### Task 11: `sebeke-haritalama-cbs`

**Metadata:**
- `slug="sebeke-haritalama-cbs"`
- `h1="Şebeke haritalama ve CBS'e (GIS) aktarım"`
- `title="Şebeke Haritalama ve CBS (GIS) Aktarımı Nedir? | LeakExpert"`
- `desc="Saha tespiti verisinin coğrafi bilgi sistemine dönüşmesi: GPS koordinat, öznitelik (çap, malzeme, döşeme yılı), CBS katmanı ve topoloji, platforma işleme ve haritayı güncel tutma."`
- `lede="Bir şebekeyi ancak <strong>güncel bir haritası varsa</strong> yönetebilirsiniz. Şebeke haritalama, sahadaki boruları, vanaları ve bağlantıları konumları ve özellikleriyle birlikte sayısal bir sisteme geçirir."`
- `card_desc="Saha verisini GPS koordinat ve özniteliklerle CBS katmanına ve platforma işleme."`
- `hero="/assets/blog/sebeke-haritalama-cbs.webp"`, `hero_alt="Şebeke haritası ekranı"`, `hero_alt_en="Network map on screen"`
- EN: `h1_en="Network mapping and transfer to GIS"`, `title_en="What Is Network Mapping and GIS Transfer? | LeakExpert"`, `desc_en="Turning field survey data into a geographic information system: GPS coordinates, attributes (diameter, material, year laid), the GIS layer and topology, transfer to the platform and keeping the map current."`, `lede_en="You can only manage a network if you have a <strong>current map</strong> of it. Network mapping moves the field's pipes, valves and connections — with their locations and properties — into a digital system."`, `card_desc_en="Turning field data with GPS coordinates and attributes into a GIS layer and the platform."`

**Gövde `<h2>`:**
1. Saha tespitinden veriye — hat güzergâhı ve derinliği (bkz. `boru-hatti-tespiti-nedir`), vana/hidrant/bağlantı konumları GPS ile ölçülür
2. Öznitelikler — her hat için çap, malzeme, döşeme yılı, basınç bölgesi; her vana için tip ve durum
3. CBS katmanı ve topoloji — noktalar ve hatların birbirine bağlı (topolojik) olması; hangi vananın hangi hattı kestiğinin sistemce bilinmesi
4. Doğruluk sınıfı — GPS ölçüm hassasiyeti, eski paftaların sayısallaştırılması, saha teyidi
5. Platforma işleme — veriler LeakExpert platformuna aktarılır; kaçak noktaları, ölçümler ve projeler aynı harita üzerinde (bkz. `/platform.html`)
6. Haritayı güncel tutma — her yeni bağlantı, onarım ve hat yenileme haritaya işlenir; güncel olmayan CBS model ve kayıp analizini bozar (bkz. `hidrolik-modelleme-nedir`)

**İç linkler:** `boru-hatti-tespiti-nedir`, `hidrolik-modelleme-nedir`, `/platform.html`, `/hizmetler.html`
**Kaçın:** CBS yazılım ürün adı, konut içi.

---

### Task 12: `kacak-onarimi-ve-dogrulama`

**Metadata:**
- `slug="kacak-onarimi-ve-dogrulama"`
- `h1="Kaçak onarımı ve onarım sonrası doğrulama"`
- `title="Kaçak Onarımı ve Onarım Sonrası Doğrulama | LeakExpert"`
- `desc="Tespit edilen kaçak noktasının onarım süreci ve onarımın gerçekten kapandığının doğrulanması: nokta teyidi, onarım tipleri, onarım sonrası gece debi tekrar ölçümü ve kapanan kayıp raporu."`
- `lede="Bir kaçağı bulmak işin yarısıdır; diğer yarısı onarımın <strong>gerçekten</strong> kaybı kapattığını göstermektir. Bu yazı, onarım sürecini ve onarım sonrası doğrulamayı özetler."`
- `card_desc="Nokta teyidi, onarım tipleri ve onarım sonrası gece debi ile kapanan kaybın doğrulanması."`
- `hero="/assets/blog/kacak-onarimi-ve-dogrulama.webp"`, `hero_alt="Kaçak noktasında onarım kazısı"`, `hero_alt_en="Repair excavation at a leak point"`
- EN: `h1_en="Leak repair and post-repair verification"`, `title_en="Leak Repair and Post-Repair Verification | LeakExpert"`, `desc_en="The repair process for a located leak point and confirming the loss is actually closed: point confirmation, repair types, repeat minimum-night-flow measurement after repair and the recovered-loss report."`, `lede_en="Finding a leak is half the job; the other half is showing the repair <strong>actually</strong> closed the loss. This article outlines the repair process and post-repair verification."`, `card_desc_en="Point confirmation, repair types, and verifying recovered loss with post-repair night flow."`

**Gövde `<h2>`:**
1. Kazı öncesi son teyit — akustik ile noktanın son kez dinlenmesi, işaretleme, hat derinliği ve diğer altyapı kontrolü (bkz. `akustik-su-kacagi-tespiti-nedir`, `boru-hatti-tespiti-nedir`)
2. Onarımı kim yapar? — kazı ve onarım idarenin veya yüklenicinin ekibince yapılır; LeakExpert'in rolü nokta tespiti ve onarım sonrası doğrulamadır
3. Onarım tipleri — tamir kelepçesi (küçük delik/çatlak), boru parçası değişimi, bağlantı/vana yenilemesi, ileri düzeyde hat yenileme
4. Onarım sonrası test — hat basınçlandırılır, birleşim yeri kontrol edilir, gerekiyorsa yıkama/dezenfeksiyon
5. Doğrulama: gece debisi tekrar — onarım öncesi ve sonrası bölge gece minimum debisi karşılaştırılır; düşüş = kapanan kaçak debisi (bkz. `debi-olcumu-nedir`, `dma-nedir`)
6. Raporlama — nokta koordinatı, onarım tarihi (idare bildirimi), öncesi/sonrası debi ve kapanan kayıp platforma işlenir; kapanmayan noktalar tekrar listeye alınır

**İç linkler:** `akustik-su-kacagi-tespiti-nedir`, `debi-olcumu-nedir`, `dma-nedir`, `su-kaybi-dusurme-yol-haritasi`, `/hizmetler.html`, `/projeler/`
**Kaçın:** "anında onarıldı", "onarım bekleyen arıza", onarımı LeakExpert yapıyormuş gibi ifade, konut içi.

---

## Task 13: Deploy ve canlı doğrulama

**Files:**
- Modify (canlı, repo dışı): Coolify `custom_nginx_configuration`

**Interfaces:**
- Consumes: Task 3 `nginx.conf` (301 kuralı dâhil).

- [ ] **Step 1: Tam doğrulama zinciri**

```bash
py tools/gen_blog.py && py tools/gen_projects.py && py tools/add_img_dims.py && py tools/minify.py
py tools/validate_all.py
py tools/linkcheck.py
```
Beklenen: `validate_all` → `70 files — 0 with issues` (33 TR + 33 EN + 4 noindex/paylaşılan; sayı Task 3 öncesi 54 + 16 yeni = 70); `linkcheck` → 0 kırık.

- [ ] **Step 2: `git push`**

```bash
git push
```
Coolify `main`'e push'ta otomatik deploy eder. Deploy durumunu bekle (Coolify MCP `list_deployments` → `get_deployment`).

- [ ] **Step 3: nginx config PATCH (301 kuralı için)**

`PROJECT.md` §4 yordamı:
```bash
py -c "import json,base64;print(json.dumps({'custom_nginx_configuration': base64.b64encode(open('nginx.conf','rb').read()).decode()}))" > patch.json
curl -X PATCH -H "Authorization: Bearer $COOLIFY_API_TOKEN" -H "Content-Type: application/json" --data @patch.json "$COOLIFY_API_URL/api/v1/applications/y7f6p5waot2jz9kvlqwasshh"
curl -X POST -H "Authorization: Bearer $COOLIFY_API_TOKEN" "$COOLIFY_API_URL/api/v1/deploy?uuid=y7f6p5waot2jz9kvlqwasshh&force=true"
```
`patch.json`'u sonra sil (`git` dışı geçici dosya).

- [ ] **Step 4: Canlı doğrulama**

```bash
curl -sI https://sukayipkacaklari.com/rehber/dma-nedir.html | grep -i "^HTTP\|^location"
curl -sI https://sukayipkacaklari.com/en/rehber/ | grep -i "^HTTP\|^location"
curl -sI https://sukayipkacaklari.com/blog/ | grep -i "^HTTP"
curl -sI https://sukayipkacaklari.com/blog/debi-olcumu-nedir.html | grep -i "^HTTP"
curl -sI https://sukayipkacaklari.com/en/blog/kacak-onarimi-ve-dogrulama.html | grep -i "^HTTP"
```
Beklenen: ilk iki komut `301` + `location:` `/blog/...`; sonraki üçü `200`.

- [ ] **Step 5: GSC + kapanış**

- Google Search Console → sitemap yeniden gönder (`sitemap.xml`), birkaç yeni `/blog/` URL'sini "Dizine eklenmesini iste".
- `PROJECT.md` §10'a not: eski `/rehber/` GSC kayıtları 301 ile `/blog/`'a taşınacak.
- Kullanıcıya özet: 12 makale (`/blog/`), 8 yeni, TR+EN; eski yollar 301.

---

## Self-Review Notları

- **Spec §2.1 (URL/dizin taşıma):** Task 3. **§2.2 (etiket):** Task 3 Step 2–4. **§2.3 (301):** Task 3 Step 5–6 + Task 13 Step 3. **§2.4 (llms/sitemap/PROJECT):** Task 3 Step 7–8 + Task 5–12 Step 3.
- **Spec §3 (8 makale):** Task 5–12, her biri metadata + `<h2>` brief + iç link + "kaçın" listesiyle.
- **Spec §4.1 (görselli kart):** Task 2 + Task 4 Step 3. **§4.2 (makale hero):** Task 4 Step 1–2, 5. **§4.3 (kürasyon + onay kapısı):** Task 1.
- **Spec §5 (jeneratör zinciri):** her task'ın doğrulama step'i + Task 13.
- **Spec §6 (validate/linkcheck):** Task 3 Step 10, Task 4 Step 6, Task 5–12 Step 4, Task 13 Step 1.
- **Spec §7 riskleri:** sitemap tek kaynak = `gen_projects.py` (Task 3 Step 3 doğrular); #3/#4 ayrımı Task 7/8 brief'lerinde çapraz link ile; nginx PATCH atlanması Task 13 Step 3 zorunlu adım.
- **Tip tutarlılığı:** `BLOG_INDEX_ITEMS` 6'lı tuple (`slug, tr_title, tr_desc, en_title, en_desc, hero`) — Task 4 Step 3 tanımlar, Task 5–12 Step 2 kullanır. `article_schema(..., image=None, date="2026-09-04")` — Task 4 Step 1 tanımlar, Task 4 Step 2 + jeneratör kullanır. `ARTICLES` dict alan seti Task 4 Interfaces'te sabit.
