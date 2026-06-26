# Account And External Execution Readiness

Audit date: 2026-06-26

This document lists the remaining account-side and external-study actions for
the current submission package. GitHub release `v1.3.0` and Zenodo DOI
`10.5281/zenodo.20907648` are published and file-verified. This is an execution
checklist, not evidence that remaining account actions or studies have been
completed. No provider keys, account
tokens, participant identifiers, or payment information belong in the
repository.

## Account-Side Blockers

| Route | Required account-side action | Repository asset |
| --- | --- | --- |
| Zenodo | Authenticated record check completed: prior DOI `10.5281/zenodo.20844038` archives an older GitHub snapshot and is not binary provenance for the current package. DOI `10.5281/zenodo.20907648` is published and file-verified for `v1.3.0`; DOI `10.5281/zenodo.20900771` remains the previous package record. | `docs/zenodo_file_state_audit.md` |
| arXiv | Confirm account status, category route, endorsement, license, and final upload action. Use the curated source zip rather than repository archive downloads. | `release/skillops-paper-source.zip` |
| OpenReview | Choose a concrete venue invitation, verify profile and emails, complete conflicts and policy declarations, then upload the PDF under that venue's rules. | `release/skillops-paper.pdf` |
| Formal venue | Recheck the live call for papers, formatting requirements, anonymity policy, artifact policy, and deadline before submission. | `docs/publication_plan.md` |

## Machine-Checkable And Judge-Sensitivity Execution Checklist

| Step | Completion rule |
| --- | --- |
| Primary external-smoke metrics | Run `python scripts/run_machine_checkable_external_analysis.py` after every bounded external provider slice. |
| Case-label sensitivity plan | Run `python scripts/run_llm_judge_sensitivity.py --dry-run` to materialize the 32-case calibration subset without credentials. |
| Bounded judge execution | If credentials are locally available, run `python scripts/run_llm_judge_sensitivity.py --run-live --provider deepseek --model deepseek-v4-flash --sample-limit 8 --max-live-rows 8` first, then repeat with Kimi only after parsing is clean. |
| Evidence separation | Treat `external_machine_checkable_metrics.csv` as primary external-smoke evidence and `llm_judge_sensitivity_summary.csv` as secondary label-sensitivity evidence. |
| Stop conditions | Stop if provider output fails schema parsing, if labels are unstable across judge providers, or if any generated file contains secrets or raw model prose. |
| Reporting boundary | Do not report broad external validation, statistical significance, or model ranking from bounded smoke or judge-sensitivity rows. |

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
6. Execute the 24-artifact pilot only after the smoke slice and judge
   sensitivity slice have no parsing, schema, label-instability, or
   secret-hygiene failures.
7. Refuse unbounded provider execution; use the full external study only after
   replacement slots, eligibility review, machine-checkable scoring rules, and
   preregistered analysis are locked.

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
| Regenerate downstream packets | Re-run selection, sampling, case construction, representation, dry-run, pilot, machine-checkable metrics, and judge-sensitivity generators for the sensitivity frame. |
| Keep claims separate | Report the sensitivity run as a robustness check only after it has its own eligibility review, live outputs, machine-checkable metrics, and statistical analysis. |

Suggested replacement pools include additional AutoGen examples, LangGraph
templates, LlamaIndex workflow examples, CrewAI examples, and other public
agent-workflow repositories with license-compatible metadata access.

## Completion Boundary

At the current release boundary, the repository is ready for account-side
checks and external-study execution planning. It does not contain final arXiv
or OpenReview submission, completed 24-artifact outcome-bearing pilot
execution, provider-backed LLM-as-judge sensitivity results, or
excluding-OpenAI sensitivity results.
