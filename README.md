<img src="https://raw.githubusercontent.com/zaidwhy/zaidwhy/main/assets/nameplate.svg" alt="Zaid Ali Syed - AI systems engineer" width="100%">

> **I build AI systems that remember, retrieve, and decide.**
> Then I try to break them - because a system that never got the chance to fail was never actually tested.

Most of what follows is a number. Every number is a link to the artifact that produced it: the merged pull request, the raw model output, the test run, the reproducible script. Nothing here asks to be believed.

B.Tech Information Technology (Honours with Research), MGM University, graduating June 2027. Open to **AI engineer / applied AI internship** roles.

<img src="https://raw.githubusercontent.com/zaidwhy/zaidwhy/main/assets/roadmap.svg" alt="Roadmap of this page, six stations on a rail: I Proof, II Failures, III Research, IV Systems, V Production, VI Provenance." width="100%">

[I. Proof](#i-the-short-version-with-receipts) · [II. Failures](#ii-the-ledger-of-things-i-got-wrong) · [III. Research](#iii-research) · [IV. Systems](#iv-systems) · [V. Production](#v-production-work) · [VI. Provenance](#vi-provenance)

---

## I. The short version, with receipts

| Claim | Proof |
|---|---|
| 3 pull requests merged into upstream OSS totalling **13.4k stars** | [tenacity #668](https://github.com/jd/tenacity/pull/668) · [returns #2480](https://github.com/dry-python/returns/pull/2480) · [gqlalchemy #390](https://github.com/memgraph/gqlalchemy/pull/390) |
| 27 pull requests merged into a **live production product** I did not build | [case study](case-studies/zabira-academy.md) |
| A customer-support analytics dashboard built from scratch for a WhatsApp support team (Python, FastAPI, pandas): all 10 aggregate totals match the support platform's own report, 146 tests, zero accessibility violations | no link: private repository, company work |
| 2 original research findings, each with a negative control and a second-model replication, **archived with a permanent DOI** | [10.5281/zenodo.22309660](https://doi.org/10.5281/zenodo.22309660) · [10.5281/zenodo.22309658](https://doi.org/10.5281/zenodo.22309658) |
| A retrieval method benchmarked against 6 baselines - including the version of it that **failed** | [TCMF write-up](https://github.com/zaidwhy/CivilizationOS/blob/main/docs/tcmf.md) · [case study](case-studies/civilizationos.md) |
| 363 tests across the ecosystem, every one offline and mocked - no API key runs any of them | `pytest --collect-only` on [personal-llm](https://github.com/zaidwhy/personal-llm) · [second-brain](https://github.com/zaidwhy/second-brain) · [github-pr-agent](https://github.com/zaidwhy/github-pr-agent) |
| Every commit on this account is cryptographically signed, and both findings carry an ORCID-bound DOI | [PROVENANCE.md](PROVENANCE.md) · [ORCID 0009-0003-4313-1510](https://orcid.org/0009-0003-4313-1510) |

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
- `2026-10-06` **dreamos-college-project** - Refresh handoff: scale benchmark, privacy audit, final deck and report ([`8b56d99`](https://github.com/zaidwhy/dreamos-college-project/commit/8b56d9998782d2af04717450fa0cc4334973a07e))
- `2026-10-06` **dreamos-college-project** - Deck: add flow, sequence, use-case and database diagrams from the desig... ([`1112498`](https://github.com/zaidwhy/dreamos-college-project/commit/11124982ecec7514d4bcf62480299ff9a6bbc5db))
- `2026-10-06` **dreamos-college-project** - Add final monitoring deck and final-year project report ([`0b33d21`](https://github.com/zaidwhy/dreamos-college-project/commit/0b33d212bb1f715f83289c560ef0e6aaf08147c3))
- `2026-10-06` **dreamos-college-project** - Add privacy audit: report where data could leave the machine ([`2761ece`](https://github.com/zaidwhy/dreamos-college-project/commit/2761ece3ff273f9cb26852bd99940784877077d7))
- `2026-10-06` **dreamos-college-project** - Fix two measured bottlenecks: localhost IPv6 delay and quadratic graph... ([`cab4fbc`](https://github.com/zaidwhy/dreamos-college-project/commit/cab4fbcb3cf4d27e119e97dc5f09ccb525b0bf89))
- `2026-10-06` **coldread** - Step 3b result: topic-word masking delays the industry half-life one st... ([`90a72d3`](https://github.com/zaidwhy/coldread/commit/90a72d38783e82035db26e1136abdd3b18795b45))
- `2026-10-06` **coldread** - HANDOFF: v1.3.0 deposited; step 3b status ([`c3dcf3d`](https://github.com/zaidwhy/coldread/commit/c3dcf3d3411fc0b714ce0aa7089a72448c4e152a))
- `2026-10-06` **coldread** - v1.3.0: step 3 (industry as a fourth attribute) written up for deposit ([`ad33ff7`](https://github.com/zaidwhy/coldread/commit/ad33ff7fb79ce82b83870fc38804979d00831816))
<!-- ACTIVITY:END -->

---

## II. The ledger of things I got wrong

<img src="https://raw.githubusercontent.com/zaidwhy/zaidwhy/main/assets/failure-ledger.svg" alt="The failure ledger: TCMF version one scored 0.02 recall at 5 on the causal signal it was built for where a causal oracle reaches 1.00, AUGUR's forecasting programme was killed by its own phase zero, COLD READ's headline finding failed to replicate on a second model, and adk-python 6190 was closed unmerged after an LGTM." width="100%">

Anyone can publish the version of their work where everything went right. The four entries above are claims I actually made, each one struck by evidence I went and collected, and each correction is published in the repository named beside it rather than quietly dropped. The [TCMF write-up](https://github.com/zaidwhy/CivilizationOS/blob/main/docs/tcmf.md) still contains the fusion formula that scored zero. [`FINDING.md`](https://github.com/zaidwhy/augur/blob/master/FINDING.md) still contains the forecasting plan its own first phase falsified. [`RESULT.md`](https://github.com/zaidwhy/coldread/blob/master/RESULT.md) still contains the headline that did not survive a second model. [adk-python #6190](https://github.com/google/adk-python/pull/6190) is closed and is on this page anyway.

That is the whole argument for the numbers further down. A result that was never allowed to fail is not evidence of anything.

---

## III. Research

Two studies. Each one carries a negative control, because a measurement without a control is a rumour, and each one was replicated on a second model family, because a finding from one model is a fact about that model.

### [COLD READ](https://github.com/zaidwhy/coldread) - the anonymity half-life belongs to the reader

<img src="https://raw.githubusercontent.com/zaidwhy/zaidwhy/main/assets/coldread-curves.svg" alt="Gender inference accuracy against words shown, for two models. llama3.1:8b clears chance at 50 words, qwen2.5:7b at 800." width="100%">

<sub>Plate 02 plots the first two readers. The third, mistral:7b, needs about 1600 words; all three are in <a href="https://github.com/zaidwhy/coldread/blob/master/RESULT.md">RESULT.md</a>.</sub>

How many words can you write before a machine knows who you are? I went looking for that number and found that the question is malformed - and why it is malformed is the finding.

72 authors from a labelled blog corpus, shown to local models in growing slices, forced to commit to gender, age band, and star sign at every step. **Star sign is the control**: it is labelled in the data and is not inferable from prose. It never cleared its floor in any of the three models, which is the only reason to trust anything else on the chart.

Same authors, same words, same prompt, three readers of the same size. One needs 50 words to beat a coin flip on gender, another 800, the third 1600. **A thirty-two-fold spread on identical text**, which means no statement of the form "you are anonymous for N words" means anything at all without naming the model doing the reading.

Corpus memorisation was tested directly rather than waved away, and ruled out. One finding from the first model - that short samples produce *confidently wrong* guesses rather than uncertainty - did **not** replicate on the second, and the write-up says so in those words.

`n=3 model families` · `negative control held` · `contamination ruled out` · `Wilson 95% intervals` · [read the result](https://github.com/zaidwhy/coldread/blob/master/RESULT.md)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22309660.svg)](https://doi.org/10.5281/zenodo.22309660) archived, citable, timestamped

### [AUGUR](https://github.com/zaidwhy/augur) - a model with a 1938 cutoff answers from 1899

<img src="https://raw.githubusercontent.com/zaidwhy/zaidwhy/main/assets/augur-drift.svg" alt="Two time-locked models on a timeline: TypeWriter-1938 speaks from 1899, a 39 year gap; Talkie-1930 speaks from 1850, an 80 year gap." width="100%">

Research groups are training language models from scratch on text that stops at a fixed historical date, to ask the past a question and get the past's answer. The assumption riding underneath is that a model with a 1938 cutoff represents 1938.

It does not. A cutoff describes the *edge* of a corpus, not its centre of gravity - and the shelves are not even. Ask such a model what year it is and it answers from where the mass of its training data sits. Both models tested answer from **four to eight decades before their stated cutoff**. One names George Washington as President. The other names Grover Cleveland and dates the term to 1893.

Tell one of them the year and it relocates forty years on the spot, correctly naming Hoover, his 1928 election, and his inauguration date. Tell the other and it does not move at all. So a time-locked model has to be characterised on **two** axes, not one: where it stands, and whether it can be moved. The practical rule falls straight out - anchor the date, then verify the anchor took, because on half the models tested it did not.

A second finding fell out of the demo. Asked whether another great war was coming, a 1930-anchored model calls it highly improbable. Asked instead to *enumerate the dangers*, the same model in the same year names the Rhineland, Poland, Czechoslovakia, and the Italo-Yugoslav quarrel, and says every one of them is armed to the teeth. Both answers were in the corpus. **The form of the question decides which 1930 you meet** - which means elicitation is not a neutral window onto a model, it is part of the measurement.

`n=2 model families` · `14-probe battery, temperature 0, fixed seed` · `raw output shipped unedited` · [read the finding](https://github.com/zaidwhy/augur/blob/master/FINDING.md)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22309658.svg)](https://doi.org/10.5281/zenodo.22309658) archived, citable, timestamped

---

## IV. Systems

One memory kernel, built once, imported by everything downstream instead of each app rebuilding retrieval:

<img src="https://raw.githubusercontent.com/zaidwhy/zaidwhy/main/assets/kernel-map.svg" alt="The personal-llm memory and RAG kernel, with 188 offline tests, imported by second-brain (110 tests), github-pr-agent (65 tests) and DreamOS." width="100%">

<!-- STATUS:START -->
- **CivilizationOS** - `200 OK` - [https://civilization-os-murex.vercel.app](https://civilization-os-murex.vercel.app)

*checked 2026-10-09 10:08 UTC, by the workflow that runs this page*
<!-- STATUS:END -->

### [CivilizationOS](https://github.com/zaidwhy/CivilizationOS) - a society of agents, and a retrieval method that failed first

*A causal memory that has to outrank a rumour with a witness, not just a similar-sounding one.*

35 agents - 10 autonomous citizens and 5 institutional councils - debate, remember, and react to injected crises, and now generate their own.

The part worth reading is **Temporal-Causal Memory Fusion**. Standard RAG retrieves on semantic similarity alone; TCMF fuses episodic memory with a causal graph over the society's own history, so a witness to a root cause outranks somebody who heard about it second-hand.

I benchmarked it against 6 baseline retrieval strategies over 300 scenarios and **the first version recovered almost none of the causal signal it was built to exploit: recall@5 of 0.02, where the causal signal alone reaches 1.00 on the identical scores.** The multiplicative fusion was the bug. A normalised additive version recovered the signal and beat every single-signal baseline in a mixed regime, and a follow-up 60-scenario study showed the retrieval choice changes the model's actual decision rather than merely its confidence. The failed version is still in the write-up, because a method that was never wrong was never tested.

`Python` · `FastAPI` · `React` · `Three.js` · `ChromaDB` · `NetworkX` · `LoRA` · `MLflow` · [live](https://civilization-os-murex.vercel.app) · [TCMF write-up](https://github.com/zaidwhy/CivilizationOS/blob/main/docs/tcmf.md)

### [Recall](https://github.com/zaidwhy/recall) - spatial memory you can talk to

*Point, ask out loud, get back the exact frame the camera saw it in.*

Point a phone camera at your space, ask out loud where you left something, get a spoken answer with the exact frame it was seen in. The voice model does not guess locations - it calls a tool that searches a vector store built from what the camera actually recorded.

```
Eval:         Recall@1 100% (10/10) · Recall@3 100% (10/10) · median latency 149ms
Embeddings:   all-MiniLM-L6-v2 via ONNX, fully local, zero embedding cost
Quota guard:  120s floor between vision calls, on-screen daily budget counter
```

`Python` · `FastAPI` · `React` · `ChromaDB` · `ONNX` · `WebSocket`

### [autocto](https://github.com/zaidwhy/autocto) - where the risk in a repo lives, from its git history alone

*The file to review first is the one that changes most and branches most.*

Five analyzers, no LLM and zero runtime dependencies: bug hotspots (churn x complexity), duplicated logic (token-shingle Jaccard), maintenance cost (size x churn x (1 + fan-in)), architectural debt (Tarjan cycles, god files, layering violations), and a migration planner that orders proposed changes with a topological sort. I/O lives in one `analyze_repo()` per analyzer, with the `git log` call behind an injectable seam; everything underneath is a pure function. 107 tests.

```
$ autocto hotspots ../recall --limit 3
frontend/src/App.jsx   churn 41 x complexity 129 = 5289
backend/main.py        churn 41 x complexity  89 = 3649
backend/memory.py      churn 11 x complexity  49 =  539
```

`Python` · `pipx install repo-autocto` · [PyPI](https://pypi.org/project/repo-autocto/)

### [Agent Factory](https://github.com/zaidwhy/agent-factory) - a build pipeline with frozen contracts

*The contract freezes before the code does, so two agents can build in parallel without seeing each other's work.*

Six specialised agents turn a one-line idea into a tested, runnable project. It is not a code generator; it is a pipeline with contracts. The architect **freezes an API contract before backend and frontend build in parallel from it**, which is the only reason two agents' output stays compatible without either one seeing the other's code. The reviewer is read-only by design. The debugger is the only agent permitted to execute, and is graded on what it fixes rather than what it writes.

Shipped 3 full projects end to end in test runs. On [Receipts.dev](https://github.com/zaidwhy/receipts-dev): 92 files, 16 bugs found and fixed, 0 type errors, 0 lint errors.

<details>
<summary>More systems</summary>

<br>

- **[personal-llm](https://github.com/zaidwhy/personal-llm)** - local-first memory + RAG kernel. 188 offline tests, fully mocked, zero-key CI. Plan-act-reflect agent loop, 4 permission-tiered tools including an SSRF-guarded fetch, full audit log.
- **[second-brain](https://github.com/zaidwhy/second-brain)** - vault ingestion, auto-linking, offline knowledge-graph viewer. 110 tests.
- **[github-pr-agent](https://github.com/zaidwhy/github-pr-agent)** - repo analysis, issue triage, PR planning. 65 tests.
- **[DreamOS](https://github.com/zaidwhy/dreamos-college-project)** - semantic file-management OS shell.
- **[resume-job-fit-ai](https://github.com/zaidwhy/resume-job-fit-ai)** - resume-to-job fit scoring with truthful rewrites. 42 unit tests, CI on every push, Pydantic-validated structured output.

</details>

---

## V. Production work

### [Zabira Academy](case-studies/zabira-academy.md) - 27 merged PRs into a live product I did not build

Twelve days. +8,838 / -1,619 across 557 file changes, into a production learning platform with real users, every change reviewed and merged by the repository owner.

Security hardening (exception leakage across 226 files, Origin checks on 60 mutating endpoints, a sanitiser bypass, session revocation), an end-to-end suite covering the seven launch-critical flows behind a CI gate, and a sitewide search feature built from the backend through to voice input.

Including the one where CI went red on my branch and the cause turned out to **predate my work by three days** - a registration validation rule silently failing a test fixture, bisected through the run history and confirmed from the failed run's Playwright snapshot. Reading the evidence beat blaming my own diff.

The codebase is private, so the [case study](case-studies/zabira-academy.md) is the record.

---

### Support analytics dashboard - built from scratch during an AI internship at Pratyaya Limited

A customer-support analytics dashboard for a WhatsApp support team (Python, FastAPI, pandas, Jinja2): daily to month-to-date performance, per-agent response, resolution and CSAT, and bot versus agent resolution, each figure shown beside the support platform's own report.

Reconciled to that platform's reports: all 10 aggregate totals match exactly and 53 of 55 per-agent response-time averages agree within one second; a figure that differs is clickable and explains why. Chat transcripts are read through a read-only, test-enforced API client to classify why chats were handed from bot to agent, which shrank the unexplained "other" bucket to about 1%. Role-based login, argon2 password hashing, a strict content-security policy, 146 automated tests, and zero accessibility violations in an axe-core audit of all 7 pages.

The repository is private and the data is the company's, so there is no link and nothing here describes a customer or a business figure.

---

## Engineering work

### [CivilizationOS](case-studies/civilizationos.md) - a retrieval method that failed its own benchmark, in public

A multi-agent society simulation, live at [civilization-os-murex.vercel.app](https://civilization-os-murex.vercel.app). TCMF, its causal-retrieval method, is benchmarked against six baselines - the first version scored recall@5 0.02 on the exact signal it was built to exploit, and the benchmark is what caught it, not a hunch. 76 API tests, 152 benchmark tests, both in CI.

### [Personal LLM](case-studies/personal-llm.md) - one kernel, three apps, and an eval suite that argued with itself

A local-first memory and RAG engine imported by three separate apps instead of rebuilt per app. Building its offline eval suite surfaced three real issues on the first run - two bugs in the eval harness and one artifact of a synthetic test double - each root-caused separately before any threshold was touched. 188 kernel tests, 363 across the fleet, 7 eval suites, all offline.

---

## Open source

**Merged:**

- **[jd/tenacity #668](https://github.com/jd/tenacity/pull/668)** · 8.8k stars - fixed static typing for `@retry`-decorated instance methods so bound-method signatures survive the decorator under mypy strict.
- **[dry-python/returns #2480](https://github.com/dry-python/returns/pull/2480)** · 4.4k stars - relaxed `future()` / `future_safe()` parameter types from `Coroutine` to the broader `Awaitable` protocol.
- **[memgraph/gqlalchemy #390](https://github.com/memgraph/gqlalchemy/pull/390)** - added unary-operator support (`IS NOT NULL`) to the query builder, with tests, docs, and a signed CLA.

**Open:** [gqlalchemy #392](https://github.com/memgraph/gqlalchemy/pull/392) (`ON CREATE` / `ON MATCH` clauses) · [django-taggit #944](https://github.com/jazzband/django-taggit/pull/944) (`remove_by_slug()` on `TaggableManager`).

**And one that closed unmerged, which is the more useful story:** [google/adk-python #6190](https://github.com/google/adk-python/pull/6190) fixed an `Optional[List[str]]` hint that broke the CLI parser. It survived a full maintainer review round - I root-caused a CI failure to a leftover repro script breaking Mypy and the linter, fixed it, got an LGTM - and then a maintainer's own commit resolved the same underlying bug first and the PR closed. Reviewed, correct, and beaten to it.

---

## Stack

```
languages   Python 3.11+ · TypeScript · SQL
ai          RAG architectures · multi-agent orchestration · LoRA fine-tuning
            structured outputs · evals · vector search · agent tool loops
backend     FastAPI · WebSocket · Node.js · Pydantic
frontend    React · Vite · Three.js
data        ChromaDB · SQLite · pgvector · NetworkX · sentence-transformers
infra       Docker · GitHub Actions · Vercel · Render · GCP
```

---

## VI. Provenance

<img src="https://raw.githubusercontent.com/zaidwhy/zaidwhy/main/assets/chain-of-custody.svg" alt="Chain of custody: a signed commit leads to an ed25519 signature verified by GitHub, to an immutable release tag, to a Zenodo DOI with an independent timestamp, to an ORCID bound to a person." width="100%">

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

Every commit on this account is signed with the key below. The artwork on this page is hand-authored SVG, served from this repository, and carries an authorship manifest in its source.

```
Zaid Ali Syed
ORCID  0009-0003-4313-1510
PGP    EFE9 4832 B2B9 80D9 B583  91F2 8FAA BCC1 B1AC 09E5
```

Full signed statement: **[PROVENANCE.md](PROVENANCE.md)** · verify with `gpg --verify` on [`PROVENANCE.sig.txt`](PROVENANCE.sig.txt)

---

**[Portfolio](https://www.solstine.dev)** · **[LinkedIn](https://linkedin.com/in/zaid-ali-syed)** · Open to AI engineer internships and applied AI roles.
