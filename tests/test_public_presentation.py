from __future__ import annotations

import zipfile
import unittest

from tests.helpers import (
    PAPER_PATH,
    PUBLIC_FACING_FILES,
    PUBLIC_PROCESS_TERMS,
    PUBLIC_TRACE_TERMS,
    README_PATH,
    RELEASE_PDF_PATH,
    RELEASE_SOURCE_ZIP_PATH,
    file_is_non_empty,
    read_text,
)


class PublicPresentationTests(unittest.TestCase):
    def test_paper_identity_and_repository_link(self) -> None:
        paper_text = read_text(PAPER_PATH)
        self.assertIn("Song Luo", paper_text)
        self.assertIn("luosongred@gmail.com", paper_text)
        self.assertIn("https://github.com/rrrrrredy", paper_text)
        self.assertNotIn("Independent Researcher", paper_text)

    def test_readme_avoids_prepublication_positioning(self) -> None:
        readme_text = read_text(README_PATH).lower()
        for term in ("dr" + "aft", "initial version", "work in " + "progress", "paper " + "dr" + "aft"):
            self.assertNotIn(term, readme_text)

    def test_public_facing_files_avoid_prohibited_process_terms(self) -> None:
        for path in PUBLIC_FACING_FILES:
            text = read_text(path).lower()
            for term in PUBLIC_PROCESS_TERMS:
                self.assertNotIn(term, text, f"Found prohibited public term {term!r} in {path}")
            for term in PUBLIC_TRACE_TERMS:
                self.assertNotIn(term, text, f"Found prohibited trace term {term!r} in {path}")

    def test_release_artifacts_exist(self) -> None:
        self.assertTrue(file_is_non_empty(RELEASE_PDF_PATH))
        self.assertTrue(file_is_non_empty(RELEASE_SOURCE_ZIP_PATH))

    def test_release_pdf_text_and_metadata_are_clean(self) -> None:
        try:
            from PyPDF2 import PdfReader
        except ImportError as exc:
            self.skipTest(f"PDF text extraction dependency unavailable: {exc}")

        reader = PdfReader(str(RELEASE_PDF_PATH))
        text = "\n".join(page.extract_text() or "" for page in reader.pages).lower()
        metadata = "\n".join(str(value) for value in dict(reader.metadata or {}).values()).lower()
        combined = f"{text}\n{metadata}"
        for term in PUBLIC_PROCESS_TERMS + PUBLIC_TRACE_TERMS:
            self.assertNotIn(term, combined, f"Found prohibited term {term!r} in release PDF")

    def test_release_source_package_is_complete_and_clean(self) -> None:
        with zipfile.ZipFile(RELEASE_SOURCE_ZIP_PATH) as package:
            names = set(package.namelist())
            self.assertIn("main.tex", names)
            self.assertIn("main.bbl", names)
            self.assertIn("references.bib", names)
            self.assertIn("README.md", names)
            for name in sorted(names):
                if not name.endswith((".tex", ".bib", ".md")):
                    continue
                text = package.read(name).decode("utf-8").lower()
                for term in PUBLIC_PROCESS_TERMS + PUBLIC_TRACE_TERMS:
                    self.assertNotIn(term, text, f"Found prohibited term {term!r} in {name}")


if __name__ == "__main__":
    unittest.main()
