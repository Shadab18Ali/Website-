# Shadab Ali — client website

Standalone multipage website for prospective website clients. The HTML, CSS, JavaScript, images, and `api/contact.mjs` are all contained in this folder. No build step or npm install is required.

## Pages

- `index.html` — name hero with "Start a project" and "View selected work", editorial image sequence, /Who am I, selected projects, proof figures, /Expertise, the closing statement, Let's talk and the footer
- `work.html` — the four projects as large editorial rows
- `case-diviniti.html`, `case-portrait-on-gold.html`, `case-majestic-india.html`, `case-uncostly.html` — project pages with the same structure: project number, cover image, name, introduction, live site link, Client / Platform / Industry / Role, /Details (challenge, solution, implementation details, results), /Image gallery and next project. On the homepage and projects page, "View project" opens the same page as a full-screen overlay; the address changes so it can be shared, and Back or Escape closes it.
- `services.html` — /Services "What I build.": Shopify development, WordPress & WooCommerce, custom web development and website redesign, each with its scope
- `about.html` — "One developer. Fully invested.", the introduction and the four-step /Process
- `contact.html` — "Let's talk about your project.", the project form (project type, current website, details, budget, timeline) and direct email / WhatsApp / LinkedIn
- `thanks.html` — shown after the contact form sends
- `404.html` — page-not-found page (Vercel serves it for missing URLs)

## Upload to GitHub and deploy on Vercel

1. Create a new GitHub repository for this client website.
2. Upload **the contents of this folder to the repository root**. `index.html`, `vercel.json`, `api/`, and `assets/` should all appear at the top level. If uploading the ZIP through GitHub's browser interface, extract it first.
3. In Vercel, choose **Add New → Project**, import that repository, and deploy with Framework Preset **Other**. Keep Root Directory at `./`, Output Directory at the project root (`.`), and leave Build Command empty. `vercel.json` also selects the Other preset.
4. For the contact form, create a Resend account and verify a sending domain. Add these Vercel Environment Variables for **Production** (and Preview if wanted): `RESEND_API_KEY`, `CONTACT_FROM_EMAIL` (for example `Shadab Ali <hello@your-verified-domain.com>`), and `CONTACT_TO_EMAIL` (your inbox). The API key stays in Vercel, never in GitHub. Redeploy after adding variables.
5. Send a real test request from the deployed `/contact.html` page and confirm it arrives at `CONTACT_TO_EMAIL`. Until those three variables and the verified sending address are set, the form shows an error and visitors can use the direct email or WhatsApp links.

Vercel's `/api/contact` function validates required fields, checks the hidden spam field, limits request size, and sends a plain-text inquiry email through Resend. The sender's address is set as the reply-to address. Local static previews prepare an email in the visitor's mail app because `python -m http.server` does not run Vercel Functions.

## How it is built

- `tools/build_pages.py` — writes every HTML page, `sitemap.xml` and `robots.txt` from one place: the header, footer, "Let's talk" block, project content, services, form options, page titles and descriptions, and structured data (Person and ProfessionalService). Edit the content there and run `python3 tools/build_pages.py` from the repository root (needs Python 3 and Pillow, which reads image sizes). Do not edit the generated HTML by hand; the next run overwrites it.
- `site.css` — the whole design system: ivory/ink palette, Inter Tight typography, the editorial grid, every section and page, motion and the reduced-motion rules.
- `site.js` — header behaviour, mobile menu, scroll reveals, parallax on the image sequence, the "View" cursor (mouse only), the project overlay, service pre-selection from `?service=`, and the contact form.
- The contact form's project types, budgets and timelines are listed in `tools/build_pages.py` (`PROJECT_TYPES`, `BUDGETS`, `TIMELINES`) and checked again in `api/contact.mjs`. If you change one list, change the other.

## Content that comes from you

Everything on the site comes from your existing site text and your own project screenshots. Project years are not shown because they are not recorded anywhere; add a `Year` row to a project's `meta` list in `tools/build_pages.py` if you want one. The figures quoted are the ones already on the site: 500+ products and 20+ custom Liquid sections for Diviniti, and Diviniti's 40% Largest Contentful Paint improvement, labelled as reported.

Testimonials: the homepage has a testimonial section that stays hidden while `TESTIMONIALS` in `tools/build_pages.py` is empty. To show it, add real quotes you have permission to use, for example `{'quote': '…', 'name': 'Client name', 'role': 'Role, Company'}`, and rerun the script.

## Images and fonts

Project images live in `assets/work/`, cropped from the full-length screenshots in the repository's history (commit `279d757`). Each image comes in two widths (for example `diviniti-cover-1600.webp` and `diviniti-cover-900.webp`) and pages let the browser pick the right one. If you replace an image, replace both widths with the same names. Browsers cache images for a day (`vercel.json`).

The font is Inter Tight (SIL Open Font License, see `assets/fonts`), self-hosted, so no requests go to Google Fonts.

## Local preview

From this folder, run `python -m http.server 4173`, then open `http://localhost:4173/`.

## Before sharing

Check the public email address, WhatsApp number, portrait, project descriptions, external project links, and permission to display screenshots. Every project result describes what was built; the only performance figure is Diviniti's reported 40% LCP improvement. Add numbers only when you can stand behind them.

## Site address

Canonical links, link-preview tags (`og:url`, `og:image`), structured data, `robots.txt`, and `sitemap.xml` use `https://website-swart-nu-54.vercel.app`. If you connect a custom domain, change `SITE_URL` near the top of `tools/build_pages.py` and run `python3 tools/build_pages.py`.

WhatsApp and LinkedIn cache link previews, so a changed preview can take a while to appear. LinkedIn's Post Inspector refreshes it immediately.
