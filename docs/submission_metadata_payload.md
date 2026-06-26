# Submission Metadata Payload

Audit date: 2026-06-26

Use this file as the copy-ready metadata source for arXiv, OpenReview, and
venue submission systems. The upload files and hashes are fixed in
`docs/submission_package_manifest.md`.

## Core Metadata

| Field | Value |
| --- | --- |
| Title | SkillOps: A Practical Framework for Designing, Testing, and Operating Modular Skills in Personal AI Agents |
| Author | Song Luo |
| Contact | luosongred@gmail.com |
| Manuscript date | June 2026 |
| Target release | https://github.com/rrrrrredy/skillops-paper/releases/tag/v1.3.0 |
| Published reference release | https://github.com/rrrrrredy/skillops-paper/releases/tag/v1.2.0 |
| Published reference DOI | https://doi.org/10.5281/zenodo.20900771 |
| Concept DOI | https://doi.org/10.5281/zenodo.20061198 |
| Next-release DOI | Fill after publishing and verifying the next GitHub/Zenodo release. |
| PDF asset | `release/skillops-paper.pdf` |
| arXiv source asset | `release/skillops-paper-source.zip` |

## Abstract

Personal AI agents increasingly rely on reusable capability modules, often
called skills, yet their design and operation remain largely informal. This
paper introduces SkillOps, a practical framework for designing, testing, and
operating modular skills in personal AI agents. The framework is derived from
open-source artifacts developed by the author and contributes a skill component
taxonomy, a lifecycle model, a failure-mode taxonomy, a design-gap matrix, and
an artifact-based evaluation design. The paper reports completed descriptive
summaries, repository-level consistency checks, a local security-guard pilot,
and live model-backed runs with DeepSeek and Kimi over trigger, constraint,
security, and memory-drift protocols. It also reports an external-validation
readiness layer: a metadata-only third-party corpus protocol, a seeded
24-artifact pilot plan, bounded runner readiness, machine-checkable external
smoke metrics, and an LLM-as-judge case-label sensitivity plan. The
contribution is therefore a bounded engineering
framework for making agent skills more explicit, testable, and maintainable,
not a claim that a particular skill format universally improves model behavior.

## arXiv Fields

| Field | Recommended value |
| --- | --- |
| Primary category | `cs.SE` |
| Optional cross-list | `cs.AI` if agent-reliability framing is emphasized; `cs.HC` only after user-facing evaluation evidence is collected |
| Comments | Source package and reproducibility artifacts available at the verified GitHub/Zenodo release; powered external statistical validation and broad user-study outcomes are not claimed. |
| Report number | Leave blank unless a venue or institution assigns one. |
| Journal reference | Leave blank unless accepted by a venue. |
| License | Choose the author's intended arXiv license at upload time. |

## OpenReview And Venue Fields

| Field | Recommended value |
| --- | --- |
| Keywords | personal AI agents; agent skills; software engineering for AI agents; artifact lifecycle; reproducibility; evaluation harnesses; operational safety |
| Subject areas | AI agents; software engineering for AI; human-agent interaction; evaluation and reproducibility; tool-use systems |
| Artifact link | Use `https://github.com/rrrrrredy/skillops-paper/releases/tag/v1.3.0`; add the Zenodo version DOI after verification. |
| Supplementary material | Use `release/skillops-paper-source.zip` only when source or supplementary upload is requested. |
| Conflict and policy fields | Complete inside the authenticated venue form. |

## Evidence Boundary For Submission Forms

Use the following boundary when a form asks for limitations, ethics, or
artifact claims:

This submission reports a personal-agent artifact lifecycle framework with
completed internal benchmarks, local guard checks, two-provider internal live
runs, bounded external smoke, machine-checkable external-smoke metrics, and an
auditable third-party corpus scaffold. It does not report a completed powered
external study, production deployment validation, or broad user-study outcome.

## Account-Side Checks

- Use the curated PDF and source zip, not GitHub's automatic source archives,
  for submission upload.
- Publish and verify the next GitHub/Zenodo release before citing the artifact
  DOI for the local hashes in `docs/submission_package_manifest.md`.
- Confirm arXiv endorsement, category, license, and final submission action
  inside the author's account.
- Confirm OpenReview venue invitation, anonymity policy, author profile,
  conflicts, and declarations inside the venue form.
- Verify Zenodo file state from the authenticated account if DOI file
  provenance is required after a release-asset refresh.
