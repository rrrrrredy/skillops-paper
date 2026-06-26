from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
RESULTS_TABLES_DIR = REPO_ROOT / "results" / "tables"

WORKLIST_PATH = RESULTS_TABLES_DIR / "external_pilot_annotation_worklist.csv"
CALIBRATION_PATH = RESULTS_TABLES_DIR / "external_pilot_annotation_calibration.csv"
ASSIGNMENT_PATH = RESULTS_TABLES_DIR / "external_annotation_assignment_manifest.csv"
ADJUDICATION_PATH = RESULTS_TABLES_DIR / "external_annotation_adjudication_log.csv"
SUMMARY_PATH = RESULTS_TABLES_DIR / "external_annotation_execution_summary.md"

ASSIGNMENT_COLUMNS = [
    "assignment_id",
    "case_id",
    "artifact_id",
    "study_family",
    "case_type",
    "review_phase",
    "reviewer_slot",
    "reviewer_id",
    "assignment_status",
    "peer_response_visibility",
    "released_data_boundary",
]

ADJUDICATION_COLUMNS = [
    "case_id",
    "artifact_id",
    "study_family",
    "case_type",
    "annotator_a_expected_behavior",
    "annotator_b_expected_behavior",
    "annotator_a_risk_label",
    "annotator_b_risk_label",
    "expected_behavior_disagreement",
    "risk_label_disagreement",
    "adjudicator_id",
    "adjudicated_expected_behavior",
    "adjudicated_risk_label",
    "adjudication_reason",
    "adjudication_status",
]

RELEASED_DATA_BOUNDARY = "metadata_only_no_contact_payment_or_private_source_data"


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def review_phase(case_id: str, calibration_case_ids: set[str]) -> str:
    if case_id in calibration_case_ids:
        return "calibration"
    return "pilot_after_calibration_lock"


def build_assignment_rows(worklist_rows: list[dict[str, str]], calibration_case_ids: set[str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in sorted(worklist_rows, key=lambda item: (review_phase(item["case_id"], calibration_case_ids), item["case_id"])):
        for reviewer_slot, reviewer_id in (("a", "rater_001"), ("b", "rater_002")):
            rows.append(
                {
                    "assignment_id": f"{row['case_id']}::{reviewer_slot}",
                    "case_id": row["case_id"],
                    "artifact_id": row["artifact_id"],
                    "study_family": row["study_family"],
                    "case_type": row["case_type"],
                    "review_phase": review_phase(row["case_id"], calibration_case_ids),
                    "reviewer_slot": reviewer_slot,
                    "reviewer_id": reviewer_id,
                    "assignment_status": "reserved_pending_external_reviewer",
                    "peer_response_visibility": "hidden_until_independent_review_complete",
                    "released_data_boundary": RELEASED_DATA_BOUNDARY,
                }
            )
    return rows


def build_adjudication_rows(worklist_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in sorted(worklist_rows, key=lambda item: item["case_id"]):
        a_expected = row.get("annotator_a_expected_behavior", "")
        b_expected = row.get("annotator_b_expected_behavior", "")
        a_risk = row.get("annotator_a_risk_label", "")
        b_risk = row.get("annotator_b_risk_label", "")
        expected_disagreement = bool(a_expected and b_expected and a_expected != b_expected)
        risk_disagreement = bool(a_risk and b_risk and a_risk != b_risk)
        status = "pending_disagreement_adjudication" if expected_disagreement or risk_disagreement else "not_ready_pending_independent_labels"
        rows.append(
            {
                "case_id": row["case_id"],
                "artifact_id": row["artifact_id"],
                "study_family": row["study_family"],
                "case_type": row["case_type"],
                "annotator_a_expected_behavior": a_expected,
                "annotator_b_expected_behavior": b_expected,
                "annotator_a_risk_label": a_risk,
                "annotator_b_risk_label": b_risk,
                "expected_behavior_disagreement": str(expected_disagreement).lower(),
                "risk_label_disagreement": str(risk_disagreement).lower(),
                "adjudicator_id": "",
                "adjudicated_expected_behavior": "",
                "adjudicated_risk_label": "",
                "adjudication_reason": "",
                "adjudication_status": status,
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


def write_summary(worklist_rows: list[dict[str, str]], assignment_rows: list[dict[str, Any]], adjudication_rows: list[dict[str, Any]]) -> None:
    phase_counts = Counter(row["review_phase"] for row in assignment_rows)
    family_counts = Counter(row["study_family"] for row in worklist_rows)
    adjudication_counts = Counter(row["adjudication_status"] for row in adjudication_rows)
    lines = [
        "# External Annotation Execution Summary",
        "",
        "This summary turns the 24-artifact pilot review plan into assignable rows and an adjudication log template. It does not report collected human labels.",
        "",
        "## Totals",
        "",
        markdown_table(
            ["Quantity", "Count"],
            [
                ["Pilot cases", str(len(worklist_rows))],
                ["Reviewer assignments", str(len(assignment_rows))],
                ["Adjudication rows", str(len(adjudication_rows))],
            ],
        ),
        "",
        "## Assignment Phases",
        "",
        markdown_table(["Phase", "Assignments"], [[key, str(value)] for key, value in sorted(phase_counts.items())]),
        "",
        "## Families",
        "",
        markdown_table(["Family", "Cases"], [[key, str(value)] for key, value in sorted(family_counts.items())]),
        "",
        "## Adjudication State",
        "",
        markdown_table(["Status", "Rows"], [[key, str(value)] for key, value in sorted(adjudication_counts.items())]),
        "",
        "## Boundary",
        "",
        "Reviewer contact details, compensation records, consent records, and private source access notes must stay outside this repository. Released tables use study-local reviewer IDs only.",
        "",
    ]
    SUMMARY_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    worklist_rows = read_csv_rows(WORKLIST_PATH)
    calibration_case_ids = {row["case_id"] for row in read_csv_rows(CALIBRATION_PATH)}
    assignment_rows = build_assignment_rows(worklist_rows, calibration_case_ids)
    adjudication_rows = build_adjudication_rows(worklist_rows)
    write_csv(ASSIGNMENT_PATH, ASSIGNMENT_COLUMNS, assignment_rows)
    write_csv(ADJUDICATION_PATH, ADJUDICATION_COLUMNS, adjudication_rows)
    write_summary(worklist_rows, assignment_rows, adjudication_rows)
    print(f"Wrote {ASSIGNMENT_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {ADJUDICATION_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {SUMMARY_PATH.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
