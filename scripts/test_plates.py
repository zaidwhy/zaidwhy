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

    def test_every_survey_plate_is_valid_svg(self):
        with tempfile.TemporaryDirectory() as out:
            original = plates.ASSETS
            plates.ASSETS = out
            try:
                for draw in (plates.route, plates.specimens, plates.faults, plates.assays,
                             plates.excavation, plates.fieldwork, plates.seal):
                    draw()
            finally:
                plates.ASSETS = original
            names = sorted(os.listdir(out))
            self.assertEqual(len(names), 7)
            for name in names:
                with open(os.path.join(out, name), encoding="utf-8") as f:
                    with self.subTest(plate=name):
                        self.assertValidSvg(f.read())


if __name__ == "__main__":
    unittest.main()
