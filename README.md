# qa-grilling

Pre-implementation QA that tries to break the design before the design becomes code.

`qa-grilling` is an Agent Skill for reviewing product specs, UI designs, architecture, implementation plans, and existing code through a broad set of QA lenses. It is inspired by the questioning style of **Grilling**: do the research first, expose the important unknowns, then ask one decision at a time.

The difference is the goal.

- Grilling asks: **Have we thought this design through?**
- qa-grilling asks: **How can this design fail?**

This is not a test-case generator with a giant checklist. It builds a model of the feature, searches for failure modes, ranks risk, and only grills the human on decisions that cannot be resolved from the available context.

> Don't start with “What tests should we write?” Start with “How can this design fail?”

## What it does

Given a PRD, issue, Figma design, architecture note, API contract, implementation plan, or codebase, qa-grilling:

1. Inspects the available context before asking questions.
2. Models actors, states, transitions, invariants, data, side effects, and dependencies.
3. Explores the design using `Feature × Quality × Event` rather than a flat checklist.
4. Applies a broad set of QA lenses: state, boundary, failure, network, concurrency, persistence, lifecycle, security, privacy, accessibility, UX, emotional trust, observability, and more.
5. Loads domain-specific packs for mobile, web, API, media, payments, notifications, offline sync, AI, and other relevant systems.
6. Separates actual defects from ambiguities, missing rules, test obligations, and accepted risks.
7. Ranks findings by risk.
8. Uses a grilling loop for unresolved product/design decisions — one question at a time, with a recommended default.
9. Produces a QA Design Report, acceptance criteria, test obligations, observability requirements, and residual risks.

## Why pre-implementation QA?

As implementation gets cheaper and faster, the expensive failures move earlier in the process. A missing rule discovered after implementation can force changes to data models, APIs, UI states, error handling, and tests at once.

qa-grilling moves QA upstream:

```text
Idea
  ↓
PRD / Design
  ↓
qa-grilling   ← break the design here
  ↓
Resolved spec
  ↓
Implementation
  ↓
Automated / exploratory QA
  ↓
Release
```

The output can flow directly into implementation:

```text
qa-grilling
   ├─ Spec decisions
   ├─ Acceptance criteria
   ├─ Test obligations
   ├─ Observability requirements
   └─ Residual risks
```

## Exploration model

A flat checklist tends to produce shallow reviews. qa-grilling instead crosses three dimensions:

```text
Feature × Quality × Event
```

For a video upload feature:

```text
upload × reliability × interruption
→ What happens if the app is killed at 73%?

upload × correctness × concurrency
→ What prevents the same video from being uploaded twice?

compression × resource usage × boundary
→ What happens when local storage is nearly full?
```

This lets the skill discover useful failure modes even when the feature is unfamiliar.

See [`references/exploration-model.md`](references/exploration-model.md).

## QA lenses

The core review covers areas such as:

- functional correctness
- state and transition validity
- inputs, validation, boundaries, equivalence classes
- data integrity and persistence
- concurrency, races, idempotency
- retry, recovery, cancellation, partial failure
- network and distributed-system behavior
- app/browser lifecycle
- compatibility and migration
- performance, memory, CPU, storage, thermal and battery impact
- authentication, authorization, security, abuse resistance
- privacy and data handling
- accessibility
- localization, time and timezone behavior
- UX, destructive actions, error recovery
- expectation, trust, anxiety, confusion and user control
- observability, supportability and testability
- rollout, rollback and operational failure

The detailed catalog lives in [`references/qa-lenses.md`](references/qa-lenses.md).

## Domain packs

The skill activates extra concerns when they are relevant instead of checking everything on every feature.

Included packs:

- Mobile
- Web
- API / distributed systems
- Offline / sync
- Media / camera / audio / video
- Notifications / background work
- Payments / transactions
- AI / LLM features
- Location / sensors
- Authentication / account lifecycle
- Analytics / experiments

See [`references/domain-packs.md`](references/domain-packs.md).

## Grilling protocol

qa-grilling does **not** ask the user things it can determine from the repo, spec, design, API schema, existing tests, or adjacent implementation.

When a decision really is unresolved, it asks exactly one question at a time:

```text
The behavior after an interrupted upload is undefined.

Recommended default: persist the upload session and resume from the last confirmed offset on next launch.

Why: restarting large uploads wastes time and bandwidth, and makes background interruption feel like data loss.

Should interrupted uploads resume automatically?
```

The answer is recorded in a decision ledger before moving to the next unresolved risk.

See [`references/grilling-protocol.md`](references/grilling-protocol.md).

## Finding types

Not everything is a bug. qa-grilling classifies findings as:

- **Defect** — the design contradicts itself or produces an invalid/unsafe outcome.
- **Ambiguity** — multiple behaviors are plausible and the intended behavior is not defined.
- **Missing rule** — a reachable state or event has no specified behavior.
- **Test obligation** — behavior is defined, but specific verification is required.
- **Observability gap** — failures may happen but cannot be diagnosed reliably.
- **Accepted risk** — a known risk the team explicitly chooses to carry.

This distinction keeps the review useful instead of turning every edge case into a debate.

## Risk model

Findings are prioritized using these factors:

- severity
- likelihood
- ambiguity
- blast radius
- irreversibility
- detectability

The skill uses P0–P3 priorities rather than pretending the score is precise mathematics.

See [`references/risk-model.md`](references/risk-model.md).

## Output

A completed review produces a compact QA Design Report with:

- scope and model
- P0/P1/P2/P3 findings
- decisions resolved during grilling
- unresolved decisions
- spec changes
- acceptance criteria
- test obligations
- observability requirements
- residual risks

Template: [`templates/qa-design-report.md`](templates/qa-design-report.md)

## Usage

Install or copy this repository into the skills directory used by your Agent Skills-compatible coding agent, preserving `SKILL.md` and the `references/` directory.

Then ask naturally, for example:

```text
Run qa-grilling on this feature before implementation.
```

```text
Review this PRD with qa-grilling. Focus on anything QA will probably catch later.
```

```text
Grill this Figma + API design before we start coding.
```

```text
Use qa-grilling on this implementation plan. Do not generate test cases first; find design holes first.
```

## Examples

- [`examples/video-upload-review.md`](examples/video-upload-review.md)
- [`examples/ui-form-review.md`](examples/ui-form-review.md)

## Design principles

1. **Research before asking.** Never make the human answer something the repository or design already answers.
2. **Model before testing.** Understand states, invariants, dependencies, and data flow before inventing cases.
3. **Risk over volume.** Ten meaningful risks beat one hundred generic checks.
4. **One decision at a time.** Grilling stays focused and interruptible.
5. **Do not invent product policy.** Recommend defaults, but mark assumptions and ask when product intent matters.
6. **QA is more than correctness.** Reliability, privacy, accessibility, performance, operability, and human trust are quality concerns too.
7. **Outputs should be executable.** Turn findings into spec decisions, acceptance criteria, test obligations, and telemetry needs.

## Inspiration

The interaction model is inspired by the Grilling concept described in this article:

https://zenn.dev/sato_frontend/articles/1a85841505b9bb

qa-grilling is an independent QA-oriented skill, not a fork of the original implementation.

Japanese documentation: [`README.ja.md`](README.ja.md)
