#!/usr/bin/env python3
"""Draws the survey plates that follow the core sample on the profile page.

The page reads as one field survey: the core sample says when the work was laid
down, and these plates say what the drill brought up (I), where my own claims
broke (II), what the lab measured (III), what is built on the kernel (IV), the
ground I dug that was not mine (V), and the seal that ties it to me (VI).

Every number here is already stated, with its source link, in README.md; this
file only draws them. Change a fact in both places or in neither.

usage: python scripts/plates.py      writes assets/plate-*.svg
"""
import math
import os
from xml.sax.saxutils import escape

from core_sample import INK, PAPER, TINTS, seeded, wave

ASSETS = os.path.join(os.path.dirname(__file__), "..", "assets")
W = 1200
WAX = "#8E2F28"
CARD = "#F7F0DF"
SERIF = "Georgia,'Times New Roman',serif"


def text(x, y, body, size=13.0, italic=False, bold=False, anchor="start", opacity=1.0, caps=False, fill=INK):
    style = [f"font-family:{SERIF}", f"font-size:{size}px"]
    if italic:
        style.append("font-style:italic")
    if bold:
        style.append("font-weight:bold")
    if caps:
        style.append("letter-spacing:.16em;text-transform:uppercase")
    return (f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" fill="{fill}" fill-opacity="{opacity}" '
            f'style="{";".join(style)}">{escape(body)}</text>')


def lines(x, y, rows, size=12.5, gap=17, **kw):
    return "".join(text(x, y + i * gap, row, size, **kw) for i, row in enumerate(rows))


def poly(points, **attrs):
    pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
    extra = " ".join(f'{k.replace("_", "-")}="{v}"' for k, v in attrs.items())
    return f'<polygon points="{pts}" {extra}/>'


def frame(h, kicker, title, subtitle, label, width=W):
    """Paper, border and heading. A list subtitle is drawn one line per item, for the narrow phone plates."""
    sub = subtitle if isinstance(subtitle, list) else [subtitle]
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {h}" width="{width}" height="{h}" role="img" aria-label="{escape(label)}">',
        f'''<defs>
<filter id="paper"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="7"/><feColorMatrix values="0 0 0 0 .17 0 0 0 0 .13 0 0 0 0 .09 0 0 0 .07 0"/><feComposite in2="SourceGraphic" operator="in"/></filter>
<pattern id="hatch" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="7" stroke="{INK}" stroke-opacity=".22" stroke-width=".8"/></pattern>
<pattern id="dots" width="9" height="9" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r=".7" fill="{INK}" fill-opacity=".4"/><circle cx="6.5" cy="6" r=".6" fill="{INK}" fill-opacity=".3"/></pattern>
<pattern id="dash" width="22" height="7" patternUnits="userSpaceOnUse"><line x1="1" y1="3.5" x2="13" y2="3.5" stroke="{INK}" stroke-opacity=".32" stroke-width=".7"/></pattern>
</defs>
<style>
.rise{{transform-box:fill-box;transform-origin:bottom;animation:rise 1.6s cubic-bezier(.3,0,.2,1) both}}
.show{{animation:show .8s ease-out both}}
@keyframes rise{{from{{transform:scaleY(0)}}to{{transform:scaleY(1)}}}}
@keyframes show{{from{{opacity:0}}to{{opacity:1}}}}
@media (prefers-reduced-motion:reduce){{.rise,.show{{animation:none}}}}
</style>''',
f'<metadata>author: Zaid Ali Syed; ORCID 0009-0003-4313-1510; PGP EFE9 4832 B2B9 80D9 B583 91F2 8FAA BCC1 B1AC 09E5; drawn by scripts/plates.py in github.com/zaidwhy/zaidwhy</metadata>',
        f'<rect width="{width}" height="{h}" fill="{PAPER}"/><rect width="{width}" height="{h}" filter="url(#paper)"/>',
        f'<rect x="18" y="18" width="{width - 36}" height="{h - 36}" fill="none" stroke="{INK}" stroke-width="1.4"/>',
        f'<rect x="24" y="24" width="{width - 48}" height="{h - 48}" fill="none" stroke="{INK}" stroke-width=".5"/>',
        text(60, 62, kicker, 12.5, caps=True),
        text(60, 97, title, 28),
        lines(60, 122, sub, 14, gap=19, italic=True, opacity=.8),
    ]


def save(name, parts):
    parts.append("</svg>")
    with open(os.path.join(ASSETS, name), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(parts))
    print("wrote", name)


def route():
    h = 230
    stations = [("I", "Specimens", "what the drill brought up"), ("II", "Fault lines", "where my claims broke"),
                ("III", "Assays", "what the lab measured"), ("IV", "Excavation", "what stands on the kernel"),
                ("V", "Field work", "ground that was not mine"), ("VI", "The seal", "how you know it is mine")]
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {h}" width="{W}" height="{h}" role="img" '
           f'aria-label="The route through this page: I Specimens, II Fault lines, III Assays, IV Excavation, V Field work, VI The seal.">',
           f'<metadata>author: Zaid Ali Syed; ORCID 0009-0003-4313-1510; PGP EFE9 4832 B2B9 80D9 B583 91F2 8FAA BCC1 B1AC 09E5; drawn by scripts/plates.py in github.com/zaidwhy/zaidwhy</metadata>',
           f'<rect width="{W}" height="{h}" fill="{PAPER}"/>',
           f'<rect x="18" y="18" width="{W - 36}" height="{h - 36}" fill="none" stroke="{INK}" stroke-width="1.4"/>',
           text(60, 60, "The route through this survey", 12.5, caps=True)]
    xs = [110 + i * 196 for i in range(6)]
    trail = " ".join(f"{x:.1f},{132 + wave(x, 'trail', 9):.1f}" for x in range(70, W - 60, 6))
    out.append(f'<polyline points="{trail}" fill="none" stroke="{INK}" stroke-width="1.3" stroke-dasharray="2 5" stroke-linecap="round"/>')
    for i, (num, name, story) in enumerate(stations):
        x = xs[i]
        y = 132 + wave(x, "trail", 9)
        out.append(poly([(x, y - 15), (x - 12, y + 7), (x + 12, y + 7)], fill=TINTS[i + 1], stroke=INK, stroke_width="1.1"))
        out.append(f'<circle cx="{x}" cy="{y - 1:.1f}" r="2" fill="{INK}"/>')
        out.append(text(x, y - 26, num, 13, anchor="middle", bold=True))
        out.append(text(x, y + 32, name, 16, anchor="middle"))
        out.append(text(x, y + 51, story, 11.5, anchor="middle", italic=True, opacity=.8))
    out.append("</svg>")
    with open(os.path.join(ASSETS, "plate-route.svg"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(out))
    print("wrote plate-route.svg")


SPECIMENS = [
    ("3", "pull requests merged upstream", ["tenacity, returns, gqlalchemy", "13.4k stars between them"]),
    ("27", "pull requests merged into a live product", ["12 days, +8,838 / -1,619 lines", "every one reviewed by its owner"]),
    ("2", "research findings with a DOI", ["each with a negative control", "and a second-model replication"]),
    ("356", "tests, all offline", ["mocked end to end", "no API key runs any of them"]),
    ("3,240", "forecasts locked before outcomes", ["hash-chained public ledger", "graded in public from 15 Nov"]),
    ("229", "scored coding-agent runs", ["pre-registered, two studies", "every transcript shipped"]),
]
SPECIMENS_LABEL = ("Plate I, specimens: 3 pull requests merged upstream into libraries with 13.4k stars; 27 pull requests merged into a live product in 12 days; "
                   "2 research findings archived with a DOI; 356 offline tests; 3,240 forecasts locked before outcomes; 229 scored coding-agent runs.")
NARROW = 520  # phone plates: about 400 px on screen keeps the smallest label near 9 px


def specimen_card(i, x, y, cw, ch, big, what, notes):
    tint = TINTS[(i * 3) % len(TINTS)]
    rock = [(x + 46 + 30 * math.cos(a) * (0.75 + 0.35 * seeded(f"{i}{k}")), y + 62 + 26 * math.sin(a) * (0.75 + 0.35 * seeded(f"r{i}{k}")))
            for k, a in enumerate([j * math.tau / 9 for j in range(9)])]
    return "".join([
        f'<g class="show" style="animation-delay:{.15 * i:.2f}s">',
        f'<rect x="{x + 3}" y="{y + 4}" width="{cw}" height="{ch}" fill="{INK}" fill-opacity=".12"/>',
        f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" fill="{CARD}" stroke="{INK}" stroke-width=".9"/>',
        poly(rock, fill=tint, stroke=INK, stroke_width="1"), poly(rock, fill="url(#dots)"),
        text(x + 110, y + 76, big, 46),
        text(x + 24, y + 118, what, 14.5),
        lines(x + 24, y + 140, notes, 12, italic=True, opacity=.8),
        f'<circle cx="{x + cw / 2}" cy="{y + 8}" r="3.2" fill="{WAX}" stroke="{INK}" stroke-width=".6"/>',
        text(x + cw - 14, y + 24, f"no. {i + 1:02d}", 10.5, anchor="end", italic=True, opacity=.6),
        "</g>"])


def specimens():
    h = 590
    out = frame(h, "Plate I  ·  Specimens", "What the drill brought up",
                "Six samples from the core, each mounted with the label that says where it came from.", SPECIMENS_LABEL)
    out.append(f'<rect x="54" y="146" width="{W - 108}" height="{h - 192}" fill="#E4D6B8" stroke="{INK}" stroke-width=".9"/>')
    cw, ch = 340, 170
    for i, (big, what, notes) in enumerate(SPECIMENS):
        out.append(specimen_card(i, 78 + (i % 3) * (cw + 24), 166 + (i // 3) * (ch + 22), cw, ch, big, what, notes))
    save("plate-specimens.svg", out)


def specimens_narrow():
    cw, ch, gap, top = NARROW - 132, 170, 18, 186
    h = top + len(SPECIMENS) * (ch + gap) + 40
    out = frame(h, "Plate I  ·  Specimens", "What the drill brought up",
                ["Six samples from the core, each mounted", "with the label that says where it came from."], SPECIMENS_LABEL, width=NARROW)
    out.append(f'<rect x="44" y="{top - 20}" width="{NARROW - 88}" height="{h - top - 10}" fill="#E4D6B8" stroke="{INK}" stroke-width=".9"/>')
    for i, (big, what, notes) in enumerate(SPECIMENS):
        out.append(specimen_card(i, 64, top + i * (ch + gap), cw, ch, big, what, notes))
    save("plate-specimens-narrow.svg", out)


def faults():
    h = 640
    entries = [
        ("TCMF v1", ["claimed: causal fusion wins", "found: recall@5 0.02, where", "the causal signal alone is 1.00", "kept in: docs/tcmf.md"]),
        ("COLD READ", ["claimed: short text gives", "confidently wrong guesses", "found: no replication on a", "second model; RESULT.md says so"]),
        ("AUGUR", ["claimed: a forecasting", "programme on old models", "found: killed by its own", "phase zero; still in FINDING.md"]),
        ("adk-python #6190", ["claimed: the fix for a CLI", "parser bug, LGTM'd", "found: a maintainer's commit", "landed first; closed, kept here"]),
        ("AFTERSHOCK", ["claimed: a song-placement", "effect, significant", "found: data terms forbade it;", "rebuilt, did not replicate"]),
    ]
    out = frame(h, "Plate II  ·  Fault lines", "Where my own claims broke",
                "Five places I said something, went looking for the evidence, and the rock gave way. The breaks stay on the record.",
                "Plate II, fault lines: five claims of mine broken by my own evidence. TCMF version one scored recall at 5 of 0.02 where the causal signal alone reaches 1.00. "
                "COLD READ's confidently-wrong finding did not replicate on a second model. AUGUR's forecasting programme was killed by its own phase zero. "
                "adk-python 6190 was closed after an LGTM when a maintainer's commit landed first. AFTERSHOCK's song-placement effect was discarded over data terms and did not replicate.")
    top, bot, left, right = 160, 380, 60, W - 60
    out.append(f'<clipPath id="block"><rect x="{left}" y="{top}" width="{right - left}" height="{bot - top}"/></clipPath>')
    fault_x = [left + (right - left) * (k + 0.5) / 5 for k in range(5)]
    lean = 0.28
    beds = [top + 22 * k for k in range(-6, 14)]
    group = ['<g clip-path="url(#block)">']
    for seg in range(6):
        drop = 14 * seg
        def fx(k, y):
            if k < 0:
                return left - 200
            if k >= 5:
                return right + 200
            return fault_x[k] + (y - (top + bot) / 2) * lean
        for b in range(len(beds) - 1):
            y0, y1 = beds[b] + drop, beds[b + 1] + drop
            shape = [(fx(seg - 1, y0), y0), (fx(seg, y0), y0), (fx(seg, y1), y1), (fx(seg - 1, y1), y1)]
            tint = TINTS[b % len(TINTS)]
            group.append(poly(shape, fill=tint, stroke=INK, stroke_width=".45", stroke_opacity=".6"))
            group.append(poly(shape, fill="url(#dash)" if b % 2 else "url(#dots)"))
    group.append("</g>")
    out.extend(group)
    out.append(f'<rect x="{left}" y="{top}" width="{right - left}" height="{bot - top}" fill="none" stroke="{INK}" stroke-width="1.2"/>')
    for k, x in enumerate(fault_x):
        x0, x1 = x + (top - (top + bot) / 2) * lean, x + (bot - (top + bot) / 2) * lean
        out.append(f'<line x1="{x0:.1f}" y1="{top}" x2="{x1:.1f}" y2="{bot}" stroke="{WAX}" stroke-width="2.6"/>')
        mx, my = (x0 + x1) / 2, (top + bot) / 2
        out.append(f'<path d="M{mx - 16:.1f} {my - 26:.1f}v14l-4 -5m4 5l4 -5" stroke="{INK}" stroke-width="1.1" fill="none"/>')
        out.append(f'<circle cx="{x0:.1f}" cy="{top - 12}" r="11" fill="{CARD}" stroke="{WAX}" stroke-width="1.4"/>')
        out.append(text(x0, top - 7.5, ["i", "ii", "iii", "iv", "v"][k], 12, anchor="middle", italic=True, fill=WAX))
    col_w = (right - left) / 5
    for k, (name, rows) in enumerate(entries):
        cx = left + col_w * k + 10
        out.append(text(cx, bot + 44, f"{['i', 'ii', 'iii', 'iv', 'v'][k]}.  {name}", 15, bold=True))
        out.append(lines(cx, bot + 70, rows, 12.2, gap=18, italic=True))
    out.append(text(W / 2, h - 44, "A result that was never allowed to fail is not evidence of anything.", 14, anchor="middle", italic=True))
    save("plate-faults.svg", out)


def assays():
    h = 680
    out = frame(h, "Plate III  ·  Assays", "What the lab measured",
                "Three samples sent for testing. Each one came back with a number nobody expected, mine included.",
                "Plate III, assays. FLAKE LAUNDERING: with a correct test, coding agents weakened it in 0 of 60 runs; with a wrong test they repaired it in 9 of 10, "
                "0 of 10 when told not to change the tests, 10 of 10 when told to find out which side is wrong. COLD READ: words before a model beats chance on gender: "
                "50 for llama3.1 8B, 800 for qwen2.5 7B, about 1600 for mistral 7B. AUGUR: a 1938-cutoff model answers from 1899, a 1930-cutoff model from 1850.")
    panel_w, gap, py = 344, 24, 150
    panels = [60 + i * (panel_w + gap) for i in range(3)]
    for px in panels:
        out.append(f'<rect x="{px}" y="{py}" width="{panel_w}" height="{h - py - 50}" fill="{CARD}" stroke="{INK}" stroke-width=".9"/>')

    # A. vials: share of runs that repaired the wrong test
    px = panels[0]
    out.append(text(px + 20, py + 32, "FLAKE LAUNDERING", 13, caps=True, bold=True))
    out.append(lines(px + 20, py + 54, ["Handed a wrong test, how often did", "the coding agent repair it?"], 12.5, italic=True))
    vials = [(9, 10, "plain brief"), (0, 10, '"do not change', 'the tests"'), (10, 10, '"find out which', 'side is wrong"')]
    for i, vial in enumerate(vials):
        got, of = vial[0], vial[1]
        vx, vtop, vbot = px + 62 + i * 110, py + 110, py + 300
        out.append(f'<rect x="{vx - 20}" y="{vtop}" width="40" height="{vbot - vtop}" rx="18" fill="#FBF7EC" stroke="{INK}" stroke-width="1.2"/>')
        level = (vbot - vtop - 8) * got / of
        if got:
            out.append(f'<rect class="rise" style="animation-delay:{.3 + .25 * i:.2f}s" x="{vx - 16}" y="{vbot - 4 - level:.1f}" width="32" height="{level:.1f}" rx="14" fill="{TINTS[2] if i < 2 else TINTS[3]}"/>')
        out.append(f'<rect x="{vx - 26}" y="{vtop - 8}" width="52" height="10" fill="{INK}" fill-opacity=".85"/>')
        out.append(text(vx, vbot + 30, f"{got} / {of}", 18, anchor="middle"))
        out.append(lines(vx, vbot + 50, list(vial[2:]), 11.5, gap=15, italic=True, anchor="middle"))
    out.append(lines(px + 20, h - 92, ["With a correct test: 0 of 60 runs weakened it,", "60 of 60 fixed the real race bug."], 12, italic=True, opacity=.85))

    # B. log ruler: words before each reader beats chance on gender
    px = panels[1]
    out.append(text(px + 20, py + 32, "COLD READ", 13, caps=True, bold=True))
    out.append(lines(px + 20, py + 54, ["Words a model reads before it beats", "a coin flip on the author's gender"], 12.5, italic=True))
    rx, ry0, ry1 = px + 120, py + 100, py + 370
    lo, hi = math.log(25), math.log(3200)
    ypos = lambda words: ry1 - (math.log(words) - lo) / (hi - lo) * (ry1 - ry0)
    out.append(f'<rect x="{rx - 9}" y="{ry0}" width="18" height="{ry1 - ry0}" fill="{TINTS[0]}" stroke="{INK}" stroke-width="1"/>')
    out.append(f'<rect x="{rx - 9}" y="{ry0}" width="18" height="{ry1 - ry0}" fill="url(#hatch)"/>')
    for words in (25, 50, 100, 200, 400, 800, 1600, 3200):
        y = ypos(words)
        out.append(f'<line x1="{rx - 15}" y1="{y:.1f}" x2="{rx - 9}" y2="{y:.1f}" stroke="{INK}" stroke-width=".8"/>')
        out.append(text(rx - 20, y + 4, f"{words:,}", 11, anchor="end", opacity=.7))
    for i, (model, words) in enumerate([("llama3.1:8b", 50), ("qwen2.5:7b", 800), ("mistral:7b", 1600)]):
        y = ypos(words)
        out.append(f'<g class="show" style="animation-delay:{.4 + .3 * i:.2f}s"><path d="M{rx + 9} {y:.1f}h28" stroke="{WAX}" stroke-width="1.6"/>'
                   f'<circle cx="{rx}" cy="{y:.1f}" r="5" fill="{WAX}"/>' + text(rx + 44, y + 4.5, f"{model}  ·  {words:,} words", 12.5) + "</g>")
    out.append(text(rx + 44, ry0 - 6, "control (star sign): never", 12, italic=True, opacity=.75))
    out.append(lines(px + 20, h - 92, ["Same 72 authors, same prompt: a thirty-two-", "fold spread. Anonymity depends on the reader."], 12, italic=True, opacity=.85))

    # C. timeline: stated cutoff against where each model speaks from
    px = panels[2]
    out.append(text(px + 20, py + 32, "AUGUR", 13, caps=True, bold=True))
    out.append(lines(px + 20, py + 54, ["Ask a time-locked model what year it is:", "it answers from the middle of its shelf"], 12.5, italic=True))
    tx0, tx1 = px + 30, px + panel_w - 30
    ty = py + 300
    year_x = lambda yr: tx0 + (yr - 1840) / 100 * (tx1 - tx0)
    out.append(f'<line x1="{tx0}" y1="{ty}" x2="{tx1}" y2="{ty}" stroke="{INK}" stroke-width="1.2"/>')
    for yr in range(1840, 1941, 20):
        out.append(f'<line x1="{year_x(yr):.1f}" y1="{ty - 4}" x2="{year_x(yr):.1f}" y2="{ty + 4}" stroke="{INK}" stroke-width=".8"/>')
        out.append(text(year_x(yr), ty + 20, str(yr), 11, anchor="middle", opacity=.7))
    for i, (model, cutoff, voice) in enumerate([("TypeWriter-1938", 1938, 1899), ("Talkie-1930", 1930, 1850)]):
        a, b = year_x(voice), year_x(cutoff)
        lift = 80 + 60 * i
        out.append(f'<path class="show" style="animation-delay:{.4 + .4 * i:.2f}s" d="M{b:.1f} {ty}Q{(a + b) / 2:.1f} {ty - lift * 2:.1f} {a:.1f} {ty}" fill="none" stroke="{WAX}" stroke-width="1.6" stroke-dasharray="5 3"/>')
        out.append(f'<circle cx="{b:.1f}" cy="{ty}" r="4" fill="{CARD}" stroke="{INK}" stroke-width="1.2"/><circle cx="{a:.1f}" cy="{ty}" r="5" fill="{WAX}"/>')
        out.append(f'<circle cx="{px + 28}" cy="{ty + 52 + 40 * i}" r="5" fill="{WAX}"/>')
        out.append(text(px + 42, ty + 56 + 40 * i, f"{model} speaks from {voice}", 12.5))
        out.append(text(px + 42, ty + 72 + 40 * i, f"{cutoff - voice} years short of its {cutoff} cutoff", 11, italic=True, opacity=.8))
    out.append(lines(px + 20, h - 92, ["Told the year, one model moves forty years;", "the other does not move at all."], 12, italic=True, opacity=.85))
    save("plate-assays.svg", out)


def excavation():
    h = 640
    out = frame(h, "Plate IV  ·  Excavation", "What stands on the kernel",
                "One memory kernel, sunk once and reached by every app below ground. The headframes above are the systems people can use.",
                "Plate IV, excavation. Surface: CivilizationOS, 10 agents and 5 councils, live; Recall, recall at 1 of 10 out of 10 at 149 ms median; autocto, 5 analyzers and 162 tests on PyPI; "
                "AFTERSHOCK, ROC AUC 0.817 on 829 held-out breakouts; Agent Factory, 6 agents on frozen contracts. Below ground the personal-llm kernel with 181 offline tests, "
                "reached by second-brain with 110 tests, github-pr-agent with 65, and DreamOS.")
    ground = 300
    layers = [(ground, ground + 70, TINTS[0], "dots"), (ground + 70, ground + 150, TINTS[1], "dash"),
              (ground + 150, ground + 230, TINTS[6], "dots"), (ground + 230, h - 40, "#9C9488", "hatch")]
    for i, (y0, y1, tint, pat) in enumerate(layers):
        top_pts = [(x, y0 + (wave(x, f"ex{i}", 4) if i else 0)) for x in range(24, W - 23, 8)]
        bot_pts = [(x, y1 + wave(x, f"ex{i + 1}", 4)) for x in range(W - 24, 23, -8)] if i < 3 else [(W - 24, y1), (24, y1)]
        out.append(poly(top_pts + bot_pts, fill=tint))
        out.append(poly(top_pts + bot_pts, fill=f"url(#{pat})"))
    out.append(f'<rect x="24" y="{ground - 8}" width="{W - 48}" height="8" fill="#6E6A3E"/>')
    for x in range(26, W - 26, 7):
        out.append(f'<line x1="{x}" y1="{ground - 8}" x2="{x + 1.5}" y2="{ground - 12 - seeded(f"g{x}") * 4:.1f}" stroke="#4E5A2C" stroke-width=".9"/>')

    surface = [("CivilizationOS", ["10 agents, 5 councils", "live"]), ("Recall", ["Recall@1 10 of 10", "149 ms median"]),
               ("autocto", ["5 analyzers, 162 tests", "on PyPI"]), ("AFTERSHOCK", ["AUC 0.817 on 829", "held-out breakouts"]),
               ("Agent Factory", ["6 agents", "frozen contracts"])]
    for i, (name, rows) in enumerate(surface):
        x = 130 + i * 210
        out.append(f'<g class="show" style="animation-delay:{.12 * i:.2f}s">')
        out.append(f'<path d="M{x - 22} {ground - 8}L{x} {ground - 74}L{x + 22} {ground - 8}M{x - 15} {ground - 30}H{x + 15}M{x - 8} {ground - 52}H{x + 8}" stroke="{INK}" stroke-width="1.4" fill="none"/>')
        out.append(f'<circle cx="{x}" cy="{ground - 78}" r="6" fill="{CARD}" stroke="{INK}" stroke-width="1.2"/>')
        out.append(text(x, ground - 128, name, 15, anchor="middle", bold=True))
        out.append(lines(x, ground - 110, rows[:1], 11.5, anchor="middle", italic=True))
        out.append(text(x, ground - 94, rows[1], 11.5, anchor="middle", italic=True, opacity=.75))
        out.append("</g>")

    shaft_x = 600
    kernel_y = h - 92
    out.append(f'<rect x="{shaft_x - 9}" y="{ground}" width="18" height="{kernel_y - ground - 24}" fill="{PAPER}" stroke="{INK}" stroke-width="1.1"/>')
    for y in range(ground + 10, kernel_y - 24, 12):
        out.append(f'<line x1="{shaft_x - 9}" y1="{y}" x2="{shaft_x + 9}" y2="{y}" stroke="{INK}" stroke-width=".5"/>')
    out.append(f'<ellipse cx="{shaft_x}" cy="{kernel_y}" rx="210" ry="30" fill="{CARD}" stroke="{WAX}" stroke-width="1.8"/>')
    out.append(text(shaft_x, kernel_y - 3, "personal-llm  ·  the memory kernel", 15, anchor="middle", bold=True))
    out.append(text(shaft_x, kernel_y + 16, "181 offline tests, keyless CI", 12, anchor="middle", italic=True))
    chambers = [("second-brain", "110 tests", 250, ground + 110), ("github-pr-agent", "65 tests", 950, ground + 110), ("DreamOS", "semantic file shell", 300, ground + 200)]
    for name, note, cx, cy in chambers:
        mid = shaft_x - 9 if cx < shaft_x else shaft_x + 9
        out.append(f'<path d="M{mid} {cy}H{cx + (70 if cx < shaft_x else -70)}" stroke="{INK}" stroke-width="7" stroke-opacity=".85"/>')
        out.append(f'<path d="M{mid} {cy}H{cx + (70 if cx < shaft_x else -70)}" stroke="{PAPER}" stroke-width="4"/>')
        out.append(f'<ellipse cx="{cx}" cy="{cy}" rx="72" ry="22" fill="{CARD}" stroke="{INK}" stroke-width="1.1"/>')
        out.append(text(cx, cy - 2, name, 13.5, anchor="middle"))
        out.append(text(cx, cy + 14, note, 11, anchor="middle", italic=True, opacity=.8))
    out.append(text(W - 60, ground + 26, "below ground: imports the kernel instead of rebuilding retrieval", 11.5, anchor="end", italic=True, opacity=.75))
    save("plate-excavation.svg", out)


def fieldwork():
    h = 560
    out = frame(h, "Plate V  ·  Field work", "Ground that was not mine",
                "Digging in codebases other people own, where every change has to pass somebody else's review.",
                "Plate V, field work. Zabira Academy: 27 pull requests merged into a live product in 12 days. Pratyaya Limited: all 10 aggregate totals match the support platform's report "
                "and 53 of 55 per-agent averages agree within one second. Upstream: 3 merged pull requests, 2 open, and adk-python 6190 closed after an LGTM.")
    cols = [60, 432, 804]
    for x in cols:
        out.append(f'<line x1="{x + 350}" y1="160" x2="{x + 350}" y2="{h - 60}" stroke="{INK}" stroke-width=".4"/>' if x != cols[-1] else "")

    x = cols[0]
    out.append(text(x, 170, "ZABIRA ACADEMY  ·  live ed-tech", 12.5, caps=True, bold=True))
    out.append(text(x, 192, "the excavation grid: one square per merged PR", 12, italic=True, opacity=.8))
    for i in range(27):
        gx, gy = x + (i % 9) * 36, 214 + (i // 9) * 36
        out.append(f'<rect class="show" style="animation-delay:{.04 * i:.2f}s" x="{gx}" y="{gy}" width="30" height="30" fill="{TINTS[(i * 5) % len(TINTS)]}" stroke="{INK}" stroke-width=".8"/>')
        out.append(f'<rect x="{gx}" y="{gy}" width="30" height="30" fill="url(#dots)"/>')
    out.append(text(x, 360, "27", 40))
    out.append(lines(x + 60, 346, ["pull requests in 12 days", "+8,838 / -1,619 across 557 file changes"], 12.5, italic=True))
    out.append(lines(x, 400, ["security hardening across 226 files,", "Origin checks on 60 endpoints, and the", "first CI-gated end-to-end suite"], 12.5, gap=18))

    x = cols[1]
    out.append(text(x, 170, "PRATYAYA LIMITED  ·  AI intern", 12.5, caps=True, bold=True))
    out.append(text(x, 192, "a dashboard reconciled to the platform's own report", 12, italic=True, opacity=.8))
    for i in range(10):
        bx = x + i * 32
        out.append(f'<circle cx="{bx + 12}" cy="232" r="11" fill="{TINTS[3]}" stroke="{INK}" stroke-width=".9"/>')
        out.append(f'<path d="M{bx + 7} 232l4 4l7 -8" stroke="{INK}" stroke-width="1.4" fill="none"/>')
    out.append(text(x, 274, "10 of 10 aggregate totals match exactly", 12.5))
    for i in range(55):
        dx, dy = x + 6 + (i % 11) * 28, 300 + (i // 11) * 22
        filled = i < 53
        out.append(f'<circle cx="{dx}" cy="{dy}" r="6.5" fill="{TINTS[1] if filled else CARD}" stroke="{INK if filled else WAX}" stroke-width="{.8 if filled else 1.6}"/>')
    out.append(lines(x, 432, ["53 of 55 per-agent averages within one second;", "the 2 that differ are clickable and explain why"], 12.5, gap=18))

    x = cols[2]
    out.append(text(x, 170, "UPSTREAM OPEN SOURCE", 12.5, caps=True, bold=True))
    out.append(text(x, 192, "fossils left in other people's code", 12, italic=True, opacity=.8))
    prs = [("tenacity #668", "8.8k stars", "merged"), ("returns #2480", "4.4k stars", "merged"), ("gqlalchemy #390", "query builder", "merged"),
           ("2 more, under review", "gqlalchemy #392, django-taggit #944", "open"), ("adk-python #6190", "LGTM, beaten to it", "closed")]
    for i, (name, note, state) in enumerate(prs):
        cy = 228 + i * 50
        cx = x + 18
        if state == "merged":
            spiral = " ".join(f"{cx + 1.2 * math.exp(.15 * t / 18) * math.cos(t / 18):.1f},{cy + 1.2 * math.exp(.15 * t / 18) * math.sin(t / 18):.1f}" for t in range(260))
            out.append(f'<circle cx="{cx}" cy="{cy}" r="13" fill="{CARD}" stroke="{INK}" stroke-width="1"/><polyline points="{spiral}" fill="none" stroke="{INK}" stroke-width="1"/>')
        else:
            dash = "3 3" if state == "open" else "1 3"
            out.append(f'<circle cx="{cx}" cy="{cy}" r="13" fill="none" stroke="{WAX if state == "closed" else INK}" stroke-width="1.2" stroke-dasharray="{dash}"/>')
        out.append(text(cx + 26, cy - 1, name, 13.5))
        out.append(text(cx + 26, cy + 15, f"{note}  ·  {state}", 11.5, italic=True, opacity=.8))
    save("plate-fieldwork.svg", out)


def seal():
    h = 400
    links = [("i", "a signed commit", "asserted by me"), ("ii", "ed25519 signature", "verified by GitHub"),
             ("iii", "an immutable tag", "held by GitHub"), ("iv", "a Zenodo DOI", "timestamped by Zenodo"),
             ("v", "an ORCID iD", "bound to a person by ORCID")]
    out = frame(h, "Plate VI  ·  The seal", "How you know it is mine",
                "Five links in the chain of custody. Four of them are asserted by somebody other than me, and none come with a copy.",
                "Plate VI, the seal: a signed commit, an ed25519 signature verified by GitHub, an immutable release tag, a Zenodo DOI with an independent timestamp, "
                "and an ORCID iD bound to a person.")
    xs = [140 + i * 230 for i in range(5)]
    cy = 230
    cord = " ".join(f"{x},{cy + 26 * math.sin((x - 140) / 230 * math.pi):.1f}" for x in range(110, 1100, 6))
    out.append(f'<polyline points="{cord}" fill="none" stroke="{INK}" stroke-width="1.4" stroke-opacity=".7"/>')
    for i, (num, what, who) in enumerate(links):
        x = xs[i]
        y = cy + 26 * math.sin((x - 140) / 230 * math.pi)
        blob = [(x + (38 + 4 * math.sin(k * 2.3 + i)) * math.cos(k * math.tau / 22), y + (38 + 4 * math.sin(k * 2.3 + i)) * math.sin(k * math.tau / 22)) for k in range(22)]
        out.append(f'<g class="show" style="animation-delay:{.2 * i:.2f}s">')
        out.append(poly(blob, fill=WAX, stroke="#5E1E19", stroke_width="1.2"))
        out.append(f'<circle cx="{x}" cy="{y:.1f}" r="26" fill="none" stroke="#F1D9C9" stroke-opacity=".55" stroke-width="1.2"/>')
        out.append(text(x, y + 7, num, 22, anchor="middle", italic=True, fill="#F6E7DA"))
        out.append(text(x, y + 72, what, 14, anchor="middle"))
        out.append(text(x, y + 90, who, 12, anchor="middle", italic=True, opacity=.8))
        out.append("</g>")
    save("plate-seal.svg", out)


if __name__ == "__main__":
    route()
    specimens()
    specimens_narrow()
    faults()
    assays()
    excavation()
    fieldwork()
    seal()
