# Publication Plan

## Artifact Citation

Use the immutable release citation for the paper package:

- GitHub release: https://github.com/rrrrrredy/skillops-paper/releases/tag/v1.0.0
- Zenodo version DOI: https://doi.org/10.5281/zenodo.20838908
- Zenodo concept DOI: https://doi.org/10.5281/zenodo.20061198

The version DOI is the right citation for a submitted paper because it fixes
the exact artifact snapshot. The concept DOI is useful as a moving reference to
the release family.

Zenodo account linking and metadata edits require an authenticated Zenodo
session or API token. The GitHub-Zenodo release record already exists; editing
or merging older records cannot be done from the repository alone.

## arXiv Route

arXiv submission should use the LaTeX source package, not a PDF compiled from
LaTeX. The account needs endorsement for the target category when arXiv requires
it. Likely categories to evaluate are `cs.SE`, `cs.AI`, and `cs.HC`:

| Category | Fit | Risk |
| --- | --- | --- |
| `cs.SE` | Strong fit for lifecycle, tests, harnesses, artifact governance. | Needs software-engineering framing and reproducibility emphasis. |
| `cs.AI` | Fit for agent skills and model-backed evaluation. | Needs stronger empirical evidence to avoid looking like tooling notes. |
| `cs.HC` | Fit for personal agents and human review workflow. | Needs human study evidence for best fit. |

Without endorsement, the practical path is to request endorsement from a
qualified submitter in the chosen category or submit after acceptance to a venue
whose publication record helps establish eligibility. Endorsement cannot be
created by repository automation.

## OpenReview Route

OpenReview submissions are venue-specific. The standard path is:

1. Create and verify an OpenReview profile with all author emails.
2. Choose the target venue group and check its author instructions.
3. Register the abstract if required.
4. Upload the PDF and any supplementary files before the venue deadline.
5. Complete conflict, author, artifact, ethics, and policy declarations.
6. Review the submission page and confirm that all authors can access it.

There is no generic guarantee that posting to OpenReview alone gives a reviewed
paper. The right route is to submit through a conference, workshop, or journal
venue hosted on OpenReview.

## Venue Fit

| Venue | Deadline status on 2026-06-25 | Fit | Recommendation |
| --- | --- | --- | --- |
| AAAI 2027 | Abstract July 21, 2026; full paper July 28, 2026 | General AI and agent systems | Possible only if the paper is sharpened around agent reliability and live evidence. |
| IUI 2027 | Abstract August 13, 2026; full paper August 20, 2026 | Intelligent interfaces and human-centered agent tooling | Strong if paired with a compact external user study or expert review. |
| CHI 2027 | Full paper due September 10, 2026 | Personal agents, HCI, workflow design | Strongest after human study and qualitative evidence. |
| FSE 2027 | Full paper due October 2, 2026 | Software-engineering lifecycle and artifact governance | Best long-paper fit if the contribution is framed as software engineering for agent skills. |
| AAMAS 2027 | Submission date listed as October 2026 TBC | Autonomous agents and multi-agent systems | Good if external corpus and ablations are expanded. |
| ICSE 2027 | Research-track registration has passed | Software engineering | Not available for this main-track cycle. |
| ICLR 2027 | 2027 dates not yet confirmed in the checked sources | Agent learning and evaluation | Monitor for official dates; likely viable only with stronger quantitative evidence. |

Best ordering:

1. FSE 2027 as the main target for the current contribution shape.
2. IUI 2027 or CHI 2027 if the human-review protocol is executed.
3. AAAI 2027 if the paper is compressed and the agent-reliability angle is made more central.
4. AAMAS 2027 if the paper adds broader agent-environment evidence.

## Submission Support Boundary

Repository automation can prepare the PDF, source package, artifact citation,
supplementary files, checklist responses, and venue-specific formatting. Account
login, endorsement, author policy declarations, conflict declarations, payment,
and final submission confirmation require the author's authenticated session
and approval.
