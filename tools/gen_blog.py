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
        "hub_title": "Water Loss &amp; Leakage Blog — Detection Methods, DMA, NRW | LeakExpert",
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
        date="2026-09-04",
        h1="Debi ölçümü nedir, şebekede nasıl yapılır?",
        title="Debi Ölçümü Nedir? Şebekede Debi Nasıl Ölçülür | LeakExpert",
        desc="Şebekede debi ölçümünün amacı, taşınabilir ultrasonik/elektromanyetik debimetre ile geçici ölçüm, kalıcı bölge sayacı, gece minimum debi.",
        lede="Kaybı yönetmek için önce <strong>ne kadar su aktığını</strong> bilmek gerekir. Debi ölçümü, bir hattan veya bölgeden birim zamanda geçen su hacmini ölçer; su kayıp-kaçak çalışmasının ilk sayısal adımıdır.",
        h1_en="What is flow measurement, and how is it done in a network?",
        title_en="What Is Flow Measurement? How Flow Is Measured in a Network | LeakExpert",
        desc_en="The purpose of network flow measurement, temporary measurement with a portable ultrasonic/electromagnetic meter, permanent zone meters and minimum night flow.",
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
        date="2026-09-04",
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
        slug="hidrolik-modelleme-nedir",
        hero="/assets/photos/basinc-test.webp",
        hero_alt="Sahada basınç ölçümü",
        hero_alt_en="Field pressure measurement",
        date="2026-09-04",
        h1="Hidrolik modelleme ve saha kalibrasyonu",
        title="Hidrolik Modelleme Nedir? Şebeke Modeli ve Saha Kalibrasyonu | LeakExpert",
        desc="Hidrolik model, içme suyu şebekesinin bilgisayar benzetimidir. Model girdileri, saha basınç-debi ölçümleriyle kalibrasyon, kayıp ve basınç senaryoları.",
        lede="Bir şehir şebekesinde \"şu vanayı kısarsam uçtaki basınç ne olur?\" sorusunu sahada denemek pahalıdır. <strong>Hidrolik model</strong>, şebekenin borularını, kotlarını ve tüketimini bilgisayarda kurup bu soruları önceden yanıtlar.",
        h1_en="Hydraulic modelling and field calibration",
        title_en="What Is Hydraulic Modelling? Network Model and Field Calibration | LeakExpert",
        desc_en="A hydraulic model is a computer simulation of a drinking-water network: model inputs, calibration against field measurements, loss and pressure scenarios.",
        lede_en="Testing \"what happens to end-of-line pressure if I throttle this valve?\" in the field is expensive. A <strong>hydraulic model</strong> builds the network's pipes, elevations and demand in software and answers those questions in advance.",
        body="""
      <div class="prose">
        <h2>Model nedir, ne işe yarar?</h2>
        <p>Hidrolik model, bir içme suyu dağıtım şebekesinin bilgisayarda kurulmuş benzetimidir. Şebeke bir grafik olarak temsil edilir: borular kenarlar, kavşak ve tüketim noktaları düğümlerdir. Her boru için uzunluk, çap, malzeme ve iç pürüzlülük; her düğüm için kot ve o düğüme atanan talep tanımlanır. Buna depo su seviyeleri ve pompa eğrileri gibi sınır koşulları eklenir. Modelleme yazılımı bu denklemleri çözerek her düğümdeki basıncı ve her borudaki debiyi hesaplar.</p>
        <p>İki temel çalışma biçimi vardır. Kararlı hâl (steady-state) çözümü, talebin sabit olduğu tek bir an için şebekeyi çözer. Uzatılmış süre benzetimi (extended-period) ise günlük bir tüketim profili boyunca saat saat çözüm üretir; depo dolup boşalması, pompa çalışma saatleri ve gece–gündüz basınç değişimi bu biçimde görülür.</p>
        <p>Model, sahada denemesi pahalı veya riskli olan soruları önceden yanıtlamak için kullanılır: <a href="/blog/basinc-yonetimi-nedir.html">basınç yönetimi</a> tasarımı, yeni boru veya depo yatırımının etkisi, bir bölgenin beslemesinin değiştirilmesi ve kayıp azaltmanın şebeke davranışına yansıması. Model bir karar destek aracıdır; gerçeğin yerini tutmaz, gerçeği tahmin eder.</p>

        <h2>Girdi verileri</h2>
        <p>Bir modelin değeri, girdi verisinin doğruluğuna bağlıdır. Ağ geometrisi genellikle şebekenin harita ve coğrafi bilgi sisteminden alınır: boru güzergâhı, çap, malzeme, döşenme yılı ve vana konumları. Bu verinin güncel ve eksiksiz olması kritik önemdedir; bu nedenle model çalışması çoğu zaman <a href="/blog/sebeke-haritalama-cbs.html">şebeke haritalama ve CBS</a> çalışmasıyla birlikte yürür.</p>
        <p>Düğüm kotları sayısal yükseklik verisinden veya nivelman ölçümünden gelir; basınç kot farkına doğrudan bağlı olduğu için kot hataları model basıncını sistematik biçimde kaydırır. Pürüzlülük katsayısı boru malzemesi ve yaşına göre başlangıçta tahmin edilir, sonra kalibrasyonla düzeltilir.</p>
        <p>Sınır koşulları da tanımlanır: depo ve terfi merkezi su seviyeleri, pompa debi–basma yüksekliği eğrileri, basınç düşürücü vana ayar değerleri ve şebekeye giren toplam üretim debisi. Bu değerlerin ölçüm kayıtlarıyla, tercihen modelin temsil ettiği güne ait kayıtlarla desteklenmesi gerekir.</p>

        <h2>Talep dağıtımı</h2>
        <p>Şebekeye giren toplam su, modeldeki düğümlere paylaştırılmak zorundadır; çünkü tüketim gerçekte binlerce abone bağlantısından çekilir, model ise sınırlı sayıda düğümle çalışır. En yaygın yöntem, her düğüme yakınındaki abone sayısı veya faturalanan tüketim payı oranında talep atamaktır. Böylece düğüm talepleri toplandığında sisteme giren ölçülmüş debiye eşit olur.</p>
        <p>Kararlı hâl çözümü tek bir talep seviyesiyle çalışır; genellikle günlük ortalama veya saatlik en yüksek talep seçilir. Uzatılmış süre benzetiminde ise düğüm taleplerine bir günlük tüketim profili uygulanır: gecenin düşük, sabah ve akşamın yüksek çarpanlarıyla saatlik talep değişimi tanımlanır. Sanayi ve kamu gibi farklı abone türleri için ayrı profiller kullanılabilir.</p>
        <p>Fiziki kayıp da bir tür taleptir ve basınçla birlikte artar. Kaba modellerde kayıp, tüm düğümlere yayılmış sabit bir ek tüketim olarak; daha ayrıntılı modellerde basınca bağlı bir sızıntı terimi olarak tanımlanır. <a href="/blog/debi-olcumu-nedir.html">Debi ölçümü</a> ve <a href="/blog/dma-nedir.html">DMA</a> gece minimum debisi, bu kayıp bileşeninin büyüklüğünü belirlemede kullanılır.</p>

        <h2>Saha kalibrasyonu</h2>
        <p>Kurulan model başlangıçta gerçeği tam yansıtmaz; pürüzlülük tahminleri, talep dağıtımı ve harita hataları çıktıyı gerçekten uzaklaştırır. Kalibrasyon, model çıktısını sahada ölçülen değerlere yaklaştırma sürecidir. Bunun için şebekede birkaç noktaya eşzamanlı basınç kaydediciler ve seçili hatlara debi ölçüm cihazları yerleştirilir; ölçüm en az bir tam gün, tercihen tipik bir hafta içi gün boyunca sürer.</p>
        <p>Aynı gün için model çalıştırılır ve modellenen basınç ile debi, ölçülen değerlerle karşılaştırılır. Fark kabul edilebilir sınırın üzerindeyse, önce belirgin hatalar (kapalı sanılan açık vana, yanlış çap, hatalı kot) düzeltilir; ardından pürüzlülük katsayıları ve talep dağıtımı, model ile ölçüm örtüşene kadar ayarlanır. Ayar, ölçüm noktalarının tümünde aynı anda makul uyum sağlayacak biçimde yapılır; tek noktayı tutturmak için diğerlerini bozmak kalibrasyon değildir.</p>
        <p>Kalibre edilmiş model, ölçümün yapıldığı çalışma koşulları için güvenilirdir. Koşullar (talep seviyesi, pompa düzeni) ölçüm aralığından uzaklaştıkça belirsizlik artar. Bu yüzden hem kararlı hâl hem de gün boyu değişim için ayrı ayrı doğrulama tercih edilir.</p>

        <h2>Senaryolar</h2>
        <p>Kalibre edilmiş bir model, &ldquo;ya şöyle olsaydı?&rdquo; sorularını sahada denemeden ucuza sınamaya yarar. Sık kullanılan senaryolardan biri basınç düşürücü vana hedef değerinin değiştirilmesidir: uç noktalarda basınç kabul edilebilir sınırın altına inmeden ayarın ne kadar düşürülebileceği modelde görülür. Bir diğeri bölge sınırlarının değiştirilmesidir; bir <a href="/blog/dma-nedir.html">DMA</a> sınır vanasının açılıp kapatılmasının komşu bölgelerin basıncına ve debisine etkisi önceden hesaplanır.</p>
        <p>Yangın debisi senaryosunda, belirli bir hidranttan yüksek debi çekilirken şebekede kalan artık basınç kontrol edilir. Kayıp azaltma senaryosunda ise fiziki kaybın belirli bir oranda düşürülmesinin gece minimum debisine ve ortalama basınca yansıması incelenir. Her senaryo, aynı kalibre modelin tek bir girdisini değiştirip yeniden çözmekle üretilir; sonuçlar mutlak sayı olarak değil, mevcut duruma göre değişim olarak yorumlanır, çünkü modelin doğruluğu sınırlıdır ve karşılaştırmalı sonuç tek bir kesin sayıdan daha güvenilirdir.</p>

        <h2>Modelin sınırları</h2>
        <p>Model, girdi verisi kadar iyidir. Eski veya eksik CBS kayıtları, kayıt dışı bağlantılar, yanlış çap veya malzeme bilgisi ve konumu bilinmeyen kapalı vanalar, çözümü sessizce yanlış tarafa çeker. Bu hatalar çoğu zaman kalibrasyonda pürüzlülük ayarına gömülür ve model &ldquo;uyuyor&rdquo; görünürken fiziksel olarak yanlış olabilir.</p>
        <p>Doğruluk abartılmamalıdır. İyi kalibre edilmiş bir model, basınçları birkaç metre su sütunu, debileri ise yüzde birkaç ile birkaç on mertebesinde hata payıyla verir; kesin bir ölçüm cihazı değildir. Şebeke değiştikçe (yeni hat, yeni abone, yenilenen boru, değişen pompa düzeni) model eskir ve periyodik olarak yeniden kalibre edilmelidir.</p>
        <p>Bu sınırlara rağmen model, sahada tek tek denenemeyecek çok sayıda seçeneği hızlı ve düşük maliyetle karşılaştırmayı sağlar. Modelleme çalışması uzaktan / video görüşmeyle planlanabilir; şebeke verisi ve ölçüm kayıtları paylaşıldıktan sonra kurulum, kalibrasyon ve senaryo çalışması birlikte yürütülür.</p>
        <ul>
          <li>Hizmet kapsamı: <a href="/hizmetler.html">Hizmetler</a></li>
          <li>Saha örnekleri: <a href="/projeler/">Projeler</a></li>
          <li>Sık sorulanlar: <a href="/sss.html">SSS</a></li>
        </ul>
      </div>
""",
        body_en="""
      <div class="prose">
        <h2>What a model is and what it is for</h2>
        <p>A hydraulic model is a computer simulation of a drinking-water distribution network. The network is a graph: pipes are edges, junctions and draw-off points nodes. Each pipe carries a length, diameter, material and roughness; each node an elevation and an assigned demand. With boundary conditions added — reservoir levels, pump curves — the software solves for the pressure at every node and the flow in every pipe.</p>
        <p>A steady-state solution solves the network for one instant of fixed demand. An extended-period simulation solves it hour by hour across a daily demand pattern, showing reservoirs filling and emptying, pump run times and the day–night pressure swing.</p>
        <p>The model answers questions that are expensive or risky to try in the field: designing <a href="/en/blog/basinc-yonetimi-nedir.html">pressure management</a>, the effect of a new main or reservoir, re-routing a zone's supply, and how loss reduction changes network behaviour. It is a decision-support tool, not a substitute for the network itself.</p>

        <h2>Input data</h2>
        <p>A model is only as good as its input data. The network geometry usually comes from the utility's map and geographic information system: pipe route, diameter, material, year laid and valve positions. Because that data must be current and complete, a modelling exercise often runs alongside a <a href="/en/blog/sebeke-haritalama-cbs.html">network mapping and GIS</a> effort.</p>
        <p>Node elevations come from a digital elevation model or a levelling survey; since pressure depends on elevation difference, elevation errors shift modelled pressure systematically. Roughness is first estimated from pipe material and age, then corrected in calibration.</p>
        <p>Boundary conditions are also defined: reservoir and pumping-station levels, pump flow–head curves, pressure-reducing valve settings and the total production flow — ideally backed by measurement records from the day the model represents.</p>

        <h2>Demand allocation</h2>
        <p>The total inflow must be shared out among the model's nodes, since consumption is really drawn from thousands of service connections while the model has far fewer. The common method assigns demand to each node in proportion to the subscribers near it, or to its share of billed consumption, so the nodal demands sum to the measured inflow.</p>
        <p>A steady-state run uses a single demand level, usually the daily average or peak hour. An extended-period run applies a daily pattern of hourly multipliers — low at night, high morning and evening — with separate patterns for customer types such as industrial or public.</p>
        <p>Physical loss is itself a kind of demand, and it rises with pressure. Coarse models enter it as a fixed extra draw across all nodes; detailed models use a pressure-dependent leakage term. <a href="/en/blog/debi-olcumu-nedir.html">Flow measurement</a> and <a href="/en/blog/dma-nedir.html">DMA</a> minimum night flow size this component.</p>

        <h2>Field calibration</h2>
        <p>A newly built model does not reflect reality exactly; roughness estimates, demand allocation and map errors move the output off the truth. Calibration brings it back toward field measurements: pressure loggers at several points and flow meters on selected mains log for at least a full day, preferably a weekday.</p>
        <p>The model is run for that same day and its pressures and flows are compared with the measurements. Obvious errors are corrected first — an open valve thought closed, a wrong diameter, a bad elevation — then roughness and demand allocation are adjusted until model and measurement agree at all points at once. Forcing one point at the cost of the others is not calibration.</p>
        <p>A calibrated model is reliable for the conditions under which it was measured; as demand level or pump configuration move away from that range, uncertainty grows.</p>

        <h2>Scenarios</h2>
        <p>A calibrated model lets &ldquo;what if?&rdquo; questions be tried cheaply. One scenario changes a pressure-reducing valve target: how far the setting can be lowered before end-of-line points fall below the acceptable limit. Another changes zone boundaries: the effect on neighbouring zones' pressure and flow of opening or closing a <a href="/en/blog/dma-nedir.html">DMA</a> boundary valve.</p>
        <p>A fire-flow scenario checks the residual pressure in the network while a high flow is drawn from a hydrant. A loss-reduction scenario examines how cutting physical loss by a given fraction feeds through to the minimum night flow and the average pressure. Each comes from changing one input of the calibrated model and solving again; results are read as a change from the present state, not as absolute numbers, since a comparative result is more trustworthy than a single hard figure.</p>

        <h2>The model's limits</h2>
        <p>A model is only as good as its input data — garbage in, garbage out. Stale or incomplete GIS records, unrecorded connections, wrong diameter or material, and unknown closed valves all pull the solution quietly the wrong way. Such errors often end up buried in the roughness adjustment during calibration, so the model can look as if it &ldquo;fits&rdquo; while being physically wrong.</p>
        <p>Accuracy should not be overstated. A well-calibrated model gives pressures to within a few metres of head and flows to within a few to a few tens of per cent; it is not a precise instrument. As the network changes — new mains, customers, renewed pipe, altered pumping — the model ages and needs periodic re-calibration.</p>
        <p>Even so, a model compares many options that could never be tried one by one in the field, quickly and cheaply. A modelling exercise can be planned over a remote or video call; once the network data and measurement records are shared, the build, calibration and scenario work proceed together.</p>
        <ul>
          <li>Service scope: <a href="/en/hizmetler.html">Services</a></li>
          <li>Field examples: <a href="/en/projeler/">Projects</a></li>
          <li>Common questions: <a href="/en/sss.html">FAQ</a></li>
        </ul>
      </div>
""",
    ),
    dict(
        slug="boru-hatti-tespiti-nedir",
        hero="/assets/blog/boru-hatti-tespiti-nedir.webp",
        hero_alt="Saha ekibi hat güzergâhını işaretliyor",
        hero_alt_en="Field crew marking a pipe route",
        date="2026-09-04",
        h1="Boru hattı güzergâhı ve derinlik tespiti",
        title="Boru Hattı Tespiti Nedir? Güzergâh ve Derinlik Belirleme | LeakExpert",
        desc="Gömülü içme suyu hatlarının güzergâh ve derinliği nasıl belirlenir: metal hatlarda elektromanyetik hat dedektörü, plastik hatlarda prob ve yer radarı (GPR).",
        lede="Kaçağı bulmadan, onarmadan veya haritalamadan önce çoğu zaman ilk soru şudur: <strong>boru tam olarak nerede ve ne kadar derinde?</strong> Hat tespiti, gömülü hattı kazmadan yüzeyden işaretleme işidir.",
        h1_en="Locating a pipe route and depth",
        title_en="What Is Pipe Locating? Determining Route and Depth | LeakExpert",
        desc_en="How the route and depth of buried drinking-water mains are found: electromagnetic pipe locators on metal mains, internal probes or GPR on plastic mains.",
        lede_en="Before finding a leak, repairing it or mapping it, the first question is often: <strong>exactly where is the pipe, and how deep?</strong> Pipe locating is marking a buried main from the surface without digging.",
        body="""
      <div class="prose">
        <h2>Neden gerekir?</h2>
        <p>Gömülü bir içme suyu hattı üzerinde çalışmadan önce çoğu zaman ilk adım, hattın yüzeydeki izdüşümünü ve yaklaşık derinliğini belirlemektir. Onarım kazısında ekskavatör kovasının nereye ineceği; yeni bir bağlantı veya vana odası planlanırken mevcut hattın tam konumu; başka altyapıların (elektrik, gaz, telekom) yakınında kazı yapılırken hasar önleme — hepsi hattın güzergâhının bilinmesine bağlıdır.</p>
        <p>Tespit sonuçları aynı zamanda kalıcı bir kayıt üretir. İşaretlenen güzergâh ve noktasal derinlikler koordinatlandırılıp <a href="/blog/sebeke-haritalama-cbs.html">şebeke haritalama ve CBS</a> çalışmasına işlenir; böylece bir sonraki kazıda ölçümü baştan tekrarlamak gerekmez. Aynı geometri, <a href="/blog/hidrolik-modelleme-nedir.html">hidrolik modelin</a> boru uzunluğu ve bağlantı topolojisi girdisini de doğrular.</p>
        <p>Kapsam belediye ve organize sanayi bölgesi dağıtım şebekeleridir; söz konusu olan, sokak ve arter hatlarının güzergâhının kazısız belirlenmesidir.</p>

        <h2>Metal hatlar: elektromanyetik hat dedektörü</h2>
        <p>Dökme demir, çelik ve font gibi iletken borular, elektromanyetik hat dedektörüyle izlenir. Sistem iki parçadan oluşur: hatta bir sinyal (alternatif akım) bindiren verici ve bu sinyalin oluşturduğu manyetik alanı yüzeyden algılayan alıcı.</p>
        <p>Sinyal hatta iki yolla verilir. Doğrudan bağlantıda verici kablosu, borunun açıkta bir noktasına (vana mili, hidrant, flanş) doğrudan kelepçelenir; bu en güçlü ve en temiz yöntemdir. İndüktif kelepçede, boruyu saran bir halka verici sinyalini boruya endükler ve bağlantı için açık metal gerekmez. Verici doğrudan zemine de kurulabilir, ancak bu durumda sinyal daha zayıf ve komşu iletkenlere kaçmaya daha yatkındır.</p>
        <p>Alıcı, güzergâh boyunca yürütülürken sinyalin en güçlü olduğu çizgi borunun izdüşümünü verir. Cihaz aynı zamanda alan geometrisinden bir derinlik tahmini hesaplar; bu değer, sinyalin tek ve bozulmamış bir iletkenden geldiği varsayımına dayanır.</p>

        <h2>Plastik (PE/PVC) hatlar</h2>
        <p>Polietilen ve PVC borular iletken değildir; üzerlerine doğrudan elektromanyetik sinyal bindirilemez. Bu hatların izlenmesi için hattın içinde veya boyunca izlenebilir bir öğe gerekir.</p>
        <p>İlk yöntem, hat içine itilen problu kablodur (prob/sonda): ucunda küçük bir verici bulunan bükülebilir bir çubuk, bir vana veya bağlantı ağzından boruya sürülür ve alıcı, prob ucunun konumunu ve derinliğini yüzeyden takip eder. İkinci yöntem sinyal telidir: boru döşenirken hattın üzerine paralel bir bakır tel gömülür; sonradan bu tele verici bağlanarak hat, metal boru gibi izlenir. Yeni PE şebekelerde sinyal teli standart bir uygulamadır. Bu iki seçenek de yoksa geriye yer radarı kalır.</p>

        <h2>Yer radarı (GPR)</h2>
        <p>Yer radarı (GPR), zemine yüksek frekanslı radar darbeleri gönderen ve farklı malzemelerin sınırlarından dönen yansımaları kaydeden bir yöntemdir. Anten zemin üzerinde bir hat boyunca çekildiğinde, gömülü boru kesiti radargramda tipik bir hiperbol izi bırakır; bu izin tepe noktası borunun yatay konumunu, derinlik ekseni ise yaklaşık gömülme derinliğini verir.</p>
        <p>GPR malzemeden bağımsızdır: metal, PE, PVC, beton künk ve hatta boşluk aynı ilkeyle görüntülenir. Buna karşılık performansı zemine çok bağlıdır. Kuru kum ve çakılda derin ve net sonuç alınırken, ıslak killi zeminde sinyal hızla sönümlenir ve birkaç on santimetreden derini görünmez olur. Derinlik arttıkça, yüzeye yakın çok sayıda başka altyapı bulunduğunda ve dolgu düzensiz olduğunda yorum zorlaşır.</p>

        <h2>İşaretleme ve derinlik</h2>
        <p>Bulunan güzergâh sahada görünür kılınır: hat ekseni yol yüzeyine sprey boyayla çizilir, yumuşak zeminde kazık veya bayrakla noktalanır. İşaretlemede yaygın uygulama, hattın merkez çizgisini ve belirli aralıklarla istasyon numaralarını yazmaktır.</p>
        <p>Derinlik, güzergâh boyunca sürekli değil, seçili noktalarda ölçülür; cihazın verdiği derinlik tahmini bu noktalara not edilir. Güzergâh ve derinlik noktaları bir el GPS'i veya total station ile koordinatlandırılır ve CBS'e aktarılabilecek bir kroki ya da sayısal katman hâline getirilir. Böylece ölçüm kalıcı bir veri ürününe dönüşür.</p>

        <h2>Doğruluğun sınırları</h2>
        <p>Hiçbir yüzey yöntemi kazıyı bire bir taklit etmez. Elektromanyetik izlemede en büyük hata kaynağı, hedef hatta paralel uzanan başka metal borular ve yoğun gömülü altyapıdır; bunlar sinyali kendilerine çeker, güzergâh çizgisini yana kaydırır ve derinlik tahminini bozar. Sinyal telinde kopukluk veya eklerdeki temassızlık, izlemeyi belirli bir noktada kesebilir.</p>
        <p>Derinlik değeri her zaman bir tahmindir; borunun tek ve düz olduğu, alanın bozulmadığı kabulüne dayanır ve genellikle gerçek derinlikten bir miktar sapar. GPR yorumu operatöre ve zemine bağlıdır; bir hiperbol her zaman aranan boru değildir.</p>
        <p>Bu nedenle kritik bir kazıdan önce, işaretlenen nokta üzerinde elle küçük bir kontrol çukuru (el çukuru) açılıp hattın gerçek konumu ve derinliği gözle doğrulanır. Tespit çalışması ve sonuçların yorumu uzaktan / video görüşmeyle planlanabilir; şebeke krokisi, malzeme bilgisi ve erişim noktaları paylaşıldıktan sonra yöntem ve işaretleme planı birlikte belirlenir.</p>
        <ul>
          <li>Hizmet kapsamı: <a href="/hizmetler.html">Hizmetler</a></li>
          <li>Saha örnekleri: <a href="/projeler/">Projeler</a></li>
          <li>Sık sorulanlar: <a href="/sss.html">SSS</a></li>
        </ul>
      </div>
""",
        body_en="""
      <div class="prose">
        <h2>Why it is needed</h2>
        <p>Before any work on a buried drinking-water main, the first step is usually to establish where the pipe runs at the surface and roughly how deep it lies. Where the excavator bucket comes down for a repair dig; the exact position of the existing main when a new connection or valve chamber is planned; damage prevention when digging near other utilities such as power or gas — all of it depends on knowing the route.</p>
        <p>Locating results also produce a permanent record. The marked route and spot depths are given coordinates and entered into a <a href="/en/blog/sebeke-haritalama-cbs.html">network mapping and GIS</a> effort, so the survey need not be repeated from scratch at the next dig. The same geometry also confirms the pipe length and connection topology that feed a <a href="/en/blog/hidrolik-modelleme-nedir.html">hydraulic model</a>.</p>
        <p>The scope is municipal and organised-industrial-zone distribution networks; what is being found is the route of street and arterial mains, without excavation.</p>

        <h2>Metal mains: the electromagnetic pipe locator</h2>
        <p>Conductive pipes — cast iron, ductile iron, steel — are traced with an electromagnetic pipe locator. The system has two parts: a transmitter that applies an alternating-current signal to the pipe, and a receiver that senses the magnetic field this signal creates from the surface.</p>
        <p>The signal is applied in one of two ways. In a direct connection the transmitter lead is clamped straight onto an exposed point of the pipe — a valve spindle, a hydrant, a flange — which is the strongest and cleanest method. With an inductive clamp, a ring around the pipe induces the signal into it and no bare metal is needed for the connection. The transmitter can also be set on the ground, but then the signal is weaker and more likely to couple onto neighbouring conductors.</p>
        <p>Walked along the route, the receiver traces the line of strongest signal as the pipe's plan position. The instrument also computes a depth estimate from the field geometry; that figure assumes the signal comes from a single, undistorted conductor.</p>

        <h2>Plastic (PE/PVC) mains</h2>
        <p>Polyethylene and PVC pipes are not conductive, so no electromagnetic signal can be applied to them directly. Tracing these mains needs a traceable element in or along the line.</p>
        <p>The first method is a push probe or sonde: a flexible rod with a small transmitter at its tip is pushed into the pipe through a valve or fitting, and the receiver follows the position and depth of the probe tip from the surface. The second is tracer wire: a copper wire is buried parallel to the pipe as it is laid, and a transmitter is later connected to that wire so the main is traced as if it were metal. On new PE networks tracer wire is standard practice. Where neither is available, ground penetrating radar remains.</p>

        <h2>Ground penetrating radar (GPR)</h2>
        <p>GPR sends high-frequency radar pulses into the ground and records the reflections that return from the boundaries between different materials. As the antenna is pulled along a line over the surface, a buried pipe cross-section leaves a characteristic hyperbola on the radargram; the apex of that trace gives the pipe's horizontal position and the depth axis its approximate burial depth.</p>
        <p>GPR is independent of material: metal, PE, PVC, concrete pipe and even a void are imaged on the same principle. Its performance, however, depends heavily on the ground. Dry sand and gravel give deep, clear results, while in wet clay the signal is absorbed quickly and little is visible below a few tens of centimetres. Interpretation gets harder with depth, in congested ground, and where the backfill is heterogeneous.</p>

        <h2>Marking and depth</h2>
        <p>The located route is made visible on site: the pipe centreline is sprayed onto the road surface with paint, or pegged and flagged in soft ground, with the centreline and station numbers written at set intervals.</p>
        <p>Depth is measured not continuously but at selected points, and the instrument's depth estimate is noted there. The route and depth points are given coordinates with a hand-held GPS or a total station and turned into a sketch or a digital layer that can be imported into GIS. The survey thus becomes a permanent data product.</p>

        <h2>The limits of accuracy</h2>
        <p>No surface method reproduces a dig exactly. In electromagnetic tracing the biggest error source is other metal pipes running parallel to the target and dense buried services; they draw the signal onto themselves, shift the route line sideways and distort the depth estimate. A break in tracer wire, or a bad contact at a joint, can stop the trace at a point.</p>
        <p>The depth figure is always an estimate; it rests on the pipe being single and straight and the field undistorted, and it usually departs somewhat from the true depth. GPR interpretation depends on the operator and the ground; a hyperbola is not always the pipe being sought.</p>
        <p>For this reason, before a critical excavation, a small hand-dug trial pit is opened over the marked point to verify the pipe's real position and depth by eye. The locating work and the interpretation of its results can be planned over a remote or video call; once the network sketch, material data and access points are shared, the method and the marking plan are set together.</p>
        <ul>
          <li>Service scope: <a href="/en/hizmetler.html">Services</a></li>
          <li>Field examples: <a href="/en/projeler/">Projects</a></li>
          <li>Common questions: <a href="/en/sss.html">FAQ</a></li>
        </ul>
      </div>
""",
    ),
    dict(
        slug="sebeke-haritalama-cbs",
        hero="/assets/blog/sebeke-haritalama-cbs.webp",
        hero_alt="Şebeke haritası ekranı",
        hero_alt_en="Network map on screen",
        date="2026-09-04",
        h1="Şebeke haritalama ve CBS'e (GIS) aktarım",
        title="Şebeke Haritalama ve CBS (GIS) Aktarımı Nedir? | LeakExpert",
        desc="Saha tespiti verisinin coğrafi bilgi sistemine dönüşmesi: GPS koordinat, öznitelik (çap, malzeme, döşeme yılı), CBS katmanı ve topoloji.",
        lede="Bir şebekeyi ancak <strong>güncel bir haritası varsa</strong> yönetebilirsiniz. Şebeke haritalama, sahadaki boruları, vanaları ve bağlantıları konumları ve özellikleriyle birlikte sayısal bir sisteme geçirir.",
        h1_en="Network mapping and transfer to GIS",
        title_en="What Is Network Mapping and GIS Transfer? | LeakExpert",
        desc_en="Turning field survey data into a geographic information system: GPS coordinates, attributes (diameter, material, year laid), the GIS layer and topology.",
        lede_en="You can only manage a network if you have a <strong>current map</strong> of it. Network mapping moves the field's pipes, valves and connections — with their locations and properties — into a digital system.",
        body="""
      <div class="prose">
        <h2>Saha tespitinden veriye</h2>
        <p>Şebeke haritalama, bir dağıtım şebekesinin fiziksel bileşenlerini — hatlar, vanalar, hidrantlar, bağlantılar — konumları ve özellikleriyle birlikte sayısal bir ortama taşıma işidir. Kapsam belediye ve organize sanayi bölgesi dağıtım şebekeleridir; haritalanan, sokak ve arter hatlarıdır.</p>
        <p>İlk girdi sahadan gelir. Hat güzergâhı ve derinliği, gömülü borunun kazısız olarak yüzeyden belirlenmesiyle bulunur (bkz. <a href="/blog/boru-hatti-tespiti-nedir.html">boru hattı tespiti</a>). Vana, hidrant ve bağlantı noktalarının konumu ise bir GPS/GNSS alıcısıyla tek tek ölçülür. Her ölçüm, bir enlem-boylam çifti ve o noktanın ne olduğunu söyleyen bir etiketle kaydedilir.</p>
        <p>Bu ham veri iki geometrik türe ayrılır: nokta nesneleri (vana, hidrant, bağlantı, ek parça) ve çizgi nesneleri (iki nokta arasında uzanan hat bölümleri). Güzergâh boyunca yürünürken toplanan koordinat dizisi, hattın çizgi geometrisini oluşturur.</p>

        <h2>Öznitelikler</h2>
        <p>Konum tek başına yeterli değildir. Haritanın işe yaraması için her nesnenin öznitelikleriyle — onu tanımlayan alanlarla — birlikte kaydedilmesi gerekir.</p>
        <p>Her hat bölümü için tipik öznitelikler şunlardır: çap, malzeme (düktil font, çelik, PE, PVC, AÇB), döşeme yılı, bağlı olduğu basınç bölgesi ve varsa iç astar bilgisi. Her vana için: tip (sürgülü, kelebek, hava, tahliye), açık/kapalı durumu, çap ve manevra yönü. Hidrantlar için tip ve çıkış çapı; bağlantılar için abone türü (ana kullanıcı, sanayi tesisi) ve bağlantı çapı.</p>
        <p>Öznitelikler, ölçüm sahadayken kayıt altına alınır; eksik bırakılan bir alan sonradan tamamlanması zor bir boşluğa dönüşür. Döşeme yılı ve malzeme gibi alanlar çoğu zaman eski paftalardan ve idari kayıtlardan derlenir, sonra saha gözlemiyle çapraz kontrol edilir.</p>

        <h2>CBS katmanı ve topoloji</h2>
        <p>Nokta ve çizgiler bir coğrafi bilgi sistemine (CBS) katman olarak yüklenir. Buradaki kritik kavram topolojidir: nesnelerin birbirine yalnızca görsel olarak değil, mantıksal olarak da bağlı olması.</p>
        <p>Topolojik olarak doğru bir katmanda hat bölümleri uçlarından düğüm noktalarında birleşir, vanalar ait oldukları hat üzerine oturur ve sistem hangi vananın hangi hattı beslediğini ya da kestiğini bilir. Bir bölümü izole etmek için hangi vanaların kapatılması gerektiği, bu bağlantı yapısından hesaplanabilir. Kopuk çizgi uçları, boşluklar veya yanlış düğüme bağlanmış bir vana bu sorguları bozar.</p>
        <p>Bu yüzden haritalama, koordinatları toplamakla bitmez; geometrinin temizlenmesi, bölümlerin doğru yerlerden bölünmesi ve bağlantıların denetlenmesi işin ayrılmaz parçasıdır.</p>

        <h2>Doğruluk sınıfı</h2>
        <p>Bir şebeke haritasının doğruluğu tek bir sayı değildir; birkaç kaynağın birleşiminden gelir ve nesneden nesneye değişir.</p>
        <p>GPS/GNSS ölçümünün kendi hassasiyeti, kullanılan alıcıya ve düzeltme servisine göre birkaç metreden birkaç santimetreye kadar değişir. Eski kâğıt paftaların sayısallaştırılmasıyla elde edilen geometri genellikle daha düşük doğruluktadır; paftanın ölçeğine, çizim hatasına ve referanslama kalitesine bağlıdır. Saha teyidi — bir vana odasının, hidrantın veya kontrol çukurunun yerinde görülmesi — bu iki kaynağı birbirine bağlar ve kaba hataları yakalar.</p>
        <p>Pratikte her nesneye bir doğruluk/kaynak etiketi verilir: &ldquo;GNSS ile ölçüldü&rdquo;, &ldquo;paftadan sayısallaştırıldı&rdquo;, &ldquo;sahada teyit edildi&rdquo;. Doğruluğu abartmamak gerekir; sayısallaştırılmış bir hat, kazıdan önce yine yüzeyden tespit ve kontrol çukuruyla doğrulanmalıdır.</p>

        <h2>Platforma işleme</h2>
        <p>Temizlenmiş CBS katmanı LeakExpert platformuna aktarılır (bkz. <a href="/platform.html">platform</a>). Böylece hat ve vana geometrisi, kaçak noktaları, debi ve basınç ölçümleri ile saha projeleri aynı harita üzerinde bir arada görünür.</p>
        <p>Bu birleşim çalışmayı hızlandırır: bir akustik tarama sonucu haritadaki gerçek hat üzerine düşer, bir DMA sınırı vanalarıyla birlikte çizilir, bir onarım kaydı ilgili hat bölümüne bağlanır. Ölçüm ve gözlem verisi artık kâğıt kroki üzerinde değil, sorgulanabilir bir katman üzerinde birikir.</p>
        <p>Platform aynı zamanda ekipler arasında tek bir güncel kaynak sağlar; saha ekibi, ofis ve analiz aynı harita sürümüne bakar.</p>

        <h2>Haritayı güncel tutma</h2>
        <p>Bir şebeke haritası, üretildiği anda eskimeye başlar. Her yeni bağlantı, her onarım, her hat yenileme ve her vana değişimi haritaya geri işlenmezse katman kısa sürede gerçeğin gerisinde kalır.</p>
        <p>Güncel olmayan bir CBS'nin bedeli yalnızca yanlış bir çizim değildir. Eksik bir hat veya yanlış bir çap, <a href="/blog/hidrolik-modelleme-nedir.html">hidrolik modelin</a> boru uzunluğu ve topoloji girdisini bozar; bilinmeyen kapalı bir vana, model ile sahayı birbirinden uzaklaştırır. Aynı şekilde su dengesi ve kayıp analizi, bölge sınırları ve abone bağlantıları hatalıysa güvenilmez sonuç verir.</p>
        <p>Bu nedenle güncelleme bir iş akışı olarak tanımlanır: sahada yapılan her değişiklik, öznitelikleriyle birlikte kaydedilip haritaya eklenir. Haritalama ve güncelleme düzeni uzaktan / video görüşmeyle planlanabilir; mevcut kroki, pafta ve kayıtlar paylaşıldıktan sonra veri modeli ve iş akışı birlikte belirlenir.</p>
        <ul>
          <li>Hizmet kapsamı: <a href="/hizmetler.html">Hizmetler</a></li>
          <li>Saha örnekleri: <a href="/projeler/">Projeler</a></li>
          <li>Sık sorulanlar: <a href="/sss.html">SSS</a></li>
        </ul>
      </div>
""",
        body_en="""
      <div class="prose">
        <h2>From field survey to data</h2>
        <p>Network mapping is the work of moving the physical components of a distribution network — mains, valves, hydrants, connections — into a digital form together with their positions and properties. The scope is municipal and organised-industrial-zone distribution networks; what is mapped is the street and arterial mains.</p>
        <p>The first input comes from the field. The route and depth of a main are found from the surface without digging (see <a href="/en/blog/boru-hatti-tespiti-nedir.html">pipe locating</a>). The positions of valves, hydrants and connections are each measured with a GPS/GNSS receiver. Every measurement is stored as a latitude–longitude pair with a label that says what the point is.</p>
        <p>This raw data falls into two geometry types: point objects (valve, hydrant, connection, fitting) and line objects (pipe segments running between two points). The string of coordinates collected while walking the route becomes the line geometry of the main.</p>

        <h2>Attributes</h2>
        <p>Position alone is not enough. For the map to be useful, every object has to be recorded with its attributes — the fields that describe it.</p>
        <p>Typical attributes for a pipe segment are: diameter, material (ductile iron, steel, PE, PVC, asbestos cement), year laid, the pressure zone it belongs to, and any lining information. For a valve: type (gate, butterfly, air, washout), open or closed state, diameter and turning direction. For hydrants, type and outlet size; for connections, the customer type (bulk user, industrial site) and the connection diameter.</p>
        <p>Attributes are captured while the survey is still in the field; a field left blank becomes a gap that is hard to fill later. Fields such as year laid and material are often compiled from old paper plans and utility records, then cross-checked against what is seen on site.</p>

        <h2>The GIS layer and topology</h2>
        <p>The points and lines are loaded into a geographic information system (GIS) as a layer. The key idea here is topology: objects being connected to one another not only visually but logically.</p>
        <p>In a topologically correct layer, pipe segments meet end to end at node points, valves sit on the main they belong to, and the system knows which valve feeds or isolates which main. Which valves must be closed to isolate a section can be computed from this connection structure. Dangling line ends, gaps, or a valve snapped to the wrong node break these queries.</p>
        <p>Mapping therefore does not end with collecting coordinates; cleaning the geometry, splitting segments at the right places and checking the connections are an inseparable part of the job.</p>

        <h2>Accuracy class</h2>
        <p>The accuracy of a network map is not a single number; it comes from the combination of several sources and varies from object to object.</p>
        <p>The precision of the GPS/GNSS measurement itself ranges from a few metres to a few centimetres depending on the receiver and the correction service used. Geometry obtained by digitising old paper plans is usually of lower accuracy; it depends on the plan's scale, drafting error and how well it is referenced. Field verification — seeing a valve chamber, a hydrant or a trial pit in place — ties the two sources together and catches gross errors.</p>
        <p>In practice each object is given an accuracy or source tag: &ldquo;measured by GNSS&rdquo;, &ldquo;digitised from a plan&rdquo;, &ldquo;verified on site&rdquo;. Accuracy should not be overstated; a digitised main should still be confirmed from the surface and with a trial pit before any excavation.</p>

        <h2>Loading into the platform</h2>
        <p>The cleaned GIS layer is transferred into the LeakExpert platform (see <a href="/en/platform.html">platform</a>). Pipe and valve geometry, leak points, flow and pressure measurements and field projects then appear together on one map.</p>
        <p>This combination speeds the work up: an acoustic survey result lands on the real main on the map, a DMA boundary is drawn with its valves, a repair record is linked to the pipe segment it belongs to. Measurement and observation data now build up on a queryable layer rather than on a paper sketch.</p>
        <p>The platform also gives the teams a single current source; the field crew, the office and the analysis all look at the same version of the map.</p>

        <h2>Keeping the map current</h2>
        <p>A network map begins to age the moment it is produced. Unless every new connection, every repair, every main renewal and every valve change is posted back to the map, the layer soon falls behind reality.</p>
        <p>The cost of an out-of-date GIS is not just a wrong drawing. A missing main or a wrong diameter corrupts the pipe length and topology input of a <a href="/en/blog/hidrolik-modelleme-nedir.html">hydraulic model</a>; an unknown closed valve pulls model and field apart. In the same way the water balance and loss analysis give unreliable results if the zone boundaries and customer connections are wrong.</p>
        <p>Updating is therefore defined as a workflow: every change made in the field is recorded with its attributes and added to the map. A mapping and updating routine can be planned over a remote or video call; once the existing sketches, plans and records are shared, the data model and the workflow are set together.</p>
        <ul>
          <li>Service scope: <a href="/en/hizmetler.html">Services</a></li>
          <li>Field examples: <a href="/en/projeler/">Projects</a></li>
          <li>Common questions: <a href="/en/sss.html">FAQ</a></li>
        </ul>
      </div>
""",
    ),
    dict(
        slug="kacak-onarimi-ve-dogrulama",
        hero="/assets/blog/kacak-onarimi-ve-dogrulama.webp",
        hero_alt="Kaçak noktasında onarım kazısı",
        hero_alt_en="Repair excavation at a leak point",
        date="2026-09-04",
        h1="Kaçak onarımı ve onarım sonrası doğrulama",
        title="Kaçak Onarımı ve Onarım Sonrası Doğrulama | LeakExpert",
        desc="Kaçak noktasının onarım süreci ve onarımın gerçekten kapandığının doğrulanması: nokta teyidi, onarım tipleri ve onarım sonrası gece debi tekrar ölçümü.",
        lede="Bir kaçağı bulmak işin yarısıdır; diğer yarısı onarımın <strong>gerçekten</strong> kaybı kapattığını göstermektir. Bu yazı, onarım sürecini ve onarım sonrası doğrulamayı özetler.",
        h1_en="Leak repair and post-repair verification",
        title_en="Leak Repair and Post-Repair Verification | LeakExpert",
        desc_en="The repair process for a located leak point and confirming the loss is actually closed: point confirmation, repair types and repeat night-flow measurement.",
        lede_en="Finding a leak is half the job; the other half is showing the repair <strong>actually</strong> closed the loss. This article outlines the repair process and post-repair verification.",
        body="""
      <div class="prose">
        <h2>Kazı öncesi son teyit</h2>
        <p>Bir kaçak noktası <a href="/blog/akustik-su-kacagi-tespiti-nedir.html">akustik tespit</a> ve korelasyonla daraltıldıktan sonra, kazıya başlamadan önce nokta bir kez daha yerinde dinlenir. Zemin mikrofonu ile en yüksek kaçak sesinin alındığı yer işaretlenir; işaret, kazının merkezini ve genişliğini belirler. Amaç, ekskavatörün doğru noktaya, gereğinden geniş olmayan bir çukurla inmesidir.</p>
        <p>İşaretlemeyle birlikte hattın güzergâhı ve derinliği de doğrulanır (bkz. <a href="/blog/boru-hatti-tespiti-nedir.html">boru hattı tespiti</a>). Elektromanyetik hat dedektörü veya yer radarı ile borunun izdüşümü ve yaklaşık gömülme derinliği kontrol edilir; aynı taramada bölgedeki diğer gömülü altyapı — elektrik, gaz, telekom, yağmur suyu — konumlandırılır. Bu adım, kazı sırasında başka bir hattın kesilmesini önler.</p>
        <p>Son teyit verisi krokiye işlenir: nokta koordinatı, tahmini derinlik, çevredeki altyapı ve yüzey durumu (asfalt, parke, yeşil alan). Kapsam belediye ve organize sanayi bölgesi dağıtım şebekeleridir; söz konusu olan sokak ve arter hatlarıdır. Bu kayıt hem idareye iletilen kazı talebinin ekidir hem de onarım sonrası doğrulamanın başlangıç referansıdır.</p>

        <h2>Onarımı kim yapar?</h2>
        <p>Kazı ve boru onarımı, şebekenin sahibi olan idarenin kendi ekibi veya idarenin sözleşmeli yüklenicisi tarafından yapılır. Yol kesme izni, trafik yönetimi, kazı, boru üzerindeki fiziki müdahale, dolgu ve üstyapı onarımı bu ekibin sorumluluğundadır. LeakExpert bu işlerde yer almaz; ana hat kazmaz, boru değiştirmez.</p>
        <p>LeakExpert'in bu projedeki rolü iki noktada toplanır. Birincisi kazı öncesi nokta teyididir: kaçağın tam yerinin ve hattın konumunun kazısız olarak belirlenmesi, böylece idare ekibinin doğru yeri açması. İkincisi onarım sonrası doğrulamadır: onarımın gerçekten kaybı kapatıp kapatmadığının gece debisi tekrar ölçülerek gösterilmesi ve kapanan kaybın raporlanması. İş bölümü bu şekilde nettir.</p>
        <p>Bu ayrım pratik bir nedene dayanır: ana hat müdahalesi yol kesme izni, iş güvenliği düzeni ve şebeke manevrası gerektirir; bunlar idarenin yetki ve sorumluluk alanındadır. LeakExpert ölçüm ve doğrulama tarafında kalarak, onarımın sonucunu bağımsız ve sayısal biçimde ortaya koyar.</p>

        <h2>Onarım tipleri</h2>
        <p>Onarım yöntemi, hasarın türüne ve borunun genel durumuna göre seçilir. Küçük bir delik veya dar bir boyuna çatlak için tamir kelepçesi kullanılır: borunun etrafına oturan, contalı çelik bir bilezik hasarı sarar ve hat kesilmeden sızdırmazlık sağlanır. Kelepçe, sınırlı ve tekil hasarlarda hızlı bir çözümdür.</p>
        <p>Enine kırık, ezilme veya kelepçeyle kapatılamayacak büyüklükte bir hasar varsa, hasarlı kısım kesilip çıkarılır ve yerine yeni bir boru parçası eklenir; iki uçta manşon veya bağlantı elemanıyla birleştirilir. Sızdıran bir bağlantı, vana veya ek parça söz konusuysa o eleman sökülüp yenisiyle değiştirilir.</p>
        <p>Aynı hat bölümünde tekrarlayan arızalar görülüyorsa — malzeme yorulmuş, korozyon ilerlemişse — noktasal onarım yerine belirli bir uzunlukta hat yenilemesi gündeme gelir. Bu karar idareye aittir ve genellikle arıza geçmişi ile hattın yaşına dayanır.</p>

        <h2>Onarım sonrası test</h2>
        <p>Fiziki müdahale bittikten sonra hat yavaşça yeniden basınçlandırılır. Ani basınçlandırma, yeni birleşim yerinde ve komşu bağlantılarda basınç darbesi oluşturabileceği için vana kademeli açılır. Basınç kararlı hâle geldiğinde onarım noktası ve manşonlar gözle ve elle kontrol edilir; nemlenme veya damlama olup olmadığına bakılır.</p>
        <p>Çukur kapatılmadan önce hat yıkanır: açılan uçtan veya en yakın hidranttan su verilerek kazı sırasında içeri girmiş olabilecek toprak ve kir dışarı alınır. Kirlenme şüphesi varsa bölüm dezenfekte edilir ve idarenin uygulamasına göre bakiye klor veya numune ile su kalitesi teyit edilir. Ancak bu kontrollerden sonra dolgu ve üstyapı onarımı yapılır.</p>
        <p>Test sırasında elde edilen gözlemler — basıncın oturma süresi, birleşim yerinin durumu, yıkama süresi — krokiye not edilir. Onarım noktası daha sonra hat üzerinde bir kayıt olarak kalır ve bir sonraki çalışmada referans alınır.</p>

        <h2>Doğrulama: gece debisi tekrar</h2>
        <p>Onarımın kaybı gerçekten kapatıp kapatmadığı, bölgenin gece minimum debisinin onarım öncesi ve sonrası değerleri karşılaştırılarak gösterilir. Gece minimum debisi, tüketimin en düşük olduğu saatlerde (yaklaşık 03:00–05:00) bölge girişinden ölçülen akıştır; bu saatlerde ölçülen akışın büyük kısmı fiziki kaçaktır (bkz. <a href="/blog/debi-olcumu-nedir.html">debi ölçümü</a>, <a href="/blog/dma-nedir.html">DMA</a>).</p>
        <p>Onarımdan birkaç gün sonra, koşullar benzerken (aynı basınç bölgesi, benzer gece, bilinen vana durumu) ölçüm tekrarlanır. Onarım öncesi ile sonrası arasındaki düşüş, o noktada kapatılan kaçak debisidir. Düşüş beklenen mertebedeyse nokta kapanmış sayılır; düşüş yoksa veya küçükse, aynı bölgede başka bir kaçak daha vardır ve arama sürer.</p>
        <p>Tek bir noktanın etkisini görmek için ölçümün hattın doğru kesitinde ve mümkünse dar bir bölgede yapılması önemlidir. Geniş bir bölgede tek bir küçük onarımın etkisi ölçüm gürültüsü içinde kaybolabilir; bu durumda adım testi ile alt hatlara inmek gerekebilir.</p>

        <h2>Raporlama</h2>
        <p>Her onarım, sonuçlarıyla birlikte LeakExpert platformuna işlenir: nokta koordinatı, onarım tarihi (idarenin bildirdiği şekliyle), yapılan onarımın tipi, onarım öncesi ve sonrası gece debisi ve bu ikisinin farkı olan kapanan kayıp. Böylece her proje için ölçülebilir bir kazanım kaydı oluşur.</p>
        <p>Doğrulamada kapanmadığı görülen noktalar tekrar tarama listesine alınır ve yeniden dinleme, korelasyon veya adım testi ile ele alınır. Kapanan noktalar ise bölgenin kayıp bilançosundan düşülür. Bu kayıtların toplamı, <a href="/blog/su-kaybi-dusurme-yol-haritasi.html">su kaybını düşürme programının</a> ilerleyişini gösteren temel veridir. Sonuçlar abartılmadan, ölçülen değerlerle raporlanır.</p>
        <p>Nokta teyidi ve onarım sonrası doğrulama düzeni uzaktan / video görüşmeyle planlanabilir; şebeke krokisi, ölçüm kayıtları ve idarenin onarım bildirimleri paylaşıldıktan sonra doğrulama planı birlikte belirlenir.</p>
        <ul>
          <li>Hizmet kapsamı: <a href="/hizmetler.html">Hizmetler</a></li>
          <li>Saha örnekleri: <a href="/projeler/">Projeler</a></li>
          <li>Sık sorulanlar: <a href="/sss.html">SSS</a></li>
        </ul>
      </div>
""",
        body_en="""
      <div class="prose">
        <h2>Final confirmation before the dig</h2>
        <p>Once a leak point has been narrowed down with <a href="/en/blog/akustik-su-kacagi-tespiti-nedir.html">acoustic detection</a> and correlation, it is listened to once more on site before digging. The spot where the ground microphone is loudest is marked, setting the centre and width of the dig so the excavator opens no wider a pit than needed.</p>
        <p>The marking step also confirms the route and depth of the main (see <a href="/en/blog/boru-hatti-tespiti-nedir.html">pipe locating</a>). An electromagnetic locator or ground penetrating radar checks the pipe's plan position and burial depth, and the same scan locates other buried services, so another line is not cut during the dig.</p>
        <p>The confirmation data goes on the sketch: the point coordinate, the estimated depth, the surrounding services and the surface type. The scope is municipal and organised-industrial-zone distribution networks; the work is on street and arterial mains. This record goes with the excavation request sent to the utility and is the starting reference for verification.</p>

        <h2>Who does the repair?</h2>
        <p>The excavation and repair are done by the utility that owns the network — its own crew or its contractor. Road-opening permits, traffic management, the dig, the work on the pipe, backfill and reinstatement are that crew's responsibility. LeakExpert takes no part in this; it does not dig mains and does not replace pipe.</p>
        <p>LeakExpert's role sits at two points: point confirmation before the dig — fixing the exact position of the leak and of the main without excavation, so the utility crew opens the right place — and verification after the repair, measuring the night flow again to show whether the loss has actually closed and reporting the recovered loss.</p>
        <p>The split has a practical reason: work on a main needs a road closure, a safety plan and network switching, all within the utility's authority. LeakExpert stays on the measurement and verification side and reports the repair result independently, in numbers.</p>

        <h2>Types of repair</h2>
        <p>The repair method follows the kind of damage and the condition of the pipe. For a small hole or a narrow longitudinal crack, a repair clamp is used: a gasketed steel band that seats around the pipe and seals the damage without cutting the line, which suits limited, isolated damage.</p>
        <p>Where there is a circumferential break, a crushed length, or damage too large for a clamp, the damaged part is cut out and a new pipe section fitted in, joined at each end with a coupling. A leaking fitting, valve or joint is removed and renewed.</p>
        <p>If the same length of main shows repeated failures — fatigued material, advanced corrosion — a full renewal of a defined length is considered instead of a spot repair. That decision rests with the utility and draws on the failure history and the age of the pipe.</p>

        <h2>Testing after the repair</h2>
        <p>Once the physical work is done, the main is re-pressurised slowly: a sudden rise can create a surge at the new joint and neighbouring connections, so the valve is opened in stages. Once the pressure has settled, the repair point and couplings are checked by eye and hand for wetting or dripping.</p>
        <p>Before the pit is closed, the main is flushed: water is run from the open end or the nearest hydrant to carry out soil and dirt that entered during the dig. If contamination is suspected, the section is disinfected and the water quality confirmed with a residual-chlorine reading or a sample, per the utility's practice. Only then are backfill and reinstatement done.</p>
        <p>The test observations — the settling time, the joint condition, the flushing time — are noted on the sketch, and the repair point stays as a record on the main for later work.</p>

        <h2>Verification: night flow again</h2>
        <p>Whether the repair has really closed the loss is shown by comparing the zone's minimum night flow before and after. That is the flow measured at the zone inlet during the hours of lowest consumption, roughly 03:00–05:00, when most of the flow is physical leakage (see <a href="/en/blog/debi-olcumu-nedir.html">flow measurement</a>, <a href="/en/blog/dma-nedir.html">DMA</a>).</p>
        <p>A few days later, under similar conditions — same pressure zone, comparable night, known valve state — the measurement is repeated. The drop between before and after is the leak rate closed at that point. A drop of the expected order means the point is closed; no drop means another leak remains.</p>
        <p>To see the effect of a single point, the measurement should be on the right section of main and, where possible, in a small zone. In a large zone one small repair can be lost in measurement noise, and a step test may be needed to reach sub-sections.</p>

        <h2>Reporting</h2>
        <p>Every repair is entered into the LeakExpert platform with its results: the point coordinate, the repair date as notified by the utility, the type of repair, the night flow before and after, and the recovered loss between the two, so each project gains a measurable record of what was won back.</p>
        <p>Points found not to have closed at verification go back on the survey list, taken up again with re-listening, correlation or a step test; points that did close come off the zone's loss balance. Together these records show the progress of a <a href="/en/blog/su-kaybi-dusurme-yol-haritasi.html">water-loss reduction programme</a>, reported with measured values and without overstatement.</p>
        <p>The point-confirmation and post-repair verification routine can be planned over a remote or video call; once the network sketch, measurement records and the utility's repair notifications are shared, the verification plan is set together.</p>
        <ul>
          <li>Service scope: <a href="/en/hizmetler.html">Services</a></li>
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
    ("hidrolik-modelleme-nedir",
     "Hidrolik modelleme nedir?", "Şebekenin bilgisayar benzetimi: girdi verisi, saha kalibrasyonu ve senaryolar.",
     "What is hydraulic modelling?", "A computer simulation of the network: input data, field calibration and scenarios.",
     "/assets/photos/basinc-test.webp"),
    ("boru-hatti-tespiti-nedir",
     "Boru hattı tespiti nedir?", "Metal ve plastik gömülü hatların güzergâh ve derinliğini kazısız belirleme.",
     "What is pipe locating?", "Finding the route and depth of buried metal and plastic mains without excavation.",
     "/assets/blog/boru-hatti-tespiti-nedir.webp"),
    ("sebeke-haritalama-cbs",
     "Şebeke haritalama ve CBS nedir?", "Saha verisini GPS koordinat ve özniteliklerle CBS katmanına ve platforma işleme.",
     "What is network mapping and GIS?", "Turning field data with GPS coordinates and attributes into a GIS layer.",
     "/assets/blog/sebeke-haritalama-cbs.webp"),
    ("kacak-onarimi-ve-dogrulama",
     "Kaçak onarımı ve doğrulama nedir?", "Nokta teyidi, onarım tipleri ve onarım sonrası gece debiyle kapanan kaybın doğrulanması.",
     "Leak repair and verification", "Point confirmation, repair types, and verifying recovered loss with post-repair night flow.",
     "/assets/blog/kacak-onarimi-ve-dogrulama.webp"),
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
