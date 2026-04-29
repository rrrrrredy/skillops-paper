from __future__ import annotations

import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
TESTS_DIR = REPO_ROOT / "tests"


if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


def iter_tests(suite: unittest.TestSuite):
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            yield from iter_tests(item)
        else:
            yield item


class ReportingResult(unittest.TestResult):
    def __init__(self) -> None:
        super().__init__()
        self.records: list[tuple[str, str, str]] = []

    def addSuccess(self, test: unittest.case.TestCase) -> None:
        super().addSuccess(test)
        self.records.append(("PASS", test.id(), ""))

    def addFailure(self, test: unittest.case.TestCase, err) -> None:
        super().addFailure(test, err)
        self.records.append(("FAIL", test.id(), self._exc_info_to_string(err, test)))

    def addError(self, test: unittest.case.TestCase, err) -> None:
        super().addError(test, err)
        self.records.append(("ERROR", test.id(), self._exc_info_to_string(err, test)))

    def addSkip(self, test: unittest.case.TestCase, reason: str) -> None:
        super().addSkip(test, reason)
        self.records.append(("SKIP", test.id(), reason))


def main() -> int:
    loader = unittest.TestLoader()
    suite = loader.discover(str(TESTS_DIR))
    expected_count = sum(1 for _ in iter_tests(suite))

    result = ReportingResult()
    suite.run(result)

    for status, test_id, details in result.records:
        print(f"{status}: {test_id}")
        if details and status in {"FAIL", "ERROR"}:
            print(details.rstrip())
        elif details and status == "SKIP":
            print(f"  reason: {details}")

    failed = len(result.failures)
    errored = len(result.errors)
    skipped = len(result.skipped)
    passed = len(result.records) - failed - errored - skipped

    print("")
    print("Final summary:")
    print(f"- tests discovered: {expected_count}")
    print(f"- passed: {passed}")
    print(f"- failed: {failed}")
    print(f"- errors: {errored}")
    print(f"- skipped: {skipped}")

    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
