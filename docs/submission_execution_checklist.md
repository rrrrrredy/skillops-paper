# Submission Execution Checklist

Audit date: 2026-06-26

## Local Package Inputs

Use these local files as the next submission package. They must be published as
a new GitHub release and verified in Zenodo before the DOI is cited as binary
provenance:

Published reference DOI for the previous public package:
`10.5281/zenodo.20900771`. Replace it with the next verified DOI before final
submission if using the refreshed local package below.

Target GitHub release: `https://github.com/rrrrrredy/skillops-paper/releases/tag/v1.3.0`.

| Target | File | SHA-256 |
| --- | --- | --- |
| arXiv source upload | `release/skillops-paper-source.zip` | `0A41FA212495EFBDE0C7D9166F2DEBE4E5517C8CD4185B00634F551382A917CE` |
| OpenReview PDF upload | `release/skillops-paper.pdf` | `687B3952611A176BAB23A2A2C223D29B5BBF1C63903080B08EA2051A57542F3D` |

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
8. Before final public upload, replace the `v1.2.0` artifact citation with the
   next verified GitHub release and Zenodo version DOI for these local hashes.

Endorsement link/code generation:

1. Log in to arXiv and start a new submission.
2. Select the target category, likely `cs.SE` for the current manuscript.
3. If arXiv requires endorsement, check the endorsement request email it sends
   to the account address. That email contains the request link for eligible
   endorsers.
4. Copy the exact request link or six-character endorsement code from arXiv.
5. Send it to one qualified endorser at a time, preferably someone whose recent
   arXiv papers are close to the paper's category.
6. After endorsement is granted, return to the submission and continue the
   upload, metadata, preview, and final submit steps.

Version route:

- If this paper has no arXiv identifier yet, use **Start New Submission** and
  upload `release/skillops-paper-source.zip` after the next artifact DOI is
  verified.
- If the paper already has an arXiv identifier, use **Replace** on the existing
  article. Do not create a second arXiv record for corrections or updates.
- Replacement comments should state the nature of the changes, for example:
  `Updated artifact DOI, clarified machine-checkable external evidence, and
  added LLM-as-judge label-sensitivity protocol.`

Suggested category decision:

| Category | Use when |
| --- | --- |
| `cs.SE` | Framing emphasizes software engineering, artifact lifecycle, testing, reproducibility, and operational governance. |
| `cs.HC` | Framing emphasizes personal agents, user-facing workflow, and human-centered evaluation. |
| `cs.AI` | Framing emphasizes agent reliability infrastructure and model behavior evaluation. |

The current manuscript is strongest for `cs.SE` or a venue submission that
values reproducible engineering artifacts. Use `cs.HC` only after the planned
user-facing evaluation layer is collected.

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
- future Zenodo account-side metadata edits;
- outcome-bearing live pilot execution with locally injected provider
  credentials.
- provider-backed LLM-as-judge sensitivity execution with locally injected
  provider credentials.

## Final Local Checks Before Account Upload

```powershell
python scripts/run_tests.py
git status --short --branch
rg -n "sk-[A-Za-z0-9]{24,}|Bearer [A-Za-z0-9._-]{20,}|AKIA[0-9A-Z]{16}" README.md paper evidence docs benchmark experiments results scripts tests release\skillops-paper-source release\main.bbl -S
```

The expected test count at this package boundary is 135.
