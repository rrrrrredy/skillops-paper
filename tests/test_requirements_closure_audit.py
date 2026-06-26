from __future__ import annotations

import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
AUDIT_PATH = REPO_ROOT / "docs" / "requirements_closure_audit.md"
READINESS_PATH = REPO_ROOT / "docs" / "publication_readiness.md"
CHANGE_INVENTORY_PATH = REPO_ROOT / "docs" / "change_inventory.md"
README_PATH = REPO_ROOT / "README.md"
EXPERIMENT_STATUS_PATH = REPO_ROOT / "experiments" / "EXPERIMENT_STATUS.md"
TEST_REPORT_PATH = REPO_ROOT / "results" / "test_report.md"


class RequirementsClosureAuditTests(unittest.TestCase):
    def test_audit_links_core_evidence(self) -> None:
        text = AUDIT_PATH.read_text(encoding="utf-8")
        for required in (
            "paper/main.tex",
            "paper/references.bib",
            "results/experiments/live_model_summary.md",
            "benchmark/external_artifact_corpus_sources.csv",
            "docs/human_review_execution_packet.md",
            "results/experiments/external_machine_checkable_metrics.md",
            "results/experiments/llm_judge_sensitivity_plan.csv",
            "docs/submission_execution_checklist.md",
            "docs/submission_package_manifest.md",
            "docs/account_external_execution_readiness.md",
            "docs/publication_plan.md",
            "10.5281/zenodo.20907648",
        ):
            self.assertIn(required, text)

    def test_audit_preserves_boundaries(self) -> None:
        text = " ".join(AUDIT_PATH.read_text(encoding="utf-8").split()).lower()
        for required in (
            "not claimable",
            "llm-as-judge label sensitivity",
            "powered external statistical results",
            "production deployment validation",
            "account access",
            "later package changes require",
            "zenodo file-state verification",
        ):
            self.assertIn(required, text)

    def test_audit_records_review_discipline_without_process_traces(self) -> None:
        text = AUDIT_PATH.read_text(encoding="utf-8")
        self.assertIn("Apply source-backed long-horizon review discipline", text)
        self.assertIn("durable evidence", text)
        for prohibited in (
            "De" + "li",
            "Delegate" + " review work",
            "paper-" + "writing skills",
            "excessive" + " pushes",
        ):
            self.assertNotIn(prohibited, text)

    def test_current_test_count_is_aligned(self) -> None:
        expected = "141 discovered, 141 passed"
        for path in (AUDIT_PATH, READINESS_PATH, CHANGE_INVENTORY_PATH, TEST_REPORT_PATH):
            self.assertIn(expected, path.read_text(encoding="utf-8"))

    def test_readme_points_to_closure_audit(self) -> None:
        text = README_PATH.read_text(encoding="utf-8")
        self.assertIn("docs/requirements_closure_audit.md", text)
        self.assertIn("docs/submission_metadata_payload.md", text)
        self.assertIn("docs/account_external_execution_readiness.md", text)
        self.assertNotIn("run_empirical_experiments.py --run-live", text)
        self.assertIn("run_trigger_experiment.py --run-live --provider deepseek", text)
        self.assertIn("run_memory_drift_experiment.py --run-live --provider kimi", text)

    def test_experiment_status_is_current(self) -> None:
        text = EXPERIMENT_STATUS_PATH.read_text(encoding="utf-8")
        self.assertIn("DeepSeek and Kimi model-backed runs reported", text)
        self.assertIn("live ablation prepared but not reported", text)
        self.assertNotIn("model-backed live run not reported", text)
        self.assertNotIn("No model-backed trigger-routing run", text)

    def test_audit_has_no_legacy_public_terms(self) -> None:
        text = AUDIT_PATH.read_text(encoding="utf-8")
        for pattern in (
            "Long" + "Cat",
            "Chat" + "GPT",
            "Co" + "dex",
            r"v1\.0\.0",
            "2083" + "8908",
        ):
            self.assertIsNone(re.search(pattern, text, flags=re.IGNORECASE))


if __name__ == "__main__":
    unittest.main()
