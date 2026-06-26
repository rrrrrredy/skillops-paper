from __future__ import annotations

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PACKET_PATH = REPO_ROOT / "docs" / "human_review_execution_packet.md"


class HumanReviewExecutionPacketTests(unittest.TestCase):
    def test_packet_exists_and_links_core_artifacts(self) -> None:
        text = PACKET_PATH.read_text(encoding="utf-8")
        self.assertIn("v1.2.0", text)
        self.assertIn("10.5281/zenodo.20900771", text)
        self.assertIn("results/tables/external_pilot_annotation_worklist.csv", text)
        self.assertIn("results/tables/external_pilot_annotation_calibration.csv", text)
        self.assertIn("results/tables/external_annotation_packet.csv", text)

    def test_packet_requires_consent_and_data_boundaries(self) -> None:
        text = " ".join(PACKET_PATH.read_text(encoding="utf-8").lower().split())
        for phrase in (
            "participation is voluntary",
            "no credentials",
            "private repositories",
            "personal contact",
            "study-local pseudonyms",
            "do not store direct contact details",
        ):
            self.assertIn(phrase, text)

    def test_packet_preserves_evidence_boundary(self) -> None:
        text = PACKET_PATH.read_text(encoding="utf-8").lower()
        self.assertIn("protocol artifact, not collected evidence", text)
        self.assertIn("readiness evidence only", text)
        self.assertIn("outcome-bearing claims require", text)
        self.assertIn("reliability statistics", text)

    def test_packet_defines_stop_conditions(self) -> None:
        text = PACKET_PATH.read_text(encoding="utf-8").lower()
        self.assertIn("stop conditions", text)
        self.assertIn("more than 20 percent", text)
        self.assertIn("private credentials", text)
        self.assertIn("metadata boundary", text)


if __name__ == "__main__":
    unittest.main()
