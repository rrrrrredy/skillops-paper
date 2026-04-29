from __future__ import annotations

import csv
import re
from collections import defaultdict
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_SAMPLES_PATH = REPO_ROOT / "benchmark" / "skill_samples.csv"
INVENTORY_PATH = REPO_ROOT / "artifacts" / "artifact_inventory.md"
OUTPUT_DIR = REPO_ROOT / "results" / "tables"
MARKDOWN_OUTPUT = OUTPUT_DIR / "artifact_coverage.md"
CSV_OUTPUT = OUTPUT_DIR / "artifact_coverage.csv"

COMPONENTS = [
    ("metadata", "Metadata"),
    ("trigger_contract", "Trigger Contract"),
    ("instructions", "Instructions"),
    ("context_boundary", "Context Boundary"),
    ("execution_constraints", "Execution Constraints"),
    ("memory_interface", "Memory Interface"),
    ("tests", "Tests"),
    ("security_checks", "Security Checks"),
    ("failure_modes", "Failure Modes"),
]

LIMITED_PATTERNS = {
    "memory_interface": [
        re.compile(r"\bno persistent\b", re.IGNORECASE),
        re.compile(r"\bno standalone memory store\b", re.IGNORECASE),
        re.compile(r"\bno persistent store of its own\b", re.IGNORECASE),
    ],
    "tests": [
        re.compile(r"\bno executable regression corpus\b", re.IGNORECASE),
        re.compile(r"\bno executable test harness\b", re.IGNORECASE),
    ],
}


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def parse_inventory(path: Path) -> tuple[str, list[str]]:
    text = path.read_text(encoding="utf-8")
    date_match = re.search(r"^Date:\s*(.+)$", text, re.MULTILINE)
    inventory_date = date_match.group(1).strip() if date_match else "unknown"
    artifact_sections = []
    for line in text.splitlines():
        if not line.startswith("## "):
            continue
        heading = line[3:].strip()
        if heading in {"Summary", "Access Note"}:
            continue
        artifact_sections.append(heading)
    return inventory_date, artifact_sections


def classify_component(component: str, value: str) -> str:
    text = value.strip()
    if not text:
        return "absent"
    for pattern in LIMITED_PATTERNS.get(component, []):
        if pattern.search(text):
            return "limited"
    return "documented"


def markdown_table(headers: list[str], rows: list[list[str]]) -> str:
    header_row = "| " + " | ".join(headers) + " |"
    separator_row = "| " + " | ".join(["---"] * len(headers)) + " |"
    body_rows = ["| " + " | ".join(row) + " |" for row in rows]
    return "\n".join([header_row, separator_row, *body_rows])


def build_component_summary(rows: list[dict[str, str]]) -> tuple[list[dict[str, object]], list[dict[str, str]]]:
    component_summary = []
    matrix_rows = []

    for artifact_row in rows:
        matrix_row = {"artifact_name": artifact_row["artifact_name"]}
        for component_key, component_label in COMPONENTS:
            status = classify_component(component_key, artifact_row[component_key])
            matrix_row[component_key] = status
        matrix_rows.append(matrix_row)

    for component_key, component_label in COMPONENTS:
        grouped_names: dict[str, list[str]] = defaultdict(list)
        for matrix_row in matrix_rows:
            grouped_names[matrix_row[component_key]].append(matrix_row["artifact_name"])
        component_summary.append(
            {
                "component_key": component_key,
                "component_label": component_label,
                "documented_count": len(grouped_names["documented"]),
                "limited_count": len(grouped_names["limited"]),
                "absent_count": len(grouped_names["absent"]),
                "documented_artifacts": grouped_names["documented"],
                "limited_artifacts": grouped_names["limited"],
                "absent_artifacts": grouped_names["absent"],
            }
        )

    return component_summary, matrix_rows


def write_csv(path: Path, component_summary: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "component",
                "documented_count",
                "limited_count",
                "absent_count",
                "documented_artifacts",
                "limited_artifacts",
                "absent_artifacts",
            ]
        )
        for item in component_summary:
            writer.writerow(
                [
                    item["component_key"],
                    item["documented_count"],
                    item["limited_count"],
                    item["absent_count"],
                    "; ".join(item["documented_artifacts"]),
                    "; ".join(item["limited_artifacts"]),
                    "; ".join(item["absent_artifacts"]),
                ]
            )


def write_markdown(
    path: Path,
    inventory_date: str,
    inventory_artifacts: list[str],
    rows: list[dict[str, str]],
    component_summary: list[dict[str, object]],
    matrix_rows: list[dict[str, str]],
) -> None:
    csv_artifact_names = [row["artifact_name"] for row in rows]
    inventory_match = set(csv_artifact_names) == set(inventory_artifacts)

    summary_rows = []
    for item in component_summary:
        summary_rows.append(
            [
                item["component_label"],
                str(item["documented_count"]),
                str(item["limited_count"]),
                str(item["absent_count"]),
                ", ".join(item["documented_artifacts"]) or "-",
                ", ".join(item["limited_artifacts"]) or "-",
            ]
        )

    matrix_table_rows = []
    for matrix_row in matrix_rows:
        matrix_table_rows.append(
            [
                matrix_row["artifact_name"],
                *[matrix_row[component_key] for component_key, _ in COMPONENTS],
            ]
        )

    markdown = "\n".join(
        [
            "# Artifact Coverage Summary",
            "",
            "This table summarizes manually constructed artifact profiles derived from",
            "`benchmark/skill_samples.csv` and cross-checked against",
            "`artifacts/artifact_inventory.md`.",
            "",
            "The counts below are descriptive summaries of inspected artifacts, not",
            "executed model results, statistical tests, or broad empirical validation.",
            "",
            "## Input Summary",
            "",
            f"- Inventory date: {inventory_date}",
            f"- Artifact rows in `skill_samples.csv`: {len(rows)}",
            f"- Artifact sections in `artifact_inventory.md`: {len(inventory_artifacts)}",
            f"- Artifact names aligned across the two inputs: {'yes' if inventory_match else 'no'}",
            "",
            "## Classification Rule",
            "",
            "- `documented`: the CSV field contains a concrete description of the component.",
            "- `limited`: the field explicitly says the artifact lacks a standalone",
            "  implementation or executable harness for that component.",
            "- `absent`: the field is blank.",
            "",
            "## Component-Level Coverage",
            "",
            markdown_table(
                [
                    "Component",
                    "Documented",
                    "Limited",
                    "Absent",
                    "Documented Artifacts",
                    "Limited Artifacts",
                ],
                summary_rows,
            ),
            "",
            "## Artifact-Level Coverage Matrix",
            "",
            markdown_table(
                ["Artifact", *[label for _, label in COMPONENTS]],
                matrix_table_rows,
            ),
            "",
            "## Limitations",
            "",
            "- These summaries come from manually constructed benchmark inputs.",
            "- The component labels reflect descriptive coding of repository summaries,",
            "  not direct execution evidence.",
            "- The table should be read as traceability support for the paper, not as",
            "  statistical validation.",
            "",
        ]
    )
    path.write_text(markdown + "\n", encoding="utf-8")


def main() -> dict[str, object]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    rows = read_csv_rows(SKILL_SAMPLES_PATH)
    inventory_date, inventory_artifacts = parse_inventory(INVENTORY_PATH)
    component_summary, matrix_rows = build_component_summary(rows)
    write_csv(CSV_OUTPUT, component_summary)
    write_markdown(
        MARKDOWN_OUTPUT,
        inventory_date,
        inventory_artifacts,
        rows,
        component_summary,
        matrix_rows,
    )
    outputs = [str(MARKDOWN_OUTPUT), str(CSV_OUTPUT)]
    print("Generated artifact coverage outputs:")
    for output in outputs:
        print(output)
    return {"outputs": outputs}


if __name__ == "__main__":
    main()
