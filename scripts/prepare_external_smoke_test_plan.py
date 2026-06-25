from __future__ import annotations

import csv
import json
import os
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
RESULTS_EXPERIMENTS_DIR = REPO_ROOT / "results" / "experiments"

PAYLOAD_JSONL_PATH = RESULTS_EXPERIMENTS_DIR / "external_representation_payloads.jsonl"
PLAN_CSV_PATH = RESULTS_EXPERIMENTS_DIR / "external_smoke_test_plan.csv"
PLAN_MD_PATH = RESULTS_EXPERIMENTS_DIR / "external_smoke_test_plan.md"

PLAN_COLUMNS = [
    "provider",
    "model",
    "credential_env",
    "credential_available",
    "payload_id",
    "condition_case_id",
    "shard_id",
    "planned_command",
    "status",
    "evidence_boundary",
]

PROVIDER_SPECS = [
    {
        "provider": "deepseek",
        "model": "deepseek-v4-flash",
        "credential_env": "DEEPSEEK_API_KEY",
    },
    {
        "provider": "kimi",
        "model": "kimi-k2.7-code",
        "credential_env": "MOONSHOT_API_KEY",
    },
]

EVIDENCE_BOUNDARY = "bounded_smoke_plan_not_external_evaluation"


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def credential_available(env_name: str) -> bool:
    return bool(os.getenv(env_name, "").strip())


def select_smoke_payloads() -> list[dict[str, Any]]:
    payloads = [
        row
        for row in read_jsonl(PAYLOAD_JSONL_PATH)
        if row["shard_id"] == "external-shard-001"
    ]
    if len(payloads) < 2:
        raise ValueError("Expected at least two payload rows in external-shard-001")
    return payloads[:2]


def build_rows() -> list[dict[str, Any]]:
    selected_payloads = select_smoke_payloads()
    rows: list[dict[str, Any]] = []
    for provider in PROVIDER_SPECS:
        available = credential_available(provider["credential_env"])
        status = "ready_for_bounded_live_smoke" if available else "not_run_missing_credentials"
        command = (
            "python scripts/run_external_payload_experiment.py --run-live "
            f"--provider {provider['provider']} --model {provider['model']} "
            "--shard external-shard-001 --sample-limit 2 --max-live-rows 2"
        )
        for payload in selected_payloads:
            rows.append(
                {
                    "provider": provider["provider"],
                    "model": provider["model"],
                    "credential_env": provider["credential_env"],
                    "credential_available": str(available).lower(),
                    "payload_id": payload["payload_id"],
                    "condition_case_id": payload["condition_case_id"],
                    "shard_id": payload["shard_id"],
                    "planned_command": command,
                    "status": status,
                    "evidence_boundary": EVIDENCE_BOUNDARY,
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


def write_markdown(rows: list[dict[str, Any]]) -> None:
    provider_rows: list[list[str]] = []
    seen: set[tuple[str, str]] = set()
    for row in rows:
        key = (row["provider"], row["model"])
        if key in seen:
            continue
        seen.add(key)
        provider_rows.append(
            [
                row["provider"],
                row["model"],
                row["credential_env"],
                row["credential_available"],
                row["status"],
            ]
        )

    lines = [
        "# External Smoke Test Plan",
        "",
        "This no-secret plan selects a two-payload bounded smoke test for each provider. It does not report external model results.",
        "",
        "## Providers",
        "",
        markdown_table(
            ["Provider", "Model", "Credential env", "Credential available", "Status"],
            provider_rows,
        ),
        "",
        "## Payload Rows",
        "",
        markdown_table(
            ["Provider", "Payload", "Condition case", "Shard", "Status"],
            [
                [
                    row["provider"],
                    row["payload_id"],
                    row["condition_case_id"],
                    row["shard_id"],
                    row["status"],
                ]
                for row in rows
            ],
        ),
        "",
    ]
    PLAN_MD_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    rows = build_rows()
    write_csv(PLAN_CSV_PATH, PLAN_COLUMNS, rows)
    write_markdown(rows)
    print(f"Wrote {PLAN_CSV_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {PLAN_MD_PATH.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
