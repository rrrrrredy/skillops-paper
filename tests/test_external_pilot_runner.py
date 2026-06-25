from __future__ import annotations

import csv
import unittest
from collections import Counter
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = REPO_ROOT / "scripts" / "run_external_pilot_experiment.py"
UTILS_PATH = REPO_ROOT / "scripts" / "external_pilot_runner_utils.py"
RUN_PLAN_PATH = REPO_ROOT / "results" / "experiments" / "external_pilot_run_plan.csv"
RUN_PLAN_MD_PATH = REPO_ROOT / "results" / "experiments" / "external_pilot_run_plan.md"
READINESS_PATH = REPO_ROOT / "results" / "experiments" / "external_pilot_provider_readiness.csv"
READINESS_MD_PATH = REPO_ROOT / "results" / "experiments" / "external_pilot_provider_readiness.md"

EXPECTED_MODELS = {
    ("deepseek", "deepseek-v4-flash"),
    ("kimi", "kimi-k2.7-code"),
}

EXPECTED_CONDITIONS = {
    "original_freeform",
    "skillops_normalized",
    "skillops_ablation",
}


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


class ExternalPilotRunnerTests(unittest.TestCase):
    def test_pilot_runner_files_exist(self) -> None:
        for path in (RUNNER_PATH, UTILS_PATH, RUN_PLAN_PATH, RUN_PLAN_MD_PATH, READINESS_PATH, READINESS_MD_PATH):
            self.assertTrue(path.exists(), f"Missing {path}")
            self.assertGreater(path.stat().st_size, 0, f"Empty {path}")

    def test_pilot_run_plan_is_bounded_and_not_outcome_evidence(self) -> None:
        rows = read_csv_rows(RUN_PLAN_PATH)
        self.assertEqual(len(rows), 576)
        self.assertEqual({(row["provider"], row["model"]) for row in rows}, EXPECTED_MODELS)
        self.assertEqual(Counter((row["provider"], row["model"]) for row in rows), Counter({model: 288 for model in EXPECTED_MODELS}))
        self.assertEqual({row["condition"] for row in rows}, EXPECTED_CONDITIONS)
        self.assertTrue({row["run_status"] for row in rows} <= {"not_run", "completed"})
        self.assertEqual({row["evidence_boundary"] for row in rows}, {"pilot_logistics_not_external_effect_estimate"})
        self.assertTrue(all(row["content_boundary"] == "metadata_only_no_third_party_prose_or_code_copied" for row in rows))

    def test_provider_readiness_has_no_secret_values(self) -> None:
        rows = read_csv_rows(READINESS_PATH)
        self.assertEqual(len(rows), 2)
        self.assertEqual({(row["provider"], row["model"]) for row in rows}, EXPECTED_MODELS)
        for row in rows:
            self.assertIn(row["credential_env"], {"DEEPSEEK_API_KEY", "MOONSHOT_API_KEY"})
            self.assertIn(row["credential_available"], {"true", "false"})
            self.assertEqual(int(row["planned_rows"]), 288)
            self.assertEqual(int(row["planned_rows"]), int(row["completed_rows"]) + int(row["pending_rows"]))
            self.assertIn("--sample-limit 4 --max-live-rows 4", row["bounded_command"])
            self.assertEqual(row["evidence_boundary"], "pilot_logistics_not_external_effect_estimate")

    def test_runner_requires_live_bounds(self) -> None:
        text = RUNNER_PATH.read_text(encoding="utf-8")
        self.assertIn("Live pilot execution requires --sample-limit", text)
        self.assertIn("Refusing to run", text)
        self.assertIn("not_run_missing_credentials", text)

    def test_summary_states_no_effect_estimate(self) -> None:
        self.assertIn("does not report external effect estimates", RUN_PLAN_MD_PATH.read_text(encoding="utf-8"))
        self.assertIn("does not report external effect estimates", READINESS_MD_PATH.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
