"""Builds every HTML page of the site from shared components.

The HTML files in the repository root are the published site, so no build step is needed to deploy.
Edit content here and regenerate when you want every page to stay consistent:

    pip install pillow        # once; used to read image sizes
    python3 tools/build_pages.py

Anything edited directly in the HTML files is overwritten the next time this script runs.
"""
import datetime, glob, html, json, os, re
from urllib.parse import quote
from PIL import Image

# ---------------------------------------------------------------- site settings
# Change SITE_URL when the site moves to a custom domain, then rerun this script.
SITE_URL = 'https://website-swart-nu-54.vercel.app'
EMAIL = 'shadab18ali@gmail.com'
WHATSAPP_NUMBER = '919931394885'
WHATSAPP = f'https://wa.me/{WHATSAPP_NUMBER}'
WHATSAPP_LABEL = '+91 99313 94885'
LINKEDIN = 'https://linkedin.com/in/shadab-ali-7b0261238'
YEAR = datetime.date.today().year
BLANK_GIF = 'data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7'

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

# Genuine client testimonials only. While this list is empty no testimonial section is published.
# Example entry: {'quote': '…', 'name': 'Client name', 'role': 'Role, Company'}
TESTIMONIALS = []

# ---------------------------------------------------------------- images
def variants(name, ext='webp', required=True):
    out = []
    for f in glob.glob(f'assets/work/{name}-*.{ext}'):
        m = re.match(rf'assets/work/{re.escape(name)}-(\d+)\.{ext}$', f)
        if m:
            out.append((int(m.group(1)), f))
    assert out or not required, f'missing image: {name}'
    return sorted(out)

def size_of(name):
    return Image.open(variants(name)[-1][1]).size

def srcset(name, ext, r=''):
    return ', '.join(f'{r}{f} {w}w' for w, f in variants(name, ext))

def smallest(name, r=''):
    return r + variants(name)[0][1]

def pic(name, alt, sizes, loading='lazy', priority=None, r='', phone=None, phone_sizes='calc(100vw - 32px)', hide_below=None, show_below=None):
    """<img> with WebP srcset, wrapped in <picture> when AVIF, a phone crop or a breakpoint rule applies."""
    vs = variants(name)
    w, h = size_of(name)
    sources = []
    if hide_below:
        sources.append(f'<source media="(max-width: {hide_below}px)" srcset="{BLANK_GIF}">')
    if show_below:
        sources.append(f'<source media="(min-width: {show_below + 1}px)" srcset="{BLANK_GIF}">')
    if phone:
        pw, ph = size_of(phone)
        for ext in ('avif', 'webp'):
            if variants(phone, ext, required=False):
                sources.append(f'<source media="(max-width: 767px)" type="image/{ext}" srcset="{srcset(phone, ext, r)}" sizes="{phone_sizes}" width="{pw}" height="{ph}">')
    if variants(name, 'avif', required=False):
        sources.append(f'<source type="image/avif" srcset="{srcset(name, "avif", r)}" sizes="{sizes}">')
    attrs = [f'src="{r}{vs[-1][1]}"', f'srcset="{srcset(name, "webp", r)}"', f'sizes="{sizes}"', f'alt="{html.escape(alt)}"',
             f'width="{w}"', f'height="{h}"', f'loading="{loading}"', 'decoding="async"']
    if priority:
        attrs.append(f'fetchpriority="{priority}"')
    tag = '<img ' + ' '.join(attrs) + '>'
    return f'<picture>{"".join(sources)}{tag}</picture>' if sources else tag

def figure(name, alt, cls, sizes, caption=None):
    cap = f'<figcaption class="label muted">{caption}</figcaption>' if caption else ''
    return f'<figure class="{cls}"><div class="media" data-reveal="clip">{pic(name, alt, sizes)}</div>{cap}</figure>'

def lines(*parts):
    """Big display headings set line by line."""
    return ' '.join(f'<span class="line">{p}</span>' for p in parts)

ARROW_UP = '<span class="arrow arrow--up" aria-hidden="true">↗</span>'
ARROW = '<span class="arrow" aria-hidden="true">→</span>'
ARROW_DOWN = '<span class="arrow arrow--down" aria-hidden="true">↓</span>'
NEW_TAB = '<span class="visually-hidden"> (opens in a new tab)</span>'

# ---------------------------------------------------------------- projects (facts come from the original portfolio)
PROJECTS = [
  dict(slug='diviniti', file='case-diviniti.html', num='01', name='Diviniti', cat='Shopify Development', platform='Shopify',
       world='diviniti', tags=('Shopify', 'Ecommerce'),
       role='Shopify development', stack=['Shopify', 'Liquid', 'CSS', 'GTM', 'Clarity'],
       scope=['Liquid sections', 'Responsive images', 'Performance', 'Tracking & SEO'],
       live='https://www.diviniti.com', exhibit='diviniti-exhibit', phone='diviniti-phone', cover_alt='Diviniti Shopify storefront homepage',
       short='A luxury Shopify storefront for a 500+ product catalogue, rebuilt around faster image loading and easier merchandising.',
       intro='A luxury Shopify storefront with a catalogue of more than 500 products, rebuilt around faster image loading and easier day-to-day merchandising.',
       meta=[('Client', 'Diviniti'), ('Platform', 'Shopify'), ('Industry', 'Luxury ecommerce'),
             ('Role', 'Shopify development, Liquid customisation, responsive implementation, performance optimisation')],
       challenge=['Managing a large ecommerce catalogue while maintaining a clean browsing experience and improving storefront performance.',
                  'Images loaded slowly, merchandising changes were hard to make, and the team needed clearer insight into how customers used the site.'],
       solution=['I worked on the Shopify implementation, developed reusable Liquid sections, improved responsive behaviour and optimised performance areas, including image loading.'],
       implementation=['Responsive image sizes, lazy loading and separate image choices for mobile and desktop',
                       '20+ editable Liquid sections, so the team can edit and reorder page content in the Shopify editor',
                       'Google Tag Manager and Microsoft Clarity for tracking, plus structured on-page SEO across the catalogue'],
       facts=[('500+', 'Products in the catalogue'), ('20+', 'Editable Liquid sections'), ('40%', 'Reported improvement in Largest Contentful Paint')],
       results=[],
       gallery=[('full', 'diviniti-feature', 'Diviniti customisation and newest treasures sections on desktop', 'Desktop'),
                ('pair', 'diviniti-m-hero', 'Diviniti homepage on mobile', 'Mobile'),
                ('pair', 'diviniti-m-custom', 'Diviniti customisation section on mobile', 'Mobile'),
                ('full', 'diviniti-express', 'Diviniti "Express yourself" campaign section on desktop', 'Desktop'),
                ('large', 'diviniti-products', 'Diviniti "Our most admired creations" product grid on desktop', 'Desktop'),
                ('detail', 'diviniti-news', 'Diviniti news and events section on desktop', 'Detail')],
       note='Page layouts are built from editable Liquid sections, so content can be rearranged in the Shopify editor without code changes.'),
  dict(slug='portrait-on-gold', file='case-portrait-on-gold.html', num='02', name='Portrait on Gold', cat='Shopify / Ecommerce Development', platform='Shopify',
       world='pog', tags=('Shopify', 'Ecommerce'),
       role='Shopify development', stack=['Shopify', 'Liquid', 'JavaScript', 'WATI'],
       scope=['Product options', 'App-free filtering', 'WhatsApp order check'],
       live='https://www.portraitongold.com', exhibit='pog-exhibit', phone='pog-phone', cover_alt='Portrait on Gold Shopify storefront homepage',
       short='A made-to-order portrait store with custom product options, app-free filtering and a WhatsApp-first order check.',
       intro='A made-to-order portrait store on Shopify, with custom product options, app-free filtering and a WhatsApp-first order check.',
       meta=[('Client', 'Portrait on Gold'), ('Platform', 'Shopify'), ('Industry', 'Made-to-order portraits'),
             ('Role', 'Shopify development, Liquid, JavaScript, WATI integration')],
       challenge=['Customers needed to choose portrait options such as size, frame and finish.',
                  'The business also needed to confirm cash-on-delivery orders before producing a personalised portrait, and wanted collection filtering without relying on a paid filter app.'],
       solution=['I implemented the product options in Liquid, the collection filtering in JavaScript, and a WhatsApp-first order verification flow through WATI.'],
       implementation=['Custom product variant logic in Liquid for size, frame and finish',
                       'App-free collection filtering in JavaScript',
                       'WhatsApp-first order verification through WATI'],
       facts=[],
       results=['Orders are confirmed on WhatsApp before a personalised portrait goes into production.',
                'Collections can be filtered without a paid filter app.'],
       gallery=[('full', 'pog-feature', 'Portrait on Gold signature series on desktop', 'Desktop'),
                ('pair', 'pog-m-hero', 'Portrait on Gold homepage on mobile', 'Mobile'),
                ('pair', 'pog-m-opulent', 'Portrait on Gold "Opulent Charm" collection on mobile', 'Mobile'),
                ('full', 'pog-begin', 'Portrait on Gold "Begin your portrait" banner on desktop', 'Desktop'),
                ('large', 'seq-pog-chosen', 'Portrait on Gold "Chosen by the finest" section on desktop', 'Desktop'),
                ('detail', 'pog-m-alchemy', 'Portrait on Gold "Alchemy of a masterpiece" section on mobile', 'Detail')],
       note='Every order is confirmed on WhatsApp before a personalised portrait goes into production.'),
  dict(slug='majestic-india', file='case-majestic-india.html', num='03', name='The Majestic India', cat='WordPress Development', platform='WordPress',
       world='majestic', tags=('WordPress', 'Website'),
       role='WordPress development', stack=['WordPress', 'Elementor'],
       scope=['Four programme pages', 'Apply Now journey', 'Mobile-first build'],
       live='https://themajesticindia.com', exhibit='majestic-exhibit', phone='majestic-phone', cover_alt='The Majestic India WordPress website homepage',
       short='A mobile-first WordPress website with a page for each of its four programmes and a clear Apply Now journey.',
       intro='A mobile-first WordPress website with a dedicated page for each of its four programmes and a clear Apply Now journey.',
       meta=[('Client', 'The Majestic India'), ('Platform', 'WordPress (Elementor)'), ('Role', 'WordPress development, responsive build')],
       challenge=['Visitors needed a clear route to each programme and an easy way to apply, especially on mobile.'],
       solution=['I built a mobile-first WordPress site with Elementor, giving each programme its own page and connecting every page to the application journey.'],
       implementation=['Four dedicated programme pages',
                       'An Apply Now journey linked from every programme page',
                       'Mobile-first, responsive layouts'],
       facts=[],
       results=['Each of the four programmes has its own page, and every page leads to the same Apply Now journey.'],
       gallery=[('full', 'majestic-feature', 'The Majestic India "Choose the path where you become" section on desktop', 'Desktop'),
                ('pair', 'majestic-m-hero', 'The Majestic India homepage on mobile', 'Mobile'),
                ('pair', 'majestic-m-platforms', 'The Majestic India platforms list on mobile', 'Mobile'),
                ('full', 'majestic-founder', 'The Majestic India founder section on desktop', 'Desktop'),
                ('large', 'majestic-platforms', 'The Majestic India platforms and testimonials sections on desktop', 'Desktop'),
                ('detail', 'majestic-blog', 'The Majestic India blog section on desktop', 'Detail')],
       note='Each of the four programmes has its own page, and every page leads to the same Apply Now journey.'),
  dict(slug='uncostly', file='case-uncostly.html', num='04', name='Uncostly', cat='WooCommerce Development', platform='WooCommerce',
       world='uncostly', tags=('WooCommerce', 'Ecommerce'),
       role='WooCommerce development', stack=['WordPress', 'WooCommerce'],
       scope=['12+ categories', 'Product comparison', 'Wishlist & tracking', 'Rental flow'],
       live='https://uncostly.in', exhibit='uncostly-exhibit', phone='uncostly-phone', cover_alt='Uncostly WooCommerce catalogue homepage',
       short='A WooCommerce equipment catalogue across 12+ categories, with comparison, wishlist, order tracking and a rental flow.',
       intro='A WooCommerce equipment catalogue across 12+ categories, with product comparison, a wishlist, order tracking and a separate rental flow.',
       meta=[('Client', 'Uncostly'), ('Platform', 'WooCommerce (WordPress)'), ('Industry', 'Equipment sales and rental'), ('Role', 'WooCommerce development')],
       challenge=['A large equipment catalogue needed to help visitors compare products and choose between buying and renting.'],
       solution=['I built the catalogue and its shopping tools in WooCommerce, with renting handled as its own flow alongside purchasing.'],
       implementation=['A catalogue structure across 12+ categories',
                       'Product comparison',
                       'Wishlist and order tracking',
                       'A separate equipment rental flow'],
       facts=[],
       results=['Visitors can compare equipment and choose to buy or rent from the same catalogue.'],
       gallery=[('full', 'uncostly-feature', 'Uncostly "Smart security kit" and trending items sections on desktop', 'Desktop'),
                ('pair', 'uncostly-m-hero', 'Uncostly homepage on mobile', 'Mobile'),
                ('pair', 'uncostly-m-categories', 'Uncostly product categories on mobile', 'Mobile'),
                ('full', 'uncostly-tiles', 'Uncostly featured product tiles on desktop', 'Desktop'),
                ('large', 'uncostly-reviews', 'Uncostly reviews and articles sections on desktop', 'Desktop'),
                ('detail', 'uncostly-m-product', 'Uncostly trending product card on mobile', 'Detail')],
       note='Buying and renting sit in the same catalogue, with a separate rental flow for equipment.'),
]

SERVICES = [
  ('shopify', '01', 'Shopify development', 'Online stores built and customised on Shopify, from a new launch to improvements on an existing store.',
   ['Shopify store development', 'Shopify 2.0 sections', 'Liquid development', 'Theme customisation', 'Custom product functionality', 'App integrations', 'Performance optimisation', 'Existing store improvements'], 'Shopify'),
  ('wordpress', '02', 'WordPress &amp; WooCommerce', 'Business websites and WooCommerce stores with content your team can manage.',
   ['Business websites', 'WooCommerce stores', 'Landing pages', 'Theme customisation', 'Responsive development', 'Performance optimisation', 'Maintenance'], 'WordPress / WooCommerce'),
  ('custom', '03', 'Custom web development', 'Focused websites and features built to your brief, when a ready-made theme is not the right fit.',
   ['Front-end development', 'Responsive websites', 'Landing pages', 'Interactive experiences', 'Custom functionality'], 'Custom Development'),
  ('redesign', '04', 'Website redesign', 'Already have a website? I can improve its design, mobile experience, speed and structure without rebuilding everything.',
   ['UX improvements', 'Visual redesign', 'Mobile optimisation', 'Performance improvements', 'Existing website upgrades'], 'Website Redesign'),
]
# Homepage "What I build" rows: title, one line, link, preview image from a project that used it.
CAPABILITIES = [
  ('Shopify development', 'Custom themes, Liquid sections, store builds', 'services.html#shopify', 'diviniti-exhibit'),
  ('WordPress development', 'Business websites your team can manage', 'services.html#wordpress', 'majestic-exhibit'),
  ('WooCommerce', 'Catalogues, comparison, wishlists, rentals', 'services.html#wordpress', 'uncostly-exhibit'),
  ('Custom development', 'JavaScript features and custom front-end', 'services.html#custom', 'pog-exhibit'),
  ('Performance', 'Faster pages and lighter images', 'services.html#redesign', 'diviniti-poster'),
]
SKILLS = ['Shopify', 'Liquid', 'WordPress', 'WooCommerce', 'Custom front-end']
WHY = [
  ('Business-first thinking', 'I start by understanding how the business works, then build the website around its real needs.'),
  ('Clean implementation', 'Practical solutions over unnecessary complexity — code your team can keep working with.'),
  ('Performance conscious', 'Image loading, responsive assets and page speed are part of the build, not an afterthought.'),
  ('Clear communication', 'You work directly with me, from the first conversation through development, testing and launch.'),
]
PROCESS = [
  ('01', 'Discover', 'Understand goals, users and requirements.'),
  ('02', 'Plan', 'Define architecture, content and technical direction.'),
  ('03', 'Build', 'Develop the experience cleanly and responsively.'),
  ('04', 'Refine', 'Test performance, responsiveness and usability.'),
  ('05', 'Launch', 'Deploy and hand over the finished product.'),
]
PROJECT_TYPES = ['Shopify', 'WordPress / WooCommerce', 'Website Redesign', 'Custom Development', 'Other']
BUDGETS = ['Under ₹25,000', '₹25,000–₹50,000', '₹50,000–₹1,00,000', '₹1,00,000+', 'Not sure yet']
TIMELINES = ['ASAP', '2–4 weeks', '1–2 months', 'Flexible']

# Email template for "Send project details" (no form or server needed).
BRIEF_SUBJECT = 'Project enquiry'
BRIEF_BODY = ('Hi Shadab,\n\nI’d like to discuss a website project.\n\n'
              'Name:\nCompany / brand:\n'
              f'Project type ({" / ".join(PROJECT_TYPES)}):\n'
              'Current website (if any):\n'
              f'Budget ({" / ".join(BUDGETS)}):\n'
              f'Timeline ({" / ".join(TIMELINES)}):\n\n'
              'Project details:\n\n')
BRIEF_MAILTO = f'mailto:{EMAIL}?subject={quote(BRIEF_SUBJECT)}&body={quote(BRIEF_BODY)}'
WHATSAPP_HELLO = f'{WHATSAPP}?text={quote("Hi Shadab, I’d like to discuss a website project.")}'

# ---------------------------------------------------------------- shared components
def head(title, desc, path, schema=None, noindex=False, r=''):
    url = SITE_URL + '/' + ('' if path == 'index.html' else path)
    image = f'{SITE_URL}/assets/og-image.jpg'
    tags = [f'<title>{title}</title>', f'<meta name="description" content="{desc}">']
    if noindex:
        tags.append('<meta name="robots" content="noindex">')
    else:
        tags.append(f'<link rel="canonical" href="{url}">')
    tags += [f'<link rel="icon" href="{r}assets/favicon.svg" type="image/svg+xml">',
             f'<link rel="apple-touch-icon" href="{r}assets/apple-touch-icon.png">',
             '<meta property="og:type" content="website">',
             '<meta property="og:site_name" content="Shadab Ali">',
             '<meta property="og:locale" content="en_GB">',
             f'<meta property="og:title" content="{title}">',
             f'<meta property="og:description" content="{desc}">',
             f'<meta property="og:url" content="{url}">',
             f'<meta property="og:image" content="{image}">',
             '<meta property="og:image:width" content="1200">',
             '<meta property="og:image:height" content="630">',
             '<meta property="og:image:alt" content="Shadab Ali — Shopify &amp; WordPress developer, with project work">',
             '<meta name="twitter:card" content="summary_large_image">',
             f'<meta name="twitter:title" content="{title}">',
             f'<meta name="twitter:description" content="{desc}">',
             f'<meta name="twitter:image" content="{image}">',
             f'<link rel="preload" href="{r}assets/fonts/inter-tight-latin.woff2" as="font" type="font/woff2" crossorigin>',
             f'<link rel="stylesheet" href="{r}site.css">',
             "<script>document.documentElement.classList.add('js');setTimeout(function(){if(!window.__site)document.documentElement.classList.remove('js')},4000)</script>",
             f'<script src="{r}site.js" defer></script>']
    if schema:
        tags.append('<script type="application/ld+json">' + json.dumps(schema, ensure_ascii=False) + '</script>')
    body = '\n  '.join(tags)
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#f5f2ec">
  {body}
</head>'''

NAV = [('work.html', 'Work'), ('about.html', 'About'), ('services.html', 'Services'), ('contact.html', 'Contact')]

def header(current=None, r=''):
    cur = ' aria-current="page"'
    links = ''.join(f'<li{" class=nav-contact" if h == "contact.html" else ""}><a href="{r}{h}"{cur if h == current else ""}>{t}</a></li>' for h, t in NAV)
    return f'''  <a class="skip-link" href="#main">Skip to content</a>
  <header class="site-header" id="top" data-header>
    <div class="wrap header-inner">
      <a class="brand" href="{r}index.html" aria-label="Shadab Ali, home">Shadab Ali</a>
      <nav class="nav" id="site-nav" aria-label="Main">
        <ul class="nav-list">{links}</ul>
        <a class="nav-cta" href="{r}contact.html">Let’s talk {ARROW_UP}</a>
        <p class="nav-extra"><a href="mailto:{EMAIL}">{EMAIL}</a><a href="{WHATSAPP}" target="_blank" rel="noopener noreferrer">WhatsApp {WHATSAPP_LABEL}</a></p>
      </nav>
      <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="site-nav" data-menu-toggle>Menu</button>
    </div>
  </header>'''

def final_cta(r=''):
    """The dark closing section used at the end of every page except Contact."""
    return f'''    <section class="final theme-dark" aria-labelledby="final-title">
      <div class="wrap final-grid">
        <h2 class="final-title" id="final-title"><span class="line split" data-reveal>Let’s</span> <span class="line split" data-reveal>make</span> <span class="line split" data-reveal>something</span> <span class="line split" data-reveal>good.</span></h2>
        <div class="final-side" data-reveal>
          <p class="final-kicker">Have a project in mind?</p>
          <a class="button button--light" href="{r}contact.html">Start a project {ARROW_UP}</a>
          <p class="final-direct">or <a href="mailto:{EMAIL}">{EMAIL}</a></p>
        </div>
      </div>
    </section>'''

def footer(r=''):
    return f'''  <footer class="site-footer theme-dark">
    <div class="wrap">
      <div class="footer-grid">
        <div class="footer-id"><p class="footer-brand">Shadab Ali</p><p class="muted">Shopify &amp; WordPress Developer</p></div>
        <nav class="footer-links" aria-label="Footer"><a href="{r}work.html">Work</a><a href="{r}services.html">Services</a><a href="{r}about.html">About</a><a href="{r}contact.html">Contact</a></nav>
        <div class="footer-links"><a href="{LINKEDIN}" target="_blank" rel="noopener noreferrer">LinkedIn{NEW_TAB}</a><a href="{WHATSAPP}" target="_blank" rel="noopener noreferrer">WhatsApp<span class="visually-hidden"> (opens WhatsApp)</span></a><a href="mailto:{EMAIL}">Email</a></div>
        <div class="footer-end"><p class="muted">© <span data-year>{YEAR}</span> Shadab Ali</p><a class="footer-top" href="#top">Back to top <span aria-hidden="true">↑</span></a></div>
      </div>
      <div class="footer-mark-wrap" aria-hidden="true"><p class="footer-mark">Shadab Ali</p></div>
    </div>
  </footer>'''

def page(head_html, body_class, current, main, r=''):
    return f'''{head_html}
<body class="{body_class}">
{header(current, r)}

  <main id="main">
{main}
  </main>

{footer(r)}
</body>
</html>
'''

def testimonials():
    """Reusable testimonial section; renders nothing until TESTIMONIALS has real entries."""
    if not TESTIMONIALS:
        return ''
    items = ''.join(f'<figure class="testimonial" data-reveal><blockquote><p>{html.escape(t["quote"])}</p></blockquote>'
                    f'<figcaption><span class="label">{html.escape(t["name"])}</span><span class="muted">{html.escape(t["role"])}</span></figcaption></figure>'
                    for t in TESTIMONIALS)
    return f'''
    <section class="section testimonials" aria-labelledby="testimonials-title">
      <div class="wrap">
        <h2 class="h3" id="testimonials-title">Client words</h2>
        <div class="testimonial-list">{items}</div>
      </div>
    </section>
'''

# ---------------------------------------------------------------- structured data
PERSON = {'@type': 'Person', '@id': f'{SITE_URL}/#person', 'name': 'Shadab Ali', 'jobTitle': 'Freelance Shopify & WordPress Developer',
          'url': f'{SITE_URL}/', 'image': f'{SITE_URL}/assets/profile.webp', 'email': f'mailto:{EMAIL}',
          'address': {'@type': 'PostalAddress', 'addressLocality': 'Delhi', 'addressCountry': 'IN'},
          'sameAs': [LINKEDIN], 'knowsAbout': ['Shopify', 'Liquid', 'WordPress', 'WooCommerce', 'JavaScript', 'Front-end development', 'Web performance']}
BUSINESS = {'@type': 'ProfessionalService', '@id': f'{SITE_URL}/#service', 'name': 'Shadab Ali — Shopify & WordPress Development',
            'url': f'{SITE_URL}/', 'image': f'{SITE_URL}/assets/og-image.jpg', 'email': f'mailto:{EMAIL}',
            'founder': {'@id': f'{SITE_URL}/#person'}, 'areaServed': 'Worldwide',
            'address': {'@type': 'PostalAddress', 'addressLocality': 'Delhi', 'addressCountry': 'IN'},
            'knowsAbout': ['Shopify development', 'WordPress development', 'WooCommerce development', 'Custom web development', 'Website redesign']}
WEBSITE = {'@type': 'WebSite', '@id': f'{SITE_URL}/#website', 'url': f'{SITE_URL}/', 'name': 'Shadab Ali',
           'description': 'Portfolio of Shadab Ali, freelance Shopify and WordPress developer.', 'inLanguage': 'en', 'publisher': {'@id': f'{SITE_URL}/#person'}}

# ---------------------------------------------------------------- project worlds (home + work page)
DESKTOP_SIZES = '(max-width: 767px) calc(100vw - 32px), 96vw'

def world_media(p, cls, sizes, name=None, phone=True, reveal=True, zoom=False):
    """A linked project image; phones get the site's own mobile screenshot."""
    img = pic(name or p['exhibit'], p['cover_alt'], sizes, phone=p['phone'] if phone else None)
    inner = f'<span class="zoom">{img}</span>' if zoom else img
    rv = ' data-reveal="clip"' if reveal else ''
    return (f'<a class="{cls}" href="{p["file"]}" data-open-project data-cursor="view" tabindex="-1" aria-hidden="true">'
            f'<span class="media"{rv}>{inner}</span></a>')

def world_phone(p, cls):
    return (f'<a class="{cls}" href="{p["file"]}" data-open-project data-cursor="view" tabindex="-1" aria-hidden="true">'
            f'<span class="media" data-reveal="clip">{pic(p["phone"], p["name"] + " on mobile", "(max-width: 767px) 1px, 22vw", hide_below=767)}</span></a>')

def world(p, title_tag):
    s = p['slug']
    tags = ' / '.join(p['tags'])
    meta = (f'<dl class="world-meta"><div><dt class="label">Role</dt><dd>{p["role"]}</dd></div>'
            f'<div><dt class="label">Stack</dt><dd>{" · ".join(p["stack"])}</dd></div>'
            f'<div><dt class="label">Scope</dt><dd>{" · ".join(p["scope"])}</dd></div></dl>')
    links = (f'<p class="world-links"><a class="button" href="{p["file"]}" data-open-project data-case-link>View case study<span class="visually-hidden">: {p["name"]}</span> {ARROW_UP}</a>'
             f'<a class="link" href="{p["live"]}" target="_blank" rel="noopener noreferrer">Live site<span class="visually-hidden">: {p["name"]}</span> {ARROW_UP}{NEW_TAB}</a></p>')
    title = f'<{title_tag} class="world-title split" id="p-{s}" data-reveal>{p["name"]}</{title_tag}>'
    cat = f'<p class="label world-cat"><span class="world-num">{p["num"]}</span> {tags}</p>'
    desc = f'<p class="world-desc">{p["short"]}</p>'
    w = p['world']
    if w == 'diviniti':
        body = f'''<div class="wrap world-head">{cat}{title}{desc}</div>
          <div class="world-stage">{world_media(p, "world-media", DESKTOP_SIZES, zoom=True)}</div>
          <div class="wrap world-foot">{meta}{links}</div>'''
    elif w == 'pog':
        body = f'''<div class="wrap world-grid">
            <div class="world-head">{cat}{title}</div>
            {world_media(p, "world-media", "(max-width: 767px) calc(100vw - 32px), 70vw")}
            {world_phone(p, "world-phone")}
            <div class="world-foot">{desc}{meta}{links}</div>
          </div>'''
    elif w == 'majestic':
        body = f'''<div class="wrap world-grid">
            {title}
            <div class="world-top">{cat}{desc}</div>
            {world_media(p, "world-media", "(max-width: 767px) calc(100vw - 32px), 76vw")}
            <div class="world-foot">{meta}{links}</div>
          </div>'''
    else:  # uncostly
        body = f'''<div class="wrap world-head">{cat}{title}</div>
          <div class="wrap"><div class="world-panel">
            {world_phone(p, "world-phone")}
            {world_media(p, "world-media", "(max-width: 767px) calc(100vw - 32px), 64vw")}
          </div></div>
          <div class="wrap world-foot">{desc}{meta}{links}</div>'''
    return f'''      <article class="world world--{w}" id="project-{s}" aria-labelledby="p-{s}">
          {body}
      </article>'''

def worlds(title_tag):
    return '\n'.join(world(p, title_tag) for p in PROJECTS)

def proof():
    items = [('500+', 'Products', 'in the catalogue'), ('20+', 'Custom sections', 'built in Liquid'), ('40%', 'LCP improvement', 'as reported')]
    lis = ''.join(f'<li><strong class="proof-num">{n}</strong><span class="proof-label">{l}<span class="muted"> {c}</span></span></li>' for n, l, c in items)
    return f'''    <section class="proof" aria-labelledby="proof-title">
      <div class="wrap proof-inner" data-reveal>
        <h2 class="proof-title" id="proof-title"><span class="label">Proof</span>Diviniti, Shopify</h2>
        <ul class="proof-list">{lis}</ul>
      </div>
    </section>'''

def process(title_tag='h2', item_tag='h3'):
    steps = ''.join(f'<li class="flow-step{" is-active" if i == 0 else ""}"><span class="label flow-num">{n}</span><{item_tag} class="flow-name">{t}</{item_tag}><p class="flow-text">{d}</p></li>'
                    for i, (n, t, d) in enumerate(PROCESS))
    return f'''    <section class="process" aria-labelledby="process-title">
      <div class="wrap">
        <div class="process-head"><{title_tag} class="h3" id="process-title">From idea to launch</{title_tag}><p class="muted">Five steps, one person, from first call to launch.</p></div>
        <ol class="flow" data-flow tabindex="0" aria-label="Process: discover, plan, build, refine, launch">{steps}</ol>
      </div>
    </section>'''

# ---------------------------------------------------------------- project detail
GALLERY_SIZES = {'full': '(max-width: 767px) 100vw, 94vw', 'pair': '(max-width: 767px) 100vw, 46vw', 'large': '(max-width: 767px) 100vw, 80vw', 'detail': '(max-width: 767px) 100vw, 40vw'}

def case_article(p, idx):
    nxt = PROJECTS[(idx + 1) % len(PROJECTS)]
    meta = ''.join(f'<div class="meta-{k.lower()}"><dt class="label">{k}</dt><dd>{v}</dd></div>' for k, v in p['meta'])
    paras = lambda items: ''.join(f'<p>{t}</p>' for t in items)
    impl = '<ul class="case-list">' + ''.join(f'<li>{t}</li>' for t in p['implementation']) + '</ul>'
    if p['facts']:
        results = '<ul class="case-facts">' + ''.join(f'<li class="case-fact"><strong>{n}</strong><span>{t}</span></li>' for n, t in p['facts']) + '</ul>'
    else:
        results = paras(p['results'])
    gallery, pair_i = [], 0
    for kind, name, alt, caption in p['gallery']:
        if kind == 'pair':
            cls = 'g-pair-a' if pair_i == 0 else 'g-pair-b'
            pair_i += 1
        elif kind == 'detail':
            gallery.append(f'<p class="g-detail-copy" data-reveal>{p["note"]}</p>')
            cls = 'g-detail'
        else:
            cls = f'g-{kind}'
        gallery.append(figure(name, alt, cls, GALLERY_SIZES[kind], caption))
    gallery_html = '\n            '.join(gallery)
    tags = ' / '.join(p['tags'])
    return f'''    <article class="case" data-case aria-labelledby="case-title">
      <div class="case-bar"><div class="wrap case-bar-inner"><a class="case-close" href="work.html" data-case-close><span class="x" aria-hidden="true"></span>Close</a><span class="label muted">{p['num']} / 0{len(PROJECTS)}</span></div></div>
      <header class="case-top world--{p['world']}">
        <div class="wrap case-head">
          <p class="label world-cat"><span class="world-num">{p['num']}</span> {tags}</p>
          <h1 class="case-title split" id="case-title" data-reveal>{p['name']}</h1>
          <div class="case-intro" data-reveal><p>{p['intro']}</p><a class="link" href="{p['live']}" target="_blank" rel="noopener noreferrer">Live site {ARROW_UP}{NEW_TAB}</a></div>
        </div>
        <figure class="case-hero"><span class="media">{pic(p['exhibit'], p['cover_alt'], DESKTOP_SIZES, loading='eager', priority='high', phone=p['phone'])}</span></figure>
        <div class="wrap"><dl class="case-meta" data-reveal>{meta}</dl></div>
      </header>
      <div class="wrap">
        <section class="case-details" aria-labelledby="details-{p['slug']}">
          <h2 class="h3" id="details-{p['slug']}">Details</h2>
          <div class="case-cols">
            <div class="case-col" data-reveal><h3 class="label">Challenge</h3>{paras(p['challenge'])}</div>
            <div class="case-col" data-reveal><h3 class="label">Solution</h3>{paras(p['solution'])}</div>
            <div class="case-col" data-reveal><h3 class="label">Implementation</h3>{impl}</div>
            <div class="case-col case-results" data-reveal><h3 class="label">Results</h3>{results}</div>
          </div>
        </section>
        <section class="case-gallery" aria-labelledby="gallery-{p['slug']}">
          <h2 class="h3" id="gallery-{p['slug']}">Image gallery</h2>
          <div class="gallery">
            {gallery_html}
          </div>
        </section>
        <nav class="case-next" aria-label="Next project"><span class="label muted">Next project</span><a href="{nxt['file']}" data-open-project>{nxt['name']} {ARROW}</a></nav>
      </div>
    </article>'''

def case_page(p, idx):
    desc = html.escape(p['intro'], quote=True)
    return page(head(f"{p['name']} — {p['cat']} Case Study | Shadab Ali", desc, p['file']), 'page-case', 'work.html', case_article(p, idx) + '\n\n' + final_cta())

# ---------------------------------------------------------------- homepage
def collage():
    by = {p['world']: p for p in PROJECTS}
    def piece(p, cls, name, alt, sizes, depth, priority=None, mobile=None, hide=True):
        img = pic(name, alt, sizes, loading='eager', priority=priority, hide_below=767 if hide else None,
                  phone=mobile, phone_sizes='calc(100vw - 32px)')
        return (f'<a class="piece {cls}" href="{p["file"]}" data-open-project data-cursor="view" tabindex="-1" aria-hidden="true" style="--d:{depth}">'
                f'<span class="piece-media">{img}</span><span class="piece-cap label">{p["name"]}</span></a>')
    return f'''<div class="collage" data-collage aria-hidden="true">
          {piece(by['majestic'], 'piece--majestic', 'majestic-tile', '', '(max-width: 767px) 1px, 14vw', 4)}
          {piece(by['diviniti'], 'piece--diviniti', 'diviniti-exhibit', '', '(max-width: 1023px) 70vw, 40vw', 7, priority='high', mobile='diviniti-poster', hide=False)}
          {piece(by['pog'], 'piece--pog', 'pog-phone', '', '(max-width: 767px) 1px, 15vw', 11)}
          {piece(by['uncostly'], 'piece--uncostly', 'uncostly-banner', '', '(max-width: 767px) 1px, 22vw', 9)}
        </div>'''

def home():
    hero = f'''    <section class="hero" aria-labelledby="hero-title">
      <div class="wrap hero-grid">
        <p class="label hero-kicker">Shopify / WordPress Developer</p>
        <h1 class="hero-title" id="hero-title"><span class="hero-line"><span>Shadab</span></span> <span class="hero-line"><span>Ali</span></span></h1>
        <p class="hero-lede">I build digital experiences for brands that want to move forward.</p>
        <div class="hero-actions"><a class="button" href="#work">View work {ARROW_DOWN}</a><a class="button button--ghost" href="contact.html">Let’s talk {ARROW_UP}</a></div>
        {collage()}
      </div>
    </section>'''
    caps = ''.join(f'<li><a class="svc" href="{h}" data-preview="{smallest(img) if img == "diviniti-poster" else variants(img)[0][1]}"><span class="svc-title">{t}</span><span class="svc-desc">{d}</span><span class="svc-arrow" aria-hidden="true">↗</span></a></li>'
                   for t, d, h, img in CAPABILITIES)
    skills = ''.join(f'<li>{s}</li>' for s in SKILLS)
    main = f'''{hero}

    <section class="intro" aria-labelledby="intro-title">
      <div class="wrap intro-grid">
        <h2 class="intro-title split" id="intro-title" data-reveal>I build digital experiences where design meets code.</h2>
        <div class="intro-body" data-reveal>
          <p>Freelance web developer in Delhi, India, building Shopify stores, WordPress websites and custom front-ends for businesses in India and around the world.</p>
          <ul class="platforms"><li>Shopify</li><li>WordPress</li><li>WooCommerce</li><li>Custom development</li></ul>
        </div>
      </div>
    </section>

    <section class="work" id="work" aria-labelledby="work-title">
      <div class="wrap work-head">
        <h2 class="h2 split" id="work-title" data-reveal>Selected work</h2>
        <p class="work-lede" data-reveal>Four client websites across Shopify, WordPress and WooCommerce — each in its own world.</p>
      </div>
{worlds('h3')}
    </section>

{proof()}

    <section class="services" aria-labelledby="services-title">
      <div class="wrap">
        <div class="services-head"><h2 class="h2 split" id="services-title" data-reveal>What I build</h2><a class="link" href="services.html">All services {ARROW}</a></div>
        <ul class="svc-list" data-svc-list>{caps}</ul>
      </div>
      <div class="svc-preview" aria-hidden="true" data-svc-preview><img alt="" width="960" height="600"></div>
    </section>
{testimonials()}
    <section class="about-band" aria-labelledby="about-title">
      <div class="wrap about-grid">
        <figure class="about-figure">
          <span class="monogram" aria-hidden="true"></span>
          <span class="about-portrait">{pic('profile', 'Portrait of Shadab Ali', '(max-width: 767px) 80vw, 36vw')}</span>
        </figure>
        <div class="about-copy">
          <h2 class="h2 split" id="about-title" data-reveal><span class="line">One developer.</span> <span class="line">Fully invested.</span></h2>
          <div class="about-text" data-reveal>
            <p class="lead">I first understand how a business works, then build the website around its real needs.</p>
            <p>I prefer practical solutions over unnecessary complexity. Clients work directly with me — from the first discussion through development, testing and launch.</p>
            <ul class="skills" aria-label="Skills">{skills}</ul>
            <a class="link" href="about.html">More about me {ARROW}</a>
          </div>
        </div>
      </div>
    </section>

{process()}

{final_cta()}'''
    schema = {'@context': 'https://schema.org', '@graph': [WEBSITE, PERSON, BUSINESS]}
    return page(head('Shadab Ali — Shopify &amp; WordPress Developer',
                     'Shadab Ali is a freelance Shopify and WordPress developer creating high-performance ecommerce websites and digital experiences for brands.',
                     'index.html', schema), 'page-home', None, main)

# ---------------------------------------------------------------- inner pages
def page_hero(label_text, title_html, lede=None, cls=''):
    lede_html = f'<p class="page-lede" data-reveal>{lede}</p>' if lede else ''
    return f'''    <section class="page-hero{(" " + cls) if cls else ""}" aria-labelledby="page-title">
      <div class="wrap page-hero-grid">
        <p class="label page-kicker">{label_text}</p>
        <h1 class="page-title split" id="page-title" data-reveal>{title_html}</h1>
        {lede_html}
      </div>
    </section>'''

def projects_page():
    main = f'''{page_hero('Work', 'Selected work', 'Four client websites across Shopify, WordPress and WooCommerce. Open a project for the challenge, the build and the live site.')}

    <section class="work work--page" aria-label="Projects">
{worlds('h2')}
    </section>

{proof()}

{final_cta()}'''
    return page(head('Selected Work — Shopify, WordPress &amp; WooCommerce Projects | Shadab Ali',
                     'Selected Shopify, WordPress and WooCommerce projects by freelance developer Shadab Ali: Diviniti, Portrait on Gold, The Majestic India and Uncostly.', 'work.html'),
                'page-projects', 'work.html', main)

def services_page():
    rows = []
    for sid, num, title, desc, scope, ptype in SERVICES:
        items = ''.join(f'<li>{x}</li>' for x in scope)
        rows.append(f'''        <article class="service" id="{sid}" aria-labelledby="{sid}-title">
          <span class="label service-num">{num}</span>
          <div class="service-body"><h2 class="service-title split" id="{sid}-title" data-reveal>{title}</h2><p>{desc}</p><a class="link" href="contact.html?service={quote(ptype)}" data-service="{ptype}">Start a project {ARROW}</a></div>
          <ul class="service-scope" aria-label="What’s included">{items}</ul>
        </article>''')
    rows_html = '\n'.join(rows)
    schema = {'@context': 'https://schema.org', **{k: v for k, v in BUSINESS.items() if k != '@id'},
              'hasOfferCatalog': {'@type': 'OfferCatalog', 'name': 'Web development services',
                                  'itemListElement': [{'@type': 'Offer', 'itemOffered': {'@type': 'Service', 'name': html.unescape(t)}} for _, _, t, _, _, _ in SERVICES]}}
    main = f'''{page_hero('Services', 'What I build.', 'New websites and online stores, or improvements to the one you already have — on the platform that suits how your business sells.')}

    <section class="services-list" aria-label="Services">
      <div class="wrap">
{rows_html}
      </div>
    </section>

{process()}

{final_cta()}'''
    return page(head('Services — Shopify, WordPress &amp; Custom Websites | Shadab Ali',
                     'Shopify development, WordPress and WooCommerce websites, custom web development and website redesigns by freelance developer Shadab Ali.',
                     'services.html', schema), 'page-services', 'services.html', main)

def about_page():
    why = ''.join(f'<li class="why-item" data-reveal><h3 class="why-title">{t}</h3><p>{dsc}</p></li>' for t, dsc in WHY)
    skills = ''.join(f'<li>{s}</li>' for s in SKILLS)
    main = f'''    <section class="about-band about-band--page" aria-labelledby="page-title">
      <div class="wrap about-grid">
        <figure class="about-figure">
          <span class="monogram" aria-hidden="true"></span>
          <span class="about-portrait">{pic('profile', 'Portrait of Shadab Ali', '(max-width: 767px) 80vw, 36vw', loading='eager')}</span>
        </figure>
        <div class="about-copy">
          <p class="label page-kicker">About</p>
          <h1 class="h1 split" id="page-title" data-reveal><span class="line">One developer.</span> <span class="line">Fully invested.</span></h1>
          <div class="about-text" data-reveal>
            <p class="lead">I’m Shadab Ali, a freelance web developer based in Delhi, working with businesses on ecommerce stores and modern web experiences.</p>
            <p>My work spans Shopify, Liquid, WordPress, WooCommerce and front-end development.</p>
            <p>I prefer practical solutions over unnecessary complexity. I first understand how the business works, then build the website around those requirements.</p>
            <p>Clients work directly with me throughout the project — from the first discussion through development, testing and launch.</p>
            <ul class="skills" aria-label="Skills">{skills}</ul>
            <p class="about-where"><span class="label">Based in</span> Delhi, India <span class="label">Working</span> Worldwide</p>
          </div>
        </div>
      </div>
    </section>

    <section class="why" aria-labelledby="why-title">
      <div class="wrap">
        <h2 class="h3" id="why-title">Why work with me</h2>
        <ul class="why-list">{why}</ul>
      </div>
    </section>

{process()}

{final_cta()}'''
    return page(head('About Shadab Ali — Freelance Web Developer in Delhi',
                     'Shadab Ali is a freelance web developer in Delhi, working with businesses worldwide on Shopify, WordPress, WooCommerce and front-end projects.',
                     'about.html'), 'page-about', 'about.html', main)

def contact_page():
    include = [('Name and company / brand', None), ('Project type', ' · '.join(PROJECT_TYPES)), ('Current website', 'If you have one'),
               ('Budget range', ' · '.join(BUDGETS)), ('Timeline', ' · '.join(TIMELINES)), ('Project details', 'What you are building and what success looks like')]
    include_html = ''
    for t, d in include:
        detail = f'<span class="muted">{d}</span>' if d else ''
        include_html += f'<li><span class="brief-item">{t}</span>{detail}</li>'
    types = '|'.join(PROJECT_TYPES)
    main = f'''    <section class="contact-hero theme-dark" aria-labelledby="page-title">
      <div class="wrap contact-grid">
        <p class="label page-kicker">Contact</p>
        <h1 class="contact-title split" id="page-title" data-reveal>{lines('Let’s talk', 'about your', 'project.')}</h1>
        <p class="contact-lede" data-reveal>Share a few details about your project and I’ll review them before getting back to you. Reach me directly — whichever is easiest.</p>
        <ul class="channels" aria-label="Direct contact">
          <li><span class="label">Email</span><a class="channel" href="mailto:{EMAIL}">{EMAIL} {ARROW_UP}</a></li>
          <li><span class="label">WhatsApp</span><a class="channel" href="{WHATSAPP_HELLO}" target="_blank" rel="noopener noreferrer">{WHATSAPP_LABEL} {ARROW_UP}<span class="visually-hidden"> (opens WhatsApp)</span></a></li>
          <li><span class="label">LinkedIn</span><a class="channel" href="{LINKEDIN}" target="_blank" rel="noopener noreferrer">Shadab Ali {ARROW_UP}{NEW_TAB}</a></li>
        </ul>
      </div>
    </section>

    <section class="brief" aria-labelledby="brief-title">
      <div class="wrap brief-grid">
        <div class="brief-head">
          <h2 class="h3" id="brief-title">What to include</h2>
          <p class="muted">A few lines on each helps me reply with something useful. Based in Delhi, India — working with clients worldwide.</p>
          <a class="button" href="{BRIEF_MAILTO}" data-brief-mail data-types="{html.escape(types)}">Send project details {ARROW_UP}</a>
          <p class="brief-note muted">Opens your email app with these headings ready to fill in.</p>
        </div>
        <ul class="brief-list" data-reveal>{include_html}</ul>
      </div>
    </section>'''
    return page(head('Contact — Start a Project | Shadab Ali',
                     'Tell Shadab Ali about your Shopify, WordPress, WooCommerce or custom website project by email, WhatsApp or LinkedIn.',
                     'contact.html'), 'page-contact', 'contact.html', main)

def not_found_page():
    r = '/'
    main = f'''    <section class="page-hero page-hero--simple" aria-labelledby="page-title">
      <div class="wrap page-hero-grid">
        <p class="label page-kicker">404</p>
        <h1 class="page-title split" id="page-title" data-reveal>Page not found.</h1>
        <p class="page-lede" data-reveal>The link may be old or mistyped. Everything else is one click away.</p>
        <div class="page-actions"><a class="button" href="{r}work.html">View work {ARROW}</a><a class="button button--ghost" href="{r}index.html">Back to home {ARROW}</a></div>
      </div>
    </section>'''
    return page(head('Page not found | Shadab Ali', 'This page could not be found.', '404.html', noindex=True, r=r), 'page-simple', None, main, r)

# ---------------------------------------------------------------- output
def write(path, content):
    with open(path, 'wb') as f:
        f.write(content.replace('\r\n', '\n').replace('\n', '\r\n').encode('utf-8'))
    print('wrote', path)

def sitemap():
    urls = ['/', '/work.html'] + [f'/{p["file"]}' for p in PROJECTS] + ['/services.html', '/about.html', '/contact.html']
    body = ''.join(f'  <url><loc>{SITE_URL}{u}</loc></url>\n' for u in urls)
    with open('sitemap.xml', 'w') as f:
        f.write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{body}</urlset>\n')
    with open('robots.txt', 'w') as f:
        f.write(f'User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n')
    print('wrote sitemap.xml, robots.txt')

if __name__ == '__main__':
    write('index.html', home())
    write('work.html', projects_page())
    for i, p in enumerate(PROJECTS):
        write(p['file'], case_page(p, i))
    write('services.html', services_page())
    write('about.html', about_page())
    write('contact.html', contact_page())
    write('404.html', not_found_page())
    sitemap()
