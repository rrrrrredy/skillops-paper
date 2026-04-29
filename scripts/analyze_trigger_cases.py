from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = REPO_ROOT / "benchmark" / "trigger_cases.csv"
OUTPUT_DIR = REPO_ROOT / "results" / "tables"
MARKDOWN_OUTPUT = OUTPUT_DIR / "trigger_summary.md"
CSV_OUTPUT = OUTPUT_DIR / "trigger_summary.csv"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def markdown_table(headers: list[str], rows: list[list[str]]) -> str:
    header_row = "| " + " | ".join(headers) + " |"
    separator_row = "| " + " | ".join(["---"] * len(headers)) + " |"
    body_rows = ["| " + " | ".join(row) + " |" for row in rows]
    return "\n".join([header_row, separator_row, *body_rows])


def write_csv(path: Path, label_counts: Counter[str], skill_counts: Counter[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["group", "value", "count"])
        for label, count in label_counts.items():
            writer.writerow(["expected_label", label, count])
        for skill, count in skill_counts.items():
            writer.writerow(["relevant_skill", skill, count])


def write_markdown(path: Path, rows: list[dict[str, str]], label_counts: Counter[str], skill_counts: Counter[str]) -> None:
    manual_prefix_count = sum(1 for row in rows if row["case_id"].startswith("manual-"))
    label_table_rows = [[label, str(count)] for label, count in label_counts.items()]
    skill_table_rows = [[skill, str(count)] for skill, count in skill_counts.items()]
    markdown = "\n".join(
        [
            "# Trigger Case Summary",
            "",
            "This summary is generated from `benchmark/trigger_cases.csv`, which is a",
            "manually constructed trigger-routing benchmark input.",
            "",
            "The counts below describe benchmark case composition only. They are not",
            "model accuracy results and should not be interpreted as broad validation or",
            "statistical significance.",
            "",
            "## Input Summary",
            "",
            f"- Total cases: {len(rows)}",
            f"- Case IDs with the `manual-` prefix: {manual_prefix_count}",
            f"- Distinct expected labels: {len(label_counts)}",
            f"- Distinct relevant skill values: {len(skill_counts)}",
            "",
            "## Counts by Expected Label",
            "",
            markdown_table(["Expected Label", "Count"], label_table_rows),
            "",
            "## Counts by Relevant Skill",
            "",
            markdown_table(["Relevant Skill", "Count"], skill_table_rows),
            "",
            "## Limitations",
            "",
            "- Every case is a manually constructed example rather than an observed user log.",
            "- The summary does not measure routing quality until a later execution layer is added.",
            "- `none` denotes cases that should not route to one of the inspected skills.",
            "",
        ]
    )
    path.write_text(markdown + "\n", encoding="utf-8")


def main() -> dict[str, object]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    rows = read_rows(INPUT_PATH)
    label_counts = Counter(row["expected_label"] for row in rows)
    skill_counts = Counter(row["relevant_skill"] for row in rows)
    write_csv(CSV_OUTPUT, label_counts, skill_counts)
    write_markdown(MARKDOWN_OUTPUT, rows, label_counts, skill_counts)
    outputs = [str(MARKDOWN_OUTPUT), str(CSV_OUTPUT)]
    print("Generated trigger case outputs:")
    for output in outputs:
        print(output)
    return {"outputs": outputs}


if __name__ == "__main__":
    main()
