from __future__ import annotations

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
RUNBOOK_PATH = REPO_ROOT / "docs" / "secure_live_experiment_runbook.md"
GITIGNORE_PATH = REPO_ROOT / ".gitignore"


class SecureLiveExperimentRunbookTests(unittest.TestCase):
    def test_runbook_exists_and_names_bounded_commands(self) -> None:
        text = RUNBOOK_PATH.read_text(encoding="utf-8")
        self.assertIn("scripts/run_external_pilot_experiment.py --dry-run", text)
        self.assertIn("--sample-limit 4 --max-live-rows 4", text)
        self.assertIn("scripts/run_tests.py", text)

    def test_runbook_forbids_secret_values_in_outputs(self) -> None:
        text = " ".join(RUNBOOK_PATH.read_text(encoding="utf-8").lower().split())
        self.assertIn("never commit api keys", text)
        self.assertIn("never credential values", text)
        self.assertIn("do not paste key values into commands", text)
        self.assertIn("secret scan", text)

    def test_gitignore_covers_local_secret_patterns(self) -> None:
        ignored = set(GITIGNORE_PATH.read_text(encoding="utf-8").splitlines())
        for pattern in (
            ".env",
            ".env.*",
            "!.env.example",
            "*.local.env",
            "*.secret",
            "*.secrets",
            "secrets/",
            "local-secrets/",
        ):
            self.assertIn(pattern, ignored)


if __name__ == "__main__":
    unittest.main()
