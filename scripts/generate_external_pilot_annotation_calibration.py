from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
RESULTS_TABLES_DIR = REPO_ROOT / "results" / "tables"
RESULTS_EXPERIMENTS_DIR = REPO_ROOT / "results" / "experiments"

PILOT_ARTIFACTS_PATH = RESULTS_EXPERIMENTS_DIR / "external_pilot_artifacts.csv"
PILOT_CONDITION_PLAN_PATH = RESULTS_EXPERIMENTS_DIR / "external_pilot_condition_plan.csv"
CASE_CONSTRUCTION_PATH = RESULTS_TABLES_DIR / "external_case_construction.csv"
WORKLIST_PATH = RESULTS_TABLES_DIR / "external_pilot_annotation_worklist.csv"
CALIBRATION_PATH = RESULTS_TABLES_DIR / "external_pilot_annotation_calibration.csv"
SUMMARY_PATH = RESULTS_TABLES_DIR / "external_pilot_annotation_calibration.md"

BASE_COLUMNS = [
    "case_id",
    "artifact_id",
    "study_family",
    "source_id",
    "source_owner",
    "ecosystem",
    "source_version",
    "artifact_reference",
    "case_type",
    "protocol_seed_request",
    "artifact_specific_user_request",
    "artifact_specific_request_status",
    "required_evidence_refs",
    "evidence_review_status",
    "expected_behavior",
    "risk_label",
    "annotator_a_id",
    "annotator_b_id",
    "annotator_a_expected_behavior",
    "annotator_b_expected_behavior",
    "annotator_a_risk_label",
    "annotator_b_risk_label",
    "adjudicated_expected_behavior",
    "adjudicated_risk_label",
    "adjudication_reason",
    "review_status",
    "evidence_boundary",
]

EVIDENCE_BOUNDARY = "pilot_annotation_plan_not_collected_annotation"


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def build_worklist_rows() -> list[dict[str, Any]]:
    pilot_artifacts = {row["artifact_id"]: row for row in read_csv_rows(PILOT_ARTIFACTS_PATH)}
    pilot_case_ids = {row["case_id"] for row in read_csv_rows(PILOT_CONDITION_PLAN_PATH)}
    case_lookup = {row["case_id"]: row for row in read_csv_rows(CASE_CONSTRUCTION_PATH)}
    if len(pilot_case_ids) != 96:
        raise ValueError(f"Expected 96 pilot case ids, found {len(pilot_case_ids)}")

    rows: list[dict[str, Any]] = []
    for case_id in sorted(pilot_case_ids):
        case_row = case_lookup.get(case_id)
        if case_row is None:
            raise ValueError(f"Missing case construction row for {case_id}")
        artifact = pilot_artifacts[case_row["artifact_id"]]
        rows.append(
            {
                "case_id": case_id,
                "artifact_id": case_row["artifact_id"],
                "study_family": artifact["study_family"],
                "source_id": case_row["source_id"],
                "source_owner": artifact["source_owner"],
                "ecosystem": artifact["ecosystem"],
                "source_version": case_row["source_version"],
                "artifact_reference": case_row["artifact_reference"],
                "case_type": case_row["case_type"],
                "protocol_seed_request": case_row["protocol_seed_request"],
                "artifact_specific_user_request": case_row["artifact_specific_user_request"],
                "artifact_specific_request_status": case_row["artifact_specific_request_status"],
                "required_evidence_refs": case_row["required_evidence_refs"],
                "evidence_review_status": case_row["evidence_review_status"],
                "expected_behavior": case_row["expected_behavior"],
                "risk_label": case_row["risk_label"],
                "annotator_a_id": "",
                "annotator_b_id": "",
                "annotator_a_expected_behavior": "",
                "annotator_b_expected_behavior": "",
                "annotator_a_risk_label": "",
                "annotator_b_risk_label": "",
                "adjudicated_expected_behavior": "",
                "adjudicated_risk_label": "",
                "adjudication_reason": "",
                "review_status": "pending_review",
                "evidence_boundary": EVIDENCE_BOUNDARY,
            }
        )
    return rows


def select_calibration_rows(worklist_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    selected_artifacts: set[str] = set()
    rows_by_family: dict[str, list[dict[str, Any]]] = {}
    for row in worklist_rows:
        rows_by_family.setdefault(row["study_family"], []).append(row)

    for family, rows in sorted(rows_by_family.items()):
        artifact_ids = sorted({row["artifact_id"] for row in rows})
        if len(artifact_ids) < 2:
            raise ValueError(f"Expected at least two pilot artifacts for {family}")
        selected_artifacts.update(artifact_ids[:2])
    return [row for row in worklist_rows if row["artifact_id"] in selected_artifacts]


def markdown_table(headers: list[str], rows: list[list[str]]) -> str:
    return "\n".join(
        [
            "| " + " | ".join(headers) + " |",
            "| " + " | ".join(["---"] * len(headers)) + " |",
            *["| " + " | ".join(row) + " |" for row in rows],
        ]
    )


def write_summary(worklist_rows: list[dict[str, Any]], calibration_rows: list[dict[str, Any]]) -> None:
    family_counts = Counter(row["study_family"] for row in calibration_rows)
    case_type_counts = Counter(row["case_type"] for row in calibration_rows)
    lines = [
        "# External Pilot Annotation Calibration",
        "",
        "This file defines the pending human-review worklist and calibration subset for the 24-artifact pilot. It does not report collected annotations.",
        "",
        "## Totals",
        "",
        markdown_table(
            ["Quantity", "Count"],
            [
                ["Pilot worklist cases", str(len(worklist_rows))],
                ["Calibration cases", str(len(calibration_rows))],
                ["Calibration artifacts", str(len({row["artifact_id"] for row in calibration_rows}))],
            ],
        ),
        "",
        "## Calibration Families",
        "",
        markdown_table(["Family", "Cases"], [[key, str(value)] for key, value in sorted(family_counts.items())]),
        "",
        "## Calibration Case Types",
        "",
        markdown_table(["Case type", "Cases"], [[key, str(value)] for key, value in sorted(case_type_counts.items())]),
        "",
    ]
    SUMMARY_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    worklist_rows = build_worklist_rows()
    calibration_rows = select_calibration_rows(worklist_rows)
    write_csv(WORKLIST_PATH, BASE_COLUMNS, worklist_rows)
    write_csv(CALIBRATION_PATH, BASE_COLUMNS, calibration_rows)
    write_summary(worklist_rows, calibration_rows)
    print(f"Wrote {WORKLIST_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {CALIBRATION_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {SUMMARY_PATH.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
