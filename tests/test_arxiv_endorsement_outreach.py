from __future__ import annotations

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
OUTREACH_PATH = REPO_ROOT / "docs" / "arxiv_endorsement_outreach.md"


class ArxivEndorsementOutreachTests(unittest.TestCase):
    def test_outreach_file_contains_official_route_and_priority(self) -> None:
        text = OUTREACH_PATH.read_text(encoding="utf-8")
        self.assertIn("https://info.arxiv.org/help/endorsement.html", text)
        self.assertIn("cs.SE", text)
        self.assertIn("John Yang", text)
        self.assertIn("Carlos E. Jimenez", text)
        self.assertIn("Shunyu Yao", text)
        self.assertIn("do not feel the paper is in scope", text)

    def test_outreach_is_small_batch_not_mass_email(self) -> None:
        text = OUTREACH_PATH.read_text(encoding="utf-8").lower()
        self.assertIn("one to three people first", text)
        self.assertIn("against emailing large numbers", text)
        self.assertIn("endorsement request link/code", text)


if __name__ == "__main__":
    unittest.main()
