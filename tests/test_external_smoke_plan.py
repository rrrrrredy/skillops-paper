from __future__ import annotations

import csv
import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PLAN_CSV_PATH = REPO_ROOT / "results" / "experiments" / "external_smoke_test_plan.csv"
PLAN_MD_PATH = REPO_ROOT / "results" / "experiments" / "external_smoke_test_plan.md"

SECRET_LIKE_PATTERN = re.compile(r"sk-[A-Za-z0-9]{12,}")


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


class ExternalSmokePlanTests(unittest.TestCase):
    def test_smoke_plan_files_exist(self) -> None:
        for path in (PLAN_CSV_PATH, PLAN_MD_PATH):
            self.assertTrue(path.exists(), f"Missing {path}")
            self.assertGreater(path.stat().st_size, 0, f"Empty {path}")

    def test_smoke_plan_is_bounded_and_no_secret(self) -> None:
        rows = read_csv_rows(PLAN_CSV_PATH)
        self.assertEqual(len(rows), 4)
        providers = {row["provider"] for row in rows}
        self.assertEqual(providers, {"deepseek", "kimi"})
        self.assertTrue(all("--sample-limit 2" in row["planned_command"] for row in rows))
        self.assertTrue(all("--max-live-rows 2" in row["planned_command"] for row in rows))
        combined = PLAN_CSV_PATH.read_text(encoding="utf-8") + PLAN_MD_PATH.read_text(encoding="utf-8")
        self.assertIsNone(SECRET_LIKE_PATTERN.search(combined))

    def test_smoke_plan_does_not_claim_results(self) -> None:
        rows = read_csv_rows(PLAN_CSV_PATH)
        self.assertTrue(all(row["evidence_boundary"] == "bounded_smoke_plan_not_external_evaluation" for row in rows))
        self.assertTrue(all(row["status"] in {"not_run_missing_credentials", "ready_for_bounded_live_smoke"} for row in rows))
        text = PLAN_MD_PATH.read_text(encoding="utf-8")
        self.assertIn("does not report external model results", text)


if __name__ == "__main__":
    unittest.main()
