# -*- coding: utf-8 -*-
"""Group B — /blog/ hub + articles, bilingual (tr + en).
Writes into the live site tree (root = tr, /en/ = en).
Shares header/footer/head/lang-switcher/open-script with gen_projects.py —
keep the two in sync (PROJECT.md §6)."""
import os

SITE = r"C:\Users\muham\Desktop\LEAKEXPERT APPS\leakexpert-site"
BASE = "https://sukayipkacaklari.com"
LANGS = ("tr", "en")

GA = ('<!-- Google Analytics 4 — gtag.js kritik yoldan çıkarıldı, boşta yüklenir -->\n'
      '<link rel="dns-prefetch" href="https://www.googletagmanager.com">\n'
      '<link rel="dns-prefetch" href="https://www.google-analytics.com">\n'
      "<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}"
      "gtag('js',new Date());gtag('config','G-ETN61F721R',{anonymize_ip:true});"
      "(function(){function l(){var s=document.createElement('script');s.async=1;"
      "s.src='https://www.googletagmanager.com/gtag/js?id=G-ETN61F721R';document.head.appendChild(s);}"
      "if('requestIdleCallback'in window){requestIdleCallback(l,{timeout:3000});}"
      "else{window.addEventListener('load',function(){setTimeout(l,1200);});}})();</script>")

OPEN_SCRIPT = """<script>
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
  var wantsTr=langs.some(function(l){return /^tr\\b/i.test(l);});
  if(!wantsTr&&cur==='tr'){sessionStorage.setItem('le-lang-redirected','1');location.replace(other);}
  else if(wantsTr&&cur==='en'){sessionStorage.setItem('le-lang-redirected','1');location.replace(other);}
}catch(e){}})();
</script>"""

PHONE_SVG = ('<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            'stroke-width="2" aria-hidden="true"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 '
            '19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 '
            '2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.9.34 1.85.57 2.81.7A2 '
            '2 0 0 1 22 16.92z"/></svg>')

# ---------------------------------------------------------------- i18n table
UI = {
    "tr": {
        "menu": [("/", "Ana Sayfa"), ("/platform.html", "Platform"), ("/hizmetler.html", "Hizmetler"),
                 ("/blog/", "Blog"), ("/projeler/", "Projeler"), ("/referanslar.html", "Referanslar"),
                 ("/hakkimizda.html", "Hakkımızda"), ("/iletisim.html", "İletişim")],
        "skip": "İçeriğe geç", "menu_aria": "Ana menü", "burger_aria": "Menüyü aç",
        "brand_aria": "LeakExpert ana sayfa", "crumb_aria": "Sayfa işaret yolu",
        "og_locale": "tr_TR", "og_locale_alt": "en_US", "html_lang": "tr", "ld_lang": "tr-TR",
        "guide": "Blog", "guide_eyebrow": "Blog",
        "dock_aria": "Hızlı iletişim", "dock_cta": "Görüşme talebi",
        "ftr_brandline": ("Belediye içme suyu şebekelerinde su kayıp kaçakları tespiti, debi/basınç izleme "
                          "ve saha yönetimi. Web ve mobil entegre platform."),
        "ftr_h_platform": "Platform", "ftr_h_corp": "Kurumsal", "ftr_h_contact": "İletişim",
        "ftr_platform": [("/platform.html#mobil", "Mobil saha uygulaması"),
                         ("/platform.html#web", "Web yönetim paneli"),
                         ("/platform.html#api", "API &amp; entegrasyon"),
                         ("/hizmetler.html", "Saha hizmetleri")],
        "ftr_corp": [("/hakkimizda.html", "Hakkımızda"), ("/projeler/", "Projeler"),
                     ("/referanslar.html", "Referanslar"), ("/blog/", "Blog"),
                     ("/sss.html", "Sık sorulan sorular"), ("/iletisim.html", "İletişim"),
                     ("/gizlilik.html", "Gizlilik politikası")],
        "ftr_rights": "© 2026 LeakExpert · Tüm hakları saklıdır.",
        "lang_tr": "Türkçe", "lang_en": "English",
        "cta_eyebrow": "Şebekeniz için", "cta_h": "Kaybı ölçelim, noktayı bulalım.",
        "cta_p": "Kısa bir görüntülü görüşmede mevcut durumu ve uygulanacak yöntemi konuşalım.",
        "cta_btn": "Görüşme talebi", "cta_btn2": "Hizmetler",
        "rel_eyebrow": "Rehberde ayrıca", "rel_h": "İlgili yazılar.",
        "hub_title": "Su Kayıp-Kaçak Rehberi — Tespit Yöntemleri, DMA, NRW | LeakExpert",
        "hub_desc": ("Su kaçağı belirtileri, akustik tespit, DMA kurulumu ve su kaybı düşürme yol haritası. "
                     "Belediye ve sanayi şebekeleri için uygulamalı rehber yazıları."),
        "hub_h1": "Su kayıp-kaçak blogu.",
        "hub_lede": ('Şebeke ve sanayi tesislerinde su kaçağını anlamak, ölçmek ve kalıcı olarak '
                     'azaltmak için uygulamalı yazılar. Yöntemin saha karşılığı için '
                     '<a class="link-arw inline-flex" href="{P}/projeler/">projelere</a> bakın.'),
        "hub_name": "Su kayıp-kaçak blogu",
        "home": "Ana Sayfa",
    },
    "en": {
        "menu": [("/", "Home"), ("/platform.html", "Platform"), ("/hizmetler.html", "Services"),
                 ("/blog/", "Blog"), ("/projeler/", "Projects"), ("/referanslar.html", "References"),
                 ("/hakkimizda.html", "About"), ("/iletisim.html", "Contact")],
        "skip": "Skip to content", "menu_aria": "Main menu", "burger_aria": "Open menu",
        "brand_aria": "LeakExpert home", "crumb_aria": "Breadcrumb",
        "og_locale": "en_US", "og_locale_alt": "tr_TR", "html_lang": "en", "ld_lang": "en-US",
        "guide": "Blog", "guide_eyebrow": "Blog",
        "dock_aria": "Quick contact", "dock_cta": "Request a consultation",
        "ftr_brandline": ("Water loss and leak detection, flow/pressure monitoring and field management "
                          "for municipal drinking-water networks. Integrated web and mobile platform."),
        "ftr_h_platform": "Platform", "ftr_h_corp": "Company", "ftr_h_contact": "Contact",
        "ftr_platform": [("/platform.html#mobil", "Mobile field app"),
                         ("/platform.html#web", "Web management panel"),
                         ("/platform.html#api", "API &amp; integration"),
                         ("/hizmetler.html", "Field services")],
        "ftr_corp": [("/hakkimizda.html", "About"), ("/projeler/", "Projects"),
                     ("/referanslar.html", "References"), ("/blog/", "Blog"),
                     ("/sss.html", "FAQ"), ("/iletisim.html", "Contact"),
                     ("/gizlilik.html", "Privacy policy")],
        "ftr_rights": "© 2026 LeakExpert · All rights reserved.",
        "lang_tr": "Türkçe", "lang_en": "English",
        "cta_eyebrow": "For your network", "cta_h": "Let's measure the loss and pinpoint it.",
        "cta_p": "In a short video call we can review the current situation and the method to apply.",
        "cta_btn": "Request a consultation", "cta_btn2": "Services",
        "rel_eyebrow": "Also in the guide", "rel_h": "Related articles.",
        "hub_title": "Water Loss & Leakage Guide — Detection Methods, DMA, NRW | LeakExpert",
        "hub_desc": ("Leak signs, acoustic detection, DMA setup and a roadmap for cutting water loss. "
                     "Practical guide articles for municipal and industrial networks."),
        "hub_h1": "Water loss & leakage blog.",
        "hub_lede": ('Practical articles on understanding, measuring and permanently reducing water loss in '
                     'distribution networks and industrial plants. For the field side of the method, see the '
                     '<a class="link-arw inline-flex" href="{P}/projeler/">projects</a>.'),
        "hub_name": "Water loss & leakage blog",
        "home": "Home",
    },
}


def pfx(lang):
    return "" if lang == "tr" else "/en"


def rel_href(lang, path):
    """root-relative href for the current language tree; path like '/', '/x.html', '/blog/'."""
    if path == "/":
        return pfx(lang) + "/"
    return pfx(lang) + path


def abs_url(lang, path):
    return BASE + (rel_href(lang, path) if path != "/" else (pfx(lang) + "/"))


def nav(active, page_path, lang):
    u = UI[lang]
    out = []
    for href, label in u["menu"]:
        cur = ' aria-current="page"' if href == active else ''
        out.append(f'      <a href="{rel_href(lang, href)}"{cur}>{label}</a>')
    tr_href = "/" if page_path == "/" else page_path
    en_href = "/en/" if page_path == "/" else "/en" + page_path
    tr_a = ' aria-current="true" class="is-active"' if lang == "tr" else ''
    en_a = ' aria-current="true" class="is-active"' if lang == "en" else ''
    out.append('      <span class="nav__lang" role="group" aria-label="Language / Dil">')
    out.append(f'        <a href="{tr_href}" hreflang="tr" lang="tr"{tr_a}>TR</a>')
    out.append('        <span class="nav__lang-sep" aria-hidden="true">|</span>')
    out.append(f'        <a href="{en_href}" hreflang="en" lang="en"{en_a}>EN</a>')
    out.append('      </span>')
    return '\n'.join(out)


def head(title, desc, page_path, lang, schema_blocks=(), ogtype="article"):
    u = UI[lang]
    canonical = abs_url(lang, page_path)
    tr_url = BASE + ("/" if page_path == "/" else page_path)
    en_url = BASE + ("/en/" if page_path == "/" else "/en" + page_path)
    sb = "\n".join(schema_blocks)
    nav_html = nav(_active_menu(page_path), page_path, lang)
    return f"""<!doctype html>
<html lang="{u['html_lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
<link rel="alternate" hreflang="tr" href="{tr_url}">
<link rel="alternate" hreflang="en" href="{en_url}">
<link rel="alternate" hreflang="x-default" href="{tr_url}">
<meta name="theme-color" content="#ffffff">
<meta property="og:type" content="{ogtype}">
<meta property="og:site_name" content="LeakExpert">
<meta property="og:locale" content="{u['og_locale']}">
<meta property="og:locale:alternate" content="{u['og_locale_alt']}">
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
<link rel="preload" as="font" type="font/woff2" href="/assets/fonts/bricolage-grotesque-600-800-latin.woff2" crossorigin>
<link rel="preload" as="font" type="font/woff2" href="/assets/fonts/bricolage-grotesque-600-800-latin-ext.woff2" crossorigin>
<link rel="preload" as="font" type="font/woff2" href="/assets/fonts/plus-jakarta-sans-400-latin.woff2" crossorigin>
{OPEN_SCRIPT}
<link rel="stylesheet" href="/assets/css/fonts.min.css">
<link rel="stylesheet" href="/assets/css/site.min.css">
{sb}
{GA}
</head>
<body>
<a class="skip" href="#main">{u['skip']}</a>

<header class="hdr">
  <div class="wrap hdr__in">
    <a class="brand" href="{rel_href(lang, '/')}" aria-label="{u['brand_aria']}">
      <img src="/assets/img/logo.svg" alt="LeakExpert" width="118" height="34" class="brand__logo">
    </a>
    <nav class="nav" id="navmenu" aria-label="{u['menu_aria']}">
{nav_html}
    </nav>
    <div class="hdr__cta">
      <a class="hdr__phone" href="tel:+905396588434">
        {PHONE_SVG}
        0539 658 84 34
      </a>
    </div>
    <button class="burger" aria-label="{u['burger_aria']}" aria-expanded="false" aria-controls="navmenu">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
    </button>
  </div>
</header>
"""


def _active_menu(page_path):
    if page_path.startswith("/blog/"):
        return "/blog/"
    return page_path


def footer(lang, page_path):
    u = UI[lang]
    tr_href = "/" if page_path == "/" else page_path
    en_href = "/en/" if page_path == "/" else "/en" + page_path
    fp = "\n".join(f'        <li><a href="{rel_href(lang, h)}">{t}</a></li>' for h, t in u["ftr_platform"])
    fc = "\n".join(f'        <li><a href="{rel_href(lang, h)}">{t}</a></li>' for h, t in u["ftr_corp"])
    return f"""
<footer class="ftr">
  <div class="wrap">
    <div class="ftr__grid">
      <div>
        <a class="brand" href="{rel_href(lang, '/')}" aria-label="{u['brand_aria']}">
          <img src="/assets/img/logo.svg" alt="LeakExpert" width="118" height="34" class="brand__logo">
        </a>
        <p class="ftr__brandline">{u['ftr_brandline']}</p>
      </div>
      <div><h4>{u['ftr_h_platform']}</h4><ul>
{fp}
      </ul></div>
      <div><h4>{u['ftr_h_corp']}</h4><ul>
{fc}
      </ul></div>
      <div><h4>{u['ftr_h_contact']}</h4><ul>
        <li class="ftr__mono">Melikgazi / Kayseri</li>
        <li class="ftr__mono"><a href="tel:+905396588434">+90 539 658 84 34</a></li>
        <li class="ftr__mono"><a href="mailto:sukayipkacaklari@gmail.com">sukayipkacaklari@gmail.com</a></li>
      </ul></div>
    </div>
    <div class="ftr__bottom">
      <span>{u['ftr_rights']}</span>
      <span class="ftr__lang">
        <a href="{tr_href}" hreflang="tr" lang="tr">{u['lang_tr']}</a>
        <span aria-hidden="true">·</span>
        <a href="{en_href}" hreflang="en" lang="en">{u['lang_en']}</a>
      </span>
      <span>sukayipkacaklari.com</span>
    </div>
  </div>
</footer>

<nav class="dock" aria-label="{u['dock_aria']}">
  <a class="btn btn--ghost btn--sm" href="{rel_href(lang, '/iletisim.html')}">{u['dock_cta']}</a>
  <a class="btn btn--sm" href="tel:+905396588434">
    {PHONE_SVG}
    0539 658 84 34
  </a>
</nav>

<script src="/assets/js/site.min.js" defer></script>
</body>
</html>
"""


def cta(lang):
    u = UI[lang]
    return f"""
  <section class="section section--tight cta-band">
    <div class="wrap">
      <div>
        <p class="eyebrow">{u['cta_eyebrow']}</p>
        <h2>{u['cta_h']}</h2>
        <p class="lede mt-14">{u['cta_p']}</p>
      </div>
      <div class="cta-band__act">
        <a class="btn" href="{rel_href(lang, '/iletisim.html')}">{u['cta_btn']} <span class="arw" aria-hidden="true">→</span></a>
        <a class="btn btn--ghost" href="{rel_href(lang, '/hizmetler.html')}">{u['cta_btn2']}</a>
      </div>
    </div>
  </section>
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


def article_schema(headline, desc, url, section, ld_lang):
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
            '  "image": "https://sukayipkacaklari.com/assets/img/og-cover.png",\n'
            '  "datePublished": "2026-09-01", "dateModified": "2026-09-01"\n'
            '}\n</script>')


def crumbnav(trail, aria):
    parts = []
    for i, (label, href) in enumerate(trail):
        if href:
            parts.append(f'<a href="{href}">{label}</a>')
        else:
            parts.append(f'<span aria-current="page">{label}</span>')
        if i < len(trail) - 1:
            parts.append('<span class="sep">/</span>')
    return f'<nav class="crumb" aria-label="{aria}">\n      ' + ''.join(parts) + '\n    </nav>'


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
        lede="Görünür bir su birikintisi çoğu kaçağın <strong>son</strong> belirtisidir. Şebeke ölçeğinde kayıp, çok daha önce verideki küçük sapmalardan okunur. İşte belediye ve sanayi içme suyu şebekelerinde en güvenilir sekiz işaret.",
        h1_en="How to tell if there is a water leak: 8 signs in a network",
        title_en="How to Tell If There Is a Water Leak? 8 Signs and How to Check | LeakExpert",
        desc_en="Signs of a hidden leak in a drinking-water network: rising night flow, pressure drop, a widening NRW gap, persistently damp ground. How is it confirmed?",
        lede_en="A visible puddle is the <strong>last</strong> sign of most leaks. At network scale, loss shows up far earlier as small deviations in the data. Here are the eight most reliable signs in municipal and industrial drinking-water networks.",
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
        body_en="""
      <div class="prose">
        <h2>1. Rising minimum night flow</h2>
        <p>The flow measured at the reservoir outlet of a zone (DMA) drops to its lowest level between 03:00 and 05:00, when demand has stopped. If this <strong>minimum night flow</strong> rises over time while population and connection count stay constant, the difference is most likely a new physical leak. This is the earliest and most objective signal in network monitoring.</p>

        <h2>2. A local pressure drop</h2>
        <p>If the pressure at the far end of a main falls gradually while pump flow is unchanged, water is leaving the system somewhere in between. A 24/7 <a href="/en/hizmetler.html#basinc">pressure logger</a> record shows that drop at hourly resolution.</p>

        <h2>3. A widening gap between water produced and water billed</h2>
        <p>The difference between the total water entering the reservoir and the water billed to customers is the <strong>non-revenue water (NRW)</strong> share. If that share is above 30% and climbing, a measurable loss has built up in the network.</p>

        <h2>4. A flow sound at one point that never stops</h2>
        <p>A continuous hiss heard even at night next to a valve, a fire hydrant or a service connection is the classic leak sound. <a href="/en/hizmetler.html#akustik">Acoustic listening</a> amplifies it with a ground microphone and locates it between two points with a correlator.</p>

        <h2>5. Ground that stays wet in dry weather, or a strip of greener grass</h2>
        <p>Edge subsidence in asphalt, moss on a pavement, soil that stays wet without rain, or a strip of grass noticeably greener than its surroundings — all are signs of a leak that has reached the surface.</p>

        <h2>6. More frequent repairs</h2>
        <p>Pipe bursts that recur at short intervals in the same area are usually linked to <strong>high or fluctuating pressure</strong>. Repairs made without introducing pressure management move the problem to a neighbouring point a few months later.</p>

        <h2>7. An unexplained rise in chlorination and pumping costs</h2>
        <p>Every cubic metre of leaking water has been treated, chlorinated and pumped. If energy and chemical consumption rise without population growth, the difference is water seeping from the network.</p>

        <h2>8. Reservoir level falling at night too</h2>
        <p>The reservoir level should stabilise once demand stops. If it keeps falling through the night, a serious leak should be sought on the transmission main between the reservoir and the first metering point.</p>

        <h2>The signs are there — now confirm the location</h2>
        <p>These signs show that a loss <em>exists</em>, not <em>where</em> it is. Locating it requires systematic field work: zoning (DMA), night-flow measurement, step testing and acoustic surveying. LeakExpert runs this cycle as a single programme and reports every point with its coordinates.</p>
        <ul>
          <li>Method detail: <a href="/en/hizmetler.html">Services</a></li>
          <li>Field examples: <a href="/en/projeler/">Projects</a></li>
          <li>Common questions: <a href="/en/sss.html">FAQ</a></li>
        </ul>
      </div>
""",
    ),
    dict(
        slug="akustik-su-kacagi-tespiti-nedir",
        h1="Akustik su kaçağı tespiti nedir, nasıl yapılır?",
        title="Akustik Su Kaçağı Tespiti Nasıl Yapılır? Yer Mikrofonu ve Korelatör | LeakExpert",
        desc="Akustik su kaçağı tespitinin adımları: gürültü kaydediciyle tarama, yer mikrofonuyla daraltma, korelatörle metrik konumlandırma. Neden gece yapılır?",
        lede="Basınçlı bir borudan kaçan su, boru cidarında ve zeminde <strong>titreşim (ses)</strong> üretir. Akustik tespit, bu sesi dinleyip kaynağına doğru daraltma sanatıdır. Tahribatsızdır; kazı yalnızca doğrulanmış noktada yapılır.",
        h1_en="What is acoustic water leak detection, and how is it done?",
        title_en="How Is Acoustic Water Leak Detection Done? Ground Microphone and Correlator | LeakExpert",
        desc_en="The steps of acoustic leak detection: survey with noise loggers, narrow down with a ground microphone, locate to the metre with a correlator. Why is it done at night?",
        lede_en="Water escaping a pressurised pipe produces <strong>vibration (sound)</strong> in the pipe wall and the ground. Acoustic detection is the craft of listening to that sound and narrowing in on its source. It is non-destructive; excavation is done only at the confirmed point.",
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
          <li>Kavram: <a href="/blog/dma-nedir.html">DMA nedir?</a></li>
          <li>Uygulanışı: <a href="/projeler/">Proje sayfaları</a></li>
        </ul>
      </div>
""",
        body_en="""
      <div class="prose">
        <h2>Why does a leak make a sound?</h2>
        <p>The pressure in the water turns into turbulence as it escapes through a hole or a crack. Depending on the pipe material, diameter, pressure and ground, that turbulence radiates a continuous sound in roughly the <strong>20–2,500 Hz</strong> range. In metal pipes the sound travels far; in plastic pipes (PE, PVC) it decays quickly, which is why measurement points are spaced more closely.</p>

        <h2>Step 1 — Preliminary zoning</h2>
        <p>The network map, valve positions and any DMA boundaries are reviewed. The area with high loss data is chosen as the priority zone to survey. If needed, the zone's minimum night flow is measured with a temporary flow logger.</p>

        <h2>Step 2 — Night survey with noise loggers</h2>
        <p><strong>Noise loggers</strong> are placed on valves and hydrants. The devices record automatically during the quietest hours of the night; points that give a continuous, high-amplitude sound are flagged as "suspect". This step quickly screens a wide area.</p>

        <h2>Step 3 — Narrowing down with a ground microphone</h2>
        <p>Along the suspect main, point-by-point listening is done from the surface with a <strong>ground microphone</strong>. The sound level rises as you approach the leak; the location of the highest reading is the leak's surface projection. A listening rod is used on valves and connections.</p>

        <h2>Step 4 — Locating to the metre with a correlator</h2>
        <p>A sensor is placed on each contact point (valve, hydrant) on either side of the leak. Using the difference in arrival time of the leak sound at the two sensors and the speed of sound in the pipe, the <strong>correlator</strong> locates the leak between the two points to <strong>within a metre</strong>. When the pipe material and diameter are entered correctly, the margin of error is very small.</p>

        <h2>Step 5 — Confirmation and hand-over</h2>
        <p>The identified point is verified with the ground microphone; its coordinates and sound level are recorded and photographed. Excavation is done only for this confirmed point. All points are entered onto the <a href="/en/hizmetler.html#cbs">GIS map</a> and the LeakExpert platform.</p>

        <h2>Why work at night?</h2>
        <p>Daytime demand, traffic and ground noise mask the leak sound. When demand stops at night the network goes quiet; the leak sound becomes relatively distinct and is picked up from much farther away.</p>

        <h2>When is it not enough on its own?</h2>
        <p>On very deep mains, large-diameter transmission pipes, high groundwater and entirely plastic new networks, the acoustic method is used together with <strong>flow/pressure measurement and step testing</strong>. That is why LeakExpert relies not on a single method but on a closed-loop programme.</p>
        <ul>
          <li>Related service: <a href="/en/hizmetler.html#akustik">Acoustic leak detection</a></li>
          <li>Concept: <a href="/en/blog/dma-nedir.html">What is a DMA?</a></li>
          <li>In practice: <a href="/en/projeler/">Project pages</a></li>
        </ul>
      </div>
""",
    ),
    dict(
        slug="dma-nedir",
        h1="DMA (İzole Ölçüm Bölgesi) nedir, nasıl kurulur?",
        title="DMA Nedir? İzole Ölçüm Bölgesi Kurulumu ve Gece Minimum Debi | LeakExpert",
        desc="DMA (District Metered Area) bir şebekeyi ölçülebilir alt bölgelere ayırır. Kurulum adımları, gece minimum debi analizi, step test ve kayıp ayrıştırma anlatımı.",
        lede="Bir şehir şebekesini bütün hâlde denetlemek zordur. <strong>DMA</strong> (District Metered Area — izole ölçüm bölgesi), şebekeyi girişi ve çıkışı sayılabilen küçük, kalıcı parçalara böler. Kayıp, ancak ölçülebildiği yerde yönetilebilir.",
        h1_en="What is a DMA (District Metered Area), and how is it set up?",
        title_en="What Is a DMA? District Metered Area Setup and Minimum Night Flow | LeakExpert",
        desc_en="A DMA (District Metered Area) splits a network into measurable sub-zones. Setup steps, minimum night flow analysis, step testing and separating out the loss.",
        lede_en="Auditing a city network as a single whole is hard. A <strong>DMA</strong> (District Metered Area) divides the network into small, permanent parts whose inflow and outflow can be counted. Loss can only be managed where it can be measured.",
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
          <li>Yol haritası: <a href="/blog/su-kaybi-dusurme-yol-haritasi.html">Su kaybını düşürme yol haritası</a></li>
        </ul>
      </div>
""",
        body_en="""
      <div class="prose">
        <h2>What does a DMA solve?</h2>
        <p>A city-wide NRW figure such as "35%" is a number, but it does not say <strong>where</strong> the loss is. When the network is split into 15–20 DMAs, each zone's own minimum night flow is monitored; the loss narrows to a few zones and the field crew is sent to the right place.</p>

        <h2>The size of a DMA</h2>
        <p>Typically <strong>500–3,000 connections</strong> or a few kilometres of main. In a DMA that is too large, small leaks disappear inside the night flow; one that is too small brings excess valve and meter cost. Size is set with regard to topography, pressure zones and natural boundaries (a stream, a main road, a railway).</p>

        <h2>Setup steps</h2>
        <h3>1. Boundary design</h3>
        <p>Zone boundaries are drawn on the network map. Every connection on the boundary is either closed permanently or converted to a metered inlet. The aim: every drop entering the zone passes through a meter.</p>
        <h3>2. Boundary valve test</h3>
        <p>The valves that must be closed are shut one by one and checked for tightness. A single boundary valve that does not seal ruins the whole measurement.</p>
        <h3>3. Inlet meter / flow meter installation</h3>
        <p>A permanent electromagnetic meter or a temporary <a href="/en/hizmetler.html#debi">ultrasonic flow meter</a> is fitted at the zone inlet; flow is logged in 15-minute steps.</p>
        <h3>4. Minimum night flow (MNF) measurement</h3>
        <p>From the minimum flow measured between 03:00 and 05:00, legitimate night use (cistern refills, industry, non-leak consumption) is subtracted. What remains is the <strong>physical loss flow</strong>. In Turkey, roughly 70% of the minimum night flow is physical loss.</p>

        <h2>Step testing — bringing the loss down to individual mains</h2>
        <p>The valves inside the DMA are closed in sequence through the night, starting from the far end. If the inlet flow drops noticeably when a valve is closed, the loss is concentrated on the main that valve feeds. The measurement area then narrows to a few hundred metres and the acoustic survey is targeted.</p>

        <h2>Permanent monitoring</h2>
        <p>A DMA is not a one-off. As the inlet meter logs continuously, the night flow rises within a few days when a new leak forms and the system gives early warning. The LeakExpert platform tracks that curve zone by zone.</p>
        <ul>
          <li>Related service: <a href="/en/hizmetler.html#dma">DMA, step &amp; zero-pressure testing</a></li>
          <li>Measurement side: <a href="/en/hizmetler.html#debi">Flow measurement &amp; NRW analysis</a></li>
          <li>Roadmap: <a href="/en/blog/su-kaybi-dusurme-yol-haritasi.html">Roadmap for cutting water loss</a></li>
        </ul>
      </div>
""",
    ),
    dict(
        slug="su-kaybi-dusurme-yol-haritasi",
        h1="Su kayıp-kaçak oranını düşürme yol haritası",
        title="Su Kayıp-Kaçak Oranını Düşürme Yol Haritası (NRW / IWA) | LeakExpert",
        desc="Fatura edilemeyen su (NRW) oranını kalıcı düşürmek için sekiz adımlı program: su dengesi, DMA, basınç yönetimi, aktif kaçak kontrolü, sayaç doğrulama.",
        lede="Su kaybını düşürmek tek seferlik bir kampanya değil, <strong>sürekli bir program</strong>dır. IWA (Uluslararası Su Birliği) çerçevesi dört kaldıraç tanımlar; sıra ve süreklilik olmadan kazanç kısa sürede geri erir.",
        h1_en="A roadmap for cutting the water loss / leakage rate",
        title_en="A Roadmap for Cutting the Water Loss Rate (NRW / IWA) | LeakExpert",
        desc_en="An eight-step programme to permanently cut the non-revenue water (NRW) rate: water balance, DMA, pressure management, active leak control, meter verification.",
        lede_en="Cutting water loss is not a one-off campaign but a <strong>continuous programme</strong>. The IWA (International Water Association) framework defines four levers; without order and continuity the gains melt away quickly.",
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
        <p>Kayıp şüphesi yüksek bir bölgede <a href="/blog/dma-nedir.html">DMA</a> kurulur, gece minimum debi ölçülür.</p>
        <h3>4. Aktif tarama</h3>
        <p>Pilot bölgede <a href="/blog/akustik-su-kacagi-tespiti-nedir.html">akustik tespit</a> + step test uygulanır, noktalar raporlanır.</p>
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
        body_en="""
      <div class="prose">
        <h2>Measure first: the IWA water balance</h2>
        <p>The water entering the system is broken down into billed consumption, unbilled legitimate consumption, apparent losses (meter error, unauthorised use) and real losses (leakage, bursts, overflows). No target can be set without this table. Output: the <strong>NRW rate</strong>, the loss volume (m³/yr) and its monetary value.</p>

        <h2>The four levers</h2>
        <ul>
          <li><strong>Pressure management</strong> — reducing excess pressure immediately lowers the leak flow and the number of new bursts.</li>
          <li><strong>Active leakage control</strong> — using DMA + acoustic surveying to find unknown leaks and repair them without delay.</li>
          <li><strong>Speed and quality of repair</strong> — the time a leak runs from detection to repair is directly a loss volume.</li>
          <li><strong>Infrastructure management</strong> — planned renewal of chronically failing mains.</li>
        </ul>

        <h2>The eight-step programme</h2>
        <h3>1. Data collection and water balance</h3>
        <p>Reservoir inlet records, customer meter readings and the network map are brought together; the baseline NRW is calculated.</p>
        <h3>2. Mapping the pressure zones</h3>
        <p>High-pressure zones are identified; pressure-reducing valve (PRV) locations are planned.</p>
        <h3>3. Pilot DMA setup</h3>
        <p>A <a href="/en/blog/dma-nedir.html">DMA</a> is set up in a zone with high suspected loss, and the minimum night flow is measured.</p>
        <h3>4. Active survey</h3>
        <p><a href="/en/blog/akustik-su-kacagi-tespiti-nedir.html">Acoustic detection</a> + step testing are applied in the pilot zone and the points are reported.</p>
        <h3>5. Fast repair cycle</h3>
        <p>Each point found is prioritised and passed to the repair crew; a check listen is done after repair.</p>
        <h3>6. Meter verification</h3>
        <p>The meters of large customers are tested; slow or stopped meters inflate apparent losses.</p>
        <h3>7. Roll-out</h3>
        <p>The method that works in the pilot is extended DMA by DMA across the city.</p>
        <h3>8. Permanent monitoring</h3>
        <p>Every DMA's night flow is monitored continuously; when a threshold is passed, the zone is surveyed again. The gain is only kept with this monitoring.</p>

        <h2>What to expect</h2>
        <p>Pressure management gives a measurable drop within weeks. Active leakage control brings a clear fall in NRW in the first year. A lasting result requires the programme to run without interruption — when it is dropped, loss climbs back a few points a year.</p>
        <ul>
          <li>Service scope: <a href="/en/hizmetler.html">Field services</a></li>
          <li>Platform support: <a href="/en/platform.html">Web + mobile platform</a></li>
          <li>Example applications: <a href="/en/projeler/">Projects</a></li>
        </ul>
      </div>
""",
    ),
]

# slug, tr_title, tr_desc, en_title, en_desc
BLOG_INDEX_ITEMS = [
    ("su-kacagi-nasil-anlasilir",
     "Su kaçağı nasıl anlaşılır?", "İçme suyu şebekesinde gizli kaybın 8 belirtisi ve nasıl doğrulandığı.",
     "How to tell if there is a water leak?", "Eight signs of hidden loss in a drinking-water network and how it is confirmed."),
    ("akustik-su-kacagi-tespiti-nedir",
     "Akustik su kaçağı tespiti nasıl yapılır?", "Gürültü kaydedici, yer mikrofonu ve korelatörle adım adım yer tespiti.",
     "How is acoustic water leak detection done?", "Step-by-step location with noise loggers, a ground microphone and a correlator."),
    ("dma-nedir",
     "DMA (İzole Ölçüm Bölgesi) nedir?", "Şebekeyi ölçülebilir bölgelere ayırmak, gece minimum debi ve step test.",
     "What is a DMA (District Metered Area)?", "Splitting the network into measurable zones, minimum night flow and step testing."),
    ("su-kaybi-dusurme-yol-haritasi",
     "Su kaybını düşürme yol haritası", "NRW / IWA çerçevesi ve sekiz adımlı kalıcı kayıp azaltma programı.",
     "A roadmap for cutting water loss", "The NRW / IWA framework and an eight-step programme for lasting loss reduction."),
]


def L(a, key, lang):
    return a[key + "_en"] if lang == "en" else a[key]


def build_article(a, lang):
    u = UI[lang]
    page_path = f"/blog/{a['slug']}.html"
    url = abs_url(lang, page_path)
    h1 = L(a, "h1", lang)
    desc = L(a, "desc", lang)
    home_abs = BASE + pfx(lang) + "/"
    guide_abs = abs_url(lang, "/blog/")
    schema = [
        breadcrumb([(u["home"], home_abs), (u["guide"], guide_abs), (h1, url)]),
        article_schema(h1, desc, url, u["guide"], u["ld_lang"]),
    ]
    hd = head(L(a, "title", lang), desc, page_path, lang, schema_blocks=schema)
    rel = [x for x in ARTICLES if x['slug'] != a['slug']][:3]
    rel_cards = "\n".join(
        f'        <a class="card" href="{rel_href(lang, "/blog/" + r["slug"] + ".html")}">'
        f'<h3>{L(r, "h1", lang)}</h3><p>{L(r, "desc", lang)[:90]}…</p></a>'
        for r in rel)
    body = f"""
<main id="main">
  <div class="wrap">
    {crumbnav([(u["home"], rel_href(lang, "/")), (u["guide"], rel_href(lang, "/blog/")), (h1, None)], u["crumb_aria"])}
  </div>

  <section class="phead">
    <div class="wrap">
      <p class="eyebrow">{u['guide_eyebrow']}</p>
      <h1>{h1}</h1>
      <p class="lede">{L(a, "lede", lang)}</p>
    </div>
  </section>

  <section class="section">
    <div class="wrap mw-900">
{L(a, "body", lang)}
    </div>
  </section>

  <section class="section section--panel">
    <div class="wrap">
      <p class="eyebrow rv">{u['rel_eyebrow']}</p>
      <h2 class="h-sec rv">{u['rel_h']}</h2>
      <div class="cards cards--3 mt-l">
{rel_cards}
      </div>
    </div>
  </section>
{cta(lang)}
</main>
"""
    write(f"{pfx(lang).lstrip('/')}/blog/{a['slug']}.html" if lang == "en" else f"blog/{a['slug']}.html",
          hd + body + footer(lang, page_path))


def build_blog_index(lang):
    u = UI[lang]
    page_path = "/blog/"
    url = abs_url(lang, page_path)
    home_abs = BASE + pfx(lang) + "/"
    items = [(s, (ten if lang == "en" else tt), (den if lang == "en" else dt))
             for s, tt, dt, ten, den in BLOG_INDEX_ITEMS]
    item_list = ", ".join(
        f'{{ "@type": "ListItem", "position": {i+1}, "url": "{abs_url(lang, "/blog/" + s + ".html")}", "name": "{t}" }}'
        for i, (s, t, d) in enumerate(items))
    schema = [
        breadcrumb([(u["home"], home_abs), (u["guide"], url)]),
        ('<script type="application/ld+json">\n{\n'
         '  "@context": "https://schema.org",\n  "@type": "CollectionPage",\n'
         f'  "name": "{u["hub_name"]}",\n'
         f'  "url": "{url}",\n  "inLanguage": "{u["ld_lang"]}",\n'
         f'  "hasPart": {{ "@type": "ItemList", "itemListElement": [ {item_list} ] }}\n'
         '}\n</script>'),
    ]
    hd = head(u["hub_title"], u["hub_desc"], page_path, lang, schema_blocks=schema, ogtype="website")
    cards = "\n".join(
        f'        <a class="card rv" href="{rel_href(lang, "/blog/" + s + ".html")}"><span class="card__ix">{i+1:02d}</span>'
        f'<h3>{t}</h3><p>{d}</p></a>'
        for i, (s, t, d) in enumerate(items))
    body = f"""
<main id="main">
  <div class="wrap">
    {crumbnav([(u["home"], rel_href(lang, "/")), (u["guide"], None)], u["crumb_aria"])}
  </div>

  <section class="phead">
    <div class="wrap">
      <p class="eyebrow">{u['guide_eyebrow']}</p>
      <h1>{u['hub_h1']}</h1>
      <p class="lede">{u['hub_lede'].replace('{P}', pfx(lang))}</p>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="cards cards--3">
{cards}
      </div>
    </div>
  </section>
{cta(lang)}
</main>
"""
    write("en/blog/index.html" if lang == "en" else "blog/index.html", hd + body + footer(lang, page_path))


if __name__ == "__main__":
    for lang in LANGS:
        for a in ARTICLES:
            build_article(a, lang)
        build_blog_index(lang)
    print("done")
