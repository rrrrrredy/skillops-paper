from __future__ import annotations

import csv
import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_FRAME_PATH = REPO_ROOT / "benchmark" / "external_artifact_corpus_sources.csv"
PROTOCOL_PATH = REPO_ROOT / "experiments" / "external_validation_protocol.md"
SCHEMA_PATH = REPO_ROOT / "experiments" / "schemas" / "external_case_schema.json"
SEED_PATH = REPO_ROOT / "experiments" / "external_case_seed.csv"
ALLOCATION_PATH = REPO_ROOT / "results" / "tables" / "external_case_allocation.csv"
CASE_PLAN_PATH = REPO_ROOT / "results" / "tables" / "external_case_plan.csv"
CONDITION_PLAN_PATH = REPO_ROOT / "results" / "tables" / "external_condition_plan.csv"
CASE_PLAN_MD_PATH = REPO_ROOT / "results" / "tables" / "external_case_plan.md"
ANNOTATION_GUIDE_PATH = REPO_ROOT / "docs" / "annotation_guide.md"
PREREG_TEMPLATE_PATH = REPO_ROOT / "docs" / "preregistration_template.md"

EXPECTED_SEED_COLUMNS = [
    "case_id",
    "source_id",
    "source_version",
    "artifact_reference",
    "artifact_family_group",
    "case_type",
    "user_request",
    "expected_behavior",
    "risk_label",
    "label_source",
    "notes",
]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


class ExternalCaseScaffoldTests(unittest.TestCase):
    def test_external_case_schema_and_seed_are_structured(self) -> None:
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        self.assertEqual(schema["title"], "External Corpus Base Case Record")
        self.assertFalse(schema.get("additionalProperties", True))

        source_ids = {row["source_id"] for row in read_csv_rows(SOURCE_FRAME_PATH)}
        with SEED_PATH.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            self.assertEqual(reader.fieldnames, EXPECTED_SEED_COLUMNS)
            rows = list(reader)

        self.assertGreaterEqual(len(rows), 8)
        self.assertEqual(len(rows), len({row["case_id"] for row in rows}))
        for row in rows:
            self.assertIn(row["source_id"], source_ids)
            self.assertTrue(row["case_id"].startswith("ext-"))
            self.assertIn(row["case_type"], schema["properties"]["case_type"]["enum"])
            self.assertIn(row["expected_behavior"], schema["properties"]["expected_behavior"]["enum"])
            self.assertIn(row["risk_label"], schema["properties"]["risk_label"]["enum"])

    def test_external_case_plan_totals_are_reproducible(self) -> None:
        for path in (ALLOCATION_PATH, CASE_PLAN_PATH, CONDITION_PLAN_PATH, CASE_PLAN_MD_PATH):
            self.assertTrue(path.exists(), f"Missing {path}")
            self.assertGreater(path.stat().st_size, 0, f"Empty {path}")

        allocation_rows = read_csv_rows(ALLOCATION_PATH)
        case_plan_rows = read_csv_rows(CASE_PLAN_PATH)
        condition_rows = read_csv_rows(CONDITION_PLAN_PATH)

        self.assertEqual(sum(int(row["target_artifacts"]) for row in allocation_rows), 240)
        self.assertEqual(sum(int(row["target_base_cases"]) for row in allocation_rows), 960)
        self.assertEqual(sum(int(row["target_base_cases"]) for row in case_plan_rows), 960)
        self.assertEqual(sum(int(row["target_condition_evaluations"]) for row in allocation_rows), 2880)
        self.assertEqual(sum(int(row["target_evaluations"]) for row in condition_rows), 2880)

        roles = {row["sampling_role"] for row in allocation_rows}
        self.assertIn("metadata_reference", roles)
        self.assertIn("sampling_candidate", roles)

    def test_protocol_and_guides_reference_scaffold(self) -> None:
        protocol = PROTOCOL_PATH.read_text(encoding="utf-8")
        guide = ANNOTATION_GUIDE_PATH.read_text(encoding="utf-8")
        prereg = PREREG_TEMPLATE_PATH.read_text(encoding="utf-8")

        for expected in (
            "experiments/schemas/external_case_schema.json",
            "experiments/external_case_seed.csv",
            "results/tables/external_case_plan.csv",
            "docs/annotation_guide.md",
            "docs/preregistration_template.md",
        ):
            self.assertIn(expected, protocol)

        self.assertIn("Two annotators independently label", guide)
        self.assertIn("Total base cases: 960", prereg)
        self.assertIn("Static source indicators, allocation files, seed cases, and schemas", prereg)


if __name__ == "__main__":
    unittest.main()
