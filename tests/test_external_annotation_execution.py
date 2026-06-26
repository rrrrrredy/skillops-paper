from __future__ import annotations

import csv
import unittest
from collections import Counter
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
ASSIGNMENT_PATH = REPO_ROOT / "results" / "tables" / "external_annotation_assignment_manifest.csv"
ADJUDICATION_PATH = REPO_ROOT / "results" / "tables" / "external_annotation_adjudication_log.csv"
EXECUTION_SUMMARY_PATH = REPO_ROOT / "results" / "tables" / "external_annotation_execution_summary.md"
RELIABILITY_PATH = REPO_ROOT / "results" / "tables" / "external_annotation_reliability.csv"
RELIABILITY_MD_PATH = REPO_ROOT / "results" / "tables" / "external_annotation_reliability.md"
WORKLIST_PATH = REPO_ROOT / "results" / "tables" / "external_pilot_annotation_worklist.csv"
CALIBRATION_PATH = REPO_ROOT / "results" / "tables" / "external_pilot_annotation_calibration.csv"
EXECUTION_PLAN_PATH = REPO_ROOT / "docs" / "external_annotation_execution_plan.md"
INTERFACE_SPEC_PATH = REPO_ROOT / "docs" / "external_annotation_interface_spec.md"
PREP_SCRIPT_PATH = REPO_ROOT / "scripts" / "prepare_external_annotation_execution.py"
RELIABILITY_SCRIPT_PATH = REPO_ROOT / "scripts" / "compute_external_annotation_reliability.py"


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


class ExternalAnnotationExecutionTests(unittest.TestCase):
    def test_execution_assets_exist(self) -> None:
        for path in (
            ASSIGNMENT_PATH,
            ADJUDICATION_PATH,
            EXECUTION_SUMMARY_PATH,
            RELIABILITY_PATH,
            RELIABILITY_MD_PATH,
            EXECUTION_PLAN_PATH,
            INTERFACE_SPEC_PATH,
            PREP_SCRIPT_PATH,
            RELIABILITY_SCRIPT_PATH,
        ):
            self.assertTrue(path.exists(), f"Missing {path}")
            self.assertGreater(path.stat().st_size, 0, f"Empty {path}")

    def test_assignment_manifest_has_two_blinded_reviewers_per_case(self) -> None:
        worklist_rows = read_csv_rows(WORKLIST_PATH)
        calibration_case_ids = {row["case_id"] for row in read_csv_rows(CALIBRATION_PATH)}
        assignment_rows = read_csv_rows(ASSIGNMENT_PATH)
        self.assertEqual(len(assignment_rows), len(worklist_rows) * 2)

        by_case = Counter(row["case_id"] for row in assignment_rows)
        self.assertTrue(all(count == 2 for count in by_case.values()))
        self.assertEqual(set(by_case), {row["case_id"] for row in worklist_rows})
        self.assertEqual({row["reviewer_id"] for row in assignment_rows}, {"rater_001", "rater_002"})
        self.assertEqual({row["peer_response_visibility"] for row in assignment_rows}, {"hidden_until_independent_review_complete"})
        self.assertEqual(
            {row["review_phase"] for row in assignment_rows if row["case_id"] in calibration_case_ids},
            {"calibration"},
        )

    def test_adjudication_log_is_not_claiming_labels(self) -> None:
        rows = read_csv_rows(ADJUDICATION_PATH)
        self.assertEqual(len(rows), 96)
        self.assertEqual({row["adjudication_status"] for row in rows}, {"not_ready_pending_independent_labels"})
        self.assertTrue(all(row["adjudicator_id"] == "" for row in rows))
        self.assertTrue(all(row["adjudicated_expected_behavior"] == "" for row in rows))
        self.assertTrue(all(row["adjudicated_risk_label"] == "" for row in rows))

    def test_reliability_is_unavailable_without_human_labels(self) -> None:
        rows = read_csv_rows(RELIABILITY_PATH)
        self.assertEqual(len(rows), 4)
        self.assertEqual({row["analysis_status"] for row in rows}, {"not_available"})
        self.assertEqual({row["records_available"] for row in rows}, {"0"})
        text = RELIABILITY_MD_PATH.read_text(encoding="utf-8")
        self.assertIn("no human labels have been collected", text)

    def test_docs_preserve_external_human_boundary(self) -> None:
        text = (EXECUTION_PLAN_PATH.read_text(encoding="utf-8") + "\n" + INTERFACE_SPEC_PATH.read_text(encoding="utf-8")).lower()
        self.assertIn("cannot truthfully serve as an external human annotator", text)
        self.assertIn("consent records", text)
        self.assertIn("payment details", text)
        self.assertIn("peer responses", text)


if __name__ == "__main__":
    unittest.main()
