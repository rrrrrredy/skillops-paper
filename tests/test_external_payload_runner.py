from __future__ import annotations

import csv
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = REPO_ROOT / "scripts" / "run_external_payload_experiment.py"
RUN_PLAN_CSV_PATH = REPO_ROOT / "results" / "experiments" / "external_payload_run_plan.csv"
RUN_PLAN_MD_PATH = REPO_ROOT / "results" / "experiments" / "external_payload_run_plan.md"


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


class ExternalPayloadRunnerTests(unittest.TestCase):
    def test_external_payload_runner_files_exist(self) -> None:
        for path in (RUNNER_PATH, RUN_PLAN_CSV_PATH, RUN_PLAN_MD_PATH):
            self.assertTrue(path.exists(), f"Missing {path}")
            self.assertGreater(path.stat().st_size, 0, f"Empty {path}")

    def test_external_payload_run_plan_is_not_run(self) -> None:
        rows = read_csv_rows(RUN_PLAN_CSV_PATH)
        self.assertEqual(len(rows), 2880)
        self.assertEqual(len(rows), len({row["condition_case_id"] for row in rows}))
        self.assertTrue(all(row["run_status"] == "not_run" for row in rows))
        self.assertTrue(all(row["content_boundary"] == "metadata_only_no_third_party_prose_or_code_copied" for row in rows))

    def test_external_payload_run_plan_keeps_shard_balance(self) -> None:
        rows = read_csv_rows(RUN_PLAN_CSV_PATH)
        shard_counts: dict[str, int] = {}
        for row in rows:
            shard_counts[row["shard_id"]] = shard_counts.get(row["shard_id"], 0) + 1
        self.assertEqual(len(shard_counts), 12)
        self.assertTrue(all(count == 240 for count in shard_counts.values()))

    def test_run_plan_summary_states_no_results(self) -> None:
        text = RUN_PLAN_MD_PATH.read_text(encoding="utf-8")
        self.assertIn("does not report external model results", text)
        self.assertIn("Selected payload rows | 2880", text)


if __name__ == "__main__":
    unittest.main()
