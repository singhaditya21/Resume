# Aditya Singh — Enterprise AI portfolio

This repository publishes a static, evidence-led portfolio for enterprise AI,
banking transformation, governed architecture and delivery leadership. GitHub
Pages serves the files directly from `main`; no framework build or runtime
service is required.

## Information architecture

- `index.html` is the recruiter- and executive-oriented portfolio entry point.
- `build-evidence.html` routes to presentation, architecture and code evidence.
- `case-study-library.html` preserves all 30 evidence-qualified case-study decks.
- `technical-projects.html` combines curated flagships with the complete
  technical-project index.
- `technical-concepts.html` preserves source-incomplete concepts with explicit
  evidence gaps rather than presenting them as implemented systems.
- `samples/technical-projects/<slug>/` holds each public technical brief,
  architecture pack and sanitized source download.
- `samples/presentations/` and `P Presentations/` contain customer-neutral
  samples and browser-friendly case-study evidence.
- `presentation-archive.html` keeps the complete authorized 16-set archive
  discoverable through release-backed downloads and a SHA-256 manifest.
- `assets/` contains shared public artwork, including the 1200 × 630 social card.

The social card keeps an editable SVG source and a committed PNG used by link
previews. On macOS, regenerate the raster after an SVG edit with:

```bash
sips -s format png assets/social-preview.svg --out assets/social-preview.png
```

## Preservation rule

**Published content is preserved.** Curation is implemented through navigation,
featured views, collection pages, filters, accordions and archive routes—not by
deleting projects, slides, diagrams, source packs or supporting evidence. Every
artifact should retain a clear route from a complete-library page.

Private source inputs are not published. Only reviewed, sanitized outputs belong
in the public technical library. Credentials, personal data, customer datasets,
deployment state and local filesystem paths must never be committed.

## Regenerating technical evidence

The technical portfolio generator treats the locally held, authorized project
archives as untrusted input. It selects allow-listed text files, redacts sensitive
material, creates architecture SVGs and emits the public project pages and ZIPs.
It never executes project code.

```bash
python3 scripts/build_technical_portfolio.py
```

Review the generated diff and the source-pack checksums before publication.

## Sitemap and local quality checks

The sitemap is derived from canonical URLs, so local working HTML without a
public canonical is never exposed automatically.

```bash
python3 scripts/generate_sitemap.py
python3 scripts/generate_sitemap.py --check
python3 scripts/site_qa.py
```

The dependency-free QA checks internal links and fragments, page landmarks,
skip links, H1 count, duplicate IDs, image alternatives, canonical/Open Graph/
Twitter/JSON-LD metadata, sitemap coverage, the social-card dimensions and
GitHub file-size limits. Assets above performance thresholds are reported as
warnings while GitHub-incompatible files fail the check.

The same checks run in `.github/workflows/site-qa.yml` for pull requests and
pushes to `main`.

## Publishing

GitHub Pages should be configured to deploy the repository root from `main`.
The `.nojekyll` marker keeps the static asset tree intact. After deployment,
verify the homepage, one technical detail page, one archive download, the
sitemap and an intentionally missing URL that exercises `404.html`. The
release-backed archive is part of the public information architecture: moving
large binaries out of the Pages tree must never remove their visible routes,
download links or checksum evidence.
