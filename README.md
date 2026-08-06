<div align="center">

[![Typing SVG](https://readme-typing-svg.demolab.com?font=JetBrains+Mono&weight=600&size=20&duration=3000&pause=1000&color=58A6FF&center=true&vCenter=true&width=700&lines=Building+AI+that+remembers+%E2%80%A2+reasons+%E2%80%A2+simulates.;Multi-agent+systems+%7C+RAG+architectures+%7C+LLM+orchestration;Python+%C2%B7+Gemini+%C2%B7+Claude+%C2%B7+FastAPI+%C2%B7+React;Open+to+AI+engineer+%2F+internship+opportunities.)](https://git.io/typing-svg)

</div>

---
Not just prompting.
I build AI systems that go beyond chatbots.

Not wrappers. Not demos. Real architectures: multi-agent coordination, novel RAG retrieval, voice-vision pipelines, fine-tuned models, autonomous build pipelines shipped end-to-end with tests, CI, and evals.

Building in public. Looking for **AI engineer / applied AI internship** roles.

---

## Flagship Projects

### [Agent Factory](https://github.com/syzayd/agent-factory) - 6-Agent Pipeline That Ships Full Projects

> One command, `/forge`, and a team of six specialized agents (idea-hunter, architect, backend-engineer, frontend-engineer, reviewer, debugger) turns nothing into a tested, runnable project.

**Not a code generator. A pipeline with contracts.** The architect freezes an API contract before backend and frontend build in parallel from it - that's what keeps two agents' output compatible without either seeing the other's code. The reviewer is read-only by design; the debugger is the only agent that runs code, graded on fixing what it finds rather than writing more.

```
Agents:       idea-hunter -> architect -> backend + frontend (parallel) -> reviewer -> debugger -> devops-engineer
Proof:        3 full projects shipped end-to-end in test runs - PinPoint, DriftGuard, Receipts.dev
Receipts.dev: 92 files, 16 bugs found and fixed (1 critical, 4 high), 0 type errors, 0 lint errors
Contract:     runs/<timestamp>/ file handoff - architect's API contract is the single source of truth
Roadmap:      Phase 1 (Claude Code subagents, live) -> Phase 2 (Python SDK orchestrator, factory.py, live)
```

`Claude Code Subagents` `Anthropic Python SDK` `Multi-Agent Orchestration` `Streaming Tool Loop` `ThreadPoolExecutor`

---

### [Receipts.dev](https://github.com/syzayd/receipts-dev) - Prove Skills With Code, Not Buzzwords

> AI-powered skill verification from real Git history. Every skill on the profile deep-links to the actual commit that proves it, via a recruiter chat that can only cite real diffs and never invent a claim.

Built by Agent Factory's full pipeline in a single run: idea to architecture to parallel backend/frontend to review to debug. GitHub OAuth with Fernet-encrypted tokens, an async GitHub client with retry, a pgvector code-chunk retriever, and grounded chat with hallucination-proof citation validation.

`Next.js 15` `FastAPI` `pgvector` `GitHub OAuth` `Celery` `Grounded RAG`

---

### [Personal LLM](https://github.com/syzayd/personal-llm) - Local-First Memory + RAG Kernel

> One memory engine, built once, imported by everything else: a local-first, privacy-preserving memory + RAG core (SQLite + ChromaDB + hybrid model router) that answers with citations and refuses honestly when it doesn't know.

**Not a demo - infrastructure.** Three downstream apps import it instead of rebuilding retrieval: [second-brain](https://github.com/syzayd/second-brain) (vault ingestion, auto-linking, offline knowledge-graph viewer - 40 tests) and [github-pr-agent](https://github.com/syzayd/github-pr-agent) (repo analysis, issue triage, PR planning - 32 tests) are public; DreamOS (an Electron AI command bar over the same engine) ships when its demo video does.

```
Tests:        100 offline, fully mocked - zero-key CI on every push
Agent layer:  plan-act-reflect loop, 4 permission-tiered tools (incl. SSRF-guarded web fetch), full audit log
Voice/vision: faster-whisper STT (offline, free) + OCR ingestion; native-crash inputs pre-validated (PyAV)
Security:     token-authenticated HTTP gateway; browser-Origin requests rejected outright
```

`Python` `FastAPI` `ChromaDB` `SQLite` `sentence-transformers` `Ollama` `Gemini` `faster-whisper`

---

### [CivilizationOS](https://github.com/syzayd/CivilizationOS) - Multi-Agent AI Society

> A living simulation: 10 autonomous citizen-agents + 5 institutional councils (35 AI agents) debate, remember, and react to injected crises - Pandemic, Drought, Cyberattack, Election, Crime Wave, and now self-generated emergent crises.

**Novel contribution - Temporal-Causal Memory Fusion (TCMF):**
Standard RAG retrieves by semantic similarity alone. TCMF fuses two streams:

```
AGORA stream    - citizen episodic memories scored by relevance x recency x importance
PANTHEON stream - societal causal graph (NetworkX DiGraph): crisis -> decision -> outcome

Fused score = episodic_score(m, q) x (1 + lambda x causal_boost(m))
```

A witness to a root cause outranks someone who heard about it second-hand. No off-the-shelf RAG system does this. Full design write-up with code and tradeoffs: [docs/tcmf.md](https://github.com/syzayd/CivilizationOS/blob/main/docs/tcmf.md)

Validated it with a controlled benchmark against 6 baseline retrieval strategies: the original multiplicative fusion scored 0.00 on the causal signal it was meant to exploit, a fixed normalized-additive version recovered it and beat every single-signal baseline in a mixed regime. A follow-up 60-scenario study showed retrieval choice changes the model's actual decision, not just its confidence.

**Latest additions:** sustained-fear auto-crisis injection so the society generates its own emergencies, per-council effectiveness scoring (debate to verdict to 60-tick fear delta), union-find citizen faction detection on mutual affinity, and a Story Rewind scrubber over the full causal timeline.

```
3-tier LLM router:  Ollama/Qwen2.5-3B ($0) -> Gemini Flash ($0) -> Claude API (~$0.002/debate)
Fine-tuning:        LoRA on Qwen2.5-3B | MLflow tracking | persona-consistency eval harness
Full-stack:         FastAPI + WebSocket <-> React + Three.js 3D city (replaced the earlier PixiJS UI)
Tests:              61 passing
Total cost:         Under $5 to build.
```

Live now: [civilization-os-murex.vercel.app](https://civilization-os-murex.vercel.app) (frontend) - backend on Render.

`Python` `TypeScript` `FastAPI` `React` `Three.js` `ChromaDB` `Ollama` `Gemini` `Claude` `LoRA` `MLflow` `NetworkX`

---

### [Recall](https://github.com/syzayd/recall) - Spatial AI Memory

> Point your phone camera at your space. Ask out loud "where did I leave my keys?" Get a spoken answer with the exact frame it was seen in.

**Not another AI wrapper.** Persistent spatial memory across sessions. Time-decay re-ranking. Gemini Live function-calling into local ChromaDB. The voice model doesn't hallucinate locations - it calls a tool that searches a vector store built from what the camera actually saw.

```
Eval (June 2026):   Recall@1 100% (10/10) | Recall@3 100% (10/10) | Median latency 149ms
Embeddings:         all-MiniLM-L6-v2 via ONNX - fully local, zero embedding cost
Voice:              Gemini Live push-to-talk with function calling
Quota management:   120s minimum between vision calls + daily budget counter on-screen
Total commits:      162
```

Live now: deployed on Render.

`Python` `FastAPI` `React` `ChromaDB` `Gemini Live` `ONNX` `WebSocket` `cloudflared`

---

### [resume-job-fit-ai](https://github.com/syzayd/resume-job-fit-ai) - AI Resume Scorer | [Live Demo](https://resume-job-fit-ai.streamlit.app)

> Fit scoring, keyword analysis, AI-rewritten bullet diffs, multi-tone cover letter, interview prep, skills gap roadmap, LinkedIn optimizer - one click.

```
Deployed:    Streamlit Community Cloud (live now, free tier, no credit card)
Tests:       29 unit tests | GitHub Actions CI on every push
Outputs:     Pydantic-validated structured JSON - no brittle string parsing
Features:    12+ tools: multi-job comparison, application tracker, cover letter, DOCX export
```

`Python` `Gemini` `Streamlit` `Pydantic` `SQLite` `pdfplumber` `GitHub Actions`

---

## Autonomous Build Agent

I run a nightly agent across my own 12-repo project fleet: it triages the next task, implements it, runs the tests, and opens a PR - every change gated by CI and a human merge, nothing lands unreviewed. Shipped and merged 30+ PRs in the past month. Coordination records (task queue, run logs) live in a private repo since they're internal tooling, not a product.

---

## Open Source

**[jd/tenacity #668](https://github.com/jd/tenacity/pull/668)** - MERGED. Fixed static typing for `@retry`-decorated instance methods so bound-method signatures survive the decorator under mypy strict.

**[dry-python/returns #2480](https://github.com/dry-python/returns/pull/2480)** - MERGED. Relaxed `future()` / `future_safe()` parameter types from `Coroutine` to the broader `Awaitable` protocol.

**[memgraph/gqlalchemy #390](https://github.com/memgraph/gqlalchemy/pull/390)** - open PR adding unary-operator support (`IS NOT NULL`) to the query builder: 4 tests, docs, CI green, CLA signed. Found and scoped with my own triage pipeline (AutoCTO), implemented keylessly via git + the GitHub CLI.

**[memgraph/gqlalchemy #392](https://github.com/memgraph/gqlalchemy/pull/392)** - open PR adding `ON CREATE` / `ON MATCH` clauses to the same query builder, with tests and docs.

**[jazzband/django-taggit #944](https://github.com/jazzband/django-taggit/pull/944)** - open PR adding `remove_by_slug()` to `TaggableManager`, with tests.

**[google/adk-python #6190](https://github.com/google/adk-python/pull/6190)** - fixed an `Optional[List[str]]` type hint bug in `cleanup_unused_files` that broke the CLI parser (labeled "good first issue" by Google's ADK team). Survived a full maintainer review round - root-caused a CI failure to a leftover repro script breaking Mypy and the pyink linter, fixed it, and got an LGTM - before a maintainer's own commit resolved the same underlying bug first, closing the PR unmerged.

---

## Tech Stack

```python
ai_ml    = ["RAG architectures", "multi-agent systems", "LoRA fine-tuning",
            "vector DBs", "LLM orchestration", "structured outputs", "evals",
            "agent pipelines with frozen API contracts"]

apis     = ["Gemini", "Claude (Anthropic)", "Ollama", "Gemini Live"]

backend  = ["Python 3.11+", "FastAPI", "WebSocket", "Node.js"]

frontend = ["React", "TypeScript", "Vite", "Three.js", "PixiJS"]

infra    = ["AWS", "Google Cloud", "Docker", "Streamlit Cloud", "cloudflared", "Vercel"]

tracking = ["MLflow", "Pydantic", "ChromaDB", "SQLite", "GitHub Actions CI"]
```

---

## Currently

- Portfolio - [zaidalisyed.vercel.app](https://zaidalisyed.vercel.app) | [source](https://github.com/syzayd/portfolio) (Next.js 16, Three.js WebGL, GSAP)
- Building in public - [LinkedIn](https://linkedin.com/in/zaid-ali-syed)
- Open to **AI engineer internships**, **applied AI roles**, early-stage startups
- Next: Agent Factory Phase 2 (Python SDK orchestrator) hardening, open-sourcing CivilizationOS fully

---

<div align="center">

![GitHub Stats](https://github-readme-stats.vercel.app/api?username=syzayd&show_icons=true&theme=github_dark&hide_border=true&bg_color=0d1117&title_color=58a6ff&icon_color=58a6ff&text_color=8b949e&hide=issues&count_private=true)

[![Top Languages](https://github-readme-stats.vercel.app/api/top-langs/?username=syzayd&layout=compact&theme=github_dark&hide_border=true&bg_color=0d1117&title_color=58a6ff&text_color=8b949e&hide=html,css)](https://github.com/syzayd)

</div>
