from __future__ import annotations

import csv
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PRIMARY_EFFECTS_PATH = REPO_ROOT / "results" / "experiments" / "external_primary_effects.csv"
F1_BOOTSTRAP_PATH = REPO_ROOT / "results" / "experiments" / "external_f1_bootstrap.csv"
MCNEMAR_PATH = REPO_ROOT / "results" / "experiments" / "external_mcnemar.csv"
ANNOTATION_RELIABILITY_PATH = REPO_ROOT / "results" / "experiments" / "external_annotation_reliability.csv"
EXCLUSIONS_PATH = REPO_ROOT / "results" / "experiments" / "external_exclusions.csv"
SUMMARY_PATH = REPO_ROOT / "results" / "experiments" / "external_statistical_analysis.md"


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


class ExternalStatisticalAnalysisTests(unittest.TestCase):
    def test_statistical_analysis_files_exist(self) -> None:
        for path in (
            PRIMARY_EFFECTS_PATH,
            F1_BOOTSTRAP_PATH,
            MCNEMAR_PATH,
            ANNOTATION_RELIABILITY_PATH,
            EXCLUSIONS_PATH,
            SUMMARY_PATH,
        ):
            self.assertTrue(path.exists(), f"Missing {path}")
            self.assertGreater(path.stat().st_size, 0, f"Empty {path}")

    def test_primary_effects_are_descriptive(self) -> None:
        rows = read_csv_rows(PRIMARY_EFFECTS_PATH)
        self.assertGreaterEqual(len(rows), 1)
        self.assertTrue({row["analysis_status"] for row in rows} <= {"no_results", "insufficient_pairs", "descriptive_only"})
        self.assertIn("skillops_normalized_vs_original_freeform", {row["contrast"] for row in rows})

    def test_bootstrap_rows_keep_cluster_counts(self) -> None:
        rows = read_csv_rows(F1_BOOTSTRAP_PATH)
        self.assertGreaterEqual(len(rows), 1)
        self.assertIn("clusters", rows[0])
        self.assertIn("ci_low", rows[0])
        self.assertIn("ci_high", rows[0])
        self.assertTrue({row["analysis_status"] for row in rows} <= {"no_results", "descriptive_cluster_bootstrap"})

    def test_mcnemar_and_annotation_boundaries(self) -> None:
        mcnemar_rows = read_csv_rows(MCNEMAR_PATH)
        self.assertGreaterEqual(len(mcnemar_rows), 1)
        self.assertTrue(
            {row["analysis_status"] for row in mcnemar_rows}
            <= {"no_results", "insufficient_pairs", "no_discordant_pairs", "descriptive_mcnemar"}
        )

        annotation_rows = read_csv_rows(ANNOTATION_RELIABILITY_PATH)
        self.assertEqual(annotation_rows[0]["metric"], "annotation_reliability")
        self.assertEqual(annotation_rows[0]["analysis_status"], "not_used_primary_evidence")

        summary = SUMMARY_PATH.read_text(encoding="utf-8")
        self.assertIn("no statistical significance is claimed", summary)
        self.assertIn("Diagnostic p, not inferential", summary)


if __name__ == "__main__":
    unittest.main()
