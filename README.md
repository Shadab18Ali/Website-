# Shadab Ali — client website

Standalone multipage website for prospective website clients. The HTML, CSS, JavaScript, images, and `api/contact.mjs` are all contained in this folder. No build step or npm install is required.

## Pages

- `index.html` — hero, expertise, selected clients, project slider, services, why work with me, testimonials (hidden until filled), process, technology, about and closing call to action
- `services.html` — the four services with their scope, and the FAQ
- `work.html` — project slider and a breakdown of each project (platform, problem, role, what I did, result, services)
- `case-diviniti.html` and `case-portrait-on-gold.html` — detailed case studies
- `about.html` — background, working directly together, technology and process
- `contact.html` — project request form (including budget and timeline) and direct contact options
- `thanks.html` — thank-you page shown after the contact form sends
- `404.html` — page-not-found page (Vercel serves it for missing URLs)

## Upload to GitHub and deploy on Vercel

1. Create a new GitHub repository for this client website.
2. Upload **the contents of this folder to the repository root**. `index.html`, `vercel.json`, `api/`, and `assets/` should all appear at the top level. If uploading the ZIP through GitHub's browser interface, extract it first.
3. In Vercel, choose **Add New → Project**, import that repository, and deploy with Framework Preset **Other**. Keep Root Directory at `./`, Output Directory at the project root (`.`), and leave Build Command empty. `vercel.json` also selects the Other preset.
4. For the contact form, create a Resend account and verify a sending domain. Add these Vercel Environment Variables for **Production** (and Preview if wanted): `RESEND_API_KEY`, `CONTACT_FROM_EMAIL` (for example `Shadab Ali <hello@your-verified-domain.com>`), and `CONTACT_TO_EMAIL` (your inbox). The API key stays in Vercel, never in GitHub. Redeploy after adding variables.
5. Send a real test request from the deployed `/contact.html` page and confirm it arrives at `CONTACT_TO_EMAIL`. Until those three variables and the verified sending address are set, the form shows an error and visitors can use the direct email or WhatsApp links.

Vercel's `/api/contact` function validates required fields, checks the hidden spam field, limits request size, and sends a plain-text inquiry email through Resend. The sender's address is set as the reply-to address. Local static previews prepare an email in the visitor's mail app because `python -m http.server` does not run Vercel Functions.

## How the styles and scripts fit together

Stylesheets load in this order, each refining the one before: `styles.css` (base layout, plus the self-hosted `@font-face` rules), `art-direction-v2.css` (current palette and page art direction), `motion.css`, `showcase.css`, the page-specific `case-study.css` or `contact-form.css`, and finally `components.css` (the conversion sections, accessible accent colours and mobile refinements).

- `script.js` — mobile menu, contact form, service pre-selection from `?service=`, testimonials preview.
- `motion.js` — hero image slider, reveal-on-scroll, scroll progress and back-to-top.
- `showcase.js` — project slider (arrows, thumbnails, swipe/drag) and the desktop cursor ring.

The header, navigation and footer are repeated in every HTML page. If you change one, change them all.

## Testimonials

The homepage has a testimonials section ready for 2–3 quotes. It ships **hidden** so placeholder text never reaches clients. Open `/index.html?preview` to see the layout with its placeholders. When you have real testimonials, follow the comment above the section in `index.html`: replace the text in a card, delete `data-placeholder` from it, delete unused cards, and remove `hidden` from the `<section>` tag.

## Images

Fonts live in `assets/fonts` (DM Sans and Space Grotesk, SIL Open Font License). Project screenshots come in several sizes: `name-desktop.webp` (full), `name-desktop-960.webp`, `name-mobile.webp`, `name-mobile-400.webp` and `name-thumb.webp` (128×106). If you replace a screenshot, replace every size of it, keeping the top of the page in frame, since each frame shows only the top of the screenshot. Images are cached by browsers for a day (`vercel.json`), so a replaced image can take up to a day to show for returning visitors.

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
