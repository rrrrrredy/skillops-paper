from __future__ import annotations

import csv
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = REPO_ROOT / "results" / "tables" / "external_sampling_manifest.csv"
SUMMARY_PATH = REPO_ROOT / "results" / "tables" / "external_sampling_manifest.md"

EXPECTED_COLUMNS = [
    "artifact_id",
    "source_owner",
    "ecosystem",
    "source_id",
    "study_family",
    "artifact_reference",
    "stratum",
    "random_seed",
    "random_key",
    "source_cap",
    "source_share",
    "owner_cap",
    "owner_share",
    "cap_status",
    "inclusion_status",
    "replacement_for",
    "eligibility_status",
    "license_policy",
    "content_boundary",
]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


class ExternalSamplingManifestTests(unittest.TestCase):
    def test_sampling_manifest_files_exist(self) -> None:
        for path in (MANIFEST_PATH, SUMMARY_PATH):
            self.assertTrue(path.exists(), f"Missing {path}")
            self.assertGreater(path.stat().st_size, 0, f"Empty {path}")

    def test_sampling_manifest_has_seeded_strata(self) -> None:
        with MANIFEST_PATH.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            self.assertEqual(reader.fieldnames, EXPECTED_COLUMNS)
            rows = list(reader)

        self.assertEqual(len(rows), 240)
        self.assertEqual(len({row["artifact_id"] for row in rows}), 240)
        self.assertEqual({row["random_seed"] for row in rows}, {"20260625"})
        self.assertTrue(all(row["random_key"] for row in rows))
        self.assertTrue(all(row["source_owner"] for row in rows))
        self.assertTrue(all(row["ecosystem"] for row in rows))
        self.assertTrue(all(row["eligibility_status"] == "pending_review" for row in rows))
        self.assertTrue(all(row["content_boundary"] == "metadata_only_no_third_party_prose_or_code_copied" for row in rows))

    def test_sampling_manifest_reports_cap_pressure(self) -> None:
        rows = read_csv_rows(MANIFEST_PATH)
        cap_statuses = {row["cap_status"] for row in rows}
        self.assertIn("cap_exceeded_requires_replacement_or_expansion", cap_statuses)
        self.assertIn("within_caps", cap_statuses)

        summary = SUMMARY_PATH.read_text(encoding="utf-8")
        self.assertIn("Rows exceeding target caps", summary)
        self.assertIn("sampling frame, not an eligibility or outcome result", summary)


if __name__ == "__main__":
    unittest.main()
