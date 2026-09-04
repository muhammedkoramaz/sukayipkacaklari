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
        "rel_eyebrow": "Blogda ayrıca", "rel_h": "İlgili yazılar.",
        "hub_title": "Su Kayıp-Kaçak Blogu — Tespit Yöntemleri, DMA, NRW | LeakExpert",
        "hub_desc": ("Su kaçağı belirtileri, akustik tespit, DMA kurulumu ve su kaybı düşürme yol haritası. "
                     "Belediye ve sanayi şebekeleri için uygulamalı blog yazıları."),
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
        "rel_eyebrow": "Also on the blog", "rel_h": "Related articles.",
        "hub_title": "Water Loss & Leakage Blog — Detection Methods, DMA, NRW | LeakExpert",
        "hub_desc": ("Leak signs, acoustic detection, DMA setup and a roadmap for cutting water loss. "
                     "Practical blog articles for municipal and industrial networks."),
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
        hero="/assets/photos/gunduz-dinleme.webp",
        hero_alt="Gündüz saha dinleme çalışması",
        hero_alt_en="Daytime field listening survey",
        date="2026-09-01",
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
        slug="debi-olcumu-nedir",
        hero="/assets/photos/debi-olcum.webp",
        hero_alt="Hat üzerinde taşınabilir ultrasonik debimetre kurulumu",
        hero_alt_en="Portable ultrasonic flow meter clamped on a main",
        h1="Debi ölçümü nedir, şebekede nasıl yapılır?",
        title="Debi Ölçümü Nedir? Şebekede Debi Nasıl Ölçülür | LeakExpert",
        desc="Şebekede debi ölçümünün amacı, taşınabilir ultrasonik/elektromanyetik debimetre ile geçici ölçüm, kalıcı bölge sayacı, gece minimum debi ve doğruluğu etkileyen etkenler.",
        lede="Kaybı yönetmek için önce <strong>ne kadar su aktığını</strong> bilmek gerekir. Debi ölçümü, bir hattan veya bölgeden birim zamanda geçen su hacmini ölçer; su kayıp-kaçak çalışmasının ilk sayısal adımıdır.",
        h1_en="What is flow measurement, and how is it done in a network?",
        title_en="What Is Flow Measurement? How Flow Is Measured in a Network | LeakExpert",
        desc_en="The purpose of network flow measurement, temporary measurement with a portable ultrasonic/electromagnetic flow meter, permanent zone meters, minimum night flow and what affects accuracy.",
        lede_en="To manage loss you first need to know <strong>how much water is flowing</strong>. Flow measurement quantifies the volume passing a main or a zone per unit time; it is the first numerical step of any water-loss programme.",
        body="""
      <div class="prose">
        <h2>Debi neden ölçülür?</h2>
        <p>Su kaybı yönetimi, ölçülemeyen bir büyüklüğü düşüremez. Bir hattan veya bölgeden birim zamanda geçen su ölçülmeden, kaybın boyutu tahmine kalır. Debi verisi, depoya basılan su ile abonelere ulaşan su arasındaki farkı sayısallaştırır ve <strong>fatura edilemeyen su (NRW)</strong> oranının temelini kurar.</p>
        <p>Bir izole ölçüm bölgesinde (DMA) giriş debisi ile bölge içindeki meşru tüketim toplamı karşılaştırıldığında, aradaki sürekli ve açıklanamayan fark fiziki kaçağa işaret eder. Ölçüm ne kadar uzun sürerse, bu fark o kadar güvenilir okunur.</p>
        <p>Gün boyunca kaydedilen debi eğrisi ayrıca bölgenin tüketim profilini çıkarır: sabah ve akşam pik saatleri, öğle düşüşü ve gecenin durgun akışı. Bu profil hem şebeke planlamasına hem de kaçak analizine girdi sağlar.</p>

        <h2>Taşınabilir ölçüm: kelepçeli ultrasonik debimetre</h2>
        <p>Geçici ölçüm kampanyalarında en yaygın araç <strong>taşınabilir ultrasonik debimetre</strong>dir. Sensörler borunun dışına kelepçeyle bağlanır; suyla temas yoktur, hat basınç altında çalışırken takılır ve servis kesintisi gerekmez. Bir bölge birkaç gün ölçülüp ekipman sonraki bölgeye taşınabilir.</p>
        <p>Doğru okuma için sensörden önce ve sonra yeterli <strong>düz boru</strong> uzunluğu bulunmalıdır — tipik olarak girişte boru çapının on katı, çıkışta beş katı kadar. Dirseğe, vanaya veya pompa çıkışına yakın montaj akış profilini bozar ve hatayı büyütür.</p>
        <p>Boru, ölçüm kesitinde tam dolu olmalıdır. Kısmen dolu bir hatta veya içinde hava yastığı bulunan noktada ultrasonik ölçüm güvenilmez sonuç verir; bu yüzden nokta seçimi ölçümün kendisi kadar önemlidir.</p>

        <h2>Kalıcı ölçüm: bölge (DMA) sayacı</h2>
        <p>Sürekli izleme için bölge girişine kalıcı bir <strong>elektromanyetik (manyetik) debimetre</strong> monte edilir. Hareketli parçası yoktur, basınç kaybı düşüktür ve geniş bir debi aralığında doğruluğunu korur; ancak montajı hattın kesilmesini gerektirir.</p>
        <p>Sayaç bir <strong>veri loggerına</strong> veya telemetri ünitesine bağlanır; akış 15 dakikalık adımlarla kaydedilir ve uzaktan okunur. Böylece her bölgenin debisi kesintisiz izlenir: yeni bir kaçak oluştuğunda gece debisi birkaç gün içinde yükselir ve sistem erken uyarı verir. Bölgeleme mantığı için <a href="/blog/dma-nedir.html">DMA nedir?</a> yazısına bakın.</p>

        <h2>Ölçüm noktası nasıl seçilir?</h2>
        <p>İdeal ölçüm noktaları şebekenin doğal kısılma yerleridir: depo veya pompa istasyonu çıkışı, bir bölgeyi besleyen tek giriş hattı veya bir DMA sınır vanası. Bu noktalarda bölgeye giren tüm su tek bir kesitten geçer ve tek ölçümle yakalanır.</p>
        <p>Seçilen kesit düz, dolu ve türbülanstan uzak olmalı; menhol veya vana odası içinde sensöre ve boruya güvenli erişim bulunmalıdır. Boru malzemesi ve gerçek iç çapı bilinmelidir, çünkü debi hesabı doğrudan kesit alanına dayanır.</p>

        <h2>Gece minimum debisi</h2>
        <p>Tüketimin neredeyse durduğu gece <strong>03:00–05:00</strong> arasında ölçülen en düşük akışa gece minimum debisi denir. Bu değerin büyük bölümü meşru gece kullanımı değil, sürekli akan fiziki kaçaktır.</p>
        <p>Abone sayısı ve nüfus sabitken gece minimum debisi zamanla yükseliyorsa, artış neredeyse her zaman yeni bir fiziki kaçaktır. Bu nedenle gece debisi, şebeke izlemede en erken ve en nesnel sinyaldir. Bölge içinde kaybı hat bazına indirmek için <a href="/blog/adim-testi-nedir.html">adım (step) testi</a> uygulanır; kavramsal çerçeve için <a href="/blog/dma-nedir.html">DMA nedir?</a> yazısına bakın.</p>

        <h2>Doğruluğu ne etkiler?</h2>
        <p>Ultrasonik ölçümde en büyük hata kaynağı yanlış girilen boru iç çapı ve malzemesidir; cihaz borudaki ses hızını bu verilerden hesaplar. Birkaç milimetrelik çap hatası bile debide yüzde birkaçlık sapmaya dönüşür.</p>
        <p>Borudaki hava kabarcıkları, kısmen dolu kesit, sensör ile boru arasında yetersiz temas (kir, pas, kalın boya) ve kurumuş temas jeli sinyali zayıflatır. Elektromanyetik sayaçta ise düşük su iletkenliği, topraklama sorunu ve boru içi kaplamanın bozulması okuma hatası yaratır.</p>
        <p>Her iki teknolojide de periyodik kalibrasyon ve montaj sonrası bağımsız bir yöntemle (örneğin depo seviye düşüş testiyle) çapraz kontrol önerilir.</p>

        <h2>Ölçümden sonuca</h2>
        <p>Toplanan debi kayıtları LeakExpert platformuna işlenir; her bölgenin gece minimum debisi, tüketim profili ve NRW payı birlikte değerlendirilir. Kayıp yoğun bölgeler önceliklendirilir ve saha ekibi akustik tarama ile step test için doğru bölgeye yönlendirilir. Debi ölçümü tek seferlik bir işlem değil, sürekli tekrarlanan bir izleme döngüsüdür.</p>
        <ul>
          <li>Yöntemin ayrıntısı: <a href="/hizmetler.html">Hizmetler</a></li>
          <li>Saha örnekleri: <a href="/projeler/">Projeler</a></li>
          <li>Sık sorulanlar: <a href="/sss.html">SSS</a></li>
        </ul>
      </div>
""",
        body_en="""
      <div class="prose">
        <h2>Why measure flow?</h2>
        <p>Water-loss management cannot reduce a quantity it does not measure. Until the water passing a main or a zone per unit time is measured, the size of the loss is left to guesswork. Flow data quantifies the gap between the water pumped into the reservoir and the water reaching customers, and it forms the basis of the <strong>non-revenue water (NRW)</strong> rate.</p>
        <p>When the inflow of a District Metered Area (DMA) is compared with the sum of legitimate consumption inside it, a continuous, unexplained difference points to physical leakage.</p>
        <p>The flow curve recorded through the day also produces the zone's consumption profile: the morning and evening peaks, the midday dip and the still flow of the night. That profile feeds both network planning and leak analysis.</p>

        <h2>Temporary measurement: the clamp-on ultrasonic flow meter</h2>
        <p>The most common tool in temporary measurement campaigns is the <strong>portable ultrasonic flow meter</strong>. The sensors are clamped to the outside of the pipe; there is no contact with the water, the meter is fitted while the main stays under pressure, and no service interruption is needed.</p>
        <p>For a correct reading there must be enough <strong>straight pipe</strong> before and after the sensor — typically ten pipe diameters upstream and five downstream. Mounting close to a bend, a valve or a pump outlet distorts the flow profile and widens the error.</p>
        <p>The pipe must be completely full at the measuring section. On a partly filled main, or at a point with an air pocket, an ultrasonic reading is unreliable; this is why choosing the point matters as much as the measurement itself.</p>

        <h2>Permanent measurement: the zone (DMA) meter</h2>
        <p>For continuous monitoring a permanent <strong>electromagnetic flow meter</strong> is installed at the zone inlet. It has no moving parts, its pressure loss is low and it holds its accuracy across a wide flow range; its installation, however, requires the main to be cut.</p>
        <p>The meter is connected to a <strong>data logger</strong> or a telemetry unit; flow is logged in 15-minute steps and read remotely. Each zone's flow is then monitored without interruption: when a new leak forms, the night flow rises within a few days and the system gives early warning. For the logic of zoning, see <a href="/en/blog/dma-nedir.html">What is a DMA?</a></p>

        <h2>How is the measuring point chosen?</h2>
        <p>The ideal measuring points are the network's natural constrictions: the outlet of a reservoir or a pumping station, the single feed main into a zone, or a DMA boundary valve. At these points all the water entering the zone passes through one section.</p>
        <p>The chosen section must be straight, full and clear of turbulence, and there must be safe access to the sensor and the pipe inside a manhole or valve chamber. The pipe material and the true internal diameter must be known, because the flow calculation rests directly on the cross-sectional area.</p>

        <h2>Minimum night flow</h2>
        <p>The lowest flow measured between <strong>03:00 and 05:00</strong>, when consumption has almost stopped, is the minimum night flow. Most of this value is not legitimate night use but continuously running physical leakage.</p>
        <p>If the minimum night flow rises over time while connection count and population stay constant, the increase is almost always a new physical leak. This makes night flow the earliest and most objective signal in network monitoring. To bring the loss down to individual mains within a zone, a <a href="/en/blog/adim-testi-nedir.html">step test</a> is used; for the conceptual framework, see <a href="/en/blog/dma-nedir.html">What is a DMA?</a></p>

        <h2>What affects accuracy?</h2>
        <p>In ultrasonic measurement the biggest source of error is a wrongly entered pipe internal diameter and material; the device computes the speed of sound in the pipe from these values. Even a few millimetres of diameter error turns into a deviation of a few per cent in flow.</p>
        <p>Air bubbles in the pipe, a partly filled section, poor contact between the sensor and the pipe (dirt, rust, thick paint) and dried coupling gel all weaken the signal. On an electromagnetic meter, low water conductivity, an earthing fault and a degraded internal lining produce reading errors.</p>
        <p>For both technologies, periodic calibration and a cross-check against an independent method after installation (a reservoir level-drop test, for example) are recommended.</p>

        <h2>From measurement to result</h2>
        <p>The flow records collected are entered into the LeakExpert platform; each zone's minimum night flow, consumption profile and NRW share are assessed together. Zones with heavy loss are prioritised and the field crew is directed to the right zone for acoustic surveying and step testing. Flow measurement is not a one-off task but a monitoring cycle that repeats continuously.</p>
        <ul>
          <li>Method detail: <a href="/en/hizmetler.html">Services</a></li>
          <li>Field examples: <a href="/en/projeler/">Projects</a></li>
          <li>Common questions: <a href="/en/sss.html">FAQ</a></li>
        </ul>
      </div>
""",
    ),
    dict(
        slug="basinc-yonetimi-nedir",
        hero="/assets/photos/basinc-logger.webp",
        hero_alt="Hat üzerinde basınç veri loggerı",
        hero_alt_en="Pressure data logger on a main",
        h1="Basınç yönetimi ve basınç bölgeleri (PMA)",
        title="Basınç Yönetimi Nedir? Basınç Bölgeleri ve PMA | LeakExpert",
        desc="Şebekede yüksek ve dalgalı basıncın kaçak ve patlaklarla ilişkisi, basınç bölgesi (PMA) kurulumu, basınç düşürücü vana ve sabit/zaman/akış kontrollü ayar.",
        lede="Şebekedeki her fazla metre basınç, hem yeni patlak riskini hem de mevcut kaçakların debisini artırır. <strong>Basınç yönetimi</strong>, şebekeyi gerektiği kadar — ne fazla, ne eksik — basınçta tutma işidir.",
        h1_en="Pressure management and pressure zones (PMA)",
        title_en="What Is Pressure Management? Pressure Zones and PMA | LeakExpert",
        desc_en="How high and fluctuating pressure drives leaks and bursts, setting up a pressure managed area (PMA), and fixed/time/flow-modulated PRV control.",
        lede_en="Every extra metre of pressure in a network raises both the risk of new bursts and the flow rate of existing leaks. <strong>Pressure management</strong> is the work of keeping the network at just the pressure it needs — no more, no less.",
        body="""
      <div class="prose">
        <h2>Basınç ile kaçak arasındaki ilişki</h2>
        <p>Basınçlı bir borudaki her açıklıktan — mikro çatlak, gevşemiş conta, korozyon deliği — kaçan su debisi, hattaki basınçla birlikte artar. Bu ilişki doğrusal değildir: kaçak debisi, basıncın <strong>N1 üssü</strong> ile orantılı kabul edilir (FAVAD yaklaşımı). N1 genellikle 0,5 ile 1,5 arasındadır; rijit borulardaki sabit alanlı delik ve çatlaklarda ~0,5'e, esnek (plastik) borulardaki arka plan sızıntılarında ~1'e, açıklığın basınçla genişlediği durumlarda daha yükseğe çıkar. Karışık bir şebekede pratik değer 1 civarındadır; yani ortalama basıncı %15 düşürmek, mevcut kaçak debisini kabaca %15 azaltır.</p>
        <p>Basıncın ikinci etkisi yeni patlaklar üzerinedir. Yüksek ortalama basınç ve özellikle pompa/vana manevralarından doğan <strong>basınç dalgalanmaları (transiyentler)</strong> boru ve bağlantılarda yorulmayı hızlandırır; arıza sıklığı artar. Basıncı hem düşürmek hem de gün içinde sabit tutmak, kırılma hızını kalıcı biçimde aşağı çeker. Bu yüzden basınç yönetimi, <a href="/blog/su-kaybi-dusurme-yol-haritasi.html">su kaybını düşürme programının</a> ilk ve en hızlı geri dönüşlü adımıdır.</p>

        <h2>Basınç bölgesi (PMA) nedir?</h2>
        <p>Basınç bölgesi (PMA — Pressure Managed Area), kot ve besleme yönü bakımından birbirine benzeyen, sınırları kapalı vanalarla belirlenmiş ve tek bir noktadan beslenen şebeke parçasıdır. Alan içindeki bağlantıların yer aldığı kot aralığı dar tutulur; böylece girişte ayarlanan tek bir çıkış basıncı, bölgenin tamamına kabul edilebilir sınırlar içinde hizmet verir.</p>
        <p>Basınç bölgesi çoğu zaman bir <a href="/blog/dma-nedir.html">izole ölçüm bölgesiyle (DMA)</a> çakışır veya onun içine yerleşir: aynı kapalı sınır hem debiyi sayılabilir kılar hem de basıncı tek girişten yönetmeye izin verir. Geniş bir kot farkı varsa alan, her biri kendi hedef basıncına sahip birden çok bölgeye ayrılır.</p>

        <h2>Basınç düşürücü vana</h2>
        <p>Bölge girişine bir <strong>basınç düşürücü vana</strong> konur. Bu, pilot devresiyle çalışan, kendinden tahrikli bir hidrolik kontrol vanasıdır: giriş basıncı ve debi değişse de kısılma oranını sürekli ayarlayarak çıkış basıncını belirlenen hedefte tutar. Marka veya modelden bağımsız olarak temel işlev aynıdır — bölgeye giren suyun basıncını ihtiyaç duyulan değere indirmek ve orada sabitlemek.</p>
        <p>Vana bir <strong>basınç veri loggerına</strong> bağlanır; giriş ve çıkış basıncı ile bölge debisi kaydedilir. Bu kayıt hem ayarın doğru çalıştığını gösterir hem de aşağıdaki kontrol tiplerinin uygulanmasına zemin hazırlar.</p>

        <h2>Ayar tipleri</h2>
        <p><strong>Sabit çıkış:</strong> Vana, giriş koşulları ne olursa olsun tek bir çıkış basıncını korur. Kurulumu en basit yöntemdir; ancak hedef, gün içindeki en yüksek talep anına göre seçilmek zorunda olduğundan, talebin düştüğü saatlerde bölge hâlâ gereğinden yüksek basınçta kalır.</p>
        <p><strong>Zaman kontrollü:</strong> Bir kontrol ünitesi, çıkış hedefini tanımlı saat aralıklarına göre değiştirir — tipik olarak gece talep düşükken daha düşük, sabah ve akşam piklerinde daha yüksek. Ek donanımı azdır; fakat gerçek talebi değil saati izlediğinden, tüketim beklenen desenden saparsa ayar da sapar.</p>
        <p><strong>Akış kontrollü:</strong> Çıkış hedefi, vanadan geçen ölçülü debinin bir fonksiyonu olarak sürekli değişir. Talep azaldıkça basınç düşer, arttıkça yükselir; kritik nokta her an tam yeterli basınçta tutulur, fazlası bölgeye verilmez. Kaçak azaltmada en etkili yöntemdir, karşılığında bir debimetre ve daha yetenekli bir kontrol ünitesi gerektirir.</p>

        <h2>Hedef basınç nasıl belirlenir?</h2>
        <p>Hedef, bölgenin ortalamasına göre değil <strong>en kritik abonesine</strong> göre seçilir: en yüksek kottaki veya besleme noktasından en uzak bağlantı. Bu noktada, en yüksek talep anında bile korunması gereken bir <strong>asgari servis basıncı</strong> vardır — idarenin bağlantı noktası için tanımladığı alt sınır.</p>
        <p>Giriş hedefi geriye doğru hesaplanır: kritik noktadaki asgari servis basıncı, artı kritik noktayla giriş arasındaki kot farkı, artı en yüksek debideki sürtünme kayıpları, artı bir güvenlik payı. Hesap, kritik noktaya yerleştirilen bir basınç loggerıyla tam bir talep çevrimi boyunca saha verisiyle doğrulanır; ayar, ölçülen en düşük değere göre ince ayarlanır.</p>

        <h2>Kazanç nasıl ölçülür?</h2>
        <p>Ölçüt, ayar öncesi ve sonrasının karşılaştırılmasıdır. Birincil gösterge bölgenin <strong>gece minimum debisidir</strong>: basınç düştüğünde gece debisi birkaç gün içinde ölçülebilir biçimde geriler. İkincil gösterge, benzer uzunluktaki dönemlerde bölgedeki <strong>patlak ve arıza sayısıdır</strong>; basınç sabitlendikçe bu sayı da düşer.</p>
        <p>Bunun için giriş ve kritik noktadaki loggerlar kalıcı bırakılır. Basınçtaki düşüşün korunduğu ve gece debisinin yeniden tırmanmadığı sürekli izlenir; eşik aşıldığında bölge yeniden taranır. Basınç yönetiminin kazancı ancak bu izlemeyle kalıcı olur.</p>

        <h2>Tasarımın doğrulanması</h2>
        <p>Sahadan toplanan basınç ve debi kayıtları — giriş, kritik nokta ve ara düğümler — kalibre edilmiş bir <a href="/blog/hidrolik-modelleme-nedir.html">hidrolik modele</a> işlenir. Model, tüm talep senaryolarında her düğümün asgari basıncın üzerinde kaldığını kontrol eder, vananın boyutunu ve kavitasyon riskini değerlendirir, zaman ve akış kontrollü profilleri sınar ve manevralardan doğacak dalgalanmaları öngörür.</p>
        <p>Bu doğrulama, ayarın yalnızca ortalama koşullarda değil uç durumlarda da güvenli olduğunu gösterir. LeakExpert; saha ölçümü, model ve kalıcı izlemeyi tek programda yürütür ve her bölgenin hedef basıncını, gece debisini ve arıza geçmişini birlikte raporlar.</p>
        <ul>
          <li>Yöntemin ayrıntısı: <a href="/hizmetler.html">Hizmetler</a></li>
          <li>Saha örnekleri: <a href="/projeler/">Projeler</a></li>
          <li>Sık sorulanlar: <a href="/sss.html">SSS</a></li>
        </ul>
      </div>
""",
        body_en="""
      <div class="prose">
        <h2>The link between pressure and leakage</h2>
        <p>The flow escaping any opening in a pressurised pipe — a hairline crack, a loosened joint, a corrosion hole — rises with the pressure in the main, and not linearly: leak flow is taken to vary with pressure raised to the power <strong>N1</strong> (the FAVAD approach). N1 usually lies between 0.5 and 1.5 — near 0.5 for fixed-area holes and cracks in rigid pipe, near 1 for background leakage in flexible (plastic) pipe, higher where the opening widens with pressure. In a mixed network the practical value is around 1, so cutting the average pressure by 15% cuts the existing leak flow by roughly 15%.</p>
        <p>Pressure has a second effect, on new bursts. High average pressure, and above all the <strong>pressure transients</strong> caused by pump and valve operations, accelerate fatigue in pipes and joints, so the break frequency rises. Lowering the pressure and holding it steady through the day drive the break rate permanently down. This is why pressure management is the first and fastest-returning step of a <a href="/en/blog/su-kaybi-dusurme-yol-haritasi.html">water-loss reduction programme</a>.</p>

        <h2>What is a pressure managed area (PMA)?</h2>
        <p>A pressure managed area (PMA) is a part of the network similar in elevation and supply direction, bounded by closed valves and fed from a single point. The range of ground levels across its connections is kept narrow, so that one outlet pressure set at the inlet serves the whole area within acceptable limits.</p>
        <p>A PMA often coincides with, or sits inside, a <a href="/en/blog/dma-nedir.html">District Metered Area (DMA)</a>: the same closed boundary that makes flow countable also allows pressure to be managed from one inlet. Where the elevation range is wide, the area is split into several zones, each with its own target pressure.</p>

        <h2>The pressure reducing valve</h2>
        <p>A <strong>pressure reducing valve (PRV)</strong> is fitted at the zone inlet. It is a self-operated hydraulic control valve driven by a pilot circuit: it continuously adjusts how far it throttles so that the downstream pressure holds at a chosen target even as the inlet pressure and the flow change. Independent of make or model, the function is the same — bring the pressure of the water entering the zone down to what is needed and hold it there.</p>
        <p>The valve is connected to a <strong>pressure data logger</strong> recording the inlet and outlet pressure and the zone flow. This record shows the setting is working and is the basis for the control modes described next.</p>

        <h2>Control modes</h2>
        <p><strong>Fixed outlet:</strong> the valve holds a single downstream pressure whatever the inlet conditions. It is the simplest to commission; but because the target must suit the moment of highest daily demand, the zone stays at more pressure than it needs when demand falls.</p>
        <p><strong>Time-modulated:</strong> a controller changes the outlet target by defined time bands — lower at night when demand is low, higher at the morning and evening peaks. It needs little extra hardware; but because it follows the clock rather than real demand, the setting drifts if consumption departs from the expected pattern.</p>
        <p><strong>Flow-modulated:</strong> the outlet target varies continuously as a function of the measured flow through the valve. As demand falls the pressure falls, as it rises the pressure rises; the critical point is kept at just-adequate pressure at all times. It is the most effective mode for cutting leakage, and in return it needs a flow meter and a more capable controller.</p>

        <h2>How is the target pressure set?</h2>
        <p>The target is chosen not for the zone average but for its <strong>critical point</strong>: the connection at the highest elevation, or the farthest from the feed. At that point a <strong>minimum service pressure</strong> must be preserved even at the moment of highest demand — the lower limit the utility defines for the connection point.</p>
        <p>The inlet target is worked back from it: the minimum service pressure at the critical point, plus the elevation difference to the inlet, plus the friction losses at peak flow, plus a safety margin. It is then verified with a pressure logger at the critical point over a full demand cycle, and the setting is trimmed to the lowest value recorded.</p>

        <h2>How is the gain measured?</h2>
        <p>The measure is a before-and-after comparison. The primary indicator is the zone's <strong>minimum night flow</strong>: when the pressure drops, it falls measurably within a few days. The secondary indicator is the <strong>count of bursts and failures</strong> over periods of similar length; as the pressure steadies, that count falls too.</p>
        <p>For this the loggers at the inlet and the critical point are left in place. That the pressure reduction holds and the night flow does not climb again is monitored continuously; when a threshold is passed, the zone is surveyed again. The gain only lasts with this monitoring.</p>

        <h2>Validating the design</h2>
        <p>The pressure and flow records collected in the field — at the inlet, the critical point and intermediate nodes — are entered into a calibrated <a href="/en/blog/hidrolik-modelleme-nedir.html">hydraulic model</a>. The model checks that every node stays above the minimum pressure under all demand scenarios, assesses the valve size and the cavitation risk, tests the time- and flow-modulated profiles, and predicts the transients that operations would produce.</p>
        <p>This validation shows the setting is safe not only in average conditions but at the extremes. LeakExpert runs field measurement, modelling and permanent monitoring as one programme, reporting each zone's target pressure, night flow and failure history together.</p>
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
        hero="/assets/photos/gece-dinleme-hero.webp",
        hero_alt="Gece akustik dinleme",
        hero_alt_en="Night-time acoustic listening",
        date="2026-09-01",
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
        hero="/assets/photos/dma-tasarim.webp",
        hero_alt="DMA sınır ve sayaç tasarımı",
        hero_alt_en="DMA boundary and meter design",
        date="2026-09-01",
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
        slug="adim-testi-nedir",
        hero="/assets/photos/gece-operasyon.webp",
        hero_alt="Gece saha operasyonu",
        hero_alt_en="Night-time field operation",
        date="2026-09-04",
        h1="Adım (step) testi ile kaçak bölgeleme",
        title="Adım (Step) Testi Nedir? Gece Kademeli Vana Kapatma | LeakExpert",
        desc="Adım testi, bir DMA içinde gece vanaları kademeli kapatarak debi düşüşlerinden kaybın hangi alt hatta yoğunlaştığını bulur.",
        lede="Bir bölgede kayıp olduğunu bilmek yetmez; <strong>hangi sokakta</strong> olduğunu daraltmak gerekir. Adım testi, gece boyunca vanaları sırayla kapatıp her adımda debinin ne kadar düştüğüne bakarak kaybı alt hatlara böler.",
        h1_en="Step testing to narrow down leakage",
        title_en="What Is a Step Test? Night-time Stepped Valve Closing | LeakExpert",
        desc_en="A step test closes valves in sequence at night within a DMA and reads the flow drops to find which sub-section holds the loss.",
        lede_en="Knowing a zone has loss is not enough; you need to narrow down <strong>which street</strong> it is on. A step test closes valves one by one through the night and watches how much flow drops at each step, splitting the loss between sub-sections.",
        body="""
      <div class="prose">
        <h2>Adım testinin amacı</h2>
        <p>Bir <a href="/blog/dma-nedir.html">izole ölçüm bölgesinde (DMA)</a> gece minimum debisi yüksek çıktığında, o bölgede fiziki kayıp olduğu bilinir; ama kaybın bölgenin hangi sokağında yoğunlaştığı bilinmez. Adım (step) testi, bu belirsizliği gidermek için bölgeyi geçici olarak küçük alt parçalara böler ve her parçanın debiye katkısını tek tek ölçer.</p>
        <p>Yöntemin çıktısı, kaybın büyük bölümünü barındıran birkaç yüz metrelik hat parçalarının sıralı bir listesidir. Bu liste olmadan akustik ekip kilometrelerce hattı nokta nokta dinlemek zorunda kalır. Adım testi tarama alanını daralttığı için <a href="/blog/akustik-su-kacagi-tespiti-nedir.html">akustik tespit</a> hem hızlanır hem de isabet oranı yükselir. Kısacası adım testi kaçağı bulmaz; kaçağın aranacağı yeri belirler.</p>

        <h2>Ön hazırlık</h2>
        <p>Testin güvenilirliği hazırlığa bağlıdır. İlk gereksinim güncel bir şebeke haritasıdır: hatların çapı, malzemesi, bağlantı yönü ve bölge içindeki tüm vanaların konumu. Harita eksikse, kapatılan vananın hangi hattı beslediği yorumlanamaz ve basamaklar anlamını yitirir.</p>
        <p>Haritadan bir vana listesi ve kapatma sırası çıkarılır; sıra, bölgenin en uç noktasından girişe doğru ilerler. Listedeki her vana testten önce gündüz denenir: tam kapanıyor mu, mili sağlam mı, kutusu erişilebilir mi. Kapanmayan veya sızdıran bir vana, o adımın debisini olduğundan düşük gösterir.</p>
        <p>Test, meşru tüketimin en düşük olduğu gece penceresinde, tipik olarak 01:00–04:00 arasında yapılır. Bu saatte abone kullanımı debinin küçük bir bölümüdür, dolayısıyla basamaklar büyük ölçüde kaçağı yansıtır. Bölgedeki aboneler kısa süreli kesinti olabileceği konusunda önceden bilgilendirilir; sürekli su gerektiren kullanıcılar varsa test planı buna göre ayarlanır.</p>

        <h2>Uygulama: vanaları sondan başa kapatmak</h2>
        <p>Bölge girişindeki debimetre bütün test boyunca kesintisiz kayıt alır; genellikle birkaç saniyelik, en fazla birkaç dakikalık adımlarla. Ekip, hazırlanan sıraya göre en uçtaki vanadan başlayarak vanaları tek tek kapatır. Her kapatma yavaş yapılır: ani kapama, hatta basınç darbesi yaratır ve tortuyu kaldırır.</p>
        <p>Bir vana kapatıldıktan sonra debinin yeni bir dengeye oturması beklenir; boru ve bağlantı hacmi doldukça akış birkaç dakika içinde sabitlenir ve okuma ancak bundan sonra alınır. Kaydedilen değer, o vananın ötesindeki tüm hat kesildiğinde girişten hâlâ akan debidir. Sonra sıradaki vana kapatılır ve aynı bekleme tekrarlanır; böylece bölge girişe doğru adım adım küçülür.</p>

        <h2>Debi basamaklarının okunması</h2>
        <p>Test bitince elde edilen veri, her vana kapatmasına karşılık gelen bir debi düşüşü dizisidir. Bir adımdaki düşüş, o vananın yeni izole ettiği hat parçasının o an taşıdığı akıştır. Gece meşru tüketim küçük olduğundan bu akışın büyük bölümü fiziki kayıp kabul edilir.</p>
        <p>Büyük bir basamak — tek bir vana kapatıldığında giriş debisinin belirgin biçimde düşmesi — o alt hatta yoğun bir kaçak olduğunu gösterir. Küçük bir basamak ise o parçanın görece sağlam olduğunu, üzerindeki kaybın düşük olduğunu söyler. Basamakların toplamı, bölge girişindeki toplam gece debisiyle tutarlı olmalıdır; büyük bir tutarsızlık kapanmayan bir vanaya veya kaçırılan bir bağlantıya işaret eder ve testin ilgili bölümü tekrarlanır.</p>
        <p>Adım testi bir konum değil, bir dağılım verir: kaybın hangi parçada olduğunu birkaç yüz metreye indirir, o parçanın neresinde olduğunu söylemez. Sayısal değerler de kesin debi ölçümü değil, göreli büyüklük karşılaştırmasıdır; sıcaklık, basınç ve vana sızıntısı sonuçları etkiler.</p>

        <h2>Yorumlama ve sonraki adım</h2>
        <p>Basamaklar büyükten küçüğe sıralanır ve yüksek kayıplı alt hatlar bir öncelik listesine dönüştürülür. Bu liste, hat parçasının uzunluğu, malzemesi ve arıza geçmişiyle birlikte akustik ekibe verilir. Ekip, en yüksek kayıplı parçadan başlayarak <a href="/blog/akustik-su-kacagi-tespiti-nedir.html">yer mikrofonu ve korelatörle</a> noktasal tespite geçer.</p>
        <p>Kayıp birden çok parçaya dağılmışsa, her biri ayrı bir saha görevi olarak planlanır. Onarım sonrası bölgenin gece minimum debisi yeniden ölçülür; düşüş beklenen mertebede değilse adım testi tekrarlanarak kalan kaybın yeri daraltılır. Bu döngü, bölge hedeflenen kayıp seviyesine inene kadar sürer. Ölçüm tarafının ayrıntısı için <a href="/blog/debi-olcumu-nedir.html">debi ölçümü</a> yazısına bakılabilir.</p>

        <h2>Riskler ve önlemler</h2>
        <p>Adım testi şebekeyi bir süre alışılmadık bir düzende çalıştırdığı için birkaç riski vardır. Vanaların kapatılıp açılmasıyla akış hızı ve yönü değişir; borudaki tortu hareketlenerek suda bulanıklık ve renk oluşturabilir. Yavaş manevra ve gerekirse test sonrası hattın yıkanması bu etkiyi sınırlar. Hızlı kapamalar ayrıca basınç dalgalanması (transiyent) yaratır ve zayıf bağlantıları zorlar.</p>
        <p>Bölge parçalara ayrıldıkça bazı kesimler geçici olarak beslemesiz kalır; bu süre içinde yangın suyu ihtiyacı doğarsa müdahale gecikebilir. Test planı itfaiye erişimini gözetmeli, kesinti pencereleri kısa tutulmalı ve ekip hızlı yeniden besleme için hazır olmalıdır. En sık yapılan ve en sinsi hata, test sonunda bir vananın kapalı unutulmasıdır; bu, kalıcı bir tek yönlü besleme ve düşük basınç bölgesi yaratır.</p>
        <p>Bu yüzden kapatmalar daima yavaş yapılır, kapatılan her vana bir kontrol listesine işlenir ve test biter bitmez tüm vanalar ters sırada açılır. Her vananın tam açıldığı, mil turu sayılarak veya hat basıncının geri geldiği görülerek teyit edilir. Ekip sahadan ayrılmadan önce bölgenin normal debisi ve basıncı eski değerlerine döndüğü doğrulanır.</p>
        <ul>
          <li>Yöntemin ayrıntısı: <a href="/hizmetler.html">Hizmetler</a></li>
          <li>Saha örnekleri: <a href="/projeler/">Projeler</a></li>
          <li>Sık sorulanlar: <a href="/sss.html">SSS</a></li>
        </ul>
      </div>
""",
        body_en="""
      <div class="prose">
        <h2>The purpose of a step test</h2>
        <p>When the minimum night flow of a <a href="/en/blog/dma-nedir.html">District Metered Area (DMA)</a> comes out high, physical loss in that zone is established, but not which street it is concentrated on. A step test divides the zone temporarily into small sub-sections and measures each one's contribution to the flow in turn.</p>
        <p>The output is an ordered list of a few-hundred-metre lengths of main that hold most of the loss. Without it, the acoustic crew must listen point by point along kilometres of pipe. Because a step test narrows the search area, <a href="/en/blog/akustik-su-kacagi-tespiti-nedir.html">acoustic detection</a> becomes faster and more accurate. A step test does not find the leak; it decides where to look for it.</p>

        <h2>Preparation</h2>
        <p>The reliability of the test rests on preparation. The first requirement is an up-to-date network map: pipe diameter, material, direction of supply and the position of every valve inside the zone. If the map is incomplete, there is no way to tell which main a closed valve feeds, and the steps lose their meaning.</p>
        <p>From the map, a valve list and a closing order are drawn up, working from the far end of the zone back toward the inlet. Every valve on the list is tried in daylight first: does it close fully, is its spindle sound, is its chamber accessible. A valve that will not close, or that passes water, makes that step's flow read lower than it is.</p>
        <p>The test is run in the night window when legitimate demand is lowest, typically between 01:00 and 04:00, so the steps largely reflect leakage rather than customer use. Customers are told in advance of a possible brief interruption; where users need water continuously, the plan is arranged around them.</p>

        <h2>Execution: closing valves from the far end back</h2>
        <p>The flow meter at the zone inlet logs continuously through the test, in steps of a second or two, at most a few minutes. Working through the prepared order, the crew closes the valves one at a time, starting at the far end. Each closure is made slowly: a sudden shut-off sends a pressure surge through the main and lifts sediment.</p>
        <p>After a valve is closed, the flow is left to settle to a new balance; as the pipe volume fills, it steadies within a few minutes, and the reading is taken only then. The value recorded is the flow still passing the inlet once everything beyond that valve is cut off. The next valve is closed and the wait repeated, so the zone shrinks step by step toward the inlet.</p>

        <h2>Reading the flow steps</h2>
        <p>The finished test leaves a series of flow drops, one per valve closure. The drop at a step is the flow the length of main just isolated by that valve was carrying at that moment. Because legitimate night use is small, most of it is taken to be physical loss.</p>
        <p>A large step — the inlet flow falling markedly when one valve is closed — shows a heavy leak on that sub-section; a small step says that length is relatively sound. The steps should sum to the total night flow at the inlet; a large mismatch points to a valve that did not close or a connection that was missed, and that part of the test is repeated.</p>
        <p>A step test gives a distribution, not a position. It brings the loss down to which length of main, within a few hundred metres, not to where on that length. The figures compare relative magnitude rather than measure flow precisely — temperature, pressure and valve leakage all affect the result.</p>

        <h2>Interpretation and the next step</h2>
        <p>The high-loss sub-sections are ordered into a priority list, with each length's material and failure history, and handed to the acoustic crew. Starting from the highest-loss length, they move to pinpoint location with a <a href="/en/blog/akustik-su-kacagi-tespiti-nedir.html">ground microphone and a correlator</a>.</p>
        <p>Where the loss is spread over several lengths, each is planned as a separate field task. After repair, the zone's minimum night flow is measured again; if the drop falls short of expectation, the step test is repeated to narrow the remaining loss. The cycle continues until the zone reaches its target loss level. For the measurement side, see the <a href="/en/blog/debi-olcumu-nedir.html">flow measurement</a> article.</p>

        <h2>Risks and precautions</h2>
        <p>Because a step test runs the network in an unusual configuration for a while, it carries risks. Closing and opening valves changes flow velocity and direction; sediment in the pipe is disturbed and can cause discolouration. Slow operation, and flushing the main afterwards if needed, limit this. Fast closures also create pressure transients that stress weak joints.</p>
        <p>As the zone is split up, some parts are left unfed for a time; if a fire-flow demand arises then, response can be delayed. The plan must allow for fire-service access and keep interruption windows short. The most insidious mistake is leaving a valve shut at the end, which creates a permanent one-way feed and a low-pressure pocket.</p>
        <p>For this reason every closed valve is entered on a checklist, and as soon as the test ends all valves are reopened in reverse order. Each is confirmed fully open by counting spindle turns or seeing the line pressure return. Before the crew leaves, the zone's normal flow and pressure are verified to have returned to their earlier values.</p>
        <ul>
          <li>Method detail: <a href="/en/hizmetler.html">Services</a></li>
          <li>Field examples: <a href="/en/projeler/">Projects</a></li>
          <li>Common questions: <a href="/en/sss.html">FAQ</a></li>
        </ul>
      </div>
""",
    ),
    dict(
        slug="sifir-basinc-testi-nedir",
        hero="/assets/blog/sifir-basinc-testi-nedir.webp",
        hero_alt="Vana odasında hat izolasyonu",
        hero_alt_en="Line isolation at a valve chamber",
        date="2026-09-04",
        h1="Sıfır basınç testi nedir?",
        title="Sıfır Basınç Testi Nedir? Hat İzolasyon Kontrolü | LeakExpert",
        desc="Sıfır basınç testi, izole edilen bir hat bölümünde basıncı sıfıra indirip basıncın geri gelip gelmediğine bakarak o bölümde kaçak olup olmadığını doğrular.",
        lede="Bazen bir hat bölümünden şüphelenilir ama kesin karar verilemez. <strong>Sıfır basınç testi</strong>, o bölümü izole edip basıncını sıfıra düşürür: basınç yavaşça geri geliyorsa içeride hâlâ su besleyen bir yol — çoğu zaman bir kaçak — vardır.",
        h1_en="What is a zero-pressure test?",
        title_en="What Is a Zero-Pressure Test? Line Isolation Check | LeakExpert",
        desc_en="A zero-pressure test isolates a section of main, drops its pressure to zero and watches whether pressure returns, confirming whether that section leaks.",
        lede_en="Sometimes a section of main is suspected but cannot be ruled in or out. A <strong>zero-pressure test</strong> isolates that section and drops its pressure to zero: if pressure creeps back, something is still feeding water in — usually a leak.",
        body="""
      <div class="prose">
        <h2>Ne zaman uygulanır?</h2>
        <p>Sıfır basınç testi, bir bölgede kayıp olduğu bilindiği ama kaynağın hâlâ daraltılamadığı durumlarda devreye girer. Genellikle bir <a href="/blog/adim-testi-nedir.html">adım (step) testi</a> ya da akustik tarama sonrasında, şüphe belirli bir hat parçasına inmiş ancak kesin karar verilememişse uygulanır. Örneğin adım testinde bir basamak beklenenden büyük çıkmış, yer mikrofonu ise o parçada net bir ses vermemiş olabilir. Bu belirsizliği gidermek için o parça tek başına sınanır.</p>
        <p>Yöntem, kısa ve sınırları belli bir hat parçası için anlamlıdır: iki sınır vanası arasında kalan, birkaç yüz metreyi geçmeyen, bağlantıları bilinen bir kesim. Parça uzadıkça izole etmek zorlaşır, boşaltma süresi uzar ve sonucun yorumu bulanıklaşır. Kapsam belediye ve organize sanayi bölgesi dağıtım şebekeleridir; test, ana hat ve bölge hatları için tasarlanmıştır.</p>

        <h2>Bölümü izole etme</h2>
        <p>İlk adım, sınanacak parçayı şebekenin geri kalanından tamamen ayırmaktır. Parçanın iki ucundaki sınır vanaları kapatılır ve her birinin gerçekten sızdırmaz oturduğu ayrı ayrı doğrulanır. Kapanmayan ya da azıcık su geçiren tek bir sınır vanası, testi baştan geçersiz kılar: dışarıdan sızan su, parçanın içindeki bir kaçakla karışır ve sonuç okunamaz hâle gelir.</p>
        <p>Vana sızdırmazlığı, mümkünse vananın arkasındaki basınç düşüşü izlenerek veya tahliye noktasından gözlemle kontrol edilir. İzole edilen parçaya bir <strong>basınç kaydedici (veri loggerı)</strong> bağlanır; kaydedici, testin tamamı boyunca kısa aralıklarla basınç kaydı alır. Parça üzerinde birden çok ölçüm noktası varsa, en düşük kotta ve sınır vanasına en uzak noktada kayıt tercih edilir.</p>

        <h2>Basıncı sıfıra indirme</h2>
        <p>Parça izole edildikten sonra içindeki su, bir hidranttan veya tahliye (washout) noktasından kontrollü biçimde boşaltılır. Boşaltma yavaş yapılır: ani açma, hatta basınç darbesi yaratır ve boru cidarındaki tortuyu harekete geçirir. Basınç kaydedici, değer sıfıra inene kadar izlenir.</p>
        <p>Basınç sıfıra ulaştığında tahliye kısılır ve parça içindeki su seviyesi dengelenene kadar kısa süre beklenir. Amaç, parçanın hiçbir dış kaynaktan beslenmediği ve iç basıncın gerçekten sıfır olduğu bir başlangıç durumu kurmaktır. Bu noktadan sonra tahliye tümüyle kapatılır.</p>

        <h2>Gözlem</h2>
        <p>Tahliye kapatıldıktan sonra basınç kaydedici izlenmeye devam eder. İki olası davranış vardır. Basınç sabit sıfırda kalıyorsa, parçaya giren hiçbir su yolu yoktur: sınır vanaları sızdırmaz ve parça üzerinde belirgin bir kaçak bulunmamaktadır; parça sağlam kabul edilir.</p>
        <p>Basınç zamanla yavaşça yükseliyorsa, parçaya hâlâ su giren bir yol vardır. Yükseliş hızı kabaca giren debiyle orantılıdır: hızlı bir tırmanış büyük bir açıklığa, çok yavaş bir tırmanış küçük bir sızıntıya işaret eder. Gözlem, basıncın eğilimi net görülene kadar sürdürülür; birkaç dakikalık kısa bir bakış yanıltıcı olabilir.</p>

        <h2>Sonucun yorumu</h2>
        <p>Basıncın geri gelmesi tek başına &ldquo;boru delik&rdquo; demek değildir. İki neden ayırt edilemez durumdadır: parça üzerinde gerçek bir kaçak olabilir ya da sınır vanalarından biri tam sızdırmaz oturmayıp dışarıdan su geçiriyor olabilir. Bu ayrımın yapılamaması yöntemin doğal sınırıdır ve rapora böyle yazılır.</p>
        <p>Ayrımı netleştirmek için sınır vanaları yeniden ve daha dikkatli kapatılıp test tekrarlanır; mümkünse vananın diğer tarafı da geçici olarak basınçsız bırakılır. Geri gelme sürüyorsa neden büyük olasılıkla parçanın içindedir. Bu durumda parça, nokta tespiti için <a href="/blog/akustik-su-kacagi-tespiti-nedir.html">akustik ekibe</a> devredilir; sıfır basınç testi kaçağın yerini vermez, yalnızca o parçada kaçak bulunduğunu doğrular. Basınç sabit sıfırda kaldıysa şüphe o parçadan kaldırılır ve arama komşu parçalara kaydırılır.</p>

        <h2>Güvenlik ve su kalitesi</h2>
        <p>Basıncı sıfıra indirmek, izole parçada ve komşu şebekede geçici olarak negatif basınç oluşturabilir. Negatif basınç, zemindeki kirli suyun bağlantı noktalarından içeri emilmesine (geri emilim) yol açabilir. Bu yüzden boşaltma kontrollü yapılır, parça gereğinden uzun süre basınçsız bırakılmaz ve iş biter bitmez hat yeniden basınçlandırılır.</p>
        <p>Yeniden basınçlandırma yavaş yapılır: vana kademeli açılır, hava tahliye noktalarından atılır ve basınç normal değerine dereceli olarak getirilir. Ardından parça bir hidranttan yıkanır; bulanıklık veya renk sürüyorsa yıkama uzatılır ve gerekiyorsa dezenfeksiyon uygulanır. Testten etkilenen bağlantılar önceden bilgilendirilir, kesinti penceresi kısa tutulur. Sonuçlar, kesinlik iddiası abartılmadan; &ldquo;parça sağlam&rdquo;, &ldquo;parçada besleyen bir yol var&rdquo; veya &ldquo;ayrım yapılamadı, tekrar gerekli&rdquo; biçiminde raporlanır.</p>
        <ul>
          <li>Yöntemin ayrıntısı: <a href="/hizmetler.html">Hizmetler</a></li>
          <li>Saha örnekleri: <a href="/projeler/">Projeler</a></li>
          <li>Sık sorulanlar: <a href="/sss.html">SSS</a></li>
        </ul>
      </div>
""",
        body_en="""
      <div class="prose">
        <h2>When is it used?</h2>
        <p>A zero-pressure test comes in where a zone is known to have loss but the source still cannot be narrowed down. It is usually applied after a <a href="/en/blog/adim-testi-nedir.html">step test</a> or an acoustic survey, when suspicion has come down to a particular length of main but no firm decision could be made. A step in the step test may have come out larger than expected, or the ground microphone may have given no clear sound on that length. To resolve that uncertainty, the length is tested on its own.</p>
        <p>The method is meaningful for a short, clearly bounded length of main: a section between two boundary valves, no more than a few hundred metres, with known connections. The longer the length, the harder it is to isolate, the longer the draw-down takes and the murkier the interpretation. The scope is municipal and organised-industrial-zone distribution networks; the test is designed for mains and zone pipes.</p>

        <h2>Isolating the section</h2>
        <p>The first step is to separate the length under test completely from the rest of the network. The boundary valves at each end of the length are closed, and each is verified separately to seat truly tight. A single boundary valve that will not close, or that passes a little water, invalidates the test from the start: water leaking in from outside mixes with any leak inside the length and the result becomes unreadable.</p>
        <p>Valve tightness is checked where possible by watching the pressure fall behind the valve, or by observation at the washout. A <strong>pressure recorder (data logger)</strong> is connected to the isolated length; it logs pressure at short intervals throughout the test. Where the length has more than one measuring point, the reading is taken at the lowest elevation and farthest from the boundary valve.</p>

        <h2>Dropping the pressure to zero</h2>
        <p>Once the length is isolated, the water inside it is drawn down in a controlled way through a hydrant or a washout point. The draw-down is done slowly: a sudden opening sends a pressure surge through the main and disturbs sediment on the pipe wall. The pressure recorder is watched until the value reaches zero.</p>
        <p>When the pressure reaches zero, the washout is throttled back and a short wait lets the water level inside the length settle. The aim is to establish a starting state in which the length is fed from no external source and the internal pressure is genuinely zero. After that, the washout is closed completely.</p>

        <h2>Observation</h2>
        <p>With the washout closed, the pressure recorder keeps logging. There are two possible behaviours. If the pressure stays flat at zero, no path feeds water into the length: the boundary valves are tight and there is no significant leak on the length; the section is taken to be sound.</p>
        <p>If the pressure creeps slowly back up, a path is still letting water into the length. The rate of rise is roughly proportional to the flow entering: a fast climb points to a large opening, a very slow climb to a small seep. Observation is continued until the trend of the pressure is clear; a brief few-minute glance can mislead.</p>

        <h2>Interpreting the result</h2>
        <p>Pressure returning does not by itself mean &ldquo;the pipe has a hole&rdquo;. Two causes cannot be told apart: there may be a real leak on the length, or one of the boundary valves may not be seating fully tight and is passing water from outside. That this ambiguity cannot be resolved is an inherent limit of the method, and it is written into the report as such.</p>
        <p>To clarify, the boundary valves are closed again more carefully and the test is repeated; where possible the far side of the valve is also left unpressurised for a time. If the return persists, the cause is most likely inside the length. The length is then handed to the <a href="/en/blog/akustik-su-kacagi-tespiti-nedir.html">acoustic crew</a> for pinpointing; a zero-pressure test does not give the leak's position, only confirms that the length holds a leak. If the pressure stayed flat at zero, suspicion is lifted from that length and the search moves to neighbouring sections.</p>

        <h2>Safety and water quality</h2>
        <p>Dropping the pressure to zero can create negative pressure for a time, in the isolated length and in the neighbouring network. Negative pressure can draw contaminated water in from the ground through connection points (back-siphonage). For this reason the draw-down is controlled, the length is not left unpressurised longer than needed, and the main is re-pressurised as soon as the work is done.</p>
        <p>Re-pressurising is done slowly: the valve is opened in stages, air is expelled at the vent points, and pressure is brought back to its normal value gradually. The length is then flushed from a hydrant; if turbidity or discolouration persists, flushing is extended and disinfection applied if needed. Connections affected by the test are notified in advance and the interruption window is kept short. Results are reported without overstating certainty — as &ldquo;section sound&rdquo;, &ldquo;a path is feeding the section&rdquo;, or &ldquo;could not be told apart, a repeat is needed&rdquo;.</p>
        <ul>
          <li>Method detail: <a href="/en/hizmetler.html">Services</a></li>
          <li>Field examples: <a href="/en/projeler/">Projects</a></li>
          <li>Common questions: <a href="/en/sss.html">FAQ</a></li>
        </ul>
      </div>
""",
    ),
    dict(
        slug="su-kaybi-dusurme-yol-haritasi",
        hero="/assets/photos/depo-cikis.webp",
        hero_alt="Depo çıkışı debi ölçüm noktası",
        hero_alt_en="Reservoir outlet flow metering point",
        date="2026-09-01",
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

# slug, tr_title, tr_desc, en_title, en_desc, hero
BLOG_INDEX_ITEMS = [
    ("su-kacagi-nasil-anlasilir",
     "Su kaçağı nasıl anlaşılır?", "İçme suyu şebekesinde gizli kaybın 8 belirtisi ve nasıl doğrulandığı.",
     "How to tell if there is a water leak?", "Eight signs of hidden loss in a drinking-water network and how it is confirmed.",
     "/assets/photos/gunduz-dinleme.webp"),
    ("debi-olcumu-nedir",
     "Debi ölçümü nedir?", "Taşınabilir ve kalıcı debimetreler, ölçüm noktası seçimi ve gece minimum debi.",
     "What is flow measurement?", "Portable and permanent flow meters, choosing the measuring point, minimum night flow.",
     "/assets/photos/debi-olcum.webp"),
    ("basinc-yonetimi-nedir",
     "Basınç yönetimi nedir?", "Basınç–kaçak ilişkisi, basınç bölgesi (PMA) ve basınç düşürücü vana ayarı.",
     "What is pressure management?", "The pressure–leak link, pressure managed areas (PMA) and PRV control.",
     "/assets/photos/basinc-logger.webp"),
    ("akustik-su-kacagi-tespiti-nedir",
     "Akustik su kaçağı tespiti nasıl yapılır?", "Gürültü kaydedici, yer mikrofonu ve korelatörle adım adım yer tespiti.",
     "How is acoustic water leak detection done?", "Step-by-step location with noise loggers, a ground microphone and a correlator.",
     "/assets/photos/gece-dinleme-hero.webp"),
    ("dma-nedir",
     "DMA (İzole Ölçüm Bölgesi) nedir?", "Şebekeyi ölçülebilir bölgelere ayırmak, gece minimum debi ve step test.",
     "What is a DMA (District Metered Area)?", "Splitting the network into measurable zones, minimum night flow and step testing.",
     "/assets/photos/dma-tasarim.webp"),
    ("adim-testi-nedir",
     "Adım (step) testi nedir?", "Gece vanaları kademeli kapatıp debi düşüşünden kaybı alt hatlara daraltma.",
     "What is a step test?", "Closing valves in steps at night and reading the flow drop to narrow the loss.",
     "/assets/photos/gece-operasyon.webp"),
    ("sifir-basinc-testi-nedir",
     "Sıfır basınç testi nedir?", "Bir hat bölümünü izole edip basıncı sıfıra indirerek kaçak var/yok kararı.",
     "What is a zero-pressure test?", "Isolating a section and dropping pressure to zero to decide leak or no leak.",
     "/assets/blog/sifir-basinc-testi-nedir.webp"),
    ("su-kaybi-dusurme-yol-haritasi",
     "Su kaybını düşürme yol haritası", "NRW / IWA çerçevesi ve sekiz adımlı kalıcı kayıp azaltma programı.",
     "A roadmap for cutting water loss", "The NRW / IWA framework and an eight-step programme for lasting loss reduction.",
     "/assets/photos/depo-cikis.webp"),
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
        article_schema(h1, desc, url, u["guide"], u["ld_lang"],
                       image=a.get("hero"), date=a.get("date", "2026-09-04")),
    ]
    hd = head(L(a, "title", lang), desc, page_path, lang, schema_blocks=schema)
    hero_html = ""
    if a.get("hero"):
        hero_html = f'''
  <section class="section section--tight">
    <div class="wrap mw-900">
      <figure class="article-hero"><img src="{a['hero']}" alt="{L(a, 'hero_alt', lang)}" loading="eager"></figure>
    </div>
  </section>'''
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
{hero_html}
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
    items = [(s, (ten if lang == "en" else tt), (den if lang == "en" else dt), hero)
             for s, tt, dt, ten, den, hero in BLOG_INDEX_ITEMS]
    item_list = ", ".join(
        f'{{ "@type": "ListItem", "position": {i+1}, "url": "{abs_url(lang, "/blog/" + s + ".html")}", "name": "{t}" }}'
        for i, (s, t, d, hero) in enumerate(items))
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
        f'        <a class="card card--media rv" href="{rel_href(lang, "/blog/" + s + ".html")}">'
        f'<img class="card__img" src="{hero}" alt="" loading="lazy" decoding="async">'
        f'<span class="card__ix">{i+1:02d}</span>'
        f'<h3>{t}</h3><p>{d}</p></a>'
        for i, (s, t, d, hero) in enumerate(items))
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
