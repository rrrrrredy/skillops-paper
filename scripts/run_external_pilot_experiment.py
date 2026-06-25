from __future__ import annotations

import argparse

from external_pilot_runner_utils import (
    LIVE_MANIFEST_CSV_PATH,
    LIVE_MANIFEST_MD_PATH,
    MAX_DEFAULT_LIVE_ROWS,
    PILOT_MODEL_PLAN_PATH,
    PLAN_COLUMNS,
    PROVIDER_SPECS,
    READINESS_CSV_PATH,
    READINESS_MD_PATH,
    REPO_ROOT,
    RUN_PLAN_CSV_PATH,
    RUN_PLAN_MD_PATH,
    build_plan_rows,
    completed_keys,
    credential_available,
    load_payload_lookup,
    read_csv_rows,
    run_live,
    select_rows,
    write_csv_rows,
    write_plan_markdown,
    write_readiness,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Prepare or run bounded live execution for the external pilot plan.")
    parser.add_argument("--dry-run", action="store_true", help="Write not-run plan and provider readiness files.")
    parser.add_argument("--run-live", action="store_true", help="Run a bounded live pilot slice.")
    parser.add_argument("--provider", choices=sorted(PROVIDER_SPECS), help="Provider to run or filter.")
    parser.add_argument("--model", help="Optional model override or filter.")
    parser.add_argument("--sample-limit", type=int, help="Maximum selected rows.")
    parser.add_argument("--max-live-rows", type=int, default=MAX_DEFAULT_LIVE_ROWS)
    parser.add_argument("--no-resume", action="store_true", help="Do not skip completed pilot rows.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.dry_run and not args.run_live:
        args.dry_run = True
    if args.run_live and args.dry_run:
        raise ValueError("Use either --dry-run or --run-live, not both")
    if args.max_live_rows < 1:
        raise ValueError("max-live-rows must be positive")

    all_rows = read_csv_rows(PILOT_MODEL_PLAN_PATH)
    payload_lookup = load_payload_lookup()
    completed = completed_keys()
    write_readiness(all_rows, completed)

    if args.dry_run:
        selected = select_rows(all_rows, args.provider, args.model, args.sample_limit, completed, resume=False)
        plan_rows = build_plan_rows(selected, payload_lookup, completed, run_status="not_run")
        write_csv_rows(RUN_PLAN_CSV_PATH, PLAN_COLUMNS, plan_rows)
        write_plan_markdown(
            RUN_PLAN_MD_PATH,
            "External Pilot Run Plan",
            "This plan consumes the seeded 24-artifact pilot and records not-run provider-condition rows. It does not report external effect estimates.",
            plan_rows,
        )
        for path in (RUN_PLAN_CSV_PATH, RUN_PLAN_MD_PATH, READINESS_CSV_PATH, READINESS_MD_PATH):
            print(f"Wrote {path.relative_to(REPO_ROOT)}")
        return 0

    if args.provider is None:
        raise ValueError("Live pilot execution requires --provider")
    model = args.model or PROVIDER_SPECS[args.provider][0]
    if args.sample_limit is None:
        raise ValueError("Live pilot execution requires --sample-limit")
    selected = select_rows(all_rows, args.provider, model, args.sample_limit, completed, resume=not args.no_resume)
    if not selected:
        raise ValueError("No pending pilot rows selected")
    if len(selected) > args.max_live_rows:
        raise ValueError(f"Refusing to run {len(selected)} rows; max-live-rows is {args.max_live_rows}")

    if not credential_available(args.provider):
        manifest_rows = build_plan_rows(selected, payload_lookup, completed, run_status="not_run_missing_credentials")
        write_csv_rows(LIVE_MANIFEST_CSV_PATH, PLAN_COLUMNS, manifest_rows)
        write_plan_markdown(
            LIVE_MANIFEST_MD_PATH,
            "External Pilot Live Manifest",
            "This manifest records a bounded live pilot selection that was not run because credentials were unavailable.",
            manifest_rows,
        )
        for path in (LIVE_MANIFEST_CSV_PATH, LIVE_MANIFEST_MD_PATH):
            print(f"Wrote {path.relative_to(REPO_ROOT)}")
        return 0

    output_path = run_live(selected, payload_lookup, args.provider, model)
    raw_display = str(output_path.relative_to(REPO_ROOT))
    manifest_rows = build_plan_rows(selected, payload_lookup, completed, run_status="submitted_bounded_live", raw_output_path=raw_display)
    write_csv_rows(LIVE_MANIFEST_CSV_PATH, PLAN_COLUMNS, manifest_rows)
    write_plan_markdown(
        LIVE_MANIFEST_MD_PATH,
        "External Pilot Live Manifest",
        "This manifest records a bounded pilot slice. It is logistics evidence, not an external effect estimate.",
        manifest_rows,
    )
    for path in (output_path, LIVE_MANIFEST_CSV_PATH, LIVE_MANIFEST_MD_PATH):
        print(f"Wrote {path.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
