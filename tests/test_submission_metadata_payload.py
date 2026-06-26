from __future__ import annotations

import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PAYLOAD_PATH = REPO_ROOT / "docs" / "submission_metadata_payload.md"
PAPER_PATH = REPO_ROOT / "paper" / "main.tex"
MANIFEST_PATH = REPO_ROOT / "docs" / "submission_package_manifest.md"
CHECKLIST_PATH = REPO_ROOT / "docs" / "submission_execution_checklist.md"


TITLE = "SkillOps: A Practical Framework for Designing, Testing, and Operating Modular Skills in Personal AI Agents"
VERSION_DOI = "10.5281/zenodo.20907648"
CONCEPT_DOI = "10.5281/zenodo.20061198"
PDF_HASH = "687B3952611A176BAB23A2A2C223D29B5BBF1C63903080B08EA2051A57542F3D"
SOURCE_HASH = "0A41FA212495EFBDE0C7D9166F2DEBE4E5517C8CD4185B00634F551382A917CE"


def normalized(text: str) -> str:
    return " ".join(text.split())


class SubmissionMetadataPayloadTests(unittest.TestCase):
    def test_payload_uses_current_title_and_author(self) -> None:
        payload = PAYLOAD_PATH.read_text(encoding="utf-8")
        paper = normalized(PAPER_PATH.read_text(encoding="utf-8"))
        self.assertIn(TITLE, payload)
        self.assertIn("Song Luo", payload)
        self.assertIn("luosongred@gmail.com", payload)
        self.assertIn("June 2026", payload)
        self.assertIn("SkillOps: A Practical Framework", paper)

    def test_payload_links_release_identity_and_hashes(self) -> None:
        payload = PAYLOAD_PATH.read_text(encoding="utf-8")
        manifest = MANIFEST_PATH.read_text(encoding="utf-8")
        for required in (
            "releases/tag/v1.3.0",
            VERSION_DOI,
            CONCEPT_DOI,
            "release/skillops-paper.pdf",
            "release/skillops-paper-source.zip",
            PDF_HASH,
            SOURCE_HASH,
        ):
            self.assertIn(required, manifest)
            if required in {PDF_HASH, SOURCE_HASH}:
                continue
            self.assertIn(required, payload)

    def test_payload_abstract_matches_paper_claim_boundary(self) -> None:
        payload = normalized(PAYLOAD_PATH.read_text(encoding="utf-8"))
        paper = normalized(PAPER_PATH.read_text(encoding="utf-8"))
        for phrase in (
            "metadata-only third-party corpus protocol",
            "machine-checkable external smoke metrics",
            "LLM-as-judge case-label sensitivity plan",
            "not a claim that a particular skill format universally improves model behavior",
        ):
            self.assertIn(phrase, payload)
            self.assertIn(phrase, paper)

    def test_payload_category_guidance_matches_checklist(self) -> None:
        payload = PAYLOAD_PATH.read_text(encoding="utf-8")
        checklist = CHECKLIST_PATH.read_text(encoding="utf-8")
        for category in ("cs.SE", "cs.AI", "cs.HC"):
            self.assertIn(category, payload)
            self.assertIn(category, checklist)
        self.assertIn("Primary category | `cs.SE`", payload)

    def test_payload_preserves_nonclaimable_limits(self) -> None:
        payload = normalized(PAYLOAD_PATH.read_text(encoding="utf-8")).lower()
        for phrase in (
            "does not report a completed powered external study",
            "machine-checkable external-smoke metrics",
            "production deployment validation",
            "broad user-study outcome",
            "verified github/zenodo release doi",
        ):
            self.assertIn(phrase, payload)
        self.assertIsNone(re.search("Long" + "Cat", payload, flags=re.IGNORECASE))


if __name__ == "__main__":
    unittest.main()
