# sukayipkacaklari.com — LeakExpert tanıtım sitesi

Saf statik site (HTML + CSS + JS, build adımı yok). `leakexpert-site/` klasörünü
olduğu gibi herhangi bir statik barındırıcıya (Netlify, Vercel, Cloudflare Pages,
cPanel / shared hosting, GitHub Pages) yükleyin. Alan adı köküne (`/`) kurulmalıdır
çünkü tüm yollar kök-görelidir (`/assets/...`, `/hizmetler.html`).

**Tema:** açık (beyaz zemin, marka mavisi `#2563eb`). Tek dünya, tek tema.

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
| `.htaccess` · `netlify.toml` | Barındırıcı ayarları (gzip, önbellek, 404) |

## Yayından önce doldurulacaklar

1. **Google Search Console** — `index.html` içindeki
   `<meta name="google-site-verification" content="BURAYA_...">` satırına doğrulama
   kodunuzu yapıştırın (veya dosya yöntemini kullanın), sonra sitemap'i gönderin:
   `https://www.sukayipkacaklari.com/sitemap.xml`
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
  mobil uygulamanın fontu) · **JetBrains Mono** (ölçüm/telemetri). Google Fonts.
- Logo: satır içi damla işareti + "Leak**Expert**" kelime markası (header/footer).
  Uygulamanın vektör logosu `assets/img/logo.svg` olarak da mevcut.

## Rakamlar (hero + og)

25+ yıl · 43 tamamlanan proje · 1.000+ km akustik dinleme · 70+ kurulan DMA.
Kaynak: `leakexpert-web` `config/siteConfig.ts`. Güncellemek için `index.html`
`hero__meta` bloğu ve `assets/img/og.html`.

## Fotoğraflar

`assets/photos/` — Kilis Belediyesi projesi saha arşivinden seçilmiş 8 kare
(gece dinleme, basınç ölçümü, depo panosu). `assets/team/` — ekip portreleri.
Yenilerini eklerken aynı adla `.jpg` koyup ilgili `<img>` `width`/`height`
değerlerini güncelleyin.
