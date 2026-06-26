# Publication Plan

## Artifact Citation

Use an immutable release citation for the submitted paper package:

- GitHub release: https://github.com/rrrrrredy/skillops-paper/releases/tag/v1.2.0
- Zenodo version DOI: https://doi.org/10.5281/zenodo.20900771
- Zenodo concept DOI: https://doi.org/10.5281/zenodo.20061198

The version DOI is the right citation for a submitted paper because it fixes the
exact artifact snapshot. The concept DOI is useful as a moving reference to the
release family.

Zenodo account linking and metadata edits require an authenticated Zenodo
session or API token. The new version record is reserved as `20900771` with
version DOI `10.5281/zenodo.20900771`. The previous `v1.1.0` record
`20844038` is retained as a historical archive and should not be used as
current binary provenance.

For subsequent public versions, do not overwrite the existing `v1.1.0` release.
Create a new GitHub release only after the final commit and let Zenodo mint the
next version DOI through the GitHub integration. Zenodo's GitHub guide states
that, once a repository is connected, new GitHub releases are automatically
ingested and archived, while GitHub's own documentation states that Zenodo
issues a new DOI each time a new GitHub release is created:

- Zenodo GitHub guide: https://help.zenodo.org/docs/github/
- Zenodo enable-repository guide: https://help.zenodo.org/docs/github/enable-repository/
- GitHub DOI guide: https://docs.github.com/en/repositories/archiving-a-github-repository/referencing-and-citing-content

## arXiv Route

arXiv submission should use the LaTeX source package, not a PDF compiled from
LaTeX. The account needs endorsement for the target category when arXiv requires
it. arXiv's endorsement documentation says first-time submitters, or submitters
entering a new category, may need endorsement; institutional email or personal
endorsement from an established arXiv author can satisfy the route depending on
account history:

- arXiv endorsement help: https://info.arxiv.org/help/endorsement.html

Likely categories to evaluate are `cs.SE`, `cs.AI`, and `cs.HC`:

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

OpenReview's own profile documentation recommends institutional email when
available; public-domain email addresses can require moderation. OpenReview also
has specific instructions for independent researchers: personal email is allowed
but moderated, and profile history should be completed carefully.

- OpenReview signup guide: https://docs.openreview.net/getting-started/creating-an-openreview-profile/signing-up-for-openreview
- OpenReview independent researcher guidance: https://docs.openreview.net/getting-started/frequently-asked-questions/i-am-an-independent-researcher-how-do-i-sign-up

There is no generic guarantee that posting to OpenReview alone gives a reviewed
paper. The right route is to submit through a conference, workshop, or journal
venue hosted on OpenReview.

## Venue Fit

| Venue | Deadline status on 2026-06-25 | Fit | Recommendation |
| --- | --- | --- | --- |
| FSE 2027 | Research full paper due October 2, 2026. Source: https://conf.researchr.org/home/fse-2027 | Software-engineering lifecycle and artifact governance | Best long-paper fit for the current contribution shape. Emphasize artifact lifecycle, reproducibility, tests, and evidence boundaries. |
| CHI 2027 | Full paper due September 10, 2026; no abstract deadline. Source: https://chi2027.acm.org/authors/papers/ | Personal agents, HCI, workflow design | Strong if the pilot annotation or expert/user study is completed before submission. |
| IUI 2027 | Abstract August 13, 2026; full paper August 20, 2026. Source: https://iui.acm.org/2027/ | Intelligent interfaces and human-centered agent tooling | Good if a compact expert-review or annotation-calibration result is completed soon. |
| AAAI 2027 | Abstract July 21, 2026; full paper July 28, 2026. Source: https://aaai.org/conference/aaai/aaai-27/ | General AI and agent systems | Time is tight; submit only if the argument is compressed around agent reliability and the current evidence is not overextended. |
| ICSE 2027 Research Track | Mandatory abstract June 23, 2026; paper June 30, 2026. Source: https://conf.researchr.org/track/icse-2027/icse-2027-research-track | Software engineering | Main-track abstract registration has passed as of June 25, 2026. Consider ICSE colocated tracks with October 2026 deadlines if the scope matches. |
| NeurIPS 2026 E\&D / workshops | E\&D full paper deadline passed on May 6, 2026; workshop contribution timing depends on accepted workshop calls. Sources: https://neurips.cc/Conferences/2026/CallForEvaluationsDatasets and https://neurips.cc/Conferences/2026/CallForWorkshops | Evaluation artifacts and benchmarks | Main E\&D deadline has passed. Consider only a matching accepted workshop with a live submission call. |
| ICLR 2027 | Official future-meetings page lists West Coast North America, but no checked submission deadline yet. Source: https://iclr.cc/Conferences/FutureMeetings | Agent learning and evaluation | Monitor official ICLR/OpenReview pages; likely needs stronger quantitative results than the current paper. |
| AAMAS 2027 | OpenReview venue exists, but checked public page did not expose deadlines. Source: https://openreview.net/group?id=ifaamas.org/AAMAS/2027/Conference | Autonomous agents and multi-agent systems | Monitor deadline release; fit improves with broader agent-environment evidence and ablations. |

Best ordering for the current manuscript:

1. FSE 2027 as the main target for the current contribution shape.
2. CHI 2027 if the human-review or expert-review layer is completed.
3. IUI 2027 if a compact pilot annotation result can be completed before August 2026.
4. AAAI 2027 only if no additional human-study work is possible and the paper is reframed as agent reliability infrastructure.
5. AAMAS 2027 or ICLR 2027 only after stronger external execution and ablation evidence.

## Submission Support Boundary

Repository automation can prepare the PDF, source package, artifact citation,
supplementary files, checklist responses, and venue-specific formatting. Account
login, endorsement, author policy declarations, conflict declarations, payment,
and final submission confirmation require the author's authenticated session
and approval.
