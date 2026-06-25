from __future__ import annotations

import csv
import json
import math
import random
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
RESULTS_EXPERIMENTS_DIR = REPO_ROOT / "results" / "experiments"
RAW_RESULTS_DIR = RESULTS_EXPERIMENTS_DIR / "raw"

PRIMARY_EFFECTS_PATH = RESULTS_EXPERIMENTS_DIR / "external_primary_effects.csv"
F1_BOOTSTRAP_PATH = RESULTS_EXPERIMENTS_DIR / "external_f1_bootstrap.csv"
MCNEMAR_PATH = RESULTS_EXPERIMENTS_DIR / "external_mcnemar.csv"
ANNOTATION_RELIABILITY_PATH = RESULTS_EXPERIMENTS_DIR / "external_annotation_reliability.csv"
EXCLUSIONS_PATH = RESULTS_EXPERIMENTS_DIR / "external_exclusions.csv"
SUMMARY_MD_PATH = RESULTS_EXPERIMENTS_DIR / "external_statistical_analysis.md"

PRIMARY_COLUMNS = [
    "contrast",
    "provider_model",
    "paired_units",
    "condition_a_rate",
    "condition_b_rate",
    "risk_difference",
    "analysis_status",
    "notes",
]

BOOTSTRAP_COLUMNS = [
    "condition",
    "provider_model",
    "clusters",
    "records",
    "behavior_match_rate",
    "bootstrap_replicates",
    "ci_low",
    "ci_high",
    "analysis_status",
]

MCNEMAR_COLUMNS = [
    "contrast",
    "provider_model",
    "paired_units",
    "b_condition_a_correct_only",
    "c_condition_b_correct_only",
    "statistic",
    "approx_p_value",
    "analysis_status",
]

ANNOTATION_COLUMNS = [
    "metric",
    "records_available",
    "analysis_status",
    "notes",
]

EXCLUSION_COLUMNS = [
    "group",
    "value",
    "metric",
    "count",
    "notes",
]

CONTRASTS = [
    ("skillops_normalized_vs_original_freeform", "skillops_normalized", "original_freeform"),
    ("skillops_normalized_vs_skillops_ablation", "skillops_normalized", "skillops_ablation"),
]


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            records.append(json.loads(line))
    return records


def external_result_files() -> list[Path]:
    return sorted(RAW_RESULTS_DIR.glob("external_condition_*.jsonl"))


def load_records() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for path in external_result_files():
        records.extend(read_jsonl(path))
    return records


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def provider_model(record: dict[str, Any]) -> str:
    return f"{record.get('provider', '')}::{record.get('model', '')}"


def behavior_correct(record: dict[str, Any]) -> bool:
    return record.get("predicted_behavior") == record.get("expected_behavior")


def format_float(value: float | None) -> str:
    if value is None or math.isnan(value):
        return ""
    return f"{value:.6f}"


def paired_records(records: list[dict[str, Any]], condition_a: str, condition_b: str, model_key: str) -> list[tuple[dict[str, Any], dict[str, Any]]]:
    by_unit: dict[tuple[str, str], dict[str, dict[str, Any]]] = {}
    for record in records:
        if provider_model(record) != model_key:
            continue
        key = (str(record.get("case_id", "")), provider_model(record))
        by_unit.setdefault(key, {})[str(record.get("condition", ""))] = record
    pairs: list[tuple[dict[str, Any], dict[str, Any]]] = []
    for unit_records in by_unit.values():
        if condition_a in unit_records and condition_b in unit_records:
            pairs.append((unit_records[condition_a], unit_records[condition_b]))
    return pairs


def build_primary_effects(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not records:
        return [
            {
                "contrast": "all",
                "provider_model": "all",
                "paired_units": 0,
                "condition_a_rate": "",
                "condition_b_rate": "",
                "risk_difference": "",
                "analysis_status": "no_results",
                "notes": "No external result records are available.",
            }
        ]

    rows: list[dict[str, Any]] = []
    for model_key in sorted({provider_model(record) for record in records}):
        for contrast, condition_a, condition_b in CONTRASTS:
            pairs = paired_records(records, condition_a, condition_b, model_key)
            if not pairs:
                rows.append(
                    {
                        "contrast": contrast,
                        "provider_model": model_key,
                        "paired_units": 0,
                        "condition_a_rate": "",
                        "condition_b_rate": "",
                        "risk_difference": "",
                        "analysis_status": "insufficient_pairs",
                        "notes": "No paired units contain both contrast conditions.",
                    }
                )
                continue
            a_hits = sum(1 for condition_a_record, _ in pairs if behavior_correct(condition_a_record))
            b_hits = sum(1 for _, condition_b_record in pairs if behavior_correct(condition_b_record))
            a_rate = a_hits / len(pairs)
            b_rate = b_hits / len(pairs)
            rows.append(
                {
                    "contrast": contrast,
                    "provider_model": model_key,
                    "paired_units": len(pairs),
                    "condition_a_rate": format_float(a_rate),
                    "condition_b_rate": format_float(b_rate),
                    "risk_difference": format_float(a_rate - b_rate),
                    "analysis_status": "descriptive_only",
                    "notes": "Paired descriptive contrast; not a powered inferential result.",
                }
            )
    return rows


def percentile(values: list[float], quantile: float) -> float:
    if not values:
        return math.nan
    ordered = sorted(values)
    index = (len(ordered) - 1) * quantile
    lower = math.floor(index)
    upper = math.ceil(index)
    if lower == upper:
        return ordered[lower]
    return ordered[lower] * (upper - index) + ordered[upper] * (index - lower)


def bootstrap_rate(records: list[dict[str, Any]], replicates: int = 400, seed: int = 20260625) -> tuple[int, float, float]:
    clusters: dict[str, list[dict[str, Any]]] = {}
    for record in records:
        clusters.setdefault(str(record.get("artifact_id", "")), []).append(record)
    cluster_ids = sorted(clusters)
    if not cluster_ids:
        return 0, math.nan, math.nan
    rng = random.Random(seed)
    rates: list[float] = []
    for _ in range(replicates):
        sampled_records: list[dict[str, Any]] = []
        for _ in cluster_ids:
            sampled_records.extend(clusters[rng.choice(cluster_ids)])
        rates.append(sum(1 for record in sampled_records if behavior_correct(record)) / len(sampled_records))
    return len(cluster_ids), percentile(rates, 0.025), percentile(rates, 0.975)


def build_bootstrap_rows(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not records:
        return [
            {
                "condition": "all",
                "provider_model": "all",
                "clusters": 0,
                "records": 0,
                "behavior_match_rate": "",
                "bootstrap_replicates": 0,
                "ci_low": "",
                "ci_high": "",
                "analysis_status": "no_results",
            }
        ]

    rows: list[dict[str, Any]] = []
    for model_key in sorted({provider_model(record) for record in records}):
        for condition in sorted({str(record.get("condition", "")) for record in records}):
            subset = [record for record in records if provider_model(record) == model_key and record.get("condition") == condition]
            if not subset:
                continue
            clusters, ci_low, ci_high = bootstrap_rate(subset)
            match_rate = sum(1 for record in subset if behavior_correct(record)) / len(subset)
            rows.append(
                {
                    "condition": condition,
                    "provider_model": model_key,
                    "clusters": clusters,
                    "records": len(subset),
                    "behavior_match_rate": format_float(match_rate),
                    "bootstrap_replicates": 400,
                    "ci_low": format_float(ci_low),
                    "ci_high": format_float(ci_high),
                    "analysis_status": "descriptive_cluster_bootstrap",
                }
            )
    return rows


def mcnemar_p_value(statistic: float | None) -> str:
    if statistic is None:
        return ""
    return format_float(math.erfc(math.sqrt(statistic / 2)))


def build_mcnemar_rows(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not records:
        return [
            {
                "contrast": "all",
                "provider_model": "all",
                "paired_units": 0,
                "b_condition_a_correct_only": 0,
                "c_condition_b_correct_only": 0,
                "statistic": "",
                "approx_p_value": "",
                "analysis_status": "no_results",
            }
        ]

    rows: list[dict[str, Any]] = []
    for model_key in sorted({provider_model(record) for record in records}):
        for contrast, condition_a, condition_b in CONTRASTS:
            pairs = paired_records(records, condition_a, condition_b, model_key)
            b_count = sum(1 for a_record, b_record in pairs if behavior_correct(a_record) and not behavior_correct(b_record))
            c_count = sum(1 for a_record, b_record in pairs if not behavior_correct(a_record) and behavior_correct(b_record))
            statistic: float | None = None
            if b_count + c_count > 0:
                statistic = (abs(b_count - c_count) - 1) ** 2 / (b_count + c_count)
            if not pairs:
                status = "insufficient_pairs"
            elif b_count + c_count == 0:
                status = "no_discordant_pairs"
            else:
                status = "descriptive_mcnemar"
            rows.append(
                {
                    "contrast": contrast,
                    "provider_model": model_key,
                    "paired_units": len(pairs),
                    "b_condition_a_correct_only": b_count,
                    "c_condition_b_correct_only": c_count,
                    "statistic": format_float(statistic),
                    "approx_p_value": mcnemar_p_value(statistic),
                    "analysis_status": status,
                }
            )
    return rows


def build_annotation_rows(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    annotation_fields = {"annotator_a_label", "annotator_b_label", "adjudicated_label"}
    annotated_records = [record for record in records if annotation_fields & set(record)]
    return [
        {
            "metric": "annotation_reliability",
            "records_available": len(annotated_records),
            "analysis_status": "not_available" if not annotated_records else "requires_reliability_estimator",
            "notes": "External live records do not include independent human annotation fields yet."
            if not annotated_records
            else "Annotation fields detected; compute agreement before reporting study outcomes.",
        }
    ]


def build_exclusion_rows(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    failed = [record for record in records if record.get("run_status") != "completed"]
    parse_failures = [record for record in records if not bool(record.get("parse_success"))]
    rows.append(
        {
            "group": "overall",
            "value": "run_status_not_completed",
            "metric": "count",
            "count": len(failed),
            "notes": "Rows with provider or execution failure.",
        }
    )
    rows.append(
        {
            "group": "overall",
            "value": "parse_failure",
            "metric": "count",
            "count": len(parse_failures),
            "notes": "Rows with invalid or unparseable model output.",
        }
    )
    for record in failed + parse_failures:
        rows.append(
            {
                "group": "condition_case_id",
                "value": record.get("condition_case_id", ""),
                "metric": "excluded_or_failed_record",
                "count": 1,
                "notes": str(record.get("error_type", "")),
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


def write_markdown(records: list[dict[str, Any]], primary_rows: list[dict[str, Any]], mcnemar_rows: list[dict[str, Any]]) -> None:
    lines = [
        "# External Statistical Analysis",
        "",
        "This report computes descriptive paired contrasts and robustness-ready tables from external live-result records. It does not claim statistical significance unless a full annotated external run is present.",
        "",
        "## Record State",
        "",
        markdown_table(
            ["Quantity", "Count"],
            [
                ["External records", str(len(records))],
                ["Provider/model groups", str(len({provider_model(record) for record in records})) if records else "0"],
                ["Artifacts", str(len({str(record.get("artifact_id", "")) for record in records})) if records else "0"],
            ],
        ),
        "",
        "## Primary Contrasts",
        "",
        markdown_table(
            ["Contrast", "Provider/model", "Pairs", "Risk difference", "Status"],
            [
                [
                    row["contrast"],
                    row["provider_model"],
                    str(row["paired_units"]),
                    row["risk_difference"],
                    row["analysis_status"],
                ]
                for row in primary_rows
            ],
        ),
        "",
        "## McNemar Diagnostics",
        "",
        markdown_table(
            ["Contrast", "Provider/model", "Pairs", "Statistic", "Approx p", "Status"],
            [
                [
                    row["contrast"],
                    row["provider_model"],
                    str(row["paired_units"]),
                    row["statistic"],
                    row["approx_p_value"],
                    row["analysis_status"],
                ]
                for row in mcnemar_rows
            ],
        ),
        "",
    ]
    SUMMARY_MD_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    records = load_records()
    primary_rows = build_primary_effects(records)
    bootstrap_rows = build_bootstrap_rows(records)
    mcnemar_rows = build_mcnemar_rows(records)
    annotation_rows = build_annotation_rows(records)
    exclusion_rows = build_exclusion_rows(records)

    write_csv(PRIMARY_EFFECTS_PATH, PRIMARY_COLUMNS, primary_rows)
    write_csv(F1_BOOTSTRAP_PATH, BOOTSTRAP_COLUMNS, bootstrap_rows)
    write_csv(MCNEMAR_PATH, MCNEMAR_COLUMNS, mcnemar_rows)
    write_csv(ANNOTATION_RELIABILITY_PATH, ANNOTATION_COLUMNS, annotation_rows)
    write_csv(EXCLUSIONS_PATH, EXCLUSION_COLUMNS, exclusion_rows)
    write_markdown(records, primary_rows, mcnemar_rows)

    print(f"Wrote {PRIMARY_EFFECTS_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {F1_BOOTSTRAP_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {MCNEMAR_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {ANNOTATION_RELIABILITY_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {EXCLUSIONS_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {SUMMARY_MD_PATH.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
