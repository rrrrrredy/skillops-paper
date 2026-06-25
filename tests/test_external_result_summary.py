from __future__ import annotations

import csv
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
RESULT_SUMMARY_CSV_PATH = REPO_ROOT / "results" / "experiments" / "external_result_summary.csv"
RESULT_SUMMARY_MD_PATH = REPO_ROOT / "results" / "experiments" / "external_result_summary.md"
STAT_SUMMARY_CSV_PATH = REPO_ROOT / "results" / "experiments" / "external_statistical_summary.csv"
STAT_SUMMARY_MD_PATH = REPO_ROOT / "results" / "experiments" / "external_statistical_summary.md"


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


class ExternalResultSummaryTests(unittest.TestCase):
    def test_external_result_summary_files_exist(self) -> None:
        for path in (RESULT_SUMMARY_CSV_PATH, RESULT_SUMMARY_MD_PATH, STAT_SUMMARY_CSV_PATH, STAT_SUMMARY_MD_PATH):
            self.assertTrue(path.exists(), f"Missing {path}")
            self.assertGreater(path.stat().st_size, 0, f"Empty {path}")

    def test_external_result_summary_reports_boundary_or_results(self) -> None:
        rows = read_csv_rows(RESULT_SUMMARY_CSV_PATH)
        self.assertGreaterEqual(len(rows), 1)
        statuses = {row["status"] for row in rows}
        self.assertTrue(statuses <= {"no_results", "computed_from_external_results"})
        if statuses == {"no_results"}:
            self.assertEqual(rows[0]["metric"], "completed_records")
            self.assertEqual(rows[0]["numerator"], "0")

    def test_external_statistical_summary_has_planned_metrics(self) -> None:
        rows = read_csv_rows(STAT_SUMMARY_CSV_PATH)
        metrics = {row["metric"] for row in rows}
        self.assertIn("routing_correct", metrics)
        self.assertIn("constraint_compliance", metrics)
        self.assertIn("parse_success", metrics)
        self.assertTrue({row["result_status"] for row in rows} <= {"no_results", "requires_statistical_model_run"})

    def test_markdown_states_no_inferential_models(self) -> None:
        text = STAT_SUMMARY_MD_PATH.read_text(encoding="utf-8")
        self.assertIn("does not run inferential models", text)


if __name__ == "__main__":
    unittest.main()
