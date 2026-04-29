from __future__ import annotations

import csv
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
BENCHMARK_DIR = REPO_ROOT / "benchmark"
RESULTS_TABLES_DIR = REPO_ROOT / "results" / "tables"
FIGURES_DIR = REPO_ROOT / "figures"
EVIDENCE_DIR = REPO_ROOT / "evidence"
PAPER_PATH = REPO_ROOT / "paper" / "main.tex"
README_PATH = REPO_ROOT / "README.md"

SKILL_SAMPLES_PATH = BENCHMARK_DIR / "skill_samples.csv"
TRIGGER_CASES_PATH = BENCHMARK_DIR / "trigger_cases.csv"
RISK_CASES_PATH = BENCHMARK_DIR / "risk_cases.csv"

ARTIFACT_COVERAGE_CSV = RESULTS_TABLES_DIR / "artifact_coverage.csv"
TRIGGER_SUMMARY_CSV = RESULTS_TABLES_DIR / "trigger_summary.csv"
RISK_SUMMARY_CSV = RESULTS_TABLES_DIR / "risk_summary.csv"

ARTIFACT_COVERAGE_MD = RESULTS_TABLES_DIR / "artifact_coverage.md"
TRIGGER_SUMMARY_MD = RESULTS_TABLES_DIR / "trigger_summary.md"
RISK_SUMMARY_MD = RESULTS_TABLES_DIR / "risk_summary.md"

SKILLOPS_LIFECYCLE_SVG = FIGURES_DIR / "skillops_lifecycle.svg"
SKILL_ANATOMY_SVG = FIGURES_DIR / "skill_anatomy.svg"
EVALUATION_PIPELINE_SVG = FIGURES_DIR / "evaluation_pipeline.svg"

EXECUTION_MATRIX_PATH = EVIDENCE_DIR / "execution_matrix.md"
EXECUTION_LOG_PATH = EVIDENCE_DIR / "execution_log.md"

REQUIRED_OUTPUTS = [
    ARTIFACT_COVERAGE_MD,
    TRIGGER_SUMMARY_MD,
    RISK_SUMMARY_MD,
    ARTIFACT_COVERAGE_CSV,
    TRIGGER_SUMMARY_CSV,
    RISK_SUMMARY_CSV,
    SKILLOPS_LIFECYCLE_SVG,
    SKILL_ANATOMY_SVG,
    EVALUATION_PIPELINE_SVG,
]

PUBLIC_FACING_FILES = [
    README_PATH,
    PAPER_PATH,
    BENCHMARK_DIR / "README.md",
    REPO_ROOT / "artifacts" / "artifact_inventory.md",
]

SKILL_SAMPLE_COLUMNS = [
    "artifact_name",
    "repository_url",
    "purpose",
    "metadata",
    "trigger_contract",
    "instructions",
    "context_boundary",
    "execution_constraints",
    "memory_interface",
    "tests",
    "security_checks",
    "failure_modes",
    "notes",
]

TRIGGER_CASE_COLUMNS = [
    "case_id",
    "user_request",
    "expected_label",
    "relevant_skill",
    "reason",
]

RISK_CASE_COLUMNS = [
    "case_id",
    "risk_type",
    "example",
    "expected_detection",
    "relevant_artifact",
    "reason",
]

ALLOWED_TRIGGER_LABELS = {
    "should_trigger",
    "should_not_trigger",
    "ambiguous",
}

ALLOWED_RISK_TYPES = {
    "prompt_injection",
    "over_broad_trigger",
    "unsafe_file_access",
    "missing_constraints",
    "stale_memory",
    "missing_tests",
    "identity_confusion",
    "privacy_leakage",
}

EXPECTED_TRIGGER_LABEL_COUNTS = {
    "should_trigger": 15,
    "should_not_trigger": 12,
    "ambiguous": 9,
}

EXPECTED_RISK_TYPE_COUNTS = {risk_type: 3 for risk_type in sorted(ALLOWED_RISK_TYPES)}

COMPONENT_ORDER = [
    "metadata",
    "trigger_contract",
    "instructions",
    "context_boundary",
    "execution_constraints",
    "memory_interface",
    "tests",
    "security_checks",
    "failure_modes",
]

COMPONENT_PAPER_LABELS = {
    "metadata": "Metadata",
    "trigger_contract": "Trigger contract",
    "instructions": "Instructions",
    "context_boundary": "Context boundary",
    "execution_constraints": "Execution constraints",
    "memory_interface": "Memory interface",
    "tests": "Tests",
    "security_checks": "Security checks",
    "failure_modes": "Failure modes",
}

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

UNSUPPORTED_TERM_PATTERNS = {
    "statistically significant": re.compile(r"\bstatistically significant\b"),
    "precision": re.compile(r"\bprecision\b"),
    "recall": re.compile(r"\brecall\b"),
    "F1": re.compile(r"\bf1\b"),
    "production validated": re.compile(r"\bproduction validated\b"),
    "user study": re.compile(r"\buser study\b"),
    "model execution": re.compile(r"\bmodel execution\b"),
    "scanner accuracy": re.compile(r"\bscanner accuracy\b"),
    "accuracy": re.compile(r"\baccuracy\b"),
    "improves agent stability": re.compile(r"\bimproves agent stability\b"),
}

SAFE_CLAIM_CONTEXT_PATTERNS = [
    re.compile(r"\bno statistical significance\b"),
    re.compile(r"\bno user study\b"),
    re.compile(r"\bno model execution\b"),
    re.compile(r"\bno scanner accuracy\b"),
    re.compile(r"\bnot measured\b"),
    re.compile(r"\bshould not be read as\b"),
    re.compile(r"\bdoes not measure\b"),
    re.compile(r"\bdo not measure\b"),
    re.compile(r"\bdoes not include\b"),
    re.compile(r"\bdid not run\b"),
    re.compile(r"\bnot run\b"),
    re.compile(r"\bnot multi-model execution performance\b"),
    re.compile(r"\brather than\b"),
    re.compile(r"\bcannot compare\b"),
    re.compile(r"\bno broad empirical validation\b"),
]

PUBLIC_PROCESS_TERMS = [
    "draft",
    "initial",
    "work in progress",
    "paper draft",
    "current stage",
    "next steps",
    "incomplete",
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def read_csv_fieldnames(path: Path) -> list[str]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return reader.fieldnames or []


def normalize_text(text: str) -> str:
    lowered = text.lower().replace("\\_", "_")
    return " ".join(lowered.split())


def latex_texttt(value: str) -> str:
    return value.replace("_", r"\_")


def classify_component_value(component: str, value: str) -> str:
    text = value.strip()
    if not text:
        return "absent"
    for pattern in LIMITED_PATTERNS.get(component, []):
        if pattern.search(text):
            return "limited"
    return "documented"


def expected_artifact_coverage_counts(skill_rows: list[dict[str, str]]) -> dict[str, dict[str, int]]:
    counts: dict[str, dict[str, int]] = {}
    for component in COMPONENT_ORDER:
        statuses = Counter(classify_component_value(component, row[component]) for row in skill_rows)
        counts[component] = {
            "documented_count": statuses["documented"],
            "limited_count": statuses["limited"],
            "absent_count": statuses["absent"],
        }
    return counts


def load_group_counts(path: Path, group_name: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in read_csv_rows(path):
        if row["group"] != group_name:
            continue
        counts[row["value"]] = int(row["count"])
    return counts


def load_artifact_coverage_counts(path: Path) -> dict[str, dict[str, int]]:
    counts: dict[str, dict[str, int]] = {}
    for row in read_csv_rows(path):
        counts[row["component"]] = {
            "documented_count": int(row["documented_count"]),
            "limited_count": int(row["limited_count"]),
            "absent_count": int(row["absent_count"]),
        }
    return counts


def run_pipeline() -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "run_all.py")],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )


def file_is_non_empty(path: Path) -> bool:
    return path.exists() and path.stat().st_size > 0


def parse_svg(path: Path) -> ET.Element:
    return ET.parse(path).getroot()


def svg_text(path: Path) -> str:
    root = parse_svg(path)
    return normalize_text(" ".join(text for text in root.itertext() if text.strip()))


def tag_local_name(tag: str) -> str:
    if "}" in tag:
        return tag.rsplit("}", 1)[1]
    return tag


def unsupported_claim_hits(text: str) -> list[tuple[str, str]]:
    normalized = normalize_text(text)
    hits: list[tuple[str, str]] = []
    for term, pattern in UNSUPPORTED_TERM_PATTERNS.items():
        for match in pattern.finditer(normalized):
            start = max(0, match.start() - 140)
            end = min(len(normalized), match.end() + 140)
            context = normalized[start:end]
            if any(safe_pattern.search(context) for safe_pattern in SAFE_CLAIM_CONTEXT_PATTERNS):
                continue
            hits.append((term, context))
    return hits
