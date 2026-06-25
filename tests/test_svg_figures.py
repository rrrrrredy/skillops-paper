from __future__ import annotations

import unittest

from tests.helpers import (
    EVALUATION_PIPELINE_SVG,
    SKILL_ANATOMY_SVG,
    SKILLOPS_LIFECYCLE_SVG,
    file_is_non_empty,
    parse_svg,
    svg_text,
    tag_local_name,
)


EXPECTED_LABELS = {
    SKILLOPS_LIFECYCLE_SVG: [
        "design",
        "lint",
        "security scan",
        "runtime injection",
        "execution",
        "self-audit",
    ],
    SKILL_ANATOMY_SVG: [
        "metadata",
        "trigger contract",
        "instructions",
        "context boundary",
        "memory interface",
        "security checks",
    ],
    EVALUATION_PIPELINE_SVG: [
        "artifact inventory",
        "benchmark cases",
        "scripts",
        "result tables",
        "interpretation",
    ],
}


class SvgFigureTests(unittest.TestCase):
    def test_svg_files_are_non_empty_and_parseable(self) -> None:
        for path in EXPECTED_LABELS:
            self.assertTrue(path.exists(), f"Missing SVG figure: {path}")
            self.assertTrue(file_is_non_empty(path), f"Empty SVG figure: {path}")
            root = parse_svg(path)
            self.assertEqual(tag_local_name(root.tag), "svg", f"Unexpected root tag in {path}")

    def test_svg_files_contain_expected_labels(self) -> None:
        for path, labels in EXPECTED_LABELS.items():
            text = svg_text(path)
            for label in labels:
                self.assertIn(label, text, f"Missing expected label {label!r} in {path}")


if __name__ == "__main__":
    unittest.main()
