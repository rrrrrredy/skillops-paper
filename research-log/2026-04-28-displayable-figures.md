# Displayable Figures Integration

Date: 2026-04-28

## Figure strategy used

- Replaced the three boxed figure notes in `paper/main.tex` with
  LaTeX-native diagrams built from `\fbox`, `\parbox`, `tabular`, and arrow
  symbols that are compatible with a standard pdflatex workflow on Overleaf.
- Kept the figure content schematic and descriptive so the rendered diagrams
  match the paper's existing claims without changing benchmark data or adding
  unsupported results.

## Why SVG conversion was not required

- The paper now renders each conceptual figure directly in LaTeX, so PDF
  output no longer depends on local SVG-to-PDF or SVG-to-PNG conversion.
- The repository SVG files remain available as separate artwork under
  `figures/`, but they are no longer required for the PDF-visible diagrams in
  `paper/main.tex`.

## Figures updated

- `fig:skill-anatomy`
- `fig:skillops-lifecycle`
- `fig:evaluation-pipeline`

## Tests run

- `C:\Users\luosong03\AppData\Local\Programs\Python\Python311\python.exe scripts\run_all.py`
- `C:\Users\luosong03\AppData\Local\Programs\Python\Python311\python.exe scripts\run_tests.py`

## Static checks

- Verified that every citation key referenced in `paper/main.tex` exists in
  `paper/references.bib`.
- Verified that every `\ref{...}` target in `paper/main.tex` has a matching
  `\label{...}`.
- Verified that no public-facing TODO remains.
- Verified that `Independent Researcher` does not appear.
- Verified that `paper/main.tex` contains no direct SVG inclusion and no
  `\includesvg`.
- Verified that benchmark numbers in the paper remain unchanged.
- Verified that the author email and GitHub profile remain present.

## Remaining blocker

- Overleaf PDF compilation is still required because a local LaTeX compiler
  was not available in this environment.
