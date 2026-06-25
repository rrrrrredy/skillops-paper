from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
RESULTS_TABLES_DIR = REPO_ROOT / "results" / "tables"
RESULTS_EXPERIMENTS_DIR = REPO_ROOT / "results" / "experiments"

SAMPLING_MANIFEST_PATH = RESULTS_TABLES_DIR / "external_sampling_manifest.csv"
ELIGIBILITY_MANIFEST_PATH = RESULTS_TABLES_DIR / "external_eligibility_manifest.csv"
CONDITION_PACKET_PATH = RESULTS_TABLES_DIR / "external_condition_packet.csv"

PILOT_ARTIFACTS_PATH = RESULTS_EXPERIMENTS_DIR / "external_pilot_artifacts.csv"
PILOT_CONDITION_PLAN_PATH = RESULTS_EXPERIMENTS_DIR / "external_pilot_condition_plan.csv"
PILOT_MODEL_PLAN_PATH = RESULTS_EXPERIMENTS_DIR / "external_pilot_model_plan.csv"
PILOT_SUMMARY_PATH = RESULTS_EXPERIMENTS_DIR / "external_pilot_plan.md"

DEFAULT_ARTIFACTS_PER_FAMILY = 6
DEFAULT_MODELS = [
    ("deepseek", "deepseek-v4-flash"),
    ("kimi", "kimi-k2.7-code"),
]

PILOT_ARTIFACT_COLUMNS = [
    "artifact_id",
    "study_family",
    "source_id",
    "source_owner",
    "ecosystem",
    "artifact_reference",
    "random_seed",
    "random_key",
    "pilot_status",
    "selection_reason",
]

PILOT_CONDITION_COLUMNS = [
    "condition_case_id",
    "case_id",
    "artifact_id",
    "study_family",
    "source_id",
    "source_owner",
    "ecosystem",
    "artifact_family_group",
    "case_type",
    "condition",
    "expected_behavior",
    "risk_label",
    "pilot_status",
]

PILOT_MODEL_COLUMNS = [
    "provider",
    "model",
    "condition_case_id",
    "case_id",
    "artifact_id",
    "study_family",
    "source_id",
    "source_owner",
    "ecosystem",
    "artifact_family_group",
    "case_type",
    "condition",
    "expected_behavior",
    "risk_label",
    "pilot_status",
    "evidence_boundary",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Prepare a bounded external pilot plan from seeded sampling manifests.")
    parser.add_argument("--artifacts-per-family", type=int, default=DEFAULT_ARTIFACTS_PER_FAMILY)
    return parser.parse_args()


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def eligibility_lookup() -> dict[str, dict[str, str]]:
    return {row["artifact_id"]: row for row in read_csv_rows(ELIGIBILITY_MANIFEST_PATH)}


def select_pilot_artifacts(artifacts_per_family: int) -> list[dict[str, Any]]:
    if artifacts_per_family < 1:
        raise ValueError("artifacts-per-family must be positive")
    eligibility = eligibility_lookup()
    sampling_rows = read_csv_rows(SAMPLING_MANIFEST_PATH)
    eligible_rows = [
        row
        for row in sampling_rows
        if eligibility.get(row["artifact_id"], {}).get("replacement_required") == "false"
        and eligibility.get(row["artifact_id"], {}).get("eligibility_status") == "pending_review"
    ]

    selected: list[dict[str, Any]] = []
    for family in sorted({row["study_family"] for row in eligible_rows}):
        family_rows = [row for row in eligible_rows if row["study_family"] == family]
        family_rows = sorted(family_rows, key=lambda row: (row["random_key"], row["artifact_id"]))
        if len(family_rows) < artifacts_per_family:
            raise ValueError(f"Not enough within-cap candidate rows for {family}: {len(family_rows)}")
        for row in family_rows[:artifacts_per_family]:
            selected.append(
                {
                    "artifact_id": row["artifact_id"],
                    "study_family": row["study_family"],
                    "source_id": row["source_id"],
                    "source_owner": row["source_owner"],
                    "ecosystem": row["ecosystem"],
                    "artifact_reference": row["artifact_reference"],
                    "random_seed": row["random_seed"],
                    "random_key": row["random_key"],
                    "pilot_status": "selected_pending_annotation",
                    "selection_reason": "first_seeded_within_cap_row_per_family",
                }
            )
    return selected


def build_condition_rows(selected_artifacts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    selected_lookup = {row["artifact_id"]: row for row in selected_artifacts}
    rows: list[dict[str, Any]] = []
    for row in read_csv_rows(CONDITION_PACKET_PATH):
        artifact = selected_lookup.get(row["artifact_id"])
        if artifact is None:
            continue
        rows.append(
            {
                "condition_case_id": row["condition_case_id"],
                "case_id": row["case_id"],
                "artifact_id": row["artifact_id"],
                "study_family": artifact["study_family"],
                "source_id": row["source_id"],
                "source_owner": artifact["source_owner"],
                "ecosystem": artifact["ecosystem"],
                "artifact_family_group": row["artifact_family_group"],
                "case_type": row["case_type"],
                "condition": row["condition"],
                "expected_behavior": row["expected_behavior"],
                "risk_label": row["risk_label"],
                "pilot_status": "selected_pending_annotation",
            }
        )
    expected_count = len(selected_artifacts) * 4 * 3
    if len(rows) != expected_count:
        raise ValueError(f"Expected {expected_count} pilot condition rows, found {len(rows)}")
    return rows


def build_model_rows(condition_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for provider, model in DEFAULT_MODELS:
        for row in condition_rows:
            rows.append(
                {
                    "provider": provider,
                    "model": model,
                    "condition_case_id": row["condition_case_id"],
                    "case_id": row["case_id"],
                    "artifact_id": row["artifact_id"],
                    "study_family": row["study_family"],
                    "source_id": row["source_id"],
                    "source_owner": row["source_owner"],
                    "ecosystem": row["ecosystem"],
                    "artifact_family_group": row["artifact_family_group"],
                    "case_type": row["case_type"],
                    "condition": row["condition"],
                    "expected_behavior": row["expected_behavior"],
                    "risk_label": row["risk_label"],
                    "pilot_status": "selected_pending_annotation",
                    "evidence_boundary": "pilot_plan_not_external_effect_estimate",
                }
            )
    return rows


def markdown_table(headers: list[str], rows: list[list[str]]) -> str:
    return "\n".join(
        [
            "| " + " | ".join(headers) + " |",
            "| " + " | ".join(["---"] * len(headers)) + " |",
            *["| " + " | ".join(row) + " |" for row in rows],
        ]
    )


def write_summary(artifact_rows: list[dict[str, Any]], condition_rows: list[dict[str, Any]], model_rows: list[dict[str, Any]]) -> None:
    family_counts = Counter(row["study_family"] for row in artifact_rows)
    source_counts = Counter(row["source_id"] for row in artifact_rows)
    owner_counts = Counter(row["source_owner"] for row in artifact_rows)
    provider_counts = Counter(f"{row['provider']}::{row['model']}" for row in model_rows)

    lines = [
        "# External Pilot Plan",
        "",
        "This plan selects a bounded, seeded 24-artifact pilot from within-cap external candidates. It is intended to estimate annotation disagreement, parse failures, provider failures, and execution logistics; it is not a final external effect estimate.",
        "",
        "## Totals",
        "",
        markdown_table(
            ["Quantity", "Count"],
            [
                ["Pilot artifacts", str(len(artifact_rows))],
                ["Pilot base cases", str(len(artifact_rows) * 4)],
                ["Pilot condition rows per model", str(len(condition_rows))],
                ["Pilot provider-condition rows", str(len(model_rows))],
            ],
        ),
        "",
        "## Families",
        "",
        markdown_table(["Family", "Artifacts"], [[key, str(value)] for key, value in sorted(family_counts.items())]),
        "",
        "## Sources",
        "",
        markdown_table(["Source", "Artifacts"], [[key, str(value)] for key, value in sorted(source_counts.items())]),
        "",
        "## Owners",
        "",
        markdown_table(["Owner", "Artifacts"], [[key, str(value)] for key, value in sorted(owner_counts.items())]),
        "",
        "## Provider Rows",
        "",
        markdown_table(["Provider/model", "Rows"], [[key, str(value)] for key, value in sorted(provider_counts.items())]),
        "",
    ]
    PILOT_SUMMARY_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    args = parse_args()
    artifact_rows = select_pilot_artifacts(args.artifacts_per_family)
    condition_rows = build_condition_rows(artifact_rows)
    model_rows = build_model_rows(condition_rows)
    write_csv(PILOT_ARTIFACTS_PATH, PILOT_ARTIFACT_COLUMNS, artifact_rows)
    write_csv(PILOT_CONDITION_PLAN_PATH, PILOT_CONDITION_COLUMNS, condition_rows)
    write_csv(PILOT_MODEL_PLAN_PATH, PILOT_MODEL_COLUMNS, model_rows)
    write_summary(artifact_rows, condition_rows, model_rows)
    print(f"Wrote {PILOT_ARTIFACTS_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {PILOT_CONDITION_PLAN_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {PILOT_MODEL_PLAN_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {PILOT_SUMMARY_PATH.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
