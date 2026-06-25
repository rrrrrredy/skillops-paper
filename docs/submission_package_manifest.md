# Submission Package Manifest

Audit date: 2026-06-25

## Immutable Artifact Citation

- GitHub release: https://github.com/rrrrrredy/skillops-paper/releases/tag/v1.1.0
- Zenodo version DOI: https://doi.org/10.5281/zenodo.20844038
- Zenodo concept DOI: https://doi.org/10.5281/zenodo.20061198

The GitHub release assets are the submission binaries named below. If Zenodo
is used as binary provenance rather than citation metadata, verify the
account-side Zenodo file state after any release-asset refresh.

## Files to Submit

| File | Purpose | SHA-256 |
| --- | --- | --- |
| `release/skillops-paper.pdf` | PDF upload for OpenReview or venue review systems | `F9774684EB4BC2CBF42D69DB3C4169436F60B0C72FCA064DE776E615CD851D65` |
| `release/skillops-paper-source.zip` | LaTeX source package for arXiv-style source upload | `0E753376C3C1C16902B3A3BCA08E384AC3EE333CF6AA86A84D6C738710E80A8F` |

Use the attached release assets above as the submission package. Do not use
GitHub's automatic source archives as the arXiv source package; those archives
are repository snapshots for software preservation, while
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
  endorsement or an accepted category route.
- OpenReview: upload `release/skillops-paper.pdf` to a concrete venue or
  workshop invitation and attach supplementary materials only when requested by
  that venue.
- Formal venue submission: use the same PDF and artifact DOI, then adapt format
  only if the target venue requires a template conversion.

## Evidence Boundary

The package supports completed internal benchmarks, local guard checks,
two-provider internal live runs, bounded external smoke, and an auditable
third-party corpus scaffold. It does not claim a completed external human study,
powered external statistical result, or production deployment validation.

## Live Pilot Boundary

The bounded pilot runner is prepared for DeepSeek and Kimi/Moonshot provider
conditions. The current shell environment does not expose provider credentials,
so the latest pilot selection manifest records `not_run_missing_credentials`
instead of model outputs. Set provider keys through a local secret mechanism
before running outcome-bearing pilot slices.
