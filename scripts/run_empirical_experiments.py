from __future__ import annotations

import argparse
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = Path(__file__).resolve().parent


if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import check_experiment_readiness  # noqa: E402
import run_ablation_experiment  # noqa: E402
import run_constraint_experiment  # noqa: E402
import run_memory_drift_experiment  # noqa: E402
import run_security_guard_experiment  # noqa: E402
import run_trigger_experiment  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run readiness and empirical experiment harness checks.")
    parser.add_argument("--dry-run", action="store_true", help="Run readiness and dry-run validation.")
    parser.add_argument("--run-live", action="store_true", help="Run live experiment execution after dry-run validation.")
    parser.add_argument("--provider", choices=["openai", "anthropic", "longcat"], help="Preferred provider for model-backed experiments.")
    parser.add_argument("--model", help="Model name for live model-backed experiments.")
    parser.add_argument(
        "--security-guard",
        choices=["local-rules", "model"],
        default="local-rules",
        help="Guard backend for the security experiment during live execution.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.dry_run and not args.run_live:
        args.dry_run = True

    readiness = check_experiment_readiness.run_readiness_check(emit_status=True)
    if not readiness["prepared"]:
        return 1

    trigger_result = run_trigger_experiment.run_experiment(
        dry_run=True,
        run_live=False,
        emit_status=True,
    )
    constraint_result = run_constraint_experiment.run_experiment(
        dry_run=True,
        run_live=False,
        emit_status=True,
    )
    security_result = run_security_guard_experiment.run_experiment(
        dry_run=True,
        run_live=False,
        guard=args.security_guard,
        emit_status=True,
    )
    memory_drift_result = run_memory_drift_experiment.run_experiment(
        dry_run=True,
        run_live=False,
        emit_status=True,
    )
    ablation_result = run_ablation_experiment.run_experiment(
        dry_run=True,
        run_live=False,
        emit_status=True,
    )

    if not args.run_live:
        return 0

    run_trigger_experiment.run_experiment(
        dry_run=False,
        run_live=True,
        provider=args.provider,
        model=args.model,
        emit_status=True,
    )
    run_constraint_experiment.run_experiment(
        dry_run=False,
        run_live=True,
        provider=args.provider,
        model=args.model,
        emit_status=True,
    )
    run_security_guard_experiment.run_experiment(
        dry_run=False,
        run_live=True,
        guard=args.security_guard,
        provider=args.provider,
        model=args.model,
        emit_status=True,
    )
    run_memory_drift_experiment.run_experiment(
        dry_run=False,
        run_live=True,
        provider=args.provider,
        model=args.model,
        emit_status=True,
    )
    run_ablation_experiment.run_experiment(
        dry_run=False,
        run_live=True,
        provider=args.provider,
        model=args.model,
        emit_status=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
