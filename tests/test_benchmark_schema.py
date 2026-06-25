from __future__ import annotations

import unittest
from collections import Counter

from tests.helpers import (
    ALLOWED_RISK_TYPES,
    ALLOWED_TRIGGER_LABELS,
    EXPECTED_RISK_TYPE_COUNTS,
    EXPECTED_TRIGGER_LABEL_COUNTS,
    RISK_CASES_PATH,
    RISK_CASE_COLUMNS,
    SKILL_SAMPLE_COLUMNS,
    SKILL_SAMPLES_PATH,
    TRIGGER_CASES_PATH,
    TRIGGER_CASE_COLUMNS,
    read_csv_fieldnames,
    read_csv_rows,
)


class BenchmarkSchemaTests(unittest.TestCase):
    def test_required_benchmark_files_exist(self) -> None:
        for path in (SKILL_SAMPLES_PATH, TRIGGER_CASES_PATH, RISK_CASES_PATH):
            self.assertTrue(path.exists(), f"Missing benchmark file: {path}")

    def test_skill_sample_columns_and_count(self) -> None:
        fieldnames = read_csv_fieldnames(SKILL_SAMPLES_PATH)
        self.assertEqual(fieldnames, SKILL_SAMPLE_COLUMNS)
        rows = read_csv_rows(SKILL_SAMPLES_PATH)
        self.assertEqual(len(rows), 5)

    def test_trigger_case_schema_and_counts(self) -> None:
        fieldnames = read_csv_fieldnames(TRIGGER_CASES_PATH)
        self.assertEqual(fieldnames, TRIGGER_CASE_COLUMNS)
        rows = read_csv_rows(TRIGGER_CASES_PATH)

        case_ids = [row["case_id"].strip() for row in rows]
        self.assertTrue(all(case_ids), "Empty trigger case_id found")
        self.assertEqual(len(case_ids), len(set(case_ids)), "Duplicate trigger case_id found")

        labels = [row["expected_label"] for row in rows]
        self.assertEqual(set(labels), ALLOWED_TRIGGER_LABELS)
        self.assertEqual(len(rows), 36)
        self.assertEqual(dict(Counter(labels)), EXPECTED_TRIGGER_LABEL_COUNTS)

    def test_risk_case_schema_and_counts(self) -> None:
        fieldnames = read_csv_fieldnames(RISK_CASES_PATH)
        self.assertEqual(fieldnames, RISK_CASE_COLUMNS)
        rows = read_csv_rows(RISK_CASES_PATH)

        case_ids = [row["case_id"].strip() for row in rows]
        self.assertTrue(all(case_ids), "Empty risk case_id found")
        self.assertEqual(len(case_ids), len(set(case_ids)), "Duplicate risk case_id found")

        risk_types = [row["risk_type"] for row in rows]
        self.assertEqual(set(risk_types), ALLOWED_RISK_TYPES)
        self.assertEqual(len(rows), 24)
        self.assertEqual(dict(Counter(risk_types)), EXPECTED_RISK_TYPE_COUNTS)


if __name__ == "__main__":
    unittest.main()
