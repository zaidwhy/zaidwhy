"""Offline checks for the profile plates: era splitting, and that every plate is valid SVG.

run: python -m unittest discover -s scripts -p "test_*.py"
No network: the core sample is rendered from synthetic months.
"""
import os
import sys
import tempfile
import unittest
import xml.dom.minidom
from datetime import date

sys.path.insert(0, os.path.dirname(__file__))
import core_sample  # noqa: E402
import plates  # noqa: E402
import repo_plates  # noqa: E402


class SplitIntoEras(unittest.TestCase):
    def test_three_quiet_months_make_an_unconformity(self):
        months = [("2024-06", 55), ("2024-07", 3), ("2024-08", 2), ("2024-09", 1), ("2024-10", 40)]
        eras, gaps = core_sample.split_into_eras(months)
        self.assertEqual(eras, [[("2024-10", 40)], [("2024-06", 55)]])
        self.assertEqual(len(gaps), 1)
        self.assertEqual([m for m, _ in gaps[0]], ["2024-07", "2024-08", "2024-09"])

    def test_two_quiet_months_stay_thin_beds(self):
        months = [("2024-06", 55), ("2024-07", 3), ("2024-08", 2), ("2024-09", 40)]
        eras, gaps = core_sample.split_into_eras(months)
        self.assertEqual(gaps, [])
        self.assertEqual(len(eras[0]), 4)

    def test_trailing_quiet_months_are_the_present_not_a_gap(self):
        months = [("2026-01", 20), ("2026-02", 1), ("2026-03", 1), ("2026-04", 1)]
        eras, gaps = core_sample.split_into_eras(months)
        self.assertEqual(gaps, [])
        self.assertEqual(eras[0][-1], ("2026-04", 1))


class Rendering(unittest.TestCase):
    def assertValidSvg(self, svg_text):
        doc = xml.dom.minidom.parseString(svg_text.encode())
        self.assertEqual(doc.documentElement.tagName, "svg")
        self.assertTrue(doc.getElementsByTagName("metadata"), "authorship manifest missing")
        self.assertNotIn(chr(0x2014), svg_text)
        # A renderer without CSS animation shows the base style, so nothing may start hidden there.
        self.assertNotRegex(svg_text, r"\.[\w-]+\{[^}]*opacity:0[;}]")

    def test_core_sample_renders_with_gap_fossil_and_crystal(self):
        months = [("2024-06", 55), ("2024-07", 63), ("2024-08", 2), ("2024-09", 0), ("2024-10", 1), ("2024-11", 900), ("2024-12", 300)]
        svg = core_sample.render(months, [("2024-11", "some-repo")], [("2024-12", "lib #1")], date(2024, 12, 15))
        self.assertValidSvg(svg)
        self.assertIn("UNCONFORMITY", svg)
        self.assertIn("still forming", svg)
        self.assertIn("some-repo", svg)
        self.assertIn("lib #1", svg)

    def test_core_sample_renders_without_any_gap(self):
        svg = core_sample.render([("2026-09", 800), ("2026-10", 600)], [], [], date(2026, 10, 28))
        self.assertValidSvg(svg)
        self.assertNotIn("UNCONFORMITY", svg)

    def test_core_sample_stays_inside_its_size_budget(self):
        # It is the first image on the profile; three years of beds measured 102 KB after outlines were deduplicated.
        months = [(f"{2024 + (i + 5) // 12}-{(i + 5) % 12 + 1:02d}", 60 if i % 7 else 900) for i in range(36)]
        svg = core_sample.render(months, [], [], date(2027, 5, 1))
        self.assertLess(len(svg.encode()), 130_000)

    def test_every_survey_plate_is_valid_svg(self):
        with tempfile.TemporaryDirectory() as out:
            original = plates.ASSETS
            plates.ASSETS = out
            try:
                for draw in (plates.route, plates.specimens, plates.specimens_narrow, plates.faults, plates.faults_narrow, plates.assays,
                             plates.excavation, plates.fieldwork, plates.seal):
                    draw()
            finally:
                plates.ASSETS = original
            names = sorted(os.listdir(out))
            self.assertEqual(len(names), 9)
            for name in names:
                with open(os.path.join(out, name), encoding="utf-8") as f:
                    with self.subTest(plate=name):
                        self.assertValidSvg(f.read())


class PlateFactsMatchReadme(unittest.TestCase):
    """plates.py copies its numbers from README.md, where each sits beside its source link.
    A number on a plate that the README does not state is a claim without a receipt."""

    def test_every_number_on_a_plate_is_stated_in_the_readme(self):
        import html
        import re

        readme_path = os.path.join(os.path.dirname(__file__), "..", "README.md")
        with open(readme_path, encoding="utf-8") as f:
            readme = f.read()
        # nightly bot blocks and ISO dates are full of digits that are not claims
        readme = re.sub(r"<!-- (ACTIVITY|STATUS):START -->.*?<!-- \1:END -->", "", readme, flags=re.S)
        readme = re.sub(r"\d{4}-\d{2}-\d{2}", "", readme).replace(",", "")
        with tempfile.TemporaryDirectory() as out:
            original = plates.ASSETS
            plates.ASSETS = out
            try:
                for draw in (plates.specimens, plates.specimens_narrow, plates.faults, plates.faults_narrow, plates.assays, plates.excavation, plates.fieldwork, plates.seal):
                    draw()
            finally:
                plates.ASSETS = original
            for name in sorted(os.listdir(out)):
                with open(os.path.join(out, name), encoding="utf-8") as f:
                    texts = [html.unescape(t) for t in re.findall(r"<text[^>]*>([^<]*)</text>", f.read())]
                for label in texts:
                    if re.fullmatch(r"[\d,]+|no\. \d+", label.strip()):
                        continue  # axis ticks and catalogue numbers, not claims
                    for number in re.findall(r"\d[\d,.]*k?", label):
                        number = number.rstrip(".,").replace(",", "")
                        with self.subTest(plate=name, label=label):
                            self.assertRegex(readme, rf"(?<![\d.]){re.escape(number)}(?!\d)")


class RepoPlates(unittest.TestCase):
    def test_every_listed_repo_renders_from_one_commit(self):
        for repo in repo_plates.REPOS:
            with self.subTest(repo=repo):
                svg = repo_plates.plate(repo, [date(2026, 10, 28)], "2026-10-28")
                xml.dom.minidom.parseString(svg.encode())
                self.assertIn("1 commit, one band per week", svg)
                self.assertIn("1 commit over 1 week,", svg)
                self.assertNotIn(chr(0x2014), svg)

    def test_strip_spans_first_to_newest_commit(self):
        days = [date(2026, 1, 5), date(2026, 1, 6), date(2026, 10, 1)]
        svg = repo_plates.plate("augur", days, "2026-10-28")
        self.assertIn("Jan 2026 to Oct 2026", svg)
        self.assertIn("3 commits", svg)


if __name__ == "__main__":
    unittest.main()
