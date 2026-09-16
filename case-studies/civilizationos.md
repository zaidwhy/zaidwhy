# Case study: a retrieval method that failed its own benchmark, in public

**A multi-agent society simulation with a named retrieval method (TCMF), benchmarked against
six baselines - and the headline finding is that the first version of that method scored
0.02 recall on the exact signal it was built to exploit, where the signal alone reaches
1.00. The fix, the benchmark, and the correction are all in the repository.**

Live: [civilization-os-murex.vercel.app](https://civilization-os-murex.vercel.app). Code:
[github.com/zaidwhy/CivilizationOS](https://github.com/zaidwhy/CivilizationOS).

---

## What it is

Ten autonomous citizens live in a small simulated town, following routines, forming
relationships, and accumulating memory. Five institutions - government, economy,
healthcare, media, police - are each governed by a council of five AI specialists who
debate before acting. Inject a crisis and the town responds: citizens react through the
lens of their occupation, councils deliberate on-screen turn by turn, and the causal
history of what led to what builds up in a queryable graph.

Standard retrieval-augmented generation finds documents by semantic similarity. That is
not enough here: when a council needs to decide what caused a crisis, the memory that
matters is not the one that sounds most like the crisis, it is the one that was actually
upstream of it in the causal chain. That gap is what TCMF (Temporal-Causal Memory Fusion)
exists to close.

---

## The formula that failed its own benchmark

TCMF fuses two signals: an episodic score (relevance x recency x importance, the
Generative-Agents formula) and a causal-boost score (how close a memory sits to the
actual causal ancestors of the current crisis in a graph, weighted by depth).

The first version combined them multiplicatively:
`episodic_score x (1 + lambda x causal_boost)`.

It looked reasonable. It also scored **recall@5 of 0.02** on the exact causal-ancestor
retrieval task it was designed for, in a benchmark run against six baselines over 300
scenarios - where the causal signal alone, unfused, reaches 1.00. The reason is simple
once you see it: a root-cause memory is often semantically *distant* from the crisis it
eventually caused. Its episodic score is near zero. Multiplying a near-zero base by any
boost, however large, stays near zero. The fusion could never lift the memory that
mattered most.

The fix was additive, not multiplicative: `normalize(episodic_score) + lambda x
causal_boost`, with episodic scores min-max normalized across the candidate pool so the
causal term can actually compete instead of being crushed by it. That recovered the
signal in full. Both versions, the failure and the fix, are in
[`docs/tcmf.md`](https://github.com/zaidwhy/CivilizationOS/blob/main/docs/tcmf.md) and
benchmarked in [`research/tcmf_paper/`](https://github.com/zaidwhy/CivilizationOS/tree/main/research/tcmf_paper)
(152 tests, running in CI).

I did not discover this by inspection. I discovered it by building the benchmark first
and then reading what it said, which is the only way a wrong formula that "looks right"
ever gets caught.

---

## A CI failure that was really a missing dependency, not a bug

When I wired the 152-test benchmark suite into GitHub Actions CI, four figure-generation
tests failed to even collect: `ModuleNotFoundError: No module named 'matplotlib'`.
Matplotlib is a real dependency of the benchmark's figure pipeline, declared in its own
`requirements-bench.txt` - but CI's install step only ran the API's `requirements.txt`,
which never needed to know about figure generation. The fix was one line, adding the
bench requirements file to the CI install step, not a code change to the tests
themselves. The distinction mattered: it would have been easy to "fix" this by weakening
or skipping the tests, which would have hidden a real dependency gap instead of closing
it.

---

## Making a public demo survive being public

The live deploy runs `POST /crisis` open to any visitor, deliberately - that is the point
of a demo. But `POST /speed` and the two manual crisis-resolve routes change the
simulation for *every* viewer at once, and the crisis-injection endpoint spends real LLM
budget when the premium tier is configured. Neither was gated.

Fixed both, with tests: the two state-changing routes now require an `X-Admin-Token`
header when one is configured (open only on an unconfigured local instance), and crisis
injection now has a per-UTC-day cap on top of its existing 30-second cooldown, so a
patient visitor cannot walk the spend cap down one request at a time. Five tests cover
the admin guard and the daily-cap boundary, including that the guard stays open when no
token is configured at all - a demo instance should not lock itself out.

---

## Architecture at a glance

FastAPI backend, React + Three.js frontend, a three-tier model router (local Ollama in
development, Gemini's free tier, Claude/OpenRouter behind a spend cap in the public
deploy), and no external database - the whole simulation lives in one Python process,
which is a deliberate simplicity tradeoff for a demo, not an oversight. Full write-up,
including failure modes and what would need to change to scale past a demo, in
[`ARCHITECTURE.md`](https://github.com/zaidwhy/CivilizationOS/blob/main/ARCHITECTURE.md).

---

## The numbers

| | |
|---|---|
| Backend tests | 76 |
| Benchmark tests (TCMF vs. 6 baselines, 300 scenarios) | 152 |
| The bug the benchmark caught | recall@5 0.02 vs. 1.00 (multiplicative vs. additive fusion) |
| Deploy | Vercel (frontend) + Render (API, free tier) |
| Cost in local development | $0 (Ollama only) |

---

## Why this is the strongest evidence of research instinct in my portfolio

Anyone can publish the version of a method where it worked. The version that scored 0.02
is still in this repository, in the same file as the fix, because the failure is the
argument: I built the measurement before I trusted the method, and when the method
failed, the benchmark is what told me, not a hunch.
