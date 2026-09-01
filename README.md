# sukayipkacaklari.com — LeakExpert tanıtım sitesi

Saf statik site (HTML + CSS + JS, build adımı yok). Alan adı köküne (`/`)
kurulmalıdır çünkü tüm yollar kök-görelidir (`/assets/...`, `/hizmetler.html`).

**Tema:** açık (beyaz zemin, marka mavisi `#2563eb`). Tek dünya, tek tema.

**Kanonik alan adı:** `https://sukayipkacaklari.com` (www **değil**). `www.` isteği
301 ile köke yönlendirilir. Tüm `<link rel="canonical">`, `og:url`, `sitemap.xml`,
`robots.txt` non-www kullanır.

## Yayın (Coolify)

Canlı: **Coolify** üzerinde `sukayipkacaklari-site` uygulaması (buildpack: `static`,
`nginx:alpine`), GitHub repo `muhammedkoramaz/sukayipkacaklari` → `main` her push'ta
otomatik deploy. Sunucu IP `45.87.120.20`, SSL Let's Encrypt (otomatik).

**nginx yapılandırması repo'daki `nginx.conf` dosyasından DEĞİL**, Coolify
uygulama ayarındaki **`custom_nginx_configuration`** alanından okunur (Coolify bu
içeriği `/etc/nginx/conf.d/default.conf` olarak yazar). Repo'daki `nginx.conf`
sadece referans/yedek kopyadır — değiştirdiğinizde Coolify ayarını da güncelleyin:

```bash
# base64'leyip PATCH:
py - <<'PY'
import json,base64
cfg=open('nginx.conf','rb').read()
open('patch.json','w').write(json.dumps({"custom_nginx_configuration": base64.b64encode(cfg).decode()}))
PY
curl -X PATCH -H "Authorization: Bearer $COOLIFY_API_TOKEN" -H "Content-Type: application/json" \
  --data @patch.json "$COOLIFY_API_URL/api/v1/applications/y7f6p5waot2jz9kvlqwasshh"
curl -X POST -H "Authorization: Bearer $COOLIFY_API_TOKEN" \
  "$COOLIFY_API_URL/api/v1/deploy?uuid=y7f6p5waot2jz9kvlqwasshh&force=true"
```

Bu dosya `http{}`/`events{}` sarmalayıcısı **içermemeli** (conf.d içine dahil
edilir): sadece `server {}` blokları + `gzip`/`add_header` gibi http-bağlamı
direktifleri. Uyguladığı: www→non-www 301, gzip, güvenlik başlıkları
(`X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy`,
`Permissions-Policy`, `Strict-Transport-Security`), `/assets/` için 1 yıl
`immutable` önbellek, `.xml/.txt` için 1 saat, güzel URL (`try_files $uri.html`),
markalı `404.html`.

## Yerelde önizleme

```bash
cd leakexpert-site
python -m http.server 8080
# http://localhost:8080
```

## Sayfa haritası

| Dosya | Sayfa |
|---|---|
| `index.html` | Ana sayfa |
| `platform.html` | Yazılım platformu (mobil + web + API) |
| `hizmetler.html` | Saha hizmetleri + yöntem |
| `projeler/` | Projeler listesi |
| `projeler/*.html` (12 sayfa) | Proje detayları: Kütahya, Batman, Çanakkale, Keşan, Kilis, Sivas, Rize, Doğubayazıt, Fatsa, Kayseri, Bodrum, Mozambik-Beira |
| `referanslar.html` | Referans kurum logoları + proje geçmişi zaman çizelgesi |
| `hakkimizda.html` | Hakkımızda + ekip fotoğrafları + saha galerisi |
| `iletisim.html` | İletişim formu + Melikgazi/Kayseri haritası |
| `sss.html` | 5 SSS (FAQPage zengin içerik) |
| `tesekkurler.html` | Form sonrası teşekkür (noindex) |
| `gizlilik.html` | Gizlilik politikası (KVKK) |
| `404.html` | Bulunamadı sayfası |
| `robots.txt` · `sitemap.xml` · `site.webmanifest` | SEO / PWA |
| `nginx.conf` | Canlı yapılandırmanın referans kopyası (asıl kaynak: Coolify `custom_nginx_configuration`) |
| `.htaccess` · `netlify.toml` | Apache/Netlify'a taşınırsa diye yedek barındırıcı ayarları (canlıda kullanılmıyor) |

## Yayından önce doldurulacaklar

1. **Google Analytics 4** — tüm HTML sayfalarda `G-XXXXXXXXXX` placeholder'ı var.
   GA4 mülkü açıp gerçek ölçüm kimliğiyle değiştirin (tek seferde tüm dosyalar):
   `grep -rl G-XXXXXXXXXX . | xargs sed -i 's/G-XXXXXXXXXX/G-GERCEKID/g'` — ve
   `scratchpad/gen_projects.py` içindeki aynı stringi de güncelleyin.
2. **Google Search Console** — `index.html` içindeki
   `<meta name="google-site-verification" content="BURAYA_...">` satırına doğrulama
   kodunuzu yapıştırın (veya dosya yöntemini kullanın), sonra sitemap'i gönderin:
   `https://sukayipkacaklari.com/sitemap.xml`
2. **İletişim formu** — şu an sunucu tarafı yok; buton bilgileri e-posta uygulamasını
   açar. Kalıcı çözüm için:
   - **Netlify:** hosting Netlify ise form otomatik çalışır (`data-netlify` hazır),
     `iletisim.html` içindeki `action` değerini `/tesekkurler.html` yapın.
   - **Formspree:** formspree.io'da form açın, `iletisim.html` içindeki
     `action="https://formspree.io/f/BURAYA_FORM_ID"` kısmına gerçek ID'yi yazın
     (placeholder değişince JS devre dışı kalır, form doğrudan gönderilir).
3. **Açık adres / harita** — tam adres netleşince `iletisim.html` içindeki
   `iframe src` (Google Haritalar `?q=...&output=embed`) ve JSON-LD `PostalAddress`
   alanını güncelleyin. Şu an: Melikgazi / Kayseri, 7/24.
4. **Ekip fotoğrafı** — `assets/team/muhammed-koramaz.jpg` günlük bir kare; stüdyo
   tarzı bir portre ile değiştirebilirsiniz (aynı ad, kare oran).
5. **Referans logoları** — `assets/brands/` içinde 11 kurum logosu var
   (`leakexpert-web/public/brands`'ten alındı). Yenisini eklemek için PNG koyup
   `index.html` ve `referanslar.html` içindeki `.logos` bloğuna bir `<div><img></div>` ekleyin.
6. **Sosyal paylaşım görseli** — `assets/img/og-cover.png` (1200×630) hazır (açık tema).
   Yeniden üretmek için `assets/img/og.html` şablonunu 1200×630 tarayıcıda açıp ekran görüntüsü alın.

## Marka

- Renkler: `--brand #2563eb` (mobil/web uygulamanın primary'siyle uyumlu),
  başarı/doğrulama `#0e9f6e`, kaçak/kritik vurgusu `#d61f69`. Tümü
  `assets/css/site.css` başındaki değişkenlerde.
- Tipografi: **Bricolage Grotesque** (başlıklar) · **Plus Jakarta Sans** (gövde —
  mobil uygulamanın fontu) · **JetBrains Mono** (ölçüm/telemetri). **Kendi
  sunucumuzda barındırılıyor** (`assets/fonts/*.woff2`, latin + latin-ext alt
  kümeleri, `assets/css/fonts.css`, `font-display:swap`, kritik yüzler preload).
  Google Fonts'a istek yok.
- Logo: gerçek kurumsal kelime markası `assets/img/logo.svg` (header/footer),
  `leakexpert-web/public/logos/logo_black_text.svg`'den.

## Rakamlar (hero + og)

25+ yıl · 43 tamamlanan proje · 1.000+ km akustik dinleme · 70+ kurulan DMA.
Kaynak: `leakexpert-web` `config/siteConfig.ts`. Güncellemek için `index.html`
`hero__meta` bloğu ve `assets/img/og.html`.

## Fotoğraflar

`assets/photos/` — Kilis Belediyesi projesi saha arşivinden seçilmiş 8 kare
(gece dinleme, basınç ölçümü, depo panosu). `assets/team/` — ekip portreleri.
Yenilerini eklerken aynı adla `.jpg` koyup ilgili `<img>` `width`/`height`
değerlerini güncelleyin.
