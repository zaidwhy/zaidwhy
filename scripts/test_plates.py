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
import apply_repo_plates  # noqa: E402


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

    def test_phone_cut_keeps_the_rock_and_drops_the_small_labels(self):
        months = [("2024-06", 55), ("2024-07", 3), ("2024-08", 2), ("2024-09", 0), ("2024-10", 900)]
        cut = core_sample.phone_cut(core_sample.render(months, [("2024-10", "some-repo")], [], date(2024, 10, 20)), "2024-06")
        self.assertValidSvg(cut)
        labels = [t for t in __import__("re").findall(r"<text[^>]*>([^<]*)</text>", cut)]
        self.assertEqual(labels, ["Core sample", "one bed per month since Jun 2024"])
        self.assertIn("<use", cut)
        self.assertNotIn("UNCONFORMITY", cut)

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
                for draw in (plates.route, plates.route_narrow, plates.specimens, plates.specimens_narrow, plates.faults, plates.faults_narrow, plates.assays, plates.assays_narrow,
                             plates.excavation, plates.excavation_narrow, plates.fieldwork, plates.fieldwork_narrow, plates.seal, plates.seal_narrow):
                    draw()
            finally:
                plates.ASSETS = original
            names = sorted(os.listdir(out))
            self.assertEqual(len(names), 14)
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
                for draw in (plates.specimens, plates.specimens_narrow, plates.faults, plates.faults_narrow, plates.assays, plates.assays_narrow, plates.excavation, plates.excavation_narrow, plates.fieldwork, plates.fieldwork_narrow, plates.seal, plates.seal_narrow):
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


class RepoPlateFactsHaveASource(unittest.TestCase):
    """Each number on a repository plate must be stated on the profile README, or listed here with its source."""

    OFF_PAGE = {
        ("longmemeval-key-audit", "141"): "status line of github.com/zaidwhy/longmemeval-key-audit README, read 2026-10-28",
    }

    def test_every_repo_plate_number_is_stated_somewhere_checkable(self):
        import re

        with open(os.path.join(os.path.dirname(__file__), "..", "README.md"), encoding="utf-8") as f:
            readme = f.read()
        readme = re.sub(r"<!-- (ACTIVITY|STATUS):START -->.*?<!-- \1:END -->", "", readme, flags=re.S)
        readme = re.sub(r"\d{4}-\d{2}-\d{2}", "", readme).replace(",", "")
        for repo, (_, _, thesis, notes) in repo_plates.REPOS.items():
            for note in notes + [thesis]:
                doi = re.search(r"10\.5281/zenodo\.\d+", note)
                if doi:
                    with self.subTest(repo=repo, note=note):
                        self.assertIn(doi.group(0), readme)
                    continue
                for number in re.findall(r"\d[\d,.]*k?", note):
                    number = number.rstrip(".,").replace(",", "")
                    if (repo, number) in self.OFF_PAGE:
                        continue
                    with self.subTest(repo=repo, note=note):
                        self.assertRegex(readme, rf"(?<![\d.]){re.escape(number)}(?!\d)")


class ScriptsAreClean(unittest.TestCase):
    def test_no_control_characters_in_any_script(self):
        # Shell heredoc edits have twice turned a regex backreference into chr(1); the regex still compiled.
        folder = os.path.dirname(__file__)
        for name in sorted(os.listdir(folder)):
            if name.endswith(".py"):
                with open(os.path.join(folder, name), encoding="utf-8") as f:
                    body = f.read()
                with self.subTest(script=name):
                    self.assertFalse([c for c in body if ord(c) < 32 and c not in "\n\t\r"])


class InstallRepoPlates(unittest.TestCase):
    def setUp(self):
        from pathlib import Path
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        self.plates, self.clone = root / "plates", root / "clone"
        self.plates.mkdir()
        self.clone.mkdir()
        days = [date(2026, 1, 5), date(2026, 10, 1)]
        (self.plates / "augur.svg").write_text(repo_plates.plate("augur", days, "2026-10-28"), encoding="utf-8")
        (self.plates / "augur-narrow.svg").write_text(repo_plates.plate_narrow("augur", days, "2026-10-28"), encoding="utf-8")
        (self.clone / "README.md").write_text("# augur\n\nBody text.\n", encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def test_fresh_readme_gets_header_and_footer_and_rerun_changes_nothing(self):
        apply_repo_plates.install(self.plates, "augur", self.clone)
        first = (self.clone / "README.md").read_text(encoding="utf-8")
        self.assertTrue(first.startswith("<picture>"))
        self.assertIn("# augur", first)
        self.assertEqual(first.count("survey at [github.com/zaidwhy]"), 1)
        self.assertTrue((self.clone / ".github" / "plate-narrow.svg").is_file())
        apply_repo_plates.install(self.plates, "augur", self.clone)
        self.assertEqual((self.clone / "README.md").read_text(encoding="utf-8"), first)

    def test_old_single_image_header_is_upgraded_in_place(self):
        (self.clone / "README.md").write_text('<img src=".github/plate.svg" alt="old" width="100%">\n\n# augur\n', encoding="utf-8")
        apply_repo_plates.install(self.plates, "augur", self.clone)
        text = (self.clone / "README.md").read_text(encoding="utf-8")
        self.assertEqual(text.count('<img src=".github/plate.svg"'), 1)
        self.assertNotIn('alt="old"', text)
        self.assertIn("plate-narrow.svg", text)

    def test_missing_phone_plate_is_refused_by_name(self):
        (self.plates / "augur-narrow.svg").unlink()
        with self.assertRaisesRegex(FileNotFoundError, "augur-narrow.svg"):
            apply_repo_plates.install(self.plates, "augur", self.clone)


class RepoPlates(unittest.TestCase):
    def test_every_listed_repo_renders_from_one_commit(self):
        for repo in repo_plates.REPOS:
            with self.subTest(repo=repo):
                svg = repo_plates.plate(repo, [date(2026, 10, 28)], "2026-10-28")
                xml.dom.minidom.parseString(svg.encode())
                self.assertIn("1 commit, one band per week", svg)
                self.assertIn("1 commit over 1 week,", svg)
                self.assertNotIn(chr(0x2014), svg)

    def test_every_listed_repo_has_a_phone_plate(self):
        for repo in repo_plates.REPOS:
            with self.subTest(repo=repo):
                svg = repo_plates.plate_narrow(repo, [date(2026, 1, 5), date(2026, 10, 1)], "2026-10-28")
                doc = xml.dom.minidom.parseString(svg.encode())
                self.assertEqual(doc.documentElement.getAttribute("width"), str(repo_plates.NARROW_W))
                self.assertIn(repo_plates.REPOS[repo][1], svg)

    def test_strip_spans_first_to_newest_commit(self):
        days = [date(2026, 1, 5), date(2026, 1, 6), date(2026, 10, 1)]
        svg = repo_plates.plate("augur", days, "2026-10-28")
        self.assertIn("Jan 2026 to Oct 2026", svg)
        self.assertIn("3 commits", svg)


if __name__ == "__main__":
    unittest.main()
