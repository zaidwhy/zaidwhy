#!/usr/bin/env python3
"""Draws assets/core-sample.svg: a geological section through my GitHub history.

One bed per month, thickness by the square root of that month's contributions.
A run of three or more near-empty months is not drawn as thin beds: it is an
unconformity, an erosion surface where time passed and nothing was deposited,
and every bed older than it is tilted, the way old rock sits under a gap.
Fossils are pull requests merged into other people's public repositories;
crystals are public repositories I founded.

Shapes are seeded by the month string, so a bed keeps its outline from night to
night and only the current month, still forming, changes. If any API call
fails the script exits non-zero and leaves the old SVG in place.
"""
import json
import math
import os
import subprocess
import sys
import urllib.request
import zlib
from datetime import date, datetime, timezone
from xml.sax.saxutils import escape

OWNER = "zaidwhy"
OUT_PATH = os.path.join(os.path.dirname(__file__), "..", "assets", "core-sample.svg")
QUIET_BELOW = 10      # a month under this many contributions counts as nothing deposited
GAP_MIN_MONTHS = 3    # this many quiet months in a row make an unconformity
FIRST_YEAR = 2022     # account created Feb 2022; years before have no calendar

W, H = 1200, 780
SEC_L, SEC_R = 60, 860          # section edges
PIVOT_X = 840                   # tilted beds have their true thickness here, where labels attach
SURFACE_Y, FLOOR_Y = 168, 700
LABEL_X = 892
INK = "#2B2118"
PAPER = "#F1E8D4"
# hand-tinted survey colours: sandstone, ochre, sienna, sage, clay, slate, umber, buff
TINTS = ["#D9C08C", "#C99A55", "#B0663F", "#97A077", "#BE8573", "#7F8C8E", "#8A6A47", "#E3CFA4"]
MONTHS = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()


def token():
    found = os.environ.get("GITHUB_TOKEN", "")
    if found:
        return found
    done = subprocess.run(["gh", "auth", "token"], capture_output=True, text=True, timeout=20)
    return done.stdout.strip()


def gh_request(url, body=None):
    req = urllib.request.Request(url, data=json.dumps(body).encode() if body else None, headers={
        "Accept": "application/vnd.github+json",
        "User-Agent": "zaidwhy-core-sample",
        "Authorization": f"Bearer {token()}",
    })
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode())


def monthly_contributions(today):
    counts = {}
    for year in range(FIRST_YEAR, today.year + 1):
        query = ('query($login:String!,$from:DateTime!,$to:DateTime!){user(login:$login){'
                 'contributionsCollection(from:$from,to:$to){contributionCalendar{'
                 'weeks{contributionDays{date contributionCount}}}}}}')
        variables = {"login": OWNER, "from": f"{year}-01-01T00:00:00Z", "to": f"{year}-12-31T23:59:59Z"}
        data = gh_request("https://api.github.com/graphql", {"query": query, "variables": variables})
        if "errors" in data:
            raise RuntimeError(f"graphql errors for {year}: {data['errors']}")
        weeks = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
        for week in weeks:
            for day in week["contributionDays"]:
                key = day["date"][:7]
                counts[key] = counts.get(key, 0) + day["contributionCount"]
    last = f"{today.year}-{today.month:02d}"
    months = sorted(k for k in counts if k <= last)
    while months and counts[months[0]] < QUIET_BELOW:
        months.pop(0)
    return [(m, counts[m]) for m in months]


def founded_repos():
    repos = gh_request(f"https://api.github.com/users/{OWNER}/repos?type=owner&per_page=100")
    return [(r["created_at"][:7], r["name"]) for r in repos if not r["fork"] and not r["private"]]


def merged_upstream_prs():
    q = f"is:pr is:merged is:public author:{OWNER} -user:{OWNER}"
    url = "https://api.github.com/search/issues?per_page=50&q=" + urllib.request.quote(q)
    items = gh_request(url)["items"]
    return [(i["closed_at"][:7], f"{i['repository_url'].rsplit('/', 1)[1]} #{i['number']}") for i in items]


def split_into_eras(months):
    """Youngest era first. Each era is a list of (month, count); gaps sit between eras."""
    eras, gaps, current, quiet = [], [], [], []
    for month, count in months:
        if count < QUIET_BELOW:
            quiet.append((month, count))
            continue
        if len(quiet) >= GAP_MIN_MONTHS and current:
            eras.append(current)
            gaps.append(quiet)
            current = []
        else:
            current.extend(quiet)
        quiet = []
        current.append((month, count))
    current.extend(quiet)  # trailing quiet months are the present, not a gap yet
    eras.append(current)
    return eras[::-1], gaps[::-1]


def seeded(text):
    return zlib.crc32(text.encode()) / 0xFFFFFFFF


def wave(x, key, amp):
    s = seeded(key)
    return amp * (0.6 * math.sin(x / 61 + s * 6.28) + 0.4 * math.sin(x / 23 + s * 17.0))


def label_for(month):
    y, m = month.split("-")
    return f"{MONTHS[int(m) - 1]} {y}"


def poly(points, **attrs):
    pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
    extra = " ".join(f'{k.replace("_", "-")}="{v}"' for k, v in attrs.items())
    return f'<polygon points="{pts}" {extra}/>'


def pattern_for(count):
    if count < 40:
        return "sand"
    if count < 120:
        return "shale"
    if count < 700:
        return "lime"
    return "massive"


XS = list(range(SEC_L, SEC_R + 1, 8))


def draw(months, repos, prs, today):
    eras, gaps = split_into_eras(months)
    weights = [sum(math.sqrt(c) for _, c in era) for era in eras]
    basement_h = 46
    usable = FLOOR_Y - SURFACE_Y - 14 - basement_h
    heights = [usable * w / sum(weights) for w in weights]

    body, labels, marks = [], [], []
    bed_center = {}  # month -> function x -> y, for placing fossils and crystals
    top_curve = lambda x: SURFACE_Y + 14 + wave(x, "surface", 1.5)
    y_cursor = SURFACE_Y + 14
    current_month = f"{today.year}-{today.month:02d}"

    for idx, era in enumerate(eras):
        era_top = top_curve
        era_bottom_y = y_cursor + heights[idx]
        is_last = idx == len(eras) - 1
        if is_last:
            base_key = "basement"
            era_bottom = lambda x, b=era_bottom_y + basement_h: FLOOR_Y + 40
        else:
            gap_key = f"gap-{gaps[idx][0][0]}"
            era_bottom = lambda x, b=era_bottom_y, k=gap_key: b + wave(x, k, 7) + 3 * math.sin(x / 9)
        slope = math.tan(math.radians(9 * idx))  # older eras dip further
        clip_id = f"era{idx}"
        top_pts = [(x, era_top(x)) for x in XS]
        bot_pts = [(x, min(era_bottom(x), FLOOR_Y)) for x in reversed(XS)]
        body.append(f'<clipPath id="{clip_id}">{poly(top_pts + bot_pts)}</clipPath>')
        group = [f'<g clip-path="url(#{clip_id})">']

        total = weights[idx]
        beds = list(era)
        if is_last:
            beds.append(("basement", None))
        y_at_pivot = y_cursor
        for n, (month, count) in enumerate(beds):
            thick = basement_h if count is None else heights[idx] * math.sqrt(count) / total
            y0, y1 = y_at_pivot, y_at_pivot + thick
            first, last_bed = n == 0, n == len(beds) - 1

            def edge(x, y, key, open_end):
                if open_end is not None:
                    return open_end
                return y + slope * (PIVOT_X - x) + wave(x, key, 2.2 if slope else 3.2)

            top_f = (lambda x, y=y0, k=month: era_top(x) - 30) if first else (lambda x, y=y0, k=month: edge(x, y, k, None))
            if last_bed:
                bot_f = lambda x: FLOOR_Y + 60 + slope * (PIVOT_X - x)
            else:
                bot_f = lambda x, y=y1, k=beds[n + 1][0]: edge(x, y, k, None)
            shape = [(x, top_f(x)) for x in XS] + [(x, bot_f(x)) for x in reversed(XS)]
            tint = "#9C9488" if count is None else TINTS[(int(month[:4]) * 12 + int(month[5:])) % len(TINTS)]
            pat = "gneiss" if count is None else pattern_for(count)
            group.append(poly(shape, fill=tint))
            group.append(poly(shape, fill=f"url(#{pat})"))
            group.append(f'<polyline points="{" ".join(f"{x:.1f},{bot_f(x):.1f}" for x in XS)}" fill="none" stroke="{INK}" stroke-opacity=".55" stroke-width=".8"/>')
            mid = (y0 + y1) / 2
            bed_center[month] = lambda x, m=mid: m + slope * (PIVOT_X - x)
            if count is None:
                labels.append((mid, "basement", f"account opened Feb 2022", True))
            else:
                note = "still forming" if month == current_month else ""
                labels.append((mid, label_for(month), f"{count:,}" + (f"  {note}" if note else ""), False))
            y_at_pivot = y1
        group.append("</g>")
        body.extend(group)

        if not is_last:
            gap = gaps[idx]
            g_pts = [(x, era_bottom(x)) for x in XS]
            body.append(f'<polyline points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in g_pts)}" fill="none" stroke="{INK}" stroke-width="2.4" stroke-linejoin="round"/>')
            for p in range(60):  # basal conglomerate: pebbles resting on the erosion surface
                px = SEC_L + 6 + seeded(f"pebble{p}{gap_key}") * (SEC_R - SEC_L - 12)
                py = era_bottom(px) - 3 - seeded(f"py{p}{gap_key}") * 7
                r = 1.6 + seeded(f"pr{p}{gap_key}") * 2.6
                body.append(f'<ellipse cx="{px:.1f}" cy="{py:.1f}" rx="{r * 1.4:.1f}" ry="{r:.1f}" fill="{PAPER}" fill-opacity=".7" stroke="{INK}" stroke-width=".7"/>')
            silent = sum(c for _, c in gap)
            marks.append((era_bottom(PIVOT_X), "UNCONFORMITY",
                          f"{label_for(gap[0][0])} to {label_for(gap[-1][0])}: {len(gap)} months, {silent} contributions"))
            top_curve = era_bottom
        y_cursor = era_bottom_y

    inclusions = []
    by_month = {}
    for month, name in repos:
        by_month.setdefault(month, []).append(("crystal", name))
    for month, name in prs:
        by_month.setdefault(month, []).append(("fossil", name))
    for month, items in by_month.items():
        if month not in bed_center:
            continue
        span = (SEC_R - 120 - (SEC_L + 140)) / max(len(items), 1)
        for i, (kind, name) in enumerate(sorted(items)):
            x = SEC_L + 140 + span * (i + 0.5) + (seeded(name) - 0.5) * span * 0.3
            y = bed_center[month](x) + (seeded(name + "y") - 0.5) * 8
            inclusions.append(glyph(kind, x, y, name))

    return body, labels, marks, inclusions, sum(c for _, c in months), months[0][0]


def glyph(kind, x, y, name):
    tag = f'<text x="{x + 15:.1f}" y="{y + 3.5:.1f}" class="tag">{escape(name)}</text>'
    if kind == "fossil":
        pts = []
        for t in range(0, 260):
            a = t / 18.0
            r = 1.2 * math.exp(0.15 * a)
            pts.append((x + r * math.cos(a), y + r * math.sin(a)))
        spiral = " ".join(f"{px:.1f},{py:.1f}" for px, py in pts)
        ribs = "".join(
            f'<line x1="{x + 0.55 * 1.2 * math.exp(0.15 * a) * math.cos(a):.1f}" y1="{y + 0.55 * 1.2 * math.exp(0.15 * a) * math.sin(a):.1f}" '
            f'x2="{x + 1.2 * math.exp(0.15 * a) * math.cos(a):.1f}" y2="{y + 1.2 * math.exp(0.15 * a) * math.sin(a):.1f}" stroke="{INK}" stroke-width=".5"/>'
            for a in [k * 0.45 for k in range(14, 32)])
        return (f'<g><circle cx="{x:.1f}" cy="{y:.1f}" r="11.5" fill="#EDE2C8" stroke="{INK}" stroke-width=".9"/>'
                f'<polyline points="{spiral}" fill="none" stroke="{INK}" stroke-width="1"/>{ribs}</g>{tag}')
    hexa = [(x + 6 * math.cos(math.radians(60 * k + 30)), y + 6 * math.sin(math.radians(60 * k + 30))) for k in range(6)]
    return (poly(hexa, fill="#F6F0E2", stroke=INK, stroke_width=".9")
            + f'<line x1="{x:.1f}" y1="{y - 6:.1f}" x2="{x:.1f}" y2="{y + 6:.1f}" stroke="{INK}" stroke-width=".5"/>' + tag)


def place_labels(labels, min_gap=13.5):
    placed, last = [], -1e9
    for mid, name, value, faint in sorted(labels):
        y = max(mid, last + min_gap)
        placed.append((mid, y, name, value, faint))
        last = y
    overflow = last - (FLOOR_Y - 4)
    if overflow > 0:
        placed = [(m, y - overflow, n, v, f) for m, y, n, v, f in placed]
    return placed


DEFS = f"""<defs>
<pattern id="sand" width="9" height="9" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r=".7" fill="{INK}" fill-opacity=".45"/><circle cx="6.5" cy="6" r=".6" fill="{INK}" fill-opacity=".35"/></pattern>
<pattern id="shale" width="22" height="7" patternUnits="userSpaceOnUse"><line x1="1" y1="3.5" x2="13" y2="3.5" stroke="{INK}" stroke-opacity=".35" stroke-width=".7"/></pattern>
<pattern id="lime" width="28" height="12" patternUnits="userSpaceOnUse"><path d="M0 .5H28M0 6.5H28M7 .5V6.5M21 6.5V12" stroke="{INK}" stroke-opacity=".3" stroke-width=".7" fill="none"/></pattern>
<pattern id="massive" width="16" height="16" patternUnits="userSpaceOnUse"><path d="M2 14L6 10M10 6L13 3" stroke="{INK}" stroke-opacity=".28" stroke-width=".7"/><circle cx="12" cy="12" r=".7" fill="{INK}" fill-opacity=".3"/></pattern>
<pattern id="gneiss" width="40" height="10" patternUnits="userSpaceOnUse"><path d="M0 5Q10 0 20 5T40 5" stroke="{INK}" stroke-opacity=".35" stroke-width=".8" fill="none"/></pattern>
<filter id="paper"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="7"/><feColorMatrix values="0 0 0 0 .17 0 0 0 0 .13 0 0 0 0 .09 0 0 0 .07 0"/><feComposite in2="SourceGraphic" operator="in"/></filter>
</defs>
<style>
.serif{{font-family:Georgia,"Times New Roman",serif}}
.cap{{font-family:Georgia,"Times New Roman",serif;letter-spacing:.18em;text-transform:uppercase}}
.tag{{font-family:Georgia,"Times New Roman",serif;font-style:italic;font-size:10.5px;fill:{INK}}}
.bit{{animation:drill 5.5s cubic-bezier(.5,0,.3,1) .6s both}}
.bore{{stroke-dasharray:4 3;animation:bore 5.5s cubic-bezier(.5,0,.3,1) .6s both}}
@keyframes drill{{from{{transform:translateY(0)}}to{{transform:translateY({FLOOR_Y - SURFACE_Y - 30}px)}}}}
@keyframes bore{{from{{clip-path:inset(0 0 100% 0)}}to{{clip-path:inset(0 0 0 0)}}}}
@media (prefers-reduced-motion:reduce){{.bit,.bore{{animation:none}}}}
</style>"""


def render(months, repos, prs, today):
    body, labels, marks, inclusions, total, first = draw(months, repos, prs, today)
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
           f'aria-label="Core sample: a geological section through {total:,} GitHub contributions since {label_for(first)}, '
           f'one rock bed per month, with merged upstream pull requests as fossils and founded repositories as crystals.">',
           DEFS,
           f'<rect width="{W}" height="{H}" fill="{PAPER}"/>',
           f'<rect width="{W}" height="{H}" filter="url(#paper)"/>',
           f'<rect x="18" y="18" width="{W - 36}" height="{H - 36}" fill="none" stroke="{INK}" stroke-width="1.4"/>',
           f'<rect x="24" y="24" width="{W - 48}" height="{H - 48}" fill="none" stroke="{INK}" stroke-width=".5"/>',
           f'<text x="{SEC_L}" y="66" class="cap" font-size="13" fill="{INK}">Plate VIII  ·  Section through the account of Zaid Ali Syed</text>',
           f'<text x="{SEC_L}" y="102" class="serif" font-size="31" fill="{INK}">Core sample, {label_for(first)} to the present</text>',
           f'<text x="{SEC_L}" y="128" class="serif" font-size="14" font-style="italic" fill="{INK}" fill-opacity=".8">'
           f'{total:,} contributions laid down one month per bed. Redrawn every night from the GitHub API.</text>']

    # ground surface, rig and borehole
    out.append(f'<rect x="{SEC_L}" y="{SURFACE_Y}" width="{SEC_R - SEC_L}" height="14" fill="#6E6A3E"/>')
    for i in range(SEC_L, SEC_R, 7):
        h = 3 + seeded(f"grass{i}") * 5
        out.append(f'<line x1="{i}" y1="{SURFACE_Y}" x2="{i + 1.5:.1f}" y2="{SURFACE_Y - h:.1f}" stroke="#4E5A2C" stroke-width=".9"/>')
    out.extend(body)
    rig_x = SEC_L + 70
    out.append(f'<path d="M{rig_x - 16} {SURFACE_Y}L{rig_x} {SURFACE_Y - 44}L{rig_x + 16} {SURFACE_Y}M{rig_x - 10} {SURFACE_Y - 14}H{rig_x + 10}M{rig_x - 6} {SURFACE_Y - 28}H{rig_x + 6}" stroke="{INK}" stroke-width="1.3" fill="none"/>')
    out.append(f'<line class="bore" x1="{rig_x}" y1="{SURFACE_Y}" x2="{rig_x}" y2="{FLOOR_Y - 6}" stroke="{INK}" stroke-width="1.6"/>')
    out.append(f'<path class="bit" d="M{rig_x - 4} {SURFACE_Y + 6}h8l-4 9z" fill="{INK}"/>')
    out.append(f'<text x="{rig_x + 22}" y="{SURFACE_Y - 30}" class="tag">today, {today.isoformat()}</text>')
    out.extend(inclusions)

    # stratigraphic log on the right
    out.append(f'<text x="{LABEL_X}" y="{SURFACE_Y - 10}" class="cap" font-size="10.5" fill="{INK}">Bed            Contributions</text>')
    for mid, y, name, value, faint in place_labels(labels):
        op = ".6" if faint else "1"
        out.append(f'<path d="M{PIVOT_X} {mid:.1f}L{LABEL_X - 14} {mid:.1f}L{LABEL_X - 6} {y:.1f}" stroke="{INK}" stroke-width=".5" fill="none" stroke-opacity=".7"/>')
        out.append(f'<circle cx="{PIVOT_X}" cy="{mid:.1f}" r="1.6" fill="{INK}"/>')
        out.append(f'<text x="{LABEL_X}" y="{y + 3.8:.1f}" class="serif" font-size="11.5" fill="{INK}" fill-opacity="{op}">{escape(name)}</text>')
        out.append(f'<text x="{W - 52}" y="{y + 3.8:.1f}" class="serif" font-size="11.5" text-anchor="end" fill="{INK}" fill-opacity="{op}" font-style="italic">{escape(value)}</text>')
    for y, title, detail in marks:
        out.append(f'<text x="{SEC_L + 160}" y="{y - 14:.1f}" class="cap" font-size="11" fill="{INK}" font-weight="bold">{title}</text>')
        out.append(f'<text x="{SEC_L + 300}" y="{y - 14:.1f}" class="tag" font-size="11.5">{escape(detail)}</text>')

    legend_y = FLOOR_Y + 32
    out.append(f'<line x1="{SEC_L}" y1="{FLOOR_Y + 12}" x2="{W - 52}" y2="{FLOOR_Y + 12}" stroke="{INK}" stroke-width=".5"/>')
    out.append(glyph("fossil", SEC_L + 12, legend_y, "fossil: a pull request merged into someone else's public code").replace('class="tag"', 'class="tag" font-size="11.5"'))
    out.append(glyph("crystal", SEC_L + 452, legend_y, "crystal: a public repository founded").replace('class="tag"', 'class="tag" font-size="11.5"'))
    out.append(f'<text x="{SEC_L + 720}" y="{legend_y + 4}" class="tag" font-size="11.5">bed thickness grows with the square root of contributions</text>')
    out.append("</svg>")
    return "\n".join(out)


def main():
    today = datetime.now(timezone.utc).date()
    months = monthly_contributions(today)
    if not months:
        sys.exit("no contribution months returned; leaving the old SVG in place")
    svg = render(months, founded_repos(), merged_upstream_prs(), today)
    with open(OUT_PATH, "w", encoding="utf-8", newline="\n") as f:
        f.write(svg)
    print(f"wrote {OUT_PATH}: {len(months)} months, {sum(c for _, c in months)} contributions")


if __name__ == "__main__":
    main()
