# SkillOps Preprint Source Package

This package is a clean LaTeX source bundle for Overleaf upload and later
adaptation for arXiv submission.

## Contents

- Main file: `main.tex`
- Bibliography file: `references.bib`
- Reference artwork: `figures/skillops_lifecycle.svg`,
  `figures/skill_anatomy.svg`, and `figures/evaluation_pipeline.svg`

## Compilation

Compile with `latexmk` when available, or run `pdflatex`, `bibtex`, and then
`pdflatex` twice.

## Figure Handling

The current paper uses LaTeX boxed placeholders for figure compatibility in a
pdflatex-oriented workflow. The SVG files in `figures/` are included as
reference artwork only. The package does not force direct SVG inclusion and
does not require local SVG conversion.

## Repository Materials

Benchmark data, scripts, and generated result tables remain in the main
repository rather than in this upload-focused source package.
