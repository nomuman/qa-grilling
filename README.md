# qa-grilling

[日本語](README.ja.md)

`qa-grilling` is an Agent Skill for reviewing specs and designs before implementation.

It looks for problems that are often found later in QA: missing states, unclear behavior, boundary cases, retries, network failures, duplicate actions, data loss, permissions, accessibility, performance, privacy, and more.

> How can this design fail?

## Install

### Codex

Install for your user account:

```bash
mkdir -p ~/.agents/skills
git clone https://github.com/nomuman/qa-grilling ~/.agents/skills/qa-grilling
```

Codex reads personal skills from `~/.agents/skills`.

Then use it from Codex:

```text
Use $qa-grilling to review this feature before implementation.
```

You can also mention the skill with `$qa-grilling` and give it a PRD, implementation plan, Figma context, or code to review.

To update:

```bash
git -C ~/.agents/skills/qa-grilling pull
```

### Claude Code

Install for your user account:

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/nomuman/qa-grilling ~/.claude/skills/qa-grilling
```

Claude Code reads personal skills from `~/.claude/skills`.

Then run:

```text
/qa-grilling
```

or ask naturally:

```text
Use qa-grilling to review this feature before implementation.
```

To update:

```bash
git -C ~/.claude/skills/qa-grilling pull
```

### Install only for one project

For Codex, put the skill under:

```text
<project>/.agents/skills/qa-grilling/
```

For Claude Code:

```text
<project>/.claude/skills/qa-grilling/
```

Keep the whole repository together. `SKILL.md` uses files in `references/`, `templates/`, and `examples/`.

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
→ What happens if the same video is uploaded twice?
```

## QA perspectives

The review covers areas including:

- states and transitions
- boundaries and invalid input
- network failures and retries
- concurrency and duplicate actions
- persistence and data integrity
- app and browser lifecycle
- compatibility and migration
- performance and resource use
- security and privacy
- accessibility
- UX and destructive actions
- user trust and control
- observability and recovery

Extra domain checks are loaded for mobile, web, APIs, offline sync, media, notifications, payments, AI, location, authentication, and analytics when relevant.

See:

- [`references/qa-lenses.md`](references/qa-lenses.md)
- [`references/domain-packs.md`](references/domain-packs.md)
- [`references/exploration-model.md`](references/exploration-model.md)

## Output

A review can produce:

- prioritized QA findings
- unresolved design decisions
- specification changes
- acceptance criteria
- test obligations
- observability requirements
- residual risks

The report template is in [`templates/qa-design-report.md`](templates/qa-design-report.md).

## Examples

```text
Use $qa-grilling on this PRD before we implement it.
```

```text
Review this Figma flow with qa-grilling. Find things QA is likely to catch later.
```

```text
Run qa-grilling on this implementation plan. Focus on data loss and recovery.
```

Example reviews:

- [`examples/video-upload-review.md`](examples/video-upload-review.md)
- [`examples/ui-form-review.md`](examples/ui-form-review.md)

## Inspiration

The interaction style is based on the Grilling concept described here:

https://zenn.dev/sato_frontend/articles/1a85841505b9bb

`qa-grilling` is an independent QA-oriented skill, not a fork of the original implementation.
