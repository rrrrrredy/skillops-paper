from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = REPO_ROOT / "benchmark" / "risk_cases.csv"
OUTPUT_DIR = REPO_ROOT / "results" / "tables"
MARKDOWN_OUTPUT = OUTPUT_DIR / "risk_summary.md"
CSV_OUTPUT = OUTPUT_DIR / "risk_summary.csv"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def markdown_table(headers: list[str], rows: list[list[str]]) -> str:
    header_row = "| " + " | ".join(headers) + " |"
    separator_row = "| " + " | ".join(["---"] * len(headers)) + " |"
    body_rows = ["| " + " | ".join(row) + " |" for row in rows]
    return "\n".join([header_row, separator_row, *body_rows])


def write_csv(path: Path, risk_counts: Counter[str], artifact_counts: Counter[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["group", "value", "count"])
        for risk_type, count in risk_counts.items():
            writer.writerow(["risk_type", risk_type, count])
        for artifact, count in artifact_counts.items():
            writer.writerow(["relevant_artifact", artifact, count])


def write_markdown(path: Path, rows: list[dict[str, str]], risk_counts: Counter[str], artifact_counts: Counter[str]) -> None:
    manual_prefix_count = sum(1 for row in rows if row["case_id"].startswith("manual-"))
    risk_table_rows = [[risk_type, str(count)] for risk_type, count in risk_counts.items()]
    artifact_table_rows = [[artifact, str(count)] for artifact, count in artifact_counts.items()]
    markdown = "\n".join(
        [
            "# Risk Case Summary",
            "",
            "This summary is generated from `benchmark/risk_cases.csv`, which is a",
            "manually constructed operational risk benchmark input.",
            "",
            "The counts below describe the benchmark inventory only. They are not model",
            "detection scores, significance claims, or broad empirical validation.",
            "",
            "## Input Summary",
            "",
            f"- Total cases: {len(rows)}",
            f"- Case IDs with the `manual-` prefix: {manual_prefix_count}",
            f"- Distinct risk types: {len(risk_counts)}",
            f"- Distinct relevant artifact values: {len(artifact_counts)}",
            "",
            "## Counts by Risk Type",
            "",
            markdown_table(["Risk Type", "Count"], risk_table_rows),
            "",
            "## Counts by Relevant Artifact",
            "",
            markdown_table(["Relevant Artifact", "Count"], artifact_table_rows),
            "",
            "## Limitations",
            "",
            "- Every case is manually written from repository inspection rather than observed incidents.",
            "- The summary does not estimate real-world prevalence or detector performance.",
            "- The table should be read as a benchmark-design inventory for later evaluation.",
            "",
        ]
    )
    path.write_text(markdown + "\n", encoding="utf-8")


def main() -> dict[str, object]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    rows = read_rows(INPUT_PATH)
    risk_counts = Counter(row["risk_type"] for row in rows)
    artifact_counts = Counter(row["relevant_artifact"] for row in rows)
    write_csv(CSV_OUTPUT, risk_counts, artifact_counts)
    write_markdown(MARKDOWN_OUTPUT, rows, risk_counts, artifact_counts)
    outputs = [str(MARKDOWN_OUTPUT), str(CSV_OUTPUT)]
    print("Generated risk case outputs:")
    for output in outputs:
        print(output)
    return {"outputs": outputs}


if __name__ == "__main__":
    main()
