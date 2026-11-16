# Responsive and mobile-quality audit

* **Date:** 2026-11-16
* **Target:** `https://stmaryspaintingworks.pages.dev`, HEAD `404f6a3`
* **Method:** headless Chromium emulation at 19 viewport sizes, 200%/300% zoom, forced colors, dark mode, reduced motion, and text scaling; DOM geometry and screenshots in OS temp only.

## Evidence catalogue

### B1 — High zoom breaks the whole hero (Blocker)
- **Where:** 195×422 CSS px (200% of 390×844) and 130×281 (300%).
- **Observed:** `documentElement.scrollWidth` 246 vs client 195 at 200%, and 246 vs 130 at 300%. H1, hero sub, CTA row and photo are all 226.3px wide at x=20, extending 51.3px past a 195px viewport. Screenshot shows the headline clipped mid-word.
- **Cause:** `PHONE_DISPLAY` uses non-breaking spaces and Hero adds another `&nbsp;`; `.btn` min-content is 226.3px. The `1fr` hero grid track defaults to `min-width:auto`, so that button forces every sibling wider than the viewport.
- **Sources:** `src/data/site.ts:4`, `src/components/Hero.astro:30`, `src/styles/global.css:206-210,301-306,515-520`.

### B2 — Sticky WhatsApp CTA leaves the screen at high zoom (Blocker)
- **Where:** 195×422 and 130×281.
- **Observed:** `.sticky-bar a` uses `flex:1` with default `min-width:auto`. At 200% the WhatsApp link right edge is 195.7px (0.7px past); at 300% it is 195.7px against a 130px viewport, leaving only an icon and the letter W. Bar `scrollWidth` 184 vs `clientWidth` 106.
- **Cause:** no `min-width:0` on flex children and no narrow-width label strategy.
- **Sources:** `src/styles/global.css:955-988`.

### B3 — Header Call button leaves the screen at high zoom (Blocker)
- **Where:** 195×422 and 130×281.
- **Observed:** `.nav-call` right edge 199.8px at both; 4.8px past a 195px viewport and 69.8px past a 130px viewport. Header `scrollWidth` 200. Logo wraps to 4 lines (115.2px tall) at 200%.
- **Cause:** logo min-content 107.3px + Call 64.4px + 40px wrap padding never shrinks; no narrow-width header strategy.
- **Sources:** `src/styles/global.css:399-420,471-505`, `src/components/Header.astro:5-21`.

### M1 — Header wraps into two rows across 640–740px (Major)
- **Where:** every integer width 640 through 740; confirmed at 640×800, 653×280, 700×900.
- **Observed:** `.site-header` height 97px while `--header-h` is 64px. Logo height 67.2px on two lines. Five nav links occupy two rows, with Call orphaned on row two (`top=52px` vs other links `top=0`). Clean 65px row only at ≥741px; clean 77px row at ≤639px.
- **Cause:** full nav returns at 640px but does not fit until 741px; `.site-nav` wraps; logo has no `white-space:nowrap`; header height token is not updated.
- **Sources:** `src/styles/global.css:77,399-436,471-505`.

### M2 — Persistent CTA disappears while the hero is still stacked (Major)
- **Where:** 640–819px, especially short landscape 653×280.
- **Observed:** sticky bar `display:flex` at 639px, `display:none` at 640px. Hero remains single-column until 820px. At 653×280 the hero is 1234px tall and the WhatsApp button is at y=313–361, entirely below the fold; only Call is visible above the fold.
- **Cause:** sticky bar is hidden at 640px but the hero 2-column threshold is 820px. No intermediate breakpoint.
- **Sources:** `src/styles/global.css:522-526,955-1008`.

### M3 — Hero photo and hero section are oversized (Major)
- **Where:** all phone widths, worse at 640–819px.
- **Observed:** at 360px the hero is ~983px; at 768px it is 1400px with a 970.7px photo; at 820px it drops to 578px. The 3:4 portrait image has no height cap.
- **Cause:** `.hero-grid` is single column below 820px; `.hero-photo img` uses `width:100%;height:100%;object-fit:cover` with no max-height and grid track `min-width:auto`.
- **Sources:** `src/styles/global.css:507-563`, `src/components/Hero.astro:54-72`.

### M4 — Section anchors land too low on phones (Major)
- **Where:** 320×568, 390×844, 430×932.
- **Observed:** `section.scroll-margin-top` computes to 89px while `.site-header` is `position:static`; `#gallery.top` after anchor jump is 88.5–89.3px. Combined with 56px section padding, roughly 145px of dead space precedes content.
- **Cause:** scroll-margin reserved for a sticky header, but mobile header is static.
- **Sources:** `src/styles/global.css:211-215,471-478`.

### M5 — Manifest cannot install as a standalone app (Major)
- **Where:** all phones.
- **Observed:** `manifest.display = "browser"`; zero service-worker registrations; no `apple-mobile-web-app-capable`; no standalone display mode. Icons and theme-color are present.
- **Cause:** install metadata incomplete. Offline is a documented non-goal, but standalone display is metadata-only.
- **Sources:** `public/manifest.webmanifest:5`, `src/layouts/Base.astro:59-81`.

### M6 — No section navigation in thumb zone (Major)
- **Where:** all phones <640px.
- **Observed:** header hides all anchors; sticky bar contains only Call and WhatsApp. Page height is 14,052–16,176px (25–29 screens). Footer navigation is at the very end.
- **Cause:** persistent bottom area carries no section links.
- **Sources:** `src/styles/global.css:471-505,955-998`, `src/components/StickyBar.astro`, `src/components/Footer.astro`.

### m1 — Brand wraps on 280/320px phones (Minor)
- **Observed:** logo text wraps to two lines, with orphan word "Works" at 320px; height 57.6px vs 44px at ≥360px.
- **Sources:** `src/styles/global.css:407-420,486-488`.

### m2 — Sticky bar hides hero meta on short phones (Minor)
- **Observed:** at 320×568, bar occupies y=488–556; hero hours/area text y=500–571 behind the opaque bar.
- **Sources:** `src/styles/global.css:955-968`.

### m3 — Ragged CTA pills at 400–428px (Minor)
- **Observed:** full-width rule ends at 399px; buttons total 414.7px and wrap to two unequal left-aligned pills at 400–428px.
- **Sources:** `src/styles/global.css:1012-1020`.

### m4 — Hero image srcset lies between 640 and 819px (Minor)
- **Observed:** `sizes="(max-width: 639px) 92vw, 560px"` but the image renders up to ~780px wide in the single-column band, so a 720w source is upscaled.
- **Sources:** `src/components/Hero.astro:62`, `src/styles/global.css:522-526`.

### m5 — Safe-area side insets ignored (Minor)
- **Observed:** `viewport-fit=cover` is set, but `.wrap` and `.sticky-bar` use fixed 20px/12px horizontal padding with no `env(safe-area-inset-left/right)`.
- **Sources:** `src/layouts/Base.astro:59`, `src/styles/global.css:206-210,955-960`.

### m6 — Forced-colors service icons invisible (Minor)
- **Observed:** `.service-icon` gradient is stripped in forced-colors light mode while SVG stroke remains white on white.
- **Sources:** `src/styles/global.css:638-657`.

### m7 — Text-only scaling has no effect and clips phone at 2× (Minor)
- **Observed:** root font-size 200% does not change body text because all sizes are px; doubling computed font sizes clips the contact Call button by 10px.
- **Sources:** `src/styles/global.css:123-130,301-306`, `src/data/site.ts:4`.

### m8 — Floating bar covers content mid-scroll (Minor)
- **Observed:** opaque bar with 12px gutters covers the bottom of cards and captions; only footer reserves 104px.
- **Sources:** `src/styles/global.css:901,955-968`.

## Root causes

1. Breakpoints are scattered at 480/640/820/1000 with an unhandled 640–819px band.
2. Flex items keep `min-width:auto`, so unbreakable phone text expands grids at high zoom.
3. Header height token and actual height diverge when nav wraps.
4. Mobile scroll margin assumes a sticky header.
5. PWA install metadata is incomplete.
6. Bottom navigation offers no section routing.

## Fix plan (approved after refutation)

All findings were independently refuted and survived. The following changes are in scope:

1. **Unify the responsive system around 640px and 880px.** Below 880px use the compact header and a docked bottom navigation bar. At 880px and above use the full header and hide the bottom bar. The hero becomes two-column from 640px, removing the 640–819px dead zone.
2. **Make every flex/grid child shrinkable** with `min-width:0`, `minmax(0,1fr)`, and wrappable phone text so 200%/300% zoom cannot force horizontal overflow. Use short logo text and icon-only controls at extremely narrow widths.
3. **Cap the hero image** with a 4:3 frame and a `min(52vh,420px)` limit; include short-height landscape behavior. Keep captions and images intact.
4. **Dock the bottom bar edge to edge** with the existing Call and WhatsApp CTAs preserved in the thumb zone, plus a second compact row or icon rail of four section links above them. Use safe-area padding, 44px targets, and matching body/footer clearance. Do not move CTAs into the header.
5. **Reset mobile anchor offset** because the header is static below 880px; keep the offset only when a sticky header is present.
6. **Set manifest `display:standalone`** and add Apple standalone metadata. No service worker or client JS is added.
7. **Fix accessibility edge cases:** forced-colors service icons, `rem` text scaling, ragged CTA widths, srcset sizing, and horizontal safe-area insets.

## Verification criteria for fixes

- No horizontal overflow and no clipped Call/WhatsApp controls at 130, 195, 280, 320, 360, 390, 414, 428, 640, 653, 768, 820, 1024 and 1920 CSS px.
- Header single row at every width from 130 to 1920, or a deliberate compact two-row pattern that updates the reserved height.
- Persistent Call and WhatsApp controls available at every width and height, including 653×280 and 300% zoom.
- Hero no taller than ~1.4 viewport heights on phones and ~1.0 on tablets; no upscaled images.
- Anchor jumps show section headings near the top with no dead band.
- Manifest reports `standalone`, iOS capable meta present, no client JS added.
- Any section reachable from the bottom bar in one tap.
- All colors still meet WCAG AA in normal, forced, and dark modes; all touch targets ≥44px; all project gates remain green.
