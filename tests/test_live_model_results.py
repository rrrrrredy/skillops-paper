from __future__ import annotations

import csv
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SUMMARY_CSV = REPO_ROOT / "results" / "experiments" / "live_model_summary.csv"
RAW_DIR = REPO_ROOT / "results" / "experiments" / "raw"


class LiveModelResultsTests(unittest.TestCase):
    def test_live_model_summary_contains_deepseek_and_kimi(self) -> None:
        self.assertTrue(SUMMARY_CSV.exists())
        with SUMMARY_CSV.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))

        providers = {row["provider"] for row in rows}
        models = {row["model"] for row in rows}
        experiments = {row["experiment"] for row in rows}

        self.assertIn("deepseek", providers)
        self.assertIn("kimi", providers)
        self.assertIn("deepseek-v4-flash", models)
        self.assertIn("kimi-k2.7-code", models)
        self.assertTrue(
            {
                "trigger_routing_accuracy",
                "constraint_compliance_rate",
                "security_guard_detection_rate",
                "memory_drift_detection",
            }.issubset(experiments)
        )

    def test_live_raw_outputs_are_sanitized(self) -> None:
        raw_files = sorted(path for path in RAW_DIR.glob("*.jsonl") if path.name != ".gitkeep")
        self.assertGreaterEqual(len(raw_files), 8)
        combined = "\n".join(path.read_text(encoding="utf-8") for path in raw_files)

        self.assertNotIn("reasoning_content", combined)
        self.assertNotIn('"role": "assistant"', combined)


if __name__ == "__main__":
    unittest.main()
