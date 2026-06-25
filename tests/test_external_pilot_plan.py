from __future__ import annotations

import csv
import unittest
from collections import Counter
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PILOT_ARTIFACTS_PATH = REPO_ROOT / "results" / "experiments" / "external_pilot_artifacts.csv"
PILOT_CONDITION_PLAN_PATH = REPO_ROOT / "results" / "experiments" / "external_pilot_condition_plan.csv"
PILOT_MODEL_PLAN_PATH = REPO_ROOT / "results" / "experiments" / "external_pilot_model_plan.csv"
PILOT_SUMMARY_PATH = REPO_ROOT / "results" / "experiments" / "external_pilot_plan.md"

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

EXPECTED_CONDITIONS = {
    "original_freeform",
    "skillops_normalized",
    "skillops_ablation",
}

EXPECTED_MODELS = {
    ("deepseek", "deepseek-v4-flash"),
    ("kimi", "kimi-k2.7-code"),
}


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


class ExternalPilotPlanTests(unittest.TestCase):
    def test_pilot_plan_files_exist(self) -> None:
        for path in (PILOT_ARTIFACTS_PATH, PILOT_CONDITION_PLAN_PATH, PILOT_MODEL_PLAN_PATH, PILOT_SUMMARY_PATH):
            self.assertTrue(path.exists(), f"Missing {path}")
            self.assertGreater(path.stat().st_size, 0, f"Empty {path}")

    def test_pilot_artifacts_are_seeded_and_family_balanced(self) -> None:
        rows = read_csv_rows(PILOT_ARTIFACTS_PATH)
        self.assertEqual(len(rows), 24)
        self.assertEqual(len({row["artifact_id"] for row in rows}), 24)
        self.assertEqual({row["random_seed"] for row in rows}, {"20260625"})
        self.assertEqual({row["pilot_status"] for row in rows}, {"selected_pending_annotation"})
        self.assertEqual(set(Counter(row["study_family"] for row in rows)), EXPECTED_FAMILIES)
        self.assertTrue(all(count == 6 for count in Counter(row["study_family"] for row in rows).values()))
        self.assertGreaterEqual(len({row["source_owner"] for row in rows}), 8)
        self.assertGreaterEqual(len({row["source_id"] for row in rows}), 6)

    def test_condition_plan_maps_four_cases_and_three_conditions_per_artifact(self) -> None:
        artifact_rows = read_csv_rows(PILOT_ARTIFACTS_PATH)
        rows = read_csv_rows(PILOT_CONDITION_PLAN_PATH)
        self.assertEqual(len(rows), 288)
        self.assertEqual(len({row["condition_case_id"] for row in rows}), 288)
        self.assertEqual(len({row["case_id"] for row in rows}), 96)
        self.assertEqual({row["artifact_id"] for row in rows}, {row["artifact_id"] for row in artifact_rows})
        self.assertEqual({row["condition"] for row in rows}, EXPECTED_CONDITIONS)
        self.assertEqual({row["case_type"] for row in rows}, EXPECTED_CASE_TYPES)

        cases_by_artifact: dict[str, set[str]] = {}
        conditions_by_case: dict[str, set[str]] = {}
        for row in rows:
            cases_by_artifact.setdefault(row["artifact_id"], set()).add(row["case_id"])
            conditions_by_case.setdefault(row["case_id"], set()).add(row["condition"])
            self.assertTrue(row["study_family"])
            self.assertTrue(row["source_owner"])
            self.assertTrue(row["ecosystem"])
            self.assertEqual(row["pilot_status"], "selected_pending_annotation")

        self.assertTrue(all(len(case_ids) == 4 for case_ids in cases_by_artifact.values()))
        self.assertTrue(all(conditions == EXPECTED_CONDITIONS for conditions in conditions_by_case.values()))

    def test_model_plan_crosses_each_condition_with_each_provider_model(self) -> None:
        rows = read_csv_rows(PILOT_MODEL_PLAN_PATH)
        self.assertEqual(len(rows), 576)
        self.assertEqual({(row["provider"], row["model"]) for row in rows}, EXPECTED_MODELS)
        self.assertEqual(Counter((row["provider"], row["model"]) for row in rows), Counter({model: 288 for model in EXPECTED_MODELS}))
        self.assertEqual({row["evidence_boundary"] for row in rows}, {"pilot_plan_not_external_effect_estimate"})
        self.assertEqual({row["condition"] for row in rows}, EXPECTED_CONDITIONS)

    def test_summary_states_pilot_boundary(self) -> None:
        text = PILOT_SUMMARY_PATH.read_text(encoding="utf-8")
        self.assertIn("not a final external effect estimate", text)
        self.assertIn("Pilot artifacts | 24", text)
        self.assertIn("Pilot provider-condition rows | 576", text)


if __name__ == "__main__":
    unittest.main()
