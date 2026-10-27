#!/usr/bin/env python3
"""Install the survey plates drawn by repo_plates.py into a local clone of a repository.

Copies <plates>/<repo>.svg and <repo>-narrow.svg to the clone's .github/, puts a <picture>
header at the top of its README (the phone plate under 600 px), and a survey footer at the
bottom. Running it again only refreshes the files and the alt text, so it is safe to re-run.
Committing and pushing stay manual: each repository has its own branch and review habits.

usage: python scripts/apply_repo_plates.py <plates_dir> <repo_name> <clone_dir>
"""
import re
import shutil
import sys
from pathlib import Path

FOOTER = ("\n---\n\n<sub>One plate from the survey at [github.com/zaidwhy](https://github.com/zaidwhy). "
          "The strip on the plate above is this repository's own commit history, one band per week.</sub>\n")
HEADER = re.compile(r'(<picture>\n<source media="\(max-width: 600px\)" srcset="\.github/plate-narrow\.svg">\n)?'
                    r'<img src="\.github/plate\.svg" alt="[^"]*" width="100%">(\n</picture>)?')


def install(plates_dir, repo, clone):
    wide, narrow = plates_dir / f"{repo}.svg", plates_dir / f"{repo}-narrow.svg"
    for plate in (wide, narrow):
        if not plate.is_file():
            raise FileNotFoundError(f"{plate} is missing; run repo_plates.py first")
    readme = clone / "README.md"
    if not readme.is_file():
        raise FileNotFoundError(f"{readme} is missing; the plate goes at the top of the README")
    (clone / ".github").mkdir(exist_ok=True)
    shutil.copyfile(wide, clone / ".github" / "plate.svg")
    shutil.copyfile(narrow, clone / ".github" / "plate-narrow.svg")

    label = re.search(r'aria-label="([^"]*)"', wide.read_text(encoding="utf-8"))
    if not label:
        raise ValueError(f"{wide} has no aria-label to use as alt text")
    header = ('<picture>\n<source media="(max-width: 600px)" srcset=".github/plate-narrow.svg">\n'
              f'<img src=".github/plate.svg" alt="{label.group(1)}" width="100%">\n</picture>')
    text = readme.read_text(encoding="utf-8")
    found = HEADER.search(text)
    if found:
        text = text[: found.start()] + header + text[found.end():]
    else:
        text = header + "\n\n" + text
    if "survey at [github.com/zaidwhy]" not in text:
        text = text.rstrip("\n") + "\n" + FOOTER
    readme.write_text(text, encoding="utf-8", newline="\n")


def main():
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    install(Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3]))
    print(f"installed plates for {sys.argv[2]} in {sys.argv[3]}")


if __name__ == "__main__":
    main()
