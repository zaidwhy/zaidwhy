# Case study: one kernel, three apps, and an eval suite that argues with itself

**A local-first memory and retrieval-augmented-generation engine, built once and
imported by three separate applications instead of being rebuilt for each. 168 tests on
the kernel itself, 334 across the three apps that depend on it, and a seven-suite offline
eval harness whose first honest result was that its own test fixture was wrong - not the
kernel.**

Code: [github.com/zaidwhy/personal-llm](https://github.com/zaidwhy/personal-llm).

---

## What it is

Ingest notes, markdown, or PDFs; retrieve them ranked by similarity, importance, and
recency; answer questions grounded in what was actually ingested, with citations - and an
honest "I don't have this in memory" instead of a guess when nothing qualifies. The
engine is UI-agnostic: a CLI, a FastAPI gateway, and a Streamlit chat interface are all
thin clients over the same `Engine` object, and two other projects in the same fleet
(second-brain, a knowledge-graph layer; github-pr-agent, a PR-triage tool) import the
kernel directly rather than reimplementing memory and retrieval.

---

## Building an eval suite that caught its own test's mistake before it could hide anything

Tests check that code does not crash. They do not check that a RAG pipeline actually
retrieves the right thing, refuses when it should, or never invents a citation. So I
built seven offline, deterministic eval suites - correctness, retrieval (recall@1/@3),
refusal, hallucination, latency, prompt-injection isolation, and a regression gate over
fixed thresholds - against a small fixed fixture corpus, no network call, no API key.

The first run failed three of the five graded suites. The honest process was to find out
why before touching anything:

1. **Hallucination showed 6 violations out of 6 answers.** Every single answer looked
   like it was inventing sources. It was not - my eval code called `ask()` with its
   default retrieval width (8) while checking citations against a narrower retrieval
   window (3) elsewhere in the same suite. Once both calls used the same `k`, violations
   dropped to zero. A bug in the harness, not the kernel.

2. **Retrieval scored 50% recall@1** on a six-document fixture about one fictional
   company's history. The offline embedder used for evals is a crude 32-dimension
   hash-of-words function (deliberately simple, since the same double is what the unit
   tests use) - and with that little resolution, six documents sharing heavy vocabulary
   ("the company," "in 2021," "the team") were indistinguishable to it. I rebuilt the
   fixture as six genuinely unrelated personal notes (a sourdough starter, a bike
   repair, a passport appointment) and separately gave the eval suite a better offline
   embedder - deterministic TF-IDF, still no network - specifically because the point of
   these suites is to test the *pipeline's logic*, not the crudeness of a hash function
   never meant to carry retrieval-quality weight.

3. **Refusal then failed in the opposite direction**: genuinely unrelated questions
   ("what is the capital of France") were not refusing. Tracing it down: a query with
   zero vocabulary overlap with the corpus embedded as a literal all-zero vector, and
   the kernel's similarity formula (`1 - squared_L2/2`, correct for two unit vectors)
   turns a zero vector against any real vector into exactly 0.5 similarity by
   construction - comfortably over the refusal threshold, for every unrelated question,
   regardless of wording. That is an artifact of my synthetic embedder producing a
   degenerate input the formula was never designed for, not a kernel bug: a real
   embedding model never emits a true zero vector. The fix lives entirely in the eval
   harness - an out-of-vocabulary fallback that hashes into the same dimensional space
   so it never degenerates - and is covered by two tests of its own, including one that
   specifically checks the fallback doesn't accidentally re-introduce the same
   collision problem in a too-small vocabulary.

All seven suites pass now, deterministically - verified by running the full suite three
times and diffing every non-timing field byte-for-byte identical, plus two dedicated
tests that assert on it. The regression gate runs in CI on every push and fails the build
if any of it slips.

---

## Why the debugging mattered more than the green checkmark

A weaker version of this suite would have declared victory the moment every number
looked plausible, or worse, would have quietly loosened the thresholds until the
failures went away. Two of the three failures here were real bugs in eval code that a
less careful pass would have blamed on the kernel; the third was a genuine, if subtle,
mismatch between a synthetic test double and the real math it was standing in for. Root-
causing each one separately, rather than patching the symptom, is what makes the final
green result mean something.

---

## The numbers

| | |
|---|---|
| Kernel tests | 168 (334 across the three apps that import it) |
| Eval suites | 7, all passing, fully deterministic |
| Correctness / retrieval / refusal | 100% / 100% recall@1 & @3 / 100% |
| Hallucination violations | 0 |
| Prompt-injection isolation | pass (retrieved content never reaches the system-role message) |
| Network calls or API keys needed to run any of it | 0 |
