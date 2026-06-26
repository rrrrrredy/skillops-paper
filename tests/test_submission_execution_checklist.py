from __future__ import annotations

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CHECKLIST_PATH = REPO_ROOT / "docs" / "submission_execution_checklist.md"
MANIFEST_PATH = REPO_ROOT / "docs" / "submission_package_manifest.md"


class SubmissionExecutionChecklistTests(unittest.TestCase):
    def test_checklist_links_release_assets_and_hashes(self) -> None:
        text = CHECKLIST_PATH.read_text(encoding="utf-8")
        manifest = MANIFEST_PATH.read_text(encoding="utf-8")
        for required in (
            "release/skillops-paper-source.zip",
            "release/skillops-paper.pdf",
            "38833A57BF1F7001EEE72D3CF2ECD8E5E68B559D6DD17832F46F4F8D6FA46974",
            "98957F4295EAFA777A234A77B9A75AFB4DE9294B50E60FE5B72565BD788F03B9",
            "10.5281/zenodo.20900771",
        ):
            self.assertIn(required, text)
            self.assertIn(required, manifest)

    def test_checklist_uses_official_submission_references(self) -> None:
        text = CHECKLIST_PATH.read_text(encoding="utf-8")
        for url in (
            "https://info.arxiv.org/help/submit_tex.html",
            "https://info.arxiv.org/help/prep.html",
            "https://info.arxiv.org/help/endorsement.html",
            "https://docs.openreview.net/getting-started/creating-an-openreview-profile/signing-up-for-openreview",
            "https://docs.openreview.net/how-to-guides/submissions-comments-reviews-and-decisions",
        ):
            self.assertIn(url, text)

    def test_checklist_preserves_claim_boundaries(self) -> None:
        text = CHECKLIST_PATH.read_text(encoding="utf-8")
        self.assertIn("Do not claim completed external user study", text)
        self.assertIn("production deployment", text)
        self.assertIn("statistical significance", text)
        self.assertIn("Non-Automatable Actions", text)

    def test_checklist_names_arxiv_source_contents(self) -> None:
        text = CHECKLIST_PATH.read_text(encoding="utf-8")
        for name in ("main.tex", "main.bbl", "references.bib", "README.md"):
            self.assertIn(name, text)


if __name__ == "__main__":
    unittest.main()
