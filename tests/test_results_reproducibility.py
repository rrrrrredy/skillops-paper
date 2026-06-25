from __future__ import annotations

import unittest
from collections import Counter

from tests.helpers import (
    ARTIFACT_COVERAGE_CSV,
    EXPECTED_RISK_TYPE_COUNTS,
    EXPECTED_TRIGGER_LABEL_COUNTS,
    REQUIRED_OUTPUTS,
    RISK_CASES_PATH,
    RISK_SUMMARY_CSV,
    SKILL_SAMPLES_PATH,
    TRIGGER_CASES_PATH,
    TRIGGER_SUMMARY_CSV,
    expected_artifact_coverage_counts,
    file_is_non_empty,
    load_artifact_coverage_counts,
    load_group_counts,
    read_csv_rows,
    run_pipeline,
)


class ResultsReproducibilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.pipeline_result = run_pipeline()

    def test_run_all_succeeds(self) -> None:
        if self.pipeline_result.returncode != 0:
            self.fail(
                "scripts/run_all.py failed.\n"
                f"stdout:\n{self.pipeline_result.stdout}\n"
                f"stderr:\n{self.pipeline_result.stderr}"
            )

    def test_expected_outputs_exist_and_are_non_empty(self) -> None:
        for path in REQUIRED_OUTPUTS:
            self.assertTrue(path.exists(), f"Expected output missing: {path}")
            self.assertTrue(file_is_non_empty(path), f"Expected non-empty output: {path}")

    def test_trigger_summary_matches_benchmark_inputs(self) -> None:
        trigger_rows = read_csv_rows(TRIGGER_CASES_PATH)
        expected_counts = dict(Counter(row["expected_label"] for row in trigger_rows))
        self.assertEqual(expected_counts, EXPECTED_TRIGGER_LABEL_COUNTS)
        self.assertEqual(load_group_counts(TRIGGER_SUMMARY_CSV, "expected_label"), expected_counts)

    def test_risk_summary_matches_benchmark_inputs(self) -> None:
        risk_rows = read_csv_rows(RISK_CASES_PATH)
        expected_counts = dict(Counter(row["risk_type"] for row in risk_rows))
        self.assertEqual(expected_counts, EXPECTED_RISK_TYPE_COUNTS)
        self.assertEqual(load_group_counts(RISK_SUMMARY_CSV, "risk_type"), expected_counts)

    def test_artifact_coverage_matches_benchmark_inputs(self) -> None:
        skill_rows = read_csv_rows(SKILL_SAMPLES_PATH)
        expected_counts = expected_artifact_coverage_counts(skill_rows)
        self.assertEqual(load_artifact_coverage_counts(ARTIFACT_COVERAGE_CSV), expected_counts)


if __name__ == "__main__":
    unittest.main()
