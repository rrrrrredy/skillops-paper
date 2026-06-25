from __future__ import annotations

import unittest

from tests.helpers import EXECUTION_LOG_PATH, EXECUTION_MATRIX_PATH, normalize_text, read_text


class EvidenceMatrixTests(unittest.TestCase):
    def test_required_evidence_files_exist(self) -> None:
        self.assertTrue(EXECUTION_MATRIX_PATH.exists(), f"Missing {EXECUTION_MATRIX_PATH}")
        self.assertTrue(EXECUTION_LOG_PATH.exists(), f"Missing {EXECUTION_LOG_PATH}")

    def test_execution_matrix_includes_status_distinctions(self) -> None:
        text = normalize_text(read_text(EXECUTION_MATRIX_PATH))
        self.assertIn("| passed |", text)
        self.assertIn("| not run |", text)

    def test_execution_matrix_states_missing_execution_layers(self) -> None:
        text = normalize_text(read_text(EXECUTION_MATRIX_PATH))
        self.assertIn("model execution was not run", text)
        self.assertIn("scanner accuracy was not measured", text)
        self.assertIn("user study and production validation were not run", text)


if __name__ == "__main__":
    unittest.main()
