from __future__ import annotations

import csv
import json
import re
import subprocess
import sys
import urllib.error
import urllib.request
from collections import Counter
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
BENCHMARK_DIR = REPO_ROOT / "benchmark"
RESULTS_TABLES_DIR = REPO_ROOT / "results" / "tables"
CACHE_ROOT = REPO_ROOT.parent / "skillops-paper-external-cache"
INPUT_PATH = BENCHMARK_DIR / "external_artifact_corpus_sources.csv"
DETAIL_CSV_PATH = RESULTS_TABLES_DIR / "external_corpus_static_analysis.csv"
SUMMARY_CSV_PATH = RESULTS_TABLES_DIR / "external_corpus_summary.csv"
SUMMARY_MD_PATH = RESULTS_TABLES_DIR / "external_corpus_summary.md"

DETAIL_COLUMNS = [
    "source_id",
    "source_name",
    "artifact_family",
    "source_url",
    "source_kind",
    "analysis_status",
    "license_declared",
    "github_stars",
    "github_forks",
    "default_branch",
    "tree_files",
    "readme_files",
    "license_files",
    "skill_md_files",
    "example_files",
    "test_files",
    "script_files",
    "workflow_files",
    "schema_files",
    "security_files",
    "manifest_files",
    "docs_files",
    "lifecycle_indicator_count",
    "analysis_notes",
]

SUMMARY_COLUMNS = ["group", "value", "metric", "count", "notes"]

GITHUB_URL_PATTERN = re.compile(r"^https://github\.com/([^/\s]+)/([^/\s#?]+)")


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def github_owner_repo(url: str) -> tuple[str, str] | None:
    match = GITHUB_URL_PATTERN.match(url.strip())
    if not match:
        return None
    owner, repo = match.groups()
    return owner, repo.removesuffix(".git")


def github_get_json(url: str) -> Any:
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "skillops-paper-static-corpus-analyzer",
        },
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))


def path_matches(path: str, *needles: str) -> bool:
    lowered = path.lower()
    return any(needle in lowered for needle in needles)


def count_static_indicators(tree_items: list[dict[str, Any]]) -> dict[str, int]:
    paths = [
        str(item.get("path", ""))
        for item in tree_items
        if item.get("type") == "blob" and str(item.get("path", "")).strip()
    ]
    basenames = [Path(path).name.lower() for path in paths]
    return {
        "tree_files": len(paths),
        "readme_files": sum(1 for name in basenames if name.startswith("readme")),
        "license_files": sum(1 for name in basenames if name in {"license", "license.md", "license.txt", "copying"}),
        "skill_md_files": sum(1 for path in paths if Path(path).name.lower() == "skill.md"),
        "example_files": sum(1 for path in paths if path_matches(path, "example", "examples", "sample", "samples")),
        "test_files": sum(1 for path in paths if path_matches(path, "test", "tests", "spec")),
        "script_files": sum(1 for path in paths if path_matches(path, "script", "scripts") or Path(path).suffix.lower() in {".py", ".js", ".ts", ".tsx", ".sh", ".ps1"}),
        "workflow_files": sum(1 for path in paths if path_matches(path, ".github/workflows", "workflow", "workflows")),
        "schema_files": sum(1 for path in paths if path_matches(path, "schema") or Path(path).suffix.lower() in {".json", ".yaml", ".yml"}),
        "security_files": sum(1 for path in paths if path_matches(path, "security", "guardrail", "guardrails", "safety", "policy")),
        "manifest_files": sum(1 for path in paths if Path(path).name.lower() in {"package.json", "pyproject.toml", "skill.toml", "manifest.json", "plugin.json"}),
        "docs_files": sum(1 for path in paths if path_matches(path, "docs/", "doc/", "documentation")),
    }


def lifecycle_indicator_count(indicators: dict[str, int]) -> int:
    indicator_names = [
        "readme_files",
        "license_files",
        "skill_md_files",
        "example_files",
        "test_files",
        "script_files",
        "workflow_files",
        "schema_files",
        "security_files",
        "manifest_files",
        "docs_files",
    ]
    return sum(1 for name in indicator_names if indicators.get(name, 0) > 0)


def analyze_github_source(source: dict[str, str], owner: str, repo: str) -> dict[str, Any]:
    repo_json = github_get_json(f"https://api.github.com/repos/{owner}/{repo}")
    default_branch = str(repo_json.get("default_branch") or "main")
    tree_json = github_get_json(
        f"https://api.github.com/repos/{owner}/{repo}/git/trees/{default_branch}?recursive=1"
    )
    tree_items = tree_json.get("tree", [])
    if not isinstance(tree_items, list):
        tree_items = []
    indicators = count_static_indicators(tree_items)
    license_obj = repo_json.get("license")
    license_declared = ""
    if isinstance(license_obj, dict):
        license_declared = str(license_obj.get("spdx_id") or license_obj.get("name") or "")

    row: dict[str, Any] = {
        "source_id": source["source_id"],
        "source_name": source["source_name"],
        "artifact_family": source["artifact_family"],
        "source_url": source["source_url"],
        "source_kind": "github_repo",
        "analysis_status": "ok",
        "license_declared": license_declared or source["license_status"],
        "github_stars": int(repo_json.get("stargazers_count") or 0),
        "github_forks": int(repo_json.get("forks_count") or 0),
        "default_branch": default_branch,
        **indicators,
        "lifecycle_indicator_count": lifecycle_indicator_count(indicators),
        "analysis_notes": "",
    }
    return row


def git_command(args: list[str], *, cwd: Path | None = None) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=str(cwd) if cwd else None,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=180,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip())
    return result.stdout


def ensure_git_tree_cache(source: dict[str, str]) -> Path:
    CACHE_ROOT.mkdir(parents=True, exist_ok=True)
    target = CACHE_ROOT / source["source_id"]
    if target.exists() and not (target / ".git").exists():
        raise RuntimeError(f"Cache path exists but is not a Git checkout: {target}")
    if (target / ".git").exists():
        git_command(["fetch", "--depth", "1", "origin"], cwd=target)
    else:
        git_command(
            [
                "clone",
                "--depth",
                "1",
                "--filter=blob:none",
                "--no-checkout",
                source["source_url"],
                str(target),
            ]
        )
    return target


def analyze_github_source_with_git(source: dict[str, str]) -> dict[str, Any]:
    checkout = ensure_git_tree_cache(source)
    branch = git_command(["rev-parse", "--abbrev-ref", "HEAD"], cwd=checkout).strip()
    paths = [
        line.strip()
        for line in git_command(["ls-tree", "-r", "--name-only", "HEAD"], cwd=checkout).splitlines()
        if line.strip()
    ]
    indicators = count_static_indicators([{"type": "blob", "path": path} for path in paths])
    return {
        "source_id": source["source_id"],
        "source_name": source["source_name"],
        "artifact_family": source["artifact_family"],
        "source_url": source["source_url"],
        "source_kind": "github_repo_git_tree",
        "analysis_status": "ok_git_fallback",
        "license_declared": source["license_status"],
        "github_stars": "",
        "github_forks": "",
        "default_branch": branch,
        **indicators,
        "lifecycle_indicator_count": lifecycle_indicator_count(indicators),
        "analysis_notes": "GitHub API unavailable; analyzed file tree from a blobless no-checkout Git clone outside the repository.",
    }


def analyze_source(source: dict[str, str]) -> dict[str, Any]:
    github_repo = github_owner_repo(source["source_url"])
    base_row: dict[str, Any] = {
        "source_id": source["source_id"],
        "source_name": source["source_name"],
        "artifact_family": source["artifact_family"],
        "source_url": source["source_url"],
        "source_kind": "web_reference",
        "analysis_status": "metadata_only",
        "license_declared": source["license_status"],
        "github_stars": "",
        "github_forks": "",
        "default_branch": "",
        "tree_files": "",
        "readme_files": "",
        "license_files": "",
        "skill_md_files": "",
        "example_files": "",
        "test_files": "",
        "script_files": "",
        "workflow_files": "",
        "schema_files": "",
        "security_files": "",
        "manifest_files": "",
        "docs_files": "",
        "lifecycle_indicator_count": "",
        "analysis_notes": "Non-GitHub source; retained as citable metadata.",
    }
    if github_repo is None:
        return base_row
    try:
        return analyze_github_source(source, *github_repo)
    except urllib.error.HTTPError as error:
        try:
            row = analyze_github_source_with_git(source)
            row["analysis_notes"] = f"GitHub API returned HTTP {error.code}; " + row["analysis_notes"]
            return row
        except (RuntimeError, subprocess.SubprocessError) as fallback_error:
            base_row["source_kind"] = "github_repo"
            base_row["analysis_status"] = f"http_error_{error.code}"
            base_row["analysis_notes"] = f"GitHub API failed and Git fallback failed: {fallback_error}"
            return base_row
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, RuntimeError) as error:
        base_row["source_kind"] = "github_repo"
        base_row["analysis_status"] = "error"
        base_row["analysis_notes"] = f"{type(error).__name__}: {error}"
        return base_row


def summarize(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    summary_rows: list[dict[str, Any]] = []
    summary_rows.append(
        {
            "group": "overall",
            "value": "sources",
            "metric": "count",
            "count": len(rows),
            "notes": "All rows from the external source frame.",
        }
    )
    ok_rows = [row for row in rows if str(row["analysis_status"]).startswith("ok")]
    summary_rows.append(
        {
            "group": "overall",
            "value": "github_static_analysis",
            "metric": "count",
            "count": len(ok_rows),
            "notes": "GitHub repositories with successful metadata and tree analysis.",
        }
    )

    for family, count in sorted(Counter(str(row["artifact_family"]) for row in rows).items()):
        summary_rows.append(
            {
                "group": "artifact_family",
                "value": family,
                "metric": "count",
                "count": count,
                "notes": "",
            }
        )

    indicator_fields = [
        "readme_files",
        "license_files",
        "skill_md_files",
        "example_files",
        "test_files",
        "script_files",
        "workflow_files",
        "schema_files",
        "security_files",
        "manifest_files",
        "docs_files",
    ]
    for field in indicator_fields:
        hit_count = sum(1 for row in ok_rows if int(row.get(field) or 0) > 0)
        summary_rows.append(
            {
                "group": "static_indicator",
                "value": field,
                "metric": "source_count",
                "count": hit_count,
                "notes": "Count among successfully analyzed GitHub repositories.",
            }
        )
    return summary_rows


def markdown_table(headers: list[str], rows: list[list[str]]) -> str:
    return "\n".join(
        [
            "| " + " | ".join(headers) + " |",
            "| " + " | ".join(["---"] * len(headers)) + " |",
            *["| " + " | ".join(row) + " |" for row in rows],
        ]
    )


def write_markdown(detail_rows: list[dict[str, Any]], summary_rows: list[dict[str, Any]]) -> None:
    ok_rows = [row for row in detail_rows if str(row["analysis_status"]).startswith("ok")]
    family_rows = [row for row in summary_rows if row["group"] == "artifact_family"]
    indicator_rows = [row for row in summary_rows if row["group"] == "static_indicator"]
    top_rows = sorted(ok_rows, key=lambda row: int(row.get("lifecycle_indicator_count") or 0), reverse=True)[:8]

    lines = [
        "# External Corpus Static Analysis",
        "",
        "This report analyzes public third-party artifact sources without copying repository prose or code into the paper artifact.",
        "",
        "## Source Families",
        "",
        markdown_table(
            ["Family", "Sources"],
            [[row["value"], str(row["count"])] for row in family_rows],
        ),
        "",
        "## Static Indicators",
        "",
        markdown_table(
            ["Indicator", "Sources"],
            [[row["value"], str(row["count"])] for row in indicator_rows],
        ),
        "",
        "## High-Coverage Sources",
        "",
        markdown_table(
            ["Source", "Family", "License", "Stars", "Indicators"],
            [
                [
                    row["source_id"],
                    row["artifact_family"],
                    str(row["license_declared"]),
                    str(row["github_stars"]),
                    str(row["lifecycle_indicator_count"]),
                ]
                for row in top_rows
            ],
        ),
        "",
    ]
    SUMMARY_MD_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    source_rows = read_csv_rows(INPUT_PATH)
    detail_rows = [analyze_source(row) for row in source_rows]
    summary_rows = summarize(detail_rows)
    write_csv(DETAIL_CSV_PATH, DETAIL_COLUMNS, detail_rows)
    write_csv(SUMMARY_CSV_PATH, SUMMARY_COLUMNS, summary_rows)
    write_markdown(detail_rows, summary_rows)
    print(f"Wrote {DETAIL_CSV_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {SUMMARY_CSV_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {SUMMARY_MD_PATH.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
