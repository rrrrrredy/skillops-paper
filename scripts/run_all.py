from __future__ import annotations

import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = Path(__file__).resolve().parent
RESULTS_DIR = REPO_ROOT / "results" / "tables"
FIGURES_DIR = REPO_ROOT / "figures"


if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import analyze_risk_cases  # noqa: E402
import analyze_structure  # noqa: E402
import analyze_trigger_cases  # noqa: E402
import generate_figures  # noqa: E402


def ensure_output_directories() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)


def main() -> dict[str, object]:
    ensure_output_directories()

    generated_outputs: list[str] = []
    generated_outputs.extend(analyze_structure.main()["outputs"])
    generated_outputs.extend(analyze_trigger_cases.main()["outputs"])
    generated_outputs.extend(analyze_risk_cases.main()["outputs"])
    figure_result = generate_figures.main()
    generated_outputs.extend(figure_result["outputs"])

    print("Generated output paths:")
    for output in generated_outputs:
        print(output)

    return {"outputs": generated_outputs, "figure_backend": figure_result["backend"]}


if __name__ == "__main__":
    main()
