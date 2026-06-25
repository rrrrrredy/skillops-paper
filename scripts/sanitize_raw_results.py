from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


SCRIPTS_DIR = Path(__file__).resolve().parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from experiment_utils import RAW_RESULTS_DIR, relative_display, sanitize_provider_response  # noqa: E402


def sanitize_record(record: dict[str, Any]) -> dict[str, Any]:
    raw_output = record.get("raw_output")
    if isinstance(raw_output, dict) and "response_json" in raw_output:
        raw_output["response_json"] = sanitize_provider_response(raw_output["response_json"])
    return record


def sanitize_file(path: Path) -> int:
    records: list[dict[str, Any]] = []
    changed = 0
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            stripped = line.strip()
            if not stripped:
                continue
            record = json.loads(stripped)
            before = json.dumps(record, sort_keys=True)
            sanitized = sanitize_record(record)
            after = json.dumps(sanitized, sort_keys=True)
            if before != after:
                changed += 1
            records.append(sanitized)

    if changed:
        with path.open("w", encoding="utf-8", newline="") as handle:
            for record in records:
                handle.write(json.dumps(record, ensure_ascii=True, sort_keys=True))
                handle.write("\n")
    return changed


def main() -> int:
    total_changed = 0
    for path in sorted(RAW_RESULTS_DIR.glob("*.jsonl")):
        changed = sanitize_file(path)
        total_changed += changed
        if changed:
            print(f"Sanitized {changed} records in {relative_display(path)}")
    print(f"Sanitized records: {total_changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
