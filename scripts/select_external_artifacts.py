from __future__ import annotations

import csv
import re
import subprocess
from pathlib import Path, PurePosixPath
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
RESULTS_TABLES_DIR = REPO_ROOT / "results" / "tables"
CACHE_ROOT = REPO_ROOT.parent / "skillops-paper-external-cache"

ALLOCATION_PATH = RESULTS_TABLES_DIR / "external_case_allocation.csv"
SELECTION_PATH = RESULTS_TABLES_DIR / "external_artifact_selection.csv"
SUMMARY_CSV_PATH = RESULTS_TABLES_DIR / "external_artifact_selection_summary.csv"
SUMMARY_MD_PATH = RESULTS_TABLES_DIR / "external_artifact_selection.md"

GITHUB_URL_PATTERN = re.compile(r"https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+")

SELECTION_COLUMNS = [
    "artifact_id",
    "study_family",
    "source_id",
    "source_name",
    "source_url",
    "source_version",
    "artifact_reference",
    "selection_status",
    "selection_basis",
    "case_count",
    "condition_evaluation_count",
    "license_policy",
    "content_boundary",
]

SUMMARY_COLUMNS = ["group", "value", "metric", "count", "notes"]

TEXTLIKE_SUFFIXES = {
    ".md",
    ".mdx",
    ".txt",
    ".json",
    ".yaml",
    ".yml",
    ".toml",
    ".py",
    ".js",
    ".ts",
    ".tsx",
    ".jsx",
    ".sh",
    ".ps1",
}

BINARY_OR_ASSET_SUFFIXES = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".webp",
    ".svg",
    ".pdf",
    ".ttf",
    ".otf",
    ".woff",
    ".woff2",
    ".zip",
}

RELEVANT_SEGMENTS = {
    "agents",
    "examples",
    "example",
    "functions",
    "pipelines",
    "prompts",
    "resources",
    "samples",
    "servers",
    "skills",
    "src",
    "templates",
    "tools",
    "workflows",
}

NON_CAPABILITY_NAMES = {
    "funding.yml",
    "license",
    "license.md",
    "license.txt",
    "copying",
    "notice",
    "readme.license",
}

NON_CAPABILITY_SEGMENTS = {
    ".github",
    ".gitlab",
    "canvas-fonts",
    "fonts",
    "font",
    "licenses",
    "license",
}

NON_CAPABILITY_NAME_PATTERNS = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in (
        r"(^|[-_])ofl(\.|$)",
        r"font[-_]?license",
        r"codeowners",
        r"dependabot",
        r"funding",
    )
]

PROHIBITED_PUBLIC_REFERENCE_PATTERNS = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in (
        "long" + "cat",
        "co" + "dex",
        "chat" + "gpt",
        "generated" + " by",
        "ai-" + "written",
        "ai-" + "generated",
        "dr" + "aft",
        "work in " + "progress",
    )
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


def github_owner_repo(url: str) -> tuple[str, str] | None:
    match = re.match(r"^https://github\.com/([^/\s]+)/([^/\s#?]+)", url.strip())
    if not match:
        return None
    owner, repo = match.groups()
    return owner, repo.removesuffix(".git")


def git_command(args: list[str], *, cwd: Path | None = None, timeout: int = 180) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=str(cwd) if cwd else None,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=timeout,
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
        try:
            git_command(["fetch", "--depth", "1", "origin"], cwd=target)
        except RuntimeError:
            pass
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
            ],
            timeout=240,
        )
    return target


def list_tree_paths(checkout: Path) -> list[str]:
    return [
        line.strip()
        for line in git_command(["ls-tree", "-r", "--name-only", "HEAD"], cwd=checkout).splitlines()
        if line.strip()
    ]


def current_commit(checkout: Path) -> str:
    return git_command(["rev-parse", "HEAD"], cwd=checkout).strip()


def show_file(checkout: Path, path: str) -> str:
    return git_command(["show", f"HEAD:{path}"], cwd=checkout, timeout=240)


def lower_segments(path: PurePosixPath) -> set[str]:
    return {part.lower() for part in path.parts}


def add_candidate(
    candidates: dict[str, tuple[int, str]],
    reference: str,
    priority: int,
    basis: str,
) -> None:
    if not reference or reference in {".", "/"}:
        return
    if any(pattern.search(reference) for pattern in PROHIBITED_PUBLIC_REFERENCE_PATTERNS):
        return
    existing = candidates.get(reference)
    if existing is None or priority < existing[0]:
        candidates[reference] = (priority, basis)


def is_capability_reference(path: PurePosixPath) -> bool:
    name = path.name.lower()
    segments = lower_segments(path)
    if name in NON_CAPABILITY_NAMES:
        return False
    if segments & NON_CAPABILITY_SEGMENTS:
        return False
    if any(pattern.search(name) for pattern in NON_CAPABILITY_NAME_PATTERNS):
        return False
    if "workflow" in segments or "workflows" in segments:
        return path.suffix.lower() in {".md", ".mdx", ".json", ".yaml", ".yml", ".py", ".js", ".ts"} and not (
            ".github" in segments
        )
    return True


def tree_path_candidates(paths: list[str]) -> list[tuple[str, str]]:
    candidates: dict[str, tuple[int, str]] = {}
    for raw_path in paths:
        path = PurePosixPath(raw_path)
        name = path.name.lower()
        suffix = path.suffix.lower()
        segments = lower_segments(path)

        if suffix in BINARY_OR_ASSET_SUFFIXES:
            continue
        if not is_capability_reference(path):
            continue
        if name == "skill.md":
            add_candidate(candidates, str(path.parent), 0, "skill_package_directory")
            continue
        if name in {"package.json", "pyproject.toml", "manifest.json", "plugin.json"} and str(path.parent) != ".":
            add_candidate(candidates, str(path.parent), 1, "manifest_directory")
            continue
        if name.startswith("readme") and str(path.parent) != ".":
            add_candidate(candidates, str(path.parent), 2, "readme_directory")
            continue
        if segments & RELEVANT_SEGMENTS and suffix in TEXTLIKE_SUFFIXES:
            add_candidate(candidates, raw_path, 3, "relevant_tree_path")
            continue
        if suffix in TEXTLIKE_SUFFIXES and str(path.parent) != ".":
            add_candidate(candidates, raw_path, 4, "textlike_tree_path")

    return [
        (reference, basis)
        for reference, (_, basis) in sorted(candidates.items(), key=lambda item: (item[1][0], item[0]))
    ]


def index_link_candidates(checkout: Path) -> list[tuple[str, str]]:
    readme_names = [
        path
        for path in list_tree_paths(checkout)
        if PurePosixPath(path).name.lower().startswith("readme")
    ]
    links: list[str] = []
    for readme_path in readme_names:
        try:
            text = show_file(checkout, readme_path)
        except RuntimeError:
            continue
        for match in GITHUB_URL_PATTERN.finditer(text):
            link = match.group(0).removesuffix(".")
            if any(pattern.search(link) for pattern in PROHIBITED_PUBLIC_REFERENCE_PATTERNS):
                continue
            if link not in links:
                links.append(link)
    return [(f"upstream:{link}", "index_upstream_link") for link in sorted(links)]


def source_candidates(source: dict[str, str]) -> tuple[str, list[tuple[str, str]]]:
    if github_owner_repo(source["source_url"]) is None:
        return "", []
    checkout = ensure_git_tree_cache(source)
    commit = current_commit(checkout)
    if source["sampling_role"] == "discovery_index":
        candidates = index_link_candidates(checkout)
        if candidates:
            return commit, candidates
    return commit, tree_path_candidates(list_tree_paths(checkout))


def build_selection_rows() -> list[dict[str, Any]]:
    allocation_rows = [row for row in read_csv_rows(ALLOCATION_PATH) if int(row["target_artifacts"]) > 0]
    output_rows: list[dict[str, Any]] = []
    global_index = 1

    for source in allocation_rows:
        target = int(source["target_artifacts"])
        commit, candidates = source_candidates(source)
        if not candidates:
            candidates = [(f"pending:{source['source_id']}:{slot:03d}", "target_slot_pending") for slot in range(1, target + 1)]
        selected = candidates[:target]
        if len(selected) < target:
            selected.extend(
                (f"pending:{source['source_id']}:{slot:03d}", "target_slot_pending")
                for slot in range(len(selected) + 1, target + 1)
            )

        for artifact_reference, basis in selected:
            status = "target_slot_pending" if basis == "target_slot_pending" else "metadata_candidate"
            output_rows.append(
                {
                    "artifact_id": f"ext-art-{global_index:03d}",
                    "study_family": source["study_family"],
                    "source_id": source["source_id"],
                    "source_name": source["source_name"],
                    "source_url": source["source_url"],
                    "source_version": commit or "pending_version_pin",
                    "artifact_reference": artifact_reference,
                    "selection_status": status,
                    "selection_basis": basis,
                    "case_count": 4,
                    "condition_evaluation_count": 12,
                    "license_policy": source["license_policy"],
                    "content_boundary": "metadata_only_no_third_party_prose_or_code_copied",
                }
            )
            global_index += 1
    return output_rows


def summarize(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    concrete_rows = [row for row in rows if row["selection_status"] == "metadata_candidate"]
    pending_rows = [row for row in rows if row["selection_status"] == "target_slot_pending"]
    summary_rows: list[dict[str, Any]] = [
        {
            "group": "overall",
            "value": "target_artifacts",
            "metric": "count",
            "count": len(rows),
            "notes": "Target rows in the external allocation, including concrete references and pending replacement slots.",
        },
        {
            "group": "overall",
            "value": "concrete_candidate_references",
            "metric": "count",
            "count": len(concrete_rows),
            "notes": "Concrete metadata-only third-party references selected from source trees or indexes.",
        },
        {
            "group": "overall",
            "value": "pending_replacement_slots",
            "metric": "count",
            "count": len(pending_rows),
            "notes": "Unfilled target slots that require eligibility review and replacement before outcome-bearing execution.",
        },
        {
            "group": "overall",
            "value": "base_cases",
            "metric": "count",
            "count": sum(int(row["case_count"]) for row in rows),
            "notes": "Four base cases are planned per candidate artifact.",
        },
        {
            "group": "overall",
            "value": "condition_evaluations",
            "metric": "count",
            "count": sum(int(row["condition_evaluation_count"]) for row in rows),
            "notes": "Each base case is crossed with three representation conditions.",
        },
    ]

    for key in ("study_family", "source_id", "selection_status", "selection_basis"):
        counts: dict[str, int] = {}
        for row in rows:
            value = str(row[key])
            counts[value] = counts.get(value, 0) + 1
        for value, count in sorted(counts.items()):
            summary_rows.append(
                {
                    "group": key,
                    "value": value,
                    "metric": "count",
                    "count": count,
                    "notes": "",
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


def write_markdown(selection_rows: list[dict[str, Any]], summary_rows: list[dict[str, Any]]) -> None:
    family_rows = [row for row in summary_rows if row["group"] == "study_family"]
    source_rows = [row for row in summary_rows if row["group"] == "source_id"]
    status_rows = [row for row in summary_rows if row["group"] == "selection_basis"]

    lines = [
        "# External Artifact Selection",
        "",
        "This file records metadata-only candidate artifact references and pending replacement slots for the planned external-corpus study. It stores repository paths, upstream links, source versions, and selection bases; it does not copy third-party prose or code.",
        "",
        "## Totals",
        "",
        markdown_table(
            ["Quantity", "Count"],
            [
                ["Target artifact slots", str(len(selection_rows))],
                [
                    "Concrete candidate references",
                    str(sum(1 for row in selection_rows if row["selection_status"] == "metadata_candidate")),
                ],
                [
                    "Pending replacement slots",
                    str(sum(1 for row in selection_rows if row["selection_status"] == "target_slot_pending")),
                ],
                ["Base cases", str(sum(int(row["case_count"]) for row in selection_rows))],
                ["Condition evaluations", str(sum(int(row["condition_evaluation_count"]) for row in selection_rows))],
            ],
        ),
        "",
        "## Families",
        "",
        markdown_table(
            ["Family", "Candidate rows"],
            [[row["value"], str(row["count"])] for row in family_rows],
        ),
        "",
        "## Sources",
        "",
        markdown_table(
            ["Source", "Candidate rows"],
            [[row["value"], str(row["count"])] for row in source_rows],
        ),
        "",
        "## Selection Basis",
        "",
        markdown_table(
            ["Basis", "Candidate rows"],
            [[row["value"], str(row["count"])] for row in status_rows],
        ),
        "",
    ]
    SUMMARY_MD_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    selection_rows = build_selection_rows()
    summary_rows = summarize(selection_rows)
    write_csv(SELECTION_PATH, SELECTION_COLUMNS, selection_rows)
    write_csv(SUMMARY_CSV_PATH, SUMMARY_COLUMNS, summary_rows)
    write_markdown(selection_rows, summary_rows)
    print(f"Wrote {SELECTION_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {SUMMARY_CSV_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {SUMMARY_MD_PATH.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
