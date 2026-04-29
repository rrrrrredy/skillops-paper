# SkillOps Artifact Inventory

Date: 2026-04-28

This inventory records the five public repositories inspected as exploratory
artifact evidence for the paper *SkillOps: A Practical Framework for Designing,
Testing, and Operating Modular Skills in Personal AI Agents*.

All observations below are based on manual inspection of public repository
contents on 2026-04-28. These artifacts support the paper's framework claims,
but they do not by themselves establish broad empirical validation.

## Summary

| Artifact | Main SkillOps role | RQ emphasis | Evidence type | Main limitation |
| --- | --- | --- | --- | --- |
| `skill-design-guide` | Skill structure, linting, and testing workflow | RQ1 primary; RQ2 secondary; RQ3 secondary | README, SKILL contract, linter script | Mostly design guidance and static checks |
| `skill-security-guard` | Pre-deployment security review | RQ3 primary; RQ2 secondary | README, scan contract, detection rules, scan entry script | Static heuristics, not runtime enforcement |
| `persistent-memory` | Long-term memory and forgetting controls | RQ2 primary; RQ1 secondary; RQ3 secondary | README, SKILL contract, memory manager script | OpenClaw-specific paths and cron model |
| `agent-self-audit` | Runtime health auditing and maintenance | RQ3 primary; RQ2 secondary | README, SKILL contract, audit criteria, quick-check script | Thresholds are handcrafted and environment-specific |
| `lobster-guard` | Identity isolation and privacy guardrails | RQ3 primary; RQ2 secondary | README, SKILL contract, identity reference | Mostly configuration guidance, little executable code |

## skill-design-guide

- Repository URL: <https://github.com/rrrrrredy/skill-design-guide>
- Purpose: Provides a structured workflow for designing, testing, linting, and
  quality-checking modular skills for OpenClaw-style agents.
- Files inspected: `README.md`, `SKILL.md`, `scripts/skill_lint.py`
- SkillOps components supported:
  - Skill metadata and frontmatter conventions
  - Trigger-contract design and boundary setting
  - Instruction structure and token-budget discipline
  - Failure handling via Gotchas and Hard Stop rules
  - Static linting and pre-publication review
- Mapping to research questions:
  - RQ1: Primary evidence for what a skill should contain as a capability unit
  - RQ2: Secondary evidence for trigger wording, context boundaries, and
    forgetting pressure
  - RQ3: Secondary evidence through linting and structural safety checks
- Evidence available:
  - `README.md` describes a four-stage lifecycle and a 12-point quality
    checklist.
  - `SKILL.md` encodes concrete trigger phrases, explicit non-applicable cases,
    Gotchas, and a Hard Stop policy.
  - `scripts/skill_lint.py` implements structural checks such as required
    files, frontmatter presence, line-count limits, version consistency,
    sensitive-pattern scanning, and basic syntax checks.
- Limitations:
  - The repository is focused on one agent ecosystem and one author's practice.
  - Most evidence is design guidance and static validation rather than measured
    behavioral outcomes.
  - The repo does not contain a benchmark corpus or executed trigger metrics.

## skill-security-guard

- Repository URL: <https://github.com/rrrrrredy/skill-security-guard>
- Purpose: Performs static security review of skill packages and SKILL files
  before installation or use.
- Files inspected: `README.md`, `SKILL.md`,
  `references/detection-rules.md`, `scripts/scan.sh`
- SkillOps components supported:
  - Security scanning before deployment
  - Prompt-injection and unsafe-file-access detection
  - Trigger reasonability review
  - Frontmatter compliance checks
  - Structured risk reporting and remediation advice
- Mapping to research questions:
  - RQ1: Secondary evidence for compliance-oriented skill metadata
  - RQ2: Secondary evidence for over-broad trigger descriptions and unsafe
    execution paths
  - RQ3: Primary evidence for linting, scanning, and operational risk control
- Evidence available:
  - `README.md` states a seven-dimension scan model and an A-F rating scheme.
  - `SKILL.md` defines workflows for single-file scans, zip scans, whitelisting,
    and limited auto-fix behavior.
  - `references/detection-rules.md` enumerates detection patterns for prompt
    injection, sensitive file access, privilege and compliance violations,
    malicious scripts, dependency risks, and description overreach.
  - `scripts/scan.sh` shows a concrete entry point for zip extraction and
    `SKILL.md` enumeration.
- Limitations:
  - The evidence is static and heuristic-driven, not a runtime sandbox.
  - Security ratings are repository-defined and not externally calibrated.
  - No executed regression suite or measured false-positive rate was inspected.

## persistent-memory

- Repository URL: <https://github.com/rrrrrredy/persistent-memory>
- Purpose: Provides long-term memory to an agent through daily logs, distilled
  facts, and a compact session-loaded memory file.
- Files inspected: `README.md`, `SKILL.md`, `scripts/memory_manager.py`
- SkillOps components supported:
  - Memory interfaces and persistence rules
  - Forgetting, distillation, and archival behavior
  - Context-size control for long-running agents
  - Setup and health-check workflows
  - Safety restrictions around who can write or recall memory
- Mapping to research questions:
  - RQ1: Secondary evidence for a skill's memory-related interfaces and file
    structure
  - RQ2: Primary evidence for trigger behavior, memory persistence, and
    forgetting controls
  - RQ3: Secondary evidence through health checks and destructive-action
    safeguards
- Evidence available:
  - `README.md` describes a three-layer memory architecture and scheduled
    digestion and distillation jobs.
  - `SKILL.md` specifies explicit trigger phrases, non-trigger boundaries,
    owner-only restrictions, and memory pruning rules.
  - `scripts/memory_manager.py` implements `init`, `digest`, `write-daily`,
    `facts`, `health`, and `archive` commands with concrete file paths and
    an 80-line `MEMORY.md` limit.
- Limitations:
  - The implementation assumes OpenClaw-style directory paths and cron usage.
  - The repository documents the workflow but does not provide measured memory
    accuracy or retrieval performance.
  - Memory quality claims remain design claims until executed benchmarks exist.

## agent-self-audit

- Repository URL: <https://github.com/rrrrrredy/agent-self-audit>
- Purpose: Lets an agent inspect its own operational health across skills,
  memory, cron setup, workspace hygiene, and configuration footprint.
- Files inspected: `README.md`, `SKILL.md`,
  `references/audit-criteria.md`, `scripts/health_check.sh`
- SkillOps components supported:
  - Runtime self-audit and maintenance checks
  - Memory and cron health review
  - Workspace hygiene and skill-count inspection
  - User-confirmed maintenance actions
  - Heartbeat-friendly quick checks
- Mapping to research questions:
  - RQ1: Secondary evidence for operational metadata that a managed skill
    ecosystem may expose
  - RQ2: Secondary evidence for context and memory maintenance pressure
  - RQ3: Primary evidence for self-auditing and operational-risk reduction
- Evidence available:
  - `README.md` documents an eight-point audit and a three-item lightweight
    heartbeat scan.
  - `SKILL.md` defines ordered audit steps and says write operations require
    explicit user confirmation.
  - `references/audit-criteria.md` records concrete thresholds for healthy,
    warning, and critical states.
  - `scripts/health_check.sh` implements quick checks for memory length, skill
    count, and `facts.yaml` presence.
- Limitations:
  - The thresholds are handcrafted rather than empirically validated.
  - The repo is strongly environment-specific.
  - The inspected evidence does not show measured before/after risk reduction.

## lobster-guard

- Repository URL: <https://github.com/rrrrrredy/lobster-guard>
- Purpose: Provides identity-verification and privacy rules for multi-user or
  group-chat agent deployments.
- Files inspected: `README.md`, `SKILL.md`,
  `references/identity-verification.md`
- SkillOps components supported:
  - Identity boundaries between owner and non-owner users
  - Sensitive-operation blacklists
  - Prompt-injection rejection rules
  - Privacy-preserving refusal behavior
  - System-prompt level guardrail guidance
- Mapping to research questions:
  - RQ1: Secondary evidence for non-functional skill constraints and deployment
    assumptions
  - RQ2: Secondary evidence for trigger boundary handling in multi-user
    settings
  - RQ3: Primary evidence for operational guardrails around identity and
    privacy
- Evidence available:
  - `README.md` describes a three-tier identity model and a list of blocked
    sensitive operations.
  - `SKILL.md` includes a concrete configuration snippet for `SOUL.md` or
    `AGENTS.md`, rejection phrasing, and explicit prompt-injection rules.
  - `references/identity-verification.md` specifies how `chat_type` and
    `chat_id` metadata are used to distinguish owner, uncertain, and non-owner
    cases.
- Limitations:
  - The repository is largely configuration guidance rather than executable
    code.
  - Correct behavior depends on trustworthy metadata from the underlying agent
    platform.
  - The focus is narrow: group-chat identity isolation rather than general
    agent security.

## Access Note

All five public repositories listed above were accessible on 2026-04-28 during
manual inspection. No source repository had to be omitted for access reasons in
this artifact pass.
