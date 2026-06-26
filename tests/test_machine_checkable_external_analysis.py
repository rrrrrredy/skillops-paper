from __future__ import annotations

import csv
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
METRICS_CSV_PATH = REPO_ROOT / "results" / "experiments" / "external_machine_checkable_metrics.csv"
METRICS_MD_PATH = REPO_ROOT / "results" / "experiments" / "external_machine_checkable_metrics.md"


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


class MachineCheckableExternalAnalysisTests(unittest.TestCase):
    def test_machine_checkable_outputs_exist(self) -> None:
        for path in (METRICS_CSV_PATH, METRICS_MD_PATH):
            self.assertTrue(path.exists(), f"Missing {path}")
            self.assertGreater(path.stat().st_size, 0, f"Empty {path}")

    def test_metrics_are_primary_machine_checkable(self) -> None:
        rows = read_csv_rows(METRICS_CSV_PATH)
        self.assertGreaterEqual(len(rows), 1)
        self.assertEqual({row["evidence_role"] for row in rows}, {"primary_machine_checkable"})
        self.assertIn("parse_success_rate", {row["metric"] for row in rows})
        self.assertIn("behavior_match_rate", {row["metric"] for row in rows})
        self.assertIn("constraint_pass_rate", {row["metric"] for row in rows})
        self.assertTrue(all(row["machine_rule"] for row in rows))

    def test_markdown_keeps_claim_boundary(self) -> None:
        text = METRICS_MD_PATH.read_text(encoding="utf-8")
        self.assertIn("primary external-smoke evidence route", text)
        self.assertIn("deterministic checks", text)
        self.assertIn("do not establish broad external effectiveness", text)


if __name__ == "__main__":
    unittest.main()
