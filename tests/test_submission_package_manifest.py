from __future__ import annotations

import hashlib
import re
import unittest
import zipfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = REPO_ROOT / "docs" / "submission_package_manifest.md"
RELEASE_PDF_PATH = REPO_ROOT / "release" / "skillops-paper.pdf"
RELEASE_SOURCE_ZIP_PATH = REPO_ROOT / "release" / "skillops-paper-source.zip"
RELEASE_SOURCE_DIR = REPO_ROOT / "release" / "skillops-paper-source"

EXPECTED_RELEASE_TAG = "v1.1.0"
EXPECTED_VERSION_DOI = "10.5281/zenodo.20844038"
EXPECTED_CONCEPT_DOI = "10.5281/zenodo.20061198"
OLD_VERSION_DOI = "10.5281/zenodo." + "2083" + "8908"
EXPECTED_ZIP_ENTRIES = {
    "main.tex",
    "main.bbl",
    "README.md",
    "references.bib",
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def manifest_hashes(text: str) -> dict[str, str]:
    rows = re.findall(r"\| `([^`]+)` \| [^|]+ \| `([A-F0-9]{64})` \|", text)
    return {path: digest for path, digest in rows}


class SubmissionPackageManifestTests(unittest.TestCase):
    def test_manifest_exists_and_pins_release_identity(self) -> None:
        text = MANIFEST_PATH.read_text(encoding="utf-8")
        self.assertIn(f"releases/tag/{EXPECTED_RELEASE_TAG}", text)
        self.assertIn(EXPECTED_VERSION_DOI, text)
        self.assertIn(EXPECTED_CONCEPT_DOI, text)

    def test_manifest_hashes_match_release_files(self) -> None:
        hashes = manifest_hashes(MANIFEST_PATH.read_text(encoding="utf-8"))
        self.assertEqual(hashes["release/skillops-paper.pdf"], sha256_file(RELEASE_PDF_PATH))
        self.assertEqual(hashes["release/skillops-paper-source.zip"], sha256_file(RELEASE_SOURCE_ZIP_PATH))

    def test_manifest_records_standalone_compile_check(self) -> None:
        text = MANIFEST_PATH.read_text(encoding="utf-8")
        self.assertIn("Standalone compile check", text)
        self.assertIn("release/skillops-paper-source.zip", text)
        self.assertIn("Tectonic", text)
        self.assertIn("main.pdf", text)

    def test_manifest_distinguishes_submission_assets_from_repository_archives(self) -> None:
        text = " ".join(MANIFEST_PATH.read_text(encoding="utf-8").split())
        self.assertIn("Use the attached release assets", text)
        self.assertIn("Do not use GitHub's automatic source archives", text)
        self.assertIn("curated LaTeX package", text)

    def test_manifest_mentions_bbl_for_arxiv_resilience(self) -> None:
        text = MANIFEST_PATH.read_text(encoding="utf-8")
        self.assertIn("main.bbl", text)
        self.assertIn("arXiv", text)

    def test_source_zip_contents_are_minimal_and_current(self) -> None:
        with zipfile.ZipFile(RELEASE_SOURCE_ZIP_PATH) as package:
            names = set(package.namelist())
            self.assertEqual(names, EXPECTED_ZIP_ENTRIES)
            for name in EXPECTED_ZIP_ENTRIES:
                archived = package.read(name)
                expanded = (RELEASE_SOURCE_DIR / name).read_bytes()
                self.assertEqual(hashlib.sha256(archived).hexdigest(), hashlib.sha256(expanded).hexdigest())

    def test_source_package_contains_current_artifact_citation(self) -> None:
        with zipfile.ZipFile(RELEASE_SOURCE_ZIP_PATH) as package:
            source_text = "\n".join(package.read(name).decode("utf-8") for name in EXPECTED_ZIP_ENTRIES)
        self.assertIn(EXPECTED_RELEASE_TAG, source_text)
        self.assertIn(EXPECTED_VERSION_DOI, source_text)
        self.assertNotIn(OLD_VERSION_DOI, source_text)


if __name__ == "__main__":
    unittest.main()
