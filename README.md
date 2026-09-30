# Shadab Ali — portfolio website

Static multipage portfolio for Shadab Ali, freelance Shopify & WordPress developer. HTML, CSS, JavaScript and images only: no framework, no server code, no build step on Vercel.

## Pages

- `index.html` — poster hero (role, name, featured project, two calls to action), 01 Intro statement, 02 Selected work (four large project displays, each in its own colour mood) and the Diviniti numbers, 03 Expertise (what I build and technology), 04 About (portrait, why work with me, the five-step process), 05 Contact (Let’s talk) and the footer
- `work.html` — the four projects and the Diviniti numbers
- `case-diviniti.html`, `case-portrait-on-gold.html`, `case-majestic-india.html`, `case-uncostly.html` — project pages: number, name, introduction, live site, cover, Client / Platform / Industry / Role, /Details (challenge, solution, implementation, results), /Image gallery and next project. On the homepage and projects page, project links open the same page as a full-screen overlay; the address changes so it can be shared, and Back or Escape closes it.
- `services.html` — the four services with their scope, and the process
- `about.html` — introduction, why work with me and the process
- `contact.html` — direct contact (email, WhatsApp, LinkedIn) and a “Send project details” button that opens an email with the brief headings ready to fill in. There is no form and nothing to configure: messages go straight to your inbox or WhatsApp.
- `404.html` — page-not-found page (Vercel serves it for missing URLs)

## Deploy on Vercel

Import the repository in Vercel with Framework Preset **Other**, Root Directory `./`, no build command and output directory `.` (`vercel.json` already selects this). Every push to `main` redeploys the site. No environment variables are needed.

## How it is built

- `tools/build_pages.py` writes every HTML page, `sitemap.xml` and `robots.txt` from one place: header, footer, final call to action, projects (role, stack, scope, case study text), services, capabilities, technology, process, page titles and descriptions, and structured data (WebSite, Person, ProfessionalService). Edit content there and run `python3 tools/build_pages.py` from the repository root (needs Python 3 and Pillow, which reads image sizes). Do not edit the generated HTML by hand; the next run overwrites it.
- `site.css` — the design system: colour tokens (canvas `#f4f1ea`, ink `#111111`, secondary `#6f6c65`, rules `#d8d3c9`), the four project moods (`theme-dark`, `theme-warm`, `theme-ivory`, `theme-white`) and the dark footer, a 12 / 8 / 4 column grid (desktop / tablet / mobile), the type scale, every section, motion and the reduced-motion rules. Hover effects only apply on devices with a real mouse, so taps on phones never leave a stuck state.
- `site.js` — slim sticky header, mobile menu, scroll reveals (word-by-word headings and image clip reveals), the section index along the left edge on wide screens, the “View project” cursor (mouse only), the project overlay, and the contact email pre-fill when a visitor arrives from a service’s “Start a project” link.

## Content that comes from you

Everything on the site comes from your existing site text and your own project screenshots. Technologies listed are only the ones used in the four projects and services. The figures quoted are the ones already on the site: 500+ products and 20+ custom Liquid sections for Diviniti, and Diviniti’s 40% Largest Contentful Paint improvement, labelled as reported. Project years are not shown because they are not recorded anywhere.

Testimonials: the homepage has a testimonial section that stays hidden while `TESTIMONIALS` in `tools/build_pages.py` is empty. To show it, add real quotes you have permission to use, for example `{'quote': '…', 'name': 'Client name', 'role': 'Role, Company'}`, and rerun the script.

## Images and fonts

Project images live in `assets/work/`, cropped from the full-length screenshots in the repository’s history (commit `279d757`). The large project images (`*-exhibit-*`, `*-phone-*`, `diviniti-poster-*`) and the portrait come in AVIF and WebP at several widths; browsers pick the smallest suitable file, and phones get the project’s mobile screenshot instead of a shrunken desktop one. Gallery images are WebP in two widths. If you replace an image, keep the same names and widths. `assets/grain.png` is the 5 KB paper texture.

The font is Inter Tight (SIL Open Font License, see `assets/fonts`), self-hosted, so no requests go to Google Fonts.

## Local preview

From this folder, run `python3 -m http.server 4173`, then open `http://localhost:4173/`.

## Site address

Canonical links, link-preview tags (`og:url`, `og:image`), structured data, `robots.txt` and `sitemap.xml` use `https://website-swart-nu-54.vercel.app`. If you connect a custom domain, change `SITE_URL` near the top of `tools/build_pages.py` and run `python3 tools/build_pages.py`.

WhatsApp and LinkedIn cache link previews, so a changed preview can take a while to appear. LinkedIn’s Post Inspector refreshes it immediately.
