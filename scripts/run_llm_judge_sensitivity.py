from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = Path(__file__).resolve().parent

if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from experiment_utils import (  # noqa: E402
    RAW_RESULTS_DIR,
    RESULTS_DIR,
    call_model,
    ensure_directories,
    filename_timestamp,
    parse_json_object,
    read_text,
    render_prompt_template,
    resolve_provider_config,
    write_csv_rows,
    write_jsonl,
)


CALIBRATION_PATH = REPO_ROOT / "results" / "tables" / "external_pilot_annotation_calibration.csv"
WORKLIST_PATH = REPO_ROOT / "results" / "tables" / "external_pilot_annotation_worklist.csv"
PROMPT_PATH = REPO_ROOT / "experiments" / "prompts" / "llm_judge_case_label_sensitivity.md"

PLAN_CSV_PATH = RESULTS_DIR / "llm_judge_sensitivity_plan.csv"
PLAN_MD_PATH = RESULTS_DIR / "llm_judge_sensitivity_plan.md"
SUMMARY_CSV_PATH = RESULTS_DIR / "llm_judge_sensitivity_summary.csv"
SUMMARY_MD_PATH = RESULTS_DIR / "llm_judge_sensitivity_summary.md"

MAX_DEFAULT_LIVE_ROWS = 32

ALLOWED_EXPECTED_BEHAVIORS = {
    "trigger",
    "no_trigger",
    "clarify_scope",
    "apply_constraint_or_refuse",
    "ambiguous",
}

ALLOWED_RISK_LABELS = {
    "none",
    "permission_boundary",
    "execution_constraint",
    "privacy",
    "irreversible_action",
    "ambiguous",
}

PLAN_COLUMNS = [
    "case_id",
    "artifact_id",
    "study_family",
    "source_id",
    "case_type",
    "expected_behavior_author",
    "risk_label_author",
    "provider",
    "model",
    "run_status",
    "prompt_hash",
    "evidence_role",
]

SUMMARY_COLUMNS = [
    "metric",
    "provider",
    "model",
    "numerator",
    "denominator",
    "rate",
    "status",
    "notes",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Prepare or run LLM-as-judge case-label sensitivity checks.")
    parser.add_argument("--dry-run", action="store_true", help="Write a not-run sensitivity plan.")
    parser.add_argument("--run-live", action="store_true", help="Run a bounded provider-backed sensitivity slice.")
    parser.add_argument("--provider", choices=["openai", "anthropic", "deepseek", "moonshot", "kimi"], help="Provider for live judging.")
    parser.add_argument("--model", help="Optional model override.")
    parser.add_argument("--sample", choices=["calibration", "worklist"], default="calibration")
    parser.add_argument("--sample-limit", type=int, default=32, help="Maximum cases selected from the chosen sample.")
    parser.add_argument("--max-live-rows", type=int, default=MAX_DEFAULT_LIVE_ROWS)
    return parser.parse_args()


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}")
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def select_rows(sample: str, sample_limit: int | None) -> list[dict[str, str]]:
    source_path = CALIBRATION_PATH if sample == "calibration" else WORKLIST_PATH
    rows = read_csv_rows(source_path)
    if sample_limit is not None:
        if sample_limit < 1:
            raise ValueError("sample-limit must be positive")
        rows = rows[:sample_limit]
    return rows


def render_prompt(row: dict[str, str]) -> str:
    template = read_text(PROMPT_PATH)
    return render_prompt_template(
        template,
        {
            "CASE_ID": row["case_id"],
            "ARTIFACT_ID": row["artifact_id"],
            "STUDY_FAMILY": row["study_family"],
            "SOURCE_ID": row["source_id"],
            "ARTIFACT_REFERENCE": row["artifact_reference"],
            "CASE_TYPE": row["case_type"],
            "SEED_REQUEST": row["protocol_seed_request"],
            "EXPECTED_BEHAVIOR": row["expected_behavior"],
            "RISK_LABEL": row["risk_label"],
        },
    )


def build_plan_rows(rows: list[dict[str, str]], provider: str | None, model: str | None, run_status: str) -> list[dict[str, Any]]:
    plan_rows: list[dict[str, Any]] = []
    for row in rows:
        prompt = render_prompt(row)
        plan_rows.append(
            {
                "case_id": row["case_id"],
                "artifact_id": row["artifact_id"],
                "study_family": row["study_family"],
                "source_id": row["source_id"],
                "case_type": row["case_type"],
                "expected_behavior_author": row["expected_behavior"],
                "risk_label_author": row["risk_label"],
                "provider": provider or "",
                "model": model or "",
                "run_status": run_status,
                "prompt_hash": sha256_text(prompt),
                "evidence_role": "secondary_label_sensitivity",
            }
        )
    return plan_rows


def normalize_judge_result(row: dict[str, str], provider: str, model: str, parsed: Any, prompt_hash: str, run_status: str, error_type: str = "") -> dict[str, Any]:
    expected_behavior = ""
    risk_label = ""
    confidence = ""
    rationale = ""
    parse_success = False
    if isinstance(parsed, dict):
        expected_behavior = str(parsed.get("expected_behavior", "")).strip()
        risk_label = str(parsed.get("risk_label", "")).strip()
        confidence = str(parsed.get("confidence", "")).strip()
        rationale = str(parsed.get("rationale", "")).strip()
        parse_success = (
            expected_behavior in ALLOWED_EXPECTED_BEHAVIORS
            and risk_label in ALLOWED_RISK_LABELS
            and confidence in {"low", "medium", "high"}
        )
        if not parse_success and not error_type:
            error_type = "invalid_judge_schema"
    elif not error_type:
        error_type = "parse_failure"

    return {
        "case_id": row["case_id"],
        "artifact_id": row["artifact_id"],
        "study_family": row["study_family"],
        "source_id": row["source_id"],
        "case_type": row["case_type"],
        "provider": provider,
        "model": model,
        "run_status": run_status,
        "parse_success": parse_success,
        "expected_behavior_author": row["expected_behavior"],
        "expected_behavior_judge": expected_behavior,
        "expected_behavior_match": parse_success and expected_behavior == row["expected_behavior"],
        "risk_label_author": row["risk_label"],
        "risk_label_judge": risk_label,
        "risk_label_match": parse_success and risk_label == row["risk_label"],
        "confidence": confidence,
        "rationale": rationale[:240],
        "prompt_hash": prompt_hash,
        "error_type": error_type,
        "evidence_role": "secondary_label_sensitivity",
    }


def rate(numerator: int, denominator: int) -> str:
    if denominator == 0:
        return ""
    return f"{numerator / denominator:.6f}"


def summary_row(metric: str, provider: str, model: str, numerator: int, denominator: int, status: str, notes: str = "") -> dict[str, Any]:
    return {
        "metric": metric,
        "provider": provider,
        "model": model,
        "numerator": numerator,
        "denominator": denominator,
        "rate": rate(numerator, denominator),
        "status": status,
        "notes": notes,
    }


def build_summary_rows(records: list[dict[str, Any]], provider: str = "", model: str = "", status: str = "not_run") -> list[dict[str, Any]]:
    if not records:
        return [
            summary_row(
                "llm_judge_case_label_sensitivity",
                provider,
                model,
                0,
                0,
                status,
                "No provider-backed judge records are available.",
            )
        ]
    return [
        summary_row(
            "judge_parse_success_rate",
            provider,
            model,
            sum(1 for record in records if bool(record["parse_success"])),
            len(records),
            "secondary_sensitivity",
        ),
        summary_row(
            "expected_behavior_label_match_rate",
            provider,
            model,
            sum(1 for record in records if bool(record["expected_behavior_match"])),
            len(records),
            "secondary_sensitivity",
            "Agreement between authored case label and provider judge label.",
        ),
        summary_row(
            "risk_label_match_rate",
            provider,
            model,
            sum(1 for record in records if bool(record["risk_label_match"])),
            len(records),
            "secondary_sensitivity",
            "Agreement between authored risk label and provider judge label.",
        ),
    ]


def markdown_table(headers: list[str], rows: list[list[str]]) -> str:
    return "\n".join(
        [
            "| " + " | ".join(headers) + " |",
            "| " + " | ".join(["---"] * len(headers)) + " |",
            *["| " + " | ".join(row) + " |" for row in rows],
        ]
    )


def write_plan_markdown(plan_rows: list[dict[str, Any]]) -> None:
    PLAN_MD_PATH.write_text(
        "\n".join(
            [
                "# LLM-as-Judge Sensitivity Plan",
                "",
                "This plan checks whether preregistered external case labels are stable under a bounded provider-backed judge. It is a secondary sensitivity analysis and does not provide primary model outcome labels.",
                "",
                markdown_table(
                    ["Cases", "Run status", "Evidence role"],
                    [[str(len(plan_rows)), plan_rows[0]["run_status"] if plan_rows else "not_run", "secondary_label_sensitivity"]],
                ),
                "",
            ]
        ),
        encoding="utf-8",
    )


def write_summary_markdown(summary_rows: list[dict[str, Any]]) -> None:
    SUMMARY_MD_PATH.write_text(
        "\n".join(
            [
                "# LLM-as-Judge Sensitivity Summary",
                "",
                "LLM-as-judge results, when present, audit case-label stability only. Primary external-smoke metrics remain machine-checkable parse, behavior-match, and constraint-pass rules.",
                "",
                markdown_table(
                    ["Metric", "Count", "Rate", "Status"],
                    [
                        [
                            row["metric"],
                            f"{row['numerator']}/{row['denominator']}",
                            row["rate"],
                            row["status"],
                        ]
                        for row in summary_rows
                    ],
                ),
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> int:
    args = parse_args()
    if not args.dry_run and not args.run_live:
        args.dry_run = True
    if args.dry_run and args.run_live:
        raise ValueError("Use either --dry-run or --run-live, not both")
    if args.max_live_rows < 1:
        raise ValueError("max-live-rows must be positive")

    selected = select_rows(args.sample, args.sample_limit)
    provider = args.provider or ""
    model = args.model or ""

    if args.dry_run:
        plan_rows = build_plan_rows(selected, provider, model, "not_run_case_label_sensitivity")
        write_csv_rows(PLAN_CSV_PATH, PLAN_COLUMNS, plan_rows)
        write_plan_markdown(plan_rows)
        summary_rows = build_summary_rows([], provider, model, "not_run_case_label_sensitivity")
        write_csv_rows(SUMMARY_CSV_PATH, SUMMARY_COLUMNS, summary_rows)
        write_summary_markdown(summary_rows)
        for path in (PLAN_CSV_PATH, PLAN_MD_PATH, SUMMARY_CSV_PATH, SUMMARY_MD_PATH):
            print(f"Wrote {path.relative_to(REPO_ROOT)}")
        return 0

    if args.provider is None:
        raise ValueError("Live LLM-as-judge sensitivity requires --provider")
    if args.sample_limit is None:
        raise ValueError("Live LLM-as-judge sensitivity requires --sample-limit")
    if len(selected) > args.max_live_rows:
        raise ValueError(f"Refusing to run {len(selected)} rows; max-live-rows is {args.max_live_rows}")

    config, reason = resolve_provider_config(args.provider, args.model)
    if config is None:
        plan_rows = build_plan_rows(selected, args.provider, args.model or "", "not_run_missing_credentials")
        write_csv_rows(PLAN_CSV_PATH, PLAN_COLUMNS, plan_rows)
        write_plan_markdown(plan_rows)
        summary_rows = build_summary_rows([], args.provider, args.model or "", "not_run_missing_credentials")
        write_csv_rows(SUMMARY_CSV_PATH, SUMMARY_COLUMNS, summary_rows)
        write_summary_markdown(summary_rows)
        print(reason)
        for path in (PLAN_CSV_PATH, PLAN_MD_PATH, SUMMARY_CSV_PATH, SUMMARY_MD_PATH):
            print(f"Wrote {path.relative_to(REPO_ROOT)}")
        return 0

    ensure_directories([RAW_RESULTS_DIR])
    output_path = RAW_RESULTS_DIR / f"llm_judge_sensitivity_{filename_timestamp()}.jsonl"
    records: list[dict[str, Any]] = []
    for row in selected:
        prompt = render_prompt(row)
        prompt_hash = sha256_text(prompt)
        try:
            response_text, _sanitized_response = call_model(prompt, config)
            parsed = parse_json_object(response_text)
            record = normalize_judge_result(row, config.provider, config.model, parsed, prompt_hash, "completed")
        except Exception as exc:  # noqa: BLE001
            record = normalize_judge_result(
                row,
                config.provider,
                config.model,
                None,
                prompt_hash,
                "failed",
                type(exc).__name__,
            )
        records.append(record)

    write_jsonl(output_path, records)
    plan_rows = build_plan_rows(selected, config.provider, config.model, "submitted_bounded_live")
    write_csv_rows(PLAN_CSV_PATH, PLAN_COLUMNS, plan_rows)
    write_plan_markdown(plan_rows)
    summary_rows = build_summary_rows(records, config.provider, config.model, "secondary_sensitivity")
    write_csv_rows(SUMMARY_CSV_PATH, SUMMARY_COLUMNS, summary_rows)
    write_summary_markdown(summary_rows)
    for path in (output_path, PLAN_CSV_PATH, PLAN_MD_PATH, SUMMARY_CSV_PATH, SUMMARY_MD_PATH):
        print(f"Wrote {path.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
