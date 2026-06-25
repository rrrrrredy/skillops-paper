from __future__ import annotations

import csv
from collections import Counter, defaultdict
from decimal import Decimal
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
BENCHMARK_DIR = REPO_ROOT / "benchmark"
EXPERIMENTS_DIR = REPO_ROOT / "experiments"
RESULTS_TABLES_DIR = REPO_ROOT / "results" / "tables"

SOURCE_FRAME_PATH = BENCHMARK_DIR / "external_artifact_corpus_sources.csv"
STATIC_ANALYSIS_PATH = RESULTS_TABLES_DIR / "external_corpus_static_analysis.csv"
SEED_CASES_PATH = EXPERIMENTS_DIR / "external_case_seed.csv"
ALLOCATION_PATH = RESULTS_TABLES_DIR / "external_case_allocation.csv"
CASE_PLAN_PATH = RESULTS_TABLES_DIR / "external_case_plan.csv"
CONDITION_PLAN_PATH = RESULTS_TABLES_DIR / "external_condition_plan.csv"
SUMMARY_PATH = RESULTS_TABLES_DIR / "external_case_plan.md"

STUDY_FAMILY_TARGETS = {
    "agent_skills": 80,
    "mcp_and_tool_recipes": 60,
    "agent_workflow_templates": 50,
    "prompt_and_function_recipes": 50,
}

ARTIFACT_FAMILY_TO_STUDY_FAMILY = {
    "agent_skill_standard": "agent_skills",
    "agent_skill_repository": "agent_skills",
    "agent_skill_index": "agent_skills",
    "mcp_server_repository": "mcp_and_tool_recipes",
    "mcp_server": "mcp_and_tool_recipes",
    "agent_workflow_repository": "agent_workflow_templates",
    "agent_workflow_template": "agent_workflow_templates",
    "prompt_corpus": "prompt_and_function_recipes",
    "function_recipe_repository": "prompt_and_function_recipes",
}

SOURCE_WEIGHTS = {
    "agent_skill_repository": 3,
    "agent_skill_index": 1,
    "mcp_server_repository": 2,
    "mcp_server": 1,
    "agent_workflow_repository": 2,
    "agent_workflow_template": 1,
    "prompt_corpus": 1,
    "function_recipe_repository": 1,
}

CASE_TYPES = {
    "positive_trigger": {
        "expected_behavior": "trigger",
        "construction_rule": "Request is in scope for the selected artifact and should be routed to it.",
    },
    "negative_trigger": {
        "expected_behavior": "no_trigger",
        "construction_rule": "Request shares surface vocabulary but falls outside the artifact boundary.",
    },
    "boundary_clarification": {
        "expected_behavior": "clarify_scope",
        "construction_rule": "Request is under-specified or missing a required precondition.",
    },
    "risk_constraint": {
        "expected_behavior": "apply_constraint_or_refuse",
        "construction_rule": "Request touches permission, privacy, safety, stale-context, or execution constraints.",
    },
}

CONDITIONS = [
    "original_freeform",
    "skillops_normalized",
    "skillops_ablation",
]

SOURCE_ALLOCATION_COLUMNS = [
    "study_family",
    "source_id",
    "source_name",
    "source_url",
    "artifact_family",
    "sampling_role",
    "selection_weight",
    "target_artifacts",
    "target_base_cases",
    "target_condition_evaluations",
    "source_version_policy",
    "license_policy",
]

CASE_PLAN_COLUMNS = [
    "case_group_id",
    "study_family",
    "source_id",
    "case_type",
    "expected_behavior",
    "target_base_cases",
    "conditions",
    "artifact_selection_rule",
    "case_construction_rule",
]

CONDITION_PLAN_COLUMNS = [
    "condition_group_id",
    "study_family",
    "source_id",
    "case_type",
    "condition",
    "target_evaluations",
    "representation_rule",
]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def study_family_for(source: dict[str, str]) -> str:
    artifact_family = source["artifact_family"]
    if artifact_family not in ARTIFACT_FAMILY_TO_STUDY_FAMILY:
        raise ValueError(f"Unmapped artifact family: {artifact_family}")
    return ARTIFACT_FAMILY_TO_STUDY_FAMILY[artifact_family]


def sampling_role(source: dict[str, str], static_row: dict[str, str] | None) -> str:
    if static_row is None or static_row.get("analysis_status") == "metadata_only":
        return "metadata_reference"
    if source["artifact_family"] == "agent_skill_index":
        return "discovery_index"
    return "sampling_candidate"


def source_weight(source: dict[str, str], role: str) -> int:
    if role == "metadata_reference":
        return 0
    return SOURCE_WEIGHTS.get(source["artifact_family"], 1)


def allocate_targets(rows: list[dict[str, Any]], target: int) -> dict[str, int]:
    weighted_rows = [row for row in rows if int(row["selection_weight"]) > 0]
    if not weighted_rows:
        raise ValueError("Cannot allocate targets without sampling candidates")
    total_weight = sum(int(row["selection_weight"]) for row in weighted_rows)
    allocation: dict[str, int] = {}
    remainders: list[tuple[Decimal, str]] = []

    for row in weighted_rows:
        source_id = str(row["source_id"])
        exact = Decimal(target * int(row["selection_weight"])) / Decimal(total_weight)
        floor = int(exact)
        allocation[source_id] = floor
        remainders.append((exact - floor, source_id))

    remainder_count = target - sum(allocation.values())
    remainders.sort(key=lambda item: (-item[0], item[1]))
    for _, source_id in remainders[:remainder_count]:
        allocation[source_id] += 1
    return allocation


def build_allocation_rows() -> list[dict[str, Any]]:
    sources = read_csv_rows(SOURCE_FRAME_PATH)
    static_rows = {row["source_id"]: row for row in read_csv_rows(STATIC_ANALYSIS_PATH)}
    staged_rows: list[dict[str, Any]] = []

    for source in sources:
        static_row = static_rows.get(source["source_id"])
        role = sampling_role(source, static_row)
        weight = source_weight(source, role)
        staged_rows.append(
            {
                "study_family": study_family_for(source),
                "source_id": source["source_id"],
                "source_name": source["source_name"],
                "source_url": source["source_url"],
                "artifact_family": source["artifact_family"],
                "sampling_role": role,
                "selection_weight": weight,
                "target_artifacts": 0,
                "target_base_cases": 0,
                "target_condition_evaluations": 0,
                "source_version_policy": "Pin commit, release tag, or immutable source snapshot before case execution.",
                "license_policy": "Record license status before copying text; keep metadata-only cases when reuse is unclear.",
            }
        )

    rows_by_family: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in staged_rows:
        rows_by_family[str(row["study_family"])].append(row)

    for study_family, target in STUDY_FAMILY_TARGETS.items():
        allocation = allocate_targets(rows_by_family[study_family], target)
        for row in rows_by_family[study_family]:
            source_target = allocation.get(str(row["source_id"]), 0)
            row["target_artifacts"] = source_target
            row["target_base_cases"] = source_target * len(CASE_TYPES)
            row["target_condition_evaluations"] = source_target * len(CASE_TYPES) * len(CONDITIONS)

    return staged_rows


def build_case_plan_rows(allocation_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in allocation_rows:
        target_artifacts = int(source["target_artifacts"])
        if target_artifacts == 0:
            continue
        for case_type, spec in CASE_TYPES.items():
            rows.append(
                {
                    "case_group_id": f"{source['source_id']}::{case_type}",
                    "study_family": source["study_family"],
                    "source_id": source["source_id"],
                    "case_type": case_type,
                    "expected_behavior": spec["expected_behavior"],
                    "target_base_cases": target_artifacts,
                    "conditions": ";".join(CONDITIONS),
                    "artifact_selection_rule": "Sample artifacts inside the source stratum after version and license checks.",
                    "case_construction_rule": spec["construction_rule"],
                }
            )
    return rows


def build_condition_plan_rows(case_plan_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    representation_rules = {
        "original_freeform": "Use the native artifact form or metadata-preserving paraphrase allowed by license.",
        "skillops_normalized": "Represent the same operational content with the SkillOps lifecycle fields.",
        "skillops_ablation": "Remove or weaken one preregistered lifecycle component while preserving task content.",
    }
    rows: list[dict[str, Any]] = []
    for case_row in case_plan_rows:
        for condition in CONDITIONS:
            rows.append(
                {
                    "condition_group_id": f"{case_row['case_group_id']}::{condition}",
                    "study_family": case_row["study_family"],
                    "source_id": case_row["source_id"],
                    "case_type": case_row["case_type"],
                    "condition": condition,
                    "target_evaluations": case_row["target_base_cases"],
                    "representation_rule": representation_rules[condition],
                }
            )
    return rows


def validate_seed_cases(allocation_rows: list[dict[str, Any]]) -> None:
    known_sources = {str(row["source_id"]) for row in allocation_rows}
    expected_columns = [
        "case_id",
        "source_id",
        "source_version",
        "artifact_reference",
        "artifact_family_group",
        "case_type",
        "user_request",
        "expected_behavior",
        "risk_label",
        "label_source",
        "notes",
    ]
    with SEED_CASES_PATH.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != expected_columns:
            raise ValueError(f"Unexpected seed columns: {reader.fieldnames}")
        rows = list(reader)

    seen_ids: set[str] = set()
    for row in rows:
        case_id = row["case_id"]
        if case_id in seen_ids:
            raise ValueError(f"Duplicate seed case id: {case_id}")
        seen_ids.add(case_id)
        if row["source_id"] not in known_sources:
            raise ValueError(f"Unknown seed source: {row['source_id']}")
        if row["artifact_family_group"] not in STUDY_FAMILY_TARGETS:
            raise ValueError(f"Unknown seed study family: {row['artifact_family_group']}")
        if row["case_type"] not in CASE_TYPES:
            raise ValueError(f"Unknown seed case type: {row['case_type']}")


def markdown_table(headers: list[str], rows: list[list[str]]) -> str:
    return "\n".join(
        [
            "| " + " | ".join(headers) + " |",
            "| " + " | ".join(["---"] * len(headers)) + " |",
            *["| " + " | ".join(row) + " |" for row in rows],
        ]
    )


def write_summary(
    allocation_rows: list[dict[str, Any]],
    case_plan_rows: list[dict[str, Any]],
    condition_plan_rows: list[dict[str, Any]],
) -> None:
    family_counts: Counter[str] = Counter()
    family_cases: Counter[str] = Counter()
    family_evaluations: Counter[str] = Counter()
    for row in allocation_rows:
        family = str(row["study_family"])
        family_counts[family] += int(row["target_artifacts"])
        family_cases[family] += int(row["target_base_cases"])
        family_evaluations[family] += int(row["target_condition_evaluations"])

    lines = [
        "# External Case Plan",
        "",
        "This file records the deterministic allocation for the planned external-corpus study. It is a protocol artifact and does not report collected outcomes.",
        "",
        "## Totals",
        "",
        markdown_table(
            ["Quantity", "Count"],
            [
                ["Target artifacts", str(sum(family_counts.values()))],
                ["Base cases", str(sum(int(row["target_base_cases"]) for row in case_plan_rows))],
                ["Condition evaluations", str(sum(int(row["target_evaluations"]) for row in condition_plan_rows))],
            ],
        ),
        "",
        "## Study Families",
        "",
        markdown_table(
            ["Family", "Artifacts", "Base cases", "Condition evaluations"],
            [
                [
                    family,
                    str(family_counts[family]),
                    str(family_cases[family]),
                    str(family_evaluations[family]),
                ]
                for family in STUDY_FAMILY_TARGETS
            ],
        ),
        "",
        "## Source Allocation",
        "",
        markdown_table(
            ["Source", "Role", "Artifacts", "Base cases", "Condition evaluations"],
            [
                [
                    str(row["source_id"]),
                    str(row["sampling_role"]),
                    str(row["target_artifacts"]),
                    str(row["target_base_cases"]),
                    str(row["target_condition_evaluations"]),
                ]
                for row in allocation_rows
            ],
        ),
        "",
    ]
    SUMMARY_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    allocation_rows = build_allocation_rows()
    validate_seed_cases(allocation_rows)
    case_plan_rows = build_case_plan_rows(allocation_rows)
    condition_plan_rows = build_condition_plan_rows(case_plan_rows)

    write_csv(ALLOCATION_PATH, SOURCE_ALLOCATION_COLUMNS, allocation_rows)
    write_csv(CASE_PLAN_PATH, CASE_PLAN_COLUMNS, case_plan_rows)
    write_csv(CONDITION_PLAN_PATH, CONDITION_PLAN_COLUMNS, condition_plan_rows)
    write_summary(allocation_rows, case_plan_rows, condition_plan_rows)

    print(f"Wrote {ALLOCATION_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {CASE_PLAN_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {CONDITION_PLAN_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {SUMMARY_PATH.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
