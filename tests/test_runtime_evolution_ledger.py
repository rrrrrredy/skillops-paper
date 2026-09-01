from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "analyze_runtime_evolution_ledger.py"
SPEC = importlib.util.spec_from_file_location("analyze_runtime_evolution_ledger", SCRIPT_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


def make_entry(index: int, previous: str | None, condition: str, quality: int) -> dict:
    material = {
        "id": f"impact-{index}",
        "proposalId": None,
        "comparisonId": None,
        "action": "study",
        "decision": "supported" if quality > 50 else "held",
        "targetKind": "skill",
        "targetPath": "skills/repository-planning/SKILL.md",
        "previousDigest": "sha256:" + "0" * 64,
        "candidateDigest": "sha256:" + str(index) * 64,
        "metrics": {"task_quality": quality, "tool_calls": index, "rule_lines": 12 + index},
        "context": {"condition": condition, "iteration": index},
        "evidenceRefs": [f"case-{index}"],
        "patternIds": [],
        "securityAttestationDigest": None,
        "note": "Fixture study result.",
        "previousEntryDigest": previous,
        "createdAt": f"2026-09-01T00:00:0{index}.000Z",
    }
    material_text = json.dumps(material, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
    digest = "sha256:" + hashlib.sha256(material_text.encode("utf-8")).hexdigest()
    entry = {
        "entry_id": material["id"],
        "proposal_id": None,
        "comparison_id": None,
        "action": material["action"],
        "decision": material["decision"],
        "target_kind": material["targetKind"],
        "target_path": material["targetPath"],
        "previous_digest": material["previousDigest"],
        "candidate_digest": material["candidateDigest"],
        "metrics": material["metrics"],
        "context": material["context"],
        "evidence_refs": material["evidenceRefs"],
        "pattern_ids": [],
        "security_attestation_digest": None,
        "note": material["note"],
        "previous_entry_digest": previous,
        "digest_material": material_text,
        "entry_digest": digest,
        "created_at": material["createdAt"],
    }
    return entry


class RuntimeEvolutionLedgerTests(unittest.TestCase):
    def test_verifies_chain_and_summarizes_conditions(self):
        first = make_entry(1, None, "no_wiki", 50)
        second = make_entry(2, first["entry_digest"], "persistent_wiki", 75)
        document = {
            "schema_version": "rew.skill-impact-ledger.v1",
            "ledger_id": "skill-impact-ledger:" + "a" * 64,
            "generated_at": "2026-09-01T00:00:10.000Z",
            "product": {"name": "runtime-evolution-workbench", "version": "0.3.0"},
            "last_entry_digest": second["entry_digest"],
            "entries": [first, second],
        }
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "ledger.json"
            path.write_text(json.dumps(document), encoding="utf-8")
            verified = MODULE.load_verified_ledger(path)
            summary = MODULE.summarize(verified)
        self.assertTrue(summary["chain_verified"])
        self.assertEqual(summary["entries_verified"], 2)
        rows = {row["condition"]: row for row in summary["conditions"]}
        self.assertEqual(rows["persistent_wiki"]["mean_task_quality"], 75.0)

    def test_rejects_field_tampering_even_when_digest_material_is_unchanged(self):
        entry = make_entry(1, None, "no_wiki", 50)
        entry["metrics"]["task_quality"] = 100
        document = {
            "schema_version": "rew.skill-impact-ledger.v1",
            "last_entry_digest": entry["entry_digest"],
            "entries": [entry],
        }
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "ledger.json"
            path.write_text(json.dumps(document), encoding="utf-8")
            with self.assertRaisesRegex(MODULE.LedgerError, "fields do not match"):
                MODULE.load_verified_ledger(path)


if __name__ == "__main__":
    unittest.main()
