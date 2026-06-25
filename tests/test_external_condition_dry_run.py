from __future__ import annotations

import csv
import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = REPO_ROOT / "experiments" / "schemas" / "external_condition_result_schema.json"
MANIFEST_PATH = REPO_ROOT / "results" / "experiments" / "external_condition_manifest.csv"
SHARD_SUMMARY_PATH = REPO_ROOT / "results" / "experiments" / "external_condition_shards.csv"
STAT_PLAN_CSV_PATH = REPO_ROOT / "results" / "experiments" / "external_statistical_analysis_plan.csv"
STAT_PLAN_MD_PATH = REPO_ROOT / "results" / "experiments" / "external_statistical_analysis_plan.md"
SUMMARY_MD_PATH = REPO_ROOT / "results" / "experiments" / "external_condition_dry_run.md"

EXPECTED_CONDITIONS = {
    "original_freeform",
    "skillops_normalized",
    "skillops_ablation",
}


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


class ExternalConditionDryRunTests(unittest.TestCase):
    def test_external_condition_dry_run_files_exist(self) -> None:
        for path in (SCHEMA_PATH, MANIFEST_PATH, SHARD_SUMMARY_PATH, STAT_PLAN_CSV_PATH, STAT_PLAN_MD_PATH, SUMMARY_MD_PATH):
            self.assertTrue(path.exists(), f"Missing {path}")
            self.assertGreater(path.stat().st_size, 0, f"Empty {path}")

    def test_external_result_schema_is_strict(self) -> None:
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        self.assertEqual(schema["title"], "External Condition Evaluation Result")
        self.assertFalse(schema.get("additionalProperties", True))
        self.assertIn("predicted_behavior", schema["required"])
        for field in ("payload_id", "run_id", "batch_id", "prompt_hash", "representation_hash", "retry_count"):
            self.assertIn(field, schema["properties"])

    def test_external_manifest_shards_pending_rows(self) -> None:
        rows = read_csv_rows(MANIFEST_PATH)
        self.assertEqual(len(rows), 2880)
        self.assertEqual(len(rows), len({row["condition_case_id"] for row in rows}))
        self.assertTrue(all(row["run_status"] == "not_run" for row in rows))
        self.assertTrue(all(row["execution_status"] == "not_run" for row in rows))
        self.assertTrue(all(row["representation_status"] == "pending_construction" for row in rows))
        self.assertEqual({row["condition"] for row in rows}, EXPECTED_CONDITIONS)

        shard_rows = read_csv_rows(SHARD_SUMMARY_PATH)
        self.assertEqual(len(shard_rows), 12)
        self.assertEqual(sum(int(row["row_count"]) for row in shard_rows), 2880)
        self.assertTrue(all(int(row["row_count"]) == 240 for row in shard_rows))

    def test_external_statistical_plan_has_no_outcome_claims(self) -> None:
        rows = read_csv_rows(STAT_PLAN_CSV_PATH)
        self.assertGreaterEqual(len(rows), 6)
        self.assertTrue(all(row["status"] == "planned_no_outcomes_yet" for row in rows))
        metrics = {row["metric"] for row in rows}
        self.assertIn("routing_correct", metrics)
        self.assertIn("constraint_compliance", metrics)
        self.assertIn("parse_success", metrics)

        summary = SUMMARY_MD_PATH.read_text(encoding="utf-8")
        self.assertIn("does not report model execution or statistical outcomes", summary)


if __name__ == "__main__":
    unittest.main()
