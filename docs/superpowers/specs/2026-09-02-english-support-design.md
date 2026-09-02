# LeakExpert — Siteye tam İngilizce desteği · Tasarım (spec)

> Tarih: 2026-09-02 · Durum: onaylandı (kullanıcı "hepsini yap, mantıklı kararları da ver" dedi)
> İlgili: `PROJECT.md` (§5 sayfa listesi, §6 jeneratörler, §7 içerik kuralları, §8 SEO)

---

## 1. Amaç ve kapsam

Türkçe statik siteye **tam paritede İngilizce** sürüm eklemek. Canlı sitenin
tüm indekslenebilir sayfaları (`PROJECT.md` §5'teki ~27 URL) İngilizce
karşılık kazanır. İngilizce metinleri Claude yazar; kullanıcı deploy öncesi
gözden geçirir.

**Kapsam dışı:** yeni tasarım/sayfa türü, CMS'e geçiş, build adımı ekleme,
`en.` subdomain, ayrı GA4 property. Tema yine yalnızca açık (light).

**Değişmez kurallar:** `PROJECT.md` §7 içerik kuralları İngilizce metinlere de
birebir uygulanır (cihaz/marka adı yok; ana sayfada şehir adı yok; "anında
onarılan / onarım bekleyen" yok; kurumsal müşteri yorumu yok; header'da
"Keşif talebi" yok; Türkiye geneli — bölgesel/şehir iniş sayfası yok; ev/bina/
konut içi kaçak tespiti yok; terim "proje").

---

## 2. URL ve dizin yapısı

- İngilizce sayfalar `/en/` önekiyle Türkçe ağacın **birebir aynası**. Slug'lar
  aynı kalır (çeviri yapılmaz), böylece TR↔EN eşleşmesi tek kurala iner:
  `EN yol = "/en" + TR yol` (kök için `/` ↔ `/en/`).

  | TR | EN |
  |---|---|
  | `/` | `/en/` |
  | `/platform.html` | `/en/platform.html` |
  | `/hizmetler.html` | `/en/hizmetler.html` |
  | `/projeler/` | `/en/projeler/` |
  | `/projeler/<slug>.html` (11) | `/en/projeler/<slug>.html` |
  | `/referanslar.html` | `/en/referanslar.html` |
  | `/hakkimizda.html` | `/en/hakkimizda.html` |
  | `/rehber/` | `/en/rehber/` |
  | `/rehber/<slug>.html` (4) | `/en/rehber/<slug>.html` |
  | `/sss.html` | `/en/sss.html` |
  | `/iletisim.html` | `/en/iletisim.html` |
  | `/gizlilik.html` | `/en/gizlilik.html` |
  | `/tesekkurler.html` | `/en/tesekkurler.html` (`noindex`) |
  | `/404.html` | `/en/404.html` (`noindex`) |

- Slug'lar Türkçe kalır (`hizmetler.html`, değil `services.html`). Gerekçe:
  eşleşme kuralının basitliği, jeneratör döngüsünün tek `slug` alanı
  kullanabilmesi, kırık link riskinin sıfırlanması. Kullanıcı görünürlüğü
  düşük (menü metinleri İngilizce; URL ikincil).
- Türkçe kök **kanonik** kalır. Her sayfada `x-default` → Türkçe URL.
- `robots.txt` değişmez (zaten her şeyi açar). `/en/` sitemap'e girer (§6).

---

## 3. `<head>` politikası (27 TR + 27 EN sayfa)

Her indekslenebilir sayfada (hem TR hem EN), karşılıklı ve tutarlı:

```html
<link rel="canonical" href="<kendi URL'si>">
<link rel="alternate" hreflang="tr" href="https://sukayipkacaklari.com/<yol>">
<link rel="alternate" hreflang="en" href="https://sukayipkacaklari.com/en/<yol>">
<link rel="alternate" hreflang="x-default" href="https://sukayipkacaklari.com/<yol>">
```

- TR sayfa: `<html lang="tr">`, `og:locale` `tr_TR` + `og:locale:alternate` `en_US`.
- EN sayfa: `<html lang="en">`, `og:locale` `en_US` + `og:locale:alternate` `tr_TR`.
- `<title>`, `meta description`, `og:title/description`, `twitter:title/description`
  İngilizce sayfada çevrilir. Açıklamalar ≤160 karakter kalır (Grup G1 kuralı),
  meta + OG + Twitter senkron.
- `tesekkurler` ve `404`: `noindex` kalır, **hreflang eklenmez** (indeksleme
  dışı). `<html lang>` yine doğru dile ayarlanır.
- Font preload'ları değişmez — `latin` + `latin-ext` alt kümeleri İngilizceyi
  zaten kapsar, **yeni woff2 yok**.
- GA4 snippet'i aynı (`G-ETN61F721R`), path bazlı ayrım GA tarafında yapılır.

### 3.1 JSON-LD

- `@id` çıpaları **aynı kalır** (`https://sukayipkacaklari.com/#org`, `#site`,
  `#hasan-koramaz`, `#muhammed-koramaz`, sayfa `#webpage`/`#article` id'leri).
  Tek varlık, iki dil — ayrı düğüm yaratılmaz.
- EN sayfalarda `inLanguage` → `en-US` (TR'de `tr-TR`). `WebPage`/`Article`/
  `FAQPage`/`BreadcrumbList` içindeki `name`, `headline`, `description`,
  `text`, soru/cevap metinleri, `knowsAbout` çevrilir.
- `Organization.address`, `telephone`, `email`, `areaServed` (Türkiye),
  `foundingLocation` (Kayseri) **değişmez**. `availableLanguage` zaten
  `["Turkish","English"]`.
- `BreadcrumbList` `item` URL'leri `/en/` önekli olur; `name`'ler İngilizce.

---

## 4. Dil değiştirici (header + footer)

- Header `<nav class="nav">` sonuna, son menü ögesinden görsel olarak ayrık
  bir blok:

  ```html
  <span class="nav__lang">
    <a href="<TR URL>" hreflang="tr" lang="tr">TR</a>
    <span aria-hidden="true">|</span>
    <a href="<EN URL>" hreflang="en" lang="en">EN</a>
  </span>
  ```

  Aktif dilin bağlantısına `aria-current="true"` ve `.is-active` sınıfı.
- Footer'da `.ftr__grid` altında aynı iki bağlantı (mevcut footer düzenine
  uygun küçük bir satır; yeni sütun eklenmez, "İletişim/Contact" sütununun
  altına bir `<p class="ftr__lang">` olarak).
- Bağlantı hedefleri **her sayfada sabit yazılır** (jeneratör/elle) — sayfa
  kendi TR ve EN karşılığını bilir. JS'e bağlı değildir.
- EN karşılığı olmayan teorik durum (tam paritede olmayacak): jeneratör
  yardımcı fonksiyonu, EN hedefi verilmezse TR köküne düşer (savunmacı
  varsayılan). Elle sayfalarda bu durum yok.
- CSS: `assets/css/site.css`'e yalnızca `.nav__lang` / `.ftr__lang` / mobil
  menüde konum stilleri. Mevcut token'lar ve renkler kullanılır. Sonra
  `py tools/minify.py`.

---

## 5. Başlangıçta bilgisayar diline göre açılış (client-side)

Statik site — sunucu tarafı içerik pazarlığı yok. `<head>` içinde, CSS'ten
**önce**, küçük **senkron** script (FOUC/flash olmadan yönlendirme):

### Davranış

1. **Kayıtlı tercih** — `localStorage['le-lang']` (`"tr"` | `"en"`), yalnızca
   kullanıcı TR|EN düğmesine tıklayınca yazılır (bkz. §5.1).
   - Değer var ve sayfanın dili farklıysa → sayfanın `hreflang` alternatifinden
     okunan karşı-dil URL'sine `location.replace()`. Tüm sitede sabitler.
2. **Tercih yok** — yalnızca **ana sayfada** (`/` veya `/en/`; script bunu
   `document.documentElement.dataset.home === "1"` ile bilir):
   - `navigator.languages` (yoksa `[navigator.language]`) taranır.
   - Hiçbiri `tr` ile başlamıyorsa ve sayfa TR ise → `/en/`'e `location.replace()`.
   - En az biri `tr` ile başlıyorsa ve sayfa EN ise → `/`'e `location.replace()`.
   - Alt sayfalarda tercih yoksa **hiçbir şey yapılmaz** (kullanıcının tıkladığı
     linke saygı).
3. **Döngü koruması** — yönlendirmeden hemen önce
   `sessionStorage['le-lang-redirected'] = "1"`; script başında bu bayrak
   varsa 1 ve 2 atlanır.

### SEO notları

- Kök URL yine **200 + Türkçe HTML** servis eder; Googlebot Türkçe içeriği
  görür ve indeksler. `hreflang` üçlüsü yön sinyalini verir.
- Yönlendirme yalnızca `navigator.languages` Türkçe içermeyen **gerçek
  kullanıcılarda** tetiklenir; cloaking değil (aynı içerik, dil tercihine
  göre yönlendirme — Google'ın tolere ettiği kalıp).
- `location.replace` kullanılır (geçmişe kirli giriş bırakmaz, geri tuşu
  çalışır).

### 5.1 Değiştirici ile etkileşim

- TR|EN bağlantılarına küçük satır-içi `onclick` yok; bunun yerine
  `assets/js/site.js`'e: `.nav__lang a`, `.ftr__lang a` tıklanınca
  `localStorage['le-lang']` tıklanan dile set edilir (link normal çalışır).
- `site.js` değişince `py tools/minify.py`.

### Uygulama

- Script `tools/` şablonlarına ve 10 elle sayfaya aynen gömülür (tek kaynak
  string; `PROJECT.md` §6'daki "head politikası değişince hem HTML hem
  jeneratör" kuralı geçerli).
- Ana sayfa işaretleyici: `<html lang="tr" data-home="1">` yalnızca `/` ve
  `/en/` sayfalarında.

---

## 6. Jeneratörler — iki dilli refaktör (Seçenek A)

`tools/gen_projects.py` (11 proje + `projeler/index.html` + **tüm
`sitemap.xml`**) ve `tools/gen_rehber.py` (`rehber/` hub + 4 makale) tek
kaynaktan hem TR hem EN üretir.

### Ortak desen (her iki script)

- `LANGS = ("tr", "en")`. Ana üretim döngüsü `for lang in LANGS:`.
- Yol öneki: `out_prefix = "" if lang == "tr" else "en/"`; dosyalar
  `SITE/<out_prefix><...>` altına yazılır. `en/` alt ağacı gerekiyorsa
  `os.makedirs(..., exist_ok=True)`.
- URL öneki: `base = BASE if lang == "tr" else BASE + "/en"`.
- **i18n tablosu**: script başında `UI = {"tr": {...}, "en": {...}}` sözlüğü —
  menü etiketleri, footer başlıkları/linkleri, "skip to content", breadcrumb
  kök adı ("Ana Sayfa"/"Home"), CTA metinleri, "Görüşme talebi"/"Request a
  consultation", eyebrow'lar vb.
- `header(current, lang)` / `nav(active, lang)` / `footer(lang)` /
  `page_head(...) `/ `head(...)` fonksiyonları `lang` parametresi alır:
  - `<html lang>` ve `data-home` doğru,
  - hreflang üçlüsü (`tr`/`en`/`x-default`) — `current` yolundan üretilir,
  - `og:locale` (+ alternate),
  - nav/footer link href'leri `/en` önekli (EN'de),
  - `.nav__lang` / `.ftr__lang` blokları bu sayfanın TR ve EN URL'siyle,
  - §5 açılış script'i,
  - `<title>`/`meta`/OG/Twitter `UI`/veri sözlüğünden.
- İçerik verisi:
  - `gen_projects.py` `P` listesindeki her `dict`e İngilizce alanlar:
    `name_en, kicker_en, h1_en, lede_en, desc_en, spec_en (etiketler),
    prose_en, ...` — TR alanlarıyla aynı şema. Rakamlar/birimler İngilizce
    biçime çevrilir (ondalık `.`, binlik `,`; "arıza/km/yıl" → "faults/km/yr").
  - `gen_rehber.py` `ARTICLES` listesine `title_en, desc_en, body_en, ...`.
  - Metin çevirileri `PROJECT.md` §7'ye uyar (marka/cihaz adı yok vb.).
- Şema blokları `lang`e göre `inLanguage`, çevrili `name/headline/description/
  text`, `/en/` breadcrumb URL'leri.

### `sitemap.xml` (yalnızca `gen_projects.py` yazar)

- `<urlset>`'e `xmlns:xhtml="http://www.w3.org/1999/xhtml"` eklenir.
- Her indekslenebilir sayfa **iki `<url>` girişi** (TR + EN), her birinde
  **üç `<xhtml:link rel="alternate">`** (`tr`, `en`, `x-default`).
- `<image:image>` girişleri her iki dilde de aynı asset yollarıyla korunur.
- `tesekkurler`, `404` sitemap'e girmez (mevcut durumla aynı).
- `lastmod` = üretim günü (mevcut davranış).
- Yardımcı `u(loc, cf, pr, imgs)` fonksiyonu, TR loc'tan EN loc türetip ikili
  yazacak şekilde genişletilir; sayfa listesi tek yerde kalır.

### Şablon eşitliği

`PROJECT.md` §6 uyarısı geçerli: `<head>` politikası, açılış script'i, nav,
footer, dil değiştirici **hem 20 elle/HTML dosyasında hem iki jeneratör
şablonunda** aynı olacak. Referans string'ler spec'in bu bölümüdür.

---

## 7. Elle yazılan 10 sayfanın İngilizce karşılığı

`/en/` altında elle: `index.html`, `platform.html`, `hizmetler.html`,
`hakkimizda.html`, `referanslar.html`, `iletisim.html`, `sss.html`,
`gizlilik.html`, `tesekkurler.html`, `404.html`.

- Her biri TR kaynağının **yapısal kopyası** (aynı sınıflar, aynı bölüm
  düzeni, aynı görseller) — yalnızca metin İngilizce, `<head>` §3 politikası,
  değiştirici §4, açılış script'i §5.
- `index.html` ve `en/index.html`: `data-home="1"`.
- `hizmetler.html`: 4 aşamalı yöntem, cihazlar jenerik İngilizce ("portable
  ultrasonic flow meter", "pressure data logger" — marka yok).
- `hakkimizda.html`: iki `Person` şeması `@id` korunur; unvanlar çevrilir.
- `iletisim.html`: form aynı Formspree placeholder (`formspree.io/f/BURAYA_
  FORM_ID`); harita embed'i aynı; adres Melikgazi/Kayseri kalır; `areaServed`
  Türkiye.
- `gizlilik.html` → "Privacy Policy". Yasal dayanak yine **KVKK** (Kanun No.
  6698) olarak anlatılır; "KVKK (Turkey's Personal Data Protection Law)" gibi
  kısa açıklama. Aynı hak/başvuru maddeleri.
- `sss.html`: 11 soru `FAQPage` şemasıyla çevrilir; ev/bina içi kaçak ima
  eden soru eklenmez (mevcut TR'de de yok).
- `tesekkurler.html`, `404.html`: `noindex`; kısa metin çevirisi; hreflang yok.

---

## 8. Destekleyici değişiklikler

- `assets/css/site.css`: `.nav__lang`, `.ftr__lang`, mobil menüde dil bloğu
  konumu. Sadece ekleme. → `py tools/minify.py` (→ `site.min.css`).
- `assets/js/site.js`: §5.1 değiştirici-tıklama → `localStorage['le-lang']`.
  → `py tools/minify.py` (→ `site.min.js`).
- `llms.txt`: İngilizce özet bölümü + `/en/` ana giriş bağlantısı eklenir.
- `site.webmanifest`: `lang`/`dir` alanı yoksa dokunulmaz; iki dilli manifest
  gerekmiyor (kapsam dışı).
- `nginx.conf` (repo referans kopyası): `location / ` bloğundan **önce**
  `/en/` için İngilizce 404:

  ```nginx
  location ^~ /en/ {
      add_header X-Powered-By "LeakExpert" always;
      add_header X-Content-Type-Options "nosniff" always;
      add_header X-Frame-Options "SAMEORIGIN" always;
      add_header Referrer-Policy "strict-origin-when-cross-origin" always;
      add_header Permissions-Policy "geolocation=(), microphone=(), camera=()" always;
      add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
      add_header Cache-Control "public, max-age=0, must-revalidate" always;
      try_files $uri $uri/ $uri.html /en/404.html;
  }
  error_page 404 /404.html;   # kök/diğer yollar için Türkçe 404
  ```

  Deploy: `PROJECT.md` §4'teki `custom_nginx_configuration` base64 PATCH +
  `deploy?force=true`. (Bu adım olmadan `/en/` kırık yolları Türkçe 404
  gösterir — kabul edilebilir ama tercih edilen İngilizce 404.)
- `.htaccess`: statik host yedeği; `ErrorDocument 404 /404.html` yeterli,
  değişiklik gerekmez.

---

## 9. Doğrulama

- `tools/validate_all.py` genişletilir:
  - Her indekslenebilir HTML'de `hreflang="tr"`, `hreflang="en"`,
    `hreflang="x-default"` üçlüsü var mı ve işaret ettiği dosyalar diskte
    çözülüyor mu (linkcheck mantığıyla).
  - `/en/**` sayfalarında `<html lang="en">`, kök ağaçta `<html lang="tr">`.
  - JSON-LD `inLanguage` alanı sayfa diliyle tutarlı.
  - Mevcut kontroller (tag dengesi, JSON-LD parse, Article zorunlu alanlar,
    img boyutları, GA etiketi) `**/*.html` üzerinden `/en/`'i zaten kapsar.
- `tools/linkcheck.py`: `/en/` linkleri zaten `**/*.html` taramasına girer;
  ek kod gerekmez.
- `tools/add_img_dims.py`: `/en/` HTML'lerine de çalışır (idempotent).
- Manuel: bir TR ve bir EN sayfada Google Rich Results / hreflang
  reciprocity gözle kontrol; değiştirici ve §5 açılış script'i tarayıcıda
  denenir (Türkçe olmayan `navigator.language` ile `/` → `/en/`).

Tipik akış (`PROJECT.md` §6 güncellenmiş hali):
`py tools/gen_projects.py` → `py tools/gen_rehber.py` → `py tools/add_img_dims.py`
→ `py tools/minify.py` → `py tools/validate_all.py` → `py tools/linkcheck.py`
→ `git commit` → `git push`.

---

## 10. Teslim dalgaları (implementation plan girdisi)

1. **Ortak altyapı**: `/en/` dizin iskeleti; `<head>`/hreflang string'i; §4
   değiştirici bloğu (CSS dahil); §5 açılış script'i; `assets/js/site.js` +
   `assets/css/site.css` düzenleme + `minify.py`; `en/404.html`,
   `en/tesekkurler.html`; `nginx.conf` `/en/` bloğu.
2. **Jeneratör refaktörü**: `gen_rehber.py` iki dilli + 4 makale EN içerik;
   `gen_projects.py` iki dilli + `projeler/index.html` EN + 11 proje EN
   içerik; iki dilli `sitemap.xml`. `py` ile üret, çıktı farkını incele.
3. **Elle EN sayfalar A**: `en/index.html`, `en/platform.html`,
   `en/hizmetler.html`.
4. **Elle EN sayfalar B**: `en/hakkimizda.html`, `en/referanslar.html`,
   `en/iletisim.html`, `en/sss.html`.
5. **Elle EN sayfalar C + çevre**: `en/gizlilik.html`; `llms.txt`;
   `PROJECT.md` §5/§6/§8 güncellemesi.
6. **Doğrulama**: `validate_all.py` genişletme; tüm araç zinciri; `linkcheck`;
   gözle hreflang + açılış script'i testi; commit.

---

## 11. Riskler / kabuller

- **Çeviri hacmi**: 11 proje detayı + 4 rehber makalesi uzun metin. Çeviriler
  teknik doğrulukla ve §7 kurallarına uyularak yazılır; kullanıcı deploy
  öncesi gözden geçirir (özellikle rakam/birim biçimleri ve kurum adları).
- **Slug'lar Türkçe**: `/en/hizmetler.html` gibi URL'ler İngilizce kullanıcıya
  bir miktar yabancı; kabul edildi (eşleşme basitliği > URL estetiği).
- **JS yönlendirme + SEO**: kök 200/Türkçe servis ettiği ve hreflang mevcut
  olduğu için düşük risk; yönlendirme yalnızca ana sayfada ve yalnızca
  tercih yoksa.
- **Jeneratör şablon kayması**: `<head>`/nav/footer/script string'i 20 HTML +
  2 şablonda aynı olmalı; spec §3–§6 tek referans. `validate_all.py`
  genişletmesi kaymayı yakalar.
- **`custom_nginx_configuration` PATCH**: `/en/` 404 için gerekli; unutulursa
  yalnızca hatalı `/en/` yollarında Türkçe 404 görünür (fonksiyonel kayıp
  yok).
