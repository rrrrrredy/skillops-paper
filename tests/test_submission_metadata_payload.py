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
VERSION_DOI = "10.5281/zenodo.20844038"
CONCEPT_DOI = "10.5281/zenodo.20061198"
PDF_HASH = "F9774684EB4BC2CBF42D69DB3C4169436F60B0C72FCA064DE776E615CD851D65"
SOURCE_HASH = "0E753376C3C1C16902B3A3BCA08E384AC3EE333CF6AA86A84D6C738710E80A8F"


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
            "releases/tag/v1.1.0",
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
            "two-annotator calibration worklist",
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
            "does not report a completed external human study",
            "powered external statistical result",
            "production deployment validation",
            "broad user-study outcome",
            "verify zenodo file state",
        ):
            self.assertIn(phrase, payload)
        self.assertIsNone(re.search("Long" + "Cat", payload, flags=re.IGNORECASE))


if __name__ == "__main__":
    unittest.main()
