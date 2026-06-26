from __future__ import annotations

import csv
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PROMPT_PATH = REPO_ROOT / "experiments" / "prompts" / "llm_judge_case_label_sensitivity.md"
PLAN_CSV_PATH = REPO_ROOT / "results" / "experiments" / "llm_judge_sensitivity_plan.csv"
PLAN_MD_PATH = REPO_ROOT / "results" / "experiments" / "llm_judge_sensitivity_plan.md"
SUMMARY_CSV_PATH = REPO_ROOT / "results" / "experiments" / "llm_judge_sensitivity_summary.csv"
SUMMARY_MD_PATH = REPO_ROOT / "results" / "experiments" / "llm_judge_sensitivity_summary.md"


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


class LlmJudgeSensitivityTests(unittest.TestCase):
    def test_plan_and_summary_files_exist(self) -> None:
        for path in (PROMPT_PATH, PLAN_CSV_PATH, PLAN_MD_PATH, SUMMARY_CSV_PATH, SUMMARY_MD_PATH):
            self.assertTrue(path.exists(), f"Missing {path}")
            self.assertGreater(path.stat().st_size, 0, f"Empty {path}")

    def test_plan_is_secondary_label_sensitivity(self) -> None:
        rows = read_csv_rows(PLAN_CSV_PATH)
        self.assertGreaterEqual(len(rows), 1)
        self.assertEqual({row["evidence_role"] for row in rows}, {"secondary_label_sensitivity"})
        self.assertTrue({row["run_status"] for row in rows} <= {"not_run_case_label_sensitivity", "not_run_missing_credentials", "submitted_bounded_live"})
        self.assertTrue(all(row["prompt_hash"] for row in rows))

    def test_summary_does_not_replace_primary_metrics(self) -> None:
        summary_text = SUMMARY_MD_PATH.read_text(encoding="utf-8")
        self.assertIn("case-label stability only", summary_text)
        self.assertIn("Primary external-smoke metrics remain machine-checkable", summary_text)
        rows = read_csv_rows(SUMMARY_CSV_PATH)
        self.assertGreaterEqual(len(rows), 1)
        self.assertTrue({row["status"] for row in rows} <= {"not_run_case_label_sensitivity", "not_run_missing_credentials", "secondary_sensitivity"})


if __name__ == "__main__":
    unittest.main()
