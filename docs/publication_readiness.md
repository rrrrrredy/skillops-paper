# Publication Readiness Report

Audit date: 2026-06-26

## Verification Status

| Check | Status | Evidence |
| --- | --- | --- |
| Repository tests | Passed | `python scripts/run_tests.py` reports 135 discovered, 135 passed. |
| Submission metadata payload | Passed | `docs/submission_metadata_payload.md` records copy-ready arXiv, OpenReview, and venue metadata tied to the current paper and release package. |
| Requirements closure audit | Passed | `docs/requirements_closure_audit.md` maps the full author request to supported evidence, bounded account actions, and not-claimable items. |
| PDF build | Passed | `release/skillops-paper.pdf` rebuilt with Tectonic. |
| Source package | Passed | `release/skillops-paper-source.zip` refreshed from paper source, generated `main.bbl`, references, and README. |
| Standalone source compile | Passed | The source zip was extracted into a repository-external temporary directory and compiled with Tectonic outside the repository context. |
| Submission asset boundary | Passed | The attached release PDF and source zip are the submission package; automatic repository source archives are not used for arXiv submission. |
| Submission execution checklist | Passed | `docs/submission_execution_checklist.md` records account-side arXiv and OpenReview actions, official references, and non-automatable boundaries. |
| Account and external execution readiness | Passed | `docs/account_external_execution_readiness.md` records account-side blockers, human annotation sequencing, bounded provider pilot order, and excluding-OpenAI sensitivity planning. |
| Versioned release | Passed | GitHub release `v1.2.0` exists with the current PDF/source assets and Zenodo record `20900771` is published. |
| Zenodo file-state audit | Published and verified | Zenodo record `20900771` has DOI `10.5281/zenodo.20900771` and a GitHub-integration archive whose embedded PDF/source assets match the release hashes; prior record `20844038` archives an older GitHub snapshot and is not binary provenance for the current PDF. |
| Public trace scan | Passed | No matches for removed model names, prepublication markers, or machine-writing traces in scanned public paths. |
| Whitespace check | Passed with Windows line-ending warnings | `git diff --check` exits 0; warnings are CRLF conversion notices. |
| External corpus boundary | Passed with replacement slots disclosed | Third-party artifact outputs are metadata-only and do not copy source prose or code; the 240-slot design currently has 232 concrete references and 8 pending replacement slots. |

## Evidence Now Supported

- Core live model runs are available for `deepseek-v4-flash` and `kimi-k2.7-code` over the internal trigger, constraint, security, and memory protocols.
- Local security guard pilot is available over 24 risk cases and 24 benign controls.
- External corpus frame covers 11 third-party sources, including 10 GitHub-hosted sources analyzed by file-tree metadata.
- External study scaffold is executable at protocol level:
  - 240 target artifact slots.
  - 232 concrete metadata-only third-party references.
  - 8 pending replacement slots requiring eligibility review and replacement
    before outcome-bearing execution.
  - 960 planned base cases.
  - 2880 pending condition rows.
  - 12 execution shards with 240 rows each.
  - Three representation payload conditions: original/freeform, SkillOps-normalized, and SkillOps-ablation.
  - Strict result schema and bounded-smoke summary boundary.
- A seeded 24-artifact external pilot execution plan is available:
  - 96 base cases.
  - 288 condition rows per provider/model.
  - 576 provider-condition rows across DeepSeek and Kimi.
  - Balanced family allocation across agent skills, workflow templates, MCP/tool
    recipes, and prompt/function recipes.
- A resumable bounded pilot runner and no-secret provider readiness plan are
  available for the 576 provider-condition rows.
- A no-secret bounded live-selection manifest records a 2-row DeepSeek pilot
  selection that was not executed because `DEEPSEEK_API_KEY` was unavailable in
  the shell environment.
- A pilot annotation layer is prepared:
  - 96 pending review cases.
  - 32 balanced calibration cases.
  - Two-annotator and adjudication fields, with no collected annotations.
  - Two-reviewer assignment manifest, adjudication log template, interface
    spec, execution plan, and reliability computation script.
- A human-review execution packet now specifies consent, data handling,
  calibration, quality controls, and stop conditions for the external review
  layer.
- Bounded external live smoke is available for 16 metadata-only condition rows:
  12 rows with `deepseek-v4-flash` and 4 rows with `kimi-k2.7-code`.
  The smoke produced 16/16 parse-success records and 5/16 expected-behavior
  matches.

## Claims Still Not Supported

- No external human annotation has been collected.
- The 24-artifact external pilot has not yet been annotated or executed as a
  powered study.
- Provider-backed pilot execution remains bounded to the completed smoke layer;
  the 24-artifact pilot has not been run as an outcome-bearing study.
- No model API key is stored in repository files or release artifacts.
- No large-scale external provider execution has been run.
- No external statistical outcomes or significance claims are supported.
- No production deployment validation is reported.
- No broad user-study claim is supported.

## Publication Readiness

The repository is prepared for author-side submission checks at the `v1.2.0`
artifact boundary. This version adds clearer evidence boundaries, DOI-pinned
release materials, external-corpus preparation, pilot-readiness, and
annotation-calibration artifacts without overclaiming.

For a public paper update, the strongest defensible positioning is:

- SkillOps is a personal-agent artifact lifecycle framework.
- The completed evidence shows reproducible internal benchmarks, local guard execution, and two-provider live model checks on internal protocols.
- The external corpus layer is prepared and auditable, with a bounded provider
  smoke completed; it is not yet a powered external evaluation.

## Publish Blockers

| Blocker | Required action |
| --- | --- |
| External statistical validation | Complete human annotation/adjudication and run the planned external statistical analysis. |
| Excluding-OpenAI sensitivity corpus | Replace OpenAI Agents SDK rows with non-OpenAI workflow-template rows, then regenerate and run a separate sensitivity frame. |
| arXiv submission | Requires account access and category endorsement or an endorsed category choice. |
| OpenReview submission | Requires selecting an active venue or workshop invitation. |
| Conference submission | Requires target venue selection, formatting check, and deadlines. |

## Recommended Next Publish Sequence

1. Review the `v1.2.0` PDF and source package locally.
2. Submit the source package through the chosen venue workflow.
3. For arXiv, use an endorsed category or obtain endorsement before upload.
4. For OpenReview, select a concrete venue or workshop invitation before upload.
5. For any later public artifact version, create a new release only after all
   paper/package edits are final, then verify the new Zenodo file state before
   updating the version DOI in submission materials.
