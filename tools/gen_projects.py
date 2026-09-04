# -*- coding: utf-8 -*-
"""Generate all project detail pages + projeler/index.html + sitemap.xml for the
LeakExpert site, bilingual (tr at root, en under /en/).
Shares header/footer/head/lang-switcher/open-script shape with gen_blog.py —
keep the two in sync (PROJECT.md §6)."""
import os, json, html, re
from datetime import date as _date

SITE = r"C:\Users\muham\Desktop\LEAKEXPERT APPS\leakexpert-site"
BASE = "https://sukayipkacaklari.com"
LANGS = ("tr", "en")

BRAND_SVG = '<img src="/assets/img/logo.svg" alt="LeakExpert" width="118" height="34" class="brand__logo">'

PHONE_SVG = ('<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">'
  '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.9.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/></svg>')

# <head> icinde calisan dil acilis script'i. Iki isi var:
#   1) TR|EN degistiricisine yapilan tiklamayi capture fazinda dinleyip secimi
#      localStorage['le-lang']'e yazar. Dinleyici <head>'de baglandigi icin
#      defer'li site.min.js henuz yuklenmemis olsa da ilk tiklama kaydedilir.
#   2) Kayitli secim yoksa yalnizca ana sayfada, site disindan gelen ziyarette ve
#      oturum basina bir kez tarayici diline gore yonlendirir; site ici gezinme
#      (ayni origin referrer) asla ezilmez.
OPEN_SCRIPT = """<script>
(function(){
  var d=document.documentElement,cur=d.lang==='en'?'en':'tr';
  try{
    document.addEventListener('click',function(e){
      for(var n=e.target;n&&n!==document;n=n.parentNode){
        if(n.tagName==='A'){
          var hl=n.getAttribute('hreflang');
          if(hl==='tr'||hl==='en'){try{localStorage.setItem('le-lang',hl);}catch(x){}}
          return;
        }
      }
    },true);
  }catch(e){}
  try{
    var alt=document.querySelector('link[rel="alternate"][hreflang="'+(cur==='en'?'tr':'en')+'"]');
    if(!alt)return;
    var other=alt.getAttribute('href');
    var pref=null;try{pref=localStorage.getItem('le-lang');}catch(e){}
    if(pref==='tr'||pref==='en'){
      if(pref!==cur)location.replace(other);
      return;
    }
    if(d.getAttribute('data-home')!=='1')return;
    if(document.referrer&&document.referrer.indexOf(location.origin+'/')===0)return;
    try{
      if(sessionStorage.getItem('le-lang-redirected'))return;
      sessionStorage.setItem('le-lang-redirected','1');
    }catch(e){}
    var langs=navigator.languages||[navigator.language||''];
    var wantsTr=langs.some(function(l){return /^tr\\b/i.test(l);});
    if(wantsTr!==(cur==='tr'))location.replace(other);
  }catch(e){}
})();
</script>"""

FONTS = (
'<link rel="preload" as="font" type="font/woff2" href="/assets/fonts/bricolage-grotesque-600-800-latin.woff2" crossorigin>\n'
'<link rel="preload" as="font" type="font/woff2" href="/assets/fonts/bricolage-grotesque-600-800-latin-ext.woff2" crossorigin>\n'
'<link rel="preload" as="font" type="font/woff2" href="/assets/fonts/plus-jakarta-sans-400-latin.woff2" crossorigin>\n'
'<link rel="stylesheet" href="/assets/css/fonts.min.css">'
)

# ---------------------------------------------------------------- i18n chrome
UI = {
    "tr": {
        "menu": [("/", "Ana Sayfa"), ("/platform.html", "Platform"), ("/hizmetler.html", "Hizmetler"),
                 ("/blog/", "Blog"), ("/projeler/", "Projeler"), ("/referanslar.html", "Referanslar"),
                 ("/hakkimizda.html", "Hakkımızda"), ("/iletisim.html", "İletişim")],
        "skip": "İçeriğe geç", "menu_aria": "Ana menü", "burger_aria": "Menüyü aç",
        "brand_aria": "LeakExpert ana sayfa", "crumb_aria": "Sayfa işaret yolu",
        "og_locale": "tr_TR", "og_locale_alt": "en_US", "html_lang": "tr",
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
        "home": "Ana Sayfa", "projects": "Projeler",
        "proj_title_suffix": "Su Kaçağı Tespiti Projesi | LeakExpert",
        "result": "Sonuç", "next_project": "Sonraki proje", "related_projects": "İlgili projeler",
        "view": "İncele", "read_project": "Projeyi oku",
        "cta_eyebrow": "Uzaktan görüşelim", "cta_h": "Şebekenizi birlikte değerlendirelim.",
        "cta_p": "Kısa bir görüntülü görüşmede mevcut durumu, yaklaşımı ve kapsamı konuşuruz.",
        "cta_btn": "Görüşme talebi", "cta_btn2": "Tüm projeler",
        "idx_title": "Projeler — Belediye Su Kayıp-Kaçak Çalışmaları | LeakExpert",
        "idx_desc": ("LeakExpert proje arşivi: Kütahya, Batman, Çanakkale, Keşan, Kilis, Sivas, Rize, "
                     "Doğubayazıt, Fatsa, Bodrum ve Mozambik-Beira. Sahadan ölçülmüş sonuçlar."),
        "idx_h1": "Sahadan ölçülmüş sonuçlar.",
        "idx_lede": ("Aşağıdaki rakamlar tamamlanmış çalışmaların raporlarından derlenmiştir. "
                     "Ekonomik büyüklükler tahminidir ve her idarede kurum verisiyle doğrulanır."),
        "idx_cta_eyebrow": "Sırada sizin şebekeniz", "idx_cta_h": "Aynı yöntemi belediyenizde uygulayalım.",
        "idx_cta_p": "Pilot bir etapla başlayıp sonuçları birlikte değerlendirelim.",
        "idx_cta_btn": "Görüşme talebi", "idx_cta_btn2": "Referanslar",
        "itemlist_name": "LeakExpert projeleri",
        "project_card_alt": "{name} projesi",
    },
    "en": {
        "menu": [("/", "Home"), ("/platform.html", "Platform"), ("/hizmetler.html", "Services"),
                 ("/blog/", "Blog"), ("/projeler/", "Projects"), ("/referanslar.html", "References"),
                 ("/hakkimizda.html", "About"), ("/iletisim.html", "Contact")],
        "skip": "Skip to content", "menu_aria": "Main menu", "burger_aria": "Open menu",
        "brand_aria": "LeakExpert home", "crumb_aria": "Breadcrumb",
        "og_locale": "en_US", "og_locale_alt": "tr_TR", "html_lang": "en",
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
        "home": "Home", "projects": "Projects",
        "proj_title_suffix": "Water Leak Detection Project | LeakExpert",
        "result": "Result", "next_project": "Next project", "related_projects": "Related projects",
        "view": "View", "read_project": "Read the project",
        "cta_eyebrow": "Let's meet remotely", "cta_h": "Let's assess your network together.",
        "cta_p": "In a short video call we go over the current situation, the approach and the scope.",
        "cta_btn": "Request a consultation", "cta_btn2": "All projects",
        "idx_title": "Projects — Municipal Water Loss & Leakage Work | LeakExpert",
        "idx_desc": ("LeakExpert project archive: Kütahya, Batman, Çanakkale, Keşan, Kilis, Sivas, Rize, "
                     "Doğubayazıt, Fatsa, Bodrum and Mozambique–Beira. Results measured in the field."),
        "idx_h1": "Results measured in the field.",
        "idx_lede": ("The figures below are compiled from the reports of completed work. Economic magnitudes "
                     "are estimates and are verified with the utility's own data in each case."),
        "idx_cta_eyebrow": "Your network could be next", "idx_cta_h": "Let's apply the same method in your municipality.",
        "idx_cta_p": "Start with a pilot phase and review the results together.",
        "idx_cta_btn": "Request a consultation", "idx_cta_btn2": "References",
        "itemlist_name": "LeakExpert projects",
        "project_card_alt": "{name} project",
    },
}


def pfx(lang):
    return "" if lang == "tr" else "/en"


def rel_href(lang, path):
    if path == "/":
        return pfx(lang) + "/"
    return pfx(lang) + path


def abs_url(lang, path):
    return BASE + (pfx(lang) + "/" if path == "/" else rel_href(lang, path))


def lang_switch(page_path, lang):
    tr_href = "/" if page_path == "/" else page_path
    en_href = "/en/" if page_path == "/" else "/en" + page_path
    tr_a = ' aria-current="true" class="is-active"' if lang == "tr" else ''
    en_a = ' aria-current="true" class="is-active"' if lang == "en" else ''
    return ('      <span class="nav__lang" role="group" aria-label="Language / Dil">\n'
            f'        <a href="{tr_href}" hreflang="tr" lang="tr"{tr_a}>TR</a>\n'
            '        <span class="nav__lang-sep" aria-hidden="true">|</span>\n'
            f'        <a href="{en_href}" hreflang="en" lang="en"{en_a}>EN</a>\n'
            '      </span>')


def header(active, page_path, lang):
    u = UI[lang]
    def a(href, label):
        cur = ' aria-current="page"' if href == active else ''
        return f'      <a href="{rel_href(lang, href)}"{cur}>{label}</a>'
    rows = "\n".join(a(href, label) for href, label in u["menu"])
    return f'''<header class="hdr">
  <div class="wrap hdr__in">
    <a class="brand" href="{rel_href(lang, "/")}" aria-label="{u['brand_aria']}">
      {BRAND_SVG}
    </a>
    <nav class="nav" id="navmenu" aria-label="{u['menu_aria']}">
{rows}
{lang_switch(page_path, lang)}
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
</header>'''


def footer(lang, page_path):
    u = UI[lang]
    tr_href = "/" if page_path == "/" else page_path
    en_href = "/en/" if page_path == "/" else "/en" + page_path
    fp = "\n".join(f'        <li><a href="{rel_href(lang, h)}">{t}</a></li>' for h, t in u["ftr_platform"])
    fc = "\n".join(f'        <li><a href="{rel_href(lang, h)}">{t}</a></li>' for h, t in u["ftr_corp"])
    return f'''<footer class="ftr">
  <div class="wrap">
    <div class="ftr__grid">
      <div>
        <a class="brand" href="{rel_href(lang, "/")}" aria-label="{u['brand_aria']}">
          {BRAND_SVG}
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
  <a class="btn btn--ghost btn--sm" href="{rel_href(lang, "/iletisim.html")}">{u['dock_cta']}</a>
  <a class="btn btn--sm" href="tel:+905396588434">
    {PHONE_SVG}
    0539 658 84 34
  </a>
</nav>

<script src="/assets/js/site.min.js" defer></script>
</body>
</html>'''


def page_head(title, desc, page_path, lang, ogtype, extra_ld):
    u = UI[lang]
    canon = abs_url(lang, page_path)
    tr_url = BASE + ("/" if page_path == "/" else page_path)
    en_url = BASE + ("/en/" if page_path == "/" else "/en" + page_path)
    return f'''<!doctype html>
<html lang="{u['html_lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{html.escape(desc, quote=True)}">
<link rel="canonical" href="{canon}">
<link rel="alternate" hreflang="tr" href="{tr_url}">
<link rel="alternate" hreflang="en" href="{en_url}">
<link rel="alternate" hreflang="x-default" href="{tr_url}">
<meta name="theme-color" content="#ffffff">
<meta property="og:type" content="{ogtype}">
<meta property="og:site_name" content="LeakExpert">
<meta property="og:locale" content="{u['og_locale']}">
<meta property="og:locale:alternate" content="{u['og_locale_alt']}">
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
{OPEN_SCRIPT}
<link rel="stylesheet" href="/assets/css/site.min.css">
{extra_ld}
<!-- Google Analytics 4 — gtag.js kritik yoldan çıkarıldı, boşta yüklenir -->
<link rel="dns-prefetch" href="https://www.googletagmanager.com">
<link rel="dns-prefetch" href="https://www.google-analytics.com">
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-ETN61F721R',{{anonymize_ip:true}});(function(){{function l(){{var s=document.createElement('script');s.async=1;s.src='https://www.googletagmanager.com/gtag/js?id=G-ETN61F721R';document.head.appendChild(s);}}if('requestIdleCallback'in window){{requestIdleCallback(l,{{timeout:3000}});}}else{{window.addEventListener('load',function(){{setTimeout(l,1200);}});}}}})();</script>
</head>
<body>
<a class="skip" href="#main">{u['skip']}</a>
'''

# ---------------------------------------------------------------- project data (tr)
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

# ---------------------------------------------------------------- project data (en)
EN = {
 "kutahya": dict(
   name="Municipality of Kütahya",
   kicker="Project · Municipality of Kütahya · Inner Aegean · 2024–2025",
   h1="Network in the &ldquo;critical&rdquo; band: 432 faults over 348.5 km.",
   lede="In an acoustic leak detection service carried out with the Water and Sewerage Directorate, the fault density found after listening to the 300 km of the initial tender rose well above international thresholds; the scope was extended and the findings were confirmed.",
   desc="Acoustic leak detection on the Kütahya drinking-water network: 348.5 km of main listened, 432 faults found. Density 1.34 faults/km/yr — about three times the EU threshold.",
   spec=[("Initial scope · main listened","300","km",0),
         ("Initial scope · leaks/faults found","403","count",1),
         ("Tender extension · additional listening","48.5","km",0),
         ("Tender extension · additional faults","29","count",0),
         ("Total main listened","348.5","km",0),
         ("Total faults found","432","count",1),
         ("Fault density","1.34","faults/km/yr",1)],
   prose=[("Comparison with international thresholds",
     ["<p>Acoustic detection performance is usually assessed by the <strong>number of faults per km per year</strong>. The <strong>1.34 faults/km/yr</strong> found in the initial work at Kütahya is:</p>",
      "<ul><li>about <strong>3 times</strong> the acceptance limit of EU Directive 2020/2184 (~0.50),</li><li>about <strong>ten times</strong> the AWWA North American average (~0.09),</li><li>within the 1.0–4.0 band defined in academic work as &ldquo;requiring rehabilitation&rdquo;.</li></ul>"]),
     ("The extension decision and its confirmation",
     ["<p>The high density showed the faults to be <strong>systematic</strong>, not random. Finding 29 more faults in the 48.5 km of additional listening carried out under Public Procurement Law No. 4734 confirmed the initial assessment.</p>"]),
     ("Why early detection matters",
     ["<p>Acoustic detection catches the great majority of faults <strong>before the ground breaks</strong>; it reduces the risk of a sudden burst, the cost of an emergency crew and the expense of surface repair.</p>"])],
   photos=[("kutahya/1.jpg","Acoustic correlation · locating between two contact points"),
           ("kutahya/2.jpg","Network main survey")],
   note="Source: the justification report for the Acoustic Leak Detection Service and the field record tables. Comparison values are based on peer-reviewed publications and institutional documents (AWWA 2018; EU Directive 2020/2184; MDPI Water 2023).",
   concl=("Systematic surveying is essential.","The findings showed that the network as a whole is in a serious deterioration process and that a regular, planned acoustic survey programme is needed. Every fault found was passed to the municipality with an urgent-repair priority.")),

 "batman": dict(
   name="Municipality of Batman",
   kicker="Project · Municipality of Batman · South-Eastern Anatolia · two-phase project",
   h1="400 km surveyed, 220 leak points located.",
   lede="In a two-phase study carried out with the BASKİ Directorate of the Municipality of Batman, a total of 400 km of drinking-water main across the city was surveyed by day and night acoustic listening, and invisible physical leaks were located with their coordinates. Flow/pressure measurement, a water balance report and GIS mapping were included.",
   desc="A two-phase acoustic water-loss study on the Batman drinking-water network: 400 km of main listened by day and night, 220 leak points located with coordinates.",
   spec=[("Main listened acoustically (phase 1 + 2)","400","km",1),
         ("Leak points located","220","count",1),
         ("Çamlıca 1 reservoir · estimated physical leakage","~68","m³/h",0),
         ("Physical-loss share of minimum night flow","~70%","",0),
         ("Example: two adjacent faults · loss flow","8","L/s",1)],
   prose=[("Scope of the work",
     ["<p>In two phases, a total of <strong>400 km</strong> of drinking-water main across the city was surveyed by day and night acoustic listening.</p>",
      "<ul><li>installation of a flow and pressure measurement system at the reservoir outlets,</li><li>point-by-point acoustic listening and correlation in the zones with heavy loss,</li><li>reporting of the 220 points found with coordinates, acoustic sound level and photographs, passed to the municipality with a repair priority,</li><li>an IWA water balance report and GIS mapping of all points.</li></ul>"]),
     ("Example: two large adjacent faults",
     ["<p>Just <strong>two</strong> fault points found side by side in the field corresponded on their own to a loss of <strong>8 L/s</strong>: about 252,288 m³ of water a year, about ₺2.77 million in revenue and about ₺882,000 in energy. On the estimate that these two faults have been running for at least 20 years, the cumulative effect is of the order of <strong>10 million m³</strong> and <strong>₺111 million</strong>.</p>",
      "<p>Each of the 220 points located carries a similar loss, though the magnitude varies.</p>"]),
     ("Hydraulic improvement",
     ["<p>At the critical points repaired, network pressure evened out, fluctuations fell and the cascade effect of faults diminished. A general decline in consumption was seen in the flow data. If the work continues, the water-loss rate is expected to fall to around 30%.</p>"])],
   photos=[("batman/1.jpg","Valve chamber · pressure logger on the trunk main"),
           ("batman/2.jpg","Valve chamber work")],
   note="Figures are compiled from the Batman project hand-over presentation (2026) and the water balance reports. Economic magnitudes are calculated on an assumed unit cost and tariff of about ₺11/m³; they are verified with the utility's data.",
   concl=("Scale is the sum of individual faults.","The 220 leaks found over 400 km point to systematic deterioration across the network. Invisible loss grows while a complaint is awaited; active, planned listening catches it before it grows.")),

 "canakkale": dict(
   name="Municipality of Çanakkale",
   kicker="Project · Municipality of Çanakkale · Marmara · 2026 · pilot",
   h1="35.5 km in 4 nights, 22 leaks — and a rising learning curve.",
   lede="A night acoustic listening pilot carried out on part of the İsmetpaşa, Cevat Paşa, Namık Kemal, M. Kemal and Fevzipaşa neighbourhoods of the central drinking-water network.",
   desc="A 4-night acoustic listening pilot on the central Çanakkale drinking-water network: 35,465 m of main, 187 recordings, 94 streets, 22 physical leaks. Finds per night rose every night.",
   spec=[("Main listened (4 nights)","35,465","m",0),
         ("Separate acoustic recordings","187","count",0),
         ("Distinct streets / avenues listened","94","count",0),
         ("Physical water leaks located","22","count",1),
         ("Leak density","~0.62","leaks/km",0),
         ("Daily rise in finds (4 → 7)","+75%","",1)],
   prose=[("Nightly breakdown",
     ["<ul><li>10 Jun · 10,116 m listened, 50 recordings, <strong>4 leaks</strong></li><li>11 Jun · 7,133 m listened, 39 recordings, <strong>5 leaks</strong></li><li>12 Jun · 11,069 m listened, 60 recordings, <strong>6 leaks</strong></li><li>13 Jun · 7,146 m listened, 38 recordings, <strong>7 leaks</strong></li></ul>"]),
     ("Why it matters",
     ["<p>The number of finds <strong>did not fall — it rose</strong>, even on the lower-distance nights. This shows the area is not saturated; yield rose as the crew learned the network and the field behaviour. If the work is stopped, that learning curve and field knowledge are lost.</p>"]),
     ("Economic magnitude (estimated)",
     ["<p>If the 22 leaks found in these 4 nights alone are not repaired, on an assumption of 0.10–0.25 L/s per leak the annual loss is of the order of <strong>69,000–173,000 m³</strong>; at ₺20/m³ that corresponds to <strong>₺1.4–3.5 million</strong> of preventable loss a year.</p>"])],
   photos=[("canakkale/1.jpg","Night shift · point-by-point listening"),
           ("canakkale/2.jpg","Daytime verification listening")],
   note="Source: the 10–13 June 2026 daily work reports, the listening record table and 22 fault detection reports. Economic figures are estimates and are verified with the utility's data. Images represent the method.",
   concl=("Phase 2: continue without interruption.","Verification listening in unsurveyed neighbourhoods and in the zones with dense finds; detection → repair within 48–72 hours → post-repair check. If the detection rate holds, there is potential to find about 330 leaks in 60 working nights.")),

 "kesan": dict(
   name="Municipality of Keşan",
   kicker="Project · Kırklareli · Municipality of Keşan · Thrace · 2026 · pilot",
   h1="56.8 km in six nights, 20 leaks.",
   lede="A pilot application to locate physical water leaks that do not surface on the Keşan drinking-water network by acoustic listening; measurement across 301 street/avenue sections in 7 neighbourhoods.",
   desc="A 6-night acoustic listening pilot on the Keşan drinking-water network: 56.8 km of main, 20 physical leaks, 7 neighbourhoods. On average one leak every 2.8 km of main.",
   spec=[("Main listened (6 nights)","56.8","km",0),
         ("Physical water leaks located","20","count",1),
         ("Neighbourhoods surveyed","7","count",0),
         ("Leak frequency","1 / 2.8","km",0),
         ("Average finds per night","~3.3","leaks",1)],
   prose=[("Findings",
     ["<p>Leaks by neighbourhood: Yukarı Zaferiye 11, Aşağı Zaferiye 4, İspat Cami 3, Cumhuriyet 1, Büyük Cami 1. They concentrate mainly on <strong>old / weak infrastructure mains</strong> and at service connection points; the problem is structural.</p>",
      "<p>Finding no leaks on the nights of 1 Aug and 3 Aug shows those areas are relatively healthy and that resources can be directed to the real problem zones.</p>"]),
     ("Financial impact (with assumptions)",
     ["<p>If these 20 leaks alone are not repaired, at 0.45–1.00 m³/h per leak and 8,760 h/yr the annual loss is <strong>≈ 79,000–175,000 m³</strong>. At a cost of ₺12/m³ and a tariff value of ₺30/m³, that is millions of ₺ a year. Exact values are clarified by a DMA minimum night flow measurement.</p>"]),
     ("Recommendation",
     ["<p>Most of the town was not surveyed. Applying the measured density to the whole town, <strong>hundreds of detectable leaks</strong> are expected. The required cycle: detection → repair → verification → reporting.</p>"])],
   photos=[("kesan/1.jpg","Night acoustic listening (represents the method)"),
           ("kesan/2.jpg","DMA design and measurement plan")],
   note="Source: the 29 July – 3 August 2026 daily work reports and 20 fault detection reports. Images represent the method.",
   concl=("Leak reduction is a matter of continuity.","New leaks form on the network all the time; without regular surveying the loss rate returns to its old level within 1–2 years. A permanent crew and DMA-based monitoring are needed.")),

 "kilis": dict(
   name="Municipality of Kilis",
   kicker="Project · Municipality of Kilis · South-Eastern Anatolia · 2023–2024",
   h1="Mapping the loss with pressure, step and zero-pressure tests.",
   lede="Water-loss detection on the Kilis drinking-water network; installation of pressure data loggers, zero-pressure and step tests, acoustic listening and billing analysis. The work lasted six months.",
   desc="Water-loss detection on the Kilis municipal water network: pressure loggers, zero-pressure and step tests, acoustic listening, GIS mapping (2023–2024).",
   spec=[("Duration","6","months",0),
         ("Pressure monitoring","24/7","logger",0),
         ("Test method","Step + zero-pressure","",1),
         ("Pressure sensor","1–30 bar data logger","",0)],
   prose=[("Method",
     ["<p>24/7 pressure monitoring was carried out by placing <strong>pressure data loggers</strong> at critical points. With a <strong>step test</strong>, mains were closed one by one to narrow down which segment the loss was concentrated in; with a <strong>zero-pressure test</strong>, the tightness of the isolated zones was measured.</p>"]),
     ("Acoustic listening",
     ["<p>In the narrowed-down zones, leak points were located to the metre by night acoustic listening and correlation; each point was recorded with its GPS coordinates, sound level and a photograph.</p>"]),
     ("Billing analysis",
     ["<p>Customer consumption records were reviewed to separate out the <strong>apparent-loss</strong> items (meter error, unauthorised use, billing) and report them independently of the physical loss.</p>"])],
   photos=[("kilis-1.jpg","Kilis · night · acoustic survey with traffic safety"),
           ("kilis-2.jpg","Pressure measurement at a customer point"),
           ("kilis-3.jpg","Data collection panel at the reservoir outlet")],
   note="Images from the field archive of the Municipality of Kilis project.",
   concl=("Physical and apparent loss are measured separately.","Pressure and flow data show where the loss is; billing analysis shows the type of loss. Together they set the right intervention priority.")),

 "sivas": dict(
   name="Municipality of Sivas",
   kicker="Project · Municipality of Sivas · Central Anatolia · 2021",
   h1="12 DMA zones, loss rate from 55% to 25%.",
   lede="To reduce water losses in the central district of Sivas, District Metered Areas (DMAs) and a central monitoring system were commissioned.",
   desc="Installation of 12 DMAs (District Metered Areas) and a water-loss management system in the central district of Sivas. The water-loss rate was cut from 55% to 25%.",
   spec=[("DMA zones installed","12","count",1),
         ("Starting loss rate","55%","",0),
         ("Target / achieved loss rate","25%","",1),
         ("Monitoring","24/7","remote",0)],
   prose=[("The challenge",
     ["<p>The city-wide water-loss rate was above 55% and there was no zonal monitoring infrastructure; it was not known where the loss occurred.</p>"]),
     ("The solution",
     ["<p>12 DMA zones were designed and installed. <strong>Flow and pressure measurement devices</strong> were placed in each zone. A central monitoring system provided minimum night flow tracking and anomaly alerts.</p>"]),
     ("Results",
     ["<ul><li>12 DMA zones installed,</li><li>water-loss rate cut from 55% to <strong>25%</strong>,</li><li>24/7 remote monitoring commissioned,</li><li>repair priorities clarified through zone-based intervention.</li></ul>"])],
   photos=[("sivas/2.jpg","Daytime acoustic listening work"),
           ("sivas/3.jpg","Confirming a located leak by excavation")],
   note="Project summary; exact rates are verified with the utility's water balance records.",
   concl=("A DMA makes the loss visible.","Without district metered areas, loss is only estimated. With a DMA, each zone's night flow is measured; intervention starts with the zone that leaks the most.")),

 "rize": dict(
   name="Municipality of Rize",
   kicker="Project · Municipality of Rize · Eastern Black Sea · 2021",
   h1="Acoustic detection in a rainy climate, on difficult ground.",
   lede="Water-loss detection on the Rize drinking-water network by acoustic listening and correlation; field work carried out on sloping terrain and in high ground moisture.",
   desc="Water-loss detection on the Municipality of Rize drinking-water network by acoustic listening and correlation (2021). Field work on sloping terrain and in high moisture.",
   spec=[("Method","Acoustic + correlation","",1),
         ("Field condition","Sloping terrain · high moisture","",0),
         ("Record","GPS + sound level + photo","",0)],
   prose=[("Field conditions",
     ["<p>Rize&#39;s steep topography and heavy rainfall regime are conditions that make acoustic listening harder: ground moisture carries sound and can produce misleading signals. For this reason every suspect point was confirmed <strong>with a correlator</strong> between two contact points.</p>"]),
     ("Result",
     ["<p>The leaks located were passed to the municipality with coordinates and photographs; a priority order was drawn up for the repair crews.</p>"])],
   photos=[("rize/1.jpg","Point listening with a ground microphone"),
           ("rize/3.jpg","Survey along a sloping main"),
           ("rize/2.jpg","Manhole check")],
   note="Images from the field archive of the Municipality of Rize project (2021).",
   concl=("Difficult ground means more verification.","On moist, sloping ground, listening alone is not enough; correlation and repeat measurement prevent a wrong excavation.")),

 "dogubayazit": dict(
   name="Municipality of Doğubayazıt",
   kicker="Project · Ağrı · Municipality of Doğubayazıt · Eastern Anatolia · 2022",
   h1="DMA-based loss reduction work.",
   lede="Water-loss detection and reduction on the Doğubayazıt drinking-water network with a district metered area approach; flow measurement, acoustic listening and repair follow-up.",
   desc="DMA-based water-loss reduction work on the Municipality of Doğubayazıt drinking-water network (2022): flow measurement, acoustic listening and repair follow-up.",
   spec=[("Approach","DMA-based","",1),
         ("Measurement","Flow + acoustic","",0),
         ("Cycle","Detection → repair → verification","",0)],
   prose=[("The work",
     ["<p>The network was divided into measurable zones; by monitoring each zone's minimum night flow, the mains with heavy loss were identified. Leak points were then located on those mains by acoustic listening.</p>"]),
     ("Repair follow-up",
     ["<p>The finds were passed to the municipality's repair crews; the cycle was closed with a post-repair check listen.</p>"])],
   photos=[("dogubayazit/2.jpg","Main check at an excavation point"),
           ("dogubayazit/1.jpg","Survey along the network route")],
   note="Project summary; images from the field archive (2022).",
   concl=("Progress zone by zone, by measuring.","Rather than surveying the whole city at once, starting with the zone that leaks the most and moving on by verifying uses resources efficiently.")),

 "ordu-fatsa": dict(
   name="Ordu · Municipality of Fatsa",
   kicker="Project · Ordu · Municipality of Fatsa · Black Sea · 2021",
   h1="From detection to excavation, closed-loop field work.",
   lede="Water-loss detection by acoustic listening on the Fatsa drinking-water network and confirmation of the located points by excavation; autumn-season field work.",
   desc="Acoustic water-loss detection on the Ordu — Municipality of Fatsa drinking-water network and confirmation by excavation (2021).",
   spec=[("Method","Acoustic listening + correlation","",1),
         ("Verification","Point confirmation by excavation","",0),
         ("Record","Coordinates + photo + sound level","",0)],
   prose=[("The work",
     ["<p>Suspect mains were listened to by day and night; the points narrowed down by correlation were marked. Each located point was <strong>confirmed by excavation</strong> during repair and the leak position was verified.</p>"]),
     ("Result",
     ["<p>The confirmed points were repaired by the municipality's crews; the coordinated fault records were entered into the GIS environment.</p>"])],
   photos=[("ordu-fatsa/1.jpg","Excavation at a located point"),
           ("ordu-fatsa/2.jpg","Check on the exposed main"),
           ("ordu-fatsa/3.jpg","Preparation before main repair")],
   note="Images from the field archive of the Fatsa project (2021).",
   concl=("Detection is completed by excavation.","However good the acoustic point, the cycle closes with repair and a post-repair check listen.")),

 "bodrum": dict(
   name="Bodrum",
   kicker="Project · Muğla · Bodrum · Aegean · 2024",
   h1="A 70% fall in pipe bursts through pressure management.",
   lede="A pressure management system was installed on the Bodrum drinking-water network to prevent bursts caused by high pressure; pressure imbalances arising from elevation differences were resolved.",
   desc="Installation of a pressure management system on the Bodrum drinking-water network: with PRVs and pressure-reducing valves, pipe bursts fell by 70% and energy costs by 30%.",
   spec=[("Pipe bursts","70%","reduction",1),
         ("Energy cost","30%","saving",1),
         ("System installed","PRV + pressure-reducing valve","",0),
         ("Monitoring","Central pressure tracking","",0)],
   prose=[("The challenge",
     ["<p>Large elevation differences caused pressure imbalances on the network; at night, excess pressure caused pipe bursts.</p>"]),
     ("The solution",
     ["<p>Pressure-reducing valves and <strong>PRV (Pressure Reducing Valve)</strong> systems were installed. Pressure monitoring points were set up and central tracking commissioned; night pressure was optimised.</p>"]),
     ("Results",
     ["<ul><li>pipe bursts fell by <strong>70%</strong>,</li><li>night pressure optimisation was achieved,</li><li>network service life was extended,</li><li>a <strong>30%</strong> saving in energy costs was achieved.</li></ul>"])],
   photos=[("bodrum/1.jpg","Pressure measurement at a customer point"),
           ("bodrum/2.jpg","DMA / pressure zone planning")],
   note="Project summary; exact values are verified with the utility's operating records.",
   concl=("Managing pressure cuts both loss and bursts.","Excess pressure raises both the leak flow and the risk of new bursts. Pressure management is one of the lowest-cost loss reduction methods.")),

 "mozambik": dict(
   name="Mozambique · Beira",
   kicker="Project · Mozambique · Beira · International · 2024",
   h1="Abroad: the Beira water leak detection study.",
   lede="Field work to locate water leaks on the drinking-water network of the city of Beira, Mozambique; applying the acoustic method in a hot climate and different infrastructure conditions.",
   desc="A water leak detection study on the Mozambique — Beira drinking-water network. LeakExpert's overseas field experience.",
   spec=[("Country","Mozambique","",1),
         ("City","Beira","",0),
         ("Method","Acoustic listening + flow measurement","",0)],
   prose=[("The work",
     ["<p>Suspect zones on the Beira network were surveyed by acoustic listening and flow measurement; working with the local team, the detection and recording method was transferred.</p>"]),
     ("Why it matters",
     ["<p>Water-loss management is a universal engineering problem; the method and equipment can be adapted to different climate and infrastructure conditions.</p>"])],
   photos=[("mozambik/1.jpg","Drinking-water infrastructure")],
   note="Images represent the work.",
   concl=("The method knows no borders.","The IWA water balance, acoustic detection and the DMA approach can be applied abroad just as in Turkey.")),
}

ORDER = [p["slug"] for p in P]


def LP(p, key, lang):
    return EN[p["slug"]][key] if lang == "en" else p[key]


def spec_html(rows):
    out = ['      <dl class="spec">']
    for label, val, unit, hi in rows:
        u = f'<span class="u">{unit}</span>' if unit else ''
        cls = ' spec__row--hi' if hi else ''
        out.append(f'        <div class="spec__row{cls}"><dt>{label}</dt><dd>{val}{u}</dd></div>')
    out.append('      </dl>')
    return "\n".join(out)


def render(i, p, lang):
    u = UI[lang]
    slug = p["slug"]
    page_path = f"/projeler/{slug}.html"
    canon = abs_url(lang, page_path)
    name = LP(p, "name", lang)
    kicker = LP(p, "kicker", lang)
    h1 = LP(p, "h1", lang)
    lede = LP(p, "lede", lang)
    desc = LP(p, "desc", lang)
    photos = LP(p, "photos", lang)
    note = LP(p, "note", lang)
    concl = LP(p, "concl", lang)
    title = f'{name} {u["proj_title_suffix"]}'
    nextp = P[(i + 1) % len(P)]
    rel3 = [P[(i + k) % len(P)] for k in (1, 2, 3)]
    _ym = re.search(r"(20\d{2})", kicker)
    _year = _ym.group(1) if _ym else "2024"
    _head = (h1.replace('&ldquo;', '').replace('&rdquo;', '').replace('&#39;', '’')
             .replace('&nbsp;', ' ').replace('"', "'"))
    _desc = desc.replace('"', "'")
    _imgs = ",".join(f'"{BASE}/assets/projects/{src.replace(".jpg", ".webp")}"'
                     for src, _ in photos)
    ld = f'''<script type="application/ld+json">
{{ "@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
 {{"@type":"ListItem","position":1,"name":"{u['home']}","item":"{BASE}{pfx(lang)}/"}},
 {{"@type":"ListItem","position":2,"name":"{u['projects']}","item":"{abs_url(lang, "/projeler/")}"}},
 {{"@type":"ListItem","position":3,"name":"{name}","item":"{canon}"}} ]}}
</script>
<script type="application/ld+json">
{{ "@context":"https://schema.org","@type":"Article",
"headline":"{name} — {_head}",
"description":"{_desc}",
"inLanguage":"{'en-US' if lang == 'en' else 'tr-TR'}","articleSection":"{u['projects']}",
"mainEntityOfPage":{{"@type":"WebPage","@id":"{canon}"}},
"isPartOf":{{"@type":"CollectionPage","@id":"{abs_url(lang, "/projeler/")}"}},
"about":{{"@type":"Thing","name":"{'Water loss and leak detection' if lang == 'en' else 'Su kayıp-kaçak tespiti'}"}},
"datePublished":"{_year}-01-01","dateModified":"2026-09-01",
"author":{{"@type":"Organization","name":"LeakExpert","url":"{BASE}/"}},
"publisher":{{"@type":"Organization","name":"LeakExpert","url":"{BASE}/","logo":{{"@type":"ImageObject","url":"{BASE}/assets/img/icon.png"}}}},
"image":[{_imgs}]}}
</script>'''

    figs = []
    for j, (src, cap) in enumerate(photos):
        figs.append(f'''        <div class="figure figure--wide{' rv' if j==0 else ' rv rv-2'}">
          <img src="/assets/projects/{src.replace(".jpg",".webp")}" alt="{cap}" loading="lazy" decoding="async">
          <span class="figure__tag">{cap}</span>
        </div>''')
    fig_block = "\n".join(figs)

    prose_html = []
    for h2, paras in LP(p, "prose", lang):
        prose_html.append(f'          <h2>{h2}</h2>')
        prose_html.extend('          ' + para for para in paras)
    prose_html = "\n".join(prose_html)

    r0, r1, r2 = ({"slug": x["slug"], "name": LP(x, "name", lang),
                   "meta": LP(x, "kicker", lang).split(" · ", 1)[-1]} for x in rel3)
    body = f'''{header("/projeler/", page_path, lang)}

<main id="main">
  <div class="wrap">
    <nav class="crumb" aria-label="{u['crumb_aria']}">
      <a href="{rel_href(lang, "/")}">{u['home']}</a><span class="sep">/</span>
      <a href="{rel_href(lang, "/projeler/")}">{u['projects']}</a><span class="sep">/</span>
      <span aria-current="page">{name}</span>
    </nav>
  </div>

  <article>
  <section class="phead">
    <div class="wrap">
      <p class="eyebrow">{kicker}</p>
      <h1>{h1}</h1>
      <p class="lede">{lede}</p>
    </div>
  </section>

  <section class="section section--tight">
    <div class="wrap">
{spec_html(LP(p, "spec", lang))}
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
          <p class="muted mono fs-74">{note}</p>
        </div>
      </div>
    </div>
  </section>

  <section class="section section--panel">
    <div class="wrap">
      <p class="eyebrow eyebrow--ok rv">{u['result']}</p>
      <h2 class="h-sec rv">{concl[0]}</h2>
      <p class="lede rv mt-14">{concl[1]}</p>
      <div class="mt-l rv"><a class="link-arw" href="{rel_href(lang, "/projeler/" + nextp["slug"] + ".html")}">{u['next_project']}: {LP(nextp, "name", lang)}</a></div>
    </div>
  </section>

  <section class="section section--tight">
    <div class="wrap">
      <p class="eyebrow rv">{u['related_projects']}</p>
      <div class="cards cards--3 mt-m">
        <a class="card rv" href="{rel_href(lang, "/projeler/" + r0["slug"] + ".html")}"><h3>{r0["name"]}</h3><p>{r0["meta"]}</p><span class="link-arw">{u['view']}</span></a>
        <a class="card rv" href="{rel_href(lang, "/projeler/" + r1["slug"] + ".html")}"><h3>{r1["name"]}</h3><p>{r1["meta"]}</p><span class="link-arw">{u['view']}</span></a>
        <a class="card rv" href="{rel_href(lang, "/projeler/" + r2["slug"] + ".html")}"><h3>{r2["name"]}</h3><p>{r2["meta"]}</p><span class="link-arw">{u['view']}</span></a>
      </div>
    </div>
  </section>

  <section class="section section--tight cta-band">
    <div class="wrap">
      <div>
        <p class="eyebrow">{u['cta_eyebrow']}</p>
        <h2>{u['cta_h']}</h2>
        <p class="lede mt-14">{u['cta_p']}</p>
      </div>
      <div class="cta-band__act">
        <a class="btn" href="{rel_href(lang, "/iletisim.html")}">{u['cta_btn']} <span class="arw" aria-hidden="true">→</span></a>
        <a class="btn btn--ghost" href="{rel_href(lang, "/projeler/")}">{u['cta_btn2']}</a>
      </div>
    </div>
  </section>
  </article>
</main>

{footer(lang, page_path)}'''

    return page_head(title, desc, page_path, lang, "article", ld) + body


def card(p, lang):
    u = UI[lang]
    src = "/assets/projects/" + p["photos"][0][0].replace(".jpg", ".webp")
    st = LP(p, "spec", lang)[:3]
    stats = "".join(f'<div><b>{v}{(" "+un) if un else ""}</b><span>{l}</span></div>' for l, v, un, _ in st)
    return f'''      <article class="case rv">
        <div class="case__media"><img src="{src}" alt="{u['project_card_alt'].format(name=LP(p, "name", lang))}" loading="lazy"></div>
        <div class="case__body">
          <span class="case__kicker">{LP(p, "kicker", lang)}</span>
          <h3>{LP(p, "h1", lang)}</h3>
          <div class="case__stats">{stats}</div>
          <a class="link-arw" href="{rel_href(lang, "/projeler/" + p["slug"] + ".html")}">{u['read_project']}</a>
        </div>
      </article>'''


def build_index(lang):
    u = UI[lang]
    page_path = "/projeler/"
    cards = "\n".join(card(p, lang) for p in P)
    idx_ld = f'''<script type="application/ld+json">
{{ "@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
 {{"@type":"ListItem","position":1,"name":"{u['home']}","item":"{BASE}{pfx(lang)}/"}},
 {{"@type":"ListItem","position":2,"name":"{u['projects']}","item":"{abs_url(lang, page_path)}"}} ]}}
</script>
<script type="application/ld+json">
{{ "@context":"https://schema.org","@type":"ItemList","name":"{u['itemlist_name']}","itemListElement":[
{",".join(f'{{"@type":"ListItem","position":{i+1},"url":"{abs_url(lang, "/projeler/" + p["slug"] + ".html")}","name":"{LP(p, "name", lang)}"}}' for i, p in enumerate(P))} ]}}
</script>'''

    idx = page_head(u["idx_title"], u["idx_desc"], page_path, lang, "website", idx_ld)
    idx += f'''{header("/projeler/", page_path, lang)}

<main id="main">
  <div class="wrap">
    <nav class="crumb" aria-label="{u['crumb_aria']}">
      <a href="{rel_href(lang, "/")}">{u['home']}</a><span class="sep">/</span><span aria-current="page">{u['projects']}</span>
    </nav>
  </div>

  <section class="phead">
    <div class="wrap">
      <p class="eyebrow">{u['projects']}</p>
      <h1>{u['idx_h1']}</h1>
      <p class="lede">{u['idx_lede']}</p>
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
        <p class="eyebrow">{u['idx_cta_eyebrow']}</p>
        <h2>{u['idx_cta_h']}</h2>
        <p class="lede mt-14">{u['idx_cta_p']}</p>
      </div>
      <div class="cta-band__act">
        <a class="btn" href="{rel_href(lang, "/iletisim.html")}">{u['idx_cta_btn']} <span class="arw" aria-hidden="true">→</span></a>
        <a class="btn btn--ghost" href="{rel_href(lang, "/referanslar.html")}">{u['idx_cta_btn2']}</a>
      </div>
    </div>
  </section>
</main>

{footer(lang, page_path)}'''
    out_dir = os.path.join(SITE, "en", "projeler") if lang == "en" else os.path.join(SITE, "projeler")
    os.makedirs(out_dir, exist_ok=True)
    open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8", newline="").write(idx)
    print("wrote", ("en/" if lang == "en" else "") + "projeler/index.html")


# ---------------------------------------------------------------- write pages
for lang in LANGS:
    out_dir = os.path.join(SITE, "en", "projeler") if lang == "en" else os.path.join(SITE, "projeler")
    os.makedirs(out_dir, exist_ok=True)
    for i, p in enumerate(P):
        out = os.path.join(out_dir, p["slug"] + ".html")
        open(out, "w", encoding="utf-8", newline="").write(render(i, p, lang))
        print("wrote", os.path.relpath(out, SITE))
    build_index(lang)

# ---------------------------------------------------------------- sitemap.xml
LM = _date.today().isoformat()
sm = ['<?xml version="1.0" encoding="UTF-8"?>',
      '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
      'xmlns:image="http://www.google.com/schemas/sitemap-image/1.1" '
      'xmlns:xhtml="http://www.w3.org/1999/xhtml">']


def u(path, cf, pr, imgs=None):
    tr = BASE + ("/" if path == "/" else path)
    en = BASE + ("/en/" if path == "/" else "/en" + path)
    for loc in (tr, en):
        sm.append(f'  <url><loc>{loc}</loc><lastmod>{LM}</lastmod><changefreq>{cf}</changefreq><priority>{pr}</priority>')
        sm.append(f'    <xhtml:link rel="alternate" hreflang="tr" href="{tr}"/>')
        sm.append(f'    <xhtml:link rel="alternate" hreflang="en" href="{en}"/>')
        sm.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{tr}"/>')
        for im in (imgs or []):
            sm.append(f'    <image:image><image:loc>{BASE}{im}</image:loc></image:image>')
        sm.append('  </url>')


u("/", "weekly", "1.0", ["/assets/img/og-cover.png"])
u("/platform.html", "monthly", "0.9")
u("/hizmetler.html", "monthly", "0.9", ["/assets/photos/gece-operasyon.webp", "/assets/photos/basinc-logger.webp"])
u("/projeler/", "weekly", "0.8")
for pp in P:
    u(f"/projeler/{pp['slug']}.html", "monthly", "0.7",
      ["/assets/projects/" + ph[0].replace('.jpg', '.webp') for ph in pp['photos']])
u("/blog/", "monthly", "0.8")
for _rs in ("su-kacagi-nasil-anlasilir", "debi-olcumu-nedir", "basinc-yonetimi-nedir", "akustik-su-kacagi-tespiti-nedir", "dma-nedir", "adim-testi-nedir", "sifir-basinc-testi-nedir", "hidrolik-modelleme-nedir", "boru-hatti-tespiti-nedir", "sebeke-haritalama-cbs", "kacak-onarimi-ve-dogrulama", "su-kaybi-dusurme-yol-haritasi"):
    u(f"/blog/{_rs}.html", "yearly", "0.7")
u("/referanslar.html", "monthly", "0.8")
u("/hakkimizda.html", "monthly", "0.7", ["/assets/team/hasan-koramaz.webp", "/assets/team/muhammed-koramaz.webp"])
u("/sss.html", "monthly", "0.7")
u("/iletisim.html", "yearly", "0.8")
u("/gizlilik.html", "yearly", "0.2")
sm.append('</urlset>')
open(os.path.join(SITE, "sitemap.xml"), "w", encoding="utf-8", newline="\n").write("\n".join(sm) + "\n")
print("wrote sitemap.xml —", len(P), "project urls x2 langs + images")
