# St. Mary's Painting Works & Home Repairs — rebrand, redesign and hosting migration

* **Author:** bkataru
* **Date:** 2026-11-16

## Overview

The existing site is a one-page lead generator for a painter in Ulsoor, Bangalore. It earns calls through phone and WhatsApp links only. The owner, publicly called Jay, no longer wants the old "Jay Painters" business name used. His Google Business Profile was created today under the name "St. Mary's Painting Works & Home Repairs", taken from a name he used early in his career. The website, GitHub repository and hosting must be brought in line with that name, and the whole site must be redesigned around the new logo.

The site stays a static Astro build with no forms, prices, booking, backend, client JavaScript or trackers. A call or a WhatsApp message is the only way to contact the business.

## Analysis (critique first)

### 1. Surge blocks indexing completely
Surge force-serves `User-agent: * Disallow: /` on all `*.surge.sh` subdomains. Our robots file never reaches crawlers. Cloudflare Pages serves `robots.txt`, `sitemap.xml` and `llms.txt` correctly on `*.pages.dev`, and preview deployments get `X-Robots-Tag: noindex` automatically. Moving to `stmaryspaintingworks.pages.dev` fixes indexing without buying a domain.

### 2. A partial rebrand would be worse than none
"Jay" appears in about 20 places: WhatsApp prefills in seven components, schema name, `og:site_name`, SEO title, header and footer wordmarks, `llms.txt`, repo name and URLs. Changing only the visible heading leaves stale brand strings in metadata and messages, which confuses both people and crawlers. Every brand reference must change in one pass from `src/data/site.ts`.

### 3. The new services are a deliberate scope expansion
The Google listing names work the old site never offered: home repairs, roof leakage fixing, patch work, tiling, plumbing, electricals, Asian and MRF PU polishing, Deco Paints and outside structure work. These must appear on the site if Google, JustDial and the site are to agree. No prices or localities may be invented for them.

### 4. The Google Sunday hours are a form artifact
The Google listing says Sunday Closed because its form cannot express occasional Sunday work. The real schedule is 7 AM to 9 PM every day. The site states the real schedule; the Google entry stays as the owner set it.

### 5. The logo is an accent, not the primary mark
The logo is a detailed blue-and-gold portrait of Mary with a halo. The owner chose a text wordmark with the logo as a smaller accent beside it. Its colors drive the new palette: deep blue, gold, light neutral surfaces. The warm orange palette is removed.

### 6. One phone number is still the whole business
Personal number equals business number. No form is wanted, so the call and WhatsApp paths must work everywhere: header, hero, services, gallery, steps, clips, contact, sticky bar and 404. Prefilled WhatsApp text must use the new brand name and stay short enough for a phone.

### 7. Legacy files are debt
The old design draft, review reports, JustDial HTML dump and Surge deployment notes describe a brand and host that no longer exist. Keeping them invites stale instructions. They are deleted; the README and this brief are rewritten.

## Confirmed facts

- **Canonical business name:** St. Mary's Painting Works & Home Repairs
- **Short display name:** St. Mary's Painting Works
- **Wordmark:** a text wordmark, with the logo used as a smaller accent beside it. The logo is not the primary mark.
- **Founding year:** 1980. This is correct and stays everywhere. JustDial displays "47 Years in Business", an artifact of its own counting; 1980 to 2026 is 46 elapsed years. The site says only "Since 1980" and never reproduces the JustDial figure.
- **Owner:** Jay in all public copy. His legal name and `jaypainterscontractors@gmail.com` cannot change and are not used as branding.
- **Phone:** +91 97316 70742. WhatsApp uses the same number.
- **Address:** #21, Gauthamapuram, Near Football Ground, R H A Penchine Line, Ulsoor, Bangalore-560008, Karnataka. The Google listing renders the same place as 21, R H A, Penchine Line, near Football Ground, Halasuru, Gowthamapuram, Bengaluru, Karnataka 560008.
- **Opening hours:** 7 AM to 9 PM, all seven days. The Google listing says Sunday Closed only because its form cannot express "open on Sundays when work requires it". The website states the real schedule.
- **Service area:** work across Bangalore is confirmed. Jay and his crews will coordinate and travel to other cities such as Hyderabad or Chennai when needed. This is an owner-confirmed exception to the "no invented localities" rule; it is stated once in public copy, in `llms.txt`, and JSON-LD `areaServed` is exactly `["Ulsoor", "Bangalore", "India"]`.
- **Google Business Profile:** category Painter. Description: "Painting works, Home repairs, Roof leakage fixing, any patch works, tiling, plumbing, electricals, Asian PU polishing, MRF PU polishing, Deco Paints, Outside Structure Work". Media: one new photo of a painter on a scaffold.
- **JustDial:** the listing was renamed to "St. Mary's Jay Painters & Home Repairs" because JustDial requires the old name to appear as a substring of the new one. Its URL changed to `/Bangalore/St-Marys-Jay-Painters-Home-Repairs-Near-Football-Ground-Ulsoor/080PXX80-XX80-261007120204-I2A4_BZDET`. Only the numeric listing ID is stable.
- **Logo:** `assets/logo.png`, a blue-and-gold portrait of Mary with a gold halo. It drives the new palette.
- **New media:** two photos arrived. Keep the painter on a scaffold. Delete the terrace and wall close-up; it was sent by mistake and is not on Google.

## What the site must do

- Use the new name in the title, meta description, headings, header, footer, JSON-LD, Open Graph, `llms.txt` and every WhatsApp prefill. Remove "Jay Painters" as a brand reference. Keep the owner's legal name and email as they are.
- Add the service lines named in the Google description: home repairs, roof leakage fixing, patch work, tiling, plumbing, electricals, Asian PU polishing, MRF PU polishing, Deco Paints and outside structure work. This is an intentional expansion of scope.
- Redesign the structure, style, presentation and content. Replace the warm orange palette with blue and gold taken from the logo. Keep the phone-first, low-bandwidth, 360px no-scroll constraints.
- Use the scaffold photo in the gallery. Remove the terrace close-up from source assets.
- Derive the favicon, apple-touch icon, 192 and 512 pixel icons and the Open Graph image from the logo.
- Publish at `stmaryspaintingworks.pages.dev` on Cloudflare Pages. There is no `jaypainters.pages.dev`.
- Rename the GitHub repository from `bkataru/jaypainters` to `bkataru/stmaryspaintingworks`, update its description and topic, and update the local remote.
- Retire and delete `jaypainters.surge.sh`.
- Delete legacy design documents, review reports and the JustDial HTML dump. Do not carry them forward. Rewrite the README for the new name and host.
- Keep all quality gates green: build, `astro check`, HTML lint and validation, CSS lint, Prettier, weight budget and link counts.

## Goals vs. Non-Goals

* **In-scope goals:** rebrand every public string; redesign palette, layout and content; add the Google-listing services; add the scaffold photo; derive logo assets; move hosting to Cloudflare Pages; rename the repository; remove Surge; delete legacy docs; keep all verification green.
* **Out-of-scope non-goals:** buying a custom domain; a Kannada or any other translated route; forms, prices, booking, payments, a CMS, a backend, login or trackers; changing the phone number, owner name, email, address or founding year; inventing localities, rates, review counts or claims.

## Alternatives Weighed

- **Keep Surge.sh and buy a custom domain.** Rejected by the author: extra annual cost, and Surge force-serves `Disallow: /` on its own subdomains, so the site cannot be indexed there.
- **Publish at `jaypainters.pages.dev` first, then move.** Rejected by the author: the "jay" name is unwanted. Only `stmaryspaintingworks.pages.dev` will exist.
- **Use the logo as the main header and hero mark.** Rejected by the author: a small accent beside a text wordmark fits a phone-first lead generator better.
- **Keep "Since 1980" out of the new brand.** Rejected by the author: 1980 is the correct founding year.
- **Vercel or GitHub Pages.** Rejected: Vercel Hobby does not allow commercial sites, and GitHub Pages terms discourage running a business on it and have sitemap fetch problems on `*.github.io`.
- **Carry the old design documents and review reports forward.** Rejected by the author: legacy debt. Delete them.

## Locked implementation decisions (resolves reviewer objections)

**Names and strings.** The wordmark reads `St. Mary's Painting Works` with a curly apostrophe. The full legal name `St. Mary's Painting Works & Home Repairs` appears in the JSON-LD `name`, `og:title`, the contact section and `llms.txt`. The short name appears in the header, footer, sticky bar and title suffix. "Since 1980" is the only years claim. Never print "47 years" — 1980 to 2026 is 46; JustDial's figure is not copied. Every WhatsApp prefill starts `Hi St. Mary’s Painting Works,` (curly apostrophe, full short name) and keeps the existing `____` placeholder and per-section intent. Static `public/404.html`, `public/manifest.webmanifest`, `public/llms.txt`, `public/robots.txt`, `public/sitemap.xml` are hand-edited; they cannot import from `site.ts`.

**JustDial exception.** The string `St-Marys-Jay-Painters-Home-Repairs` in the JustDial URL, and the listing name `St. Mary's Jay Painters & Home Repairs` where quoted, are the only permitted "Jay" survivors alongside the owner's name and email. A brand check greps the repo and expects exactly that whitelist.

**Palette (hex values from the logo, all pairs measured AA).** Deep navy `#0B1F3A` for text and dark sections; logo blue `#012B7E` for primary buttons; mid blue `#0A4FA8` for hover and links; gold `#F0A010` for rules, badges, focus rings and accent surfaces; light surface `#F7F9FC`; white cards `#FFFFFF`; muted text `#42526B`. Contrast: navy on light 15.66, white on primary blue 12.74, white on mid blue 7.79, navy on gold 7.66, muted on light 7.51. Call buttons use primary blue. WhatsApp buttons use mid blue, not green, so the two actions stay distinct and both stay inside the logo palette. Stylelint does not check contrast, so these values are fixed here and not improvised in components.

**Logo assets.** `assets/logo.png` is committed. A PIL script `scripts/make-brand-assets.py` produces: `public/favicon.svg` (a simple navy tile with a gold halo ring and the letter "S", legible at 16 px — the portrait itself is not shrunk to icon size); `public/apple-touch-icon.png` 180×180; `public/icon-192.png` and `public/icon-512.png` with the same mark on navy; `public/og.jpg` 1200×630 with the logo, the short name and "Ulsoor, Bangalore · Since 1980" on navy, under 200 KB. `og:image:alt` becomes descriptive of that image and carries no old brand name. The inline data-URI favicon in `Base.astro` is removed.

**Media.** Only the two new photos in `assets/originals/` are affected: delete `WhatsApp Image 2026-11-16 at 5.01.29 PM.jpeg`; keep `WhatsApp Image 2026-11-16 at 5.01.29 PM (1).jpeg`, resize to longest side 1200 and ≤150 KB, save as `public/gallery/local-scaffold-painter-01.jpg`, add one `GALLERY` entry with an accurate caption, then run `scripts/make-webp.py` to build its four WebP rungs. Existing gallery and clip entries stay. `scripts/check-weight.py` is updated so its hero measurement reads the `hero: true` entry from `site.ts` instead of a retired filename.

**Services.** Keep the five existing `SERVICE_GROUPS` and their structure. Merge the genuinely new Google items into them: Home interiors gains "Home repairs", "Patch work", "Tiling", "Plumbing", "Electricals"; Outside and waterproof gains "Roof leakage fixing" and "Outside structure work"; Decorative gains "Deco Paints"; Wood and polish becomes "Wood, PU and polish" with "Asian PU polishing" and "MRF PU polishing". Keep 3D, texture, spray and statue work where they are. Drop `priceRange` from JSON-LD; no prices are published.

**Host files.** Delete `public/CNAME` (Surge-only). Update `astro.config.mjs` `site` to `https://stmaryspaintingworks.pages.dev`; `public/robots.txt` Sitemap line, `public/sitemap.xml` loc, and all `public/llms.txt` URLs to the same origin. Deploy by direct upload: `npx wrangler pages deploy ./dist --project-name stmaryspaintingworks`. No Git integration, so the repo rename cannot break the webhook. Record build command `npm run build`, output `dist`, and rollback as redeploying a prior Cloudflare deployment. Tag the pre-migration commit before any destructive step.

**Deletion list.** `docs/design_draft.md`, `docs/designs/`, `docs/reviews/` and the top-level `justdial/` dump are deleted. `docs/concepts_brief.md` stays as the single brief. `assets/originals/`, `assets/gallery-locked/`, `assets/justdial/`, `assets/video/`, `assets/posters/` stay as source inputs with provenance. `dist/`, `node_modules/`, `.astro/` stay ignored.

**Gates.** `npm run build`, `npm run check`, `npm run lint:html`, `npm run validate:html`, `npm run lint:css`, `npx prettier --check "src/**/*.{astro,ts,css}"`, `python scripts/check-weight.py`, a repo-wide brand grep against the whitelist, and counts of `tel:` and `wa.me` links in `dist/index.html` at or above the current 7 and 11. Live acceptance: HTTP 200 on `/`, served robots and llms, canonical and sitemap on `pages.dev`, new wordmark in HTML, no `surge.sh` or unwhitelisted `Jay` in `dist/`.

**GitHub.** `gh repo rename stmaryspaintingworks --repo bkataru/jaypainters`, then `gh repo edit bkataru/stmaryspaintingworks --description "Static lead-gen site for St. Mary's Painting Works & Home Repairs, Ulsoor Bangalore painters since 1980. Astro, phone/WhatsApp CTAs, hosted on Cloudflare Pages." --add-topic astro --add-topic static-site`, then `git remote set-url origin https://github.com/bkataru/stmaryspaintingworks.git`. Rename `package.json` `name` to `stmaryspaintingworks`.

**Ordering.** Tag, build all assets and content, run all gates, deploy to Cloudflare, verify live, rename GitHub, tear down `jaypainters.surge.sh` with `npx surge teardown jaypainters.surge.sh` under the existing account, commit and push last. No destructive step happens before live verification.

## Key Decisions & Staging for Next Steps

1. Freeze the name, facts, service list and locked decisions above. Components import every string from `src/data/site.ts`; the six static `public/` files are edited by hand and verified by grep.
2. Generate the blue-and-gold brand assets with `scripts/make-brand-assets.py` and apply the fixed hex values to `global.css`, `site.ts`, `manifest.webmanifest` and `404.html`.
3. Prepare media: delete the bad photo, add the scaffold photo with its WebP ladder, fix the hero measurement in the weight script.
4. Rewrite components and content, then host files, then delete legacy files.
5. Run all gates, tag, deploy to Cloudflare Pages, verify the live page, rename the repository, tear down Surge, commit and push.
