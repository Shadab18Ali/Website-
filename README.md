# Shadab Ali — client website

Standalone multipage website for prospective website clients. The HTML, CSS, JavaScript, images, and `api/contact.mjs` are all contained in this folder. No build step or npm install is required.

## Pages

- `index.html` — introduction, image slider, selected projects
- `services.html` — services and FAQ
- `work.html` — project gallery
- `case-diviniti.html` and `case-portrait-on-gold.html` — detailed case studies
- `about.html` — background and process
- `contact.html` — project request form and direct contact options
- `thanks.html` — thank-you page shown after the contact form sends
- `404.html` — page-not-found page (Vercel serves it for missing URLs)

## Upload to GitHub and deploy on Vercel

1. Create a new GitHub repository for this client website.
2. Upload **the contents of this folder to the repository root**. `index.html`, `vercel.json`, `api/`, and `assets/` should all appear at the top level. If uploading the ZIP through GitHub's browser interface, extract it first.
3. In Vercel, choose **Add New → Project**, import that repository, and deploy with Framework Preset **Other**. Keep Root Directory at `./`, Output Directory at the project root (`.`), and leave Build Command empty. `vercel.json` also selects the Other preset.
4. For the contact form, create a Resend account and verify a sending domain. Add these Vercel Environment Variables for **Production** (and Preview if wanted): `RESEND_API_KEY`, `CONTACT_FROM_EMAIL` (for example `Shadab Ali <hello@your-verified-domain.com>`), and `CONTACT_TO_EMAIL` (your inbox). The API key stays in Vercel, never in GitHub. Redeploy after adding variables.
5. Send a real test request from the deployed `/contact.html` page and confirm it arrives at `CONTACT_TO_EMAIL`. Until those three variables and the verified sending address are set, the form shows an error and visitors can use the direct email or WhatsApp links.

Vercel's `/api/contact` function validates required fields, checks the hidden spam field, limits request size, and sends a plain-text inquiry email through Resend. The sender's address is set as the reply-to address. Local static previews prepare an email in the visitor's mail app because `python -m http.server` does not run Vercel Functions.

## Local preview

From this folder, run `python -m http.server 4173`, then open `http://localhost:4173/`.

## Before sharing

Check the public email address, WhatsApp number, portrait, project descriptions, external project links, and permission to display screenshots. The case studies describe what was built and leave out performance or order-reduction figures; add those back only with numbers you can stand behind.

## Site address

Canonical links, link-preview tags (`og:url`, `og:image`), `robots.txt`, and `sitemap.xml` use `https://website-swart-nu-54.vercel.app`. If you connect a custom domain, replace that address everywhere:

```
grep -rl 'website-swart-nu-54.vercel.app' . | xargs sed -i 's#https://website-swart-nu-54.vercel.app#https://your-domain.com#g'
```

WhatsApp and LinkedIn cache link previews, so a changed preview can take a while to appear. LinkedIn's Post Inspector refreshes it immediately.
