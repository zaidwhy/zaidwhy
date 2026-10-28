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

## Refine log
- Round 4 (performance): core-sample.svg drew each bed outline three times (tint, hatching, boundary line). Each outline is now defined once and drawn twice by `<use>`, with the stroke drawing the boundary: 177 KB to 93 KB, pixel diff 0.76% (the count and date text). A size-budget test (36 months under 130 KB) guards it.

- Round 5 (renderers without CSS animation): the fade-in elements had `opacity:0` as their base style, so converters and thumbnailers drew them blank: 5.7% of the seal plate and 5.0% of the specimens plate went missing in a Chromium render with `animation:none` forced. The animation now starts from transparent instead, and every plate loses 0.00% with animation off. A test rejects any base `opacity:0` rule.

- Round 6 (facts): a test now renders the plates and requires every number on them to appear in the README outside the bot blocks and dates. It was checked by planting three wrong numbers (27 to 28, 13.4k to 13.5k, 188 to 189); each one failed the test. The first real run caught two plate facts with no written source: the reader model names behind 50/800/1600 words, and AUGUR's 39 and 80 year gaps. Both had only been stated in the alt text of the charts the plates replaced. They are now stated in the Assays section.

- Round 7 (scan never clean): the craft-guard scan of README.md always reported one finding, from the bot-written status list. `update_telemetry.py` now writes the status as a table and also checks AFTERSHOCK, which the README claims is live. The "More systems" list became a table as well. The scan reports 0 findings for the first time. Another session corrected personal-llm to 181 offline tests and the fleet to 356 (commit 6e95d98) and regenerated the plates; the round-6 fact test passes against those numbers.

- Round 8 (full flow, stranger read): 10 tests pass, and the telemetry, core sample, 7 plates and 12 repo plates all regenerate (the plates byte-identical to what is committed). Of 43 external links, 38 return 200. The other 5 are bot walls: both DOIs resolve to zenodo.org and the Zenodo API answers 200, LinkedIn answers scripts with 999. All 7 local paths exist. Every commit Zaid authored in the last 60 is signed (26 G); the 34 unsigned ones are the bot's, as the README says. Fixed three misleading lines: "every number links to the artifact" (plate numbers are not links; now: stated again in the text with a link); "each specimen is reproducible from a public record" (the 27 PRs are in a private codebase; now says so and points to the case study); the footer's role target, which contradicted the intro.

- Round 9 (phones): at a 390 px phone width a 1200 px plate is drawn 358 px wide, so its 12 px notes come out near 3.6 px. Plate I now has a 520 px single-column twin (`plate-specimens-narrow.svg`, `specimens_narrow()` sharing `specimen_card()` with the wide plate). The README serves it through `<picture><source media="(max-width: 600px)">`, which GitHub's sanitizer keeps (checked through the markdown API). Loading GitHub's own rendered markup at 390 px picks the narrow plate, with notes near 8.3 px; at 1280 px it picks the wide plate. The wide plate is unchanged apart from line breaks. Headless Chromium could not reach github.com from this machine, so the live page itself was not loaded.

- Round 10 (phones, Plate II): `plate-faults-narrow.svg`, 520 px, the faulted block above the five entries stacked one per row; `fault_block()` is shared with the wide plate, which regenerates identical apart from line breaks. Served under 600 px through `<picture>` like Plate I.

- Round 11 (phones, Plate V): `plate-fieldwork-narrow.svg` stacks the Zabira grid, the Pratyaya reconciliation and the upstream fossils one under another. The three sections are now functions placed by origin, shared with the wide plate, which regenerates identical apart from line breaks.

- Round 12 (phones, Plate III): the three assay panels are now `flake_panel`, `coldread_panel` and `augur_panel`, placed by origin; the only thing that tied them to the plate was the footnote position, now relative to the panel. `plate-assays-narrow.svg` stacks them; the wide plate regenerates identical apart from line breaks.

- Round 13 (phones, Plate IV): `plate-excavation-narrow.svg` is its own composition, because five headframes in a row do not stack: the surface systems become a list of small headframes, and the shaft keeps the kernel and its three chambers. `strata()`, `SURFACE`, `CHAMBERS` and `KERNEL_NOTE` are shared with the wide plate. Another session committed new test counts (second-brain 116, ecosystem 381, commit b590812) from this same checkout mid-round; that commit also carried this round's refactor, so the history splits the work across two commits.

- Round 14 (phones, route and Plate VI): `plate-route-narrow.svg` runs the six stations down a vertical trail and `plate-seal-narrow.svg` hangs the five seals on a vertical cord, sharing `STATIONS`, `station_marker()`, `SEALS` and `wax_seal()` with the wide plates (both identical apart from line breaks). Every plate on the page now has a phone twin: 7 `<picture>` elements, 14 plates.

- Round 15 (phones, the core sample): `phone_cut()` in `core_sample.py` crops the nightly plate to the rock, drops every label and leader (they fall below 4 px on a phone) and adds a 34 px title. The nightly job writes and commits `core-sample-narrow.svg` next to the full plate, and the README serves it under 600 px. A full layout refactor was ruled out because about 80 references to module-level layout constants sit in a script that runs unattended every night. All 8 images on the page now have phone versions.

- Round 16 (repo plate facts): the repo plates had no check tying their numbers to a source. `RepoPlateFactsHaveASource` now requires each one on the profile README (DOIs matched whole), or in an explicit `OFF_PAGE` list that names its source; one entry, longmemeval's 141 items, read from that repo's README. Planted errors (162 to 163, 116 to 117, a DOI digit) each fail it. While writing it, a shell edit turned the test's `\1` backreference into chr(1) for the second time tonight, which silently stopped it stripping the bot blocks; `ScriptsAreClean` now fails on any control character in a script.

- Round 17 (LinkedIn banner): `weekend-profile-update/creative/banner_core.py` cropped at a fixed y=452, but the unconformity had already moved to a mean of y=466 as October's bed thickened. `strip_centre()` now measures the erosion line from the plate (falls back to the section middle when there is no gap), and the script body moved into `main()` so the function can be imported and checked. Regenerated: centred at y=454, same composition. The PNG still needs uploading on LinkedIn by Zaid.

- Round 18 (phones, repo plates): `plate_narrow()` in `repo_plates.py` draws a 520 px plate (thesis wrapped, notes stacked, motif scaled beside them). The plate head is now shared, and a wide plate generated by the old and new code from the same commits is byte-identical. All 12 repos now carry `.github/plate-narrow.svg`, served under 600 px through `<picture>`; GitHub keeps the switch in each README checked (4 of 4 sampled). The wide plates were refreshed at the same time with today's commit strips.

- Round 19 (reproducibility): installing plates into the repos ran from two throwaway scripts in a scratch folder that can be wiped. `scripts/apply_repo_plates.py` now does it: it copies both plates, writes or upgrades the `<picture>` header, adds the footer once, and refuses by name when a plate or README is missing. Three tests cover a fresh README (and that a re-run changes nothing), upgrading the old single-image header, and a missing phone plate. Run against the real augur clone, it produced an empty diff, so it reproduces what was pushed. 17 tests in all.

## Needs Zaid
- Nothing open. Resolved 2026-10-28 on Zaid's go-ahead: India resumes rebuilt (381 and 162, both 1 page, career e46e8b9); LinkedIn banner uploaded by Zaid; PROVENANCE.sig.txt re-signed to cover the script-drawn plates (8b506a1, verified from GitHub raw).

- Round 20 (resume check, review only): compared the India resumes with PROFILE-FACTS.yaml; two stale counts, listed under Needs Zaid. No resume file changed.

## Next
- Refresh the repo plates monthly, or when a headline number changes: `python scripts/repo_plates.py <out>`, then `python scripts/apply_repo_plates.py <out> <repo> <clone>` for each clone, then commit and push each repo (fetch first).
