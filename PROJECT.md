# LeakExpert · sukayipkacaklari.com — Proje Kılavuzu

> Bu dosya projenin tek referans noktası. Yeni bir oturuma/geliştiriciye "her şey burada" demek için.
> Son güncelleme: 2026-09-01. Geliştirici notları için ayrıca `README.md`.

---

## 1. Firma bilgileri (site genelinde kullanılan)

| Alan | Değer |
|---|---|
| Marka | **LeakExpert** — "Su Kayıp Kaçakları" |
| İş | Belediye + sanayi (OSB) içme suyu şebekelerinde su kayıp-kaçak tespiti, debi/basınç izleme, saha yönetimi + kendi yazılım platformu |
| Deneyim | 25+ yıl · kuruluş 2004 |
| Ofis adresi | **Melikgazi / Kayseri** (kayıtlı merkez — hizmet alanı **Türkiye geneli**) |
| Telefon | **+90 539 658 84 34** · `tel:+905396588434` · `wa.me/905396588434` |
| E-posta | **sukayipkacaklari@gmail.com** |
| Ekip | Hasan Koramaz (Su Kayıp Kaçakları Uzmanı, Kurucu) · M. Muhammed Koramaz (Bilgisayar Mühendisi — platform & saha yürütme) |

---

## 2. Adresler ve erişim

| Ne | Adres |
|---|---|
| Canlı site | **https://sukayipkacaklari.com** (kanonik **non-www**; `www.` → 301 → apex) |
| GitHub repo | `github.com/muhammedkoramaz/sukayipkacaklari` — branch `main` |
| Yerel çalışma dizini | `C:\Users\muham\Desktop\LEAKEXPERT APPS\leakexpert-site\` |
| Eski Next.js uygulaması (asset kaynağı) | `C:\Users\muham\Desktop\LEAKEXPERT APPS\leakexpert-web\` |
| Coolify app | ad `sukayipkacaklari-site` · uuid **`y7f6p5waot2jz9kvlqwasshh`** |
| Sunucu IP | **`45.87.120.20`** · SSL Let's Encrypt (otomatik) |
| GA4 ölçüm kimliği | **`G-ETN61F721R`** (tüm sayfalarda + jeneratörlerde gömülü) |
| Google Search Console | Doğrulandı 2026-09-01 · sitemap gönderildi |

Coolify API çağrıları `$COOLIFY_API_TOKEN` ve `$COOLIFY_API_URL` ortam değişkenlerini kullanır.

---

## 3. Teknik yapı

- **Saf statik site**: elle yazılmış HTML + CSS + JS. Build adımı yok. Kök dizine (`/`) kurulur (tüm yollar kök-göreli).
- **CSS/JS minify**: kaynak `assets/css/site.css` · `fonts.css` · `assets/js/site.js` elle düzenlenir; `py tools/minify.py` bunlardan `*.min.css` / `*.min.js` üretir. HTML **daima `.min` sürümlere** referans verir. `.min` dosyaları repoya commit edilir (deploy'da build yok).
- **Tema**: sadece açık (light). Marka mavisi `#2563eb`. Tokenlar `assets/css/site.css` başında.
- **Fontlar**: kendi sunucumuzda (`assets/fonts/*.woff2`) — Bricolage Grotesque (başlık), Plus Jakarta Sans (gövde), JetBrains Mono (veri). `assets/css/fonts.css`. Google Fonts'a istek yok.
- **Görseller**: WebP (`assets/projects/`, `assets/photos/`, `assets/brands/`, `assets/team/`). OG kapağı `assets/img/og-cover.png`.
- **Logo**: `assets/img/logo.svg` (gerçek kurumsal kelime markası) header + footer. Şemalarda `logo` = `assets/img/icon.png` (2000×2000 raster).

---

## 4. Yayın / deploy (Coolify)

`main`'e her `git push` → Coolify otomatik deploy eder.

**Kritik nokta — nginx yapılandırması:** repo'daki `nginx.conf` dosyası **kullanılmaz**.
Coolify `static` buildpack, config'i uygulama ayarındaki **`custom_nginx_configuration`**
alanından okur (bunu `/etc/nginx/conf.d/default.conf` olarak yazar). Repo'daki `nginx.conf`
sadece referans kopyadır.

nginx config değiştirmek için:

```bash
# 1) base64'le ve PATCH et
py -c "import json,base64;print(json.dumps({'custom_nginx_configuration': base64.b64encode(open('nginx.conf','rb').read()).decode()}))" > patch.json
curl -X PATCH -H "Authorization: Bearer $COOLIFY_API_TOKEN" -H "Content-Type: application/json" \
  --data @patch.json "$COOLIFY_API_URL/api/v1/applications/y7f6p5waot2jz9kvlqwasshh"
# 2) deploy
curl -X POST -H "Authorization: Bearer $COOLIFY_API_TOKEN" \
  "$COOLIFY_API_URL/api/v1/deploy?uuid=y7f6p5waot2jz9kvlqwasshh&force=true"
# 3) durum
curl -s -H "Authorization: Bearer $COOLIFY_API_TOKEN" "$COOLIFY_API_URL/api/v1/deployments/<deployment_uuid>"
```

`custom_nginx_configuration` içeriği **conf.d formatında** olmalı: sadece `server {}` blokları +
`gzip`/`add_header` gibi http-bağlamı direktifleri. `http {}` / `events {}` sarmalayıcısı **KOYMA**
(nginx çöker → 503). Notlar: create/PATCH `fqdn` anahtarını reddeder → `domains` kullan.

**Config'in uyguladıkları:** `www` → non-www 301 · gzip · güvenlik başlıkları
(`X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy`, `Permissions-Policy`,
`Strict-Transport-Security`) · `/assets/**` 1 yıl `immutable` cache · `.xml/.txt` 1 saat ·
güzel URL (`try_files $uri $uri/ $uri.html`) · markalı `error_page 404 /404.html`.

---

## 5. Sayfalar (25 URL · sitemap.xml)

| Yol | İçerik | Şema |
|---|---|---|
| `/` | Ana sayfa | Organization+ProfessionalService, WebSite |
| `/platform.html` | Yazılım platformu (mobil + web + API) | SoftwareApplication (featureList) |
| `/hizmetler.html` | Saha hizmetleri + 4 aşamalı yöntem | Service, OfferCatalog, BreadcrumbList |
| `/projeler/` | Proje listesi | BreadcrumbList, ItemList |
| `/projeler/*.html` (**11**) | Proje detayları: Kütahya, Batman, Çanakkale, Keşan, Kilis, Sivas, Rize, Doğubayazıt, Fatsa, Bodrum, Mozambik-Beira | BreadcrumbList, Article (image dizisi, datePublished, isPartOf) |
| `/referanslar.html` | Kurum logoları + proje geçmişi | BreadcrumbList |
| `/hakkimizda.html` | Ekip + saha galerisi | AboutPage, Person ×2 |
| `/rehber/` | Rehber hub | CollectionPage |
| `/rehber/*.html` (**4**) | su-kacagi-nasil-anlasilir · akustik-su-kacagi-tespiti-nedir · dma-nedir · su-kaybi-dusurme-yol-haritasi | BreadcrumbList, Article |
| `/sss.html` | **11** SSS | FAQPage |
| `/iletisim.html` | Form + Melikgazi/Kayseri haritası | LocalBusiness (areaServed = Türkiye), BreadcrumbList |
| `/gizlilik.html` | KVKK gizlilik politikası | BreadcrumbList |
| `/tesekkurler.html` | Form sonrası (`noindex`) | — |
| `/404.html` | Bulunamadı (`noindex`) | — |
| `robots.txt` · `sitemap.xml` · `site.webmanifest` | SEO / PWA | — |

---

## 6. Sayfa üretimi (jeneratörler → `tools/`)

Bazı sayfalar elle değil script ile üretilir. Scriptler artık repo'da `tools/` altında.
Windows'ta `py` (Python 3.10) + `PYTHONUTF8=1` ile çalıştır.

| Script | Ne üretir |
|---|---|
| `tools/gen_projects.py` | 11 proje sayfası + `projeler/index.html` + `sitemap.xml` (proje verisi `P` listesinde) |
| `tools/gen_rehber.py` | `/rehber/` hub + 4 makale (`ARTICLES` listesinde) |
| `tools/add_img_dims.py` | **Her jeneratör çalıştırmasından sonra** — tüm yerel `<img>`'lere gerçek `width`/`height` ekler (CLS düzeltmesi; idempotent) |
| `tools/minify.py` | `site.css` / `fonts.css` / `site.js` → `*.min.*` üretir. **CSS/JS kaynağı değiştiyse çalıştır.** Bağımlılık yok, idempotent |
| `tools/validate_all.py` | tag dengesi + JSON-LD parse + Article zorunlu alanlar + img boyut + GA etiketi |
| `tools/linkcheck.py` | kırık iç link taraması |

Tipik akış: `py tools/gen_projects.py` → `py tools/gen_rehber.py` → `py tools/add_img_dims.py` → (`site.css`/`site.js` değiştiyse `py tools/minify.py`) → `py tools/validate_all.py` → `py tools/linkcheck.py` → `git commit` → `git push` (Coolify deploy eder).

> Jeneratör şablonları (`gen_projects.py`, `gen_rehber.py`) `<head>` bloğunu — meta description, font preload, GA snippet, `.min` referansları — kendi içlerinde tutar. `<head>` politikası değişirse **hem 27 HTML'i hem iki jeneratör şablonunu** güncelle, yoksa ilk `regen` geri alır.

`SITE` yolu her jeneratörün başında sabit yazılı — repo taşınırsa orayı güncelle. `nginx.conf`
değiştiyse ayrıca §4'teki `custom_nginx_configuration` PATCH'i unutma.

---

## 7. İçerik kuralları — İHLAL ETME

Bunlar kullanıcının açık talimatları. Yeni içerik eklerken hepsine uy:

1. **Açık tema** her yerde. Terim "**proje**", "vaka" değil.
2. **Cihaz/marka adı yok** (Keller, SEBA, Sitelab, Aktek… hiçbiri). Jenerik yaz: "basınç veri loggerı", "taşınabilir ultrasonik debimetre".
3. **Ana sayfada şehir adı yok.** Örnekler "Bir belediyede …" der.
4. **"anında onarılan" / "onarım bekleyen"** ifadeleri hiçbir proje sayfasında geçmez.
5. **Müşteri yorumu / referans metni yok** (kurumsal müşteri). Onun yerine proje fotoğrafları.
6. **Header'da "Keşif talebi" butonu yok.** CTA'lar "görüşme / uzaktan görüntülü görüşme talebi" çerçevesinde; saha ziyareti değil.
7. Header'da **gerçek logo** (`logo.svg`), çizilmiş damla ikonu değil.
8. **Batman / Kütahya** vurgusu = toplam taranan km + toplam bulunan arıza sayısı (yan yana 2 arıza anekdotu değil).
9. **Bölgesel / Kayseri hizmet konumlandırması yok** — Türkiye geneli çalışılır. Şehir iniş sayfası yapma. Ofis adresi (Melikgazi/Kayseri) iletişim/footer/şemada kalır ama `areaServed` = yalnızca Türkiye.
10. **Ev / bina / konut içi kaçak tespiti yok.** Kapsam sadece belediye + sanayi (OSB) dağıtım şebekeleri. İç tesisat kaçağı ima eden SSS/içerik ekleme.

---

## 8. SEO — yapılanlar

| Grup | İş |
|---|---|
| **A** | non-www kanonik + `www`→301 · güvenlik/gzip/cache başlıkları (nginx custom config) · anahtar kelime title/meta/H1 · hreflang (tr/x-default) · self-hosted fontlar · WebP görseller · genişletilmiş şema (Organization/ProfessionalService + WebSite + Person) · iç linkleme · sitemap `lastmod` + `image` · GA4 |
| **B** | `/rehber/` bölümü (hub + 4 SEO makalesi) · SSS 5 → 11 soru (FAQPage) |
| **C** | Proje sayfaları Article şeması derinleştirme (gerçek foto `image` dizisi, `datePublished`, `isPartOf` CollectionPage) · `platform.html` SoftwareApplication `featureList` · şema `logo` → `icon.png` standardizasyonu · GA `preconnect`/`dns-prefetch` · 60 `<img>`'e `width`/`height` (CLS) |
| **Sonra** | "**su kayıp kaçakları**" tam ifadesi görünür metne (ana sayfa title/meta/OG/eyebrow/lede + 25 sayfa footer marka satırı) — domain adının birebir karşılığı |
| **Sonra** | Kayseri bölgesel konumlandırması tamamen kaldırıldı (yerel iniş sayfası + "Kayseri Merkez" projesi silindi, 12→11 proje) · ev/bina içi kaçak ibareleri kaldırıldı (SSS sorusu, rehber maddesi, hizmetler wording) |
| **D** (2026-09-02) | SEOptimer + Rank Math denetimlerine göre: **(G1)** 13 sayfada meta description ≤160 krk'e indirildi (meta + OG + Twitter senkron) · **(G2)** `/llms.txt` eklendi · **(G3)** ölü `google-site-verification` placeholder meta'sı silindi · **(G4)** ana sayfa `Organization` şemasına `founder` (Hasan + Muhammed, `@id`'li — `hakkimizda.html` Person'larıyla eşleşir), `foundingLocation`, `numberOfEmployees` eklendi · **(G5)** `tools/minify.py` + `site.min.css`/`fonts.min.css`/`site.min.js`, 27 HTML + 2 jeneratör `.min`'e repoint (Rank Math "minify" FAIL kapandı) · **(G6)** ~110 satır-içi `style=""` → `site.css` utility sınıfları (1:1, görsel değişiklik yok) · **(G7)** mobil CLS 0.218 / LCP 3.8s: Bricolage başlık fontu `font-display:optional` (başlıkta swap→kayma yok), font preload yanlış subset düzeltildi (`-latin-ext` → asıl gereken `-latin` + `-ext`), GA `gtag.js` `requestIdleCallback` ile kritik yoldan çıkarıldı (27 sayfa) |
| **Bekliyor (kullanıcı)** | SPF + DMARC TXT kayıtları (Cloudflare) · sosyal profiller → açılınca şema `sameAs`'e eklenecek · `iletisim.html` formu hâlâ `formspree.io/f/BURAYA_FORM_ID` placeholder |

## 9. SEO — neden henüz Google'da çıkmıyoruz

- Site **yeni yayında** (~2026-09-01). `site:sukayipkacaklari.com` henüz sonuç vermiyor = **indekslenmedi**.
- **Sıfır backlink, sıfır domain yaşı.** Google rekabetli ticari terimlerde yeni domainleri aylarca temkinli sıralar.
- On-page SEO **tamam** — eksik olan **zaman + off-site sinyaller**, daha fazla kod değil.
- 1. sıradaki AKATED = 20+ yıllık dernek (Altyapı ve Kazısız Teknolojiler Derneği), yüzlerce backlink — kıyaslanabilir rakip değil.
- Gerçekçi beklenti: marka adıyla ("LeakExpert", "sukayipkacaklari") aramalarda 4-8 hafta; "su kayıp kaçakları" gibi rekabetli terimde ilk sayfa 3-6+ ay + birkaç gerçek backlink.

## 10. Yapılacaklar (kullanıcı tarafı)

- [ ] **Google İşletme Profili** — `business.google.com`, Melikgazi/Kayseri adres + telefon (sitedekiyle birebir). Açıklama metni hazır (oturuma bak).
- [ ] **GSC → URL İncele → "Dizine Eklenmesini İste"** — ana sayfa + `/hizmetler.html`, `/platform.html`, `/rehber/`, birkaç proje.
- [ ] **Backlink**: LinkedIn şirket sayfası (siteye link), Kayseri TSO / sektör dizinleri, su kayıp-kaçak forumları (`waterlossforum.org`), ihale/tedarikçi platformları, belediye referanslarından geri link.
- [ ] **Bing Webmaster Tools** — siteyi ekle, sitemap gönder.
- [ ] `index.html`'deki `google-site-verification` meta'sı hâlâ placeholder (GSC başka yöntemle doğrulandığı için sorun değil; istenirse temizlenir).
- [ ] GA4 → Raporlar › Gerçek Zamanlı'dan trafiği izle.
