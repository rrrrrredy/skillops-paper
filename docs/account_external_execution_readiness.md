# Account And External Execution Readiness

Audit date: 2026-06-26

This document lists the remaining account-side and external-study actions for
the `v1.1.0` release. It is an execution checklist, not evidence that those
account actions or studies have been completed. No provider keys, account
tokens, participant identifiers, or payment information belong in the
repository.

## Account-Side Blockers

| Route | Required account-side action | Repository asset |
| --- | --- | --- |
| Zenodo | Verify the authenticated record for `10.5281/zenodo.20844038` and confirm whether the stored files match the refreshed GitHub release assets. Do not use the DOI as binary provenance until that account-side file state is checked. | `docs/submission_package_manifest.md` |
| arXiv | Confirm account status, category route, endorsement, license, and final upload action. Use the curated source zip rather than repository archive downloads. | `release/skillops-paper-source.zip` |
| OpenReview | Choose a concrete venue invitation, verify profile and emails, complete conflicts and policy declarations, then upload the PDF under that venue's rules. | `release/skillops-paper.pdf` |
| Formal venue | Recheck the live call for papers, formatting requirements, anonymity policy, artifact policy, and deadline before submission. | `docs/publication_plan.md` |

## Human Annotation Execution Checklist

| Step | Completion rule |
| --- | --- |
| Consent and data boundary | Confirm reviewer consent, compensation, data retention, and allowed artifact access before sharing packets. |
| Calibration | Run the 32-case calibration subset first and adjudicate disagreements before opening the 96-case pilot worklist. |
| Independent review | Use two independent reviewers per case; keep annotator fields empty until real labels are collected. |
| Adjudication | Resolve disagreements only after both reviewers finish; record rationale without personal identifiers. |
| Stop conditions | Stop if reviewers cannot access pinned source references, if license status blocks representation construction, or if expected-behavior labels are ambiguous after adjudication. |
| Reporting boundary | Do not report human-review outcomes until calibration, full pilot labels, adjudication, and reliability checks are complete. |

## Provider Live Pilot Order

1. Confirm no provider secrets are stored in repository files, shell history
   exports, generated results, or release artifacts.
2. Set provider keys only through a local secret mechanism or process
   environment outside the repository.
3. Run `python scripts/run_external_pilot_experiment.py --dry-run` and inspect
   `results/experiments/external_pilot_provider_readiness.md`.
4. Run a bounded smoke slice first, using `--run-live`, one provider, one
   model, `--sample-limit 4`, and `--max-live-rows 4`.
5. Sanitize and summarize outputs before increasing the bound.
6. Execute the 24-artifact pilot only after annotation/adjudication is complete
   and the smoke slice has no parsing, schema, or secret-hygiene failures.
7. Refuse unbounded provider execution; use the full external study only after
   replacement slots, eligibility review, annotation, and preregistered
   analysis are locked.

## Excluding-OpenAI Sensitivity Corpus Plan

The current external frame treats OpenAI Agents SDK examples as third-party
provider-adjacent contrast classes, not author-authored artifacts. To remove
any perception that provider-adjacent examples influence the conclusion, run a
sensitivity corpus that excludes `openai-agents-python` and `openai-agents-js`.

| Action | Completion rule |
| --- | --- |
| Exclude provider-adjacent rows | Remove source ids `openai-agents-python` and `openai-agents-js` from the sensitivity selection. |
| Preserve study-family balance | Replace their 28 workflow-template rows with non-OpenAI workflow-template rows where possible. |
| Expand corpus if needed | If the existing frame cannot supply replacements without exceeding owner/source caps, add new third-party workflow repositories before execution. |
| Regenerate downstream packets | Re-run selection, sampling, annotation, representation, dry-run, pilot, and summary generators for the sensitivity frame. |
| Keep claims separate | Report the sensitivity run as a robustness check only after it has its own eligibility review, annotation, live outputs, and statistical analysis. |

Suggested replacement pools include additional AutoGen examples, LangGraph
templates, LlamaIndex workflow examples, CrewAI examples, and other public
agent-workflow repositories with license-compatible metadata access.

## Completion Boundary

At the current release boundary, the repository is ready for account-side
checks and external-study execution planning. It does not contain completed
Zenodo account verification after the latest asset refresh, final arXiv or
OpenReview submission, completed human annotation, completed 24-artifact
outcome-bearing pilot execution, or excluding-OpenAI sensitivity results.
