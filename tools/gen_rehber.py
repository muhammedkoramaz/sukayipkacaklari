# -*- coding: utf-8 -*-
"""Group B — /rehber/ hub + articles + Kayseri local landing page.
Writes into the live site tree. Shares header/footer/head with existing pages."""
import os

SITE = r"C:\Users\muham\Desktop\LEAKEXPERT APPS\leakexpert-site"
BASE = "https://sukayipkacaklari.com"
GA = ('<!-- Google Analytics 4 — gtag.js kritik yoldan çıkarıldı, boşta yüklenir -->\n'
      '<link rel="dns-prefetch" href="https://www.googletagmanager.com">\n'
      '<link rel="dns-prefetch" href="https://www.google-analytics.com">\n'
      "<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}"
      "gtag('js',new Date());gtag('config','G-ETN61F721R',{anonymize_ip:true});"
      "(function(){function l(){var s=document.createElement('script');s.async=1;"
      "s.src='https://www.googletagmanager.com/gtag/js?id=G-ETN61F721R';document.head.appendChild(s);}"
      "if('requestIdleCallback'in window){requestIdleCallback(l,{timeout:3000});}"
      "else{window.addEventListener('load',function(){setTimeout(l,1200);});}})();</script>")

NAV_ITEMS = [
    ('/', 'Ana Sayfa'), ('/platform.html', 'Platform'), ('/hizmetler.html', 'Hizmetler'),
    ('/rehber/', 'Rehber'), ('/projeler/', 'Projeler'), ('/referanslar.html', 'Referanslar'),
    ('/hakkimizda.html', 'Hakkımızda'), ('/iletisim.html', 'İletişim'),
]

def nav(active):
    out = []
    for href, label in NAV_ITEMS:
        cur = ' aria-current="page"' if href == active else ''
        out.append(f'      <a href="{href}"{cur}>{label}</a>')
    return '\n'.join(out)

PHONE_SVG = ('<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            'stroke-width="2" aria-hidden="true"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 '
            '19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 '
            '2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.9.34 1.85.57 2.81.7A2 '
            '2 0 0 1 22 16.92z"/></svg>')

def head(title, desc, canonical, extra_preload_prefix="/", schema_blocks=()):
    p = extra_preload_prefix
    sb = "\n".join(schema_blocks)
    return f"""<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
<link rel="alternate" hreflang="tr" href="{canonical}">
<link rel="alternate" hreflang="x-default" href="{canonical}">
<meta name="theme-color" content="#ffffff">
<meta property="og:type" content="article">
<meta property="og:site_name" content="LeakExpert">
<meta property="og:locale" content="tr_TR">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{BASE}/assets/img/og-cover.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{BASE}/assets/img/og-cover.png">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" href="/assets/img/icon.png">
<link rel="apple-touch-icon" href="/assets/icons/app-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preload" as="font" type="font/woff2" href="{p}assets/fonts/bricolage-grotesque-600-800-latin.woff2" crossorigin>
<link rel="preload" as="font" type="font/woff2" href="{p}assets/fonts/bricolage-grotesque-600-800-latin-ext.woff2" crossorigin>
<link rel="preload" as="font" type="font/woff2" href="{p}assets/fonts/plus-jakarta-sans-400-latin.woff2" crossorigin>
<link rel="stylesheet" href="/assets/css/fonts.min.css">
<link rel="stylesheet" href="/assets/css/site.min.css">
{sb}
{GA}
</head>
<body>
<a class="skip" href="#main">İçeriğe geç</a>

<header class="hdr">
  <div class="wrap hdr__in">
    <a class="brand" href="/" aria-label="LeakExpert ana sayfa">
      <img src="/assets/img/logo.svg" alt="LeakExpert" width="118" height="34" class="brand__logo">
    </a>
    <nav class="nav" id="navmenu" aria-label="Ana menü">
{{nav_html}}
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
</header>
"""

FOOTER = f"""
<footer class="ftr">
  <div class="wrap">
    <div class="ftr__grid">
      <div>
        <a class="brand" href="/" aria-label="LeakExpert ana sayfa">
          <img src="/assets/img/logo.svg" alt="LeakExpert" width="118" height="34" class="brand__logo">
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
</html>
"""

def breadcrumb(items):
    els = ", ".join(
        f'{{ "@type": "ListItem", "position": {i+1}, "name": "{n}", "item": "{u}" }}'
        for i, (n, u) in enumerate(items))
    return ('<script type="application/ld+json">\n{\n'
            '  "@context": "https://schema.org",\n'
            '  "@type": "BreadcrumbList",\n'
            f'  "itemListElement": [ {els} ]\n'
            '}\n</script>')

def article_schema(headline, desc, url, section):
    return ('<script type="application/ld+json">\n{\n'
            '  "@context": "https://schema.org",\n'
            '  "@type": "Article",\n'
            f'  "headline": "{headline}",\n'
            f'  "description": "{desc}",\n'
            f'  "mainEntityOfPage": {{ "@type": "WebPage", "@id": "{url}" }},\n'
            f'  "articleSection": "{section}",\n'
            '  "inLanguage": "tr-TR",\n'
            '  "author": { "@type": "Organization", "name": "LeakExpert", "url": "https://sukayipkacaklari.com/" },\n'
            '  "publisher": { "@type": "Organization", "name": "LeakExpert", "url": "https://sukayipkacaklari.com/",\n'
            '    "logo": { "@type": "ImageObject", "url": "https://sukayipkacaklari.com/assets/img/icon.png" } },\n'
            '  "image": "https://sukayipkacaklari.com/assets/img/og-cover.png",\n'
            '  "datePublished": "2026-09-01", "dateModified": "2026-09-01"\n'
            '}\n</script>')

def crumbnav(trail):
    # trail: list of (label, href or None)
    parts = []
    for i, (label, href) in enumerate(trail):
        if href:
            parts.append(f'<a href="{href}">{label}</a>')
        else:
            parts.append(f'<span aria-current="page">{label}</span>')
        if i < len(trail) - 1:
            parts.append('<span class="sep">/</span>')
    return '<nav class="crumb" aria-label="Sayfa işaret yolu">\n      ' + ''.join(parts) + '\n    </nav>'

CTA = """
  <section class="section section--tight cta-band">
    <div class="wrap">
      <div>
        <p class="eyebrow">Şebekeniz için</p>
        <h2>Kaybı ölçelim, noktayı bulalım.</h2>
        <p class="lede mt-14">Kısa bir görüntülü görüşmede mevcut durumu ve uygulanacak yöntemi konuşalım.</p>
      </div>
      <div class="cta-band__act">
        <a class="btn" href="/iletisim.html">Görüşme talebi <span class="arw" aria-hidden="true">→</span></a>
        <a class="btn btn--ghost" href="/hizmetler.html">Hizmetler</a>
      </div>
    </div>
  </section>
"""

def write(path, html):
    full = os.path.join(SITE, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8", newline="\n") as f:
        f.write(html)
    print("wrote", path, f"({len(html)} b)")

# ------------------------------------------------------------------ ARTICLES
ARTICLES = [
    dict(
        slug="su-kacagi-nasil-anlasilir",
        h1="Su kaçağı nasıl anlaşılır? Şebekede 8 belirti",
        title="Su Kaçağı Nasıl Anlaşılır? 8 Belirti ve Kontrol Yöntemi | LeakExpert",
        desc="İçme suyu şebekesinde gizli su kaçağının belirtileri: gece minimum debi artışı, basınç düşüşü, NRW oranının açılması, sürekli nemli zemin. Nasıl doğrulanır?",
        section="Rehber",
        lede="Görünür bir su birikintisi çoğu kaçağın <strong>son</strong> belirtisidir. Şebeke ölçeğinde kayıp, çok daha önce verideki küçük sapmalardan okunur. İşte belediye ve sanayi içme suyu şebekelerinde en güvenilir sekiz işaret.",
        body="""
      <div class="prose">
        <h2>1. Gece minimum debisinin yükselmesi</h2>
        <p>Bir bölgenin (DMA) depo çıkışında ölçülen debi, tüketimin durduğu gece 03:00–05:00 arasında en düşük seviyesine iner. Bu <strong>gece minimum debisi</strong> zamanla artıyorsa ve nüfus/abone sayısı sabitse, aradaki fark büyük olasılıkla yeni bir fiziki kaçaktır. Şebeke izlemede en erken ve en nesnel sinyal budur.</p>

        <h2>2. Bölgesel basınç düşüşü</h2>
        <p>Pompa debisi değişmediği hâlde bir hattın ucundaki basınç kademeli düşüyorsa, arada su bir yerden sistemi terk ediyor demektir. 7/24 <a href="/hizmetler.html#basinc">basınç loggerı</a> kaydı, bu düşüşü saatlik çözünürlükte gösterir.</p>

        <h2>3. Fatura edilen suyla üretilen su arasındaki makasın açılması</h2>
        <p>Depoya giren toplam su ile abonelere fatura edilen su arasındaki fark, <strong>fatura edilemeyen su (NRW)</strong> oranıdır. Bu oran %30'un üzerindeyse ve tırmanıyorsa, şebekede ölçülmesi gereken bir kayıp birikmiştir.</p>

        <h2>4. Belirli bir noktada hiç kesilmeyen akış sesi</h2>
        <p>Vananın, yangın hidrantının veya abone bağlantısının yanında gece bile duyulan sürekli "fışırtı", klasik kaçak sesidir. <a href="/hizmetler.html#akustik">Akustik dinleme</a> bu sesi yer mikrofonuyla büyütür ve korelatörle iki nokta arasında konumlandırır.</p>

        <h2>5. Kuru havada sürekli nemli kalan zemin veya yeşeren şerit</h2>
        <p>Asfaltta kenar çökmesi, kaldırımda yosunlanma, yağış olmadığı hâlde ıslak kalan toprak veya çevresine göre belirgin yeşeren bir çim şeridi — yüzeye ulaşmış bir kaçağın işaretidir.</p>

        <h2>6. Onarım sıklığının artması</h2>
        <p>Aynı bölgede kısa aralıklarla tekrarlayan boru patlamaları çoğunlukla <strong>yüksek veya dalgalı basınçla</strong> ilişkilidir. Basınç yönetimi devreye alınmadan yapılan onarımlar, sorunu birkaç ay sonra komşu noktaya taşır.</p>

        <h2>7. Klorlama ve pompa maliyetlerinin açıklanamayan artışı</h2>
        <p>Kaçan her metreküp su; arıtılmış, klorlanmış ve basılmıştır. Nüfus artmadan enerji ve kimyasal tüketimi yükseliyorsa, fark şebekede sızan sudur.</p>

        <h2>8. Rezervuar seviyesinin gece de düşmesi</h2>
        <p>Depo seviyesi, tüketim durduğunda sabitlenmelidir. Gece boyunca da düşüyorsa, depo ile ilk ölçüm noktası arasındaki isale hattında ciddi bir kaçak aranmalıdır.</p>

        <h2>Belirti var — sıra doğrulamada</h2>
        <p>Bu işaretler kaybın <em>varlığını</em> gösterir, <em>yerini</em> değil. Yer tespiti için sistematik bir saha çalışması gerekir: bölgeleme (DMA), gece debi ölçümü, adım adım (step) test ve akustik tarama. LeakExpert bu döngüyü tek programda yürütür ve her noktayı koordinatıyla raporlar.</p>
        <ul>
          <li>Yöntemin ayrıntısı: <a href="/hizmetler.html">Hizmetler</a></li>
          <li>Saha örnekleri: <a href="/projeler/">Projeler</a></li>
          <li>Sık sorulanlar: <a href="/sss.html">SSS</a></li>
        </ul>
      </div>
""",
    ),
    dict(
        slug="akustik-su-kacagi-tespiti-nedir",
        h1="Akustik su kaçağı tespiti nedir, nasıl yapılır?",
        title="Akustik Su Kaçağı Tespiti Nasıl Yapılır? Yer Mikrofonu ve Korelatör | LeakExpert",
        desc="Akustik su kaçağı tespitinin adımları: gürültü kaydediciyle tarama, yer mikrofonuyla daraltma, korelatörle metrik konumlandırma. Neden gece yapılır?",
        section="Rehber",
        lede="Basınçlı bir borudan kaçan su, boru cidarında ve zeminde <strong>titreşim (ses)</strong> üretir. Akustik tespit, bu sesi dinleyip kaynağına doğru daraltma sanatıdır. Tahribatsızdır; kazı yalnızca doğrulanmış noktada yapılır.",
        body="""
      <div class="prose">
        <h2>Kaçak neden ses çıkarır?</h2>
        <p>Sudaki basınç, delik veya çatlaktan dışarı çıkarken türbülansa dönüşür. Bu türbülans; boru malzemesine, çapına, basınca ve zemine bağlı olarak yaklaşık <strong>20–2.500 Hz</strong> aralığında sürekli bir ses yayar. Metal borularda ses uzağa taşınır; plastik (PE, PVC) borularda hızla söner, bu yüzden ölçüm noktaları sıklaştırılır.</p>

        <h2>Adım 1 — Ön bölgeleme</h2>
        <p>Şebeke haritası, vana konumları ve varsa DMA sınırları incelenir. Kayıp verisi yüksek olan bölge, taranacak öncelikli alan olarak seçilir. Gerekirse geçici debi loggerıyla bölgenin gece minimum debisi ölçülür.</p>

        <h2>Adım 2 — Gürültü kaydedicilerle gece taraması</h2>
        <p>Vanalara ve hidrantlara <strong>gürültü kaydedici (noise logger)</strong> yerleştirilir. Cihazlar gecenin en sessiz saatlerinde otomatik kayıt alır; sürekli ve yüksek genlikli ses veren noktalar "şüpheli" olarak işaretlenir. Bu, geniş alanı hızla eleme adımıdır.</p>

        <h2>Adım 3 — Yer mikrofonuyla daraltma</h2>
        <p>Şüpheli hat üzerinde, zeminden <strong>yer mikrofonu</strong> ile nokta nokta dinleme yapılır. Kaçağa yaklaştıkça ses seviyesi yükselir, en yüksek okumanın alındığı yer kaçağın izdüşümüdür. Vana ve bağlantılarda dinleme çubuğu kullanılır.</p>

        <h2>Adım 4 — Korelatörle metrik konumlandırma</h2>
        <p>Kaçağın iki yanındaki temas noktalarına (vana, hidrant) birer sensör konur. <strong>Korelatör</strong>, kaçak sesinin iki sensöre varış zamanı farkını ve borudaki ses hızını kullanarak kaçağı iki nokta arasında <strong>metre mertebesinde</strong> konumlandırır. Boru malzemesi ve çapı doğru girildiğinde hata payı çok düşüktür.</p>

        <h2>Adım 5 — Doğrulama ve teslim</h2>
        <p>Belirlenen nokta yer mikrofonuyla teyit edilir, koordinatı ve ses seviyesi kaydedilir, fotoğraflanır. Kazı yalnızca bu doğrulanmış nokta için yapılır. Tüm noktalar <a href="/hizmetler.html#cbs">CBS haritasına</a> ve LeakExpert platformuna işlenir.</p>

        <h2>Neden gece çalışılır?</h2>
        <p>Gündüz tüketimi, trafik ve zemin gürültüsü kaçak sesini maskeler. Gece tüketim durunca şebeke sessizleşir; kaçağın sesi göreli olarak belirginleşir ve çok daha uzaktan yakalanır.</p>

        <h2>Hangi durumlarda tek başına yetmez?</h2>
        <p>Çok derin hatlar, geniş çaplı isale boruları, yüksek yeraltı suyu ve tümüyle plastik yeni şebekelerde akustik yöntem <strong>debi/basınç ölçümü ve step testiyle</strong> birlikte kullanılır. LeakExpert bu yüzden tek yönteme değil, kapalı döngü bir programa dayanır.</p>
        <ul>
          <li>İlişkili hizmet: <a href="/hizmetler.html#akustik">Akustik sızıntı tespiti</a></li>
          <li>Kavram: <a href="/rehber/dma-nedir.html">DMA nedir?</a></li>
          <li>Uygulanışı: <a href="/projeler/">Proje sayfaları</a></li>
        </ul>
      </div>
""",
    ),
    dict(
        slug="dma-nedir",
        h1="DMA (İzole Ölçüm Bölgesi) nedir, nasıl kurulur?",
        title="DMA Nedir? İzole Ölçüm Bölgesi Kurulumu ve Gece Minimum Debi | LeakExpert",
        desc="DMA (District Metered Area) bir şebekeyi ölçülebilir alt bölgelere ayırır. Kurulum adımları, gece minimum debi analizi, step test ve kayıp ayrıştırma anlatımı.",
        section="Rehber",
        lede="Bir şehir şebekesini bütün hâlde denetlemek zordur. <strong>DMA</strong> (District Metered Area — izole ölçüm bölgesi), şebekeyi girişi ve çıkışı sayılabilen küçük, kalıcı parçalara böler. Kayıp, ancak ölçülebildiği yerde yönetilebilir.",
        body="""
      <div class="prose">
        <h2>DMA neyi çözer?</h2>
        <p>Şehir geneli NRW oranı "%35" gibi bir sayı verir ama kaybın <strong>nerede</strong> olduğunu söylemez. Şebeke 15–20 DMA'ya bölündüğünde, her bölgenin kendi gece minimum debisi izlenir; kayıp birkaç bölgeye daralır ve saha ekibi doğru yere gönderilir.</p>

        <h2>Bir DMA'nın büyüklüğü</h2>
        <p>Tipik olarak <strong>500–3.000 abone</strong> veya birkaç kilometre hat. Çok büyük DMA'da küçük kaçaklar gece debisi içinde kaybolur; çok küçük DMA ise fazla vana ve sayaç maliyeti getirir. Topografya, basınç bölgeleri ve doğal sınırlar (dere, ana yol, demiryolu) gözetilerek belirlenir.</p>

        <h2>Kurulum adımları</h2>
        <h3>1. Sınır tasarımı</h3>
        <p>Şebeke haritası üzerinde bölge sınırları çizilir. Sınırdaki tüm bağlantılar ya kalıcı kapatılır ya da sayaçlı girişe dönüştürülür. Amaç: bölgeye giren her damlanın sayaçtan geçmesi.</p>
        <h3>2. Sınır vanası testi</h3>
        <p>Kapatılması gereken vanalar tek tek kapatılıp sızdırmazlığı kontrol edilir. Kapanmayan tek bir sınır vanası, tüm ölçümü bozar.</p>
        <h3>3. Giriş sayacı / debimetre montajı</h3>
        <p>Bölge girişine kalıcı elektromanyetik sayaç veya geçici <a href="/hizmetler.html#debi">ultrasonik debimetre</a> takılır; akış 15 dakikalık adımlarla kaydedilir.</p>
        <h3>4. Gece minimum debi (MNF) ölçümü</h3>
        <p>03:00–05:00 arası ölçülen minimum debiden, meşru gece tüketimi (sifon dolumları, sanayi, kaçak olmayan kullanım) çıkarılır. Kalan değer <strong>fiziki kayıp debisidir</strong>. Türkiye'de gece minimum debisinin yaklaşık %70'i fiziki kayıptır.</p>

        <h2>Step test — kaybı hat bazına indirmek</h2>
        <p>DMA içindeki vanalar, gece boyunca uçtan başlayarak sırayla kapatılır. Bir vana kapandığında giriş debisi belirgin düşüyorsa, o vananın beslediği hatta kayıp yoğunlaşmıştır. Böylece ölçüm sahası birkaç yüz metreye iner ve akustik tarama hedeflenir.</p>

        <h2>Kalıcı izleme</h2>
        <p>Kurulan DMA bir kereye mahsus değildir. Giriş sayacı sürekli kayıt aldıkça, yeni bir kaçak oluştuğunda gece debisi birkaç gün içinde yükselir ve sistem erken uyarı verir. LeakExpert platformu bu eğriyi bölge bölge takip eder.</p>
        <ul>
          <li>İlişkili hizmet: <a href="/hizmetler.html#dma">DMA, step &amp; sıfır basınç testi</a></li>
          <li>Ölçüm tarafı: <a href="/hizmetler.html#debi">Debi ölçümü &amp; NRW analizi</a></li>
          <li>Yol haritası: <a href="/rehber/su-kaybi-dusurme-yol-haritasi.html">Su kaybını düşürme yol haritası</a></li>
        </ul>
      </div>
""",
    ),
    dict(
        slug="su-kaybi-dusurme-yol-haritasi",
        h1="Su kayıp-kaçak oranını düşürme yol haritası",
        title="Su Kayıp-Kaçak Oranını Düşürme Yol Haritası (NRW / IWA) | LeakExpert",
        desc="Fatura edilemeyen su (NRW) oranını kalıcı düşürmek için sekiz adımlı program: su dengesi, DMA, basınç yönetimi, aktif kaçak kontrolü, sayaç doğrulama.",
        section="Rehber",
        lede="Su kaybını düşürmek tek seferlik bir kampanya değil, <strong>sürekli bir program</strong>dır. IWA (Uluslararası Su Birliği) çerçevesi dört kaldıraç tanımlar; sıra ve süreklilik olmadan kazanç kısa sürede geri erir.",
        body="""
      <div class="prose">
        <h2>Önce ölç: IWA su dengesi</h2>
        <p>Sisteme giren su, faturalı tüketim, faturasız meşru tüketim, idari kayıp (sayaç hatası, kaçak kullanım) ve fiziki kayıp (sızıntı, patlak, taşma) kalemlerine ayrılır. Bu tablo çıkarılmadan hedef konulamaz. Çıktı: <strong>NRW oranı</strong>, kayıp hacmi (m³/yıl) ve parasal karşılığı.</p>

        <h2>Dört kaldıraç</h2>
        <ul>
          <li><strong>Basınç yönetimi</strong> — fazla basıncı düşürmek kaçak debisini ve yeni patlak sayısını anında azaltır.</li>
          <li><strong>Aktif kaçak kontrolü</strong> — DMA + akustik tarama ile bilinmeyen kaçakları bulup bekletmeden onarmak.</li>
          <li><strong>Onarım hızı ve kalitesi</strong> — bir kaçağın tespitten onarıma kadar akan süresi doğrudan kayıp hacmidir.</li>
          <li><strong>Altyapı yönetimi</strong> — kronik arızalı hatların planlı yenilenmesi.</li>
        </ul>

        <h2>Sekiz adımlı program</h2>
        <h3>1. Veri toplama ve su dengesi</h3>
        <p>Depo giriş kayıtları, abone sayaç okumaları ve şebeke haritası bir araya getirilir; başlangıç NRW'si hesaplanır.</p>
        <h3>2. Basınç bölgelerinin haritalanması</h3>
        <p>Yüksek basınçlı bölgeler tespit edilir; basınç düşürücü vana (PRV) noktaları planlanır.</p>
        <h3>3. Pilot DMA kurulumu</h3>
        <p>Kayıp şüphesi yüksek bir bölgede <a href="/rehber/dma-nedir.html">DMA</a> kurulur, gece minimum debi ölçülür.</p>
        <h3>4. Aktif tarama</h3>
        <p>Pilot bölgede <a href="/rehber/akustik-su-kacagi-tespiti-nedir.html">akustik tespit</a> + step test uygulanır, noktalar raporlanır.</p>
        <h3>5. Hızlı onarım döngüsü</h3>
        <p>Bulunan her nokta önceliklendirilip onarım ekibine iletilir; onarım sonrası kontrol dinlemesi yapılır.</p>
        <h3>6. Sayaç doğrulama</h3>
        <p>Büyük abonelerin sayaçları test edilir; yavaş/duran sayaçlar idari kaybı büyütür.</p>
        <h3>7. Yaygınlaştırma</h3>
        <p>Pilotta işleyen yöntem, şehir geneline DMA DMA genişletilir.</p>
        <h3>8. Kalıcı izleme</h3>
        <p>Her DMA'nın gece debisi sürekli izlenir; eşik aşıldığında bölge yeniden taranır. Kazanç ancak bu izlemeyle korunur.</p>

        <h2>Ne beklemeli?</h2>
        <p>Basınç yönetimi haftalar içinde ölçülebilir düşüş verir. Aktif kaçak kontrolü ilk yıl NRW'de belirgin gerileme sağlar. Kalıcı sonuç için programın kesintisiz sürmesi şarttır — bırakıldığında kayıp yılda birkaç puan geri tırmanır.</p>
        <ul>
          <li>Hizmet kapsamı: <a href="/hizmetler.html">Saha hizmetleri</a></li>
          <li>Platform desteği: <a href="/platform.html">Web + mobil platform</a></li>
          <li>Örnek uygulamalar: <a href="/projeler/">Projeler</a></li>
        </ul>
      </div>
""",
    ),
]

REHBER_INDEX_ITEMS = [
    ("su-kacagi-nasil-anlasilir", "Su kaçağı nasıl anlaşılır?", "İçme suyu şebekesinde gizli kaybın 8 belirtisi ve nasıl doğrulandığı."),
    ("akustik-su-kacagi-tespiti-nedir", "Akustik su kaçağı tespiti nasıl yapılır?", "Gürültü kaydedici, yer mikrofonu ve korelatörle adım adım yer tespiti."),
    ("dma-nedir", "DMA (İzole Ölçüm Bölgesi) nedir?", "Şebekeyi ölçülebilir bölgelere ayırmak, gece minimum debi ve step test."),
    ("su-kaybi-dusurme-yol-haritasi", "Su kaybını düşürme yol haritası", "NRW / IWA çerçevesi ve sekiz adımlı kalıcı kayıp azaltma programı."),
]

def build_article(a):
    url = f"{BASE}/rehber/{a['slug']}.html"
    schema = [
        breadcrumb([("Ana Sayfa", f"{BASE}/"), ("Rehber", f"{BASE}/rehber/"), (a['h1'], url)]),
        article_schema(a['h1'], a['desc'], url, a['section']),
    ]
    h = head(a['title'], a['desc'], url, extra_preload_prefix="/", schema_blocks=schema)
    h = h.replace("{nav_html}", nav("/rehber/"))
    # related list = other 3 articles
    rel = [x for x in ARTICLES if x['slug'] != a['slug']][:3]
    rel_cards = "\n".join(
        f'        <a class="card" href="/rehber/{r["slug"]}.html"><h3>{r["h1"]}</h3><p>{r["desc"][:90]}…</p></a>'
        for r in rel)
    body = f"""
<main id="main">
  <div class="wrap">
    {crumbnav([("Ana Sayfa", "/"), ("Rehber", "/rehber/"), (a['h1'], None)])}
  </div>

  <section class="phead">
    <div class="wrap">
      <p class="eyebrow">Rehber</p>
      <h1>{a['h1']}</h1>
      <p class="lede">{a['lede']}</p>
    </div>
  </section>

  <section class="section">
    <div class="wrap mw-900">
{a['body']}
    </div>
  </section>

  <section class="section section--panel">
    <div class="wrap">
      <p class="eyebrow rv">Rehberde ayrıca</p>
      <h2 class="h-sec rv">İlgili yazılar.</h2>
      <div class="cards cards--3 mt-l">
{rel_cards}
      </div>
    </div>
  </section>
{CTA}
</main>
"""
    write(f"rehber/{a['slug']}.html", h + body + FOOTER)

def build_rehber_index():
    url = f"{BASE}/rehber/"
    item_list = ", ".join(
        f'{{ "@type": "ListItem", "position": {i+1}, "url": "{BASE}/rehber/{s}.html", "name": "{t}" }}'
        for i, (s, t, d) in enumerate(REHBER_INDEX_ITEMS))
    schema = [
        breadcrumb([("Ana Sayfa", f"{BASE}/"), ("Rehber", url)]),
        ('<script type="application/ld+json">\n{\n'
         '  "@context": "https://schema.org",\n  "@type": "CollectionPage",\n'
         '  "name": "Su kayıp-kaçak rehberi",\n'
         f'  "url": "{url}",\n  "inLanguage": "tr-TR",\n'
         f'  "hasPart": {{ "@type": "ItemList", "itemListElement": [ {item_list} ] }}\n'
         '}\n</script>'),
    ]
    title = "Su Kayıp-Kaçak Rehberi — Tespit Yöntemleri, DMA, NRW | LeakExpert"
    desc = ("Su kaçağı belirtileri, akustik tespit, DMA kurulumu ve su kaybı düşürme yol haritası. "
            "Belediye ve sanayi şebekeleri için uygulamalı rehber yazıları.")
    h = head(title, desc, url, extra_preload_prefix="/", schema_blocks=schema)
    h = h.replace("{nav_html}", nav("/rehber/"))
    cards = "\n".join(
        f'        <a class="card rv" href="/rehber/{s}.html"><span class="card__ix">{i+1:02d}</span>'
        f'<h3>{t}</h3><p>{d}</p></a>'
        for i, (s, t, d) in enumerate(REHBER_INDEX_ITEMS))
    body = f"""
<main id="main">
  <div class="wrap">
    {crumbnav([("Ana Sayfa", "/"), ("Rehber", None)])}
  </div>

  <section class="phead">
    <div class="wrap">
      <p class="eyebrow">Rehber</p>
      <h1>Su kayıp-kaçak rehberi.</h1>
      <p class="lede">Şebeke ve sanayi tesislerinde su kaçağını anlamak, ölçmek ve kalıcı olarak
        azaltmak için uygulamalı yazılar. Yöntemin saha karşılığı için
        <a class="link-arw inline-flex" href="/projeler/">projelere</a> bakın.</p>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="cards cards--3">
{cards}
      </div>
    </div>
  </section>
{CTA}
</main>
"""
    write("rehber/index.html", h + body + FOOTER)

if __name__ == "__main__":
    for a in ARTICLES:
        build_article(a)
    build_rehber_index()
    print("done")
