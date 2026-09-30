# Shadab Ali — client website

Standalone multipage website for prospective website clients. The HTML, CSS, JavaScript, images, and `api/contact.mjs` are all contained in this folder. No build step or npm install is required.

## Pages

- `index.html` — letter-by-letter name hero, editorial image sequence, /Who am I, selected projects, numbers, "Build better. Grow smarter.", selected clients, Let's talk and the closing name
- `work.html` — the four projects as large editorial rows
- `case-diviniti.html`, `case-portrait-on-gold.html`, `case-majestic-india.html`, `case-uncostly.html` — project detail pages (close, cover, live site, intro, client/platform/industry/role, /Details challenge and solution, /Image gallery, next project). On the homepage and projects page, "View project" opens the same page as a full-screen overlay; the address changes so it can be shared, and Back or Escape closes it.
- `services.html` — the four services with their scope, and the FAQ
- `about.html` — introduction, working directly together, process, why work with me and tools
- `contact.html` — Let's talk details and the project brief form (including budget and timeline)
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

- `site.css` — the whole design system: ivory/ink palette, Inter Tight typography, the editorial grid, every section and page, motion and the reduced-motion rules.
- `site.js` — header behaviour, mobile menu, scroll reveals, parallax on the image sequence, the "View" cursor (mouse only), the project overlay, service pre-selection from `?service=`, and the contact form.
- The header, footer and "Let's talk" section are repeated in every HTML page. If you change one, change them all.

## Content that comes from you

Everything on the site comes from your existing site text and your own project screenshots. Project years are not shown because they are not recorded anywhere; add a `Year` row to a project's details list in its `case-*.html` file if you want one. The only figure quoted is Diviniti's 40% Largest Contentful Paint improvement, labelled as reported.

## Images and fonts

Project images live in `assets/work/`, cropped from the full-length screenshots in the repository's history (commit `279d757`). Each image comes in two widths (for example `diviniti-cover-1600.webp` and `diviniti-cover-900.webp`) and pages let the browser pick the right one. If you replace an image, replace both widths with the same names. Browsers cache images for a day (`vercel.json`).

The font is Inter Tight (SIL Open Font License, see `assets/fonts`), self-hosted, so no requests go to Google Fonts.

## Local preview

From this folder, run `python -m http.server 4173`, then open `http://localhost:4173/`.

## Before sharing

Check the public email address, WhatsApp number, portrait, project descriptions, external project links, and permission to display screenshots. The only figure the site quotes is Diviniti's 40% Largest Contentful Paint improvement, labelled as reported. Every other project result describes what was built. Add numbers only when you can stand behind them.

## Site address

Canonical links, link-preview tags (`og:url`, `og:image`), `robots.txt`, and `sitemap.xml` use `https://website-swart-nu-54.vercel.app`. If you connect a custom domain, replace that address everywhere:

```
grep -rl 'website-swart-nu-54.vercel.app' . | xargs sed -i 's#https://website-swart-nu-54.vercel.app#https://your-domain.com#g'
```

WhatsApp and LinkedIn cache link previews, so a changed preview can take a while to appear. LinkedIn's Post Inspector refreshes it immediately.
