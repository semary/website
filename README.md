# Mohamed Sameer portfolio

A static HTML portfolio deployed by Netlify. No framework, build step, external font service, or runtime package dependencies.

## Local review

```sh
python3 scripts/check_site.py
python3 -m http.server 8765
```

Open `http://localhost:8765/` for the site. Open `/scripts/responsive.html` locally or on a Netlify deploy preview to inspect 320, 390, and 768 pixel layouts. The review page is excluded from indexing.

## Content updates

Treat the current `index.html` portfolio as the editorial source for `llms.txt`. Keep product scope, metric labels, periods, and qualifications aligned whenever either changes. The six banking products exclude the separate food-delivery and AI-interview projects. Identified opportunities are not realised revenue; Q1-to-Q4 growth is not year-over-year growth. Career figures are self-reported.

Run `python3 scripts/check_site.py` after changes. It checks the specific profile consistency rules, local links, anchor targets, image metadata, and JSON-LD. This is not a substitute for visual review or independent verification of career claims.

## Performance and accessibility

The page uses system fonts and a preloaded 56 KB WebP portrait. All content and the native mobile menu work without JavaScript. A small enhancement closes the menu on link selection or Escape. Google Tag Manager remains as configured; third-party tags can affect real-world performance. `_headers` sets conservative caching for images and always revalidates `llms.txt`.
