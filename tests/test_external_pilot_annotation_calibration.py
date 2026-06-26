from __future__ import annotations

import csv
import unittest
from collections import Counter
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
GENERATOR_PATH = REPO_ROOT / "scripts" / "generate_external_pilot_annotation_calibration.py"
WORKLIST_PATH = REPO_ROOT / "results" / "tables" / "external_pilot_annotation_worklist.csv"
CALIBRATION_PATH = REPO_ROOT / "results" / "tables" / "external_pilot_annotation_calibration.csv"
SUMMARY_PATH = REPO_ROOT / "results" / "tables" / "external_pilot_annotation_calibration.md"

EXPECTED_FAMILIES = {
    "agent_skills",
    "agent_workflow_templates",
    "mcp_and_tool_recipes",
    "prompt_and_function_recipes",
}

EXPECTED_CASE_TYPES = {
    "positive_trigger",
    "negative_trigger",
    "boundary_clarification",
    "risk_constraint",
}


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


class ExternalPilotAnnotationCalibrationTests(unittest.TestCase):
    def test_pilot_annotation_files_exist(self) -> None:
        for path in (GENERATOR_PATH, WORKLIST_PATH, CALIBRATION_PATH, SUMMARY_PATH):
            self.assertTrue(path.exists(), f"Missing {path}")
            self.assertGreater(path.stat().st_size, 0, f"Empty {path}")

    def test_worklist_covers_all_pilot_base_cases(self) -> None:
        rows = read_csv_rows(WORKLIST_PATH)
        self.assertEqual(len(rows), 96)
        self.assertEqual(len({row["case_id"] for row in rows}), 96)
        self.assertEqual(len({row["artifact_id"] for row in rows}), 24)
        self.assertEqual(set(Counter(row["study_family"] for row in rows)), EXPECTED_FAMILIES)
        self.assertTrue(all(count == 24 for count in Counter(row["study_family"] for row in rows).values()))
        self.assertEqual({row["case_type"] for row in rows}, EXPECTED_CASE_TYPES)

    def test_calibration_subset_is_balanced(self) -> None:
        rows = read_csv_rows(CALIBRATION_PATH)
        self.assertEqual(len(rows), 32)
        self.assertEqual(len({row["artifact_id"] for row in rows}), 8)
        self.assertTrue(all(count == 8 for count in Counter(row["study_family"] for row in rows).values()))
        self.assertTrue(all(count == 8 for count in Counter(row["case_type"] for row in rows).values()))
        self.assertEqual({row["review_status"] for row in rows}, {"pending_review"})
        self.assertEqual({row["evidence_boundary"] for row in rows}, {"pilot_label_sensitivity_plan_not_model_outcomes"})

    def test_annotation_fields_are_empty_before_review(self) -> None:
        for row in read_csv_rows(CALIBRATION_PATH):
            self.assertEqual(row["annotator_a_id"], "")
            self.assertEqual(row["annotator_b_id"], "")
            self.assertEqual(row["adjudicated_expected_behavior"], "")
            self.assertEqual(row["adjudicated_risk_label"], "")

    def test_summary_states_no_model_outcomes(self) -> None:
        text = SUMMARY_PATH.read_text(encoding="utf-8")
        self.assertIn("does not report model outcomes", text)
        self.assertIn("Pilot worklist cases | 96", text)
        self.assertIn("Calibration cases | 32", text)


if __name__ == "__main__":
    unittest.main()
