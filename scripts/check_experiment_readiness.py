from __future__ import annotations

import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = Path(__file__).resolve().parent


if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from experiment_utils import (  # noqa: E402
    BENCHMARK_DIR,
    PROMPTS_DIR,
    RAW_RESULTS_DIR,
    RESULTS_DIR,
    SCHEMAS_DIR,
    detect_provider_env_vars,
    ensure_directories,
    relative_display,
)


INPUT_PATHS = [
    BENCHMARK_DIR / "trigger_cases.csv",
    BENCHMARK_DIR / "risk_cases.csv",
    BENCHMARK_DIR / "skill_samples.csv",
]

PROMPT_PATHS = [
    PROMPTS_DIR / "trigger_routing_skillops.md",
    PROMPTS_DIR / "trigger_routing_freeform.md",
    PROMPTS_DIR / "constraint_skillops.md",
    PROMPTS_DIR / "constraint_vague.md",
    PROMPTS_DIR / "security_guard_detection.md",
]

SCHEMA_PATHS = [
    SCHEMAS_DIR / "trigger_result_schema.json",
    SCHEMAS_DIR / "constraint_result_schema.json",
    SCHEMAS_DIR / "security_guard_result_schema.json",
]


def run_readiness_check(emit_status: bool = True) -> dict[str, object]:
    ensure_directories([RESULTS_DIR, RAW_RESULTS_DIR])
    statuses: list[tuple[Path, bool]] = []
    for path in [*INPUT_PATHS, *PROMPT_PATHS, *SCHEMA_PATHS]:
        statuses.append((path, path.exists()))

    credentials = detect_provider_env_vars()
    prepared = all(is_present for _, is_present in statuses)

    if emit_status:
        print(f"Experiment readiness: {'prepared' if prepared else 'not ready'}")
        print("Input files:")
        for path in INPUT_PATHS:
            print(f"- {relative_display(path)}: {'present' if path.exists() else 'missing'}")
        print("Prompt files:")
        for path in PROMPT_PATHS:
            print(f"- {relative_display(path)}: {'present' if path.exists() else 'missing'}")
        print("Schema files:")
        for path in SCHEMA_PATHS:
            print(f"- {relative_display(path)}: {'present' if path.exists() else 'missing'}")
        print("Result directories:")
        print(f"- {relative_display(RESULTS_DIR)}: present")
        print(f"- {relative_display(RAW_RESULTS_DIR)}: present")
        print("Provider credentials:")
        for env_name, present in credentials.items():
            print(f"- {env_name}: {'present' if present else 'absent'}")

    return {
        "prepared": prepared,
        "credentials": credentials,
        "missing_paths": [
            relative_display(path)
            for path, is_present in statuses
            if not is_present
        ],
    }


def main() -> int:
    result = run_readiness_check()
    return 0 if result["prepared"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
