#!/usr/bin/env python3
"""Verify and summarize a Runtime Evolution Workbench Skill Impact Ledger."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from statistics import fmean
from typing import Any


SCHEMA_VERSION = "rew.skill-impact-ledger.v1"
SUMMARY_SCHEMA_VERSION = "skillops.runtime-evolution-summary.v1"
METRICS = (
    "task_quality",
    "tool_calls",
    "input_tokens",
    "output_tokens",
    "wall_time_ms",
    "rule_lines",
    "rule_words",
    "rollback_count",
    "cross_model_transfer",
)


class LedgerError(ValueError):
    """Raised when an impact ledger cannot be trusted for analysis."""


def sha256_text(value: str) -> str:
    return "sha256:" + hashlib.sha256(value.encode("utf-8")).hexdigest()


def expected_material(entry: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": entry["entry_id"],
        "proposalId": entry["proposal_id"],
        "comparisonId": entry["comparison_id"],
        "action": entry["action"],
        "decision": entry["decision"],
        "targetKind": entry["target_kind"],
        "targetPath": entry["target_path"],
        "previousDigest": entry["previous_digest"],
        "candidateDigest": entry["candidate_digest"],
        "metrics": entry["metrics"],
        "context": entry["context"],
        "evidenceRefs": entry["evidence_refs"],
        "patternIds": entry["pattern_ids"],
        "securityAttestationDigest": entry["security_attestation_digest"],
        "note": entry["note"],
        "previousEntryDigest": entry["previous_entry_digest"],
        "createdAt": entry["created_at"],
    }


def load_verified_ledger(path: Path) -> dict[str, Any]:
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise LedgerError(f"cannot read ledger: {exc}") from exc
    if not isinstance(document, dict) or document.get("schema_version") != SCHEMA_VERSION:
        raise LedgerError("unsupported Skill Impact Ledger schema")
    entries = document.get("entries")
    if not isinstance(entries, list):
        raise LedgerError("ledger entries must be an array")

    previous = None
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            raise LedgerError(f"entry {index} is not an object")
        if entry.get("previous_entry_digest") != previous:
            raise LedgerError(f"entry {index} breaks the forward chain")
        material_text = entry.get("digest_material")
        if not isinstance(material_text, str):
            raise LedgerError(f"entry {index} has no digest material")
        if sha256_text(material_text) != entry.get("entry_digest"):
            raise LedgerError(f"entry {index} digest does not match its material")
        try:
            material = json.loads(material_text)
        except json.JSONDecodeError as exc:
            raise LedgerError(f"entry {index} digest material is invalid JSON") from exc
        try:
            expected = expected_material(entry)
        except KeyError as exc:
            raise LedgerError(f"entry {index} is missing {exc.args[0]}") from exc
        if material != expected:
            raise LedgerError(f"entry {index} fields do not match its digest material")
        previous = entry["entry_digest"]
    if document.get("last_entry_digest") != previous:
        raise LedgerError("last_entry_digest does not match the verified chain")
    return document


def summarize(document: dict[str, Any]) -> dict[str, Any]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for entry in document["entries"]:
        condition = entry.get("context", {}).get("condition", "unassigned")
        grouped[str(condition)].append(entry)

    conditions = []
    for condition in sorted(grouped):
        entries = grouped[condition]
        row: dict[str, Any] = {
            "condition": condition,
            "entries": len(entries),
            "decisions": dict(sorted(Counter(entry["decision"] for entry in entries).items())),
            "rollback_events": sum(
                entry["action"] == "rollback" or entry["decision"] in {"rolled_back", "rollback_conflict"}
                for entry in entries
            ),
        }
        for metric in METRICS:
            values = [entry["metrics"].get(metric) for entry in entries]
            numeric = [float(value) for value in values if isinstance(value, (int, float)) and not isinstance(value, bool)]
            row[f"mean_{metric}"] = round(fmean(numeric), 4) if numeric else None
        conditions.append(row)

    return {
        "schema_version": SUMMARY_SCHEMA_VERSION,
        "source_schema_version": document["schema_version"],
        "ledger_id": document.get("ledger_id"),
        "last_entry_digest": document.get("last_entry_digest"),
        "chain_verified": True,
        "entries_verified": len(document["entries"]),
        "conditions": conditions,
        "claim_boundary": "Descriptive summary of a verified local ledger; no causal, provider, or model-family certification.",
    }


def write_outputs(summary: dict[str, Any], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "runtime-evolution-summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    fieldnames = ["condition", "entries", "rollback_events", *[f"mean_{metric}" for metric in METRICS]]
    with (output_dir / "runtime-evolution-summary.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in summary["conditions"]:
            writer.writerow({key: row.get(key) for key in fieldnames})

    lines = [
        "# Runtime evolution ledger summary",
        "",
        f"- Chain verified: `{str(summary['chain_verified']).lower()}`",
        f"- Entries verified: `{summary['entries_verified']}`",
        f"- Last entry: `{summary['last_entry_digest']}`",
        "",
        "| Condition | Entries | Task quality | Tool calls | Input tokens | Output tokens | Rule lines | Rollbacks | Transfer |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in summary["conditions"]:
        value = lambda key: "" if row.get(key) is None else str(row[key])
        lines.append(
            f"| {row['condition']} | {row['entries']} | {value('mean_task_quality')} | "
            f"{value('mean_tool_calls')} | {value('mean_input_tokens')} | {value('mean_output_tokens')} | "
            f"{value('mean_rule_lines')} | {row['rollback_events']} | {value('mean_cross_model_transfer')} |"
        )
    lines.extend(["", summary["claim_boundary"], ""])
    (output_dir / "runtime-evolution-summary.md").write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="rew.skill-impact-ledger.v1 JSON file")
    parser.add_argument("--output-dir", required=True, type=Path, help="directory for JSON, CSV, and Markdown summaries")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        document = load_verified_ledger(args.input)
        summary = summarize(document)
        write_outputs(summary, args.output_dir)
    except LedgerError as exc:
        raise SystemExit(f"error: {exc}") from exc
    print(f"verified {summary['entries_verified']} entries -> {args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
