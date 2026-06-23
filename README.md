<div align="center">

[![Typing SVG](https://readme-typing-svg.demolab.com?font=JetBrains+Mono&weight=600&size=20&duration=3000&pause=1000&color=58A6FF&center=true&vCenter=true&width=700&lines=Building+AI+that+remembers+%E2%80%A2+reasons+%E2%80%A2+simulates.;Multi-agent+systems+%7C+RAG+architectures+%7C+LLM+orchestration;Python+%C2%B7+Gemini+%C2%B7+Claude+%C2%B7+FastAPI+%C2%B7+React;Open+to+AI+engineer+%2F+internship+opportunities.)](https://git.io/typing-svg)

</div>

---

I build AI systems that go beyond chatbots.

Not wrappers. Not demos. Real architectures: multi-agent coordination, novel RAG retrieval, voice-vision pipelines, fine-tuned models shipped end-to-end with tests, CI, and evals.

Building in public. Looking for **AI engineer / applied AI internship** roles.

---

## Flagship Projects

### [CivilizationOS](https://github.com/syzayd/CivilizationOS) - Multi-Agent AI Society

> A living simulation: 10 autonomous citizen-agents + 5 institutional councils (35 AI agents) debate, remember, and react to injected crises - Pandemic, Drought, Cyberattack, Election, Crime Wave.

**Novel contribution - Temporal-Causal Memory Fusion (TCMF):**
Standard RAG retrieves by semantic similarity alone. TCMF fuses two streams:

```
AGORA stream    - citizen episodic memories scored by relevance x recency x importance
PANTHEON stream - societal causal graph (NetworkX DiGraph): crisis -> decision -> outcome

Fused score = episodic_score(m, q) x (1 + lambda x causal_boost(m))
```

A witness to a root cause outranks someone who heard about it second-hand. No off-the-shelf RAG system does this.

```
3-tier LLM router:  Ollama/Qwen2.5-3B ($0) -> Gemini Flash ($0) -> Claude API (~$0.002/debate)
Fine-tuning:        LoRA on Qwen2.5-3B | MLflow tracking | persona-consistency eval harness
Full-stack:         FastAPI + WebSocket <-> React + PixiJS isometric city UI
Tests:              48 passing
Total cost:         Under $5 to build. 118 commits.
```

`Python` `TypeScript` `FastAPI` `React` `ChromaDB` `Ollama` `Gemini` `Claude` `LoRA` `MLflow` `NetworkX`

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

## Tech Stack

```python
ai_ml    = ["RAG architectures", "multi-agent systems", "LoRA fine-tuning",
            "vector DBs", "LLM orchestration", "structured outputs", "evals"]

apis     = ["Gemini", "Claude (Anthropic)", "Ollama", "Gemini Live"]

backend  = ["Python 3.11+", "FastAPI", "WebSocket", "Node.js"]

frontend = ["React", "TypeScript", "Vite", "PixiJS"]

infra    = ["AWS", "Google Cloud", "Docker", "Streamlit Cloud", "cloudflared"]

tracking = ["MLflow", "Pydantic", "ChromaDB", "SQLite", "GitHub Actions CI"]
```

---

## Currently

- Building in public - [LinkedIn](https://linkedin.com/in/zaidsyed)
- Open to **AI engineer internships**, **applied AI roles**, early-stage startups
- Next: demo video for Recall + open-sourcing CivilizationOS fully

---

<div align="center">

![GitHub Stats](https://github-readme-stats.vercel.app/api?username=syzayd&show_icons=true&theme=github_dark&hide_border=true&bg_color=0d1117&title_color=58a6ff&icon_color=58a6ff&text_color=8b949e&hide=issues&count_private=true)

[![Top Languages](https://github-readme-stats.vercel.app/api/top-langs/?username=syzayd&layout=compact&theme=github_dark&hide_border=true&bg_color=0d1117&title_color=58a6ff&text_color=8b949e&hide=html,css)](https://github.com/syzayd)

</div>
