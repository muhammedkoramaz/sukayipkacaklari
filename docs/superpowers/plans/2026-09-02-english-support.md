# Tam İngilizce Desteği — Uygulama Planı

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Türkçe statik siteye, `/en/` alt ağacında tam paritede İngilizce sürüm eklemek; ziyaretçi tarayıcı diline göre ilk açılışta doğru dile yönlendirilsin.

**Architecture:** El ile yazılan 10 sayfanın `/en/` altında İngilizce kopyaları oluşturulur; jeneratörle üretilen 17 sayfa için `tools/gen_projects.py` ve `tools/gen_rehber.py` iki dilli hale getirilir (tek kaynak, `for lang in ("tr","en")` döngüsü) ve `sitemap.xml` hreflang çiftleriyle yeniden yazılır. Her sayfaya karşılıklı `hreflang` üçlüsü, header/footer dil değiştirici ve `<head>` içinde küçük senkron bir açılış script'i eklenir. Bu repoda "test" = `tools/validate_all.py` + `tools/linkcheck.py` araç zinciri; `validate_all.py` hreflang/lang kontrolleriyle genişletilir ve önce kırmızıya döner (failing check), sayfalar eklendikçe yeşile döner.

**Tech Stack:** El yazımı HTML + CSS + vanilla JS, build yok. Python 3.10 jeneratör/validator scriptleri (`py`, `PYTHONUTF8=1`). Deploy: Coolify static buildpack + nginx. GA4 `G-ETN61F721R`.

**Spec:** `docs/superpowers/specs/2026-09-02-english-support-design.md`

## Global Constraints

- **İçerik kuralları (`PROJECT.md` §7) — İngilizce metinlere de birebir uygulanır:** cihaz/marka adı yok (Keller, SEBA, Sitelab, Aktek… hiçbiri — jenerik yaz: "pressure data logger", "portable ultrasonic flow meter"); ana sayfada şehir adı yok ("At a municipality…"); "anında onarılan / onarım bekleyen" ifadeleri hiçbir proje sayfasında geçmez; kurumsal müşteri yorumu / referans metni yok (yerine proje fotoğrafları); header'da "site survey request" / "keşif" butonu yok — CTA'lar "consultation / remote video call" çerçevesinde; header'da gerçek logo (`logo.svg`); Batman/Kütahya vurgusu = toplam taranan km + toplam bulunan arıza; bölgesel/Kayseri konumlandırması yok, `areaServed` = yalnızca Türkiye (Turkey); ev/bina/konut içi kaçak tespiti yok — kapsam yalnızca belediye (municipal) + sanayi (industrial/OIZ) dağıtım şebekeleri; terim "project", "case" değil.
- **Kanonik host:** `https://sukayipkacaklari.com` (non-www). Türkçe kök kanonik; `x-default` her sayfada Türkçe URL'ye işaret eder.
- **Slug'lar çevrilmez:** EN yol = `"/en" + TR yol`. `/en/hizmetler.html`, `/en/projeler/batman.html` vb. `/` ↔ `/en/`.
- **Tema:** yalnızca açık (light). Marka mavisi `#2563eb`. Yeni font/woff2 yok (latin + latin-ext İngilizceyi kapsar).
- **Meta açıklama ≤ 160 karakter** (Grup G1); `meta description` + `og:description` + `twitter:description` senkron.
- **GA snippet'i değişmez:** `G-ETN61F721R`, `requestIdleCallback` ile boşta yüklenir. `validate_all.py` her HTML'de `googletagmanager.com"` + `G-ETN61F721R` arar.
- **JSON-LD `@id` çıpaları aynı kalır** iki dilde (`.../#org`, `.../#site`, `.../#hasan-koramaz`, `.../#muhammed-koramaz`). EN sayfalarda yalnızca `inLanguage` → `en-US` ve görünen metin alanları (`name`, `headline`, `description`, `text`, breadcrumb `name`, `knowsAbout`) çevrilir; `address`/`telephone`/`email`/`areaServed`/`foundingLocation` değişmez.
- **`tesekkurler` ve `404`:** `noindex` kalır, **hreflang eklenmez**; `<html lang>` yine doğru dile ayarlanır; açılış script'i bu sayfalarda no-op (hreflang yoksa erken `return`).
- **Şablon eşitliği:** aşağıdaki A–H referans string'leri 10 el sayfası + 2 jeneratör şablonunda **birebir aynı** olacak. Değişiklik olursa hepsi güncellenir (`PROJECT.md` §6).
- **Her task sonunda araç zinciri yeşil olacak** (aksi belirtilmedikçe): `PYTHONUTF8=1 py tools/validate_all.py` ve `PYTHONUTF8=1 py tools/linkcheck.py`. CSS/JS değiştiyse önce `PYTHONUTF8=1 py tools/minify.py`. Jeneratör değiştiyse önce `PYTHONUTF8=1 py tools/gen_projects.py && PYTHONUTF8=1 py tools/gen_rehber.py && PYTHONUTF8=1 py tools/add_img_dims.py`.
- **Commit dili:** Türkçe konu satırı. Her commit sonuna:
  ```
  Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
  Claude-Session: https://claude.ai/code/session_01Swkc2UwjdvFSjCZANasFuE
  ```

---

## Referans string'ler (A–H)

Bu bölüm normatiftir. `{...}` yer tutucuları her sayfada somut değerlerle doldurulur. Boşluk/girinti dahil aynen kullanılacak.

### A. `<head>` — hreflang üçlüsü (canonical'dan hemen sonra)

```html
<link rel="alternate" hreflang="tr" href="{TR_URL}">
<link rel="alternate" hreflang="en" href="{EN_URL}">
<link rel="alternate" hreflang="x-default" href="{TR_URL}">
```

`{TR_URL}` / `{EN_URL}` = tam mutlak URL. Ana sayfa: `https://sukayipkacaklari.com/` ve `https://sukayipkacaklari.com/en/`. Diğer: `https://sukayipkacaklari.com/<yol>` ve `https://sukayipkacaklari.com/en/<yol>`. Dizin sayfaları (`projeler/`, `rehber/`) sonda `/` ile.

### B. `<head>` — og:locale çifti (mevcut tek `og:locale` satırının yerine)

TR sayfa:
```html
<meta property="og:locale" content="tr_TR">
<meta property="og:locale:alternate" content="en_US">
```
EN sayfa:
```html
<meta property="og:locale" content="en_US">
<meta property="og:locale:alternate" content="tr_TR">
```

### C. `<html>` etiketi

- TR sayfa: `<html lang="tr">` — ana sayfa (`/`): `<html lang="tr" data-home="1">`
- EN sayfa: `<html lang="en">` — ana sayfa (`/en/`): `<html lang="en" data-home="1">`

### D. `<head>` — açılış (dil algılama) script'i

Konum: hreflang `<link>`'lerinden **sonra**, `<link rel="stylesheet">`'lerden **önce**. Aynen:

```html
<script>
(function(){try{
  var d=document.documentElement,cur=d.lang==='en'?'en':'tr';
  var alt=document.querySelector('link[rel="alternate"][hreflang="'+(cur==='en'?'tr':'en')+'"]');
  if(!alt)return;
  var other=alt.getAttribute('href');
  if(sessionStorage.getItem('le-lang-redirected'))return;
  var pref=null;try{pref=localStorage.getItem('le-lang');}catch(e){}
  if(pref==='tr'||pref==='en'){
    if(pref!==cur){sessionStorage.setItem('le-lang-redirected','1');location.replace(other);}
    return;
  }
  if(d.getAttribute('data-home')!=='1')return;
  var langs=navigator.languages||[navigator.language||''];
  var wantsTr=langs.some(function(l){return /^tr\b/i.test(l);});
  if(!wantsTr&&cur==='tr'){sessionStorage.setItem('le-lang-redirected','1');location.replace(other);}
  else if(wantsTr&&cur==='en'){sessionStorage.setItem('le-lang-redirected','1');location.replace(other);}
}catch(e){}})();
</script>
```

### E. Header dil değiştirici (nav içinde, son `<a>`'dan sonra)

`<nav class="nav" id="navmenu" ...>` içinde, son menü bağlantısından sonra:

```html
      <span class="nav__lang" role="group" aria-label="Language / Dil">
        <a href="{TR_URL}" hreflang="tr" lang="tr"{TR_ACTIVE}>TR</a>
        <span class="nav__lang-sep" aria-hidden="true">|</span>
        <a href="{EN_URL}" hreflang="en" lang="en"{EN_ACTIVE}>EN</a>
      </span>
```

- `{TR_URL}` / `{EN_URL}` burada **kök-göreli yol**: ana sayfa `/` ve `/en/`; diğer `/<yol>` ve `/en/<yol>`.
- Bulunulan dilin `<a>`'sına `{..._ACTIVE}` = ` aria-current="true" class="is-active"`; diğerine boş string.

### F. Footer dil değiştirici (`.ftr__bottom` içinde, mevcut iki `<span>` arasına)

```html
      <span class="ftr__lang">
        <a href="{TR_URL}" hreflang="tr" lang="tr">Türkçe</a>
        <span aria-hidden="true">·</span>
        <a href="{EN_URL}" hreflang="en" lang="en">English</a>
      </span>
```

Kök-göreli yollar (E ile aynı).

### G. `assets/js/site.js` — eklenecek blok (IIFE içinde, "reveal on scroll" `return`'ünden **önce**)

```js
  /* language switcher — remember explicit choice */
  var langLinks = document.querySelectorAll('.nav__lang a, .ftr__lang a');
  Array.prototype.forEach.call(langLinks, function (a) {
    a.addEventListener('click', function () {
      try { localStorage.setItem('le-lang', a.getAttribute('lang') === 'en' ? 'en' : 'tr'); } catch (e) {}
    });
  });
```

### H. `assets/css/site.css` — eklenecek kural (dosya sonuna, mevcut token'larla)

```css
/* dil değiştirici */
.nav__lang { display: inline-flex; align-items: center; gap: .45rem; margin-left: 6px;
  font-family: var(--f-mono); font-size: .8rem; font-weight: 500; }
.nav__lang a { color: var(--ink-2); text-decoration: none; padding: 4px 4px; border-radius: var(--radius-sm); }
.nav__lang a:hover { color: var(--ink); background: var(--bg-2); }
.nav__lang a.is-active { color: var(--brand-ink); font-weight: 700; }
.nav__lang-sep { color: var(--line-strong); }
.ftr__lang { display: inline-flex; align-items: center; gap: .4rem; }
.ftr__lang a { color: inherit; text-decoration: underline; text-underline-offset: 2px; }
@media (max-width: 980px) {
  .nav--open .nav__lang { margin: 6px 0 0; padding-top: 12px; border-top: 1px solid var(--line);
    width: 100%; font-size: 1rem; }
}
```

> `--f-mono` token adı `assets/css/site.css` `:root`'ta doğrulanacak (muhtemelen `--f-mono` veya `--f-data`); farklıysa gerçek adı kullan.

---

## Dosya yapısı

**Yeni (el ile) — `/en/` kök sayfalar:**
- `en/index.html`, `en/platform.html`, `en/hizmetler.html`, `en/hakkimizda.html`, `en/referanslar.html`, `en/iletisim.html`, `en/sss.html`, `en/gizlilik.html`, `en/tesekkurler.html`, `en/404.html`

**Yeni (jeneratör üretir) — çalıştırınca oluşur, elle düzenlenmez:**
- `en/projeler/index.html`, `en/projeler/<slug>.html` ×11
- `en/rehber/index.html`, `en/rehber/<slug>.html` ×4

**Değişecek:**
- `assets/css/site.css` (+`site.min.css`) — H bloğu
- `assets/js/site.js` (+`site.min.js`) — G bloğu
- `tools/gen_projects.py` — iki dilli döngü + `UI` sözlüğü + `P` listesine `*_en` alanları + iki dilli `sitemap.xml`
- `tools/gen_rehber.py` — iki dilli döngü + `UI` sözlüğü + `ARTICLES` listesine `*_en` alanları
- `tools/validate_all.py` — hreflang üçlüsü + `<html lang>` + `inLanguage` kontrolleri
- 10 mevcut TR kök sayfa (`index.html`, `platform.html`, `hizmetler.html`, `hakkimizda.html`, `referanslar.html`, `iletisim.html`, `sss.html`, `gizlilik.html`, `tesekkurler.html`, `404.html`) — A/B/C/D/E/F blokları
- `nginx.conf` — `/en/` location bloğu
- `llms.txt` — İngilizce satır + `/en/` bağlantısı
- `sitemap.xml` — jeneratör yeniden yazar (elle düzenlenmez)
- `PROJECT.md` — §5 (yeni URL'ler), §6 (jeneratör notu), §8 (yapılan iş kaydı)

**Not:** `tools/add_img_dims.py`, `tools/linkcheck.py` `**/*.html` tarar → `/en/` otomatik kapsanır, kod değişmez.

---

## Faz 0 — Doğrulayıcı önce (failing check)

### Task 1: `validate_all.py`'ye hreflang + lang kontrolleri

**Files:**
- Modify: `tools/validate_all.py`

**Interfaces:**
- Produces: genişletilmiş `validate_all.py`; indekslenebilir her HTML için `hreflang tr/en/x-default` üçlüsü + hedef dosyanın diskte çözülmesi + `<html lang>` ağaç-tutarlılığı + JSON-LD `inLanguage` tutarlılığı kontrol edilir. `noindex` sayfalar (`tesekkurler`, `404`) hreflang kontrolünden muaf.

- [ ] **Step 1: Kontrol fonksiyonunu ekle**

`tools/validate_all.py` içinde, `files=sorted(...)` satırından sonra, ana döngüye şu kontrolleri ekle (mevcut `issues`/`print` desenine uy):

```python
def resolve_href(h):
    h = h.split('#')[0].split('?')[0]
    if h.startswith('http'):
        h = h.split('sukayipkacaklari.com', 1)[-1] if 'sukayipkacaklari.com' in h else h
    if h in ('', '/'):
        return True
    p = h.lstrip('/')
    if p.endswith('/'):
        p += 'index.html'
    return os.path.isfile(p) or os.path.isfile(p + '.html')

# ana döngü içinde, her f/s için:
noindex = 'name="robots" content="noindex' in s.replace(' ', '').replace('"robots"content=', '"robots" content=') \
          or 'noindex' in (re.search(r'<meta name="robots"[^>]*>', s) or type('', (), {'group': lambda self: ''})()).group()
is_en = f.startswith('en' + os.sep) or f.startswith('en/')
want_lang = 'en' if is_en else 'tr'
mhtml = re.search(r'<html[^>]*\blang="([^"]+)"', s)
lang_ok = bool(mhtml) and mhtml.group(1) == want_lang
href = dict(re.findall(r'<link rel="alternate" hreflang="([^"]+)" href="([^"]+)"', s))
hreflang_ok = noindex or (
    {'tr', 'en', 'x-default'} <= set(href)
    and all(resolve_href(href[k]) for k in ('tr', 'en', 'x-default'))
)
ld_lang_ok = True
for b in jblocks:
    for m in re.finditer(r'"inLanguage"\s*:\s*"([^"]+)"', b):
        if not m.group(1).lower().startswith(want_lang):
            ld_lang_ok = False
```

`if left or p.err or ...` koşuluna `or not lang_ok or not hreflang_ok or not ld_lang_ok` ekle ve ilgili `print` satırlarını ekle:

```python
        if not lang_ok: print(f'   <html lang> beklenen "{want_lang}", bulunan {mhtml.group(1) if mhtml else "yok"}')
        if not hreflang_ok: print('   hreflang tr/en/x-default üçlüsü eksik veya hedefi çözülemiyor:', dict(href))
        if not ld_lang_ok: print(f'   JSON-LD inLanguage sayfa diliyle ({want_lang}) uyumsuz')
```

- [ ] **Step 2: Çalıştır — kırmızıya dönmeli**

Run: `PYTHONUTF8=1 py tools/validate_all.py`
Expected: mevcut 27 TR sayfanın çoğu `✗` — sebep "hreflang tr/en/x-default üçlüsü eksik" (henüz `en` alternatifi yok). `tesekkurler.html` / `404.html` bu kontrolde temiz kalmalı (noindex muafiyeti). Bu beklenen "failing test".

- [ ] **Step 3: Commit**

```bash
git add tools/validate_all.py
git commit -m "Doğrulayıcı: hreflang üçlüsü + <html lang> + inLanguage kontrolleri"
```

---

## Faz 1 — Ortak altyapı

### Task 2: CSS + JS — dil değiştirici stilleri ve tıklama hafızası

**Files:**
- Modify: `assets/css/site.css` (H bloğu, dosya sonu), `assets/js/site.js` (G bloğu)
- Regenerate: `assets/css/site.min.css`, `assets/js/site.min.js`

**Interfaces:**
- Produces: `.nav__lang`, `.nav__lang-sep`, `.ftr__lang` sınıf stilleri; `.nav__lang a, .ftr__lang a` tıklanınca `localStorage['le-lang']` yazan JS. Sonraki task'lar bu sınıfları kullanır.

- [ ] **Step 1: `:root` token adını doğrula**

Run: `PYTHONUTF8=1 py -c "import re;print([l for l in open('assets/css/site.css',encoding='utf-8').read().splitlines() if '--f-' in l])"`
Beklenen: mono/veri fontu token adı (ör. `--f-mono`). H bloğundaki `var(--f-mono)`'yu gerçek adla değiştir.

- [ ] **Step 2: H bloğunu `site.css` sonuna ekle** (yukarıdaki referans H, token adı düzeltilmiş).

- [ ] **Step 3: G bloğunu `site.js`'e ekle** — IIFE içinde `/* reveal on scroll */` yorumundan **önce**, referans G aynen.

- [ ] **Step 4: Minify**

Run: `PYTHONUTF8=1 py tools/minify.py`
Expected: `site.min.css` ve `site.min.js` güncellendi, hata yok.

- [ ] **Step 5: Araç zinciri**

Run: `PYTHONUTF8=1 py tools/validate_all.py` (Task 1'deki aynı hreflang hataları — yeni hata yok), `PYTHONUTF8=1 py tools/linkcheck.py` (0 broken).

- [ ] **Step 6: Commit**

```bash
git add assets/css/site.css assets/css/site.min.css assets/js/site.js assets/js/site.min.js
git commit -m "Dil değiştirici: CSS stilleri + seçimi hatırlayan JS"
```

### Task 3: TR kök sayfalara A/B/C/D/E/F bloklarını uygula (10 dosya)

**Files:**
- Modify: `index.html`, `platform.html`, `hizmetler.html`, `hakkimizda.html`, `referanslar.html`, `iletisim.html`, `sss.html`, `gizlilik.html`, `tesekkurler.html`, `404.html`

**Interfaces:**
- Consumes: referans A–F, Task 2 CSS/JS sınıfları.
- Produces: 10 TR sayfa artık `hreflang en` alternatifi, `og:locale:alternate`, açılış script'i ve TR|EN değiştirici içerir. `index.html` `<html lang="tr" data-home="1">`.

- [ ] **Step 1: Her dosyada `<head>` düzenle**
  - `<link rel="alternate" hreflang="tr" ...>` ve `<link rel="alternate" hreflang="x-default" ...>` satırlarını referans A üçlüsüyle değiştir (aralarına `hreflang="en"` eklenir). `{TR_URL}`/`{EN_URL}` bu sayfaya özgü (bkz. Global Constraints URL tablosu).
  - Tek `<meta property="og:locale" content="tr_TR">` satırını referans B (TR) çiftiyle değiştir.
  - hreflang satırlarından sonra, `<link rel="stylesheet">`'ten önce referans D script'ini ekle.

- [ ] **Step 2: `<html>` etiketi** — `index.html`: `<html lang="tr" data-home="1">`. Diğer 9: `<html lang="tr">` (zaten öyle; dokunma).

- [ ] **Step 3: Header değiştirici** — her dosyada `<nav class="nav" id="navmenu">` içinde son `<a>`'dan sonra referans E. Bulunulan sayfa TR olduğu için `{TR_ACTIVE}` = ` aria-current="true" class="is-active"`, `{EN_ACTIVE}` = boş. `{TR_URL}`/`{EN_URL}` kök-göreli.
  - `tesekkurler.html` ve `404.html`'de header yoksa bu adımı ve footer adımını atla; yalnızca `<html lang>` + D script (D, hreflang bulamayınca no-op — yine de ekle) + not: bu iki sayfada A/B **eklenmez** (noindex).

- [ ] **Step 4: Footer değiştirici** — `.ftr__bottom` içindeki iki `<span>` arasına referans F.

- [ ] **Step 5: Araç zinciri**

Run: `PYTHONUTF8=1 py tools/validate_all.py`
Expected: 10 TR kök sayfa artık bu kontrolde temiz **ama** hedefteki `en/...` dosyaları henüz yok → "hedefi çözülemiyor" hatası. Bu beklenen; jeneratör sayfaları (17) hâlâ eski hreflang'le `✗`.
Run: `PYTHONUTF8=1 py tools/linkcheck.py`
Expected: header/footer `href="/en/..."` bağlantıları → **broken links** listelenecek. Bu da beklenen (EN sayfalar Faz 2–4'te gel+). Not düş, devam.

- [ ] **Step 6: Commit**

```bash
git add index.html platform.html hizmetler.html hakkimizda.html referanslar.html iletisim.html sss.html gizlilik.html tesekkurler.html 404.html
git commit -m "TR kök sayfalar: hreflang en + og:locale:alternate + açılış script'i + TR|EN değiştirici"
```

### Task 4: `nginx.conf` + `llms.txt` + EN 404/teşekkürler iskeleti

**Files:**
- Modify: `nginx.conf`, `llms.txt`
- Create: `en/404.html`, `en/tesekkurler.html`

**Interfaces:**
- Consumes: TR `404.html` / `tesekkurler.html` yapısı, referans C/D.
- Produces: `/en/` için nginx location + İngilizce 404; `en/404.html`, `en/tesekkurler.html` (`noindex`, hreflang yok).

- [ ] **Step 1: `nginx.conf` — `location / ` bloğundan önce** referans spec §8'deki `location ^~ /en/ { ... try_files $uri $uri/ $uri.html /en/404.html; }` bloğunu ekle; dosyadaki mevcut `error_page 404 /404.html;` satırını `location ^~ /en/` sonrasında bırak (kök için Türkçe 404).

- [ ] **Step 2: `en/404.html`** — TR `404.html`'in yapısal kopyası: `<html lang="en">`, tüm görünen metin İngilizce ("Page not found", geri dön linki `/en/`), `<meta name="robots" content="noindex">` korunur, GA snippet korunur, referans D script eklenir (no-op), hreflang **yok**. Header/footer varsa referans E/F (`{EN_ACTIVE}` EN'de).

- [ ] **Step 3: `en/tesekkurler.html`** — TR `tesekkurler.html` yapısal kopyası: `<html lang="en">`, İngilizce teşekkür metni, `noindex` korunur, GA korunur, D script eklenir, hreflang yok.

- [ ] **Step 4: `llms.txt`** — sonuna İngilizce özet satırı + `https://sukayipkacaklari.com/en/` bağlantısı ekle (mevcut biçime uygun, kısa).

- [ ] **Step 5: Araç zinciri**

Run: `PYTHONUTF8=1 py tools/validate_all.py` (yeni 2 EN sayfa noindex → temiz; genel durum değişmedi), `PYTHONUTF8=1 py tools/linkcheck.py` (broken link sayısı Task 3'ten azaldı: `/en/` 404/teşekkürler artık var).

- [ ] **Step 6: Commit**

```bash
git add nginx.conf llms.txt en/404.html en/tesekkurler.html
git commit -m "Altyapı: /en/ nginx location + İngilizce 404/teşekkürler + llms.txt"
```

---

## Faz 2 — Jeneratör refaktörü

### Task 5: `gen_rehber.py` — iki dilli iskelet (içerik hariç)

**Files:**
- Modify: `tools/gen_rehber.py`

**Interfaces:**
- Produces: `head(...)`, `nav(active, lang)`, `footer(lang)` (veya `FOOTER` → fonksiyon), ana yazım döngüsü `for lang in ("tr","en")`. `UI = {"tr": {...}, "en": {...}}` sözlüğü: `skip` ("İçeriğe geç"/"Skip to content"), `menu` (8 etiket), `footer_h` (footer başlıkları + linkleri), `crumb_home` ("Ana Sayfa"/"Home"), CTA metinleri. EN çıktısı `SITE/en/rehber/...`, URL tabanı `BASE + "/en"`.
- Consumes: referans A/B/C/D/E/F.

- [ ] **Step 1: `UI` sözlüğünü ekle** — script başına, `NAV_ITEMS` yerine:

```python
UI = {
  "tr": {
    "menu": [("/", "Ana Sayfa"), ("/platform.html", "Platform"), ("/hizmetler.html", "Hizmetler"),
             ("/rehber/", "Rehber"), ("/projeler/", "Projeler"), ("/referanslar.html", "Referanslar"),
             ("/hakkimizda.html", "Hakkımızda"), ("/iletisim.html", "İletişim")],
    "skip": "İçeriğe geç", "crumb_home": "Ana Sayfa",
    "menu_aria": "Ana menü", "burger_aria": "Menüyü aç",
  },
  "en": {
    "menu": [("/", "Home"), ("/platform.html", "Platform"), ("/hizmetler.html", "Services"),
             ("/rehber/", "Guide"), ("/projeler/", "Projects"), ("/referanslar.html", "References"),
             ("/hakkimizda.html", "About"), ("/iletisim.html", "Contact")],
    "skip": "Skip to content", "crumb_home": "Home",
    "menu_aria": "Main menu", "burger_aria": "Open menu",
  },
}
def prefix(lang): return "" if lang == "tr" else "/en"
def out_dir(lang): return SITE if lang == "tr" else os.path.join(SITE, "en")
```

- [ ] **Step 2: `nav(active, lang)`** — `UI[lang]["menu"]` üzerinde döner; her `href` `prefix(lang) + href` (kök `/` için `prefix(lang) + "/"`); `active` karşılaştırması prefiksli yola göre; referans E dil değiştirici bloğunu sona ekler (`{TR_URL}` = `href`, `{EN_URL}` = `"/en" + href`; aktif olan `lang`e göre `is-active`).

- [ ] **Step 3: `head(...)`** — `lang` parametresi al: `<html lang="{lang}">` (rehber sayfalarında `data-home` yok), referans A üçlüsü (`canonical` = `BASE+prefix+yol`, TR/EN mutlak URL'ler), referans B çifti (`lang`e göre), referans D script (stylesheet'ten önce), `og:locale`. Font preload prefix'i kök-mutlak kalır (`/assets/...`).

- [ ] **Step 4: `FOOTER` → `footer(lang)`** — footer link href'leri `prefix(lang)` ile; başlıklar/metinler `UI[lang]` (bu task'ta TR string'leri kopyala, EN'i "TODO" değil gerçek çeviriyle doldur: "Platform"/"Corporate"/"Contact" başlıkları, alt linkler). `.ftr__bottom`'a referans F. `© 2026 LeakExpert · Tüm hakları saklıdır.` → EN: `© 2026 LeakExpert · All rights reserved.`

- [ ] **Step 5: Ana döngü** — dosya yazımını `for lang in ("tr", "en"):` içine al; `os.makedirs(os.path.join(out_dir(lang), "rehber"), exist_ok=True)`; çıktıları `out_dir(lang)` altına yaz. Bu task'ta makale gövdeleri hâlâ TR (içerik Task 6'da) — EN çıktısı geçici olarak TR gövde + EN çerçeve üretebilir; **ama** commit'te bunu yapma: bu task yalnızca `rehber/index.html` (hub) + TR makaleleri değişmeden üretmeli, EN döngüsü kod olarak hazır ama `ARTICLES` EN alanları gelene kadar EN makale yazımı `continue` ile atlanır. Hub'ın EN'i (`en/rehber/index.html`) bu task'ta üretilir (kısa, çevrilir).

- [ ] **Step 6: Üret + doğrula**

Run: `PYTHONUTF8=1 py tools/gen_rehber.py`
Expected: `rehber/index.html` + 4 TR makale değişmeden (git diff minimal: yalnızca hreflang/script/switcher eklentileri), `en/rehber/index.html` yeni.
Run: `PYTHONUTF8=1 py tools/add_img_dims.py && PYTHONUTF8=1 py tools/validate_all.py`
Expected: `rehber/*` TR sayfalar hâlâ "en hedefi çözülemiyor" (EN makaleler yok) — Task 6'da kapanır. `en/rehber/index.html` temiz.

- [ ] **Step 7: Commit**

```bash
git add tools/gen_rehber.py rehber/ en/rehber/
git commit -m "gen_rehber: iki dilli iskelet (UI sözlüğü, lang'li head/nav/footer, en/ döngüsü)"
```

### Task 6: `gen_rehber.py` — 4 makalenin İngilizce içeriği

**Files:**
- Modify: `tools/gen_rehber.py` (`ARTICLES` listesi + EN yazım kolu)

**Interfaces:**
- Consumes: Task 5 iskeleti.
- Produces: `ARTICLES` her ögesine `title_en`, `desc_en`, `body_en` (HTML string, TR `body` ile aynı yapı), gerekiyorsa `headline_en`. EN döngüsü artık makale yazar → `en/rehber/<slug>.html` ×4. JSON-LD `Article` `inLanguage="en-US"`, `headline`/`description` EN; `@id` çıpaları korunur; `datePublished` aynı.

- [ ] **Step 1:** `ARTICLES` listesindeki 4 makale için `*_en` alanlarını ekle. Çeviri kuralları: `PROJECT.md` §7; teknik terimler doğru İngilizce karşılığı ("acoustic leak detection", "district metered area (DMA)", "non-revenue water (NRW)", "minimum night flow", "step test", "zero-pressure test"); sayı biçimi İngilizce (ondalık `.`). Slug'lar Türkçe kalır.

- [ ] **Step 2:** EN döngüsündeki `continue` kaldır; makale gövdesi `body_en`, başlık `title_en`, meta `desc_en`, breadcrumb `UI["en"]["crumb_home"]` + "Guide".

- [ ] **Step 3: Üret + doğrula**

Run: `PYTHONUTF8=1 py tools/gen_rehber.py && PYTHONUTF8=1 py tools/add_img_dims.py && PYTHONUTF8=1 py tools/validate_all.py`
Expected: `rehber/*` TR **ve** `en/rehber/*` EN sayfalar bu kontrolde temiz (karşılıklı hreflang çözülüyor). `linkcheck` `/en/rehber/` linkleri artık kırık değil.

- [ ] **Step 4: Gözle kontrol** — `en/rehber/dma-nedir.html` tarayıcıda/okuyarak: yapı TR ile aynı mı, §7 ihlali var mı, JSON-LD `inLanguage` `en-US` mi.

- [ ] **Step 5: Commit**

```bash
git add tools/gen_rehber.py en/rehber/
git commit -m "gen_rehber: 4 rehber makalesinin İngilizce içeriği (en/rehber/)"
```

### Task 7: `gen_projects.py` — iki dilli iskelet + iki dilli sitemap

**Files:**
- Modify: `tools/gen_projects.py`

**Interfaces:**
- Consumes: referans A–F, Task 5'teki `UI` deseni (aynısını buraya kopyala — iki script paralel, `PROJECT.md` §6).
- Produces: `header(current, lang)`, `page_head(title, desc, canon, ogtype, extra_ld, lang, tr_url, en_url, is_home=False)`, `footer(lang)`; ana döngü `for lang in ("tr","en")`; `projeler/index.html` + `en/projeler/index.html`. **`sitemap.xml`**: `<urlset>`'e `xmlns:xhtml="http://www.w3.org/1999/xhtml"`; `u(...)` yardımcı fonksiyonu her sayfayı TR+EN iki `<url>` olarak yazar, her birine 3 `<xhtml:link rel="alternate" hreflang="tr|en|x-default" href="...">`. `tesekkurler`/`404` sitemap'e girmez.

- [ ] **Step 1:** `UI` sözlüğü + `prefix`/`out_dir` helper'larını `gen_projects.py`'ye ekle (Task 5 ile birebir aynı içerik; `menu`'ye `crumb` ihtiyaçları için `projeler`/`Projects` zaten var).

- [ ] **Step 2:** `header(current)` → `header(current, lang)`: nav `UI[lang]["menu"]`, href'ler `prefix(lang)`; referans E bloğu; `brand` `aria-label` `lang`e göre ("LeakExpert ana sayfa"/"LeakExpert home"); `href="/"` → `prefix(lang)+"/"`; `burger`/`nav` aria `UI[lang]`.

- [ ] **Step 3:** `page_head(...)` → `lang`, `tr_url`, `en_url`, `is_home` parametreleri; `<html lang="{lang}"{ ' data-home="1"' if is_home else ''}>`; referans A (mutlak `tr_url`/`en_url`), B, D; `<a class="skip">` metni `UI[lang]["skip"]`.

- [ ] **Step 4:** `FOOTER` → `footer(lang)` (Task 5 Step 4 ile aynı kurallar).

- [ ] **Step 5:** Ana döngü `for lang in ("tr","en")`: `projeler/index.html` her iki dilde üretilir (index metni bu task'ta çevrilir — kısa); proje **detay** sayfaları bu task'ta yalnızca TR (`if lang=="en": continue` detay kolunda) — içerik Task 8'de. `os.makedirs(os.path.join(out_dir(lang),"projeler"), exist_ok=True)`.

- [ ] **Step 6: `sitemap.xml` iki dilli** — `u()` fonksiyonunu değiştir:

```python
sm = ['<?xml version="1.0" encoding="UTF-8"?>',
      '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
      'xmlns:image="http://www.google.com/schemas/sitemap-image/1.1" '
      'xmlns:xhtml="http://www.w3.org/1999/xhtml">']
def u(path, cf, pr, imgs=None):
    # path: kök-göreli, "/" veya "/x.html" veya "/dir/"
    tr = f"{BASE}{path}"
    en = f"{BASE}/en{path if path != '/' else '/'}"
    for loc in (tr, en):
        sm.append(f'  <url><loc>{loc}</loc><lastmod>{LM}</lastmod><changefreq>{cf}</changefreq><priority>{pr}</priority>')
        sm.append(f'    <xhtml:link rel="alternate" hreflang="tr" href="{tr}"/>')
        sm.append(f'    <xhtml:link rel="alternate" hreflang="en" href="{en}"/>')
        sm.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{tr}"/>')
        for im in (imgs or []):
            sm.append(f'    <image:image><image:loc>{BASE}{im}</image:loc></image:image>')
        sm.append('  </url>')
```

Mevcut `u(f"{BASE}/", ...)` çağrılarını `u("/", ...)`, `u(f"{BASE}/platform.html", ...)` → `u("/platform.html", ...)` vb. kök-göreli path'e çevir.

- [ ] **Step 7: Üret + doğrula**

Run: `PYTHONUTF8=1 py tools/gen_projects.py && PYTHONUTF8=1 py tools/gen_rehber.py && PYTHONUTF8=1 py tools/add_img_dims.py`
Run: `PYTHONUTF8=1 py -c "import xml.dom.minidom,pathlib;xml.dom.minidom.parseString(pathlib.Path('sitemap.xml').read_text(encoding='utf-8'));print('sitemap OK')"`
Run: `PYTHONUTF8=1 py tools/validate_all.py`
Expected: `projeler/index.html` + `en/projeler/index.html` temiz; proje detay TR sayfaları hâlâ "en hedefi çözülemiyor" (Task 8'de kapanır).

- [ ] **Step 8: Commit**

```bash
git add tools/gen_projects.py projeler/ en/projeler/ sitemap.xml
git commit -m "gen_projects: iki dilli iskelet + hreflang'li iki dilli sitemap.xml"
```

### Task 8: `gen_projects.py` — 11 proje sayfasının İngilizce içeriği

**Files:**
- Modify: `tools/gen_projects.py` (`P` listesi + EN detay kolu)

**Interfaces:**
- Consumes: Task 7 iskeleti.
- Produces: `P` her `dict`e EN alanları: `name_en, kicker_en, h1_en, lede_en, desc_en, spec_en` (etiket listesi; sayı/birim aynı ama birim metni İngilizce: "adet"→"count"/"faults", "arıza/km/yıl"→"faults/km/yr", "km" aynı), `prose_en` (TR `prose` ile aynı `(başlık, [paragraf,...])` yapısı). EN döngüsündeki `continue` kalkar → `en/projeler/<slug>.html` ×11. `Article`/`BreadcrumbList` JSON-LD EN metin + `inLanguage="en-US"`, `@id` korunur, `datePublished`/`image` dizisi aynı.

- [ ] **Step 1:** 11 projenin her biri için `*_en` alanlarını yaz. Çeviri: `PROJECT.md` §7 (özellikle §7.2 marka yok, §7.4 "anında onarılan" yok, §7.8 Batman/Kütahya = toplam km + toplam arıza). Kurum adları: "X Belediyesi" → "Municipality of X" / "X Municipality" (tutarlı seç, hepsinde aynı kalıp). Bölge adları İngilizce ("İç Ege" → "Inner Aegean"). Ondalık ayraç `.`, binlik `,`.

- [ ] **Step 2:** EN detay kolundaki `continue`'yu kaldır; şablon alanlarını `*_en` ile besle.

- [ ] **Step 3: Üret + tam araç zinciri**

Run: `PYTHONUTF8=1 py tools/gen_projects.py && PYTHONUTF8=1 py tools/gen_rehber.py && PYTHONUTF8=1 py tools/add_img_dims.py && PYTHONUTF8=1 py tools/validate_all.py && PYTHONUTF8=1 py tools/linkcheck.py`
Expected: `validate_all.py` — **0 issues** hedeflenir (tüm TR + EN sayfalar hreflang/lang temiz). `linkcheck.py` — **0 broken** (tüm `/en/...` linkleri artık mevcut).

- [ ] **Step 4: Gözle kontrol** — `en/projeler/batman.html` + `en/projeler/kutahya.html`: yapı/rakamlar TR ile aynı mı, §7 ihlali (marka adı, "anında onarılan") var mı, breadcrumb "Home / Projects / …" mı.

- [ ] **Step 5: Commit**

```bash
git add tools/gen_projects.py en/projeler/ sitemap.xml
git commit -m "gen_projects: 11 proje sayfasının İngilizce içeriği (en/projeler/)"
```

---

## Faz 3 — El ile yazılan İngilizce sayfalar

> Ortak yöntem (her sayfa için): TR kaynağı `cp <tr> en/<tr>` ile kopyala, sonra: `<html lang="en">` (index'te `data-home="1"`); `<head>` içinde `<title>`/`meta description`/OG/Twitter başlık+açıklama EN (≤160); referans A (mutlak URL'ler bu sayfaya özgü, `x-default`+`tr` = TR URL, `en` = kendi URL'si); referans B (EN); referans D script; referans C. Header referans E (`{EN_ACTIVE}` EN linkte). Footer referans F. JSON-LD: `inLanguage` `en-US`, görünen metin alanları çevrili, `@id` korunur, `address`/`telephone`/`areaServed` değişmez. **Tüm** görünen gövde metni çevrilir; sınıflar, bölüm sırası, `<img>` src/width/height, GA snippet **değişmez**. §7 kurallarına uy.

### Task 9: `en/index.html`

**Files:**
- Create: `en/index.html` (kaynak: `index.html`)

- [ ] **Step 1:** `index.html`'i `en/index.html`'e kopyala.
- [ ] **Step 2:** Yukarıdaki ortak yöntemi uygula. `<html lang="en" data-home="1">`. hreflang: `tr`/`x-default` = `https://sukayipkacaklari.com/`, `en` = `https://sukayipkacaklari.com/en/`. Header/footer değiştirici kök-göreli `/` ve `/en/`.
- [ ] **Step 3:** Ana sayfa metni: hero, "su kayıp kaçakları" görünür ifadesi TR SEO için ana sayfada kalır → EN ana sayfada karşılığı "water loss & leakage" doğal biçimde; **şehir adı yok** (§7.3). "Bir belediyede…" → "At a municipality…". CTA "Görüşme talebi" → "Request a consultation".
- [ ] **Step 4:** JSON-LD `@graph`: `Organization`+`ProfessionalService` `description` EN, `knowsAbout` EN, `slogan` EN; `WebSite` `inLanguage` `en-US`, `alternateName` EN; `@id`'ler aynı; `founder` Person `jobTitle` EN.
- [ ] **Step 5:** Araç zinciri: `PYTHONUTF8=1 py tools/validate_all.py` (`en/index.html` temiz; `index.html` karşılıklı hreflang artık çözülüyor), `PYTHONUTF8=1 py tools/linkcheck.py`.
- [ ] **Step 6: Commit** — `git add en/index.html && git commit -m "en/index.html: İngilizce ana sayfa"`

### Task 10: `en/platform.html`

**Files:**
- Create: `en/platform.html` (kaynak: `platform.html`)

- [ ] **Step 1:** Kopyala.
- [ ] **Step 2:** Ortak yöntem. hreflang: TR = `/platform.html`, EN = `/en/platform.html`.
- [ ] **Step 3:** Metin: mobil saha uygulaması / web yönetim paneli / API bölümleri EN. `SoftwareApplication` JSON-LD `featureList` EN, `name`/`description` EN, `inLanguage` `en-US`, `@id` korunur.
- [ ] **Step 4:** Araç zinciri (validate + linkcheck) temiz.
- [ ] **Step 5: Commit** — `git add en/platform.html && git commit -m "en/platform.html: İngilizce platform sayfası"`

### Task 11: `en/hizmetler.html`

**Files:**
- Create: `en/hizmetler.html` (kaynak: `hizmetler.html`)

- [ ] **Step 1:** Kopyala.
- [ ] **Step 2:** Ortak yöntem. hreflang: `/hizmetler.html` ↔ `/en/hizmetler.html`. Menüde aktif öge "Services" (`aria-current="page"`).
- [ ] **Step 3:** 4 aşamalı yöntem metni EN; cihazlar jenerik ("pressure data logger", "portable ultrasonic flow meter" — marka yok §7.2); ev/bina içi kaçak ifadesi eklenmez (§7.10). `Service`/`OfferCatalog`/`BreadcrumbList` JSON-LD EN, `inLanguage` `en-US`, `@id` korunur, breadcrumb "Home / Services".
- [ ] **Step 4:** Araç zinciri temiz.
- [ ] **Step 5: Commit** — `git add en/hizmetler.html && git commit -m "en/hizmetler.html: İngilizce hizmetler sayfası"`

### Task 12: `en/hakkimizda.html`

**Files:**
- Create: `en/hakkimizda.html` (kaynak: `hakkimizda.html`)

- [ ] **Step 1:** Kopyala.
- [ ] **Step 2:** Ortak yöntem. hreflang `/hakkimizda.html` ↔ `/en/hakkimizda.html`.
- [ ] **Step 3:** Ekip metni EN; `25+ yıl · kuruluş 2004` → "25+ years · founded 2004". Ofis "Melikgazi / Kayseri" kalır ama bölgesel konumlandırma yok (§7.9). `AboutPage` + 2×`Person` JSON-LD: `@id` (`#hasan-koramaz`, `#muhammed-koramaz`) korunur, `jobTitle`/`description` EN, `inLanguage` `en-US`.
- [ ] **Step 4:** Araç zinciri temiz.
- [ ] **Step 5: Commit** — `git add en/hakkimizda.html && git commit -m "en/hakkimizda.html: İngilizce hakkımızda sayfası"`

### Task 13: `en/referanslar.html`

**Files:**
- Create: `en/referanslar.html` (kaynak: `referanslar.html`)

- [ ] **Step 1:** Kopyala.
- [ ] **Step 2:** Ortak yöntem. hreflang `/referanslar.html` ↔ `/en/referanslar.html`.
- [ ] **Step 3:** Kurum logoları + proje geçmişi metni EN. **Müşteri yorumu eklenmez** (§7.5) — mevcut yapı (logolar + proje listesi) korunur. `BreadcrumbList` EN "Home / References".
- [ ] **Step 4:** Araç zinciri temiz.
- [ ] **Step 5: Commit** — `git add en/referanslar.html && git commit -m "en/referanslar.html: İngilizce referanslar sayfası"`

### Task 14: `en/iletisim.html`

**Files:**
- Create: `en/iletisim.html` (kaynak: `iletisim.html`)

- [ ] **Step 1:** Kopyala.
- [ ] **Step 2:** Ortak yöntem. hreflang `/iletisim.html` ↔ `/en/iletisim.html`.
- [ ] **Step 3:** Form etiketleri/placeholder'ları EN; form `action` **aynı** (`formspree.io/f/BURAYA_FORM_ID` placeholder — değiştirme). Harita embed `src` **aynı**. Adres Melikgazi/Kayseri; telefon/e-posta aynı. Form başarı yönlendirmesi `tesekkurler.html` → `/en/tesekkurler.html` (Formspree `_next` veya redirect alanı varsa `/en/` sürümüne çevir; yoksa dokunma). `LocalBusiness` JSON-LD: `areaServed` = Türkiye/Turkey (§7.9), `@id` korunur, `inLanguage` `en-US`, breadcrumb "Home / Contact".
- [ ] **Step 4:** Araç zinciri temiz.
- [ ] **Step 5: Commit** — `git add en/iletisim.html && git commit -m "en/iletisim.html: İngilizce iletişim sayfası"`

### Task 15: `en/sss.html`

**Files:**
- Create: `en/sss.html` (kaynak: `sss.html`)

- [ ] **Step 1:** Kopyala.
- [ ] **Step 2:** Ortak yöntem. hreflang `/sss.html` ↔ `/en/sss.html`.
- [ ] **Step 3:** 11 soru+cevap EN çeviri; ev/bina içi kaçak ima eden yeni soru **eklenmez** (§7.10). `FAQPage` JSON-LD: her `Question`/`acceptedAnswer` `text` EN, `inLanguage` `en-US`, `@id` korunur, soru sayısı 11.
- [ ] **Step 4:** Araç zinciri temiz (`validate_all.py` `FAQPage` parse'ı geçmeli).
- [ ] **Step 5: Commit** — `git add en/sss.html && git commit -m "en/sss.html: İngilizce SSS sayfası"`

### Task 16: `en/gizlilik.html`

**Files:**
- Create: `en/gizlilik.html` (kaynak: `gizlilik.html`)

- [ ] **Step 1:** Kopyala.
- [ ] **Step 2:** Ortak yöntem. hreflang `/gizlilik.html` ↔ `/en/gizlilik.html`. `<title>` "Privacy Policy | LeakExpert".
- [ ] **Step 3:** Metni EN çevir; yasal dayanak **KVKK (Law No. 6698, Turkey's Personal Data Protection Law)** olarak anlatılır — GDPR'a çevirme. Aynı hak maddeleri, aynı başvuru adresi (`sukayipkacaklari@gmail.com`). `BreadcrumbList` EN.
- [ ] **Step 4:** Araç zinciri temiz.
- [ ] **Step 5: Commit** — `git add en/gizlilik.html && git commit -m "en/gizlilik.html: İngilizce gizlilik politikası"`

---

## Faz 4 — Kapanış

### Task 17: Tam doğrulama + `PROJECT.md` güncellemesi

**Files:**
- Modify: `PROJECT.md`

**Interfaces:**
- Consumes: tüm önceki task'lar.
- Produces: yeşil araç zinciri kanıtı; `PROJECT.md` §5 (yeni ~27 `/en/` URL satırı), §6 (jeneratör iki dilli notu + güncel tipik akış), §8 (yeni satır: "Tam İngilizce desteği — `/en/` alt ağacı").

- [ ] **Step 1: Tam zincir, sıfırdan üret**

Run:
```
PYTHONUTF8=1 py tools/gen_projects.py && PYTHONUTF8=1 py tools/gen_rehber.py && PYTHONUTF8=1 py tools/add_img_dims.py && PYTHONUTF8=1 py tools/minify.py && PYTHONUTF8=1 py tools/validate_all.py && PYTHONUTF8=1 py tools/linkcheck.py
```
Expected: `validate_all.py` → `N files — 0 with issues`. `linkcheck.py` → `broken links: 0`. `git status` — jeneratör çıktısında beklenmeyen diff yok.

- [ ] **Step 2: `sitemap.xml` sağlaması**

Run: `PYTHONUTF8=1 py -c "import pathlib,re;t=pathlib.Path('sitemap.xml').read_text(encoding='utf-8');locs=re.findall(r'<loc>([^<]+)</loc>',t);print(len(locs),'url;',sum('/en/' in l for l in locs),'en');import xml.dom.minidom;xml.dom.minidom.parseString(t);print('xml OK')"`
Expected: TR ve EN url sayıları eşit; `xmlns:xhtml` mevcut; her `<url>` 3 `xhtml:link` içerir; `tesekkurler`/`404` yok.

- [ ] **Step 3: hreflang karşılıklılık örneklemesi** — `index.html` ↔ `en/index.html`, `hizmetler.html` ↔ `en/hizmetler.html`, `rehber/dma-nedir.html` ↔ `en/rehber/dma-nedir.html`, `projeler/batman.html` ↔ `en/projeler/batman.html`: her biri diğerini `hreflang` ile gösteriyor, `x-default` TR'ye işaret ediyor.

- [ ] **Step 4: Tarayıcı testi (claude-in-chrome veya kullanıcı)** — `navigator.language` `en-US` iken `https://sukayipkacaklari.com/` (yerelde `/`) → `/en/`'e yönleniyor; TR|EN düğmesi karşı dile geçiyor ve seçim `localStorage['le-lang']`'e yazılıp kalıcı oluyor; `sessionStorage` bayrağı döngü engelliyor.

- [ ] **Step 5: `PROJECT.md`** — §5 tablosuna `/en/**` satırları; §6'ya "Jeneratörler `for lang in ('tr','en')` ile hem kök hem `/en/` üretir; `sitemap.xml` hreflang çiftli" notu; §8'e teslim satırı.

- [ ] **Step 6: Commit**

```bash
git add PROJECT.md sitemap.xml
git commit -m "Kapanış: tam İngilizce desteği doğrulandı + PROJECT.md güncellendi"
```

- [ ] **Step 7: Deploy notu (kullanıcıya)** — `nginx.conf` değişti; `PROJECT.md` §4'teki `custom_nginx_configuration` base64 PATCH + `deploy?force=true` gerekli (yoksa hatalı `/en/` yollarında Türkçe 404 görünür — fonksiyonel kayıp yok). `git push` sonrası Coolify otomatik deploy eder.

---

## Self-Review

**1. Spec coverage:**
- §2 URL yapısı / slug kararı → Task 3,5,7,9–16 (URL tablosu Global Constraints'te). ✔
- §3 `<head>` politikası (hreflang, og:locale, lang, JSON-LD `@id`/`inLanguage`) → referans A/B/C + Task 3 (TR), Task 5/7 (jeneratör), Task 9–16 (el). ✔
- §4 dil değiştirici → referans E/F + Task 2 (CSS/JS), her sayfa task'ı. ✔
- §5 açılış script'i → referans D + Task 3/5/7/9–16; `data-home` → referans C; §5.1 tıklama hafızası → referans G / Task 2. ✔
- §6 jeneratör iki dilli + sitemap → Task 5,6,7,8. ✔
- §7 el sayfalar → Task 9–16. ✔
- §8 CSS/JS/llms/nginx → Task 2,4; `webmanifest` dokunulmuyor (spec: kapsam dışı). ✔
- §9 doğrulama → Task 1 (validator genişletme), Task 17 (tam zincir + gözle). ✔
- §10 dalgalar → Faz 0–4 eşlemesi birebir. ✔
- §11 riskler → Task 8/6 gözle kontrol adımları, Task 17 Step 7 deploy notu. ✔

**2. Placeholder scan:** Referans string'ler (A–H) tam ve birebir. Çeviri gövde metinleri "actual content" değil çünkü bunlar içerik deliverable'ı (fonksiyon gövdesi muadili) — her task hangi kaynağı çevireceğini, hangi §7 kuralına uyacağını, hangi JSON-LD alanını değiştireceğini açıkça söylüyor. `formspree.io/f/BURAYA_FORM_ID` bilinçli olarak korunuyor (mevcut durum). "TODO/TBD" yok.

**3. Type consistency:** `prefix(lang)`, `out_dir(lang)`, `UI[lang]` iki jeneratörde aynı imza. `u(path, cf, pr, imgs)` yeni imza (path artık kök-göreli) — Task 7 Step 6'da tüm çağrılar güncelleniyor. `head(...)`/`page_head(...)` `lang` parametresi Task 5/7'de ekleniyor, Task 6/8 aynı imzayı kullanıyor. `localStorage` anahtarı her yerde `le-lang`, `sessionStorage` `le-lang-redirected`. CSS sınıfları `.nav__lang`, `.nav__lang-sep`, `.ftr__lang`, `.is-active` — referans E/F/G/H'de tutarlı.

**Bulunan sorunlar:** yok — plan spec ile hizalı.
