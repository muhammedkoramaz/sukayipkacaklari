# LeakExpert — `/rehber/` → `/blog/` taşıma + 8 yeni makale · Tasarım (spec)

> Tarih: 2026-09-04 · Durum: onaylandı (kullanıcı "devam" dedi — kapsam: 8 makalenin
> hepsi, TR+EN, `/blog/` yoluna taşı, kartlar görselli)
> İlgili: `PROJECT.md` (§5 sayfa listesi, §6 jeneratörler, §7 içerik kuralları, §8 SEO),
> `docs/superpowers/specs/2026-09-02-english-support-design.md`

---

## 1. Amaç ve kapsam

Rakip site `sukayipkacak.com`'un "uygulamalar" + blog kapsamındaki, LeakExpert
sitesinde henüz karşılığı olmayan konular için **8 yeni makale** yazmak; mevcut
`/rehber/` bölümünü **`/blog/`** olarak yeniden adlandırıp taşımak; hub kartlarına
ve makalelere **görsel** eklemek.

**Kesin sınır:** Rakibin makale metinleri **kopyalanmaz, "biraz değiştirilerek"
de kopyalanmaz.** Yalnızca konu başlıkları referans alınır; tüm metin sıfırdan,
özgün olarak yazılır. İngilizce sürümleri Claude yazar; kullanıcı deploy öncesi
gözden geçirir.

**Kapsam dışı:** CMS'e geçiş, build adımı, ayrı `blog.` subdomain, yorum sistemi,
yazar sayfaları, tarih/etiket arşivi, RSS. Tema yine yalnızca açık (light).

**Değişmez kurallar (`PROJECT.md` §7 — TR ve EN metinlerin ikisine de uygulanır):**
cihaz/marka adı yok (jenerik: "taşınabilir ultrasonik debimetre", "basınç veri
loggerı", "elektromanyetik hat dedektörü"); ana sayfada/örneklerde şehir adı yok
("bir belediyede…"); **"anında onarılan / onarım bekleyen" ifadesi hiçbir yerde
geçmez**; kurumsal müşteri yorumu yok; header'da "Keşif talebi" butonu yok, CTA =
görüntülü görüşme talebi (saha ziyareti değil); Türkiye geneli — bölgesel/şehir
iniş sayfası yok; **ev/bina/konut içi kaçak tespiti yok** — kapsam yalnızca
belediye + sanayi (OSB) dağıtım şebekeleri; terim "proje".

---

## 2. Bölüm taşıma: `/rehber/` → `/blog/`

### 2.1 URL ve dizin

- Yeni yollar: `/blog/` ve `/en/blog/`. Makale slug'ları **Türkçe kalır** ve
  değişmez (mevcut 4 makale dâhil). Eşleşme kuralı korunur: `EN yol = "/en" + TR yol`.
- Dosya taşıma: `git mv rehber blog` + `git mv en/rehber en/blog`.
- Jeneratör: `git mv tools/gen_rehber.py tools/gen_blog.py`; içindeki tüm
  `/rehber/` yol sabitleri ve çıktı yolları `/blog/` olur; başlıktaki modül
  açıklaması güncellenir.

### 2.2 Görünen etiket "Blog"

Aşağıdaki yerlerde "Rehber" → "Blog", `/rehber/` → `/blog/`:

| Yer | Ayrıntı |
|---|---|
| `gen_blog.py` `UI` dict | `menu`, `ftr_corp`, `guide`, `guide_eyebrow`, `hub_title`, `hub_desc`, `hub_h1`, `hub_lede`, `hub_name`, breadcrumb adı (TR "Blog", EN "Blog") |
| `gen_projects.py` | paylaşılan menü + footer "Kurumsal" listesi (iki jeneratör senkron — §6) |
| El-HTML ×20 | 10 kök (`index, platform, hizmetler, referanslar, hakkimizda, sss, iletisim, gizlilik, tesekkurler, 404`) + 10 `en/` karşılığı: `<nav class="nav">` linki, `.nav__lang` içindeki hreflang yolları yok (onlar sayfa-özel), footer "Kurumsal" `<li><a href="/blog/">Blog</a></li> |
| `projeler/*.html` + `en/projeler/*.html` | jeneratör üretimi — `gen_projects.py` değişince regen ile düzelir |
| JSON-LD | `BreadcrumbList` position 2 adı "Blog"; hub `CollectionPage` `name` "Blog" / "Blog" (EN). `@type` değişmez (`CollectionPage`, makalelerde `Article`). |

### 2.3 301 yönlendirme

Site henüz Google'da indekslenmedi (`PROJECT.md` §9), yani yol değişikliği
maliyetsiz; yine de eski yolları yakalamak için:

- **nginx** (`nginx.conf`, `location /`'ten önce):
  ```nginx
  location ~ ^/(en/)?rehber(/.*)?$ { return 301 /$1blog$2; }
  ```
  Deploy: `PROJECT.md` §4 — `custom_nginx_configuration` base64 PATCH + `deploy?uuid=…&force=true`.
- **`.htaccess`** (repo'da tutulan yedek, canlıda kullanılmıyor):
  `RedirectMatch 301 ^/(en/)?rehber(/.*)?$ /$1blog$2`

### 2.4 Diğer dosyalar

- `llms.txt`: "## Rehber (kavramsal içerik)" → "## Blog"; 5 TR link + EN satırındaki
  `/rehber/` → `/blog/`; 8 yeni makale linki eklenir.
- `sitemap.xml`: tüm `/rehber/` → `/blog/`; 8 yeni makale × (TR + EN) = **16 yeni
  `<url>`**, her biri hreflang üçlüsü (`tr` / `en` / `x-default`→TR) + `lastmod`
  2026-09-04. Hub `lastmod` güncellenir. (Üretimi hangi jeneratörün yaptığı
  planlama sırasında doğrulanır — `PROJECT.md` §6'ya göre `gen_projects.py`.)
- `PROJECT.md`: §5 tablo (`/rehber/` satırları → `/blog/`, makale sayısı 4 → 12,
  TR indekslenebilir 25 → 33, EN 25 → 33, toplam 50 → 66), §6 jeneratör adı
  `gen_rehber.py` → `gen_blog.py`, §8'e "F (2026-09-04)" satırı.

---

## 3. İçerik — 8 yeni makale

Hedef biçim: mevcut rehber yazıları gibi. ~600–900 kelime, 5–8 `<h2>`, açılış
`lede` (`<strong>` vurgulu), kapanışta "yöntemin saha karşılığı" + iç link listesi
(`/hizmetler.html`, `/projeler/`, `/sss.html`, ilgili diğer blog yazıları),
sonda `cta-band`. Her makale `Article` JSON-LD (`headline`, `description`,
`datePublished` 2026-09-04, `inLanguage`, `image` [hero], `isPartOf` →
`/blog/` CollectionPage, `publisher` Organization `@id`).

Her `ARTICLES` dict alanları: `slug`, `h1`, `title`, `desc`, `lede`, `card_desc`,
`hero` (asset yolu), `hero_alt`, `hero_alt_en`, `h1_en`, `title_en`, `desc_en`,
`lede_en`, `card_desc_en`, `body`, `body_en`.

| # | slug | H1 (TR) | Ana bölümler (taslak) | İç linkler | Hero görsel |
|---|---|---|---|---|---|
| 1 | `debi-olcumu-nedir` | Debi ölçümü nedir, şebekede nasıl yapılır? | Debi neden ölçülür · taşınabilir ultrasonik/EM debimetre · kalıcı bölge (DMA) sayacı · ölçüm noktası ve düz boru şartı · gece minimum debi · doğruluk ve hata kaynakları | `dma-nedir`, `adim-testi-nedir`, `hizmetler.html`, `projeler/` | `assets/photos/debi-olcum.webp` |
| 2 | `basinc-yonetimi-nedir` | Basınç yönetimi ve basınç bölgeleri (PMA) | Basınç–kaçak/patlak ilişkisi (N1) · basınç bölgesi (PMA) nedir · basınç düşürücü vana · sabit / zaman / akış kontrollü ayar · kazançların ölçülmesi | `dma-nedir`, `su-kaybi-dusurme-yol-haritasi`, `hidrolik-modelleme-nedir` | `assets/photos/basinc-logger.webp` |
| 3 | `adim-testi-nedir` | Adım (step) testi ile kaçak bölgeleme | Amaç · hazırlık (vana listesi, gece penceresi) · kademeli kapatma ve debi basamakları · yorumlama (hangi alt hatta kayıp) · riskler ve iletişim | `dma-nedir`, `debi-olcumu-nedir`, `akustik-su-kacagi-tespiti-nedir` | `assets/photos/gece-operasyon.webp` |
| 4 | `sifir-basinc-testi-nedir` | Sıfır basınç testi nedir? | Ne zaman uygulanır · hattı izole etme · basıncı sıfıra indirme ve gözlem · "tutuyor / tutmuyor" kararı · adım adım uygulama · güvenlik ve su kalitesi | `adim-testi-nedir`, `akustik-su-kacagi-tespiti-nedir` | Drive kürasyon (vana/izolasyon) |
| 5 | `hidrolik-modelleme-nedir` | Hidrolik modelleme ve saha kalibrasyonu | Model nedir, ne işe yarar · girdiler (boru, kot, tüketim, sınır koşulları) · saha basınç/debi ölçümüyle kalibrasyon · kayıp ve basınç yönetimi senaryoları · sınırlar | `basinc-yonetimi-nedir`, `dma-nedir`, `sebeke-haritalama-cbs` | `assets/photos/basinc-test.webp` |
| 6 | `boru-hatti-tespiti-nedir` | Boru hattı güzergâhı ve derinlik tespiti | Neden gerekir · metal hat: elektromanyetik hat dedektörü · plastik (PE/PVC) hat: dâhili prob, sinyal teli, yer radarı (GPR) · işaretleme ve derinlik · doğruluğun sınırları | `sebeke-haritalama-cbs`, `hizmetler.html` | Drive kürasyon (saha, işaretleme) |
| 7 | `sebeke-haritalama-cbs` | Şebeke haritalama ve CBS'e (GIS) aktarım | Saha tespitinden veriye · GPS koordinat + öznitelik (çap, malzeme, döşeme yılı) · CBS katmanı ve topoloji · LeakExpert platformuna işleme · haritayı güncel tutma | `boru-hatti-tespiti-nedir`, `platform.html` | Drive kürasyon (harita/ekran) veya platform görseli |
| 8 | `kacak-onarimi-ve-dogrulama` | Kaçak onarımı ve onarım sonrası doğrulama | Nokta teyidi ve kazı öncesi kontrol · onarım tipleri (kelepçe, parça değişimi, hat yenileme — idare/yüklenici ekibi yapar) · onarım sonrası gece debi tekrar ölçümü · kapanan kayıp ve raporlama | `akustik-su-kacagi-tespiti-nedir`, `debi-olcumu-nedir`, `su-kaybi-dusurme-yol-haritasi` | Drive kürasyon (kazı/onarım) |

**§7.4 uyarısı (madde 8):** Makale, onarımı **idarenin/yüklenicinin** yaptığı,
LeakExpert'in rolünün **nokta tespiti + onarım sonrası doğrulama** olduğu
çerçevesinde yazılır. "Anında onarıldı", "onarım bekleyen arıza" gibi ifadeler
kullanılmaz.

Hub `CollectionPage` `hasPart` listesi 12 maddeye çıkar (4 mevcut + 8 yeni),
sıralama: giriş/genel → ölçüm → bölgeleme/test → modelleme → hat tespiti/harita →
onarım → yol haritası.

---

## 4. Kart + makale görselleri

### 4.1 Hub kartı (görselli)

- `gen_blog.py` kart şablonu: `<a class="card card--media">` içinde en üstte
  `<img class="card__img" width="…" height="…" loading="lazy" decoding="async">`
  (16:9), altında mevcut `card__ix` numara + `<h3>` + `<p>`.
- `assets/css/site.css`'e `.card--media` / `.card__img` kuralları (16:9 `aspect-ratio`,
  `object-fit:cover`, üst köşe yuvarlama, numara rozeti görsel üstüne
  konumlanır). Değişiklikten sonra `py tools/minify.py` → `site.min.css`.
- Mevcut 4 makale de görselli karta geçer (hero görselleri: `su-kacagi-nasil-anlasilir`
  → `photos/gunduz-dinleme.webp`, `akustik-…` → `photos/gece-dinleme-hero.webp`,
  `dma-nedir` → `photos/dma-tasarim.webp`, `su-kaybi-dusurme-yol-haritasi` →
  `photos/depo-cikis.webp`; planlamada uygunluk teyit edilir).

### 4.2 Makale sayfası hero

- `lede`'den sonra tam genişlik `<figure>` + `<img>` (hero). `projeler/*.html`
  görsel desenine yaslanır.
- `Article` JSON-LD `image` dizisine hero mutlak URL'si.
- EN sürüm aynı dosyayı kullanır, `alt`/`figcaption` İngilizce.

### 4.3 Görsel kaynağı ve kürasyon hattı

- Öncelik: repodaki `assets/photos/*.webp` (11 kürasyonlu dosya).
- Eksik konular (#4, #6, #7, #8 ve gerekirse diğerleri) için: Drive
  `G:\Drive'ım\SKK` (özellikle `YAPILAN İŞLER/<şehir>/FOTOĞRAFLAR/…`,
  ~4.338 dosya) içinden Claude aday seçer → 1600px genişlik, WebP q~80,
  EXIF temiz → `assets/blog/<slug>.webp`.
- **Onay kapısı:** yeni görseller `assets/blog/` altına konduktan sonra Claude
  kullanıcıya küçük bir önizleme (Artifact galeri) sunar; kullanıcı onaylamadan
  jeneratör çalıştırılmaz. Fotoğraflarda kişi yüzü / plaka / kurum tabelası
  görünüyorsa kırpılır veya elenir (kurumsal müşteri gizliliği — §7.5 ruhu).
- Son adım: `py tools/add_img_dims.py` (tüm yeni `<img>`'lere gerçek `width`/`height`).

---

## 5. Jeneratör / derleme zinciri

1. Görsel kürasyon + kullanıcı onayı (§4.3).
2. `git mv` (rehber→blog ×2) + `git mv tools/gen_rehber.py tools/gen_blog.py`.
3. `gen_blog.py`: 8 yeni `ARTICLES` dict (body + body_en + hero alanları),
   görselli kart şablonu, 12 maddelik hub listesi, `/blog/` yolları, "Blog"
   etiketleri.
4. `gen_projects.py`: paylaşılan menü/footer "Blog" + `/blog/` (senkron).
5. El-HTML ×20: menü + footer linkleri "Blog" + `/blog/`.
6. `nginx.conf` 301 kuralı · `.htaccess` · `llms.txt` · `sitemap.xml` · `PROJECT.md`.
7. Çalıştır: `py tools/gen_blog.py` → `py tools/gen_projects.py` →
   `py tools/add_img_dims.py` → `py tools/minify.py` → `py tools/validate_all.py`
   → `py tools/linkcheck.py`. Hepsi 0 hata / 0 kırık link olmalı.
8. `git add -A && git commit && git push` (Coolify otomatik deploy).
9. Coolify: `custom_nginx_configuration` base64 PATCH + `deploy?uuid=y7f6p5waot2jz9kvlqwasshh&force=true`.
10. Deploy sonrası doğrulama: `curl -I https://sukayipkacaklari.com/rehber/dma-nedir.html`
    → `301` → `/blog/dma-nedir.html`; `/blog/` ve 2–3 yeni makale `200`;
    `/en/blog/…` `200`; eski `/en/rehber/…` → `301`.

---

## 6. `validate_all.py` / `linkcheck.py` etkisi

- `validate_all.py`: yeni 16 URL için hreflang üçlüsü diskte çözülmeli; `<html lang>`
  ağaç tutarlılığı; `Article` zorunlu alanları (`headline`, `datePublished`,
  `image`); `inLanguage`. Script'te sabit `rehber` yolu geçiyorsa `blog`'a çekilir.
- `linkcheck.py`: hiçbir dosyada `/rehber/` iç linki kalmamalı (301'e düşmesin).

---

## 7. Riskler / açık noktalar

- **Görsel uygunluğu:** Drive fotoğrafları WhatsApp kalitesinde ve kişisel/kurumsal
  veri içerebilir. Onay kapısı (§4.3) bunu yönetir; yeterli temiz görsel çıkmazsa
  ilgili kart `assets/photos/` içinden en yakın jenerik görsele düşer.
- **`sitemap.xml` üretimi:** iki jeneratör de dokunuyorsa çakışma; planlamada
  hangisinin yazdığı netleştirilip tek kaynak korunur.
- **`#3`/`#4` ayrımı:** kullanıcı ayrı istedi. İçerik yazımında örtüşme olursa
  çapraz link ile ayrıştırılır (step test = bölgeleme; sıfır basınç = doğrulama).
- **`nginx` PATCH atlanırsa:** eski `/rehber/` yolları markalı `/404.html`'e düşer
  (fonksiyonel kayıp yok, sadece 301 yok). Deploy adımı 9 zorunlu.
