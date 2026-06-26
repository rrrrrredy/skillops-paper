from __future__ import annotations

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
AUDIT_PATH = REPO_ROOT / "docs" / "zenodo_file_state_audit.md"
READINESS_PATH = REPO_ROOT / "docs" / "publication_readiness.md"


class ZenodoFileStateAuditTests(unittest.TestCase):
    def test_audit_records_checked_doi_and_mismatch(self) -> None:
        text = AUDIT_PATH.read_text(encoding="utf-8")
        self.assertIn("10.5281/zenodo.20844038", text)
        self.assertIn("10.5281/zenodo.20900771", text)
        self.assertIn("v1.2.0", text)
        self.assertIn("2e10f7b5d8ea9b0e7e1b1ec0b35a4ab5", text)
        self.assertIn("92928f0890c188251ea930e6975d48e3", text)
        self.assertIn("rrrrrredy-skillops-paper-00824b0", text)
        self.assertIn("98957f4295eafa777a234a77b9a75afb4de9294b50e60fe5b72565bd788f03b9", text)
        self.assertIn("38833a57bf1f7001eee72d3cf2ecd8e5e68b559d6dd17832f46f4f8d6fa46974", text)
        self.assertIn("79fe4794f7788aa44c4438aa7ce8781a9e42ed56f17e3c50922695e085c5ba61", text)
        self.assertIn("faafae3ceb8cd28d4f0b2caafc3d06fb9fc59c3cbecdfa95e1ea5d427b0ee1b8", text)
        self.assertIn("Do not use it as binary provenance", text)

    def test_readiness_marks_current_zenodo_as_verified(self) -> None:
        text = READINESS_PATH.read_text(encoding="utf-8")
        self.assertIn("Zenodo file-state audit", text)
        self.assertIn("Published and verified", text)
        self.assertIn("embedded PDF/source assets match", text)


if __name__ == "__main__":
    unittest.main()
