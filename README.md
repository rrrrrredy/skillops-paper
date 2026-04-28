# SkillOps Paper

This repository contains the paper draft, research logs, benchmark files, scripts, figures, and reproducible artifacts for the paper:

**SkillOps: A Practical Framework for Designing, Testing, and Operating Modular Skills in Personal AI Agents**

Author: **Song Luo**  
Affiliation: **Independent Researcher**

## Status

Work in progress.

Current stage:

- Paper specification created.
- Related work notes drafted.
- Initial references collected.
- Artifact inventory, benchmark files, scripts, figures, and paper draft are still under development.

## Research Questions

**RQ1:** What structural components should a skill include as an agent capability unit?

**RQ2:** How do trigger descriptions, context injection, execution constraints, and forgetting affect agent stability?

**RQ3:** Can automated linting, security scanning, and self-auditing reduce operational risk?

## Artifact Base

This paper is based on the following open-source artifacts developed by the author:

- [skill-design-guide](https://github.com/rrrrrredy/skill-design-guide)
- [skill-security-guard](https://github.com/rrrrrredy/skill-security-guard)
- [persistent-memory](https://github.com/rrrrrredy/persistent-memory)
- [agent-self-audit](https://github.com/rrrrrredy/agent-self-audit)
- [lobster-guard](https://github.com/rrrrrredy/lobster-guard)

These artifacts are treated as exploratory engineering evidence and reproducible case material, not as proof of large-scale empirical validation.

## Planned Evaluation

The initial evaluation will be small-scale, artifact-based, and reproducible.

Planned components:

1. Skill structure coverage analysis.
2. Trigger robustness benchmark.
3. Context injection and memory behavior analysis.
4. Security scanning and self-audit case study.
5. Failure case analysis.

## Repository Structure

```text
paper/          LaTeX source files and references
benchmark/      Manually constructed benchmark cases
scripts/        Reproducible analysis scripts
results/        Generated tables and intermediate outputs
figures/        Generated figures and diagrams
research-log/   Research notes, design decisions, and audit logs
artifacts/      Artifact inventory and links to source repositories
```

## Target Venue Strategy

The intended path is:

1. GitHub artifact release.
2. Zenodo artifact DOI.
3. TechRxiv or OSF preprint.
4. Workshop submission for feedback.
5. arXiv submission after endorsement.

Tentative arXiv category strategy:

- Primary: `cs.SE`
- Cross-list: `cs.AI`, `cs.CR`

## Reproducibility

All benchmark files, scripts, tables, and figures will be added to this repository as the project develops.

Manually constructed benchmark cases will be clearly labeled.

The repository is intended to make the paper's artifact base inspectable and reproducible, while keeping the limitations of a small-scale independent research project explicit.

## Limitations

This project is based on a single independent researcher's open-source practice.

The initial evaluation is expected to be small-scale and exploratory.

The paper will not claim broad empirical validation without additional external evidence.
