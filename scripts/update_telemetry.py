#!/usr/bin/env python3
"""Pulls real commit activity and a real live-status check into README.md.

Only ever writes what the API/HTTP check actually returned. On any request
failure, the corresponding marker block is left untouched rather than
filled with placeholder content.
"""
import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone

OWNER = "zaidwhy"
ACTIVITY_REPOS = [
    "agent-factory", "augur", "aura-private-ai-memory", "autocto",
    "CivilizationOS", "coldread", "dreamos-college-project",
    "github-pr-agent", "personal-llm", "recall", "receipts-dev",
    "resume-job-fit-ai", "second-brain",
]
ACTIVITY_COUNT = 8
LIVE_SYSTEMS = [
    ("CivilizationOS", "https://civilization-os-murex.vercel.app"),
]
README_PATH = os.path.join(os.path.dirname(__file__), "..", "README.md")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
EM_DASH = chr(0x2014)


def api_get(url):
    req = urllib.request.Request(url, headers={
        "Accept": "application/vnd.github+json",
        "User-Agent": "zaidwhy-profile-telemetry",
        **({"Authorization": f"Bearer {TOKEN}"} if TOKEN else {}),
    })
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode())


def sanitize(text):
    text = text.splitlines()[0] if text else ""
    text = text.replace(EM_DASH, " - ").replace("`", "'")
    text = text.strip()
    if len(text) > 72:
        text = text[:71].rstrip() + "..."
    return text


def build_activity_block():
    commits = []
    for repo in ACTIVITY_REPOS:
        try:
            data = api_get(f"https://api.github.com/repos/{OWNER}/{repo}/commits?per_page=5")
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ValueError) as e:
            print(f"WARN: could not fetch commits for {repo}: {e}", file=sys.stderr)
            continue
        for c in data:
            try:
                date = c["commit"]["author"]["date"]
                msg = sanitize(c["commit"]["message"])
                sha = c["sha"][:7]
                url = c["html_url"]
            except (KeyError, TypeError):
                continue
            commits.append((date, repo, msg, sha, url))

    if not commits:
        return None  # leave existing block untouched

    commits.sort(key=lambda x: x[0], reverse=True)
    lines = []
    for date, repo, msg, sha, url in commits[:ACTIVITY_COUNT]:
        day = date.split("T")[0]
        lines.append(f"- `{day}` **{repo}** - {msg} ([`{sha}`]({url}))")
    return "\n".join(lines)


def build_status_block():
    lines = []
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    any_result = False
    for name, url in LIVE_SYSTEMS:
        try:
            req = urllib.request.Request(url, method="HEAD", headers={
                "User-Agent": "zaidwhy-profile-telemetry",
            })
            with urllib.request.urlopen(req, timeout=15) as resp:
                code = resp.status
            state = f"`{code} OK`" if code == 200 else f"`{code}`"
        except urllib.error.HTTPError as e:
            state = f"`{e.code}`"
        except Exception as e:
            state = f"`unreachable` ({type(e).__name__})"
        lines.append(f"- **{name}** - {state} - [{url}]({url})")
        any_result = True
    if not any_result:
        return None
    lines.append(f"\n*checked {now}, by the workflow that runs this page*")
    return "\n".join(lines)


def replace_block(content, marker, new_body):
    if new_body is None:
        return content
    start = f"<!-- {marker}:START -->"
    end = f"<!-- {marker}:END -->"
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.DOTALL)
    if not pattern.search(content):
        print(f"WARN: markers for {marker} not found, skipping", file=sys.stderr)
        return content
    return pattern.sub(f"{start}\n{new_body}\n{end}", content)


def main():
    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    content = replace_block(content, "ACTIVITY", build_activity_block())
    content = replace_block(content, "STATUS", build_status_block())

    with open(README_PATH, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)


if __name__ == "__main__":
    main()
