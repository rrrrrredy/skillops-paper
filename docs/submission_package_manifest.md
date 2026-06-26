# Submission Package Manifest

Audit date: 2026-06-25

## Artifact Citation State

- Published reference release: https://github.com/rrrrrredy/skillops-paper/releases/tag/v1.2.0
- Published reference DOI: https://doi.org/10.5281/zenodo.20900771
- Target release: https://github.com/rrrrrredy/skillops-paper/releases/tag/v1.3.0
- Zenodo concept DOI: https://doi.org/10.5281/zenodo.20061198
- Next-release DOI: fill after publishing the updated GitHub release and
  verifying the new Zenodo file state.

The local files below are the current submission package. They supersede the
published `v1.2.0` package and must receive a new GitHub release tag and Zenodo
version DOI before the DOI is cited as binary provenance. The account-side
Zenodo file-state audit found that prior DOI `10.5281/zenodo.20844038`
archives an older GitHub snapshot; the `v1.2.0` DOI remains valid for the
previous published package, not for the local hashes below.

## Files to Submit

| File | Purpose | SHA-256 |
| --- | --- | --- |
| `release/skillops-paper.pdf` | PDF upload for OpenReview or venue review systems | `687B3952611A176BAB23A2A2C223D29B5BBF1C63903080B08EA2051A57542F3D` |
| `release/skillops-paper-source.zip` | LaTeX source package for arXiv-style source upload | `0A41FA212495EFBDE0C7D9166F2DEBE4E5517C8CD4185B00634F551382A917CE` |

Use the local files above as the submission package after the next release is
published and file-verified. Do not use GitHub's automatic source archives as
the arXiv source package; those archives are repository snapshots for software preservation, while
`release/skillops-paper-source.zip` is the curated LaTeX package.

The source package contains `main.tex`, `main.bbl`, `references.bib`, and
`README.md`. The paper source has no external figures or auxiliary TeX inputs;
it uses BibTeX with `references.bib`, while `main.bbl` is included to make the
arXiv bibliography path deterministic.

Standalone compile check: extracting `release/skillops-paper-source.zip` into a
clean temporary directory outside the repository and running Tectonic on
`main.tex` successfully produced `main.pdf` on 2026-06-26.

## Submission Routes

- arXiv: upload `release/skillops-paper-source.zip` after confirming category
  endorsement or an accepted category route, and after replacing the artifact
  citation with the next verified DOI.
- OpenReview: upload `release/skillops-paper.pdf` to a concrete venue or
  workshop invitation and attach supplementary materials only when requested by
  that venue.
- Formal venue submission: use the same PDF and the next verified artifact
  DOI, then adapt format only if the target venue requires a template
  conversion.

## Evidence Boundary

The package supports completed internal benchmarks, local guard checks,
two-provider internal live runs, bounded external smoke, an auditable
third-party corpus scaffold, primary machine-checkable external-smoke metrics,
and an LLM-as-judge case-label sensitivity plan. It does not claim completed
powered external statistical validation, broad user-study outcomes, or
production deployment validation.

## Live Pilot Boundary

The bounded pilot runner is prepared for DeepSeek and Kimi/Moonshot provider
conditions. The current shell environment does not expose provider credentials,
so the latest pilot selection manifest records `not_run_missing_credentials`
instead of model outputs. Set provider keys through a local secret mechanism
before running outcome-bearing pilot slices.
