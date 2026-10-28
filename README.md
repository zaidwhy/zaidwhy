<picture>
<source media="(max-width: 600px)" srcset="https://raw.githubusercontent.com/zaidwhy/zaidwhy/main/assets/core-sample-narrow.svg">
<img src="https://raw.githubusercontent.com/zaidwhy/zaidwhy/main/assets/core-sample.svg" alt="Frontispiece, a core sample: a geological section through every GitHub contribution on this account since June 2024, one rock bed per month and thicker beds for busier months. An eleven-month gap from July 2025 to May 2026 shows as an unconformity, an erosion surface above older tilted beds. Merged upstream pull requests sit in the August 2026 bed as fossils and every public repository sits as a crystal in the month it was founded." width="100%">
</picture>

<sub>Read it like a road cut: the youngest rock is on top. Each bed is one month, and its thickness grows with the square root of that month's contributions. The wavy line is an <b>unconformity</b>: eleven months in which almost nothing was laid down, kept on the plate instead of smoothed over, and the older beds under it lie tilted as old rock does. Fossils are pull requests merged into other people's code; crystals are repositories founded. A GitHub Action redraws the plate every night from the API (<a href="scripts/core_sample.py">scripts/core_sample.py</a>), so the top bed is still forming as you read this.</sub>

> **I build AI systems that remember, retrieve and decide. Then I go looking for the place they break.**

This page is a field survey. The core sample above shows when the work was laid down. The six plates below follow it: what the drill brought up, where my own claims gave way, what the lab measured, what stands on the kernel, the ground I dug that was not mine, and how you can tell all of it is mine. Every number on a plate is stated again in the text beside it, with a link to the artifact that produced it.

B.Tech Information Technology (Honors with Research), MGM University, graduating June 2027. Open to **backend, AI engineer and new-grad roles in India** from January 2027.

<picture>
<source media="(max-width: 600px)" srcset="https://raw.githubusercontent.com/zaidwhy/zaidwhy/main/assets/plate-route-narrow.svg">
<img src="https://raw.githubusercontent.com/zaidwhy/zaidwhy/main/assets/plate-route.svg" alt="The route through this survey: I Specimens, II Fault lines, III Assays, IV Excavation, V Field work, VI The seal." width="100%">
</picture>

[I. Specimens](#i-specimens) · [II. Fault lines](#ii-fault-lines) · [III. Assays](#iii-assays) · [IV. Excavation](#iv-excavation) · [V. Field work](#v-field-work) · [VI. The seal](#vi-the-seal)

---

## Now: AFTERSHOCK, built in public and graded in public

**3,240 forecasts, locked in a hash-chained public ledger before any outcome exists.** [AFTERSHOCK](https://github.com/zaidwhy/aftershock) forecasts which countries a Netflix breakout charts in next, with Qloo's taste graph for what that audience loves there ([live](https://aftershock-qloo.vercel.app)). It is the same argument as the rest of this page, run forward in time: I committed to the numbers first, and the first grades land on 15 Nov 2026 whether I like them or not.

Three things I did to it that were meant to hurt:

- **I pre-registered the sponsor's claim and tried to lose it.** Does Qloo's launch kit beat an LLM's? The question, four arms, the metrics (overlap, no LLM judge) and the decision rule were committed on 27 Oct, before any LLM answer was collected: [EXPERIMENT_KITS.md](https://github.com/zaidwhy/aftershock/blob/main/docs/EXPERIMENT_KITS.md). It is reported whichever way it lands.
- **I tested my own headline feature and said what it did.** Adding Qloo to the country forecast gave no lift (ROC AUC 0.8182 against 0.8188), so the probability is history-only and the site says so.
- **I threw away my best result.** A song-placement effect that looked significant rested on data scraped from a site whose terms forbid automated collection. I read the terms, deleted the data and everything computed from it, rebuilt the ground truth from MusicBrainz, and re-ran the identical test. It did not replicate. The README says so.

```bash
# Verify the ledger yourself: no key, no network, prints None when every link in the chain holds.
git clone https://github.com/zaidwhy/aftershock && cd aftershock
wc -l ledger/forecasts.jsonl
python -c "from aftershock import ledger; print(ledger.verify())"
```

---

## I. Specimens

<picture>
<source media="(max-width: 600px)" srcset="https://raw.githubusercontent.com/zaidwhy/zaidwhy/main/assets/plate-specimens-narrow.svg">
<img src="https://raw.githubusercontent.com/zaidwhy/zaidwhy/main/assets/plate-specimens.svg" alt="Plate I, specimens: 3 pull requests merged upstream into libraries with 13.4k stars; 27 pull requests merged into a live product in 12 days; 2 research findings archived with a DOI; 381 offline tests; 3,240 forecasts locked before outcomes; 229 scored coding-agent runs." width="100%">
</picture>

Six samples from the core, each with a label that says where it was dug up. None of them is a self-description. Five are counts you can reproduce from a public record; the sixth, 27 pull requests into a private codebase, rests on the [case study](case-studies/zabira-academy.md) because the code cannot be shown.

<details>
<summary><b>Every specimen, with its receipt</b></summary>

| Claim | Proof |
|---|---|
| 3,240 forecasts locked in a public hash-chained ledger before their outcomes, and a pre-registered test of whether a sponsor API beats an LLM; my best result was discarded after reading a data source's terms and did not replicate on licensed data | [AFTERSHOCK](https://github.com/zaidwhy/aftershock) · [pre-registration](https://github.com/zaidwhy/aftershock/blob/main/docs/EXPERIMENT_KITS.md) |
| 3 pull requests merged into upstream OSS totalling **13.4k stars** | [tenacity #668](https://github.com/jd/tenacity/pull/668) · [returns #2480](https://github.com/dry-python/returns/pull/2480) · [gqlalchemy #390](https://github.com/memgraph/gqlalchemy/pull/390) |
| 27 pull requests merged into a **live production product** I did not build | [case study](case-studies/zabira-academy.md) |
| A customer-support analytics dashboard built from scratch for a chat support team (Python, FastAPI, pandas): all 10 aggregate totals match the support platform's own report, 222 tests | no link: private repository, company work |
| A 229-run pre-registered study of a coding agent: it fixed real race bugs instead of weakening the test (0 of 60), and **"do not change the tests" broke legitimate repairs (9/10 to 0/10)** | [RESULT.md](https://github.com/zaidwhy/flake-laundering/blob/master/RESULT.md) |
| 2 original research findings, each with a negative control and a second-model replication, **archived with a permanent DOI** | [10.5281/zenodo.22309660](https://doi.org/10.5281/zenodo.22309660) · [10.5281/zenodo.22309658](https://doi.org/10.5281/zenodo.22309658) |
| A retrieval method benchmarked against 6 baselines - including the version of it that **failed** | [TCMF write-up](https://github.com/zaidwhy/CivilizationOS/blob/main/docs/tcmf.md) · [case study](case-studies/civilizationos.md) |
| 381 tests across the ecosystem, every one offline and mocked - no API key runs any of them | `pytest --collect-only` (personal-llm: `tests/ evals/`) on [personal-llm](https://github.com/zaidwhy/personal-llm) · [second-brain](https://github.com/zaidwhy/second-brain) · [github-pr-agent](https://github.com/zaidwhy/github-pr-agent) |
| Every commit I author is cryptographically signed (the nightly activity bot's `auto:` commits are not), and both findings carry an ORCID-bound DOI | [PROVENANCE.md](PROVENANCE.md) · [ORCID 0009-0003-4313-1510](https://orcid.org/0009-0003-4313-1510) |

</details>

<details>
<summary><b>Don't take my word for any of it - here is how to falsify this page</b></summary>

<br>

```bash
# The merged pull requests. Check the author field.
gh pr view 668  --repo jd/tenacity         --json state,mergedAt,author
gh pr view 2480 --repo dry-python/returns  --json state,mergedAt,author
gh pr view 390  --repo memgraph/gqlalchemy --json state,mergedAt,author

# The research. Re-run the analysis on the shipped raw data.
git clone https://github.com/zaidwhy/coldread && cd coldread
python analyze.py out/results-qwen2.5_7b-instruct.jsonl

# The commit signatures.
git clone https://github.com/zaidwhy/augur && cd augur
git log --show-signature -3
```

If any of it does not reproduce, the claim above is wrong and I want to know.

</details>

**Recent activity, pulled live from the repos below every night, not written by hand:**

<!-- ACTIVITY:START -->
- `2026-10-28` **second-brain** - Record the end-to-end ingest and search check in the rebuilt venv ([`fddee1f`](https://github.com/zaidwhy/second-brain/commit/fddee1f6872f703be95873ae48129cd77b5759aa))
- `2026-10-27` **dreamos-college-project** - Phone-width survey plate under 600 px ([`dfb5e0c`](https://github.com/zaidwhy/dreamos-college-project/commit/dfb5e0cfaaa7bf3543b748b6e69548b0e59bb254))
- `2026-10-27` **github-pr-agent** - Phone-width survey plate under 600 px ([`2be6677`](https://github.com/zaidwhy/github-pr-agent/commit/2be667730e374ee01a9f003b7b7b52723f5544ea))
- `2026-10-27` **second-brain** - Phone-width survey plate under 600 px ([`02f554c`](https://github.com/zaidwhy/second-brain/commit/02f554c1fbb41163cb84892b8d969fbb34487590))
- `2026-10-27` **personal-llm** - Phone-width survey plate under 600 px ([`cdf1c88`](https://github.com/zaidwhy/personal-llm/commit/cdf1c88530616f4538862f7df79d2eb9c42d4224))
- `2026-10-27` **augur** - Phone-width survey plate under 600 px ([`42fee7c`](https://github.com/zaidwhy/augur/commit/42fee7c92de548b1f54f31bcb0f6de51d42300be))
- `2026-10-27` **coldread** - Phone-width survey plate under 600 px ([`32a08e5`](https://github.com/zaidwhy/coldread/commit/32a08e58d6a793ac88c876a3463c849aa04a9e6a))
- `2026-10-27` **autocto** - Phone-width survey plate under 600 px ([`c0defa9`](https://github.com/zaidwhy/autocto/commit/c0defa99d54f9e9188a73bf207b56a01e4d3fd8b))
<!-- ACTIVITY:END -->

---

## II. Fault lines

<picture>
<source media="(max-width: 600px)" srcset="https://raw.githubusercontent.com/zaidwhy/zaidwhy/main/assets/plate-faults-narrow.svg">
<img src="https://raw.githubusercontent.com/zaidwhy/zaidwhy/main/assets/plate-faults.svg" alt="Plate II, fault lines: five claims of mine broken by my own evidence: TCMF version one, COLD READ's confidently-wrong finding, AUGUR's forecasting programme, adk-python 6190, and AFTERSHOCK's song-placement effect." width="100%">
</picture>

Anyone can publish the version of their work where everything held. These are five places where I made a claim, went and collected the evidence, and the evidence broke it. Every correction stays in the repository it belongs to. The [TCMF write-up](https://github.com/zaidwhy/CivilizationOS/blob/main/docs/tcmf.md) still shows the fusion formula that scored 0.02. [`RESULT.md`](https://github.com/zaidwhy/coldread/blob/master/RESULT.md) still states the headline that did not survive a second model. [`FINDING.md`](https://github.com/zaidwhy/augur/blob/master/FINDING.md) still has the forecasting plan its own first phase falsified. [adk-python #6190](https://github.com/google/adk-python/pull/6190) is closed and on this page anyway, and the [AFTERSHOCK README](https://github.com/zaidwhy/aftershock) still says why its best result was thrown away.

That is the argument for every number on this page: a result that was never allowed to fail is not evidence of anything.

---

## III. Assays

<picture>
<source media="(max-width: 600px)" srcset="https://raw.githubusercontent.com/zaidwhy/zaidwhy/main/assets/plate-assays-narrow.svg">
<img src="https://raw.githubusercontent.com/zaidwhy/zaidwhy/main/assets/plate-assays.svg" alt="Plate III, assays. FLAKE LAUNDERING: handed a wrong test, coding agents repaired it in 9 of 10 runs, 0 of 10 when told not to change the tests, 10 of 10 when told to find out which side is wrong. COLD READ: words before a model beats chance on gender, 50, 800 or about 1600 depending on the model. AUGUR: a 1938-cutoff model answers from 1899, a 1930-cutoff model from 1850." width="100%">
</picture>

Three samples sent to the lab. Each study has a negative control, because a measurement without one proves nothing. The two older studies were replicated on a second model family. The newest uses one agent and one model, and says so in its first paragraph.

### [FLAKE LAUNDERING](https://github.com/zaidwhy/flake-laundering) - the rule meant to stop it is what broke

**The guard everyone reaches for is what broke it.** On a test that really was wrong, *"do not change the tests"* took correct repairs from 9 of 10 down to 0 of 10. One sentence fixed it.

`229 scored runs` · `pre-registered, two studies` · `negative and positive controls` · `blind LLM judge + hand review` · `every transcript shipped` · [read the result](https://github.com/zaidwhy/flake-laundering/blob/master/RESULT.md)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23721575.svg)](https://doi.org/10.5281/zenodo.23721575) archived, citable, timestamped

<details>
<summary>Read the full story</summary>

A subagent on this very portfolio once made six failing Playwright tests pass by retrying a click until the menu opened. The test was right; a visitor's first click really was being lost. So I measured whether that is what coding agents do: web apps with seeded race bugs, a mock backend that is slow half the time, and Claude Code told to get CI green. Each run is scored by re-running the original test 50 times on a clean copy of the app, never by the agent's word.

**It fixes the app.** 0 of 60 plain-brief runs weakened the test, 60 of 60 fixed the race, including when the cause was split across lazy modules, buried in a 44-file app, or met while shipping an unrelated feature. My pre-registered hypothesis was falsified.

The control is where it got interesting. On tests that really were wrong, the guard everyone reaches for, **"do not change the tests", took correct repairs from 9 of 10 to 0 of 10**: every agent kept the bad test and bent working code around it. One sentence fixed it - "the test may be wrong or the app may be wrong; find out which" - 10 of 10 repaired, 0 of 40 correct tests weakened.

</details>

### [COLD READ](https://github.com/zaidwhy/coldread) - the anonymity half-life belongs to the reader

**Same 72 authors, same words, three readers of one size: 50, 800 or 1600 words before each one beats a coin flip** (llama3.1:8b, qwen2.5:7b and mistral:7b in that order). How long you stay anonymous depends on the model reading you, not on the text.

`n=3 model families` · `negative control held` · `contamination ruled out` · `Wilson 95% intervals` · [read the result](https://github.com/zaidwhy/coldread/blob/master/RESULT.md)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22309660.svg)](https://doi.org/10.5281/zenodo.22309660) archived, citable, timestamped

<details>
<summary>Read the full story</summary>

How many words can you write before a machine knows who you are? I went looking for that number and found that the question is malformed - and why it is malformed is the finding.

72 authors from a labelled blog corpus, shown to local models in growing slices, forced to commit to gender, age band, and star sign at every step. **Star sign is the control**: it is labelled in the data and is not inferable from prose. It never cleared its floor in any of the three models, which is the only reason to trust anything else on the chart.

Same authors, same words, same prompt, three readers of the same size. One needs 50 words to beat a coin flip on gender, another 800, the third 1600. **A thirty-two-fold spread on identical text**, which means no statement of the form "you are anonymous for N words" means anything at all without naming the model doing the reading.

Corpus memorisation was tested directly rather than waved away, and ruled out. One finding from the first model - that short samples produce *confidently wrong* guesses rather than uncertainty - did **not** replicate on the second, and the write-up says so in those words.

</details>

### [AUGUR](https://github.com/zaidwhy/augur) - a model with a 1938 cutoff answers from 1899

**A cutoff marks the edge of a corpus, not its centre.** Asked what year it is, both time-locked models answer from four to eight decades before their stated cutoff: TypeWriter-1938 from 1899, 39 years short, and Talkie-1930 from 1850, 80 years short.

`n=2 model families` · `14-probe battery, temperature 0, fixed seed` · `raw output shipped unedited` · [read the finding](https://github.com/zaidwhy/augur/blob/master/FINDING.md)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22309658.svg)](https://doi.org/10.5281/zenodo.22309658) archived, citable, timestamped

<details>
<summary>Read the full story</summary>

Research groups are training language models from scratch on text that stops at a fixed historical date, to ask the past a question and get the past's answer. The assumption riding underneath is that a model with a 1938 cutoff represents 1938.

It does not. A cutoff describes the *edge* of a corpus, not its centre of gravity - and the shelves are not even. Ask such a model what year it is and it answers from where the mass of its training data sits. Both models tested answer from **four to eight decades before their stated cutoff**. One names George Washington as President. The other names Grover Cleveland and dates the term to 1893.

Tell one of them the year and it relocates forty years on the spot, correctly naming Hoover, his 1928 election, and his inauguration date. Tell the other and it does not move at all. So a time-locked model has to be characterised on **two** axes, not one: where it stands, and whether it can be moved. The practical rule falls straight out - anchor the date, then verify the anchor took, because on half the models tested it did not.

A second finding fell out of the demo. Asked whether another great war was coming, a 1930-anchored model calls it highly improbable. Asked instead to *enumerate the dangers*, the same model in the same year names the Rhineland, Poland, Czechoslovakia, and the Italo-Yugoslav quarrel, and says every one of them is armed to the teeth. Both answers were in the corpus. **The form of the question decides which 1930 you meet** - which means elicitation is not a neutral window onto a model, it is part of the measurement.

</details>

---

## IV. Excavation

<picture>
<source media="(max-width: 600px)" srcset="https://raw.githubusercontent.com/zaidwhy/zaidwhy/main/assets/plate-excavation-narrow.svg">
<img src="https://raw.githubusercontent.com/zaidwhy/zaidwhy/main/assets/plate-excavation.svg" alt="Plate IV, excavation: five systems on the surface (CivilizationOS, Recall, autocto, AFTERSHOCK, Agent Factory) and below ground the personal-llm memory kernel with 181 offline tests, reached by second-brain, github-pr-agent and DreamOS." width="100%">
</picture>

The kernel was sunk once and every app below ground draws from it, instead of each one rebuilding retrieval. The headframes on the surface are the systems people can use, each with the one number it is judged by.

<!-- STATUS:START -->
| Live system | Answered |
|---|---|
| [CivilizationOS](https://civilization-os-murex.vercel.app) | `200 OK` |
| [AFTERSHOCK](https://aftershock-qloo.vercel.app) | `200 OK` |

*checked 2026-10-28 09:21 UTC, by the workflow that runs this page*
<!-- STATUS:END -->

### [CivilizationOS](https://github.com/zaidwhy/CivilizationOS) - a society of agents, and a retrieval method that failed first

*A causal memory that has to outrank a rumour with a witness, not just a similar-sounding one.*

<details>
<summary>Dig notes</summary>

10 autonomous citizens and 5 institutional councils debate, remember, and react to injected crises, and now generate their own.

The part worth reading is **Temporal-Causal Memory Fusion**. Standard RAG retrieves on semantic similarity alone; TCMF fuses episodic memory with a causal graph over the society's own history, so a witness to a root cause outranks somebody who heard about it second-hand.

I benchmarked it against 6 baseline retrieval strategies over 300 scenarios and **the first version recovered almost none of the causal signal it was built to exploit: recall@5 of 0.02, where the causal signal alone reaches 1.00 on the identical scores.** The multiplicative fusion was the bug. A normalised additive version recovered the signal and beat every single-signal baseline in a mixed regime, and a follow-up 60-scenario study showed the retrieval choice changes the model's actual decision rather than merely its confidence. The failed version is still in the write-up, because a method that was never wrong was never tested.

</details>

`Python` · `FastAPI` · `React` · `Three.js` · `ChromaDB` · `NetworkX` · [live](https://civilization-os-murex.vercel.app) · [TCMF write-up](https://github.com/zaidwhy/CivilizationOS/blob/main/docs/tcmf.md)

### [Recall](https://github.com/zaidwhy/recall) - spatial memory you can talk to

*Point, ask out loud, get back the exact frame the camera saw it in.*

<details>
<summary>Dig notes</summary>

Point a phone camera at your space, ask out loud where you left something, get a spoken answer with the exact frame it was seen in. The voice model does not guess locations - it calls a tool that searches a vector store built from what the camera actually recorded.

```
Eval:         Recall@1 100% (10/10) · Recall@3 100% (10/10) · median latency 149ms
Embeddings:   all-MiniLM-L6-v2 via ONNX, fully local, zero embedding cost
Quota guard:  120s floor between vision calls, on-screen daily budget counter
```

</details>

`Python` · `FastAPI` · `React` · `ChromaDB` · `ONNX` · `WebSocket`

### [autocto](https://github.com/zaidwhy/autocto) - where the risk in a repo lives, from its git history alone

*The file to review first is the one that changes most and branches most.*

<details>
<summary>Dig notes</summary>

Five analyzers, no LLM and zero runtime dependencies: bug hotspots (churn x complexity), duplicated logic (token-shingle Jaccard), maintenance cost (size x churn x (1 + fan-in)), architectural debt (Tarjan cycles, god files, layering violations), and a migration planner that orders proposed changes with a topological sort. I/O lives in one `analyze_repo()` per analyzer, with the `git log` call behind an injectable seam; everything underneath is a pure function. 162 tests on main.

```
$ autocto hotspots ../recall --limit 3
frontend/src/App.jsx   churn 41 x complexity 129 = 5289
backend/main.py        churn 41 x complexity  89 = 3649
backend/memory.py      churn 11 x complexity  49 =  539
```

</details>

`Python` · `pipx install repo-autocto` · [PyPI](https://pypi.org/project/repo-autocto/)

### [AFTERSHOCK](https://github.com/zaidwhy/aftershock) - forecasts where a Netflix breakout spreads next, and grades itself in public

*The forecast is locked in a hash-chained file before the outcome exists.*

<details>
<summary>Dig notes</summary>

Weekly it reads Netflix's public per-country Top 10, finds titles that just broke out, and forecasts the countries they reach next (history-only model, ROC AUC 0.817 on 829 held-out breakouts). Qloo's taste graph supplies the launch kit and city hotspots. The measured part: Qloo added nothing to the country forecast (AUC 0.8188 against 0.8182), and a soundtrack-song result that looked significant on Tunefind data was discarded when its terms forbade automated collection and did not replicate on MusicBrainz data. Every probability for the week of 18 Oct 2026 (3,240 rows, 35 breakouts) is in `ledger/forecasts.jsonl`, graded from 15 Nov. 89 tests.

</details>

`Python` · `FastAPI` · `MCP` · [live](https://aftershock-qloo.vercel.app) · [pre-registered experiment](https://github.com/zaidwhy/aftershock/blob/main/docs/EXPERIMENT_KITS.md)

### [Agent Factory](https://github.com/zaidwhy/agent-factory) - a build pipeline with frozen contracts

*The contract freezes before the code does, so two agents can build in parallel without seeing each other's work.*

<details>
<summary>Dig notes</summary>

Six specialised agents turn a one-line idea into a tested, runnable project. It is not a code generator; it is a pipeline with contracts. The architect **freezes an API contract before backend and frontend build in parallel from it**, which is the only reason two agents' output stays compatible without either one seeing the other's code. The reviewer is read-only by design. The debugger is the only agent permitted to execute, and is graded on what it fixes rather than what it writes.

Shipped 3 full projects end to end in test runs. On [Receipts.dev](https://github.com/zaidwhy/receipts-dev): 92 files, 16 bugs found and fixed, 0 type errors, 0 lint errors.

</details>

<details>
<summary>More systems</summary>

<br>

| Repository | What it does | Tests |
|---|---|---|
| [personal-llm](https://github.com/zaidwhy/personal-llm) | Local-first memory and RAG kernel: a plan-act-reflect agent loop, 4 permission-tiered tools including an SSRF-guarded fetch, a full audit log | 181 offline, fully mocked, zero-key CI |
| [second-brain](https://github.com/zaidwhy/second-brain) | Vault ingestion, auto-linking and an offline knowledge-graph viewer | 116 |
| [github-pr-agent](https://github.com/zaidwhy/github-pr-agent) | Repo analysis, issue triage and PR planning | 84 |
| [DreamOS](https://github.com/zaidwhy/dreamos-college-project) | Semantic file-management OS shell | |
| [resume-job-fit-ai](https://github.com/zaidwhy/resume-job-fit-ai) | Resume-to-job fit scoring with truthful rewrites and Pydantic-validated structured output | 49 unit tests, CI on every push |

</details>

<sub>Case studies: [CivilizationOS](case-studies/civilizationos.md) - a retrieval method that failed its own benchmark, in public · [Personal LLM](case-studies/personal-llm.md) - one kernel, three apps, and an eval suite that argued with itself</sub>

---

## V. Field work

<picture>
<source media="(max-width: 600px)" srcset="https://raw.githubusercontent.com/zaidwhy/zaidwhy/main/assets/plate-fieldwork-narrow.svg">
<img src="https://raw.githubusercontent.com/zaidwhy/zaidwhy/main/assets/plate-fieldwork.svg" alt="Plate V, field work: 27 pull requests merged into Zabira Academy in 12 days; at Pratyaya Limited all 10 aggregate totals match the support platform's report and 53 of 55 per-agent averages agree within one second; upstream, 3 merged pull requests, 2 open, and adk-python 6190 closed after an LGTM." width="100%">
</picture>

Building your own project is the easy dig. This plate covers ground that belonged to someone else: a live product with paying users, a company's support data, and libraries whose maintainers owed me nothing. Every change had to pass somebody else's review.

### [Zabira Academy](case-studies/zabira-academy.md) - 27 merged PRs into a live product I did not build

<details>
<summary>Dig notes</summary>

Twelve days. +8,838 / -1,619 across 557 file changes, into a production learning platform with real users, every change reviewed and merged by the repository owner.

Security hardening (exception leakage across 226 files, Origin checks on 60 mutating endpoints, a sanitiser bypass, session revocation), an end-to-end suite covering the seven launch-critical flows behind a CI gate, and a sitewide search feature built from the backend through to voice input.

Including the one where CI went red on my branch and the cause turned out to **predate my work by three days** - a registration validation rule silently failing a test fixture, bisected through the run history and confirmed from the failed run's Playwright snapshot. Reading the evidence beat blaming my own diff.

The codebase is private, so the [case study](case-studies/zabira-academy.md) is the record.

</details>

### Support analytics dashboard - built from scratch during an AI internship at Pratyaya Limited

<details>
<summary>Dig notes</summary>

A customer-support analytics dashboard for a chat support team (Python, FastAPI, pandas, Jinja2): daily to month-to-date performance, per-agent response, resolution and CSAT, and bot versus agent resolution, each figure shown beside the support platform's own report.

Reconciled to that platform's reports: all 10 aggregate totals match exactly and 53 of 55 per-agent response-time averages agree within one second; a figure that differs is clickable and explains why. Chat transcripts are read through a read-only, test-enforced API client to classify why chats were handed from bot to agent, which shrank the unexplained "other" bucket to about 1%. Role-based login, argon2 password hashing, a strict content-security policy, and 222 automated tests.

The repository is private and the data is the company's, so there is no link and nothing here describes a customer or a business figure.

</details>

### Upstream open source

**Merged:**

- **[jd/tenacity #668](https://github.com/jd/tenacity/pull/668)** · 8.8k stars - fixed static typing for `@retry`-decorated instance methods so bound-method signatures survive the decorator under mypy strict.
- **[dry-python/returns #2480](https://github.com/dry-python/returns/pull/2480)** · 4.4k stars - relaxed `future()` / `future_safe()` parameter types from `Coroutine` to the broader `Awaitable` protocol.
- **[memgraph/gqlalchemy #390](https://github.com/memgraph/gqlalchemy/pull/390)** - added unary-operator support (`IS NOT NULL`) to the query builder, with tests, docs, and a signed CLA.

**Open:** [gqlalchemy #392](https://github.com/memgraph/gqlalchemy/pull/392) (`ON CREATE` / `ON MATCH` clauses) · [django-taggit #944](https://github.com/jazzband/django-taggit/pull/944) (`remove_by_slug()` on `TaggableManager`).

**And one that closed unmerged, which is the more useful story:** [google/adk-python #6190](https://github.com/google/adk-python/pull/6190) fixed an `Optional[List[str]]` hint that broke the CLI parser. It survived a full maintainer review round - I root-caused a CI failure to a leftover repro script breaking Mypy and the linter, fixed it, got an LGTM - and then a maintainer's own commit resolved the same underlying bug first and the PR closed. Reviewed, correct, and beaten to it.

<details>
<summary>The field kit</summary>

```
languages   Python 3.11+ · TypeScript · SQL · PHP
ai          RAG architectures · multi-agent orchestration · LLM evals
            structured outputs · evals · vector search · agent tool loops
backend     FastAPI · WebSocket · Node.js · Pydantic · Playwright E2E
frontend    React · Vite · Three.js
data        ChromaDB · SQLite · pgvector · NetworkX · sentence-transformers
infra       Docker · GitHub Actions · Vercel · Render
```

</details>

---

## VI. The seal

<picture>
<source media="(max-width: 600px)" srcset="https://raw.githubusercontent.com/zaidwhy/zaidwhy/main/assets/plate-seal-narrow.svg">
<img src="https://raw.githubusercontent.com/zaidwhy/zaidwhy/main/assets/plate-seal.svg" alt="Plate VI, the seal: a signed commit, an ed25519 signature verified by GitHub, an immutable release tag, a Zenodo DOI with an independent timestamp, and an ORCID iD bound to a person." width="100%">
</picture>

Five links, and the useful property is that four of them are asserted by somebody other than me. GitHub checks the signature. Zenodo issues the timestamp. ORCID binds the iD to a person. A repository can be cloned in a second; none of that comes with it.

<details>
<summary><b>How to tell this work from a copy of it</b></summary>

<br>

```bash
# 1. Whose signature is on the history? A copy carries commits it cannot re-sign.
gh api repos/OWNER/REPO/commits --jq '.[0].commit.verification'

# 2. Which DOI does the write-up resolve to, and whose ORCID does that record list?
curl -sIL https://doi.org/10.5281/zenodo.22309658 | grep -i location

# 3. Does the fork still load assets, badges, or CI status from the original account?
grep -rn 'raw.githubusercontent.com\|/actions/workflows/' README.md

# 4. Does the LICENSE copyright line match the account that published it?
head -3 LICENSE
```

Check 3 is the one that tends to settle it. A README copied wholesale keeps pulling its images and its CI badge from wherever it was copied from, which means the copy renders the original's URL to prove the copy's claim.

</details>

<br>

Every commit I author is signed with the key below; the nightly activity bot's `auto:` commits are not. The plates on this page are drawn by code in this repository ([`core_sample.py`](scripts/core_sample.py), [`plates.py`](scripts/plates.py)), served from it, and carry an authorship manifest in their source.

```
Zaid Ali Syed
ORCID  0009-0003-4313-1510
PGP    EFE9 4832 B2B9 80D9 B583  91F2 8FAA BCC1 B1AC 09E5
```

Full signed statement: **[PROVENANCE.md](PROVENANCE.md)** · verify with `gpg --verify` on [`PROVENANCE.sig.txt`](PROVENANCE.sig.txt)

---

**[Portfolio](https://www.solstine.dev)** · **[LinkedIn](https://www.linkedin.com/in/zaidalisyed)** · Open to backend, AI engineer and new-grad roles in India from January 2027.
