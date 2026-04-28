# Paper Consistency Patch

Date: 2026-04-28

## Files inspected

- `README.md`
- `paper/main.tex`
- `paper/references.bib`
- `research-log/2026-04-27-paper-spec.md`
- `research-log/2026-04-27-related-work-notes.md`

## Citation issues fixed

- Added missing cited keys:
  - `amershi2019guidelines`
  - `brown2020language`
  - `gamma1994design`
  - `ganguli2022redteaming`
  - `ouyang2022training`
  - `parnas1972criteria`
  - `szyperski2002component`
- Fixed the Voyager citation-key mismatch by updating the manuscript to use
  `wang2024voyager` consistently.
- Reformatted `paper/references.bib` into normalized multi-line BibTeX entries.
- Cleaned several previously malformed author-name encodings in existing BibTeX
  entries.

## Tables added to the paper

- Skill structural components
- RQ to framework component to evaluation method mapping
- Failure modes taxonomy
- Informal skills vs SkillOps-managed skills comparison
- Existing artifact summary table retained

## TODOs resolved or retained

Resolved in `paper/main.tex`:

- Replaced the author-contact TODO with the GitHub contact URL.
- Replaced result-placeholder TODO language with explicit implementation-status
  language.
- Replaced figure TODO text with compilable boxed figure placeholders for:
  - SkillOps lifecycle
  - Skill anatomy
- Removed citation-verification TODO comments from the manuscript body and
  replaced them with a cleaner related-work treatment.
- Expanded Related Work using the stronger literature categories from the
  2026-04-27 notes while keeping the section concise.

Retained as intentional status, not TODO placeholders:

- No generated benchmark result tables are included yet.
- No final figure artwork is included yet.
- Benchmark cases and scripts are still pending implementation in the repository.

## Remaining blockers

- A LaTeX compiler was not available in the current environment during this
  patch, so full compilation could not be verified here.
- The repository still lacks executed benchmark artifacts, so the paper remains
  a framework-and-evaluation-design preprint rather than a results paper.
- Final diagrams, benchmark cases, scripts, and generated outputs are still
  needed before a stronger public preprint release.
