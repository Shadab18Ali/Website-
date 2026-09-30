"""Builds every HTML page of the site from shared components.

The HTML files in the repository root are the published site, so no build step is needed to deploy.
Edit content here and regenerate when you want every page to stay consistent:

    pip install pillow        # once; used to read image sizes
    python3 tools/build_pages.py

Anything edited directly in the HTML files is overwritten the next time this script runs.
"""
import glob, html, json, os, re
from PIL import Image

# ---------------------------------------------------------------- site settings
# Change SITE_URL when the site moves to a custom domain, then rerun this script.
SITE_URL = 'https://website-swart-nu-54.vercel.app'
EMAIL = 'shadab18ali@gmail.com'
WHATSAPP = 'https://wa.me/919931394885'
WHATSAPP_LABEL = '+91 99313 94885'
LINKEDIN = 'https://linkedin.com/in/shadab-ali-7b0261238'
BLANK_GIF = 'data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7'

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

# Genuine client testimonials only. While this list is empty no testimonial section is published.
# Example entry: {'quote': '…', 'name': 'Client name', 'role': 'Role, Company'}
TESTIMONIALS = []

# ---------------------------------------------------------------- images
def variants(name):
    out = []
    for f in glob.glob(f'assets/work/{name}-*.webp'):
        m = re.match(rf'assets/work/{re.escape(name)}-(\d+)\.webp$', f)
        if m:
            out.append((int(m.group(1)), f))
    assert out, f'missing image: {name}'
    return sorted(out)

def img(name, alt, sizes, loading='lazy', priority=None, r=''):
    vs = variants(name)
    w, h = Image.open(vs[-1][1]).size
    srcset = ', '.join(f'{r}{f} {vw}w' for vw, f in vs)
    attrs = [f'src="{r}{vs[-1][1]}"', f'srcset="{srcset}"', f'sizes="{sizes}"', f'alt="{html.escape(alt)}"',
             f'width="{w}"', f'height="{h}"', f'loading="{loading}"', 'decoding="async"']
    if priority:
        attrs.append(f'fetchpriority="{priority}"')
    return '<img ' + ' '.join(attrs) + '>'

def figure(name, alt, cls, sizes, caption=None):
    cap = f'<figcaption class="label muted">{caption}</figcaption>' if caption else ''
    return f'<figure class="{cls}"><div class="seq-media" data-reveal="clip">{img(name, alt, sizes)}</div>{cap}</figure>'

def label(text, tag='p', cls='', id_=None):
    idattr = f' id="{id_}"' if id_ else ''
    extra = f' {cls}' if cls else ''
    return f'<{tag} class="label{extra}"{idattr}><span class="slash" aria-hidden="true">/</span>{text}</{tag}>'

def lines(*parts):
    """Big display headings set line by line."""
    return ' '.join(f'<span class="line">{p}</span>' for p in parts)

# ---------------------------------------------------------------- projects (facts come from the original portfolio)
PROJECTS = [
  dict(slug='diviniti', file='case-diviniti.html', num='01', name='Diviniti', cat='Shopify Development', platform='Shopify',
       live='https://www.diviniti.com', cover='diviniti-cover', cover_alt='Diviniti Shopify storefront homepage',
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
       live='https://www.portraitongold.com', cover='pog-cover', cover_alt='Portrait on Gold Shopify storefront homepage',
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
       live='https://themajesticindia.com', cover='majestic-cover', cover_alt='The Majestic India WordPress website homepage',
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
       live='https://uncostly.in', cover='uncostly-cover', cover_alt='Uncostly WooCommerce catalogue homepage',
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
PROJECT_TYPES = ['Shopify', 'WordPress / WooCommerce', 'Website Redesign', 'Custom Development', 'Other']
BUDGETS = ['Under ₹25,000', '₹25,000–₹50,000', '₹50,000–₹1,00,000', '₹1,00,000+', 'Not sure yet']
TIMELINES = ['ASAP', '2–4 weeks', '1–2 months', 'Flexible']
EXPERTISE = ['Shopify', 'Liquid', 'WordPress', 'WooCommerce', 'HTML', 'CSS', 'JavaScript', 'Responsive development', 'Performance optimisation']

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
             f'<meta property="og:title" content="{title}">',
             f'<meta property="og:description" content="{desc}">',
             f'<meta property="og:url" content="{url}">',
             f'<meta property="og:image" content="{image}">',
             '<meta property="og:image:width" content="1200">',
             '<meta property="og:image:height" content="630">',
             '<meta property="og:image:alt" content="Shadab Ali, freelance web developer">',
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
  <meta name="theme-color" content="#f1ede5">
  {body}
</head>'''

NAV = [('work.html', 'Projects'), ('services.html', 'Services'), ('about.html', 'About'), ('contact.html', 'Contact')]

def header(current=None, r=''):
    cur = ' aria-current="page"'
    links = ''.join(f'<a href="{r}{h}"{cur if h == current else ""}>{t}</a>' for h, t in NAV)
    return f'''  <a class="skip-link" href="#main">Skip to content</a>
  <header class="site-header" id="top" data-header>
    <div class="wrap header-inner">
      <a class="brand" href="{r}index.html" aria-label="Shadab Ali, home">Shadab Ali</a>
      <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="site-nav" data-menu-toggle>Menu</button>
      <nav class="nav" id="site-nav" aria-label="Main">{links}<a class="nav-cta" href="{r}contact.html">Start a project</a><p class="nav-extra"><a href="mailto:{EMAIL}">{EMAIL}</a><a href="{WHATSAPP}" target="_blank" rel="noopener noreferrer">WhatsApp {WHATSAPP_LABEL}</a></p></nav>
    </div>
  </header>'''

def contact_list(r=''):
    return f'''<dl class="talk-grid" data-reveal>
          <div class="talk-item"><dt class="label">Email</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd></div>
          <div class="talk-item"><dt class="label">WhatsApp</dt><dd><a href="{WHATSAPP}" target="_blank" rel="noopener noreferrer">{WHATSAPP_LABEL}<span class="visually-hidden"> (opens WhatsApp)</span></a></dd></div>
          <div class="talk-item"><dt class="label">LinkedIn</dt><dd><a href="{LINKEDIN}" target="_blank" rel="noopener noreferrer">Shadab Ali<span class="visually-hidden"> on LinkedIn (opens in a new tab)</span></a></dd></div>
          <div class="talk-item"><dt class="label">Location</dt><dd>Delhi, India<br>Working worldwide</dd></div>
        </dl>'''

def talk(r=''):
    """Homepage contact section."""
    return f'''    <section class="section talk" id="talk" aria-labelledby="talk-title">
      <div class="wrap">
        {label('Contact')}
        <h2 class="talk-title split" id="talk-title" data-reveal>Let’s talk</h2>
        {contact_list(r)}
        <div class="talk-cta"><a class="button" href="{r}contact.html">Start a project <span aria-hidden="true">→</span></a></div>
      </div>
    </section>'''

def cta(r=''):
    """Closing call to action for inner pages."""
    return f'''    <section class="section cta" aria-labelledby="cta-title">
      <div class="wrap">
        {label('Next step')}
        <h2 class="cta-title split" id="cta-title" data-reveal>Have a project in mind?</h2>
        <div class="cta-actions" data-reveal><a class="button" href="{r}contact.html">Start a project <span aria-hidden="true">→</span></a><a class="arrow-link" href="{r}work.html">View selected work <span class="arrow" aria-hidden="true">→</span></a></div>
        <p class="cta-direct" data-reveal>Or reach me directly: <a href="mailto:{EMAIL}">{EMAIL}</a> · <a href="{WHATSAPP}" target="_blank" rel="noopener noreferrer">WhatsApp<span class="visually-hidden"> (opens WhatsApp)</span></a></p>
      </div>
    </section>'''

def footer(r=''):
    return f'''  <footer class="site-footer">
    <div class="wrap">
      <div class="footer-grid">
        <div class="footer-col"><p class="footer-brand">Shadab Ali</p><p>Freelance Web Developer</p></div>
        <div class="footer-col"><p>Delhi, India</p><p>Working worldwide</p></div>
        <nav class="footer-col footer-links" aria-label="Footer"><a href="{r}work.html">Projects</a><a href="{r}services.html">Services</a><a href="{r}about.html">About</a><a href="{r}contact.html">Contact</a></nav>
        <div class="footer-col footer-links"><a href="{LINKEDIN}" target="_blank" rel="noopener noreferrer">LinkedIn<span class="visually-hidden"> (opens in a new tab)</span></a><a href="mailto:{EMAIL}">Email</a><a href="{WHATSAPP}" target="_blank" rel="noopener noreferrer">WhatsApp<span class="visually-hidden"> (opens WhatsApp)</span></a></div>
      </div>
      <div class="footer-name-wrap" aria-hidden="true"><p class="footer-name">Shadab Ali</p></div>
      <div class="footer-bar"><p class="footer-copy">© <span data-year>2026</span> Shadab Ali</p><a class="footer-top" href="#top">Back to top <span aria-hidden="true">↑</span></a></div>
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
        {label('Client words', 'h2', id_='testimonials-title')}
        <div class="testimonial-list">{items}</div>
      </div>
    </section>
'''

# ---------------------------------------------------------------- structured data
PERSON = {'@type': 'Person', '@id': f'{SITE_URL}/#person', 'name': 'Shadab Ali', 'jobTitle': 'Freelance Web Developer',
          'url': f'{SITE_URL}/', 'image': f'{SITE_URL}/assets/profile.webp', 'email': f'mailto:{EMAIL}',
          'address': {'@type': 'PostalAddress', 'addressLocality': 'Delhi', 'addressCountry': 'IN'},
          'sameAs': [LINKEDIN], 'knowsAbout': ['Shopify', 'Liquid', 'WordPress', 'WooCommerce', 'Front-end development', 'Web performance']}
BUSINESS = {'@type': 'ProfessionalService', '@id': f'{SITE_URL}/#service', 'name': 'Shadab Ali — Freelance Web Development',
            'url': f'{SITE_URL}/', 'image': f'{SITE_URL}/assets/og-image.jpg', 'email': f'mailto:{EMAIL}',
            'founder': {'@id': f'{SITE_URL}/#person'}, 'areaServed': 'Worldwide',
            'address': {'@type': 'PostalAddress', 'addressLocality': 'Delhi', 'addressCountry': 'IN'},
            'knowsAbout': ['Shopify development', 'WordPress development', 'WooCommerce development', 'Custom web development', 'Website redesign']}

# ---------------------------------------------------------------- project list (home + projects page)
def project_list(title_tag):
    out = []
    for i, p in enumerate(PROJECTS):
        mods = (' project--alt' if i % 2 else '') + (' project--inset' if i in (1, 2) else '')
        out.append(f'''        <article class="project{mods}" aria-labelledby="p-{p['slug']}">
          <div class="grid project-head">
            <span class="label project-num">Project {p['num']}</span>
            <{title_tag} class="project-title split" id="p-{p['slug']}" data-reveal>{p['name']}</{title_tag}>
            <div class="project-info">
              <p class="project-cat">{p['cat']}</p>
              <a class="view-link" href="{p['file']}" data-open-project>View project<span class="visually-hidden">: {p['name']}</span> <span class="arrow" aria-hidden="true">↗</span></a>
            </div>
          </div>
          <a class="project-media" href="{p['file']}" data-open-project data-cursor="view" tabindex="-1" aria-hidden="true" data-reveal="clip">{img(p['cover'], p['cover_alt'], '92vw')}</a>
        </article>''')
    return '\n'.join(out)

# ---------------------------------------------------------------- project detail
GALLERY_SIZES = {'full': '(max-width: 760px) 100vw, 96vw', 'pair': '(max-width: 760px) 100vw, 46vw', 'large': '(max-width: 760px) 100vw, 80vw', 'detail': '(max-width: 760px) 100vw, 40vw'}

def case_article(p, idx):
    nxt = PROJECTS[(idx + 1) % len(PROJECTS)]
    meta = ''.join(f'<div class="meta-{k.lower()}"><dt class="label">{k}</dt><dd>{v}</dd></div>' for k, v in p['meta'])
    paras = lambda items: ''.join(f'<p>{t}</p>' for t in items)
    impl = '<ul class="case-list">' + ''.join(f'<li>{t}</li>' for t in p['implementation']) + '</ul>'
    if p['facts']:
        results = '<ul class="case-facts">' + ''.join(f'<li class="case-fact"><strong>{n}</strong><span class="label">{t}</span></li>' for n, t in p['facts']) + '</ul>'
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
    gallery_html = '\n          '.join(gallery)
    return f'''    <article class="case wrap" data-case aria-labelledby="case-title">
      <div class="case-bar"><a class="case-close" href="work.html" data-case-close><span class="x" aria-hidden="true"></span>Close</a><span class="label muted">Project {p['num']} / 0{len(PROJECTS)}</span></div>
      <figure class="case-hero"><div class="seq-media">{img(p['cover'], p['cover_alt'], '(max-width: 760px) 100vw, 96vw', loading='eager', priority='high')}</div></figure>
      <header class="grid case-head">
        <span class="label case-num">Project {p['num']} · {p['cat']}</span>
        <h1 class="case-title split" id="case-title" data-reveal>{p['name']}</h1>
        <div class="case-intro" data-reveal><p>{p['intro']}</p><a class="arrow-link" href="{p['live']}" target="_blank" rel="noopener noreferrer">View live site <span class="arrow" aria-hidden="true">↗</span><span class="visually-hidden"> (opens in a new tab)</span></a></div>
      </header>
      <dl class="case-meta" data-reveal>{meta}</dl>
      <section class="case-details" aria-labelledby="details-{p['slug']}">
        {label('Details', 'h2', id_='details-' + p['slug'])}
        <div class="grid case-cols">
          <div class="case-col" data-reveal><h3>Challenge</h3>{paras(p['challenge'])}</div>
          <div class="case-col" data-reveal><h3>Solution</h3>{paras(p['solution'])}</div>
          <div class="case-col" data-reveal><h3>Implementation</h3>{impl}</div>
          <div class="case-col case-results" data-reveal><h3>Results</h3>{results}</div>
        </div>
      </section>
      <section class="case-gallery" aria-labelledby="gallery-{p['slug']}">
        {label('Image gallery', 'h2', id_='gallery-' + p['slug'])}
        <div class="grid gallery">
          {gallery_html}
        </div>
      </section>
      <nav class="case-next" aria-label="Next project"><span class="label muted">Next project</span><a href="{nxt['file']}" data-open-project>{nxt['name']} <span class="arrow" aria-hidden="true">→</span></a></nav>
    </article>'''

def case_page(p, idx):
    desc = html.escape(p['intro'], quote=True)
    return page(head(f"{p['name']} — {p['cat']} Case Study | Shadab Ali", desc, p['file']), 'page-case', 'work.html', case_article(p, idx) + '\n\n' + cta())

# ---------------------------------------------------------------- homepage
def hero_letter(ch, i):
    return f'<span class="l"><span style="--i:{i}">{ch}</span></span>'

def hero_shot(name, cls, i, sizes, mobile_hidden=False, priority=None):
    tag = img(name, '', sizes, loading='eager', priority=priority)
    if mobile_hidden:
        tag = f'<picture><source media="(max-width: 760px)" srcset="{BLANK_GIF}">{tag}</picture>'
    return f'<span class="hero-shot {cls}" style="--i:{i}">{tag}</span>'

def home():
    sha = ''.join(hero_letter(c, i) for i, c in enumerate('SHA'))
    dab = ''.join(hero_letter(c, i + 3) for i, c in enumerate('DAB'))
    ali = ''.join(hero_letter(c, i + 6) for i, c in enumerate('ALI'))
    hero = f'''    <section class="hero wrap" aria-labelledby="hero-title">
      <p class="label hero-role">Freelance Web<br>Developer</p>
      <h1 class="hero-name" id="hero-title">
        <span class="visually-hidden">Shadab Ali, freelance web developer</span>
        <span class="hero-line hero-line-1" aria-hidden="true">
          <span class="hero-group g-sha">{sha}</span>
          {hero_shot('hero-pog', 'shot-pog', 1, '(max-width: 760px) 20vw, 10vw')}
          <span class="hero-group g-dab">{dab}</span>
          {hero_shot('hero-uncostly', 'shot-uncostly', 2, '18vw', mobile_hidden=True)}
        </span>
        <span class="hero-line hero-line-2" aria-hidden="true">
          {hero_shot('hero-diviniti', 'shot-diviniti', 0, '31vw', mobile_hidden=True, priority='high')}
          <span class="hero-group g-ali">{ali}</span>
          {hero_shot('hero-majestic', 'shot-majestic', 3, '(max-width: 760px) 23vw, 9vw')}
        </span>
      </h1>
      <div class="hero-foot">
        <div class="hero-intro">
          <p>Shopify, WordPress and custom websites built for businesses that want a stronger, faster and more effective online presence. Based in Delhi, working with clients worldwide.</p>
          <div class="hero-actions"><a class="button" href="contact.html">Start a project <span aria-hidden="true">→</span></a><a class="arrow-link" href="#projects">View selected work <span class="arrow" aria-hidden="true">↓</span></a></div>
        </div>
        <a class="scroll-cue" href="#who">Scroll down <span class="scroll-line" aria-hidden="true"></span></a>
      </div>
    </section>'''
    seq = [
      ('seq-diviniti-collections', 'Diviniti curated collections on mobile', 'seq-1', '(max-width: 760px) 62vw, 22vw', 'Diviniti — Mobile', '0.06'),
      ('seq-pog-chosen', 'Portrait on Gold "Chosen by the finest" section on desktop', 'seq-2', '(max-width: 760px) 80vw, 56vw', 'Portrait on Gold — Desktop', '-0.05'),
      ('seq-majestic-founder', 'The Majestic India founder section on desktop', 'seq-3', '(max-width: 760px) 100vw, 88vw', 'The Majestic India — Desktop', '0.04'),
      ('seq-uncostly-kit', 'Uncostly smart security kit section on mobile', 'seq-4', '(max-width: 760px) 62vw, 22vw', 'Uncostly — Mobile', '-0.07'),
      ('seq-diviniti-custom', 'Diviniti customisation section on desktop', 'seq-5', '(max-width: 760px) 80vw, 64vw', 'Diviniti — Desktop', '0.05'),
    ]
    seq_html = '\n'.join(f'          <figure class="seq {cls}" data-parallax="{speed}"><div class="seq-media" data-reveal="clip">{img(n, alt, sizes)}</div><figcaption class="label muted">{cap}</figcaption></figure>'
                         for n, alt, cls, sizes, cap, speed in seq)
    stats = [('500+', 'Product catalogue experience', 'Diviniti Shopify store', ''),
             ('20+', 'Custom Shopify sections', 'Built for Diviniti', ''),
             ('40%', 'Reported LCP improvement', 'Diviniti Shopify project', ''),
             ('Shopify<br>WordPress<br>WooCommerce', 'Core platforms', 'Across all four selected projects', ' stat-num--text')]
    stats_html = ''.join(f'<li class="stat" data-reveal><strong class="stat-num{mod}">{n}</strong><span class="label stat-label">{t}</span><span class="stat-context">{c}</span></li>'
                         for n, t, c, mod in stats)
    expertise = ''.join(f'<li>{t}</li>' for t in EXPERTISE)
    main = f'''{hero}

    <section class="sequence" aria-label="Screens from client websites">
      <div class="wrap grid seq-grid">
{seq_html}
      </div>
    </section>

    <section class="section intro" id="who" aria-labelledby="who-title">
      <div class="wrap grid">
        {label('Who am I', 'h2', 'intro-label', 'who-title')}
        <p class="statement split" data-reveal>I build digital experiences where thoughtful design meets practical development.</p>
        <figure class="intro-portrait"><div class="seq-media" data-reveal="clip">{img('profile', 'Portrait of Shadab Ali', '(max-width: 760px) 50vw, 24vw')}</div></figure>
        <div class="intro-copy" data-reveal>
          <p>I’m Shadab Ali, a freelance web developer based in Delhi, India.</p>
          <p>I work across Shopify, Liquid, WordPress, WooCommerce and custom front-end development. I start by understanding how a business works, then build the website around its real needs.</p>
          <p>Clean interfaces, responsive development, useful functionality and performance — for clients in India and around the world.</p>
          <a class="arrow-link" href="about.html">More about me <span class="arrow" aria-hidden="true">→</span></a>
        </div>
      </div>
    </section>

    <section class="section projects" id="projects" aria-labelledby="projects-title">
      <div class="wrap">
        <div class="projects-head">{label('Selected projects', 'h2', id_='projects-title')}<span class="label muted">0{len(PROJECTS)}</span></div>
{project_list('h3')}
      </div>
    </section>

    <section class="section stats" aria-labelledby="stats-title">
      <div class="wrap">
        {label('Proof', 'h2', id_='stats-title')}
        <ul class="stats-grid">{stats_html}</ul>
      </div>
    </section>

    <section class="section expertise" aria-labelledby="expertise-title">
      <div class="wrap grid">
        <div class="expertise-intro">{label('Expertise', 'h2', id_='expertise-title')}<p>The platforms and skills behind every project.</p></div>
        <ul class="tools expertise-list" data-reveal>{expertise}</ul>
      </div>
    </section>
{testimonials()}
    <section class="manifesto" aria-labelledby="manifesto-title">
      <div class="wrap">
        <h2 class="manifesto-text" id="manifesto-title"><span class="line split" data-reveal>Build better.</span> <span class="line line-2 split" data-reveal>Grow smarter.</span></h2>
        <div class="manifesto-links"><a class="button" href="contact.html">Start a project <span aria-hidden="true">→</span></a><a class="arrow-link" href="work.html">View selected work <span class="arrow" aria-hidden="true">→</span></a></div>
      </div>
    </section>

{talk()}'''
    schema = {'@context': 'https://schema.org', '@graph': [PERSON, BUSINESS]}
    return page(head('Shadab Ali | Freelance Shopify &amp; WordPress Developer',
                     'Freelance web developer specialising in Shopify, WordPress, WooCommerce and custom websites. Explore selected work by Shadab Ali.',
                     'index.html', schema), 'page-home', None, main)

# ---------------------------------------------------------------- inner pages
def projects_page():
    main = f'''    <section class="page-hero wrap" aria-labelledby="page-title">
      {label('Projects')}
      <h1 class="page-title split" id="page-title" data-reveal>Selected work</h1>
      <div class="grid"><p class="page-lede" data-reveal>Four client websites across Shopify, WordPress and WooCommerce. Open a project to see the challenge, the solution and the live site.</p></div>
    </section>

    <section class="projects" aria-label="Projects">
      <div class="wrap">
{project_list('h2')}
      </div>
    </section>

{cta()}'''
    return page(head('Selected Work | Shadab Ali', 'Selected Shopify, WordPress and WooCommerce projects by freelance web developer Shadab Ali: Diviniti, Portrait on Gold, The Majestic India and Uncostly.', 'work.html'),
                'page-projects', 'work.html', main)

def services_page():
    rows = []
    for sid, num, title, desc, scope, ptype in SERVICES:
        feature = ' service--feature' if sid == 'redesign' else ''
        items = ''.join(f'<li>{x}</li>' for x in scope)
        rows.append(f'''        <article class="grid service{feature}" id="{sid}" aria-labelledby="{sid}-title">
          <span class="label service-num">{num}</span>
          <div class="service-body"><h2 class="service-title split" id="{sid}-title" data-reveal>{title}</h2><p>{desc}</p><a class="arrow-link" href="contact.html" data-service="{ptype}">Start a project <span class="arrow" aria-hidden="true">→</span></a></div>
          <ul class="service-scope" aria-label="What’s included">{items}</ul>
        </article>''')
    rows_html = '\n'.join(rows)
    schema = {'@context': 'https://schema.org', **{k: v for k, v in BUSINESS.items() if k != '@id'},
              'hasOfferCatalog': {'@type': 'OfferCatalog', 'name': 'Web development services',
                                  'itemListElement': [{'@type': 'Offer', 'itemOffered': {'@type': 'Service', 'name': html.unescape(t)}} for _, _, t, _, _, _ in SERVICES]}}
    main = f'''    <section class="page-hero wrap" aria-labelledby="page-title">
      {label('Services')}
      <h1 class="page-title split" id="page-title" data-reveal>What I build.</h1>
      <div class="grid"><p class="page-lede" data-reveal>New websites and online stores, or improvements to the one you already have — on the platform that suits how your business sells.</p></div>
    </section>

    <section class="services-list" aria-label="Services">
      <div class="wrap">
{rows_html}
      </div>
    </section>

{cta()}'''
    return page(head('Services — Shopify, WordPress &amp; Custom Websites | Shadab Ali',
                     'Shopify development, WordPress and WooCommerce websites, custom web development and website redesigns by freelance developer Shadab Ali.',
                     'services.html', schema), 'page-services', 'services.html', main)

def about_page():
    steps = [('01', 'Discover', 'Understand the business, goals, audience and current challenges.'),
             ('02', 'Plan', 'Define the structure, platform, features and development approach.'),
             ('03', 'Build', 'Develop the website with responsive behaviour and clean implementation.'),
             ('04', 'Launch', 'Test, optimise and prepare for release.')]
    steps_html = ''.join(f'<li data-reveal><span class="label step-num">{n}</span><h3 class="step-title">{t}</h3><p class="step-text">{d}</p></li>' for n, t, d in steps)
    main = f'''    <section class="page-hero wrap" aria-labelledby="page-title">
      {label('About')}
      <h1 class="page-title about-title split" id="page-title" data-reveal>{lines('One', 'developer.', 'Fully', 'invested.')}</h1>
    </section>

    <section class="about-intro" aria-label="Introduction">
      <div class="wrap grid">
        <figure class="about-portrait"><div class="seq-media" data-reveal="clip">{img('profile', 'Portrait of Shadab Ali', '(max-width: 760px) 92vw, 40vw', loading='eager')}</div></figure>
        <div class="about-copy" data-reveal>
          <p>I’m Shadab Ali, a freelance web developer based in Delhi, working with businesses on ecommerce stores and modern web experiences.</p>
          <p>My work spans Shopify, Liquid, WordPress, WooCommerce and front-end development.</p>
          <p>I prefer practical solutions over unnecessary complexity. I first understand how the business works, then build the website around those requirements.</p>
          <p>Clients work directly with me throughout the project — from the first discussion through development, testing and launch.</p>
          <dl class="about-meta"><div><dt class="label muted">Based in</dt><dd>Delhi, India</dd></div><div><dt class="label muted">Working</dt><dd>Worldwide</dd></div></dl>
        </div>
      </div>
    </section>

    <section class="section" aria-labelledby="process-title">
      <div class="wrap">
        {label('Process', 'h2', id_='process-title')}
        <ol class="steps big-list">{steps_html}</ol>
      </div>
    </section>

{cta()}'''
    return page(head('About | Shadab Ali, Freelance Web Developer in Delhi',
                     'Shadab Ali is a freelance web developer in Delhi, working with businesses worldwide on Shopify, WordPress, WooCommerce and front-end projects.',
                     'about.html'), 'page-about', 'about.html', main)

def contact_page():
    opt = lambda xs: ''.join(f'<option>{x}</option>' for x in xs)
    main = f'''    <section class="page-hero wrap contact-hero" aria-labelledby="page-title">
      {label('Contact')}
      <h1 class="page-title split" id="page-title" data-reveal>{lines('Let’s talk', 'about your', 'project.')}</h1>
    </section>

    <section class="brief" id="brief" aria-labelledby="brief-title">
      <div class="wrap grid">
        <div class="brief-intro">
          {label('Project brief', 'h2', id_='brief-title')}
          <p>Share a few details about your project and I’ll review them before getting back to you. You can also reach me directly by email or WhatsApp.</p>
        </div>
        <form class="brief-form" id="inquiryForm" name="website-inquiry" method="POST" action="/api/contact" data-reveal>
          <input type="hidden" name="form-name" value="website-inquiry">
          <p class="form-honeypot" hidden><label>Leave this field blank <input name="bot-field" tabindex="-1" autocomplete="off"></label></p>
          <div class="form-row">
            <label class="field"><span class="label">Name <span aria-hidden="true">*</span></span><input name="name" type="text" autocomplete="name" placeholder="Your name" maxlength="100" required></label>
            <label class="field"><span class="label">Email <span aria-hidden="true">*</span></span><input name="email" type="email" autocomplete="email" placeholder="you@company.com" maxlength="200" required></label>
          </div>
          <div class="form-row">
            <label class="field"><span class="label">Project type <span aria-hidden="true">*</span></span><select name="service" required><option value="" selected disabled>Select a project type</option>{opt(PROJECT_TYPES)}</select></label>
            <label class="field"><span class="label">Current website <span class="optional">(optional)</span></span><input name="website" type="url" autocomplete="url" placeholder="https://" maxlength="250"></label>
          </div>
          <label class="field"><span class="label">Project details <span aria-hidden="true">*</span></span><textarea name="details" rows="4" placeholder="What are you building, and what would success look like?" maxlength="3000" required></textarea></label>
          <div class="form-row">
            <label class="field"><span class="label">Budget <span class="optional">(optional)</span></span><select name="budget"><option value="" selected>Select a range</option>{opt(BUDGETS)}</select></label>
            <label class="field"><span class="label">Timeline <span class="optional">(optional)</span></span><select name="timeline"><option value="" selected>Select a timeline</option>{opt(TIMELINES)}</select></label>
          </div>
          <button class="button" type="submit">Start the conversation <span aria-hidden="true">→</span></button>
          <p class="form-status" role="status" id="formStatus" tabindex="-1">Fields marked * are required. Nothing is sent until you press the button.</p>
        </form>
      </div>
    </section>

    <section class="section direct" aria-labelledby="direct-title">
      <div class="wrap">
        {label('Direct contact', 'h2', id_='direct-title')}
        {contact_list()}
      </div>
    </section>'''
    return page(head('Start a Project | Shadab Ali',
                     'Tell Shadab Ali about your Shopify, WordPress, WooCommerce or custom website project, or get in touch directly by email or WhatsApp.',
                     'contact.html'), 'page-contact', 'contact.html', main)

def simple_page(path, title, desc, lab, heading, text, r=''):
    main = f'''    <section class="page-hero wrap" aria-labelledby="page-title">
      {label(lab)}
      <h1 class="page-title split" id="page-title" data-reveal>{heading}</h1>
      <div class="grid"><p class="page-lede" data-reveal>{text}</p></div>
      <div class="manifesto-links"><a class="button" href="{r}work.html">View selected work <span aria-hidden="true">→</span></a><a class="arrow-link" href="{r}index.html">Back to home <span class="arrow" aria-hidden="true">→</span></a></div>
    </section>'''
    return page(head(title, desc, path, noindex=True, r=r), 'page-simple', 'contact.html' if path == 'thanks.html' else None, main, r)

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
    write('thanks.html', simple_page('thanks.html', 'Project request received | Shadab Ali', 'Thanks for contacting Shadab Ali about your website project.', 'Thank you', 'Request received.', 'Thanks for reaching out. I’ll review your project details and reply by email.'))
    write('404.html', simple_page('404.html', 'Page not found | Shadab Ali', 'This page could not be found.', '404', 'Page not found.', 'The link may be old or mistyped. Everything else is one click away.', r='/'))
    sitemap()
