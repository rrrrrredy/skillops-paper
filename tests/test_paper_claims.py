from __future__ import annotations

import unittest

from tests.helpers import (
    ARTIFACT_COVERAGE_CSV,
    COMPONENT_PAPER_LABELS,
    PAPER_PATH,
    RISK_CASES_PATH,
    RISK_SUMMARY_CSV,
    TRIGGER_CASES_PATH,
    TRIGGER_SUMMARY_CSV,
    latex_texttt,
    load_artifact_coverage_counts,
    load_group_counts,
    normalize_text,
    read_csv_rows,
    read_text,
    unsupported_claim_hits,
)


class PaperClaimsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.paper_text = read_text(PAPER_PATH)
        cls.paper_text_normalized = normalize_text(cls.paper_text)

    def test_benchmark_totals_match_results_tables(self) -> None:
        trigger_rows = read_csv_rows(TRIGGER_CASES_PATH)
        risk_rows = read_csv_rows(RISK_CASES_PATH)

        self.assertEqual(len(trigger_rows), 36)
        self.assertEqual(len(risk_rows), 24)
        self.assertIn("profiles five artifacts", self.paper_text_normalized)
        self.assertIn("contains 36 trigger cases", self.paper_text_normalized)
        self.assertIn("contains 24 operational-risk cases", self.paper_text_normalized)

        self.assertEqual(load_group_counts(TRIGGER_SUMMARY_CSV, "expected_label"), {
            "should_trigger": 15,
            "should_not_trigger": 12,
            "ambiguous": 9,
        })
        self.assertEqual(load_group_counts(RISK_SUMMARY_CSV, "risk_type"), {
            "prompt_injection": 3,
            "over_broad_trigger": 3,
            "unsafe_file_access": 3,
            "missing_constraints": 3,
            "stale_memory": 3,
            "missing_tests": 3,
            "identity_confusion": 3,
            "privacy_leakage": 3,
        })

    def test_paper_trigger_table_matches_results(self) -> None:
        for label, count in load_group_counts(TRIGGER_SUMMARY_CSV, "expected_label").items():
            snippet = normalize_text(
                f"Expected label & \\texttt{{{latex_texttt(label)}}} & {count}"
            )
            self.assertIn(snippet, self.paper_text_normalized)

    def test_paper_risk_table_matches_results(self) -> None:
        for risk_type, count in load_group_counts(RISK_SUMMARY_CSV, "risk_type").items():
            snippet = normalize_text(
                f"Risk type & \\texttt{{{latex_texttt(risk_type)}}} & {count}"
            )
            self.assertIn(snippet, self.paper_text_normalized)

    def test_paper_artifact_coverage_table_matches_results(self) -> None:
        coverage_counts = load_artifact_coverage_counts(ARTIFACT_COVERAGE_CSV)
        for component, counts in coverage_counts.items():
            label = COMPONENT_PAPER_LABELS[component]
            snippet = normalize_text(
                f"{label} & {counts['documented_count']} & "
                f"{counts['limited_count']} & {counts['absent_count']}"
            )
            self.assertIn(snippet, self.paper_text_normalized)

    def test_unsupported_claim_terms_are_only_used_in_limiting_contexts(self) -> None:
        hits = unsupported_claim_hits(self.paper_text)
        self.assertEqual([], hits, f"Unsupported claim contexts found: {hits}")


if __name__ == "__main__":
    unittest.main()
