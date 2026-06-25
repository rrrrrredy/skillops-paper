from __future__ import annotations

import argparse
import csv
import hashlib
import random
import re
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
RESULTS_TABLES_DIR = REPO_ROOT / "results" / "tables"

SELECTION_PATH = RESULTS_TABLES_DIR / "external_artifact_selection.csv"
SAMPLING_MANIFEST_PATH = RESULTS_TABLES_DIR / "external_sampling_manifest.csv"
SAMPLING_SUMMARY_PATH = RESULTS_TABLES_DIR / "external_sampling_manifest.md"

DEFAULT_SEED = 20260625
SOURCE_CAP = 0.25
OWNER_CAP = 0.15

MANIFEST_COLUMNS = [
    "artifact_id",
    "source_owner",
    "ecosystem",
    "source_id",
    "study_family",
    "artifact_reference",
    "stratum",
    "random_seed",
    "random_key",
    "source_cap",
    "source_share",
    "owner_cap",
    "owner_share",
    "cap_status",
    "inclusion_status",
    "replacement_for",
    "eligibility_status",
    "license_policy",
    "content_boundary",
]


ECOSYSTEM_BY_SOURCE = {
    "agent-skills-spec": "agent-skills-standard",
    "anthropics-skills": "anthropic",
    "voltagent-awesome": "community-index",
    "mcp-reference-servers": "model-context-protocol",
    "github-mcp-server": "github",
    "openai-agents-python": "openai",
    "openai-agents-js": "openai",
    "autogen-examples": "microsoft",
    "langgraph-template": "langchain",
    "prompts-chat": "prompt-corpus",
    "open-webui-functions": "open-webui",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build seeded external sampling manifest from selected artifact references.")
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED, help="Deterministic randomization seed.")
    return parser.parse_args()


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def github_owner(url: str) -> str:
    match = re.match(r"^https://github\.com/([^/\s]+)/", url.strip())
    return match.group(1).lower() if match else "non-github"


def upstream_owner(reference: str) -> str | None:
    match = re.match(r"^upstream:https://github\.com/([^/\s]+)/", reference.strip())
    return match.group(1).lower() if match else None


def stable_random_key(seed: int, artifact_id: str, source_id: str, reference: str) -> str:
    digest = hashlib.sha256(f"{seed}|{artifact_id}|{source_id}|{reference}".encode("utf-8")).hexdigest()
    return digest[:16]


def owner_for_row(row: dict[str, str]) -> str:
    return upstream_owner(row["artifact_reference"]) or github_owner(row["source_url"])


def stratum_for_row(row: dict[str, str], owner: str, ecosystem: str) -> str:
    return "|".join(
        [
            row["study_family"],
            ecosystem,
            owner,
            row["selection_basis"],
        ]
    )


def build_manifest_rows(selection_rows: list[dict[str, str]], seed: int) -> list[dict[str, Any]]:
    if not selection_rows:
        raise ValueError("No external artifact selection rows found")

    rng = random.Random(seed)
    owner_counts: dict[str, int] = {}
    source_counts: dict[str, int] = {}
    for row in selection_rows:
        owner = owner_for_row(row)
        owner_counts[owner] = owner_counts.get(owner, 0) + 1
        source_counts[row["source_id"]] = source_counts.get(row["source_id"], 0) + 1

    rows: list[dict[str, Any]] = []
    total = len(selection_rows)
    for row in selection_rows:
        owner = owner_for_row(row)
        ecosystem = ECOSYSTEM_BY_SOURCE.get(row["source_id"], "other")
        base_key = stable_random_key(seed, row["artifact_id"], row["source_id"], row["artifact_reference"])
        random_key = f"{base_key}-{rng.randrange(0, 2**16):04x}"
        source_share = source_counts[row["source_id"]] / total
        owner_share = owner_counts[owner] / total
        cap_status = "within_caps"
        if source_share > SOURCE_CAP or owner_share > OWNER_CAP:
            cap_status = "cap_exceeded_requires_replacement_or_expansion"
        rows.append(
            {
                "artifact_id": row["artifact_id"],
                "source_owner": owner,
                "ecosystem": ecosystem,
                "source_id": row["source_id"],
                "study_family": row["study_family"],
                "artifact_reference": row["artifact_reference"],
                "stratum": stratum_for_row(row, owner, ecosystem),
                "random_seed": seed,
                "random_key": random_key,
                "source_cap": SOURCE_CAP,
                "source_share": f"{source_share:.6f}",
                "owner_cap": OWNER_CAP,
                "owner_share": f"{owner_share:.6f}",
                "cap_status": cap_status,
                "inclusion_status": "included_pending_eligibility_review",
                "replacement_for": "",
                "eligibility_status": "pending_review",
                "license_policy": row["license_policy"],
                "content_boundary": row["content_boundary"],
            }
        )
    return sorted(rows, key=lambda item: (item["random_key"], item["artifact_id"]))


def count_by(rows: list[dict[str, Any]], key: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in rows:
        value = str(row[key])
        counts[value] = counts.get(value, 0) + 1
    return dict(sorted(counts.items()))


def markdown_table(headers: list[str], rows: list[list[str]]) -> str:
    return "\n".join(
        [
            "| " + " | ".join(headers) + " |",
            "| " + " | ".join(["---"] * len(headers)) + " |",
            *["| " + " | ".join(row) + " |" for row in rows],
        ]
    )


def write_summary(rows: list[dict[str, Any]]) -> None:
    source_counts = count_by(rows, "source_id")
    owner_counts = count_by(rows, "source_owner")
    ecosystem_counts = count_by(rows, "ecosystem")
    total = len(rows)
    max_source_share = max(source_counts.values()) / total
    max_owner_share = max(owner_counts.values()) / total
    cap_exceeded = sum(1 for row in rows if row["cap_status"] != "within_caps")

    lines = [
        "# External Sampling Manifest",
        "",
        "This manifest adds deterministic randomization keys and owner/ecosystem strata to the metadata-only external artifact selection. It is a sampling frame, not an eligibility or outcome result.",
        "",
        "## Totals",
        "",
        markdown_table(
            ["Quantity", "Value"],
            [
                ["Artifact rows", str(total)],
                ["Source cap target", f"{SOURCE_CAP:.2f}"],
                ["Owner cap target", f"{OWNER_CAP:.2f}"],
                ["Largest current source share", f"{max_source_share:.3f}"],
                ["Largest current owner share", f"{max_owner_share:.3f}"],
                ["Rows exceeding target caps", str(cap_exceeded)],
                ["Eligibility status", "pending_review"],
            ],
        ),
        "",
        "## Ecosystems",
        "",
        markdown_table(["Ecosystem", "Rows"], [[key, str(value)] for key, value in ecosystem_counts.items()]),
        "",
        "## Sources",
        "",
        markdown_table(["Source", "Rows"], [[key, str(value)] for key, value in source_counts.items()]),
        "",
        "## Owners",
        "",
        markdown_table(["Owner", "Rows"], [[key, str(value)] for key, value in owner_counts.items()]),
        "",
    ]
    SAMPLING_SUMMARY_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    args = parse_args()
    selection_rows = read_csv_rows(SELECTION_PATH)
    manifest_rows = build_manifest_rows(selection_rows, args.seed)
    write_csv(SAMPLING_MANIFEST_PATH, MANIFEST_COLUMNS, manifest_rows)
    write_summary(manifest_rows)
    print(f"Wrote {SAMPLING_MANIFEST_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {SAMPLING_SUMMARY_PATH.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
