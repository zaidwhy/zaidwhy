#!/usr/bin/env python3
"""Draws the header plate for each public repository, in the profile's survey style.

Each plate carries the repository's thesis, the three facts it is judged by, a
motif for what kind of work it is, and a core strip drawn from that
repository's own commit history: one band per week from the first commit to
the newest, darker where more was laid down. Facts are copied from
PROFILE-FACTS.yaml or the repository's own README; change them there first.

usage: python scripts/repo_plates.py <out_dir> [repo ...]
writes <out_dir>/<repo>.svg; needs an authenticated `gh` for the commit history.
"""
import math
import os
import subprocess
import textwrap
import sys
from collections import Counter
from datetime import datetime, timedelta
from xml.sax.saxutils import escape

from core_sample import INK, PAPER, TINTS
from plates import CARD, WAX, text

OWNER = "zaidwhy"
W, H = 1200, 330
NARROW_W = 520  # phone plate, served under 600 px

REPOS = {
    "CivilizationOS": ("system", "CivilizationOS", "A causal memory that has to outrank a rumour with a witness, not a similar-sounding one.",
                       ["10 agents, 5 councils", "TCMF against 6 baselines, 300 scenarios", "live on Vercel"]),
    "recall": ("system", "Recall", "Point, ask out loud, and get back the exact frame the camera saw it in.",
               ["Recall@1 10 of 10", "149 ms median latency", "local ONNX embeddings"]),
    "agent-factory": ("system", "Agent Factory", "The contract freezes before the code does, so two agents can build in parallel.",
                      ["6 specialised agents", "frozen API contracts", "3 projects shipped in test runs"]),
    "resume-job-fit-ai": ("system", "Resume Job-Fit AI", "Scores a resume against a job description, and rewrites without inventing experience.",
                          ["49 unit tests", "Pydantic-validated output", "CI on every push"]),
    "autocto": ("tool", "autocto", "The file to review first is the one that changes most and branches most.",
                ["5 analyzers, no LLM", "162 tests", "pipx install repo-autocto"]),
    "personal-llm": ("kernel", "Personal LLM", "One memory kernel, sunk once and imported by three apps.",
                     ["181 offline tests", "answers with citations or refuses", "keyless CI"]),
    "second-brain": ("chamber", "Second Brain", "A vault that links itself, built on the personal-llm kernel.",
                     ["116 tests", "auto-linking on ingest", "offline graph viewer"]),
    "github-pr-agent": ("chamber", "GitHub PR Agent", "The planning half of a pull-request agent: analyze, triage, plan.",
                        ["84 tests", "imports the personal-llm kernel", "no API key in CI"]),
    "dreamos-college-project": ("chamber", "DreamOS", "A file manager that finds things by what they mean, not where they were put.",
                                ["final-year B.Tech project", "imports the personal-llm kernel", "MGM University, IICT"]),
    "coldread": ("research", "COLD READ", "How long you stay anonymous depends on the model reading you, not on the text.",
                 ["50, 800 or 1600 words", "3 model families, negative control held", "DOI 10.5281/zenodo.22309660"]),
    "augur": ("research", "AUGUR", "A cutoff marks the edge of a corpus, not its centre.",
              ["1938 cutoff, answers 1899", "2 model families, 14 probes", "DOI 10.5281/zenodo.22309658"]),
    "longmemeval-key-audit": ("research", "LongMemEval Key Audit", "Does the benchmark's own evidence support its gold answers?",
                              ["protocol frozen at prereg-v1", "parked after 5 of 141 items", "no findings claimed"]),
}


def commit_days(repo):
    done = subprocess.run(["gh", "api", f"repos/{OWNER}/{repo}/commits?per_page=100", "--paginate",
                           "--jq", ".[].commit.author.date"], capture_output=True, text=True, timeout=120, check=True)
    return [datetime.fromisoformat(d.replace("Z", "+00:00")).date() for d in done.stdout.split()]


def motif(kind, x, y):
    if kind == "research":
        return (f'<rect x="{x - 22}" y="{y - 60}" width="44" height="120" rx="20" fill="#FBF7EC" stroke="{INK}" stroke-width="1.3"/>'
                f'<rect class="rise" x="{x - 18}" y="{y - 4}" width="36" height="60" rx="16" fill="{TINTS[2]}"/>'
                f'<rect x="{x - 28}" y="{y - 70}" width="56" height="11" fill="{INK}" fill-opacity=".85"/>')
    if kind == "system":
        return (f'<path d="M{x - 34} {y + 60}L{x} {y - 52}L{x + 34} {y + 60}M{x - 23} {y + 24}H{x + 23}M{x - 12} {y - 14}H{x + 12}" '
                f'stroke="{INK}" stroke-width="1.6" fill="none"/><circle cx="{x}" cy="{y - 58}" r="9" fill="{CARD}" stroke="{INK}" stroke-width="1.3"/>'
                f'<line x1="{x - 60}" y1="{y + 60}" x2="{x + 60}" y2="{y + 60}" stroke="#4E5A2C" stroke-width="3"/>')
    if kind == "kernel":
        rungs = "".join(f'<line x1="{x - 10}" y1="{yy}" x2="{x + 10}" y2="{yy}" stroke="{INK}" stroke-width=".6"/>' for yy in range(y - 56, y + 30, 11))
        return (f'<line x1="{x - 60}" y1="{y - 62}" x2="{x + 60}" y2="{y - 62}" stroke="#4E5A2C" stroke-width="3"/>'
                f'<rect x="{x - 10}" y="{y - 62}" width="20" height="96" fill="{PAPER}" stroke="{INK}" stroke-width="1.2"/>{rungs}'
                f'<ellipse cx="{x}" cy="{y + 46}" rx="62" ry="18" fill="{CARD}" stroke="{WAX}" stroke-width="1.8"/>')
    if kind == "chamber":
        return (f'<rect x="{x - 8}" y="{y - 64}" width="16" height="70" fill="{PAPER}" stroke="{INK}" stroke-width="1.1"/>'
                f'<path d="M{x - 8} {y}H{x - 54}" stroke="{INK}" stroke-width="7"/><path d="M{x - 8} {y}H{x - 54}" stroke="{PAPER}" stroke-width="4"/>'
                f'<ellipse cx="{x - 58}" cy="{y}" rx="30" ry="15" fill="{CARD}" stroke="{INK}" stroke-width="1.1"/>'
                f'<ellipse cx="{x}" cy="{y + 50}" rx="54" ry="14" fill="{CARD}" stroke="{WAX}" stroke-width="1.4"/>'
                f'<rect x="{x - 8}" y="{y + 6}" width="16" height="32" fill="{PAPER}" stroke="{INK}" stroke-width="1.1"/>')
    hexa = [(x + 46 * math.cos(math.radians(60 * k + 30)), y + 46 * math.sin(math.radians(60 * k + 30))) for k in range(6)]
    pts = " ".join(f"{px:.1f},{py:.1f}" for px, py in hexa)
    return (f'<polygon points="{pts}" fill="#F6F0E2" stroke="{INK}" stroke-width="1.4"/>'
            f'<path d="M{x} {y - 46}V{y + 46}M{x - 40} {y - 23}L{x + 40} {y + 23}M{x - 40} {y + 23}L{x + 40} {y - 23}" stroke="{INK}" stroke-width=".6"/>')


def core_strip(days, x0, x1, y, h):
    weeks = Counter((d - timedelta(days=d.weekday())) for d in days)
    first, last = min(weeks), max(weeks)
    span = (last - first).days // 7 + 1
    bw = (x1 - x0) / span
    peak = max(weeks.values())
    out = [f'<rect x="{x0}" y="{y}" width="{x1 - x0}" height="{h}" rx="{h / 2}" fill="{CARD}" stroke="{INK}" stroke-width="1"/>',
           f'<clipPath id="core"><rect x="{x0}" y="{y}" width="{x1 - x0}" height="{h}" rx="{h / 2}"/></clipPath><g clip-path="url(#core)">']
    for i in range(span):
        week = first + timedelta(weeks=i)
        n = weeks.get(week, 0)
        if not n:
            continue
        shade = 0.25 + 0.75 * math.sqrt(n / peak)
        tint = TINTS[(week.isocalendar()[1] // 4) % len(TINTS)]
        out.append(f'<rect x="{x0 + i * bw:.2f}" y="{y}" width="{max(bw, 1.2):.2f}" height="{h}" fill="{tint}" fill-opacity="{shade:.2f}" stroke="{PAPER}" stroke-width=".6"/>')
    out.append("</g>")
    out.append(f'<rect x="{x0}" y="{y}" width="{x1 - x0}" height="{h}" rx="{h / 2}" fill="none" stroke="{INK}" stroke-width="1"/>')
    return "".join(out), min(days), max(days), len(days), span


def plate_head(width, h, label):
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {h}" width="{width}" height="{h}" role="img" aria-label="{escape(label)}">',
        f'<metadata>author: Zaid Ali Syed; ORCID 0009-0003-4313-1510; PGP EFE9 4832 B2B9 80D9 B583 91F2 8FAA BCC1 B1AC 09E5; drawn by scripts/repo_plates.py in github.com/zaidwhy/zaidwhy</metadata>',
        f'''<defs><filter id="paper"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="7"/><feColorMatrix values="0 0 0 0 .17 0 0 0 0 .13 0 0 0 0 .09 0 0 0 .07 0"/><feComposite in2="SourceGraphic" operator="in"/></filter></defs>
<style>.rise{{transform-box:fill-box;transform-origin:bottom;animation:rise 1.6s cubic-bezier(.3,0,.2,1) .3s both}}@keyframes rise{{from{{transform:scaleY(0)}}to{{transform:scaleY(1)}}}}@media (prefers-reduced-motion:reduce){{.rise{{animation:none}}}}</style>''',
        f'<rect width="{width}" height="{h}" fill="{PAPER}"/><rect width="{width}" height="{h}" filter="url(#paper)"/>',
        f'<rect x="18" y="18" width="{width - 36}" height="{h - 36}" fill="none" stroke="{INK}" stroke-width="1.4"/>',
        f'<rect x="24" y="24" width="{width - 48}" height="{h - 48}" fill="none" stroke="{INK}" stroke-width=".5"/>',
    ]


def plate_label(repo, commits, span, first, last):
    _, title, thesis, notes = REPOS[repo]
    return (f"{title}: {thesis} {'; '.join(notes)}. Core strip: {commits} commit{'s' if commits != 1 else ''} over {span} week{'s' if span != 1 else ''}, "
            f"{first.strftime('%b %Y')} to {last.strftime('%b %Y')}.")


def plate_narrow(repo, days, taken):
    """The same plate at 520 px for phones: thesis wrapped, notes stacked, motif beside the notes."""
    kind, title, thesis, notes = REPOS[repo]
    thesis_rows = textwrap.wrap(thesis, 46)
    notes_top = 140 + 20 * len(thesis_rows) + 22
    strip_y = notes_top + 26 * len(notes) + 52
    h = strip_y + 74
    strip, first, last, commits, span = core_strip(days, 60, NARROW_W - 60, strip_y, 18)
    parts = plate_head(NARROW_W, h, plate_label(repo, commits, span, first, last)) + [
        text(60, 62, f"Survey of github.com/{OWNER}  ·  {kind}", 12, caps=True),
        text(60, 104, title, 32),
    ]
    parts += [text(60, 136 + 20 * i, row, 15, italic=True, opacity=.85) for i, row in enumerate(thesis_rows)]
    for i, note in enumerate(notes):
        y = notes_top + 26 * i
        parts.append(f'<circle cx="65" cy="{y - 5}" r="4" fill="{WAX}"/>')
        parts.append(text(78, y, note, 14))
    mx, my = NARROW_W - 92, notes_top + 20
    parts.append(f'<g transform="translate({mx} {my}) scale(.55) translate({-mx} {-my})">{motif(kind, mx, my)}</g>')
    parts.append(text(60, strip_y - 12, f"core strip: {commits} commit{'s' if commits != 1 else ''}, one band per week", 11.5, italic=True, opacity=.75))
    parts.append(strip)
    parts.append(text(60, strip_y + 40, f"{first.strftime('%b %Y')} to {last.strftime('%b %Y')}  ·  taken {taken}", 11.5, italic=True, opacity=.75))
    parts.append("</svg>")
    return "\n".join(parts)


def plate(repo, days, taken):
    kind, title, thesis, notes = REPOS[repo]
    strip, first, last, commits, span = core_strip(days, 60, W - 60, 262, 20)
    label = (f"{title}: {thesis} {'; '.join(notes)}. Core strip: {commits} commit{'s' if commits != 1 else ''} over {span} week{'s' if span != 1 else ''}, "
             f"{first.strftime('%b %Y')} to {last.strftime('%b %Y')}.")
    parts = plate_head(W, H, label) + [
        text(60, 62, f"Survey of github.com/{OWNER}  ·  {kind}", 12, caps=True),
        text(60, 106, title, 38),
        text(60, 136, thesis, 15, italic=True, opacity=.85),
    ]
    for i, note in enumerate(notes):
        nx = 60 + i * 290
        parts.append(f'<circle cx="{nx + 5}" cy="{184}" r="4" fill="{WAX}"/>')
        parts.append(text(nx + 18, 189, note, 14))
    parts.append(f'<line x1="60" y1="214" x2="{W - 260}" y2="214" stroke="{INK}" stroke-width=".4"/>')
    parts.append(motif(kind, W - 150, 128))
    parts.append(strip)
    parts.append(text(60, 250, f"core strip: {commits} commit{'s' if commits != 1 else ''}, one band per week", 11.5, italic=True, opacity=.75))
    parts.append(text(W - 60, 250, f"{first.strftime('%b %Y')} to {last.strftime('%b %Y')}  ·  taken {taken}", 11.5, anchor="end", italic=True, opacity=.75))
    parts.append("</svg>")
    return "\n".join(parts)


def main():
    out_dir = sys.argv[1]
    os.makedirs(out_dir, exist_ok=True)
    taken = datetime.now().date().isoformat()  # local date: the plate is drawn where I am
    for repo in sys.argv[2:] or REPOS:
        days = commit_days(repo)
        if not days:
            print(f"skip {repo}: no commits returned")
            continue
        with open(os.path.join(out_dir, f"{repo}.svg"), "w", encoding="utf-8", newline="\n") as f:
            f.write(plate(repo, days, taken))
        with open(os.path.join(out_dir, f"{repo}-narrow.svg"), "w", encoding="utf-8", newline="\n") as f:
            f.write(plate_narrow(repo, days, taken))
        print(f"wrote {repo}.svg: {len(days)} commits")


if __name__ == "__main__":
    main()
