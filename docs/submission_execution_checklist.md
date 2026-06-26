# Submission Execution Checklist

Audit date: 2026-06-26

## Fixed Package Inputs

Use these files from the `v1.2.0` release assets:

| Target | File | SHA-256 |
| --- | --- | --- |
| arXiv source upload | `release/skillops-paper-source.zip` | `38833A57BF1F7001EEE72D3CF2ECD8E5E68B559D6DD17832F46F4F8D6FA46974` |
| OpenReview PDF upload | `release/skillops-paper.pdf` | `98957F4295EAFA777A234A77B9A75AFB4DE9294B50E60FE5B72565BD788F03B9` |

The arXiv source package contains `main.tex`, `main.bbl`,
`references.bib`, and `README.md`. Use the attached release asset, not GitHub's
automatic source archives.

## arXiv Route

Official references:

- TeX upload preparation: https://info.arxiv.org/help/submit_tex.html
- Metadata fields: https://info.arxiv.org/help/prep.html
- Submission verification guidance: https://info.arxiv.org/help/submit/index.html
- Endorsement: https://info.arxiv.org/help/endorsement.html

Account-side checklist:

1. Confirm account access and category endorsement for the chosen category.
2. Select a category consistent with the paper's actual contribution and venue
   plan.
3. Upload `release/skillops-paper-source.zip`.
4. Let arXiv process the source and inspect the generated PDF.
5. Fill metadata using the paper title, author, abstract, and DOI-backed
   artifact citation.
6. Check title, abstract, author order, comments, license, and category before
   the final submission action.
7. Do not claim completed external user study, production deployment
   validation, or statistical significance.

Suggested category decision:

| Category | Use when |
| --- | --- |
| `cs.SE` | Framing emphasizes software engineering, artifact lifecycle, testing, reproducibility, and operational governance. |
| `cs.HC` | Framing emphasizes personal agents, human review workflow, and user-facing evaluation. |
| `cs.AI` | Framing emphasizes agent reliability infrastructure and model behavior evaluation. |

The current manuscript is strongest for `cs.SE` or a venue submission that
values reproducible engineering artifacts. Use `cs.HC` only after the planned
human-review layer is collected.

## OpenReview Route

Official references:

- OpenReview profile signup: https://docs.openreview.net/getting-started/creating-an-openreview-profile/signing-up-for-openreview
- Independent researcher signup guidance: https://docs.openreview.net/getting-started/frequently-asked-questions/i-am-an-independent-researcher-how-do-i-sign-up
- Submission and revision guidance: https://docs.openreview.net/how-to-guides/submissions-comments-reviews-and-decisions
- Venue page pattern: https://openreview.net/group?id=[venueid]

Account-side checklist:

1. Confirm the author profile is active and includes current emails,
   affiliation or independent researcher information, and conflict-relevant
   history.
2. Select a live venue or workshop invitation; OpenReview is venue-specific and
   a generic upload is not a reviewed venue submission.
3. Upload `release/skillops-paper.pdf`.
4. Enter title, abstract, author list, keywords, subject areas, conflicts, and
   artifact links exactly as required by the venue form.
5. Add the immutable artifact DOI:
   `https://doi.org/10.5281/zenodo.20900771`.
6. Attach supplementary files only if the venue form requests them.
7. Review venue policy fields, author declarations, conflicts, and anonymity
   settings before final submission.

## Non-Automatable Actions

These actions require the author's authenticated session or external
participants:

- arXiv account access, endorsement, category selection, license selection, and
  final submission action;
- OpenReview account/profile verification, venue invitation selection, conflict
  declarations, policy declarations, and final submission action;
- Zenodo account-side metadata edits;
- external human-review recruitment, consent, compensation, annotation, and
  adjudication;
- outcome-bearing live pilot execution with locally injected provider
  credentials.

## Final Local Checks Before Account Upload

```powershell
python scripts/run_tests.py
git status --short --branch
rg -n "sk-[A-Za-z0-9]{24,}|Bearer [A-Za-z0-9._-]{20,}|AKIA[0-9A-Z]{16}" README.md paper evidence docs benchmark experiments results scripts tests release\skillops-paper-source release\main.bbl -S
```

The expected test count at this package boundary is 121.
