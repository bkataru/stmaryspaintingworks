# St. Mary’s Painting Works

Static one-page lead generator for a painter in Ulsoor, Bangalore. Built with
Astro, with no forms, prices, booking, backend, client JavaScript or trackers.
A phone call or a WhatsApp message is the only way to get in touch. Maintainer:
bkataru.

The site is hosted on Cloudflare Pages at
<https://stmaryspaintingworks.pages.dev>. That origin is the canonical `site`
in `astro.config.mjs` and drives the canonical tag, JSON-LD `url`, sitemap and
Open Graph image.

## Prerequisites

- Node >= 18, npm >= 9
- Python 3 with Pillow (`PIL`) for the image and brand-asset scripts
- Wrangler, used on demand through `npx` for deployment (no global install needed)

## Build and deploy

```sh
npm install
npm run build
npx wrangler pages deploy ./dist --project-name stmaryspaintingworks
```

`npm run build` writes the static site to `dist/`. The deploy command uploads
that directory directly to the Cloudflare Pages project
`stmaryspaintingworks`; there is no Git integration or preview URL step. Run
every quality gate below before deploying.

### Rollback

Rollback means redeploying a prior Cloudflare deployment. In the Cloudflare
Pages dashboard, open the project's deployment history, choose a known-good
deployment and redeploy it. Because deployment is a direct upload from `dist/`,
you can also rebuild from a known-good commit and upload that `dist/` again.

## Quality gates

All nine must pass before a publish.

| Gate | Command | Pass criteria |
| --- | --- | --- |
| Build | `npm run build` | Exits 0; `dist/` is produced. |
| Type and template check | `npm run check` | Exits 0; no Astro or TypeScript errors. |
| HTML rules | `npm run lint:html` | Exits 0; no htmlhint errors. |
| HTML5 conformance | `npm run validate:html` | Exits 0; no html-validate errors. |
| CSS rules | `npm run lint:css` | Exits 0; no stylelint errors. |
| Formatting | `npx prettier --check "src/**/*.{astro,ts,css}"` | Exits 0; no unformatted files. |
| Weight and freshness budget | `npm run lint:weight` (runs `python scripts/check-weight.py`) | First view <= 250 KiB / 256,000 bytes (HTML + CSS + preloaded fonts + hero WebP); every image <= 150 KB; every clip <= 3 MB; every gallery entry has a JPEG plus four WebP rungs; no stray WebP in `public/gallery/`. |
| Brand whitelist | `npm run check:brand` (runs `python scripts/check-brand.py`) | Exits 0; no legacy brand strings and no unwhitelisted name variants remain. |
| Contact links | Count `tel:` and `wa.me` in `dist/index.html` | At least 7 `tel:` links and at least 11 `wa.me` links. |

Tooling installed for these: `htmlhint`, `html-validate`, `stylelint` with
`stylelint-config-standard`, and `prettier` with `prettier-plugin-astro`.
`.prettierignore` keeps vendored skills, source assets, generated output and
`dist/` out of formatting.

After a deploy, confirm the live site returns HTTP 200 on `/`, that
`robots.txt` and `llms.txt` are served, that the canonical and sitemap point at
the Pages origin, and that the rendered HTML carries the new wordmark.

## Editing content

All facts live in `src/data/site.ts`: phone, hours, address, map URL, service
groups with their WhatsApp prefill text, gallery list, clip list and
`LAST_VERIFIED`. Components import these values and do not hard-code them. Edit
one value, rebuild and redeploy. Captions must describe what is visible in the
photo. Phone and WhatsApp links may not be removed from any section.

The files in `public/` that cannot import from `site.ts` are edited by hand:
`404.html`, `manifest.webmanifest`, `llms.txt`, `robots.txt` and `sitemap.xml`.
Keep their brand strings, the canonical origin and the contact links in sync
with `site.ts`.

## Regenerating WebP variants

`python scripts/make-webp.py` rebuilds `public/gallery-webp/` from the JPEGs in
`public/gallery/`. Each gallery JPEG produces a full-size WebP plus a
320/480/720 px width ladder (`<slug>-320.webp`, `<slug>-480.webp`,
`<slug>-720.webp`, aspect preserved). The ladder rungs feed the `srcset` and
`sizes` on grid tiles, featured images and the hero, with the JPEG as the
`<img src>` fallback. WebP is used unconditionally through `<source>`; the
script aborts on a 0-byte variant. Never place a `.webp` file in
`public/gallery/` — the weight check fails on strays there.

## Regenerating brand assets

`python scripts/make-brand-assets.py` derives the site's icons and social image
from the logo. It writes `public/favicon.svg`, `public/apple-touch-icon.png`
(180x180), `public/icon-192.png`, `public/icon-512.png` and `public/og.jpg`
(1200x630, kept under 200 KB). Run it whenever the logo or the brand marks
change, then rebuild.

## Adding a photo

1. Compress to 150 KB or less (longest side 1200 px, JPEG quality ~72).
2. Drop the JPEG into `public/gallery/` with a plain slug name.
3. Add its `{ file, caption, width, height }` entry to `GALLERY` in
   `src/data/site.ts`, with an accurate caption.
4. Run `python scripts/make-webp.py` to rebuild `public/gallery-webp/`.
5. Rebuild and run the weight check.

## Notes

- The short wordmark is `St. Mary’s Painting Works`; the full legal name is
  `St. Mary’s Painting Works & Home Repairs`.
- The site states "Since 1980" and publishes no other years figure.
- No forms, prices, booking, payments, CMS, backend, login or trackers.
