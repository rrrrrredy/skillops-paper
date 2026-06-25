from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
RESULTS_TABLES_DIR = REPO_ROOT / "results" / "tables"
RESULTS_EXPERIMENTS_DIR = REPO_ROOT / "results" / "experiments"
PROMPTS_DIR = REPO_ROOT / "experiments" / "prompts"

CASE_CONSTRUCTION_PATH = RESULTS_TABLES_DIR / "external_case_construction.csv"
MANIFEST_PATH = RESULTS_EXPERIMENTS_DIR / "external_condition_manifest.csv"
PROMPT_PATH = PROMPTS_DIR / "external_condition_evaluation.md"
PAYLOAD_JSONL_PATH = RESULTS_EXPERIMENTS_DIR / "external_representation_payloads.jsonl"
PAYLOAD_INDEX_PATH = RESULTS_EXPERIMENTS_DIR / "external_representation_payload_index.csv"
SUMMARY_PATH = RESULTS_EXPERIMENTS_DIR / "external_representation_payloads.md"

INDEX_COLUMNS = [
    "payload_id",
    "condition_case_id",
    "case_id",
    "artifact_id",
    "source_id",
    "artifact_family_group",
    "case_type",
    "condition",
    "shard_id",
    "payload_status",
    "prompt_path",
    "content_boundary",
]

CONTENT_BOUNDARY = "metadata_only_no_third_party_prose_or_code_copied"


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def relative(path: Path) -> str:
    return str(path.relative_to(REPO_ROOT)).replace("\\", "/")


def payload_id(condition_case_id: str) -> str:
    return "payload-" + condition_case_id.replace("::", "-").replace("_", "-")


def case_lookup() -> dict[str, dict[str, str]]:
    return {row["case_id"]: row for row in read_csv_rows(CASE_CONSTRUCTION_PATH)}


def base_reference_block(manifest_row: dict[str, str], case_row: dict[str, str]) -> list[str]:
    return [
        f"Source id: {manifest_row['source_id']}",
        f"Source version: {case_row['source_version']}",
        f"Artifact reference: {case_row['artifact_reference']}",
        f"Artifact family: {manifest_row['artifact_family_group']}",
        "Content boundary: metadata reference only; source prose and code are not copied into this payload.",
    ]


def original_freeform_representation(manifest_row: dict[str, str], case_row: dict[str, str]) -> str:
    lines = [
        "Representation condition: original_freeform",
        "Native artifact content is represented by metadata reference only.",
        *base_reference_block(manifest_row, case_row),
        "Reviewer task: construct the native/freeform representation from the pinned source before execution when license and data-handling checks permit it.",
    ]
    return "\n".join(lines)


def skillops_normalized_representation(manifest_row: dict[str, str], case_row: dict[str, str]) -> str:
    lines = [
        "Representation condition: skillops_normalized",
        "SkillOps lifecycle fields are present as metadata-only placeholders.",
        *base_reference_block(manifest_row, case_row),
        "Lifecycle fields:",
        "- metadata: source id, source version, artifact reference, and family are recorded.",
        "- trigger contract: reviewer must fill from the pinned source before execution.",
        "- context boundary: reviewer must fill required inputs, credentials, environment, and data boundaries.",
        "- execution constraints: reviewer must fill permissions, irreversible actions, and stop conditions.",
        "- tests and checks: reviewer must link source-visible tests or mark absent.",
        "- failure modes: reviewer must identify risk, ambiguity, stale-context, and permission-boundary cases.",
    ]
    return "\n".join(lines)


def ablated_component(case_type: str) -> str:
    return {
        "positive_trigger": "trigger_contract",
        "negative_trigger": "trigger_contract",
        "boundary_clarification": "context_boundary",
        "risk_constraint": "execution_constraints",
    }.get(case_type, "trigger_contract")


def skillops_ablation_representation(manifest_row: dict[str, str], case_row: dict[str, str]) -> str:
    component = ablated_component(manifest_row["case_type"])
    lines = [
        "Representation condition: skillops_ablation",
        f"Ablated lifecycle component: {component}",
        *base_reference_block(manifest_row, case_row),
        "Lifecycle fields:",
        "- metadata: source id, source version, artifact reference, and family are recorded.",
        f"- {component}: intentionally withheld for the preregistered ablation condition.",
        "- remaining fields: reviewer must fill from the pinned source before execution when license and data-handling checks permit it.",
    ]
    return "\n".join(lines)


def build_representation(manifest_row: dict[str, str], case_row: dict[str, str]) -> str:
    condition = manifest_row["condition"]
    if condition == "original_freeform":
        return original_freeform_representation(manifest_row, case_row)
    if condition == "skillops_normalized":
        return skillops_normalized_representation(manifest_row, case_row)
    if condition == "skillops_ablation":
        return skillops_ablation_representation(manifest_row, case_row)
    raise ValueError(f"Unexpected condition: {condition}")


def build_payloads() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    cases = case_lookup()
    manifest_rows = read_csv_rows(MANIFEST_PATH)
    payload_rows: list[dict[str, Any]] = []
    index_rows: list[dict[str, Any]] = []

    for manifest_row in manifest_rows:
        case_id = manifest_row["case_id"]
        if case_id not in cases:
            raise ValueError(f"Missing case construction row for {case_id}")
        case_row = cases[case_id]
        representation = build_representation(manifest_row, case_row)
        identifier = payload_id(manifest_row["condition_case_id"])
        payload_rows.append(
            {
                "payload_id": identifier,
                "condition_case_id": manifest_row["condition_case_id"],
                "case_id": case_id,
                "artifact_id": manifest_row["artifact_id"],
                "source_id": manifest_row["source_id"],
                "source_version": case_row["source_version"],
                "artifact_reference": case_row["artifact_reference"],
                "artifact_family_group": manifest_row["artifact_family_group"],
                "case_type": manifest_row["case_type"],
                "condition": manifest_row["condition"],
                "shard_id": manifest_row["shard_id"],
                "prompt_path": relative(PROMPT_PATH),
                "artifact_representation": representation,
                "user_request": case_row["user_request"],
                "expected_behavior": manifest_row["expected_behavior"],
                "risk_label": manifest_row["risk_label"],
                "payload_status": "template_ready_not_run",
                "content_boundary": CONTENT_BOUNDARY,
            }
        )
        index_rows.append(
            {
                "payload_id": identifier,
                "condition_case_id": manifest_row["condition_case_id"],
                "case_id": case_id,
                "artifact_id": manifest_row["artifact_id"],
                "source_id": manifest_row["source_id"],
                "artifact_family_group": manifest_row["artifact_family_group"],
                "case_type": manifest_row["case_type"],
                "condition": manifest_row["condition"],
                "shard_id": manifest_row["shard_id"],
                "payload_status": "template_ready_not_run",
                "prompt_path": relative(PROMPT_PATH),
                "content_boundary": CONTENT_BOUNDARY,
            }
        )
    return payload_rows, index_rows


def markdown_table(headers: list[str], rows: list[list[str]]) -> str:
    return "\n".join(
        [
            "| " + " | ".join(headers) + " |",
            "| " + " | ".join(["---"] * len(headers)) + " |",
            *["| " + " | ".join(row) + " |" for row in rows],
        ]
    )


def write_summary(payload_rows: list[dict[str, Any]]) -> None:
    condition_counts: dict[str, int] = {}
    family_counts: dict[str, int] = {}
    for row in payload_rows:
        condition_counts[row["condition"]] = condition_counts.get(row["condition"], 0) + 1
        family_counts[row["artifact_family_group"]] = family_counts.get(row["artifact_family_group"], 0) + 1

    lines = [
        "# External Representation Payloads",
        "",
        "This report summarizes metadata-only payload templates for future external-condition execution. It does not copy third-party prose or code and does not report model execution.",
        "",
        "## Totals",
        "",
        markdown_table(
            ["Quantity", "Count"],
            [
                ["Payload rows", str(len(payload_rows))],
                ["Prompt template", relative(PROMPT_PATH)],
            ],
        ),
        "",
        "## Conditions",
        "",
        markdown_table(
            ["Condition", "Payload rows"],
            [[condition, str(count)] for condition, count in sorted(condition_counts.items())],
        ),
        "",
        "## Families",
        "",
        markdown_table(
            ["Family", "Payload rows"],
            [[family, str(count)] for family, count in sorted(family_counts.items())],
        ),
        "",
    ]
    SUMMARY_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    payload_rows, index_rows = build_payloads()
    write_jsonl(PAYLOAD_JSONL_PATH, payload_rows)
    write_csv(PAYLOAD_INDEX_PATH, INDEX_COLUMNS, index_rows)
    write_summary(payload_rows)
    print(f"Wrote {PAYLOAD_JSONL_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {PAYLOAD_INDEX_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {SUMMARY_PATH.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
