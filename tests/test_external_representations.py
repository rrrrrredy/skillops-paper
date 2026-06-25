from __future__ import annotations

import csv
import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PROMPT_PATH = REPO_ROOT / "experiments" / "prompts" / "external_condition_evaluation.md"
PAYLOAD_JSONL_PATH = REPO_ROOT / "results" / "experiments" / "external_representation_payloads.jsonl"
PAYLOAD_INDEX_PATH = REPO_ROOT / "results" / "experiments" / "external_representation_payload_index.csv"
SUMMARY_PATH = REPO_ROOT / "results" / "experiments" / "external_representation_payloads.md"

EXPECTED_CONDITIONS = {
    "original_freeform",
    "skillops_normalized",
    "skillops_ablation",
}

CONTENT_BOUNDARY = "metadata_only_no_third_party_prose_or_code_copied"


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


class ExternalRepresentationTests(unittest.TestCase):
    def test_external_representation_files_exist(self) -> None:
        for path in (PROMPT_PATH, PAYLOAD_JSONL_PATH, PAYLOAD_INDEX_PATH, SUMMARY_PATH):
            self.assertTrue(path.exists(), f"Missing {path}")
            self.assertGreater(path.stat().st_size, 0, f"Empty {path}")

    def test_payloads_cover_manifest_conditions(self) -> None:
        payload_rows = read_jsonl(PAYLOAD_JSONL_PATH)
        index_rows = read_csv_rows(PAYLOAD_INDEX_PATH)
        self.assertEqual(len(payload_rows), 2880)
        self.assertEqual(len(index_rows), 2880)
        self.assertEqual({row["condition"] for row in payload_rows}, EXPECTED_CONDITIONS)
        self.assertEqual(len(payload_rows), len({row["payload_id"] for row in payload_rows}))
        self.assertEqual(len(index_rows), len({row["payload_id"] for row in index_rows}))

    def test_payloads_are_metadata_only_and_not_run(self) -> None:
        payload_rows = read_jsonl(PAYLOAD_JSONL_PATH)
        self.assertTrue(all(row["payload_status"] == "template_ready_not_run" for row in payload_rows))
        self.assertTrue(all(row["content_boundary"] == CONTENT_BOUNDARY for row in payload_rows))
        self.assertTrue(all("source prose and code are not copied" in row["artifact_representation"] for row in payload_rows))
        self.assertTrue(all("expected_behavior" in row for row in payload_rows))

    def test_payload_conditions_have_distinct_representation_text(self) -> None:
        payload_rows = read_jsonl(PAYLOAD_JSONL_PATH)
        by_condition = {row["condition"]: row["artifact_representation"] for row in payload_rows[:3]}
        self.assertIn("Native artifact content is represented by metadata reference only", by_condition["original_freeform"])
        self.assertIn("SkillOps lifecycle fields are present", by_condition["skillops_normalized"])
        self.assertIn("Ablated lifecycle component", by_condition["skillops_ablation"])

    def test_prompt_template_has_required_placeholders(self) -> None:
        text = PROMPT_PATH.read_text(encoding="utf-8")
        self.assertIn("{{CONDITION_CASE_ID}}", text)
        self.assertIn("{{ARTIFACT_REPRESENTATION}}", text)
        self.assertIn("{{USER_REQUEST}}", text)


if __name__ == "__main__":
    unittest.main()
