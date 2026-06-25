from __future__ import annotations

import csv
import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SELECTION_PATH = REPO_ROOT / "results" / "tables" / "external_artifact_selection.csv"
SUMMARY_CSV_PATH = REPO_ROOT / "results" / "tables" / "external_artifact_selection_summary.csv"
SUMMARY_MD_PATH = REPO_ROOT / "results" / "tables" / "external_artifact_selection.md"

EXPECTED_COLUMNS = [
    "artifact_id",
    "study_family",
    "source_id",
    "source_name",
    "source_url",
    "source_version",
    "artifact_reference",
    "selection_status",
    "selection_basis",
    "case_count",
    "condition_evaluation_count",
    "license_policy",
    "content_boundary",
]

PROHIBITED_REFERENCE_PATTERN = re.compile(
    "|".join(
        [
            "Long" + "Cat",
            "long" + "cat",
            "Co" + "dex",
            "Chat" + "GPT",
            "generated" + " by",
            "AI-" + "written",
            "AI-" + "generated",
            "dr" + "aft",
            "work in " + "progress",
        ]
    ),
    re.IGNORECASE,
)

NON_CAPABILITY_REFERENCE_PATTERN = re.compile(
    r"(^|/)(\.github|\.gitlab|canvas-fonts|fonts?|licenses?)(/|$)|"
    r"(^|/)(funding\.yml|license(\.md|\.txt)?|copying|notice|codeowners|dependabot[^/]*)$|"
    r"(^|/)[^/]*ofl\.txt$",
    re.IGNORECASE,
)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


class ExternalArtifactSelectionTests(unittest.TestCase):
    def test_external_artifact_selection_files_exist(self) -> None:
        for path in (SELECTION_PATH, SUMMARY_CSV_PATH, SUMMARY_MD_PATH):
            self.assertTrue(path.exists(), f"Missing {path}")
            self.assertGreater(path.stat().st_size, 0, f"Empty {path}")

    def test_external_artifact_selection_totals(self) -> None:
        with SELECTION_PATH.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            self.assertEqual(reader.fieldnames, EXPECTED_COLUMNS)
            rows = list(reader)

        self.assertEqual(len(rows), 240)
        self.assertEqual(len(rows), len({row["artifact_id"] for row in rows}))
        self.assertEqual(sum(int(row["case_count"]) for row in rows), 960)
        self.assertEqual(sum(int(row["condition_evaluation_count"]) for row in rows), 2880)
        self.assertTrue(all(row["artifact_reference"] for row in rows))
        self.assertTrue(all(row["content_boundary"] == "metadata_only_no_third_party_prose_or_code_copied" for row in rows))
        self.assertEqual(sum(1 for row in rows if row["selection_status"] == "metadata_candidate"), 232)
        self.assertEqual(sum(1 for row in rows if row["selection_status"] == "target_slot_pending"), 8)

    def test_external_artifact_selection_is_metadata_only(self) -> None:
        rows = read_csv_rows(SELECTION_PATH)
        statuses = {row["selection_status"] for row in rows}
        bases = {row["selection_basis"] for row in rows}
        self.assertIn("metadata_candidate", statuses)
        self.assertIn("skill_package_directory", bases)
        self.assertIn("index_upstream_link", bases)
        self.assertFalse(any(re.search(r"\n|```", row["artifact_reference"]) for row in rows))
        self.assertFalse(any(PROHIBITED_REFERENCE_PATTERN.search(row["artifact_reference"]) for row in rows))
        self.assertFalse(any(NON_CAPABILITY_REFERENCE_PATTERN.search(row["artifact_reference"]) for row in rows))

        summary = SUMMARY_MD_PATH.read_text(encoding="utf-8")
        self.assertIn("does not copy third-party prose or code", summary)
        self.assertIn("Concrete candidate references | 232", summary)
        self.assertIn("Pending replacement slots | 8", summary)


if __name__ == "__main__":
    unittest.main()
