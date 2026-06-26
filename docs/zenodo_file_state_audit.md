# Zenodo File-State Audit

Audit date: 2026-06-26

## Record Checked

| Field | Value |
| --- | --- |
| Zenodo record | `https://zenodo.org/records/20844038` |
| Version DOI | `10.5281/zenodo.20844038` |
| Concept DOI | `10.5281/zenodo.20061198` |
| GitHub release | `https://github.com/rrrrrredy/skillops-paper/releases/tag/v1.1.0` |

## Current Reserved Version

| Field | Value |
| --- | --- |
| Zenodo record | `https://zenodo.org/uploads/20900771` |
| Reserved version DOI | `10.5281/zenodo.20900771` |
| Planned GitHub release | `https://github.com/rrrrrredy/skillops-paper/releases/tag/v1.2.0` |
| Status | Reserved, not file-verified until publish completes. |

## Finding

The authenticated Zenodo account has the repository enabled and the record is published as `v1.1.0`. The Zenodo file area contains one GitHub-integration archive:

| File | Size | MD5 |
| --- | ---: | --- |
| `rrrrrredy/skillops-paper-v1.1.0.zip` | 943028 | `2e10f7b5d8ea9b0e7e1b1ec0b35a4ab5` |

The archive preview includes the repository `release/` directory, but the embedded release assets do not match the current GitHub release assets:

| Asset | Current GitHub release SHA-256 | Zenodo embedded SHA-256 |
| --- | --- | --- |
| `release/skillops-paper.pdf` | `98957f4295eafa777a234a77b9a75afb4de9294b50e60fe5b72565bd788f03b9` | `79fe4794f7788aa44c4438aa7ce8781a9e42ed56f17e3c50922695e085c5ba61` |
| `release/skillops-paper-source.zip` | `38833a57bf1f7001eee72d3cf2ecd8e5e68b559d6dd17832f46f4f8d6fa46974` | `faafae3ceb8cd28d4f0b2caafc3d06fb9fc59c3cbecdfa95e1ea5d427b0ee1b8` |

The Zenodo archive root is `rrrrrredy-skillops-paper-fea8b38`, while the current `v1.1.0` GitHub release target is `ac6d6d66d44fa81caa209fa645b06e0290e8aecb`.

## Consequence

Use `10.5281/zenodo.20844038` only as the archived `v1.1.0` software record. Do not use it as binary provenance for the current PDF and curated source package.

## Required Fix

Publish the reserved `v1.2.0` record with the current PDF/source package, then verify the Zenodo file hashes against `docs/submission_package_manifest.md`.
