# Profile handoff - 2026-10-30

## State
- The page is **Neo-Kyoto** (e8769a8): the header is a film, `assets/neokyoto-hero.webp` (1440 px, 24 fps, 12.6 MB), with `assets/neokyoto-hero-phone.webp` (600 px pagoda close-up) served under 600 px through `<picture>`. The scene and its capture script are in `scripts/neokyoto/`; the hero is the kept 1800 px frames encoded at 1440 px, quality 80.
- The seven plates shown (roadmap, failure-ledger, flake-laundering, coldread-curves, augur-drift, kernel-map, chain-of-custody) are hand-authored SVG restyled into the film's palette with Geist Mono embedded; data and positions unchanged. The restyle script and the design history live in the private repo zaidwhy/weekend-profile-update (creative/round15).
- `PROVENANCE.sig.txt` re-signed 2026-10-30 (088ba1b) to cover the film and the restyled plates; it verifies from raw.githubusercontent.
- The nightly workflow updates the ACTIVITY and STATUS blocks and runs the plate tests; the core-sample redraw was retired (c644825), and a manual run was green on every step.
- Tests: `python -m unittest discover -s scripts -p "test_*.py"` (17, offline, all pass). The plate-facts test checks only plates the README shows.
- Kept but not shown: the survey plates (core-sample, plate-*.svg), nameplate.svg, hero.svg, terminal.svg.

## Watch
- raw.githubusercontent serves the 12.6 MB hero as application/octet-stream (nosniff) while the 7.7 MB phone file is image/webp. Chromium renders both; Firefox and desktop Safari were not tested. If the hero shows blank there, re-encode it under about 8 MB.
- An auto-commit hook commits every editor save in this repo; fold those into one signed commit before pushing.

## Next
Nothing open.
