from __future__ import annotations

import csv
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_SELECTION_PATH = REPO_ROOT / "results" / "tables" / "external_artifact_selection.csv"
CASE_CONSTRUCTION_PATH = REPO_ROOT / "results" / "tables" / "external_case_construction.csv"
ANNOTATION_PACKET_PATH = REPO_ROOT / "results" / "tables" / "external_annotation_packet.csv"
CONDITION_PACKET_PATH = REPO_ROOT / "results" / "tables" / "external_condition_packet.csv"
SUMMARY_PATH = REPO_ROOT / "results" / "tables" / "external_annotation_packet.md"

EXPECTED_CASE_TYPES = {
    "positive_trigger",
    "negative_trigger",
    "boundary_clarification",
    "risk_constraint",
}

EXPECTED_CONDITIONS = {
    "original_freeform",
    "skillops_normalized",
    "skillops_ablation",
}

EXPECTED_BEHAVIORS = {
    "trigger",
    "no_trigger",
    "clarify_scope",
    "apply_constraint_or_refuse",
}


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


class ExternalAnnotationPacketTests(unittest.TestCase):
    def test_annotation_packet_files_exist(self) -> None:
        for path in (CASE_CONSTRUCTION_PATH, ANNOTATION_PACKET_PATH, CONDITION_PACKET_PATH, SUMMARY_PATH):
            self.assertTrue(path.exists(), f"Missing {path}")
            self.assertGreater(path.stat().st_size, 0, f"Empty {path}")

    def test_case_construction_has_four_cases_per_artifact(self) -> None:
        artifact_rows = read_csv_rows(ARTIFACT_SELECTION_PATH)
        case_rows = read_csv_rows(CASE_CONSTRUCTION_PATH)
        self.assertEqual(len(artifact_rows), 240)
        self.assertEqual(len(case_rows), 960)
        self.assertEqual(len(case_rows), len({row["case_id"] for row in case_rows}))

        by_artifact: dict[str, set[str]] = {}
        for row in case_rows:
            by_artifact.setdefault(row["artifact_id"], set()).add(row["case_type"])
            self.assertIn(row["case_type"], EXPECTED_CASE_TYPES)
            self.assertIn(row["expected_behavior"], EXPECTED_BEHAVIORS)
            self.assertEqual(row["label_source"], "protocol_seed")
            self.assertTrue(row["user_request"])

        self.assertEqual(set(by_artifact), {row["artifact_id"] for row in artifact_rows})
        self.assertTrue(all(case_types == EXPECTED_CASE_TYPES for case_types in by_artifact.values()))

    def test_annotation_packet_is_pending_review_only(self) -> None:
        rows = read_csv_rows(ANNOTATION_PACKET_PATH)
        self.assertEqual(len(rows), 960)
        self.assertTrue(all(row["review_status"] == "pending_review" for row in rows))
        self.assertTrue(all(row["adjudicated_expected_behavior"] == "" for row in rows))
        self.assertTrue(all(row["adjudicated_risk_label"] == "" for row in rows))

    def test_condition_packet_crosses_three_conditions(self) -> None:
        case_rows = read_csv_rows(CASE_CONSTRUCTION_PATH)
        condition_rows = read_csv_rows(CONDITION_PACKET_PATH)
        self.assertEqual(len(condition_rows), 2880)
        self.assertEqual(len(condition_rows), len({row["condition_case_id"] for row in condition_rows}))

        conditions_by_case: dict[str, set[str]] = {}
        for row in condition_rows:
            conditions_by_case.setdefault(row["case_id"], set()).add(row["condition"])
            self.assertEqual(row["representation_status"], "pending_construction")
            self.assertEqual(row["execution_status"], "not_run")

        self.assertEqual(set(conditions_by_case), {row["case_id"] for row in case_rows})
        self.assertTrue(all(conditions == EXPECTED_CONDITIONS for conditions in conditions_by_case.values()))

    def test_summary_states_no_collected_outcomes(self) -> None:
        text = SUMMARY_PATH.read_text(encoding="utf-8")
        self.assertIn("does not report collected annotations or behavioral outcomes", text)
        self.assertIn("Base cases | 960", text)
        self.assertIn("Condition rows | 2880", text)


if __name__ == "__main__":
    unittest.main()
