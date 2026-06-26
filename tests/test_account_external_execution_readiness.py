from __future__ import annotations

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
READINESS_PATH = REPO_ROOT / "docs" / "account_external_execution_readiness.md"


class AccountExternalExecutionReadinessTests(unittest.TestCase):
    def test_readiness_file_exists(self) -> None:
        self.assertTrue(READINESS_PATH.exists())
        self.assertGreater(READINESS_PATH.stat().st_size, 0)

    def test_account_side_boundaries_are_explicit(self) -> None:
        text = READINESS_PATH.read_text(encoding="utf-8")
        normalized = " ".join(text.split())
        for required in (
            "10.5281/zenodo.20900771",
            "10.5281/zenodo.20844038",
            "release/skillops-paper-source.zip",
            "release/skillops-paper.pdf",
            "is not binary provenance for the current PDF/source package",
            "docs/zenodo_file_state_audit.md",
        ):
            self.assertIn(required, text)
        for prohibited in ("provider keys", "account tokens", "payment information"):
            self.assertIn(prohibited, normalized)

    def test_human_annotation_and_provider_order_are_bounded(self) -> None:
        text = READINESS_PATH.read_text(encoding="utf-8")
        self.assertIn("32-case calibration subset", text)
        self.assertIn("96-case pilot worklist", text)
        self.assertIn("external_annotation_assignment_manifest.csv", text)
        self.assertIn("compute_external_annotation_reliability.py", text)
        self.assertIn("--sample-limit 4", text)
        self.assertIn("--max-live-rows 4", text)
        self.assertIn("Refuse unbounded provider execution", text)
        self.assertIn("Do not report human-review outcomes", text)

    def test_openai_sensitivity_plan_is_separate_from_claims(self) -> None:
        text = READINESS_PATH.read_text(encoding="utf-8")
        self.assertIn("Excluding-OpenAI Sensitivity Corpus Plan", text)
        self.assertIn("openai-agents-python", text)
        self.assertIn("openai-agents-js", text)
        self.assertIn("Replace their 28 workflow-template rows", text)
        self.assertIn("Keep claims separate", text)
        self.assertIn("sensitivity results", text)


if __name__ == "__main__":
    unittest.main()
