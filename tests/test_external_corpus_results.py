from __future__ import annotations

import csv
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DETAIL_CSV_PATH = REPO_ROOT / "results" / "tables" / "external_corpus_static_analysis.csv"
SUMMARY_CSV_PATH = REPO_ROOT / "results" / "tables" / "external_corpus_summary.csv"
SUMMARY_MD_PATH = REPO_ROOT / "results" / "tables" / "external_corpus_summary.md"


class ExternalCorpusResultsTests(unittest.TestCase):
    def test_external_corpus_result_files_exist(self) -> None:
        for path in (DETAIL_CSV_PATH, SUMMARY_CSV_PATH, SUMMARY_MD_PATH):
            self.assertTrue(path.exists(), f"Missing {path}")
            self.assertGreater(path.stat().st_size, 0, f"Empty {path}")

    def test_external_static_analysis_has_successful_github_rows(self) -> None:
        with DETAIL_CSV_PATH.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))

        self.assertGreaterEqual(len(rows), 10)
        ok_rows = [row for row in rows if row["analysis_status"].startswith("ok")]
        self.assertGreaterEqual(len(ok_rows), 5)
        self.assertTrue(any(row["skill_md_files"] not in {"", "0"} for row in ok_rows))
        self.assertTrue(any(row["test_files"] not in {"", "0"} for row in ok_rows))
        self.assertTrue(any(row["security_files"] not in {"", "0"} for row in ok_rows))

    def test_external_summary_reports_static_indicators(self) -> None:
        with SUMMARY_CSV_PATH.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))

        indicators = {row["value"]: int(row["count"]) for row in rows if row["group"] == "static_indicator"}
        self.assertIn("readme_files", indicators)
        self.assertIn("test_files", indicators)
        self.assertIn("script_files", indicators)
        self.assertGreater(indicators["readme_files"], 0)


if __name__ == "__main__":
    unittest.main()
