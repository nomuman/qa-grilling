# Case study: qa-grilling reviews itself

[日本語](self-review-v1.0.0.ja.md)

This is a public, edited dogfooding record for the review that prepared `qa-grilling` for `v1.0.0`. It shows what the skill found, which decisions required human judgment, how the findings changed the repository, and which claims were actually verified.

It is not a raw conversation transcript. Private context, local paths, account information, and unrelated host diagnostics were removed.

## Why this case matters

A prospective adopter needs more than a polished example output. This case answers:

- Can the skill find defects in its own instructions and release process?
- Does grilling lead to explicit decisions rather than an endless questionnaire?
- Can findings be traced into repository changes and verification?
- Does the evidence justify the release claim?

## Review target

- Baseline commit: [`38df618`](https://github.com/nomuman/qa-grilling/commit/38df618facdc572ec82f0f32e7a2d2e006a0de77)
- Candidate label: `v1.0.0-rc1` on [PR #1](https://github.com/nomuman/qa-grilling/pull/1)
- Intended immutable release: `v1.0.0`; it is not release evidence until the tag and GitHub Release exist
- Review style: interactive, then implementation and one-shot release-candidate evaluation
- Primary artifacts: `SKILL.md`, references, examples, README files, repository metadata, and release configuration

Public-safe equivalent invocation:

```text
$qa-grilling perform a deep pre-release review of this skill itself.
Focus on invocation behavior, safety boundaries, context efficiency,
cross-host compatibility, evaluation quality, and release integrity.
Ask only unresolved high-risk decisions one at a time.
```

## Decisions resolved during grilling

| Decision | Outcome | Why it mattered |
|---|---|---|
| D-001 | Explicit-only in Codex and Claude Code | Ordinary reviews must not unexpectedly become a multi-turn grilling session |
| D-002 | MIT License | Adoption and redistribution rights must be clear |
| D-003 | Semantic Versioning, immutable tags, Releases, and a changelog | Review behavior must be reproducible and rollbackable |
| D-004 | Progressive disclosure by review depth and domain | Review evidence needs the context budget more than a large always-loaded catalog |
| D-005 | Interactive asks only unresolved P0/P1 decisions by default; one-shot never stalls on a question | The workflow must be useful in both conversations and non-interactive runs |
| D-006 | `standard` is the default depth | The default should model behavior without forcing the cost of a deep audit |

## Findings and outcomes

| Finding ID | Decision / assumption | Changed artifact | Acceptance / test | Verification status |
|---|---|---|---|---|
| F-001 | defect; no product decision | `SKILL.md` safety boundary | AC-001: artifact instructions never grant authority; E-006/E-007 | static/local pass; live-host negative smoke required |
| F-002 | D-002 | `LICENSE`, `scripts/validate_skill.py` | AC-002: MIT artifact exists and validates | static/local pass |
| F-003 | D-001 | `agents/openai.yaml`, `SKILL.md` | AC-003: explicit invocation works and ordinary review stays inactive; E-019 | Codex explicit invocation pass; implicit and Claude runs blocked/unverified |
| F-004 | D-003 | `CHANGELOG.md`, READMEs, release workflow | AC-004: published install resolves to immutable `v1.0.0` | blocked until tag, Release, and post-release install exist |
| F-005 | D-004/D-006 | `SKILL.md`, `references/domains/*` | AC-005: E-008 loads only relevant packs | static/local pass; Codex routing smoke pass |
| F-006 | implementation assumption A-001 | `scripts/validate_skill.py`, `tests/`, workflow, `evals/` | AC-006: negative fixtures and candidate CI pass | local negative tests pass; final-candidate CI required |
| F-007 | defect; no product decision | READMEs | AC-007: examples and case studies stay outside runtime routing | static/local pass |
| F-008 | implementation assumption A-002 | `SKILL.md`, report template, `evals/results/` | AC-008: evidence classes are never substituted | static/local pass |
| F-009 | implementation assumption A-003 | `references/domains/agent-skills.md` | AC-009: E-021 activates Agent Skill concerns | static/local pass; Codex live routing pass |
| F-010 | implementation assumption A-004 | `SKILL.md`, E-016/E-017 | AC-010: unrelated accessible context is not inspected or reported | isolated Codex smoke pass; Claude required |
| F-011 | implementation assumption A-005 | `SKILL.md`, E-015 | AC-011: quick review stays focused | policy and test added; before/after efficiency improvement unverified |
| F-012 | implementation assumption A-006 | report template | AC-012: substantial review maps finding through evidence | static/local pass; adopter usability not independently measured |

## Before and after

Before the review, the skill was a broad monolithic prompt with no explicit invocation policy, safety/authority boundary, license, deterministic validation, CI, immutable release process, or cross-host rubric.

The `v1.0.0` candidate has:

- explicit-only invocation metadata for both supported hosts;
- an untrusted-input and read-only review boundary;
- depth and interaction modes with stopping conditions;
- core lenses plus selectively loaded domain packs;
- an Agent Skill-specific QA pack;
- evidence coverage and end-to-end traceability;
- structural validation with negative tests;
- 22 behavioral cases and persistent release-candidate evidence;
- MIT licensing, security reporting, changelog, CI, and immutable-release instructions.

## Evidence and limitations

| Verification class | Evidence | Limitation |
|---|---|---|
| static/local | Repository validation, negative fixtures, Markdown/YAML checks, independent rubric review | Static inspection cannot prove host behavior |
| live-host/device/E2E | Codex explicit invocation and adversarial one-shot smoke | Implicit non-activation and the calibrated final candidate must still be run |
| blocked/unverified, target: live-host | Claude Code 2.1.251 is installed but unauthenticated | Authentication-dependent behavior must pass before cross-host certification |
| CI | Pull-request validation | CI proves only the checks it runs |
| release/production | Tagged installation and post-release smoke | Available only after publication |

The case intentionally preserves blocked and unverified evidence. Dogfooding is useful, but it can share the author's assumptions. Independent and cross-host evaluation remain necessary.

## Adoption guidance

This skill is a good fit when a team wants to resolve risky design ambiguity before implementation and turn the result into acceptance criteria, verification work, observability, and residual risk.

It is not a replacement for domain experts, legal or safety review, device/E2E testing, CI, release validation, or production evidence. It should not be used as a reason to execute commands or modify systems during a review-only request.

See the [behavior rubric](../evals/README.md) and [v1.0.0 release-candidate record](../evals/results/v1.0.0-rc1.md) for the release gates behind this case.
