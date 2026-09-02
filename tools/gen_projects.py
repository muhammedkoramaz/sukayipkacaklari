# -*- coding: utf-8 -*-
"""Generate all project detail pages + projeler/index.html for LeakExpert site."""
import os, json, html

SITE = r"C:\Users\muham\Desktop\LEAKEXPERT APPS\leakexpert-site"
BASE = "https://sukayipkacaklari.com"

BRAND_SVG = '<img src="/assets/img/logo.svg" alt="LeakExpert" width="118" height="34" class="brand__logo">'

PHONE_SVG = ('<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">'
  '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.9.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/></svg>')

def header(current):
    def a(href, label):
        cur = ' aria-current="page"' if current == href else ''
        return f'      <a href="{href}"{cur}>{label}</a>'
    nav = "\n".join([
        a("/", "Ana Sayfa"), a("/platform.html", "Platform"), a("/hizmetler.html", "Hizmetler"),
        a("/rehber/", "Rehber"), a("/projeler/", "Projeler"), a("/referanslar.html", "Referanslar"),
        a("/hakkimizda.html", "Hakkımızda"), a("/iletisim.html", "İletişim"),
    ])
    return f'''<header class="hdr">
  <div class="wrap hdr__in">
    <a class="brand" href="/" aria-label="LeakExpert ana sayfa">
      {BRAND_SVG}
    </a>
    <nav class="nav" id="navmenu" aria-label="Ana menü">
{nav}
    </nav>
    <div class="hdr__cta">
      <a class="hdr__phone" href="tel:+905396588434">
        {PHONE_SVG}
        0539 658 84 34
      </a>
    </div>
    <button class="burger" aria-label="Menüyü aç" aria-expanded="false" aria-controls="navmenu">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
    </button>
  </div>
</header>'''

FOOTER = f'''<footer class="ftr">
  <div class="wrap">
    <div class="ftr__grid">
      <div>
        <a class="brand" href="/" aria-label="LeakExpert ana sayfa">
          {BRAND_SVG}
        </a>
        <p class="ftr__brandline">Belediye içme suyu şebekelerinde su kayıp kaçakları tespiti, debi/basınç izleme ve saha yönetimi. Web ve mobil entegre platform.</p>
      </div>
      <div><h4>Platform</h4><ul>
        <li><a href="/platform.html#mobil">Mobil saha uygulaması</a></li>
        <li><a href="/platform.html#web">Web yönetim paneli</a></li>
        <li><a href="/platform.html#api">API &amp; entegrasyon</a></li>
        <li><a href="/hizmetler.html">Saha hizmetleri</a></li>
      </ul></div>
      <div><h4>Kurumsal</h4><ul>
        <li><a href="/hakkimizda.html">Hakkımızda</a></li>
        <li><a href="/projeler/">Projeler</a></li><li><a href="/referanslar.html">Referanslar</a></li>
        <li><a href="/rehber/">Rehber</a></li>
        <li><a href="/sss.html">Sık sorulan sorular</a></li>
        <li><a href="/iletisim.html">İletişim</a></li>
        <li><a href="/gizlilik.html">Gizlilik politikası</a></li>
      </ul></div>
      <div><h4>İletişim</h4><ul>
        <li class="ftr__mono">Melikgazi / Kayseri</li>
        <li class="ftr__mono"><a href="tel:+905396588434">+90 539 658 84 34</a></li>
        <li class="ftr__mono"><a href="mailto:sukayipkacaklari@gmail.com">sukayipkacaklari@gmail.com</a></li>
      </ul></div>
    </div>
    <div class="ftr__bottom">
      <span>© 2026 LeakExpert · Tüm hakları saklıdır.</span>
      <span>sukayipkacaklari.com</span>
    </div>
  </div>
</footer>

<nav class="dock" aria-label="Hızlı iletişim">
  <a class="btn btn--ghost btn--sm" href="/iletisim.html">Görüşme talebi</a>
  <a class="btn btn--sm" href="tel:+905396588434">
    {PHONE_SVG}
    0539 658 84 34
  </a>
</nav>

<script src="/assets/js/site.min.js" defer></script>
</body>
</html>'''

FONTS = (
'<link rel="preload" as="font" type="font/woff2" href="/assets/fonts/bricolage-grotesque-600-800-latin.woff2" crossorigin>\n'
'<link rel="preload" as="font" type="font/woff2" href="/assets/fonts/bricolage-grotesque-600-800-latin-ext.woff2" crossorigin>\n'
'<link rel="preload" as="font" type="font/woff2" href="/assets/fonts/plus-jakarta-sans-400-latin.woff2" crossorigin>\n'
'<link rel="stylesheet" href="/assets/css/fonts.min.css">'
)

def page_head(title, desc, canon, ogtype, extra_ld):
    return f'''<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{html.escape(desc, quote=True)}">
<link rel="canonical" href="{canon}">
<link rel="alternate" hreflang="tr" href="{canon}">
<link rel="alternate" hreflang="x-default" href="{canon}">
<meta name="theme-color" content="#ffffff">
<meta property="og:type" content="{ogtype}">
<meta property="og:site_name" content="LeakExpert">
<meta property="og:locale" content="tr_TR">
<meta property="og:title" content="{html.escape(title, quote=True)}">
<meta property="og:description" content="{html.escape(desc, quote=True)}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{BASE}/assets/img/og-cover.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{BASE}/assets/img/og-cover.png">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" href="/assets/img/icon.png">
<link rel="apple-touch-icon" href="/assets/icons/app-icon.png">
<link rel="manifest" href="/site.webmanifest">
{FONTS}
<link rel="stylesheet" href="/assets/css/site.min.css">
{extra_ld}
<!-- Google Analytics 4 — gtag.js kritik yoldan çıkarıldı, boşta yüklenir -->
<link rel="dns-prefetch" href="https://www.googletagmanager.com">
<link rel="dns-prefetch" href="https://www.google-analytics.com">
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-ETN61F721R',{{anonymize_ip:true}});(function(){{function l(){{var s=document.createElement('script');s.async=1;s.src='https://www.googletagmanager.com/gtag/js?id=G-ETN61F721R';document.head.appendChild(s);}}if('requestIdleCallback'in window){{requestIdleCallback(l,{{timeout:3000}});}}else{{window.addEventListener('load',function(){{setTimeout(l,1200);}});}}}})();</script>
</head>
<body>
<a class="skip" href="#main">İçeriğe geç</a>
'''

# ---------------------------------------------------------------- project data
P = [
 dict(slug="kutahya", name="Kütahya Belediyesi", kicker="Proje · Kütahya Belediyesi · İç Ege · 2024–2025",
   h1="Şebeke &ldquo;kritik&rdquo; bantta: 348,5 km&#39;de 432 arıza.",
   lede="Su ve Kanalizasyon Müdürlüğü ile yürütülen akustik kaçak tespiti hizmetinde, başlangıç ihalesindeki 300 km dinlendikten sonra bulunan yoğunluk uluslararası eşiklerin çok üzerine çıktı; kapsam genişletildi ve bulgular doğrulandı.",
   desc="Kütahya içme suyu şebekesinde akustik kaçak tespiti: 348,5 km hat dinlendi, 432 arıza bulundu. Yoğunluk 1,34 arıza/km/yıl — AB eşiğinin yaklaşık üç katı.",
   spec=[("Başlangıç kapsamı · dinlenen hat","300","km",0),
         ("Başlangıç kapsamı · tespit edilen kaçak/arıza","403","adet",1),
         ("İhale artışı · ilave dinleme","48,5","km",0),
         ("İhale artışı · ilave arıza","29","adet",0),
         ("Toplam dinlenen hat","348,5","km",0),
         ("Toplam tespit edilen arıza","432","adet",1),
         ("Arıza yoğunluğu","1,34","arıza/km/yıl",1)],
   prose=[("Uluslararası eşiklerle karşılaştırma",
     ["<p>Akustik tespit performansı genellikle <strong>yıllık km başına arıza sayısı</strong> ile değerlendirilir. Kütahya&#39;da başlangıç çalışmasında elde edilen <strong>1,34 arıza/km/yıl</strong>:</p>",
      "<ul><li>AB Direktifi 2020/2184 kabul sınırının (~0,50) yaklaşık <strong>3 katı</strong>,</li><li>AWWA Kuzey Amerika ortalamasının (~0,09) yaklaşık <strong>on katı</strong>,</li><li>akademik çalışmalarda &ldquo;rehabilitasyon gerektiren&rdquo; olarak tanımlanan 1,0–4,0 bandında.</li></ul>"]),
     ("Genişleme kararı ve doğrulama",
     ["<p>Yüksek yoğunluk, arızaların rastlantısal değil <strong>sistematik</strong> olduğunu gösteriyordu. 4734 sayılı Kanun kapsamında yapılan 48,5 km&#39;lik ilave dinlemede 29 arıza daha bulunması, başlangıç değerlendirmesini doğruladı.</p>"]),
     ("Neden erken tespit",
     ["<p>Akustik tespit, arızaların büyük çoğunluğunu <strong>zemin kırımı öncesinde</strong> yakalar; ani patlama riskini, acil ekip maliyetini ve yüzey onarım masrafını düşürür.</p>"])],
   photos=[("kutahya/1.jpg","Akustik korelasyon · iki temas noktası arasında konum tespiti"),
           ("kutahya/2.jpg","Şebeke hattı taraması")],
   note="Kaynak: Akustik Kaçak Tespiti Hizmeti gerekçe raporu ve saha kayıt tabloları. Karşılaştırma değerleri hakemli yayın ve kurum belgelerine dayanır (AWWA 2018; AB Direktifi 2020/2184; MDPI Water 2023).",
   concl=("Sistematik tarama zorunlu.","Bulgular, şebekenin genel hatlarıyla ciddi bir bozulma sürecinde olduğunu ve düzenli, planlı bir akustik tarama programının gerekli olduğunu ortaya koydu. Tespit edilen her arıza acil onarım önceliğiyle belediyeye iletildi.")),

 dict(slug="batman", name="Batman Belediyesi", kicker="Proje · Batman Belediyesi · Güneydoğu Anadolu · 2 fazlı proje",
   h1="400 km tarama, 220 sızıntı noktası tespiti.",
   lede="Batman Belediyesi BASKİ Müdürlüğü ile iki fazlı yürütülen çalışmada; şehir genelinde toplam 400 km içme suyu hattı gece ve gündüz akustik dinlemeyle tarandı, görünmeyen fiziki kaçaklar koordinatıyla tespit edildi. Debi/basınç ölçümü, su dengesi raporu ve CBS haritalama dahil.",
   desc="Batman içme suyu şebekesinde 2 fazlı akustik kayıp-kaçak çalışması: 400 km hat gece ve gündüz dinlendi, 220 sızıntı noktası koordinatıyla tespit edildi.",
   spec=[("Akustik dinlenen hat (1. + 2. faz)","400","km",1),
         ("Tespit edilen sızıntı noktası","220","adet",1),
         ("Çamlıca 1 depo · tahmini fiziki kaçak","~68","m³/saat",0),
         ("Gece min. debinin fiziki kayıp payı","~%70","",0),
         ("Örnek: yan yana iki arıza · kayıp debisi","8","L/sn",1)],
   prose=[("Çalışmanın kapsamı",
     ["<p>İki faz halinde, şehir genelinde toplam <strong>400 km</strong> içme suyu hattı gece ve gündüz akustik dinlemeyle tarandı.</p>",
      "<ul><li>Depo çıkışlarına debi ve basınç ölçüm sistemi kurulumu,</li><li>kaybın yoğun olduğu bölgelerde nokta nokta akustik dinleme ve korelasyon,</li><li>tespit edilen 220 noktanın koordinat, akustik ses seviyesi ve fotoğrafla raporlanıp belediyeye onarım önceliğiyle iletilmesi,</li><li>IWA su dengesi raporu ve tüm noktaların CBS haritalaması.</li></ul>"]),
     ("Örnek: yan yana iki büyük arıza",
     ["<p>Sahada yan yana bulunan yalnızca <strong>iki</strong> arıza noktası tek başına <strong>8 L/sn</strong> kayba karşılık geliyordu: yılda ≈ 252.288 m³ su, ≈ 2,77 milyon ₺ gelir ve ≈ 882.000 ₺ enerji kaybı. Bu iki arızanın en az 20 yıldır sürdüğü tahminiyle kümülatif etki <strong>10 milyon m³</strong> ve <strong>111 milyon ₺</strong> düzeyindedir.</p>",
      "<p>Tespit edilen 220 noktanın her biri, büyüklüğü değişmekle birlikte benzer bir kayıp taşır.</p>"]),
     ("Hidrolik iyileşme",
     ["<p>Onarılan kritik noktalarda şebeke basıncı dengelendi, dalgalanmalar azaldı ve arızaların zincirleme etkisi düştü. Debi verilerinde genel tüketim gerilemesi gözlendi. Çalışmanın sürdürülmesiyle su kaybı oranının %30&#39;lar seviyesine inmesi beklenmektedir.</p>"])],
   photos=[("batman/1.jpg","Vana odası · ana hat üzerinde basınç loggerı"),
           ("batman/2.jpg","Vana odası çalışması")],
   note="Rakamlar Batman İş Teslim Sunumu (2026) ve su dengesi raporlarından derlenmiştir. Ekonomik büyüklükler ≈ 11 TL/m³ birim maliyet ve tarife varsayımıyla hesaplanmıştır; kurum verisiyle doğrulanır.",
   concl=("Ölçek, tek tek arızaların toplamıdır.","400 km&#39;de bulunan 220 sızıntı, şebeke genelinde sistemli bir bozulmaya işaret eder. Görünmeyen kayıp, şikâyet beklendiğinde büyür; aktif ve planlı dinleme onu büyümeden yakalar.")),

 dict(slug="canakkale", name="Çanakkale Belediyesi", kicker="Proje · Çanakkale Belediyesi · Marmara · 2026 · pilot",
   h1="4 gecede 35,5 km, 22 kaçak — ve yükselen bir öğrenme eğrisi.",
   lede="Merkez içme suyu şebekesinde İsmetpaşa, Cevat Paşa, Namık Kemal, M. Kemal ve Fevzipaşa mahallelerinin bir bölümünde yürütülen gece akustik dinleme pilotu.",
   desc="Çanakkale merkez içme suyu şebekesinde 4 gecelik gece akustik dinleme pilotu: 35.465 m hat, 187 kayıt, 94 sokak, 22 fiziki kaçak. Tespit/gece her gece arttı.",
   spec=[("Dinlenen hat (4 gece)","35.465","m",0),
         ("Ayrı akustik kayıt","187","adet",0),
         ("Dinlenen farklı sokak / cadde","94","adet",0),
         ("Tespit edilen fiziki su kaçağı","22","adet",1),
         ("Kaçak yoğunluğu","~0,62","kaçak/km",0),
         ("Günlük tespit artışı (4 → 7)","+%75","",1)],
   prose=[("Günlük dağılım",
     ["<ul><li>10.06 · 10.116 m dinleme, 50 kayıt, <strong>4 kaçak</strong></li><li>11.06 · 7.133 m dinleme, 39 kayıt, <strong>5 kaçak</strong></li><li>12.06 · 11.069 m dinleme, 60 kayıt, <strong>6 kaçak</strong></li><li>13.06 · 7.146 m dinleme, 38 kayıt, <strong>7 kaçak</strong></li></ul>"]),
     ("Neden önemli",
     ["<p>Tespit sayısı, düşük metrajlı gecelerde bile <strong>azalmadı, arttı</strong>. Bu, sahanın doygunluğa ulaşmadığını; ekip şebeke ve saha davranışını öğrendikçe verimin yükseldiğini gösterir. Çalışma durdurulursa bu öğrenme eğrisi ve saha bilgisi kaybolur.</p>"]),
     ("Ekonomik büyüklük (tahmini)",
     ["<p>Yalnızca bu 4 gecede bulunan 22 kaçak onarılmazsa, kaçak başına 0,10–0,25 L/sn varsayımıyla yıllık kayıp yaklaşık <strong>69.000–173.000 m³</strong> mertebesindedir; 20 TL/m³ ile yılda <strong>1,4–3,5 milyon TL</strong> önlenebilir kayba karşılık gelir.</p>"])],
   photos=[("canakkale/1.jpg","Gece vardiyası · nokta nokta dinleme"),
           ("canakkale/2.jpg","Gündüz doğrulama dinlemesi")],
   note="Kaynak: 10–13.06.2026 Günlük Çalışma Raporları, dinleme kayıt tablosu ve 22 adet Arıza Tespit Raporu. Ekonomik rakamlar tahminidir, kurum verisiyle doğrulanır. Görseller yöntemi temsil eder.",
   concl=("Faz 2: kesintisiz devam.","Taranmamış mahalleler ve tespitin yoğun olduğu bölgelerde doğrulama dinlemesi; tespit → 48–72 saat içinde onarım → onarım sonrası kontrol. Tespit hızı korunursa 60 iş gecesinde yaklaşık 330 kaçak tespit potansiyeli bulunur.")),

 dict(slug="kesan", name="Keşan Belediyesi", kicker="Proje · Kırklareli · Keşan Belediyesi · Trakya · 2026 · pilot",
   h1="Altı gecede 56,8 km, 20 kaçak.",
   lede="Keşan içme suyu şebekesinde yüzeye çıkmayan fiziki su kaçaklarının akustik dinleme yöntemiyle tespiti için yürütülen pilot uygulama; 7 mahallede 301 sokak/cadde kesiminde ölçüm.",
   desc="Keşan içme suyu şebekesinde 6 gecelik akustik dinleme pilotu: 56,8 km hat, 20 fiziki kaçak, 7 mahalle. Ortalama her 2,8 km hatta bir kaçak.",
   spec=[("Dinlenen hat (6 gece)","56,8","km",0),
         ("Tespit edilen fiziki su kaçağı","20","adet",1),
         ("Taranan mahalle","7","adet",0),
         ("Kaçak sıklığı","1 / 2,8","km",0),
         ("Gece başına ortalama tespit","~3,3","kaçak",1)],
   prose=[("Bulgular",
     ["<p>Kaçaklar mahalleye göre: Yukarı Zaferiye 11, Aşağı Zaferiye 4, İspat Cami 3, Cumhuriyet 1, Büyük Cami 1. Ağırlıkla <strong>eski/zayıf altyapı hatlarında</strong> ve abone bağlantı noktalarında yoğunlaşıyor; sorun yapısaldır.</p>",
      "<p>01.08 ve 03.08 gecelerinde kaçak bulunmaması, o bölgelerin görece sağlıklı olduğunu ve kaynakların gerçek sorun bölgelerine yönlendirilebileceğini gösterir.</p>"]),
     ("Mali etki (varsayımlarla)",
     ["<p>Yalnızca bu 20 kaçağın onarılmaması hâlinde; kaçak başına 0,45–1,00 m³/saat ve 8.760 saat/yıl ile yıllık kayıp <strong>≈ 79.000–175.000 m³</strong>. 12 TL/m³ maliyet ve 30 TL/m³ tarife değeriyle yılda milyonlarca TL. Kesin değerler DMA gece minimum debi ölçümüyle netleştirilir.</p>"]),
     ("Öneri",
     ["<p>Şehrin büyük kısmı taranmadı. Ölçülen yoğunluk şehir geneline uygulandığında <strong>yüzlerce tespit edilebilir kaçak</strong> beklenir. Gerekli döngü: Tespit → Onarım → Doğrulama → Raporlama.</p>"])],
   photos=[("kesan/1.jpg","Gece akustik dinleme (yöntemi temsil eder)"),
           ("kesan/2.jpg","DMA tasarımı ve ölçüm planı")],
   note="Kaynak: 29.07–03.08.2026 Günlük Çalışma Raporları ve 20 adet Arıza Tespit Raporu. Görseller yöntemi temsil eder.",
   concl=("Kaçak azaltma süreklilik işidir.","Şebekede sürekli yeni kaçaklar oluşur; düzenli tarama olmadan kayıp oranı 1–2 yıl içinde eski seviyesine döner. Kalıcı ekip ve DMA bazlı izleme gereklidir.")),

 dict(slug="kilis", name="Kilis Belediyesi", kicker="Proje · Kilis Belediyesi · Güneydoğu Anadolu · 2023–2024",
   h1="Basınç, step ve sıfır basınç testleriyle kaybın haritası.",
   lede="Kilis içme suyu şebekesinde kayıp-kaçak tespiti; basınç veri loggerı kurulumu, sıfır basınç ve step testleri, akustik dinleme ve tahakkuk analizi. Çalışma altı ay sürdü.",
   desc="Kilis Belediyesi su şebekesinde kayıp-kaçak tespiti: basınç loggerları, sıfır basınç ve step testleri, akustik dinleme, CBS haritalama (2023–2024).",
   spec=[("Çalışma süresi","6","ay",0),
         ("Basınç izleme","7/24","logger",0),
         ("Test yöntemi","Step + sıfır basınç","",1),
         ("Basınç ölçer","1–30 bar data loggerı","",0)],
   prose=[("Yöntem",
     ["<p>Kritik noktalara <strong>basınç veri loggerları</strong> yerleştirilerek 7/24 basınç takibi yapıldı. <strong>Step testi</strong> ile hat hat kapatma yapılarak kaybın hangi segmentte yoğunlaştığı daraltıldı; <strong>sıfır basınç testi</strong> ile izole bölgelerin sızdırmazlığı ölçüldü.</p>"]),
     ("Akustik dinleme",
     ["<p>Daraltılan bölgelerde gece akustik dinleme ve korelasyonla kaçak noktaları metrik hassasiyetle bulundu; her nokta GPS koordinatı, ses seviyesi ve fotoğrafla kayıt altına alındı.</p>"]),
     ("Tahakkuk analizi",
     ["<p>Abone tüketim kayıtları incelenerek <strong>idari kayıp</strong> (sayaç hatası, kaçak kullanım, faturalama) kalemleri ayrıştırıldı ve fiziki kayıptan bağımsız olarak raporlandı.</p>"])],
   photos=[("kilis-1.jpg","Kilis · gece · trafik güvenliğiyle akustik tarama"),
           ("kilis-2.jpg","Abone noktasında basınç ölçümü"),
           ("kilis-3.jpg","Depo çıkışı veri toplama panosu")],
   note="Görseller Kilis Belediyesi projesi saha arşivinden.",
   concl=("Fiziki ve idari kayıp ayrı ayrı ölçülür.","Basınç ve debi verisi kaybın nerede olduğunu; tahakkuk analizi ise kaybın türünü gösterir. İkisi birlikte, doğru müdahale önceliğini verir.")),

 dict(slug="sivas", name="Sivas Belediyesi", kicker="Proje · Sivas Belediyesi · İç Anadolu · 2021",
   h1="12 DMA bölgesi, %55&#39;ten %25&#39;e kayıp oranı.",
   lede="Sivas merkez ilçede su kayıplarının azaltılması amacıyla İzole Ölçüm Bölgesi (DMA) kurulumu ve merkezi izleme sistemi devreye alındı.",
   desc="Sivas merkez ilçede 12 adet DMA (İzole Ölçüm Bölgesi) kurulumu ve su kayıp yönetim sistemi. Su kayıp oranı %55'ten %25'e düşürüldü.",
   spec=[("Kurulan DMA bölgesi","12","adet",1),
         ("Başlangıç kayıp oranı","%55","",0),
         ("Hedef / ulaşılan kayıp oranı","%25","",1),
         ("İzleme","7/24","uzaktan",0)],
   prose=[("Zorluk",
     ["<p>Şehir genelinde su kayıp oranı %55&#39;in üzerindeydi ve bölgesel izleme altyapısı bulunmuyordu; kaybın nerede oluştuğu bilinemiyordu.</p>"]),
     ("Çözüm",
     ["<p>12 adet DMA bölgesi tasarlanarak kuruldu. Her bölgeye <strong>debi ve basınç ölçüm cihazları</strong> yerleştirildi. Merkezi izleme sistemi ile gece minimum debi takibi ve anomali uyarısı sağlandı.</p>"]),
     ("Sonuçlar",
     ["<ul><li>12 adet DMA bölgesi kuruldu,</li><li>su kayıp oranı %55&#39;ten <strong>%25&#39;e</strong> düşürüldü,</li><li>7/24 uzaktan izleme devreye alındı,</li><li>bölge bazlı müdahale ile onarım öncelikleri netleşti.</li></ul>"])],
   photos=[("sivas/2.jpg","Gündüz akustik dinleme çalışması"),
           ("sivas/3.jpg","Tespit edilen kaçağın kazıyla doğrulanması")],
   note="Proje özeti; kesin oranlar idarenin su dengesi kayıtlarıyla doğrulanır.",
   concl=("DMA, kaybı görünür kılar.","İzole ölçüm bölgeleri olmadan kayıp yalnızca tahmin edilir. DMA ile her bölgenin gece debisi ölçülür; müdahale, en çok kaçıran bölgeden başlar.")),

 dict(slug="rize", name="Rize Belediyesi", kicker="Proje · Rize Belediyesi · Doğu Karadeniz · 2021",
   h1="Yağışlı iklimde, zorlu zeminde akustik tespit.",
   lede="Rize içme suyu şebekesinde akustik dinleme ve korelasyon yöntemiyle kayıp-kaçak tespiti; eğimli arazi ve yüksek zemin nemi koşullarında yürütülen saha çalışması.",
   desc="Rize Belediyesi içme suyu şebekesinde akustik dinleme ve korelasyonla kayıp-kaçak tespiti (2021). Eğimli arazi ve yüksek nem koşullarında saha çalışması.",
   spec=[("Yöntem","Akustik + korelasyon","",1),
         ("Saha koşulu","Eğimli arazi · yüksek nem","",0),
         ("Kayıt","GPS + ses seviyesi + foto","",0)],
   prose=[("Saha koşulları",
     ["<p>Rize&#39;nin dik topografyası ve yüksek yağış rejimi, akustik dinlemeyi zorlaştıran koşullardır: zemin nemi sesi taşır ve yanıltıcı sinyaller üretebilir. Bu nedenle her şüpheli nokta <strong>korelatörle</strong> iki temas noktası arasında doğrulandı.</p>"]),
     ("Sonuç",
     ["<p>Tespit edilen kaçaklar koordinat ve fotoğrafla belediyeye iletildi; onarım ekipleri için öncelik sırası çıkarıldı.</p>"])],
   photos=[("rize/1.jpg","Yer mikrofonuyla nokta dinleme"),
           ("rize/3.jpg","Eğimli hat üzerinde tarama"),
           ("rize/2.jpg","Rögar kontrolü")],
   note="Görseller Rize Belediyesi projesi saha arşivinden (2021).",
   concl=("Zorlu zemin, daha çok doğrulama demektir.","Nemli ve eğimli sahada tek başına dinleme yeterli olmaz; korelasyon ve tekrar ölçüm, yanlış kazıyı önler.")),

 dict(slug="dogubayazit", name="Doğubayazıt Belediyesi", kicker="Proje · Ağrı · Doğubayazıt Belediyesi · Doğu Anadolu · 2022",
   h1="DMA bazlı kayıp azaltım çalışması.",
   lede="Doğubayazıt içme suyu şebekesinde izole ölçüm bölgesi yaklaşımıyla kayıp-kaçak tespiti ve azaltımı; debi ölçümü, akustik dinleme ve onarım takibi.",
   desc="Doğubayazıt Belediyesi içme suyu şebekesinde DMA bazlı kayıp-kaçak azaltım çalışması (2022): debi ölçümü, akustik dinleme ve onarım takibi.",
   spec=[("Yaklaşım","DMA bazlı","",1),
         ("Ölçüm","Debi + akustik","",0),
         ("Döngü","Tespit → onarım → doğrulama","",0)],
   prose=[("Çalışma",
     ["<p>Şebeke, ölçülebilir bölgelere ayrıldı; her bölgenin gece minimum debisi izlenerek kaybın yoğun olduğu hatlar belirlendi. Ardından bu hatlarda akustik dinlemeyle kaçak noktaları tespit edildi.</p>"]),
     ("Onarım takibi",
     ["<p>Tespitler belediye onarım ekiplerine iletildi; onarım sonrası kontrol dinlemesiyle döngü kapatıldı.</p>"])],
   photos=[("dogubayazit/2.jpg","Kazı noktasında hat kontrolü"),
           ("dogubayazit/1.jpg","Şebeke güzergâhı taraması")],
   note="Proje özeti; görseller saha arşivinden (2022).",
   concl=("Bölge bölge, ölçerek ilerlemek.","Şehir genelini tek seferde taramak yerine, en çok kaçıran bölgeden başlayıp doğrulayarak ilerlemek kaynakları verimli kullanır.")),

 dict(slug="ordu-fatsa", name="Ordu · Fatsa Belediyesi", kicker="Proje · Ordu · Fatsa Belediyesi · Karadeniz · 2021",
   h1="Tespitten kazıya, kapalı döngü saha çalışması.",
   lede="Fatsa içme suyu şebekesinde akustik dinleme ile kayıp-kaçak tespiti ve tespit edilen noktaların kazı ile doğrulanması; sonbahar dönemi saha çalışması.",
   desc="Ordu — Fatsa Belediyesi içme suyu şebekesinde akustik kayıp-kaçak tespiti ve kazıyla doğrulama (2021).",
   spec=[("Yöntem","Akustik dinleme + korelasyon","",1),
         ("Doğrulama","Kazı ile nokta teyidi","",0),
         ("Kayıt","Koordinat + foto + ses seviyesi","",0)],
   prose=[("Çalışma",
     ["<p>Şüpheli hatlar gece ve gündüz dinlendi; korelasyonla daraltılan noktalar işaretlendi. Tespit edilen her nokta, onarım aşamasında <strong>kazı ile doğrulandı</strong> ve kaçağın konumu teyit edildi.</p>"]),
     ("Sonuç",
     ["<p>Doğrulanan noktalar belediye ekiplerince onarıldı; koordinatlı arıza kayıtları CBS ortamına işlendi.</p>"])],
   photos=[("ordu-fatsa/1.jpg","Tespit noktasında kazı"),
           ("ordu-fatsa/2.jpg","Exposed hat üzerinde kontrol"),
           ("ordu-fatsa/3.jpg","Hat onarımı öncesi hazırlık")],
   note="Görseller Fatsa projesi saha arşivinden (2021).",
   concl=("Tespit, kazıyla tamamlanır.","Akustik nokta ne kadar iyi olsa da döngü, onarım ve onarım sonrası kontrol dinlemesiyle kapanır.")),


 dict(slug="bodrum", name="Bodrum", kicker="Proje · Muğla · Bodrum · Ege · 2024",
   h1="Basınç yönetimiyle boru patlaklarında %70 azalma.",
   lede="Bodrum içme suyu şebekesinde yüksek basınç kaynaklı patlakların önlenmesi için basınç yönetim sistemi kuruldu; rakım farklarından doğan basınç dengesizlikleri giderildi.",
   desc="Bodrum içme suyu şebekesinde basınç yönetim sistemi kurulumu: PRV ve basınç kırıcı vanalarla boru patlak sayısı %70 azaldı, enerji maliyetlerinde %30 tasarruf.",
   spec=[("Boru patlak sayısı","%70","azaldı",1),
         ("Enerji maliyeti","%30","tasarruf",1),
         ("Kurulan sistem","PRV + basınç kırıcı vana","",0),
         ("İzleme","Merkezi basınç takibi","",0)],
   prose=[("Zorluk",
     ["<p>Yüksek rakım farkları nedeniyle şebekede basınç dengesizlikleri yaşanıyordu; gece saatlerinde aşırı basınç boru patlaklarına neden oluyordu.</p>"]),
     ("Çözüm",
     ["<p>Basınç kırıcı vanalar ve <strong>PRV (Pressure Reducing Valve)</strong> sistemleri kuruldu. Basınç izleme noktaları oluşturularak merkezi takip devreye alındı; gece basıncı optimize edildi.</p>"]),
     ("Sonuçlar",
     ["<ul><li>Boru patlak sayısı <strong>%70</strong> azaldı,</li><li>gece basınç optimizasyonu sağlandı,</li><li>şebeke ömrü uzatıldı,</li><li>enerji maliyetlerinde <strong>%30</strong> tasarruf sağlandı.</li></ul>"])],
   photos=[("bodrum/1.jpg","Abone noktasında basınç ölçümü"),
           ("bodrum/2.jpg","DMA / basınç bölgesi planlaması")],
   note="Proje özeti; kesin değerler idarenin işletme kayıtlarıyla doğrulanır.",
   concl=("Basıncı yönetmek, kaybı ve patlağı birlikte düşürür.","Fazla basınç hem kaçak debisini hem de yeni patlak riskini artırır. Basınç yönetimi, en düşük maliyetli kayıp azaltma yöntemlerinden biridir.")),

 dict(slug="mozambik", name="Mozambik · Beira", kicker="Proje · Mozambik · Beira · Uluslararası · 2024",
   h1="Yurt dışında: Beira su kaçakları tespit çalışması.",
   lede="Mozambik&#39;in Beira kentinde içme suyu şebekesinde su kaçaklarının tespitine yönelik saha çalışması; sıcak iklim ve farklı altyapı koşullarında akustik yöntemin uygulanması.",
   desc="Mozambik — Beira içme suyu şebekesinde su kaçakları tespit çalışması. LeakExpert'in yurt dışı saha deneyimi.",
   spec=[("Ülke","Mozambik","",1),
         ("Kent","Beira","",0),
         ("Yöntem","Akustik dinleme + debi ölçümü","",0)],
   prose=[("Çalışma",
     ["<p>Beira şebekesinde şüpheli bölgeler akustik dinleme ve debi ölçümüyle tarandı; yerel ekiple birlikte çalışılarak tespit ve kayıt yöntemi aktarıldı.</p>"]),
     ("Neden önemli",
     ["<p>Su kaybı yönetimi evrensel bir mühendislik problemidir; yöntem ve ekipman, farklı iklim ve altyapı koşullarına uyarlanabilir.</p>"])],
   photos=[("mozambik/1.jpg","İçme suyu altyapısı")],
   note="Görseller çalışmayı temsil eder.",
   concl=("Yöntem sınır tanımaz.","IWA su dengesi, akustik tespit ve DMA yaklaşımı; Türkiye&#39;de olduğu gibi yurt dışında da uygulanabilir.")),
]

ORDER = [p["slug"] for p in P]

def spec_html(rows):
    out = ['      <dl class="spec">']
    for label, val, unit, hi in rows:
        u = f'<span class="u">{unit}</span>' if unit else ''
        cls = ' spec__row--hi' if hi else ''
        out.append(f'        <div class="spec__row{cls}"><dt>{label}</dt><dd>{val}{u}</dd></div>')
    out.append('      </dl>')
    return "\n".join(out)

def render(i, p):
    slug = p["slug"]; canon = f"{BASE}/projeler/{slug}.html"
    title = f'{p["name"]} — {p["h1"].split(":")[0].replace("&ldquo;","").replace("&rdquo;","").replace("&#39;","’")[:52].strip()} | LeakExpert'
    # simpler stable title
    title = f'{p["name"]} Su Kaçağı Tespiti Projesi | LeakExpert'
    nextp = P[(i + 1) % len(P)]
    rel3 = [P[(i + k) % len(P)] for k in (1, 2, 3)]
    import re as _re
    _ym = _re.search(r"(20\d{2})", p["kicker"])
    _year = _ym.group(1) if _ym else "2024"
    _head = (p["h1"].replace('&ldquo;', '').replace('&rdquo;', '').replace('&#39;', '’')
             .replace('&nbsp;', ' ').replace('"', "'"))
    _desc = p["desc"].replace('"', "'")
    _imgs = ",".join(f'"{BASE}/assets/projects/{src.replace(".jpg", ".webp")}"'
                     for src, _ in p["photos"])
    ld = f'''<script type="application/ld+json">
{{ "@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
 {{"@type":"ListItem","position":1,"name":"Ana Sayfa","item":"{BASE}/"}},
 {{"@type":"ListItem","position":2,"name":"Projeler","item":"{BASE}/projeler/"}},
 {{"@type":"ListItem","position":3,"name":"{p["name"]}","item":"{canon}"}} ]}}
</script>
<script type="application/ld+json">
{{ "@context":"https://schema.org","@type":"Article",
"headline":"{p["name"]} — {_head}",
"description":"{_desc}",
"inLanguage":"tr-TR","articleSection":"Projeler",
"mainEntityOfPage":{{"@type":"WebPage","@id":"{canon}"}},
"isPartOf":{{"@type":"CollectionPage","@id":"{BASE}/projeler/"}},
"about":{{"@type":"Thing","name":"Su kayıp-kaçak tespiti"}},
"datePublished":"{_year}-01-01","dateModified":"2026-09-01",
"author":{{"@type":"Organization","name":"LeakExpert","url":"{BASE}/"}},
"publisher":{{"@type":"Organization","name":"LeakExpert","url":"{BASE}/","logo":{{"@type":"ImageObject","url":"{BASE}/assets/img/icon.png"}}}},
"image":[{_imgs}]}}
</script>'''

    figs = []
    for j, (src, cap) in enumerate(p["photos"]):
        cls = "figure figure--wide" if j == 0 else "figure figure--wide"
        figs.append(f'''        <div class="{cls}{' rv' if j==0 else ' rv rv-2'}">
          <img src="/assets/projects/{src.replace(".jpg",".webp")}" alt="{cap}" loading="lazy" decoding="async">
          <span class="figure__tag">{cap}</span>
        </div>''')
    fig_block = "\n".join(figs)

    prose_html = []
    for h2, paras in p["prose"]:
        prose_html.append(f'          <h2>{h2}</h2>')
        prose_html.extend('          ' + para for para in paras)
    prose_html = "\n".join(prose_html)

    r0, r1, r2 = ({"slug": x["slug"], "name": x["name"], "meta": x["kicker"].replace("Proje · ", "")} for x in rel3)
    body = f'''{header("/projeler/")}

<main id="main">
  <div class="wrap">
    <nav class="crumb" aria-label="Sayfa işaret yolu">
      <a href="/">Ana Sayfa</a><span class="sep">/</span>
      <a href="/projeler/">Projeler</a><span class="sep">/</span>
      <span aria-current="page">{p["name"]}</span>
    </nav>
  </div>

  <article>
  <section class="phead">
    <div class="wrap">
      <p class="eyebrow">{p["kicker"]}</p>
      <h1>{p["h1"]}</h1>
      <p class="lede">{p["lede"]}</p>
    </div>
  </section>

  <section class="section section--tight">
    <div class="wrap">
{spec_html(p["spec"])}
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="split split--top">
        <div class="prose rv">
{prose_html}
        </div>
        <div class="rv rv-2 grid-14">
{fig_block}
          <p class="muted mono fs-74">{p["note"]}</p>
        </div>
      </div>
    </div>
  </section>

  <section class="section section--panel">
    <div class="wrap">
      <p class="eyebrow eyebrow--ok rv">Sonuç</p>
      <h2 class="h-sec rv">{p["concl"][0]}</h2>
      <p class="lede rv mt-14">{p["concl"][1]}</p>
      <div class="mt-l rv"><a class="link-arw" href="/projeler/{nextp["slug"]}.html">Sonraki proje: {nextp["name"]}</a></div>
    </div>
  </section>

  <section class="section section--tight">
    <div class="wrap">
      <p class="eyebrow rv">İlgili projeler</p>
      <div class="cards cards--3 mt-m">
        <a class="card rv" href="/projeler/{r0["slug"]}.html"><h3>{r0["name"]}</h3><p>{r0["meta"]}</p><span class="link-arw">İncele</span></a>
        <a class="card rv" href="/projeler/{r1["slug"]}.html"><h3>{r1["name"]}</h3><p>{r1["meta"]}</p><span class="link-arw">İncele</span></a>
        <a class="card rv" href="/projeler/{r2["slug"]}.html"><h3>{r2["name"]}</h3><p>{r2["meta"]}</p><span class="link-arw">İncele</span></a>
      </div>
    </div>
  </section>

  <section class="section section--tight cta-band">
    <div class="wrap">
      <div>
        <p class="eyebrow">Uzaktan görüşelim</p>
        <h2>Şebekenizi birlikte değerlendirelim.</h2>
        <p class="lede mt-14">Kısa bir görüntülü görüşmede mevcut durumu, yaklaşımı ve kapsamı konuşuruz.</p>
      </div>
      <div class="cta-band__act">
        <a class="btn" href="/iletisim.html">Görüşme talebi <span class="arw" aria-hidden="true">→</span></a>
        <a class="btn btn--ghost" href="/projeler/">Tüm projeler</a>
      </div>
    </div>
  </section>
  </article>
</main>

{FOOTER}'''

    return page_head(title, p["desc"], canon, "article", ld) + body

for i, p in enumerate(P):
    out = os.path.join(SITE, "projeler", p["slug"] + ".html")
    open(out, "w", encoding="utf-8", newline="").write(render(i, p))
    print("wrote", os.path.relpath(out, SITE))

# ---------------------------------------------------------------- index page
def card(p):
    src = "/assets/projects/" + p["photos"][0][0].replace(".jpg", ".webp")
    st = p["spec"][:3]
    stats = "".join(f'<div><b>{v}{(" "+u) if u else ""}</b><span>{l}</span></div>' for l, v, u, _ in st)
    return f'''      <article class="case rv">
        <div class="case__media"><img src="{src}" alt="{p['name']} projesi" loading="lazy"></div>
        <div class="case__body">
          <span class="case__kicker">{p['kicker']}</span>
          <h3>{p['h1']}</h3>
          <div class="case__stats">{stats}</div>
          <a class="link-arw" href="/projeler/{p['slug']}.html">Projeyi oku</a>
        </div>
      </article>'''

cards = "\n".join(card(p) for p in P)
idx_ld = f'''<script type="application/ld+json">
{{ "@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
 {{"@type":"ListItem","position":1,"name":"Ana Sayfa","item":"{BASE}/"}},
 {{"@type":"ListItem","position":2,"name":"Projeler","item":"{BASE}/projeler/"}} ]}}
</script>
<script type="application/ld+json">
{{ "@context":"https://schema.org","@type":"ItemList","name":"LeakExpert projeleri","itemListElement":[
{",".join(f'{{"@type":"ListItem","position":{i+1},"url":"{BASE}/projeler/{p["slug"]}.html","name":"{p["name"]}"}}' for i,p in enumerate(P))} ]}}
</script>'''

idx = page_head("Projeler — Belediye Su Kayıp-Kaçak Çalışmaları | LeakExpert",
  "LeakExpert proje arşivi: Kütahya, Batman, Çanakkale, Keşan, Kilis, Sivas, Rize, Doğubayazıt, Fatsa, Bodrum ve Mozambik-Beira. Sahadan ölçülmüş sonuçlar.",
  f"{BASE}/projeler/", "website", idx_ld)
idx += f'''{header("/projeler/")}

<main id="main">
  <div class="wrap">
    <nav class="crumb" aria-label="Sayfa işaret yolu">
      <a href="/">Ana Sayfa</a><span class="sep">/</span><span aria-current="page">Projeler</span>
    </nav>
  </div>

  <section class="phead">
    <div class="wrap">
      <p class="eyebrow">Projeler</p>
      <h1>Sahadan ölçülmüş sonuçlar.</h1>
      <p class="lede">Aşağıdaki rakamlar tamamlanmış çalışmaların raporlarından derlenmiştir. Ekonomik büyüklükler tahminidir ve her idarede kurum verisiyle doğrulanır.</p>
    </div>
  </section>

  <section class="section">
    <div class="wrap wrap--wide grid-20">
{cards}
    </div>
  </section>

  <section class="section section--tight cta-band">
    <div class="wrap">
      <div>
        <p class="eyebrow">Sırada sizin şebekeniz</p>
        <h2>Aynı yöntemi belediyenizde uygulayalım.</h2>
        <p class="lede mt-14">Pilot bir etapla başlayıp sonuçları birlikte değerlendirelim.</p>
      </div>
      <div class="cta-band__act">
        <a class="btn" href="/iletisim.html">Görüşme talebi <span class="arw" aria-hidden="true">→</span></a>
        <a class="btn btn--ghost" href="/referanslar.html">Referanslar</a>
      </div>
    </div>
  </section>
</main>

{FOOTER}'''
open(os.path.join(SITE, "projeler", "index.html"), "w", encoding="utf-8", newline="").write(idx)
print("wrote projeler/index.html")

# sitemap (lastmod + image entries)
from datetime import date as _date
LM = _date.today().isoformat()
sm = ['<?xml version="1.0" encoding="UTF-8"?>',
      '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">']
def u(loc, cf, pr, imgs=None):
    sm.append(f'  <url><loc>{loc}</loc><lastmod>{LM}</lastmod><changefreq>{cf}</changefreq><priority>{pr}</priority>')
    for im in (imgs or []):
        sm.append(f'    <image:image><image:loc>{BASE}{im}</image:loc></image:image>')
    sm.append('  </url>')
u(f"{BASE}/", "weekly", "1.0", ["/assets/img/og-cover.png"])
u(f"{BASE}/platform.html", "monthly", "0.9")
u(f"{BASE}/hizmetler.html", "monthly", "0.9", ["/assets/photos/gece-operasyon.webp", "/assets/photos/basinc-logger.webp"])
u(f"{BASE}/projeler/", "weekly", "0.8")
for pp in P:
    u(f"{BASE}/projeler/{pp['slug']}.html", "monthly", "0.7",
      ["/assets/projects/" + ph[0].replace('.jpg', '.webp') for ph in pp['photos']])
u(f"{BASE}/rehber/", "monthly", "0.8")
for _rs in ("su-kacagi-nasil-anlasilir", "akustik-su-kacagi-tespiti-nedir", "dma-nedir", "su-kaybi-dusurme-yol-haritasi"):
    u(f"{BASE}/rehber/{_rs}.html", "yearly", "0.7")
u(f"{BASE}/referanslar.html", "monthly", "0.8")
u(f"{BASE}/hakkimizda.html", "monthly", "0.7", ["/assets/team/hasan-koramaz.webp", "/assets/team/muhammed-koramaz.webp"])
u(f"{BASE}/sss.html", "monthly", "0.7")
u(f"{BASE}/iletisim.html", "yearly", "0.8")
u(f"{BASE}/gizlilik.html", "yearly", "0.2")
sm.append('</urlset>')
open(os.path.join(SITE, "sitemap.xml"), "w", encoding="utf-8", newline="\n").write("\n".join(sm) + "\n")
print("wrote sitemap.xml with", len(P), "project urls + images")
