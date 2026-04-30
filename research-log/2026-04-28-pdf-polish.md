# 2026-04-28 PDF Polish

Repository: `D:\Codex\skillops-paper-artifact-benchmark`
Branch: `pdf-polish`

## Summary

- Hidden hyperlink boxes with `\hypersetup{hidelinks,breaklinks=true}`.
- Added `xurl` before `hyperref` to improve line breaking for URLs and paths.
- Reworked the path-heavy artifact and evaluation passages into break-safe lists
  using `\path{...}`.
- Replaced `\date{\today}` with `\date{April 2026}`.
- Refreshed `release/skillops-paper-source/main.tex` from `paper/main.tex`.
- Kept `release/skillops-paper-source/references.bib` in sync with
  `paper/references.bib`.
- Recreated `release/skillops-paper-source.zip`.

## Validation

- Ran `scripts/run_all.py`.
- Ran `scripts/run_tests.py`.
- Final test result: `22/22` passed.
- Ran static manuscript and package audits for citation coverage, label/reference
  coverage, public-facing wording, author metadata, and absence of direct SVG
  inclusion.

## Remaining Step

- Recompile the refreshed source package in Overleaf to confirm the final PDF
  presentation changes.
