# Zenodo File-State Audit

Audit date: 2026-06-26

## Historical Record Checked

| Field | Value |
| --- | --- |
| Zenodo record | `https://zenodo.org/records/20844038` |
| Version DOI | `10.5281/zenodo.20844038` |
| Concept DOI | `10.5281/zenodo.20061198` |
| GitHub release | `https://github.com/rrrrrredy/skillops-paper/releases/tag/v1.1.0` |

The authenticated Zenodo account has the repository enabled. The historical
`v1.1.0` record contains one GitHub-integration archive:

| File | Size | MD5 |
| --- | ---: | --- |
| `rrrrrredy/skillops-paper-v1.1.0.zip` | 943028 | `2e10f7b5d8ea9b0e7e1b1ec0b35a4ab5` |

The archive preview includes the repository `release/` directory, but the
embedded release assets do not match the current `v1.2.0` release assets:

| Asset | Current release SHA-256 | Historical embedded SHA-256 |
| --- | --- | --- |
| `release/skillops-paper.pdf` | `98957f4295eafa777a234a77b9a75afb4de9294b50e60fe5b72565bd788f03b9` | `79fe4794f7788aa44c4438aa7ce8781a9e42ed56f17e3c50922695e085c5ba61` |
| `release/skillops-paper-source.zip` | `38833a57bf1f7001eee72d3cf2ecd8e5e68b559d6dd17832f46f4f8d6fa46974` | `faafae3ceb8cd28d4f0b2caafc3d06fb9fc59c3cbecdfa95e1ea5d427b0ee1b8` |

Use `10.5281/zenodo.20844038` only as the archived `v1.1.0` software
record. Do not use it as binary provenance for the current PDF/source package.

## Current Published Version

| Field | Value |
| --- | --- |
| Zenodo record | `https://zenodo.org/records/20900771` |
| Version DOI | `10.5281/zenodo.20900771` |
| Concept DOI | `10.5281/zenodo.20061198` |
| GitHub release | `https://github.com/rrrrrredy/skillops-paper/releases/tag/v1.2.0` |
| Status | Published and file-verified. |

Zenodo's GitHub integration ingested the `v1.2.0` GitHub release and published
one repository archive:

| File | Size | MD5 |
| --- | ---: | --- |
| `rrrrrredy/skillops-paper-v1.2.0.zip` | 925624 | `92928f0890c188251ea930e6975d48e3` |

The downloaded archive root is `rrrrrredy-skillops-paper-00824b0`. Its embedded
release assets match the local submission package:

| Embedded asset | Embedded SHA-256 | Expected SHA-256 |
| --- | --- | --- |
| `release/skillops-paper.pdf` | `98957f4295eafa777a234a77b9a75afb4de9294b50e60fe5b72565bd788f03b9` | `98957f4295eafa777a234a77b9a75afb4de9294b50e60fe5b72565bd788f03b9` |
| `release/skillops-paper-source.zip` | `38833a57bf1f7001eee72d3cf2ecd8e5e68b559d6dd17832f46f4f8d6fa46974` | `38833a57bf1f7001eee72d3cf2ecd8e5e68b559d6dd17832f46f4f8d6fa46974` |

The embedded `release/main.bbl` contains `v1.2.0` and does not contain
`v1.1.0`.

## Consequence

The `v1.2.0` Zenodo record is the immutable public archive for the release
family and is binary provenance for the embedded current PDF/source package.
For arXiv submission, still use the curated release asset
`release/skillops-paper-source.zip` rather than Zenodo's repository archive.
