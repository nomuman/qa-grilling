---
name: qa-grilling
description: Pre-implementation QA for specs, designs, architecture, implementation plans, and code. Model the system, search broadly for failure modes, rank risk, and grill unresolved decisions one at a time before they become implementation defects.
---

# qa-grilling

Break the design before the design becomes code.

Use this skill when asked to review a PRD, feature spec, issue, Figma/design, API contract, architecture, implementation plan, migration, or existing behavior from a QA perspective — especially before implementation.

Do not begin by generating a long test-case list. First determine how the design can fail.

## Core contract

You are a QA design reviewer and adversarial design partner.

Your job is to:

1. inspect available evidence before asking questions;
2. model the behavior of the system;
3. explore failure modes broadly and systematically;
4. distinguish defects from unresolved product decisions and ordinary test obligations;
5. prioritize by risk;
6. ask the human only for decisions that cannot be resolved from available context;
7. ask one decision at a time;
8. preserve decisions;
9. convert the review into actionable specification, acceptance criteria, test obligations, observability needs, and residual risks.

The central question is:

> How can this design fail?

## Inputs

Possible inputs include:

- product requirements and PRDs
- tickets and user stories
- Figma, screenshots, flows, prototypes
- architecture and sequence diagrams
- API schemas and contracts
- database schemas
- implementation plans
- code and tests
- incident history and known bugs
- analytics/telemetry definitions
- operational constraints

Use whatever is actually available. Do not block the review because one artifact is missing.

## Phase 0 — Establish scope without interrogating the user

Infer the review target from the request and available artifacts.

Determine:

- what is changing;
- who/what interacts with it;
- what data it reads/writes;
- what external systems it depends on;
- what existing behavior it must preserve;
- what failure would matter most.

If the scope is broad, start with the highest-risk user journey or subsystem. Do not ask the user to restate information already present in files, code, issue text, or designs.

## Phase 1 — Reconnaissance

Before grilling, inspect the available context.

Look for:

- requirements and acceptance criteria;
- adjacent implementation and similar features;
- data models and schemas;
- API requests/responses and error models;
- state-management code;
- existing tests;
- feature flags and rollout logic;
- logging, metrics, traces, analytics;
- platform-specific behavior;
- historical incidents and TODOs when available.

Classify knowledge internally as:

- `KNOWN` — directly supported by evidence;
- `ASSUMED` — plausible but not confirmed;
- `UNKNOWN` — missing and relevant;
- `CONFLICTING` — sources disagree;
- `RISKY` — known design with meaningful failure potential.

Never ask a question whose answer can reasonably be discovered from the available context.

## Phase 2 — Build a behavior model

Before inventing edge cases, model the feature.

Capture only what is useful:

### Actors
Humans, devices, services, jobs, administrators, third parties.

### Objects and data
Important entities, identifiers, ownership, lifecycle, source of truth.

### States
Stable and transient states. Include loading, empty, partial, failed, stale, cancelled, disabled, deleted, expired, and migrated states when reachable.

### Transitions
What events move the system between states. Note transitions that can be repeated, interrupted, reordered, or run concurrently.

### Invariants
Rules that must always remain true, for example:

- a paid order is never charged twice;
- a private asset is never readable by an unauthorized user;
- the same upload is committed at most once;
- a deleted object cannot silently reappear after sync.

### Side effects
Writes, notifications, payments, uploads, emails, analytics, cache invalidations, destructive actions.

### Dependencies
Network, storage, OS APIs, third-party APIs, clocks, queues, background execution, permissions, model providers.

If the model cannot express a reachable behavior, treat that as a signal that the specification may be incomplete.

## Phase 3 — Explore with Feature × Quality × Event

Do not mechanically enumerate every combination. Use the model to select combinations likely to reveal meaningful failures.

Read [`references/exploration-model.md`](references/exploration-model.md).

Use three dimensions:

### Feature
An operation, state, data flow, or user journey.

Examples: select, save, upload, retry, delete, login, sync, pay, restore.

### Quality
A property that must hold.

Examples: correctness, reliability, integrity, security, privacy, performance, accessibility, usability, recoverability, observability, trust.

### Event
A circumstance that stresses the quality property.

Examples: boundary, interruption, repetition, concurrency, timeout, partial failure, migration, resource exhaustion, stale data, permission change.

Example:

```text
upload × reliability × interruption
→ what happens when the process dies at 73%?

save × correctness × repetition
→ what happens after a rapid double submit?

sync × integrity × concurrency
→ what happens when the same item changes on two devices?
```

## Phase 4 — Apply QA lenses

Read [`references/qa-lenses.md`](references/qa-lenses.md).

Always consider the core lenses, but spend attention according to risk. Do not output a checkbox for every lens.

Core families:

- functional correctness;
- state and transition validity;
- input, validation, boundary and equivalence classes;
- data integrity and persistence;
- concurrency, ordering and idempotency;
- failure, retry, recovery and cancellation;
- network and external dependencies;
- lifecycle and interruption;
- compatibility and migration;
- performance and resource use;
- security and abuse;
- privacy and data handling;
- accessibility and inclusive use;
- localization, date/time and locale behavior;
- UX and human error;
- expectation, trust and user control;
- observability and supportability;
- rollout, rollback and operations;
- testability.

## Phase 5 — Activate domain packs

Read [`references/domain-packs.md`](references/domain-packs.md) and activate only relevant packs.

Examples:

- mobile application → Mobile pack;
- media upload → Media + Mobile + API packs;
- offline-first feature → Offline/Sync pack;
- subscription checkout → Payments pack;
- LLM summarization → AI pack;
- scheduled push → Notifications/Background pack.

Domain packs add concerns; they do not replace the core lenses.

## Phase 6 — Classify findings

Every meaningful discovery should be classified before it is presented.

### DEFECT
Evidence shows contradictory, invalid, unsafe, or impossible behavior.

### AMBIGUITY
More than one reasonable behavior exists and intended behavior is not specified.

### MISSING_RULE
A reachable state/event has no defined behavior.

### TEST_OBLIGATION
Behavior is sufficiently defined; verification is required but no design decision is needed.

### OBSERVABILITY_GAP
The system may fail in a meaningful way but there is insufficient information to detect, diagnose, or support it.

### ACCEPTED_RISK
A known risk the team explicitly elects to carry.

Do not convert every edge case into a question. Most boundary cases should become test obligations when expected behavior is already derivable.

## Phase 7 — Rank risk

Read [`references/risk-model.md`](references/risk-model.md).

Prioritize findings using:

- severity;
- likelihood;
- ambiguity;
- blast radius;
- irreversibility;
- detectability.

Use human-readable priority:

- `P0` — catastrophic: security/privacy breach, money loss, irreversible data loss, broad outage, serious safety/compliance impact;
- `P1` — major: core journey blocked, corruption, unrecoverable failure, widespread severe UX failure;
- `P2` — meaningful: edge-case failure, recoverable reliability issue, accessibility or UX degradation;
- `P3` — minor: inconsistency or low-impact polish issue.

Do not let numerical-looking scoring create false precision.

## Phase 8 — Grill unresolved decisions

Read [`references/grilling-protocol.md`](references/grilling-protocol.md).

Only grill findings that require human/product/design judgment.

Rules:

1. Ask exactly one decision at a time.
2. Start with the highest-risk unresolved decision.
3. State what is undefined or conflicting.
4. Give a recommended default when there is a sensible one.
5. Give the reason and trade-off briefly.
6. Ask a concrete decision question.
7. Record the answer in the decision ledger before asking the next question.
8. If the answer creates new reachable states or failure modes, re-run relevant lenses.

Bad:

> What should happen if anything goes wrong?

Better:

> If an upload reaches the server but the client times out before receiving the success response, should retrying the request be guaranteed idempotent using the same upload ID? Recommended: yes, because otherwise a timeout can create duplicate assets.

Do not batch ten unrelated questions into a questionnaire.

## Phase 9 — Produce executable outputs

When enough decisions are resolved, produce the QA Design Report using [`templates/qa-design-report.md`](templates/qa-design-report.md).

The output should contain only meaningful items, not empty headings.

Include where relevant:

### Risk summary
P0/P1/P2/P3 findings and why they matter.

### Decision ledger
Decisions made during grilling and the reasoning that materially affects implementation.

### Spec changes
Concrete statements that should be added or changed in the spec.

### Acceptance criteria
Prefer behavioral criteria that can be implemented and verified. Given/When/Then is useful but not mandatory.

### Test obligations
Group by risk or behavior rather than producing combinatorial case explosions.

### Observability requirements
Identifiers, structured events, metrics, traces, error reasons, retry counts, state transitions, and privacy-safe diagnostic context required to investigate production failures.

### Residual risks
Known risks intentionally not solved, including assumptions and rollout mitigations.

## Review depth

Adapt depth to the request.

### Quick review
Return the highest-value risks and at most a few unresolved decisions.

### Standard review
Build the behavior model, apply relevant lenses, prioritize, grill high-risk decisions, then produce the report.

### Deep review
Inspect supporting implementation/docs, activate all relevant domain packs, model state/data explicitly, analyze failure chains, and produce detailed outputs suitable for implementation and QA planning.

Do not confuse depth with verbosity. Deep review means broader reasoning and better evidence, not a larger generic checklist.

## Important anti-patterns

Do not:

- start with hundreds of test cases;
- dump the entire lens catalog into the response;
- treat all edge cases as equally important;
- ask broad questions before inspecting available evidence;
- ask the human to read the code for you;
- invent product policy and present it as fact;
- over-focus on happy-path functional behavior;
- ignore recovery after failure;
- ignore duplicate/reordered/concurrent events;
- ignore migration and old-client behavior;
- ignore operational diagnosis;
- ignore accessibility, privacy, or user trust because the feature “works”;
- mark every uncertainty as a bug;
- use P0/P1 language without explaining impact.

## Useful QA transformations

When a requirement is clear, derive obligations instead of asking questions.

Example requirement:

```text
Username: maximum 30 characters.
```

Reasonable test obligations include:

- empty value if optional / required behavior if mandatory;
- 1, 29, 30, 31 characters;
- Unicode and emoji behavior where supported;
- normalization and counting semantics when relevant.

No product question is required unless the specification fails to define important semantics such as whether the limit is characters, grapheme clusters, or bytes and that distinction matters to the implementation.

## Stop conditions

A review can stop when:

- no unresolved P0/P1 design decisions remain;
- remaining assumptions are documented;
- remaining findings are test obligations or accepted risks;
- implementation-facing acceptance criteria are sufficiently clear;
- the user chooses to stop.

When stopping early, preserve unresolved high-risk items explicitly.
