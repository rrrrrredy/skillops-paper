from __future__ import annotations

import shutil
import zipfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
RELEASE_DIR = REPO_ROOT / "release"
COMPILED_PDF = RELEASE_DIR / "main.pdf"
PUBLIC_PDF = RELEASE_DIR / "skillops-paper.pdf"
SOURCE_DIR = RELEASE_DIR / "skillops-paper-source"
SOURCE_ZIP = RELEASE_DIR / "skillops-paper-source.zip"

SOURCE_FILES = [
    (REPO_ROOT / "paper" / "main.tex", "main.tex"),
    (REPO_ROOT / "paper" / "references.bib", "references.bib"),
    (REPO_ROOT / "README.md", "README.md"),
]


def _assert_release_child(path: Path) -> None:
    resolved_release = RELEASE_DIR.resolve()
    resolved_path = path.resolve()
    if resolved_path != resolved_release and resolved_release not in resolved_path.parents:
        raise RuntimeError(f"Refusing to modify path outside release directory: {resolved_path}")


def main() -> int:
    RELEASE_DIR.mkdir(parents=True, exist_ok=True)
    if COMPILED_PDF.exists():
        shutil.copy2(COMPILED_PDF, PUBLIC_PDF)
    elif not PUBLIC_PDF.exists():
        raise FileNotFoundError(f"Missing compiled PDF: {COMPILED_PDF}")

    _assert_release_child(SOURCE_DIR)
    if SOURCE_DIR.exists():
        shutil.rmtree(SOURCE_DIR)
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)

    for source_path, archive_name in SOURCE_FILES:
        if not source_path.exists():
            raise FileNotFoundError(f"Missing source file: {source_path}")
        shutil.copy2(source_path, SOURCE_DIR / archive_name)

    _assert_release_child(SOURCE_ZIP)
    if SOURCE_ZIP.exists():
        SOURCE_ZIP.unlink()
    with zipfile.ZipFile(SOURCE_ZIP, "w", compression=zipfile.ZIP_DEFLATED) as package:
        for _, archive_name in SOURCE_FILES:
            package.write(SOURCE_DIR / archive_name, archive_name)

    print(f"Wrote {PUBLIC_PDF.relative_to(REPO_ROOT)}")
    print(f"Wrote {SOURCE_ZIP.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
