# ShiroKin Studio — Game Showcase V2

Conversion-first single-page redesign. Retains the black/gold wordmark and League Spartan brand typography.

## Source
- index.html — semantic and responsive storefront; Area 81 is first, Guild Master second, Biome Bites marked in development (no broken store link).
- style.css — mobile-first compact game layout, accessible sizing and reduced effects.
- script.js — optional GA4 click-event hook (no analytics data is sent unless GA4 is configured).
- scripts/optimize_images.py — locally generate WebP derivatives from existing repo PNG assets.
- .github/workflows/optimize-assets.yml — build optimized assets on feature branch; check if GitHub Actions has write access.

## Test
- 320, 375, 390, 768, 1366, 1920 widths: inspect in real browser.
- Use Google Lighthouse Mobile to check LCP, layout shifts and page-size transfer.
- Verify all active store links on device; test mobile browser and 125% scale.
- Keep existing CNAME, app-ads.txt and verification files untouched.

## Important
`assets/optimized/*.webp` are generated files and must exist before the HTML is deployed to `main`. `area81-bg.png` etc. are the original art and can be kept in repo for future editing; WebP is used in visible image surfaces. This site uses static HTML/CSS and works on GitHub Pages.

## Automated screenshot test
Run `python scripts/test_site.py` after `pip install playwright` and `playwright install chromium`; GitHub Actions runs this automatically for 320, 375, 390, 768, 1366 and 1920px and saves screenshots as artifacts.