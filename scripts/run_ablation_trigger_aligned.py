#!/usr/bin/env python3
"""Aligned Ablation Trigger-Routing Experiment.

Runs the ablation trigger-routing slice with skill definitions aligned to
benchmark/trigger_cases.csv (SkillOps artifact skills, not translation).

Usage:
    python3 scripts/run_ablation_trigger_aligned.py --dry-run
    python3 scripts/run_ablation_trigger_aligned.py --run-live --provider deepseek --model deepseek-chat --repeats 1
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# --- Paths ---
REPO_ROOT = Path(__file__).resolve().parent.parent
BENCHMARK_DIR = REPO_ROOT / "benchmark"
ALIGNED_DIR = REPO_ROOT / "experiments" / "ablation_trigger_aligned"
VARIANTS_DIR = ALIGNED_DIR / "variants"
RESULTS_DIR = REPO_ROOT / "results" / "experiments"
RAW_DIR = RESULTS_DIR / "raw"
RESEARCH_LOG_DIR = REPO_ROOT / "research-log"

TRIGGER_CASES_PATH = BENCHMARK_DIR / "trigger_cases.csv"

VARIANT_NAMES = [
    "full_skillops",
    "no_trigger_boundary",
    "freeform_only",
    "no_execution_constraints",
    "no_security_checks",
    "no_memory_interface",
]

# --- Helpers ---

def utc_timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def utc_file_timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def prompt_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def parse_json_response(text: str) -> dict | None:
    """Try to extract JSON from model response."""
    # Strip markdown code fences if present
    cleaned = text.strip()
    if cleaned.startswith("```"):
        lines = cleaned.split("\n")
        # Remove first and last lines (fences)
        lines = [l for l in lines[1:] if not l.strip().startswith("```")]
        cleaned = "\n".join(lines).strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        # Try to find JSON object in text
        start = cleaned.find("{")
        end = cleaned.rfind("}") + 1
        if start >= 0 and end > start:
            try:
                return json.loads(cleaned[start:end])
            except json.JSONDecodeError:
                return None
    return None


def safe_divide(a: int, b: int) -> float | None:
    return a / b if b > 0 else None


# --- Provider config (reuse from experiment_utils if available) ---

def get_provider_config(provider: str, model: str) -> dict:
    """Build provider config for API calls."""
    import os
    if provider == "deepseek":
        api_key = os.environ.get("DEEPSEEK_API_KEY", "")
        base_url = os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1")
        return {
            "provider": "deepseek",
            "model": model or "deepseek-chat",
            "endpoint": f"{base_url.rstrip('/')}/chat/completions",
            "api_key": api_key,
        }
    elif provider == "longcat":
        api_key = os.environ.get("LONGCAT_API_KEY", "")
        base_url = os.environ.get("LONGCAT_BASE_URL", "https://api.longcat.chat/openai/v1")
        return {
            "provider": "longcat",
            "model": model or "LongCat-Flash-Chat",
            "endpoint": f"{base_url.rstrip('/')}/chat/completions",
            "api_key": api_key,
        }
    else:
        raise ValueError(f"Unsupported provider: {provider}")


def call_api(prompt: str, config: dict, max_retries: int = 5) -> tuple[str, dict]:
    """Call the model API with retry logic."""
    import urllib.request
    import urllib.error

    time.sleep(0.5)  # rate-limit guard

    payload = {
        "model": config["model"],
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0,
        "max_tokens": 1024,
    }

    request_data = json.dumps(payload).encode("utf-8")
    last_error = None

    for attempt in range(max_retries + 1):
        req = urllib.request.Request(
            url=config["endpoint"],
            data=request_data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {config['api_key']}",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=180) as response:
                body = json.loads(response.read().decode("utf-8"))
                text = body["choices"][0]["message"]["content"]
                return text, body
        except urllib.error.HTTPError as error:
            if error.code == 429 and attempt < max_retries:
                retry_after = error.headers.get("Retry-After")
                wait = float(retry_after) if retry_after else min(2 ** attempt * 5, 120)
                print(f"  [429] Rate limited, waiting {wait}s (attempt {attempt+1}/{max_retries})")
                time.sleep(wait)
                last_error = error
                continue
            if error.code >= 500 and attempt < max_retries:
                wait = min(2 ** attempt * 2, 60)
                print(f"  [{error.code}] Server error, retrying in {wait}s")
                time.sleep(wait)
                last_error = error
                continue
            details = error.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"HTTP {error.code}: {details}") from error
        except urllib.error.URLError as error:
            if attempt < max_retries:
                wait = min(2 ** attempt * 2, 60)
                time.sleep(wait)
                last_error = error
                continue
            raise RuntimeError(f"Network error: {error}") from error

    raise RuntimeError(f"Max retries exceeded: {last_error}")


# --- Validation ---

def validate_inputs() -> tuple[list[dict], dict[str, str]]:
    """Validate all required inputs exist and return cases + variant texts."""
    errors = []

    if not TRIGGER_CASES_PATH.exists():
        errors.append(f"Missing: {TRIGGER_CASES_PATH}")

    variant_texts: dict[str, str] = {}
    for name in VARIANT_NAMES:
        path = VARIANTS_DIR / f"{name}.md"
        if path.exists():
            variant_texts[name] = read_text(path)
        else:
            errors.append(f"Missing variant: {path}")

    if errors:
        for e in errors:
            print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    with open(TRIGGER_CASES_PATH, newline="", encoding="utf-8") as f:
        cases = list(csv.DictReader(f))

    print(f"Inputs validated:")
    print(f"  Cases: {len(cases)}")
    print(f"  Variants: {len(variant_texts)} ({', '.join(variant_texts.keys())})")
    print(f"  Total calls: {len(cases) * len(variant_texts)}")

    return cases, variant_texts


# --- Experiment execution ---

def run_experiment(cases: list[dict], variant_texts: dict[str, str], config: dict, repeats: int) -> list[dict]:
    """Run the aligned ablation trigger-routing experiment."""
    records = []
    total = len(cases) * len(variant_texts) * repeats
    done = 0

    for variant_name, skill_def in variant_texts.items():
        print(f"\n--- Variant: {variant_name} ({len(cases)} cases × {repeats} repeats) ---")

        for case_row in cases:
            for repeat_idx in range(repeats):
                prompt = f"{skill_def}\n\n## User Request\n\ncase_id: {case_row['case_id']}\nRequest: {case_row['user_request']}"

                started_at = utc_timestamp()
                try:
                    response_text, response_json = call_api(prompt, config)
                    error_msg = ""
                except Exception as e:
                    response_text = ""
                    response_json = {}
                    error_msg = str(e)
                completed_at = utc_timestamp()

                # Parse response
                parsed = parse_json_response(response_text) if response_text else None
                parsing_status = "success" if parsed else ("error" if response_text else "empty")

                predicted_label = ""
                predicted_skill = ""
                confidence = ""
                rationale = ""

                if parsed:
                    predicted_label = parsed.get("predicted_label", "")
                    predicted_skill = parsed.get("predicted_skill", "")
                    confidence = parsed.get("confidence", "")
                    rationale = parsed.get("rationale", "")

                record = {
                    "provider": config["provider"],
                    "model": config["model"],
                    "experiment": "ablation_trigger_aligned",
                    "variant": variant_name,
                    "case_id": case_row["case_id"],
                    "expected_label": case_row["expected_label"],
                    "expected_skill": case_row["relevant_skill"],
                    "predicted_label": predicted_label,
                    "predicted_skill": predicted_skill,
                    "repeat_index": repeat_idx,
                    "prompt_hash": prompt_hash(prompt),
                    "raw_response": response_text,
                    "normalized_prediction": {
                        "label": predicted_label,
                        "skill": predicted_skill,
                        "confidence": confidence,
                        "rationale": rationale,
                    },
                    "parsing_status": parsing_status,
                    "error": error_msg,
                    "started_at_utc": started_at,
                    "completed_at_utc": completed_at,
                }
                records.append(record)
                done += 1

                if done % 20 == 0:
                    print(f"  Progress: {done}/{total} ({done*100//total}%)")

    return records


# --- Metrics computation ---

def compute_metrics(records: list[dict]) -> list[dict]:
    """Compute metrics by variant."""
    metrics_rows = []

    for variant_name in VARIANT_NAMES:
        variant_records = [r for r in records if r["variant"] == variant_name]
        if not variant_records:
            continue

        # Filter out parse failures for metric computation
        valid = [r for r in variant_records if r["parsing_status"] == "success"]
        total_cases = len(variant_records)
        parse_failures = sum(1 for r in variant_records if r["parsing_status"] != "success")
        exec_failures = sum(1 for r in variant_records if r["error"])

        # should_trigger is positive class
        should_trigger = [r for r in valid if r["expected_label"] == "should_trigger"]
        should_not = [r for r in valid if r["expected_label"] == "should_not_trigger"]
        ambiguous = [r for r in valid if r["expected_label"] == "ambiguous"]

        # True positives: expected=should_trigger AND predicted=should_trigger
        tp = sum(1 for r in should_trigger if r["predicted_label"] == "should_trigger")
        # All predicted as should_trigger
        predicted_positive = sum(1 for r in valid if r["predicted_label"] == "should_trigger")
        # False positives on should_not_trigger cases
        fp_on_neg = sum(1 for r in should_not if r["predicted_label"] == "should_trigger")

        # Precision, Recall, F1
        precision = safe_divide(tp, predicted_positive)
        recall = safe_divide(tp, len(should_trigger))
        f1 = (2 * precision * recall / (precision + recall)) if (precision and recall and (precision + recall) > 0) else 0.0

        # False trigger rate on should_not_trigger
        false_trigger_rate = safe_divide(fp_on_neg, len(should_not))

        # Ambiguity handling: how many ambiguous cases predicted as "ambiguous"
        ambig_correct = sum(1 for r in ambiguous if r["predicted_label"] == "ambiguous")
        ambiguity_handling_rate = safe_divide(ambig_correct, len(ambiguous))

        # Skill routing accuracy: among should_trigger cases that predicted should_trigger, did they route to correct skill?
        correct_skill = sum(1 for r in should_trigger
                          if r["predicted_label"] == "should_trigger"
                          and r["predicted_skill"] == r["expected_skill"])
        skill_routing_accuracy = safe_divide(correct_skill, tp) if tp > 0 else None

        metrics_rows.append({
            "variant": variant_name,
            "precision": f"{precision:.4f}" if precision is not None else "n/a",
            "recall": f"{recall:.4f}" if recall is not None else "n/a",
            "f1": f"{f1:.4f}" if f1 is not None else "n/a",
            "false_trigger_rate": f"{false_trigger_rate:.4f}" if false_trigger_rate is not None else "n/a",
            "ambiguity_handling_rate": f"{ambiguity_handling_rate:.4f}" if ambiguity_handling_rate is not None else "n/a",
            "skill_routing_accuracy": f"{skill_routing_accuracy:.4f}" if skill_routing_accuracy is not None else "n/a",
            "cases": str(total_cases),
            "parse_failures": str(parse_failures),
            "execution_failures": str(exec_failures),
            "tp": str(tp),
            "predicted_positive": str(predicted_positive),
            "should_trigger_total": str(len(should_trigger)),
            "should_not_trigger_total": str(len(should_not)),
            "ambiguous_total": str(len(ambiguous)),
        })

    return metrics_rows


def write_metrics_csv(metrics: list[dict], path: Path):
    if not metrics:
        return
    fieldnames = list(metrics[0].keys())
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(metrics)


def write_metrics_md(metrics: list[dict], config: dict, raw_path: Path, md_path: Path):
    lines = [
        "# Aligned Ablation Trigger-Routing Metrics",
        "",
        f"- Provider: `{config['provider']}`",
        f"- Model: `{config['model']}`",
        f"- Raw output: `{raw_path.relative_to(REPO_ROOT)}`",
        f"- Experiment: `ablation_trigger_aligned`",
        "",
        "| Variant | Precision | Recall | F1 | False Trigger Rate | Ambiguity Handling | Skill Routing Acc | Cases | Parse Fail |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for m in metrics:
        lines.append(
            f"| {m['variant']} | {m['precision']} | {m['recall']} | {m['f1']} | "
            f"{m['false_trigger_rate']} | {m['ambiguity_handling_rate']} | "
            f"{m['skill_routing_accuracy']} | {m['cases']} | {m['parse_failures']} |"
        )
    lines.append("")
    md_path.write_text("\n".join(lines), encoding="utf-8")


# --- Main ---

def main() -> int:
    parser = argparse.ArgumentParser(description="Run aligned ablation trigger-routing experiment.")
    parser.add_argument("--dry-run", action="store_true", help="Validate inputs only.")
    parser.add_argument("--run-live", action="store_true", help="Run live API calls.")
    parser.add_argument("--provider", default="deepseek", choices=["deepseek", "longcat"],
                       help="Provider for API calls.")
    parser.add_argument("--model", default="deepseek-chat", help="Model name.")
    parser.add_argument("--repeats", type=int, default=1, help="Repeats per case.")
    args = parser.parse_args()

    print("=" * 60)
    print("Aligned Ablation Trigger-Routing Experiment")
    print("=" * 60)

    cases, variant_texts = validate_inputs()
    print("\n✅ Dry-run validation passed.")

    if args.dry_run and not args.run_live:
        print("Live run skipped (--dry-run only).")
        return 0

    if not args.run_live:
        print("Pass --run-live to execute.")
        return 0

    # Build config
    config = get_provider_config(args.provider, args.model)
    if not config["api_key"]:
        print(f"ERROR: No API key found for provider '{args.provider}'.")
        print(f"  Set DEEPSEEK_API_KEY or LONGCAT_API_KEY environment variable.")
        return 1

    print(f"\nProvider: {config['provider']}")
    print(f"Model: {config['model']}")
    print(f"Endpoint: {config['endpoint']}")
    print(f"Repeats: {args.repeats}")
    print(f"Total calls: {len(cases) * len(variant_texts) * args.repeats}")

    # Connectivity test
    print("\nTesting API connectivity...")
    try:
        test_resp, _ = call_api("Reply with exactly: {\"status\": \"ok\"}", config)
        print(f"  ✅ API responding: {test_resp[:50]}")
    except Exception as e:
        print(f"  ❌ API test failed: {e}")
        return 1

    # Run experiment
    print("\n" + "=" * 60)
    print("Starting live experiment...")
    print("=" * 60)
    start_time = time.time()

    records = run_experiment(cases, variant_texts, config, args.repeats)

    elapsed = time.time() - start_time
    print(f"\n✅ Experiment complete. {len(records)} records in {elapsed:.1f}s")

    # Write raw output
    ts = utc_file_timestamp()
    raw_path = RAW_DIR / f"ablation_trigger_aligned_{ts}.jsonl"
    with open(raw_path, "w", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    print(f"  Raw output: {raw_path.relative_to(REPO_ROOT)}")

    # Compute and write metrics
    metrics = compute_metrics(records)
    csv_path = RESULTS_DIR / "ablation_trigger_aligned_metrics.csv"
    md_path = RESULTS_DIR / "ablation_trigger_aligned_metrics.md"
    write_metrics_csv(metrics, csv_path)
    write_metrics_md(metrics, config, raw_path, md_path)
    print(f"  Metrics CSV: {csv_path.relative_to(REPO_ROOT)}")
    print(f"  Metrics MD: {md_path.relative_to(REPO_ROOT)}")

    # Write research log
    RESEARCH_LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_path = RESEARCH_LOG_DIR / "2026-04-30-ablation-trigger-aligned.md"
    log_lines = [
        "# Aligned Ablation Trigger-Routing Run Log",
        "",
        f"Date: {utc_timestamp()}",
        f"Provider: {config['provider']}",
        f"Model: {config['model']}",
        f"Repeats: {args.repeats}",
        f"Total records: {len(records)}",
        f"Elapsed: {elapsed:.1f}s",
        "",
        "## Results Summary",
        "",
        "| Variant | Precision | Recall | F1 | Skill Routing Acc |",
        "| --- | --- | --- | --- | --- |",
    ]
    for m in metrics:
        log_lines.append(f"| {m['variant']} | {m['precision']} | {m['recall']} | {m['f1']} | {m['skill_routing_accuracy']} |")
    log_lines += [
        "",
        "## Errors",
        "",
        f"Parse failures: {sum(int(m['parse_failures']) for m in metrics)}",
        f"Execution failures: {sum(int(m['execution_failures']) for m in metrics)}",
        "",
        "## Files Generated",
        "",
        f"- Raw: `{raw_path.relative_to(REPO_ROOT)}`",
        f"- Metrics CSV: `{csv_path.relative_to(REPO_ROOT)}`",
        f"- Metrics MD: `{md_path.relative_to(REPO_ROOT)}`",
        f"- Research log: `{log_path.relative_to(REPO_ROOT)}`",
    ]
    log_path.write_text("\n".join(log_lines), encoding="utf-8")
    print(f"  Research log: {log_path.relative_to(REPO_ROOT)}")

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    for m in metrics:
        print(f"  {m['variant']}: P={m['precision']} R={m['recall']} F1={m['f1']} SkillAcc={m['skill_routing_accuracy']}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
