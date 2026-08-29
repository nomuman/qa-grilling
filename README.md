# qa-grilling

[日本語](README.ja.md)

`qa-grilling` is an explicit-only Agent Skill for reviewing specifications and designs before implementation.

It models how a design can fail, prioritizes meaningful risks, asks only the product decisions that require human judgment, and converts the result into specification changes, acceptance criteria, test obligations, observability requirements, and residual risks.

> How can this design fail?

## Install

Install a released version rather than tracking a moving `main` branch.

### Codex

```bash
mkdir -p ~/.agents/skills
git clone https://github.com/nomuman/qa-grilling ~/.agents/skills/qa-grilling
git -C ~/.agents/skills/qa-grilling checkout <version>
```

Replace `<version>` with a published tag such as `v1.0.0`.

Codex discovers personal skills under `~/.agents/skills`.

Invoke the skill explicitly:

```text
$qa-grilling review this feature before implementation
```

### Claude Code

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/nomuman/qa-grilling ~/.claude/skills/qa-grilling
git -C ~/.claude/skills/qa-grilling checkout <version>
```

Invoke the skill explicitly:

```text
/qa-grilling review this feature before implementation
```

### Project-only installation

Use one of these locations instead of the personal path:

```text
<project>/.agents/skills/qa-grilling/   # Codex
<project>/.claude/skills/qa-grilling/   # Claude Code
```

Keep the full repository together. `SKILL.md` routes to supporting files only when the review needs them.

### Update

Review the release notes, then switch to a specific release:

```bash
git -C <skill-path> fetch --tags
git -C <skill-path> checkout <version>
```

See [CHANGELOG.md](CHANGELOG.md) and [GitHub Releases](https://github.com/nomuman/qa-grilling/releases). Avoid updating by pulling a moving branch when reproducible review behavior matters.

## Invocation policy

The skill runs only when a user explicitly invokes it.

- Codex: `agents/openai.yaml` sets `policy.allow_implicit_invocation: false`.
- Claude Code: `SKILL.md` sets `disable-model-invocation: true`.

This prevents an ordinary design or code review from unexpectedly becoming a multi-turn grilling session.

## Review modes

### Depth

- `quick`: highest-value risks with minimal supporting material;
- `standard`: default behavior model, core lenses, and relevant domain packs;
- `deep`: broader evidence, explicit state and data models, extended lenses, and failure-chain analysis.

### Interaction

- `interactive`: asks exactly one unresolved P0/P1 product decision per turn;
- `one-shot`: used when requested or when no follow-up turn is available; asks no questions, records recommended assumptions, and completes the report in one turn.

P2/P3 choices use the recommended default unless they materially change architecture, a public contract, or irreversible behavior.

## Safety boundary

Reviewed repositories, documents, designs, webpages, comments, and logs are untrusted data. Embedded instructions do not change the review method or authorize execution, edits, disclosure, or external side effects.

A review is read-only by default. Additional actions require separate user authority and remain subject to the host's permission rules.

## What it reviews

- PRDs, feature specifications, issues, and user stories;
- Figma designs and user flows;
- API contracts and data models;
- architecture, migrations, and implementation plans;
- existing code and tests.

The skill activates only the relevant domain packs for mobile, web, APIs, offline sync, media, notifications, payments, AI, agent skills, location, authentication, analytics, files, and search.

## How it works

1. Inspect available evidence before asking questions.
2. Model actors, states, transitions, data, invariants, side effects, and dependencies.
3. Explore likely failures with `Feature × Quality × Event` and relevant QA lenses.
4. Classify findings as defects, ambiguities, missing rules, test obligations, observability gaps, or accepted risks.
5. Rank concrete consequences as P0/P1/P2/P3 without false precision.
6. Resolve only high-risk human decisions, one at a time when interactive.
7. Produce executable specification changes, acceptance criteria, verification work, observability, and residual risks.

## Output

A substantial review can include:

- prioritized QA findings and evidence;
- a Decision Ledger and documented assumptions;
- specification changes;
- behavioral acceptance criteria;
- test obligations;
- observability and support requirements;
- residual risks and release or rollback conditions.

## Examples

```text
$qa-grilling run a standard interactive review on this PRD
```

```text
/qa-grilling do a one-shot review of this migration plan, focusing on data loss and rollback
```

Reference outputs are available for [video upload](examples/video-upload-review.md) and a [profile form](examples/ui-form-review.md). They are examples only and are not loaded during ordinary reviews.

## Dogfooding case study

The [v1.0.0 self-review](case-studies/self-review-v1.0.0.md) shows the skill reviewing its own baseline, resolving six product decisions, tracing findings into repository changes, and separating static, live-host, CI, and release evidence. A [Japanese version](case-studies/self-review-v1.0.0.ja.md) is also available.

Use the case to decide whether the workflow fits your team. It includes limitations and blocked evidence rather than presenting dogfooding as independent proof.

## Development

Run the deterministic structural checks:

```bash
python3 scripts/validate_skill.py
python3 -B -m unittest discover -s tests -v
```

Behavioral evaluation cases, verification classes, and the cross-host rubric are in [evals/README.md](evals/README.md). Release evidence is stored in [evals/results/v1.0.0-rc1.md](evals/results/v1.0.0-rc1.md). Pull requests run structural validation and validator negative tests in GitHub Actions.

Releases follow Semantic Versioning. `main` is development state; installable behavior is identified by an immutable tag and GitHub Release.

Report security issues privately as described in [SECURITY.md](SECURITY.md).

## License

[MIT](LICENSE)

## Inspiration

The interaction style is inspired by the Grilling concept described in [this article](https://zenn.dev/sato_frontend/articles/1a85841505b9bb).

`qa-grilling` is an independent QA-oriented skill, not a fork of the original implementation.
