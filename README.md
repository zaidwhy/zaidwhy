<div align="center">

[![Typing SVG](https://readme-typing-svg.demolab.com?font=JetBrains+Mono&weight=600&size=20&duration=3000&pause=1000&color=58A6FF&center=true&vCenter=true&width=700&lines=Building+AI+that+remembers+%E2%80%A2+reasons+%E2%80%A2+simulates.;Multi-agent+systems+%7C+RAG+architectures+%7C+LLM+orchestration;Python+%C2%B7+Gemini+%C2%B7+Claude+%C2%B7+FastAPI+%C2%B7+React;Open+to+AI+engineer+%2F+internship+opportunities.)](https://git.io/typing-svg)

</div>

---

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

**Latest additions:** sustained-fear auto-crisis injection so the society generates its own emergencies, per-council effectiveness scoring (debate to verdict to 60-tick fear delta), union-find citizen faction detection on mutual affinity, and a Story Rewind scrubber over the full causal timeline.

```
3-tier LLM router:  Ollama/Qwen2.5-3B ($0) -> Gemini Flash ($0) -> Claude API (~$0.002/debate)
Fine-tuning:        LoRA on Qwen2.5-3B | MLflow tracking | persona-consistency eval harness
Full-stack:         FastAPI + WebSocket <-> React + Three.js 3D city (replaced the earlier PixiJS UI)
Tests:              54 passing
Total cost:         Under $5 to build.
```

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

`Python` `FastAPI` `React` `ChromaDB` `Gemini Live` `ONNX` `WebSocket` `cloudflared`

---

### [resume-job-fit-ai](https://github.com/syzayd/resume-job-fit-ai) - AI Resume Scorer | [Live Demo](https://resume-job-fit-ai.streamlit.app)

> Fit scoring, keyword analysis, AI-rewritten bullet diffs, multi-tone cover letter, interview prep, skills gap roadmap, LinkedIn optimizer - one click.

```
Deployed:    Streamlit Community Cloud (live now, free tier, no credit card)
Tests:       26 unit tests | GitHub Actions CI on every push
Outputs:     Pydantic-validated structured JSON - no brittle string parsing
Features:    12+ tools: multi-job comparison, application tracker, cover letter, DOCX export
```

`Python` `Gemini` `Streamlit` `Pydantic` `SQLite` `pdfplumber` `GitHub Actions`

---

## Open Source

**[google/adk-python #6190](https://github.com/google/adk-python/pull/6190)** - fixed an `Optional[List[str]]` type hint bug in `cleanup_unused_files` that broke the CLI parser (labeled "good first issue" by Google's ADK team). Went through a maintainer review round: root-caused a CI failure to a leftover repro script breaking Mypy and the pyink linter, removed it, verified pyink/isort/ruff clean locally, and re-pushed a single focused fix.

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
