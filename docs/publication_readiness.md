# Publication Readiness Report

Audit date: 2026-06-25

## Verification Status

| Check | Status | Evidence |
| --- | --- | --- |
| Repository tests | Passed | `python scripts/run_tests.py` reports 67/67 passed. |
| PDF build | Passed | `release/skillops-paper.pdf` rebuilt with Tectonic. |
| Source package | Passed | `release/skillops-paper-source.zip` refreshed from paper source, references, and README. |
| Public trace scan | Passed | No matches for removed model names, prepublication markers, or machine-writing traces in scanned public paths. |
| Whitespace check | Passed with Windows line-ending warnings | `git diff --check` exits 0; warnings are CRLF conversion notices. |
| External corpus boundary | Passed | Third-party artifact outputs are metadata-only and do not copy source prose or code. |

## Evidence Now Supported

- Core live model runs are available for `deepseek-v4-flash` and `kimi-k2.7-code` over the internal trigger, constraint, security, and memory protocols.
- Local security guard pilot is available over 24 risk cases and 24 benign controls.
- External corpus frame covers 11 third-party sources, including 10 GitHub-hosted sources analyzed by file-tree metadata.
- External study scaffold is executable at protocol level:
  - 240 metadata-only candidate artifact references.
  - 960 planned base cases.
  - 2880 pending condition rows.
  - 12 execution shards with 240 rows each.
  - Three representation payload conditions: original/freeform, SkillOps-normalized, and SkillOps-ablation.
  - Strict result schema and bounded-smoke summary boundary.
- Bounded external live smoke is available for 16 metadata-only condition rows:
  12 rows with `deepseek-v4-flash` and 4 rows with `kimi-k2.7-code`.
  The smoke produced 16/16 parse-success records and 5/16 expected-behavior
  matches.

## Claims Still Not Supported

- No external human annotation has been collected.
- No large-scale external provider execution has been run.
- No external statistical outcomes or significance claims are supported.
- No production deployment validation is reported.
- No broad user-study claim is supported.

## Publication Readiness

The repository is ready for internal author review and a single final commit. The paper is substantially stronger than the previous artifact because it now distinguishes completed evidence from external-validation scaffolding, pins the archived release DOI, removes legacy model references, and adds reproducible external-corpus preparation without overclaiming.

For a public paper update, the strongest defensible positioning is:

- SkillOps is a personal-agent artifact lifecycle framework.
- The completed evidence shows reproducible internal benchmarks, local guard execution, and two-provider live model checks on internal protocols.
- The external corpus layer is prepared and auditable, with a bounded provider
  smoke completed; it is not yet a powered external evaluation.

## Publish Blockers

| Blocker | Required action |
| --- | --- |
| External statistical validation | Complete human annotation/adjudication and run the planned external statistical analysis. |
| Zenodo metadata or new version DOI | Requires authenticated Zenodo account or token. |
| arXiv submission | Requires account access and category endorsement or an endorsed category choice. |
| OpenReview submission | Requires selecting an active venue or workshop invitation. |
| Conference submission | Requires target venue selection, formatting check, and deadlines. |

## Recommended Final Publish Sequence

1. Review the PDF and source package locally.
2. Commit all changes once.
3. Push once to GitHub.
4. Create a release tag only when the author approves the new public version number.
5. Archive the release artifact on Zenodo and update citation metadata.
