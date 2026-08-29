# qa-grilling

[日本語](README.ja.md)

`qa-grilling` is an Agent Skill for reviewing specs and designs before implementation.

It looks for problems that are often found later in QA: missing states, unclear behavior, boundary cases, retries, network failures, duplicate actions, data loss, permissions, accessibility, performance, privacy, and more.

It is based on the idea of Grilling, but focuses on one question:

> How can this design fail?

## What it reviews

You can use it with:

- PRDs and feature specs
- issues and user stories
- Figma designs and UI flows
- API contracts
- architecture and implementation plans
- existing code

## How it works

1. Read the available spec, design, code, and tests.
2. Model states, transitions, data, side effects, and dependencies.
3. Look for failure modes from multiple QA perspectives.
4. Rank findings by risk.
5. Ask only the questions that require a product or design decision, one at a time.
6. Turn the result into concrete changes, acceptance criteria, and test points.

The skill uses `Feature × Quality × Event` to find cases that a flat checklist can miss.

Example:

```text
upload × reliability × interruption
→ What happens if the app is killed during upload?

upload × correctness × concurrency
→ What prevents the same file from being uploaded twice?
```

## QA areas

The core review includes:

- state transitions
- boundaries and invalid input
- retry, cancel, and recovery
- network failures and timeouts
- concurrency and idempotency
- persistence and data integrity
- app and browser lifecycle
- compatibility and migration
- performance and resource usage
- security and privacy
- accessibility and localization
- UX and destructive actions
- user trust and control
- observability and supportability
- rollout and rollback

Extra domain checks are included for mobile, web, API, offline sync, media, notifications, payments, AI, location, authentication, and analytics.

See:

- [`references/qa-lenses.md`](references/qa-lenses.md)
- [`references/domain-packs.md`](references/domain-packs.md)
- [`references/exploration-model.md`](references/exploration-model.md)

## Output

A review can produce:

- prioritized findings
- unresolved decisions
- spec changes
- acceptance criteria
- test obligations
- observability requirements
- residual risks

Template: [`templates/qa-design-report.md`](templates/qa-design-report.md)

## Usage

Copy or clone this repository into the skills directory used by your Agent Skills-compatible coding agent.

Then ask, for example:

```text
Run qa-grilling on this feature before implementation.
```

```text
Review this PRD with qa-grilling and find issues QA is likely to catch later.
```

```text
Review this Figma and API design before we start coding.
```

## Examples

- [`examples/video-upload-review.md`](examples/video-upload-review.md)
- [`examples/ui-form-review.md`](examples/ui-form-review.md)

## Grilling

If the answer already exists in the spec, design, code, or tests, the skill should not ask the user.

If a decision is still missing, it asks one question at a time and records the answer before moving on.

See [`references/grilling-protocol.md`](references/grilling-protocol.md).

## Inspiration

The interaction style was inspired by the Grilling concept described here:

https://zenn.dev/sato_frontend/articles/1a85841505b9bb

`qa-grilling` is an independent QA-oriented skill, not a fork of the original implementation.
