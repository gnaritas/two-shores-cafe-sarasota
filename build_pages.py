#!/usr/bin/env python3
"""build_pages.py — Two Shores Café (Sarasota FL), template v2, card t_d85b08d2.
Custom identity: "two shores of the Rio de la Plata" — petrol/tide night hero, cream paper
body, dulce-amber accents, twin-wave motif. No builder runtime, no third-party JS.
Facts ONLY from: Business Debut 2026-09-04 interview; IG @twoshorescafe bio+posts;
FB Page intro (id 61593478889291); GBP card pid ChIJA_6h5kcVw4gRx0sbmigPGhI (scan 11-27).
Built 2026-11-27. <!-- BUILT-2026-11-27 --> marker per ruling uid 3034."""
import os, json, html

HERE = os.path.dirname(os.path.abspath(__file__))
PUBLIC = os.path.join(HERE, "public")
FACTS = json.load(open(os.path.join(HERE, "site_facts.json")))
ORIGIN = "https://two-shores-cafe-sarasota-demo.up.railway.app"

SITE = "Two Shores Café"
TEL = FACTS["phone"]
TEL_HREF = "tel:" + FACTS["phone_e164"]
EMAIL = FACTS["email"]
ADDR1 = "7321 N Tamiami Trail"
ADDR_FULL = "7321 N Tamiami Trail, Sarasota, FL 34243"
FB = "https://www.facebook.com/profile.php?id=61593478889291"
IG = "https://www.instagram.com/twoshorescafe/"
OG_URL = ORIGIN + "/og.png"
MAPQ = "https://www.google.com/maps?q=" + ADDR1.replace(" ", "+") + "+Sarasota,+FL+34243&output=embed"
HRS_SHORT = "Mon–Sat 7 a.m.–5 p.m. · Sun 7 a.m.–3 p.m."

def esc(s): return html.escape(str(s), quote=True)

# ---------------- shared chrome ----------------
WAVES_GLYPH = ('<svg class="mark" viewBox="0 0 40 26" width="30" height="19" aria-hidden="true" focusable="false">'
 '<path d="M2 8c4-6 8-6 12 0s8 6 12 0 8-6 12 0" fill="none" stroke="#c9d7db" stroke-width="2.4" stroke-linecap="round"/>'
 '<path d="M2 18c4-6 8-6 12 0s8 6 12 0 8-6 12 0" fill="none" stroke="#d18a3a" stroke-width="2.4" stroke-linecap="round"/></svg>')

def head(title, path, desc, ld=None):
    ld_block = f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>' if ld else ""
    return f'''<!DOCTYPE html>
<!-- BUILT-2026-11-27 -->
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="noindex, nofollow">
<link rel="canonical" href="{ORIGIN}{path}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{esc(SITE)}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{ORIGIN}{path}">
<meta property="og:image" content="{OG_URL}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{OG_URL}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/style.css">
{ld_block}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site">
  <a class="brand" href="/">{WAVES_GLYPH}<span>Two&nbsp;Shores&nbsp;<em>Café</em></span></a>
  <nav aria-label="Main">
    <a href="/menu">Menu</a>
    <a href="/uruguayan-bakery-sarasota">Bakery</a>
    <a href="/visit">Visit</a>
    <a href="/contact">Contact</a>
    <a class="btn call" href="{TEL_HREF}">Call {esc(TEL)}</a>
  </nav>
</header>
<main id="main">
'''

FOOTER = f'''</main>
<footer class="site">
  <div class="fwrap">
    <p class="fbrand">{WAVES_GLYPH} Two Shores Café — a Uruguayan-Argentinian coffee shop &amp; bakery in Sarasota, Florida.</p>
    <address class="fnap">{esc(ADDR_FULL)} · <a href="{TEL_HREF}">{esc(TEL)}</a> · <a href="mailto:{EMAIL}">{EMAIL}</a></address>
    <p class="fhrs">{esc(HRS_SHORT)} · <a href="{FB}">Facebook</a> · <a href="{IG}">Instagram</a></p>
    <p class="footline">{esc(ADDR1)}, Sarasota, FL 34243</p>
  </div>
</footer>
</body>
</html>
'''

def MAPBLOCK(id_, h=380):
    return (f'<div class="mapcell"><iframe title="Map showing Two Shores Café at {esc(ADDR1)}, Sarasota, FL 34243" '
            f'src="{MAPQ}" width="100%" height="{h}" style="border:0;border-radius:14px" referrerpolicy="no-referrer-when-downgrade" '
            f'tabindex="0" loading="eager"></iframe></div>')

# ---------------- JSON-LD pieces ----------------
GEO = {"@type": "GeoCoordinates", "latitude": float(FACTS["lat"]), "longitude": float(FACTS["lon"])}
POSTAL = {"@type": "PostalAddress", "streetAddress": ADDR1, "addressLocality": "Sarasota",
          "addressRegion": "FL", "postalCode": "34243", "addressCountry": "US"}
HOURS = [
    {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
     "opens": "07:00", "closes": "17:00"},
    {"@type": "OpeningHoursSpecification", "dayOfWeek": "Sunday", "opens": "07:00", "closes": "15:00"},
]
def ld_cafe(url_root):
    return {
        "@type": ["CafeOrCoffeeShop", "BakeryBusiness"], "@id": url_root + "/#cafe",
        "name": SITE, "url": url_root + "/", "telephone": "+1 941 298 9252",
        "image": OG_URL, "address": POSTAL, "geo": GEO,
        "openingHoursSpecification": HOURS,
        "servesCuisine": ["Uruguayan", "Argentinian"],
        "sameAs": [FB, IG],
        "hasMenu": {"@type": "Menu", "@id": url_root + "/menu#menu", "name": "Counter menu",
                    "hasMenuItem": [
                        {"@type": "MenuItem", "name": "Alfajores de chocolate", "description": "Soft cookies filled with dulce de leche, coated in chocolate — big ones and small"},
                        {"@type": "MenuItem", "name": "Rosca de chicharrones", "description": "Ring bread baked with chicharrones, out of the oven around 9 a.m."},
                        {"@type": "MenuItem", "name": "Budín Cake d'Oro", "description": "Pound cake, featured in the shop's weekend deal"},
                        {"@type": "MenuItem", "name": "Lomito", "description": "Grilled beef sandwich, made to order on grill days"},
                        {"@type": "MenuItem", "name": "Chivito al pan", "description": "Uruguayan classic sandwich, made to order on grill days"},
                        {"@type": "MenuItem", "name": "Choripán", "description": "Chorizo in bread, grilled to order"},
                        {"@type": "MenuItem", "name": "Milanesa de carne", "description": "Breaded beef, made to order on grill days"},
                        {"@type": "MenuItem", "name": "Coffee", "description": "Counter-service coffee, all day"}
                    ]}
    }
def ld_webpage(name, path, desc, entity=False, crumbs=None):
    node = {"@type": "WebPage", "@id": ORIGIN + path, "url": ORIGIN + path,
            "name": name, "description": desc, "inLanguage": "en"}
    if entity: node["about"] = {"@id": ORIGIN + "/#cafe"}
    if crumbs: node["breadcrumb"] = {"@id": ORIGIN + path + "#bread"}
    return node
def ld_crumbs(path, items):
    return {"@type": "BreadcrumbList", "@id": ORIGIN + path + "#bread",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": ORIGIN + u}
                                for i, (n, u) in enumerate(items)]}
def ld_service(name, path, stype, desc):
    return {"@type": "Service", "@id": ORIGIN + path + "#service", "name": name,
            "serviceType": stype, "description": desc,
            "areaServed": {"@type": "AdministrativeArea", "name": "Sarasota, Florida"},
            "provider": {"@id": ORIGIN + "/#cafe"}, "url": ORIGIN + path}

def ld_graph(parts): return {"@context": "https://schema.org", "@graph": parts}

# ---------------- pages ----------------
def page_home():
    faq = [
        ("What is on the menu at Two Shores Café?",
         "Uruguayan pastries and breads baked in-house — alfajores de chocolate, roscas de chicharrones, budines — plus counter-service coffee, and on grill days chivito, lomito, choripán and milanesa made to order. The counter rotates; the day's specials are posted on Instagram and Facebook."),
        ("Are you open on Sunday?",
         "Yes. Two Shores Café is open Monday through Saturday 7 a.m.–5 p.m. and Sunday 7 a.m.–3 p.m. Holiday hours are announced on Facebook and Instagram."),
        ("Can I order in Spanish?",
         "Sí, se puede pedir en español. The counter is bilingual — Spanish and English both welcome."),
        ("Do you host events?",
         "Yes — cultural events like the tango afternoon on Saturday, December 5 at 3 p.m. Dates are announced on the café's Instagram and Facebook pages."),
    ]
    ld = ld_graph([
        {"@type": "WebSite", "@id": ORIGIN + "/#site", "url": ORIGIN + "/", "name": SITE + ", Sarasota FL",
         "publisher": {"@id": ORIGIN + "/#cafe"}, "inLanguage": "en"},
        ld_cafe(ORIGIN),
        ld_webpage("Two Shores Café — Uruguayan Bakery & Coffee, Sarasota FL", "/",
                   "Uruguayan pastries, breads and counter-service coffee in Sarasota — alfajores, roscas de chicharrones, grill-day chivito and choripán. Mon–Sat 7–5, Sun 7–3.",
                   entity=True, crumbs=True),
        ld_crumbs("/", [(SITE, "/")]),
        {"@type": "FAQPage", "@id": ORIGIN + "/#faq", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]},
    ])
    faq_html = "".join(
        f'<div class="qa"><h3>{esc(q)}</h3><p>{esc(a)}</p></div>' for q, a in faq)
    return head("Two Shores Café — Uruguayan Bakery & Coffee, Sarasota FL", "/",
                "Uruguayan pastries, breads and counter-service coffee at 7321 N Tamiami Trail, Sarasota, FL. Alfajores, roscas de chicharrones, grill-day sandwiches. Open Mon–Sat 7–5, Sun 7–3.", ld) + f'''
<section class="tide">
  <div class="wrap hero">
    <p class="eyebrow">Uruguayan-Argentinian coffee shop · Sarasota, Florida</p>
    <h1>Uruguayan pastries and counter coffee — seven mornings a&nbsp;week.</h1>
    <p class="lead">Two Shores Café bakes the pastries and breads Valeria Borba and Milton Rodriguez grew up with in Uruguay — and pulls coffee at the counter all day, at {esc(ADDR1)} in Sarasota.</p>
    <p class="cta-row"><a class="btn solid" href="/menu">See what&rsquo;s on the counter</a> <a class="btn ghost" href="{TEL_HREF}">Call {esc(TEL)}</a></p>
    <p class="openline">{esc(HRS_SHORT)}<br>{esc(ADDR_FULL)}</p>
  </div>
  <svg class="seaway" viewBox="0 0 1440 110" preserveAspectRatio="none" aria-hidden="true" focusable="false">
    <path d="M0 44c120-36 240-36 360 0s240 36 360 0 240-36 360 0 120 36 0 36V110H0Z" fill="#faf4e6"/>
    <path d="M0 70c120-36 240-36 360 0s240 36 360 0 240-36 360 0 120 36 0 36" fill="none" stroke="#d18a3a" stroke-width="3"/>
  </svg>
</section>

<section class="strip">
  <div class="wrap quote-grid">
    <blockquote>
      <p>“When we moved to Sarasota, Florida, there was nothing here from our country, so we wanted to bring part of our culture to this place.”</p>
      <cite>Valeria Borba, co-owner — Business Debut, September 2026</cite>
    </blockquote>
    <div class="story">
      <h2>Two shores, one counter</h2>
      <p>Valeria and Milton — born and raised in Uruguay, married, with a shop two blocks from their house — opened Two Shores Café on Saturday, September 5, 2026, with free coffee and a pastry for everyone who came. They oversee the baking and the counter themselves with a small team.</p>
      <p>The idea was simple: the pastries, breads and grilled sandwiches they grew up with, the kind Valeria told the press she felt Sarasota customers had not seen yet — served the way a café in Montevideo serves them.</p>
      <p class="cta-row"><a class="btn line" href="/visit">Hours &amp; directions</a></p>
    </div>
  </div>
</section>

<section class="cards">
  <div class="wrap">
    <h2 class="sec">On the counter</h2>
    <div class="grid3">
      <article class="card">
        <h3><a href="/uruguayan-bakery-sarasota">The bakery</a></h3>
        <p>Chocolate alfajores filled with dulce de leche, rosca de chicharrones out of the oven around 9 a.m., budines on the weekend counter.</p>
        <p class="more"><a href="/uruguayan-bakery-sarasota">Breads &amp; pastries →</a></p>
      </article>
      <article class="card">
        <h3><a href="/parrilla-sarasota">Grill days</a></h3>
        <p>When the parrilla is lit: lomito, chivito al pan, choripán and milanesa de carne — made to order, announced the day it happens.</p>
        <p class="more"><a href="/parrilla-sarasota">From both shores →</a></p>
      </article>
      <article class="card">
        <h3><a href="/menu">Coffee &amp; specials</a></h3>
        <p>Counter-service coffee, all day. Today&rsquo;s bakes, grill days and weekend deals are posted on Instagram and Facebook.</p>
        <p class="more"><a href="/menu">Full menu page →</a></p>
      </article>
    </div>
  </div>
</section>

<section class="findus">
  <div class="wrap find-grid">
    <div>
      <h2>Seven mornings, both languages</h2>
      <ul class="hrs">
        <li><span>Monday – Saturday</span><b>7 a.m. – 5 p.m.</b></li>
        <li><span>Sunday</span><b>7 a.m. – 3 p.m.</b></li>
      </ul>
      <p>Sí, se puede pedir en español. Holiday hours are announced on Facebook and Instagram. Cultural events — like the tango afternoon on Saturday, December 5 at 3 p.m. — land on the same pages.</p>
      <p class="cta-row"><a class="btn solid dark" href="{TEL_HREF}">Call {esc(TEL)}</a> <a class="btn line" href="/contact">Send a note</a></p>
    </div>
    {MAPBLOCK("m-home")}
  </div>
</section>

<section class="faq">
  <div class="wrap">
    <h2 class="sec">Questions people ask</h2>
    <div class="faq-grid">{faq_html}</div>
  </div>
</section>
''' + FOOTER

def page_menu():
    ld = ld_graph([
        {"@type": "MenuPage", "@id": ORIGIN + "/menu#page", "url": ORIGIN + "/menu",
         "name": "Menu — Two Shores Café, Sarasota FL", "inLanguage": "en",
         "mainEntity": {"@id": ORIGIN + "/menu#menu"}, "about": {"@id": ORIGIN + "/#cafe"},
         "breadcrumb": {"@id": ORIGIN + "/menu#bread"}},
        ld_cafe(ORIGIN)["hasMenu"],
        ld_crumbs("/", [(SITE, "/")]),
        ld_crumbs("/menu", [(SITE, "/"), ("Menu", "/menu")]),
    ])
    return head("Menu — Two Shores Café, Sarasota FL", "/menu",
                "What Two Shores Café serves: chocolate alfajores, rosca de chicharrones, budines, Uruguayan breads, grill-day chivito, lomito, choripán, milanesa and counter coffee.", ld) + f'''
<section class="pagehead"><div class="wrap">
  <p class="eyebrow">The counter</p>
  <h1>What&rsquo;s on the counter</h1>
  <p class="lead">The menu rotates like it does back home — the bakes change with the week, the grill lights on announced days. Today&rsquo;s specials ride on <a href="{IG}">Instagram</a> and <a href="{FB}">Facebook</a>; this is the regular cast.</p>
</div></section>

<section class="menu">
  <div class="wrap mgrid">
    <article class="mcol">
      <h2>Bakery counter <a class="inlnk" href="/uruguayan-bakery-sarasota">deeper →</a></h2>
      <ul class="mitems">
        <li><b>Alfajores de chocolate</b><span>Two soft cookies sandwiching dulce de leche, coated in chocolate — grandes y chicos, baked in-house.</span></li>
        <li><b>Rosca de chicharrones</b><span>Ring bread with chicharrones, recién horneada — posted ready at 9 a.m.</span></li>
        <li><b>Budines</b><span>Pound cakes including Cake d&rsquo;Oro — recent weekend deal: three for $12.</span></li>
        <li><b>Uruguayan breads</b><span>The breads Valeria told Business Debut she felt Sarasota had not seen.</span></li>
      </ul>
    </article>
    <article class="mcol">
      <h2>Grill days <a class="inlnk" href="/parrilla-sarasota">deeper →</a></h2>
      <ul class="mitems">
        <li><b>Chivito al pan</b><span>The Uruguayan everything-sandwich, built to order when the parrilla is lit.</span></li>
        <li><b>Lomito</b><span>Grilled beef on bread, recién hecho a la parrilla.</span></li>
        <li><b>Choripán</b><span>Chorizo grilled and sandwiched, the stall-side classic of both shores.</span></li>
        <li><b>Milanesa de carne</b><span>Breaded beef, made to order.</span></li>
      </ul>
    </article>
    <article class="mcol">
      <h2>Coffee &amp; the everyday</h2>
      <ul class="mitems">
        <li><b>Counter coffee</b><span>Order at the register, all day, seven days a week.</span></li>
        <li><b>Weekend deals</b><span>Como todos los fines de semana — offers posted every weekend.</span></li>
        <li><b>Holiday pre-orders</b><span>Thanksgiving orders ran to a posted cutoff — the café takes holiday pre-orders with the calendar.</span></li>
      </ul>
      <p class="note">Prices follow the posted counter board and the day&rsquo;s social posts — nothing here is invented.</p>
    </article>
  </div>
  <div class="wrap cta-band">
    <p>Want one of these waiting when you walk in? Call the counter.</p>
    <p class="cta-row"><a class="btn solid dark" href="{TEL_HREF}">Call {esc(TEL)}</a> <a class="btn line" href="/contact">Or send a note</a></p>
  </div>
</section>
''' + FOOTER

def page_bakery():
    ld = ld_graph([
        ld_service("Uruguayan bakery, pastries & breads", "/uruguayan-bakery-sarasota",
                   "Bakery", "Chocolate alfajores with dulce de leche, roscas de chicharrones, budines and Uruguayan breads baked in-house at Two Shores Café, Sarasota FL."),
        {"@type": "Bakery", "@id": ORIGIN + "/uruguayan-bakery-sarasota#bakery", "name": "Two Shores Café bakery counter",
         "url": ORIGIN + "/uruguayan-bakery-sarasota", "parentOrganization": {"@id": ORIGIN + "/#cafe"}},
        ld_webpage("Uruguayan Alfajores, Roscas & Breads — Two Shores Café, Sarasota FL", "/uruguayan-bakery-sarasota",
                   "In-house Uruguayan baking: alfajores de chocolate filled with dulce de leche, rosca de chicharrones ready around 9 a.m., budines and breads.",
                   entity=True, crumbs=True),
        ld_crumbs("/uruguayan-bakery-sarasota", [(SITE, "/"), ("Menu", "/menu"), ("Bakery", "/uruguayan-bakery-sarasota")]),
    ])
    return head("Uruguayan Alfajores, Roscas & Breads — Two Shores Café, Sarasota FL", "/uruguayan-bakery-sarasota",
                "The in-house bakery at Two Shores Café, Sarasota: alfajores de chocolate with dulce de leche, rosca de chicharrones baked mornings, budines and Uruguayan breads.", ld) + f'''
<section class="pagehead"><div class="wrap">
  <p class="eyebrow">Baked here, every day</p>
  <h1>The bakery — alfajores, roscas and breads</h1>
  <p class="lead">Valeria bakes. The press asked her what Sarasota was missing, and her answer was the pastry counter of her hometown — “delicious coffees” alongside it. Here is what that counter carries.</p>
</div></section>

<section class="detail">
  <div class="wrap dgrid">
    <article class="ditem">
      <h2>Alfajores de chocolate</h2>
      <p>“Grandes y chicos, hechos con mucho amor” — big ones and small, made with a lot of love, their own words. Two soft cookies sandwiching dulce de leche under a chocolate coat: the dessert counter of every Uruguayan panadería, at {esc(ADDR1)}.</p>
    </article>
    <article class="ditem">
      <h2>Rosca de chicharrones</h2>
      <p>A ring bread worked through with chicharrones, baked fresh — the shop posts it <em>listas a las 9:00 a.m.</em>, ready mid-morning. Come before it&rsquo;s gone.</p>
    </article>
    <article class="ditem">
      <h2>Budines</h2>
      <p>Pound cakes on the counter — Cake d&rsquo;Oro among them, the one the shop recently ran three-for-$12 as its weekend deal.</p>
    </article>
    <article class="ditem">
      <h2>Uruguayan breads</h2>
      <p>The breads to go with the coffee, baked in the shop — what Valeria told Business Debut she felt customers in Sarasota had not seen yet.</p>
    </article>
  </div>
  <div class="wrap cta-band">
    <p>The bakes rotate week to week — today&rsquo;s oven is announced on <a href="{IG}">Instagram</a> and <a href="{FB}">Facebook</a>.</p>
    <p class="cta-row"><a class="btn solid dark" href="{TEL_HREF}">Call {esc(TEL)}</a> <a class="btn line" href="/menu">See the whole counter</a></p>
  </div>
</section>
''' + FOOTER

def page_parrilla():
    ld = ld_graph([
        ld_service("Parrilla: chivito, lomito, choripán & milanesa", "/parrilla-sarasota",
                   "Restaurant counter service", "On grill days Two Shores Café grills chivito al pan, lomito, choripán and milanesa de carne to order at 7321 N Tamiami Trail, Sarasota FL."),
        ld_webpage("Parrilla: Lomito, Chivito & Choripán — Two Shores Café, Sarasota FL", "/parrilla-sarasota",
                   "Grill days at Two Shores Café: chivito al pan, lomito, choripán and milanesa de carne made to order — Uruguayan-Argentinian classics in Sarasota.",
                   entity=True, crumbs=True),
        ld_crumbs("/parrilla-sarasota", [(SITE, "/"), ("Menu", "/menu"), ("Parrilla", "/parrilla-sarasota")]),
    ])
    return head("Parrilla: Lomito, Chivito & Choripán — Two Shores Café, Sarasota FL", "/parrilla-sarasota",
                "Grill days at Two Shores Café in Sarasota: chivito al pan, lomito, choripán and milanesa de carne, made to order on the parrilla. Announced day-of on Instagram and Facebook.", ld) + f'''
<section class="pagehead"><div class="wrap">
  <p class="eyebrow">“Hoy prendemos la parrilla”</p>
  <h1>Grill days — lomito, chivito and choripán</h1>
  <p class="lead">On announced days the café fires the parrilla and builds the sandwiches of the Río de la Plata to order — the food both Uruguay and Argentina stand on, sandwiched and eaten standing up at the counter.</p>
</div></section>

<section class="detail">
  <div class="wrap dgrid">
    <article class="ditem">
      <h2>Chivito al pan</h2>
      <p>Uruguay&rsquo;s everything sandwich — steak and the works, in bread. The shop&rsquo;s posts call it by name; when the grill is lit, it&rsquo;s built to order.</p>
    </article>
    <article class="ditem">
      <h2>Lomito</h2>
      <p>The neighbor sandwich: tender beef lomito, grilled and sandwiched <em>recién hecho</em>. Posted the morning it happens.</p>
    </article>
    <article class="ditem">
      <h2>Choripán</h2>
      <p>Chorizo straight off the grill into bread — the stall classic of both shores of the river, chorizo included in the shop&rsquo;s grill-day posts.</p>
    </article>
    <article class="ditem">
      <h2>Milanesa de carne</h2>
      <p>Breaded beef, thin and fried, the lunch counter of Montevideo and Buenos Aires alike — on the grill-day card.</p>
    </article>
  </div>
  <div class="wrap cta-band">
    <p>The grill lights on posted days — watch <a href="{IG}">Instagram</a> or <a href="{FB}">Facebook</a> that morning, or call the counter.</p>
    <p class="cta-row"><a class="btn solid dark" href="{TEL_HREF}">Call {esc(TEL)}</a> <a class="btn line" href="/visit">Hours &amp; directions</a></p>
  </div>
</section>
''' + FOOTER

def page_visit():
    ld = ld_graph([
        ld_cafe(ORIGIN),
        ld_webpage("Hours & Directions — Two Shores Café, Sarasota FL", "/visit",
                   "Two Shores Café hours: Mon–Sat 7 a.m.–5 p.m., Sun 7–3. At 7321 N Tamiami Trail, Sarasota, FL 34243. Call (941) 298-9252.",
                   entity=True, crumbs=True),
        ld_crumbs("/visit", [(SITE, "/"), ("Visit", "/visit")]),
    ])
    return head("Hours & Directions — Two Shores Café, Sarasota FL", "/visit",
                "Open Mon–Sat 7 a.m.–5 p.m. and Sunday 7 a.m.–3 p.m. at 7321 N Tamiami Trail, Sarasota, FL 34243 — tap to call (941) 298-9252 or write from this page.", ld) + f'''
<section class="pagehead"><div class="wrap">
  <p class="eyebrow">Come by</p>
  <h1>Hours &amp; directions</h1>
  <p class="lead">Two Shores Café is on {esc(ADDR1)}, open seven days a week. Coffee and the pastry counter run all day; the grill&rsquo;s days are announced on social.</p>
</div></section>

<section class="visit">
  <div class="wrap vgrid">
    <div class="vinfo">
      <h2>Hours</h2>
      <ul class="hrs">
        <li><span>Monday</span><b>7 a.m. – 5 p.m.</b></li>
        <li><span>Tuesday</span><b>7 a.m. – 5 p.m.</b></li>
        <li><span>Wednesday</span><b>7 a.m. – 5 p.m.</b></li>
        <li><span>Thursday</span><b>7 a.m. – 5 p.m.</b></li>
        <li><span>Friday</span><b>7 a.m. – 5 p.m.</b></li>
        <li><span>Saturday</span><b>7 a.m. – 5 p.m.</b></li>
        <li><span>Sunday</span><b>7 a.m. – 3 p.m.</b></li>
      </ul>
      <p class="note">Holiday hours and closures are posted on <a href="{FB}">Facebook</a> and <a href="{IG}">Instagram</a> — Thanksgiving week ran early closes and holiday pre-orders, as usual.</p>
      <h2>Find the door</h2>
      <address class="big">{esc(ADDR_FULL)}<br><a href="{TEL_HREF}">{esc(TEL)}</a> · <a href="mailto:{EMAIL}">{EMAIL}</a></address>
      <p class="cta-row"><a class="btn solid dark" href="{TEL_HREF}">Tap to call</a> <a class="btn line" href="/contact">Contact form</a></p>
      <p>Sí, se puede pedir en español. The counter works in both languages, and events — like the tango afternoon Saturday, December 5 at 3 p.m. — are announced on the shop&rsquo;s social pages.</p>
    </div>
    {MAPBLOCK("m-visit", 460)}
  </div>
</section>
''' + FOOTER

def page_contact():
    ld = ld_graph([
        ld_cafe(ORIGIN),
        ld_webpage("Contact — Two Shores Café, Sarasota FL", "/contact",
                   "Contact Two Shores Café: call (941) 298-9252, write Info@twoshorescafe.com, or use the form — 7321 N Tamiami Trail, Sarasota, FL 34243.",
                   entity=True, crumbs=True),
        ld_crumbs("/contact", [(SITE, "/"), ("Contact", "/contact")]),
    ])
    return head("Contact — Two Shores Café, Sarasota FL", "/contact",
                "Call (941) 298-9252 or write Info@twoshorescafe.com — or send a note from this form and the counter will answer. 7321 N Tamiami Trail, Sarasota, FL 34243.", ld) + f'''
<section class="pagehead"><div class="wrap">
  <p class="eyebrow">Talk to the counter</p>
  <h1>Contact</h1>
  <p class="lead">Call, write, or use the form — questions, pre-orders, birthday budines and events all land the same place. The day&rsquo;s menu is on <a href="{IG}">Instagram</a> and <a href="{FB}">Facebook</a>.</p>
</div></section>

<section class="contact">
  <div class="wrap cgrid">
    <form class="cform" method="post" action="/contact">
      <div class="frow">
        <label for="f-name">Your name<input id="f-name" name="name" type="text" maxlength="120" required autocomplete="name"></label>
        <label for="f-phone">Phone (optional)<input id="f-phone" name="phone" type="tel" maxlength="40" autocomplete="tel"></label>
      </div>
      <label for="f-email">Email (optional)<input id="f-email" name="email" type="email" maxlength="160" autocomplete="email"></label>
      <label for="f-msg">Message<textarea id="f-msg" name="message" rows="5" maxlength="2000" required placeholder="What can we bake or grill for you?"></textarea></label>
      <p><button class="btn solid dark wide" type="submit">Send to the café</button></p>
      <p class="note">We answer from the same phone and email listed here. Se puede escribir en español.</p>
    </form>
    <aside class="cinfo">
      <address class="big">{SITE}<br>{esc(ADDR_FULL)}<br><a href="{TEL_HREF}">{esc(TEL)}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a></address>
      <ul class="hrs">
        <li><span>Mon – Sat</span><b>7 a.m. – 5 p.m.</b></li>
        <li><span>Sunday</span><b>7 a.m. – 3 p.m.</b></li>
      </ul>
      <p><a href="{FB}">Facebook</a> · <a href="{IG}">Instagram</a></p>
      {MAPBLOCK("m-contact", 300)}
    </aside>
  </div>
</section>
''' + FOOTER

def page_privacy():
    ld = ld_graph([
        ld_cafe(ORIGIN),
        ld_webpage("Privacy — Two Shores Café, Sarasota FL", "/privacy",
                   "How the Two Shores Cafe contact form works: no analytics, no trackers, no third-party scripts.",
                   entity=True, crumbs=True),
        ld_crumbs("/privacy", [(SITE, "/"), ("Privacy", "/privacy")]),
    ])
    return head("Privacy — Two Shores Café, Sarasota FL", "/privacy",
                "Two Shores Café's website: no analytics, no cookies of its own, no third-party scripts — the contact form just sends a message to the counter.", ld) + f'''
<section class="pagehead"><div class="wrap">
  <p class="eyebrow">Short and honest</p>
  <h1>Privacy</h1>
</div></section>

<section class="legal">
  <div class="wrap">
    <h2>What this site does</h2>
    <p>This is the café&rsquo;s own website: static pages, one contact form, and an embedded Google Map. It runs no analytics, no advertising trackers and no third-party scripts, and it sets no cookies of its own. The embedded map may set cookies under Google&rsquo;s own policy once you interact with it.</p>
    <h2>The contact form</h2>
    <p>What you type — name, phone, email, message — is delivered to {SITE}&rsquo;s inbox ({EMAIL}) for the sole purpose of answering you. It is not added to any list, sold, or shared. Ask and we&rsquo;ll confirm what we hold.</p>
    <h2>Questions</h2>
    <p>Call the café at {TEL}, or write {EMAIL} and the counter will answer.</p>
    <p class="note">Effective November 27, 2026. This page explains this website only; the café&rsquo;s in-shop practices are the counter&rsquo;s business.</p>
  </div>
</section>
''' + FOOTER

def page_404():
    return head("Page not found — Two Shores Café", "/404",
                "That page isn't here. Back to Two Shores Café's menu, hours, contact or home page.") + f'''
<section class="pagehead slim"><div class="wrap">
  <p class="eyebrow">404</p>
  <h1>That one&rsquo;s not on the counter.</h1>
  <p class="lead">The page you asked for isn&rsquo;t here. Start over from somewhere warm:</p>
  <p class="cta-row"><a class="btn solid dark" href="/menu">Menu</a> <a class="btn line" href="/visit">Hours</a> <a class="btn line" href="/contact">Contact</a></p>
</div></section>
''' + FOOTER

def page_thanks():
    return head("Message sent — Two Shores Café", "/thanks",
                "Thanks — your message is on its way to Two Shores Café's inbox. Need it faster? Call (941) 298-9252.") + f'''
<section class="pagehead slim"><div class="wrap">
  <p class="eyebrow">Sent</p>
  <h1>Mensaje enviado — thank you.</h1>
  <p class="lead">Your note is on its way to the café&rsquo;s inbox. Need an answer before we get to the counter? Call {TEL}.</p>
  <p class="cta-row"><a class="btn solid dark" href="{TEL_HREF}">Call {esc(TEL)}</a> <a class="btn line" href="/">Back to the shop</a></p>
</div></section>
''' + FOOTER

# ---------------- stylesheet ----------------
CSS = r'''/* Two Shores Café — petrol tide + cream paper + dulce amber. Hand-rolled, no frameworks. */
:root{
  --ink:#1b2a32; --petrol:#10404d; --tide:#0a2c37; --plata:#c9d7db; --sky:#e9f1f2;
  --cream:#faf4e6; --paper:#f2e8d4; --line:#dccfb4; --amber:#b4681b; --amber-hi:#d18a3a;
  --rose:#b65f6b; --serif:"Iowan Old Style","Palatino Linotype",Palatino,Georgia,"Times New Roman",serif;
  --sans:ui-sans-serif,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
}
*{box-sizing:border-box}
*{margin:0}
html{scroll-behavior:smooth}
body{font-family:var(--sans);color:var(--ink);background:var(--cream);line-height:1.55;font-size:17px}
h1,h2,h3,.brand,blockquote p{font-family:var(--serif);font-weight:700;line-height:1.12;letter-spacing:-.01em}
h1{font-size:clamp(2.1rem,5.2vw,3.4rem)}
h2{font-size:clamp(1.35rem,3vw,1.9rem)}
h3{font-size:1.15rem}
a{color:var(--amber)}
a:hover{color:var(--amber-hi)}
img{max-width:100%;height:auto}
.wrap{max-width:1080px;margin:0 auto;padding:0 24px}
.skip{position:absolute;left:-9999px}
.skip:focus{left:12px;top:12px;background:var(--amber);color:#fff;padding:8px 14px;border-radius:8px;z-index:9}
address{font-style:normal}

/* header */
header.site{position:sticky;top:0;z-index:8;display:flex;align-items:center;justify-content:space-between;gap:18px;flex-wrap:wrap;padding:14px 24px;background:var(--tide);border-bottom:1px solid rgba(201,215,219,.24)}
.brand{display:flex;align-items:center;gap:10px;color:var(--cream);text-decoration:none;font-size:1.18rem}
.brand em{font-style:normal;color:var(--amber-hi)}
.brand .mark{flex:0 0 auto}
nav{display:flex;align-items:center;gap:22px;flex-wrap:wrap}
nav a{color:var(--plata);text-decoration:none;font-weight:600;font-size:.95rem}
nav a:hover{color:#fff}
.btn{display:inline-block;border-radius:999px;padding:11px 22px;font-weight:700;font-size:.95rem;text-decoration:none;border:2px solid transparent;cursor:pointer}
.btn.solid{background:var(--amber);color:#fff}
.btn.solid:hover{background:var(--amber-hi);color:#fff}
.btn.solid.dark{background:var(--ink)}
.btn.solid.dark:hover{background:#2c4250;color:#fff}
.btn.ghost{border-color:var(--plata);color:var(--cream)}
.btn.ghost:hover{border-color:#fff;color:#fff}
.btn.line{border-color:var(--line);color:var(--ink)}
.btn.line:hover{border-color:var(--amber);color:var(--amber)}
.btn.call{background:var(--amber);color:#fff;padding:9px 18px}
.btn.wide{width:100%;text-align:center;font-family:var(--sans)}

/* hero */
.tide{position:relative;background:linear-gradient(180deg,var(--tide) 0%,var(--petrol) 78%,#17505f 100%);color:var(--cream);padding:74px 24px 128px}
.hero{max-width:880px;position:relative}
.eyebrow{font-family:var(--sans);text-transform:uppercase;letter-spacing:.16em;font-size:.78rem;font-weight:800;color:var(--amber-hi);margin-bottom:14px}
.tide h1{color:var(--cream);margin-bottom:18px}
.lead{font-size:1.13rem;max-width:34em;color:var(--plata)}
.tide .lead a{color:var(--amber-hi)}
.cta-row{display:flex;gap:14px;flex-wrap:wrap;margin-top:24px}
.openline{margin-top:26px;color:var(--plata);font-size:.95rem}
.seaway{position:absolute;left:0;right:0;bottom:-2px;width:100%;height:96px;display:block}

/* story */
.strip{background:var(--cream);padding:64px 24px 30px}
.quote-grid{display:grid;grid-template-columns:minmax(340px,1.15fr) minmax(340px,1fr);gap:48px;align-items:start}
blockquote{border-left:5px solid var(--amber);padding-left:24px}
blockquote p{font-size:clamp(1.3rem,2.6vw,1.7rem);font-family:var(--serif);line-height:1.35}
blockquote cite{display:block;margin-top:14px;font-style:normal;color:#6a5f4c;font-size:.95rem}
.story h2{margin-bottom:14px}
.story p+p{margin-top:14px}

/* cards */
.cards{background:var(--cream);padding:46px 24px 58px}
.sec{margin-bottom:26px}
.grid3{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:22px}
.card{background:#fffaf0;border:1px solid var(--line);border-radius:16px;padding:26px 24px;box-shadow:0 1px 0 rgba(27,42,50,.05)}
.card h3 a{color:var(--ink);text-decoration:none}
.card h3 a:hover{color:var(--amber)}
.card p{margin-top:10px;color:#3c4a52}
.card .more{margin-top:16px;font-weight:700}
.card .more a{text-decoration:none}

/* find-us */
.findus{background:var(--petrol);color:var(--sky);padding:64px 24px}
.findus h2{color:#fff;margin-bottom:16px}
.findus p{color:var(--plata)}
.find-grid{display:grid;grid-template-columns:minmax(320px,1fr) minmax(340px,1.15fr);gap:44px;align-items:center}
ul.hrs{list-style:none;padding:0;margin:0 0 20px;border-collapse:separate}
ul.hrs li{display:flex;justify-content:space-between;gap:22px;padding:10px 16px;border-bottom:1px solid rgba(201,215,219,.28)}
.findus ul.hrs li:first-child{border-top:1px solid rgba(201,215,219,.28)}
ul.hrs span{font-weight:600}
ul.hrs b{font-family:var(--serif);font-weight:700}
.mapcell{width:100%;min-width:0}
.mapcell iframe{display:block;width:100%;min-height:280px}

/* faq */
.faq{background:var(--cream);padding:56px 24px 72px}
.faq-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:20px}
.qa{background:#fffaf0;border:1px solid var(--line);border-radius:14px;padding:22px}
.qa h3{color:var(--petrol)}
.qa p{margin-top:10px;color:#3c4a52}

/* inner page heads */
.pagehead{background:linear-gradient(180deg,var(--tide),var(--petrol));color:var(--cream);padding:56px 24px 44px;border-bottom:4px solid var(--amber)}
.pagehead h1{color:var(--cream);margin-bottom:14px}
.pagehead .lead{color:var(--plata)}
.pagehead .lead a{color:var(--amber-hi)}
.pagehead.slim{padding:64px 24px 56px;text-align:center}
.pagehead.slim .cta-row{justify-content:center}

/* menu */
.menu{padding:52px 24px 30px;background:var(--cream)}
.mgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:26px}
.mcol{background:#fffaf0;border:1px solid var(--line);border-radius:18px;padding:26px 24px}
.mcol h2{font-size:1.35rem;border-bottom:2px solid var(--amber);padding-bottom:10px;margin-bottom:14px}
.inlnk{font-family:var(--sans);font-size:.8rem;font-weight:700;text-decoration:none}
ul.mitems{list-style:none;padding:0}
ul.mitems li{padding:12px 0;border-bottom:1px dashed var(--line)}
ul.mitems li:last-child{border-bottom:0}
ul.mitems b{font-family:var(--serif);font-size:1.06rem;display:block;color:var(--ink)}
ul.mitems span{display:block;color:#4a5760;margin-top:4px;font-size:.97rem}
.note{color:#6a5f4c;font-size:.9rem;margin-top:14px}
.cta-band{max-width:1080px;margin:34px auto 0;background:var(--paper);border:1px solid var(--line);border-radius:18px;padding:26px 28px;display:flex;justify-content:space-between;align-items:center;gap:20px;flex-wrap:wrap}
.cta-band p{margin:0;font-family:var(--serif);font-size:1.15rem}
.cta-band .cta-row{margin-top:0}
.menu .cta-band{margin-left:auto;margin-right:auto;padding-left:28px;padding-right:28px}

/* detail pages */
.detail{padding:52px 24px 30px;background:var(--cream)}
.dgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:26px}
.ditem{background:#fffaf0;border:1px solid var(--line);border-radius:18px;padding:26px 24px}
.ditem h2{font-size:1.3rem;border-bottom:2px solid var(--amber);padding-bottom:10px;margin-bottom:12px}
.ditem p+p{margin-top:12px}
.detail .cta-band{margin-left:auto;margin-right:auto}

/* visit */
.visit{padding:52px 24px 64px;background:var(--cream)}
.vgrid{display:grid;grid-template-columns:minmax(320px,1fr) minmax(340px,1.15fr);gap:44px;align-items:start}
.vinfo h2{margin:22px 0 12px}
.vinfo ul.hrs li{border-bottom:1px solid var(--line)}
.vinfo ul.hrs li:first-child{border-top:1px solid var(--line)}
.vinfo ul.hrs span{color:var(--ink)}
.vinfo ul.hrs b{color:var(--petrol)}
address.big{font-family:var(--serif);font-size:1.18rem;line-height:1.5;margin:10px 0 18px}

/* contact */
.contact{padding:52px 24px 64px;background:var(--cream)}
.cgrid{display:grid;grid-template-columns:minmax(320px,1.25fr) minmax(280px,.85fr);gap:44px;align-items:start}
.cform{background:#fffaf0;border:1px solid var(--line);border-radius:18px;padding:30px 28px}
.cform label{display:flex;flex-direction:column;gap:6px;font-weight:700;font-size:.95rem;margin-bottom:16px}
.frow{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.cform input,.cform textarea{font:inherit;font-weight:400;padding:11px 13px;border:1px solid var(--line);border-radius:10px;background:#fff;color:var(--ink);width:100%}
.cform input:focus,.cform textarea:focus{outline:2px solid var(--amber);border-color:var(--amber)}
.cinfo .hrs{margin-top:6px}
.cinfo ul.hrs li{border-bottom:1px solid var(--line)}
.cinfo ul.hrs li:first-child{border-top:1px solid var(--line)}
.cinfo .mapcell{margin-top:18px}

/* legal */
.legal{padding:48px 24px 64px;background:var(--cream)}
.legal h2{margin:24px 0 10px}
.legal p+p{margin-top:14px}
.legal .wrap{max-width:760px}

/* footer */
footer.site{background:var(--tide);color:var(--plata);padding:48px 24px 40px;border-top:4px solid var(--amber)}
.fwrap{max-width:1080px;margin:0 auto}
.fbrand{font-family:var(--serif);font-size:1.12rem;color:var(--cream);display:flex;align-items:center;gap:10px;flex-wrap:wrap}
.fnap{margin-top:14px}
.fhrs{margin-top:8px}
footer.site a{color:var(--amber-hi);text-decoration:none}
footer.site a:hover{color:#fff;text-decoration:underline}
.footline{margin-top:20px;font-size:.85rem;color:#8fa5ad}

@media (max-width:900px){
  .quote-grid,.find-grid,.vgrid,.cgrid{grid-template-columns:1fr}
  .tide{padding-bottom:110px}
}
@media (max-width:640px){
  header.site{padding:12px 16px}
  nav{gap:14px}
  .tide{padding:56px 16px 96px}
  .cta-band{flex-direction:column;align-items:flex-start}
  .frow{grid-template-columns:1fr}
  .mapcell iframe{min-height:260px}
}
'''

def main():
    os.makedirs(PUBLIC, exist_ok=True)
    pages = {
        "index.html": page_home(),
        "menu.html": page_menu(),
        "uruguayan-bakery-sarasota.html": page_bakery(),
        "parrilla-sarasota.html": page_parrilla(),
        "visit.html": page_visit(),
        "contact.html": page_contact(),
        "privacy.html": page_privacy(),
        "404.html": page_404(),
        "thanks.html": page_thanks(),
    }
    for name, doc in pages.items():
        with open(os.path.join(PUBLIC, name), "w", encoding="utf-8") as f:
            f.write(doc)
        print("wrote", name, len(doc.encode()), "bytes")
    with open(os.path.join(PUBLIC, "style.css"), "w", encoding="utf-8") as f:
        f.write(CSS)
    print("wrote style.css", len(CSS.encode()), "bytes")
    core = ["/", "/menu", "/uruguayan-bakery-sarasota", "/parrilla-sarasota", "/visit", "/contact", "/privacy"]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + \
         "".join(f"  <url><loc>{ORIGIN}{p}</loc><lastmod>2026-11-27</lastmod></url>\n" for p in core) + "</urlset>\n"
    open(os.path.join(PUBLIC, "sitemap.xml"), "w").write(sm)
    rb = f"""User-agent: *
Allow: /
Disallow: /thanks
Disallow: /open
Disallow: /healthz

Sitemap: {ORIGIN}/sitemap.xml
"""
    open(os.path.join(PUBLIC, "robots.txt"), "w").write(rb)
    fav = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="12" fill="#0a2c37"/><path d="M8 26c8-11 16-11 24 0s16 11 24 0" fill="none" stroke="#c9d7db" stroke-width="4.5" stroke-linecap="round"/><path d="M8 42c8-11 16-11 24 0s16 11 24 0" fill="none" stroke="#d18a3a" stroke-width="4.5" stroke-linecap="round"/></svg>\n'''
    open(os.path.join(PUBLIC, "favicon.svg"), "w").write(fav)
    print("wrote sitemap.xml, robots.txt, favicon.svg")

if __name__ == "__main__":
    main()
