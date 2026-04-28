# SkillOps Paper

This repository contains the working paper draft, research logs, benchmark
design notes, bibliography, figures directory, and reproducibility scaffolding
for:

**SkillOps: A Practical Framework for Designing, Testing, and Operating Modular Skills in Personal AI Agents**

Author: **Song Luo**  
Affiliation: **Independent Researcher**

## Status

This repository is an active first-preprint workspace.

The current draft is internally consistent enough for review as a preprint
draft, but it is still incomplete in two important ways:

- The paper now includes framework tables, figure placeholders, and a cleaned
  bibliography.
- Generated benchmark results are not yet included.

## Linked Artifact Base

The paper is grounded in the following open-source artifacts maintained by the
author:

- [skill-design-guide](https://github.com/rrrrrredy/skill-design-guide)
- [skill-security-guard](https://github.com/rrrrrredy/skill-security-guard)
- [persistent-memory](https://github.com/rrrrrredy/persistent-memory)
- [agent-self-audit](https://github.com/rrrrrredy/agent-self-audit)
- [lobster-guard](https://github.com/rrrrrredy/lobster-guard)

These repositories are treated as exploratory engineering evidence and case
material. They are not presented as proof of broad empirical validation.

## Current Stage

The project is currently at the following stage:

- Paper framing, research questions, and methodology draft are in place.
- Related-work coverage is now substantially expanded and tied to the paper's
  claims.
- Conceptual framework tables are present in the LaTeX draft.
- Benchmark design is specified, but benchmark cases, scripts, and generated
  result tables are still pending.
- Figure environments exist as compilable placeholders pending final artwork.

## Research Questions

**RQ1:** What structural components should a skill include as an agent
capability unit?

**RQ2:** How do trigger descriptions, context injection, execution constraints,
and forgetting affect agent stability?

**RQ3:** Can automated linting, security scanning, and self-auditing reduce
operational risk?

## Repository Structure

```text
paper/          LaTeX source files and bibliography
benchmark/      Planned benchmark cases and evaluation inputs
scripts/        Planned reproducible analysis scripts
results/        Planned generated tables and intermediate outputs
figures/        Planned diagrams and generated figures
research-log/   Design notes, literature notes, and audit logs
artifacts/      Artifact inventory and links to source repositories
```

## Benchmark Files

The first benchmark-design layer now lives in:

- `artifacts/artifact_inventory.md`
- `benchmark/README.md`
- `benchmark/skill_samples.csv`
- `benchmark/trigger_cases.csv`
- `benchmark/risk_cases.csv`

These files are manually constructed from public repository inspection. They
document the benchmark inputs, but they do not contain generated results,
evaluation tables, or figures.

## Target Venue Strategy

The current publication strategy is staged rather than single-shot:

1. Maintain the GitHub repository as the canonical artifact base.
2. Prepare an OSF or TechRxiv-style preprint release once the benchmark
   implementation is less skeletal.
3. Seek workshop feedback on the framework and evaluation design.
4. Submit a later revision to arXiv after the paper and artifact package are
   more mature.

If the paper keeps its current operational framing, `cs.SE` remains a plausible
primary category with `cs.AI` as a cross-list. If later revisions foreground
agent design more strongly than engineering lifecycle, that balance may shift.

## Reproducibility

The repository is intended to make the paper inspectable and incrementally
reproducible.

Current reproducibility status:

- The paper source and bibliography are versioned in this repository.
- The benchmark design is documented in the paper and research logs.
- Directory structure for benchmark cases, scripts, results, and figures is in
  place.
- Generated benchmark artifacts are not yet committed because the benchmark has
  not yet been fully implemented or executed.

Future revisions should add benchmark inputs, scripts, generated tables,
figure-generation steps, and any annotation guidance needed for manual review.

## Limitations

This project remains intentionally modest:

- It is based on a single independent researcher's open-source practice.
- It does not yet report generated benchmark results.
- It should not be read as evidence of broad empirical validation.
- The benchmark is expected to be small-scale and partially manual even after it
  is implemented.

## Current Next Steps

- Implement the benchmark cases described in the paper.
- Add scripts that generate the planned evaluation tables.
- Replace boxed figure placeholders with final diagrams.
- Run a full LaTeX compilation pass once a compiler is available.
- Prepare an external review pass focused on claim strength and evaluation
  scope.
