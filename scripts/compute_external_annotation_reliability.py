from __future__ import annotations

import csv
import math
from collections import Counter
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
RESULTS_TABLES_DIR = REPO_ROOT / "results" / "tables"

WORKLIST_PATH = RESULTS_TABLES_DIR / "external_pilot_annotation_worklist.csv"
RELIABILITY_PATH = RESULTS_TABLES_DIR / "external_annotation_reliability.csv"
RELIABILITY_MD_PATH = RESULTS_TABLES_DIR / "external_annotation_reliability.md"

RELIABILITY_COLUMNS = [
    "metric",
    "label_field",
    "records_available",
    "value",
    "analysis_status",
    "notes",
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


def format_float(value: float | None) -> str:
    if value is None or math.isnan(value):
        return ""
    return f"{value:.6f}"


def paired_labels(rows: list[dict[str, str]], left_field: str, right_field: str) -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []
    for row in rows:
        left = row.get(left_field, "").strip()
        right = row.get(right_field, "").strip()
        if left and right:
            pairs.append((left, right))
    return pairs


def raw_agreement(pairs: list[tuple[str, str]]) -> float | None:
    if not pairs:
        return None
    return sum(1 for left, right in pairs if left == right) / len(pairs)


def cohens_kappa(pairs: list[tuple[str, str]]) -> float | None:
    if not pairs:
        return None
    observed = raw_agreement(pairs)
    if observed is None:
        return None
    left_counts = Counter(left for left, _ in pairs)
    right_counts = Counter(right for _, right in pairs)
    labels = sorted(set(left_counts) | set(right_counts))
    total = len(pairs)
    expected = sum((left_counts[label] / total) * (right_counts[label] / total) for label in labels)
    if math.isclose(1.0 - expected, 0.0):
        return None
    return (observed - expected) / (1.0 - expected)


def reliability_rows(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    specs = [
        (
            "expected_behavior",
            "annotator_a_expected_behavior",
            "annotator_b_expected_behavior",
            "Independent expected-behavior labels are required before reporting agreement.",
        ),
        (
            "risk_label",
            "annotator_a_risk_label",
            "annotator_b_risk_label",
            "Independent risk labels are required before reporting agreement.",
        ),
    ]
    output_rows: list[dict[str, Any]] = []
    for label_field, left_field, right_field, missing_note in specs:
        pairs = paired_labels(rows, left_field, right_field)
        if not pairs:
            output_rows.extend(
                [
                    {
                        "metric": "raw_agreement",
                        "label_field": label_field,
                        "records_available": 0,
                        "value": "",
                        "analysis_status": "not_available",
                        "notes": missing_note,
                    },
                    {
                        "metric": "cohens_kappa",
                        "label_field": label_field,
                        "records_available": 0,
                        "value": "",
                        "analysis_status": "not_available",
                        "notes": missing_note,
                    },
                ]
            )
            continue
        output_rows.extend(
            [
                {
                    "metric": "raw_agreement",
                    "label_field": label_field,
                    "records_available": len(pairs),
                    "value": format_float(raw_agreement(pairs)),
                    "analysis_status": "descriptive_reliability",
                    "notes": "Agreement over rows with two completed independent labels.",
                },
                {
                    "metric": "cohens_kappa",
                    "label_field": label_field,
                    "records_available": len(pairs),
                    "value": format_float(cohens_kappa(pairs)),
                    "analysis_status": "descriptive_reliability",
                    "notes": "Cohen kappa over rows with two completed independent labels.",
                },
            ]
        )
    return output_rows


def markdown_table(headers: list[str], rows: list[list[str]]) -> str:
    return "\n".join(
        [
            "| " + " | ".join(headers) + " |",
            "| " + " | ".join(["---"] * len(headers)) + " |",
            *["| " + " | ".join(row) + " |" for row in rows],
        ]
    )


def write_summary(rows: list[dict[str, Any]]) -> None:
    lines = [
        "# External Annotation Reliability",
        "",
        "This report computes inter-reviewer reliability when independent human labels are present. The current repository state keeps the metrics unavailable when no human labels have been collected.",
        "",
        markdown_table(
            ["Metric", "Label field", "Records", "Value", "Status"],
            [
                [
                    row["metric"],
                    row["label_field"],
                    str(row["records_available"]),
                    row["value"],
                    row["analysis_status"],
                ]
                for row in rows
            ],
        ),
        "",
    ]
    RELIABILITY_MD_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    source_rows = read_csv_rows(WORKLIST_PATH)
    rows = reliability_rows(source_rows)
    write_csv(RELIABILITY_PATH, RELIABILITY_COLUMNS, rows)
    write_summary(rows)
    print(f"Wrote {RELIABILITY_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {RELIABILITY_MD_PATH.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
