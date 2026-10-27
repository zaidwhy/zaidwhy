# Profile handoff - 2026-10-28

## State
- README is a field survey: `assets/core-sample.svg` (nightly, `scripts/core_sample.py`), then six plates from `scripts/plates.py` (route, specimens, faults, assays, excavation, fieldwork, seal). Facts on the plates are copied from README sections; change both or neither.
- Twelve public repos carry `.github/plate.svg` from `scripts/repo_plates.py` plus a survey footer. Those plates are static and say "taken <date>".
- Tests: `python -m unittest discover -s scripts -p "test_*.py"` (8 tests, offline). The nightly Action runs them and redraws the core sample only on green; neither step can block the activity commit.

## Decisions taken while Zaid was asleep (reverse any of them freely)
- AFTERSHOCK and flake-laundering did not get a repo plate: other sessions were editing them on 2026-10-28. Run `python scripts/repo_plates.py <out> aftershock` after adding both to `REPOS`, then copy to each repo's `.github/plate.svg`.
- Archived repos (aura-private-ai-memory, receipts-dev) were left untouched.
- PROVENANCE.md (signed) still says the SVGs are "hand-authored". The plates are drawn by scripts in this repo and carry the manifest in `<metadata>`. Re-signing is Zaid's call; the README already states how the plates are drawn.
- The old neon assets (hero, terminal, roadmap, failure-ledger, kernel-map, chain-of-custody, coldread-curves, augur-drift, flake-laundering) are no longer referenced but were kept in `assets/`.

## Next
- Re-run `repo_plates.py` monthly, or when a repo's headline numbers change, so the strips do not go stale.
- Zaid: upload `weekend-profile-update/creative/banner-core.png` as the LinkedIn background.
