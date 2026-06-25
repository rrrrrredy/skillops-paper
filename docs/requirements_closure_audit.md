# Requirements Closure Audit

Audit date: 2026-06-26

This audit maps the full author request to repository evidence. It separates
supported paper claims from account-side, credential-side, and human-subject
work that cannot be completed inside the repository.

## Status Legend

| Status | Meaning |
| --- | --- |
| Supported | Repository evidence, tests, or release assets support the item. |
| Bounded | The repository contains protocol, package, or runner support, but the remaining action depends on credentials, accounts, venue state, or external reviewers. |
| Not claimable | The item is intentionally excluded from paper claims until new evidence exists. |

## Request Closure Matrix

| Request | Status | Evidence | Remaining boundary |
| --- | --- | --- | --- |
| Paper review, code review, and necessary artifact review | Supported | `docs/change_inventory.md`, `evidence/execution_log.md`, `results/test_report.md`, `tests/` | External peer review is not included. |
| Update body, practice, tests, references, and release package | Supported | `paper/main.tex`, `paper/references.bib`, `release/skillops-paper.pdf`, `release/skillops-paper-source.zip` | Venue-specific formatting remains target-dependent. |
| Add experiment design and run feasible experiments | Supported | `experiments/`, `scripts/run_*_experiment.py`, `results/experiments/live_model_summary.md`, `results/experiments/external_result_summary.md` | Powered external execution is reserved for the planned follow-up. |
| Provide an ordered work list | Supported | `docs/publication_readiness.md`, `docs/publication_plan.md`, `docs/submission_execution_checklist.md` | Author-side account actions remain outside repository automation. |
| Strengthen research framing and claim structure | Supported | `paper/main.tex` claim structure, limitations, related work, and evidence boundaries | Subjective paper quality still benefits from venue reviewers. |
| Apply source-backed long-horizon review discipline | Supported | This audit, `evidence/execution_log.md`, `docs/publication_readiness.md`, and repeated test gates | The repository records durable evidence rather than relying on conversation state. |
| Preserve independent review boundaries | Supported | `docs/requirements_closure_audit.md`, `docs/publication_readiness.md`, and tests distinguish supported, bounded, and not-claimable items. | Internal review transcripts are not public artifact evidence. |
| Replace legacy model references and rerun with current providers | Supported | `results/experiments/live_model_summary.md`, `evidence/execution_log.md`, hygiene scans in `tests/test_public_presentation.py` | Future provider additions require fresh result summaries and claim checks. |
| Agent and harness practice must be reflected | Supported | `paper/main.tex`, `scripts/experiment_utils.py`, `scripts/external_pilot_runner_utils.py`, `evidence/execution_matrix.md` | More production traffic would require a separate deployment study. |
| Model-backed live experiments | Supported | DeepSeek and Kimi core live runs plus bounded external smoke in `results/experiments/raw/` and summaries | Large-scale live execution remains bounded by cost, credentials, and review. |
| External skill corpus beyond author artifacts | Bounded | `benchmark/external_artifact_corpus_sources.csv`, `results/tables/external_artifact_selection.csv`, `results/tables/external_corpus_summary.md` | The 240-slot design contains 232 concrete metadata-only references plus 8 pending replacement slots; eligibility review, replacement, and annotation remain pending. |
| Large-scale statistical significance | Not claimable | `results/experiments/external_statistical_analysis.md` records descriptive diagnostics and boundary language | Requires completed annotation, model execution, and preregistered inference. |
| External user or expert study | Bounded | `docs/human_review_execution_packet.md`, `docs/annotation_guide.md`, `results/tables/external_pilot_annotation_worklist.csv` | Recruitment, consent, compensation, annotation, and adjudication require external participants. |
| Remove public writing and tool-operation traces | Supported | `tests/test_public_presentation.py`, release PDF/source package scans, repository-level text scans | Re-run scans before any new release. |
| Distinguish this paper from the same-name 2026 work | Supported | `paper/main.tex` related-work and positioning sections | Keep the title/subtitle and abstract focused on personal-agent artifact lifecycle. |
| Pin GitHub and Zenodo citation | Bounded | `docs/submission_package_manifest.md`, `docs/publication_plan.md`, release `v1.1.0`, DOI `10.5281/zenodo.20844038` | GitHub release assets are aligned; Zenodo file-state verification after asset refresh requires an authenticated Zenodo session or token. |
| Prepare arXiv route | Bounded | `release/skillops-paper-source.zip`, `docs/submission_execution_checklist.md`, `docs/submission_package_manifest.md` | Account access, endorsement, category, license, and final submission action remain author-side. |
| Prepare OpenReview route | Bounded | `release/skillops-paper.pdf`, `docs/submission_execution_checklist.md`, `docs/publication_plan.md` | A concrete venue invitation, conflicts, declarations, and final submission action remain author-side. |
| Prepare submission metadata | Supported | `docs/submission_metadata_payload.md` | Venue-specific form fields may still differ. |
| Prepare account-side and external execution readiness | Supported | `docs/account_external_execution_readiness.md` | Zenodo, arXiv, OpenReview, provider keys, human reviewers, and sensitivity execution remain account-side or external-study actions. |
| Formal venue screening | Supported | `docs/publication_plan.md` | Deadlines and calls should be rechecked before submission. |

## Evidence Summary

- The release package is pinned at `v1.1.0` with Zenodo version DOI
  `10.5281/zenodo.20844038`.
- The arXiv source package contains `main.tex`, `main.bbl`, `references.bib`,
  and `README.md`.
- Repository tests at this audit boundary: 126 discovered, 126 passed.
- The public package reports completed internal benchmarks, local guard checks,
  two-provider internal live runs, bounded external smoke, and an auditable
  external-corpus scaffold.
- The public package does not report external human annotation, powered
  external statistical results, production deployment validation, or broad
  user-study outcomes.

## Recommended Order From Here

1. Author-side review of `release/skillops-paper.pdf` and
   `docs/submission_execution_checklist.md`.
2. Choose between FSE-oriented software-engineering submission and a
   human-centered route that first completes the review layer.
3. If submitting to arXiv, use `release/skillops-paper-source.zip` and the
   checklist category guidance.
4. If submitting through OpenReview, pick a concrete venue and use
   `release/skillops-paper.pdf` plus the DOI-backed artifact link.
5. For a stronger next public version, complete the external review layer,
   then run the preregistered pilot and statistical analysis.
