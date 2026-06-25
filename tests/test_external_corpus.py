from __future__ import annotations

import csv
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
EXTERNAL_CORPUS_PATH = REPO_ROOT / "benchmark" / "external_artifact_corpus_sources.csv"
EXTERNAL_PROTOCOL_PATH = REPO_ROOT / "experiments" / "external_validation_protocol.md"

EXPECTED_COLUMNS = [
    "source_id",
    "source_name",
    "source_url",
    "artifact_family",
    "license_status",
    "reuse_status",
    "sample_fields",
    "lifecycle_mapping",
    "notes",
]


class ExternalCorpusTests(unittest.TestCase):
    def test_external_corpus_sources_are_structured(self) -> None:
        self.assertTrue(EXTERNAL_CORPUS_PATH.exists())
        with EXTERNAL_CORPUS_PATH.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            self.assertEqual(reader.fieldnames, EXPECTED_COLUMNS)
            rows = list(reader)

        self.assertGreaterEqual(len(rows), 10)
        self.assertEqual(len(rows), len({row["source_id"] for row in rows}))
        for row in rows:
            self.assertTrue(row["source_url"].startswith("https://"))
            self.assertTrue(row["artifact_family"])
            self.assertTrue(row["lifecycle_mapping"])

    def test_external_validation_protocol_exists(self) -> None:
        self.assertTrue(EXTERNAL_PROTOCOL_PATH.exists())
        text = EXTERNAL_PROTOCOL_PATH.read_text(encoding="utf-8")
        self.assertIn("960 cases", text)
        self.assertIn("mixed-effects logistic model", text)
        self.assertIn("48-72 participants", text)


if __name__ == "__main__":
    unittest.main()
