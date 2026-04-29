from __future__ import annotations

import unittest

from tests.helpers import PAPER_PATH, PUBLIC_FACING_FILES, PUBLIC_PROCESS_TERMS, README_PATH, read_text


class PublicPresentationTests(unittest.TestCase):
    def test_paper_identity_and_repository_link(self) -> None:
        paper_text = read_text(PAPER_PATH)
        self.assertIn("Song Luo", paper_text)
        self.assertIn("luosongred@gmail.com", paper_text)
        self.assertIn("https://github.com/rrrrrredy", paper_text)
        self.assertNotIn("Independent Researcher", paper_text)

    def test_readme_avoids_draft_positioning(self) -> None:
        readme_text = read_text(README_PATH).lower()
        for term in ("draft", "initial version", "work in progress", "paper draft"):
            self.assertNotIn(term, readme_text)

    def test_public_facing_files_avoid_prohibited_process_terms(self) -> None:
        for path in PUBLIC_FACING_FILES:
            text = read_text(path).lower()
            for term in PUBLIC_PROCESS_TERMS:
                self.assertNotIn(term, text, f"Found prohibited public term {term!r} in {path}")


if __name__ == "__main__":
    unittest.main()
