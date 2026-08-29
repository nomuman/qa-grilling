# Grilling protocol

The grilling loop exists to resolve design decisions, not to interview the user for context the agent could discover itself.

Use it only in interactive mode. In one-shot or non-interactive work, apply the recommended default, record it as an assumption, and complete the report without asking a question.

## Before asking

For each candidate question:

1. Search available specs, code, tests, designs, schemas, and adjacent behavior.
2. Decide whether the answer is already known or safely derivable.
3. If behavior is defined, convert it to a test obligation instead of asking.
4. If implementation is obviously defective, report a defect instead of asking for product preference.
5. Ask only when a meaningful product/design choice remains.

## Question shape

Each turn should contain one decision.

Use this structure when helpful:

```text
[What is undefined/conflicting]

Recommended default: [one concrete choice]

Why: [short reason / trade-off]

[One decision question]
```

Do not force the exact wording when a shorter natural question works.

## Good questions

Good questions:

- point to a reachable scenario;
- explain why the decision matters;
- separate recommendation from known fact;
- are answerable without writing an essay;
- resolve one branch of the design tree.

Example:

```text
The server may complete an upload after the client times out, so a retry can arrive after the asset already exists.

Recommended default: use the same upload ID as an idempotency key until the operation reaches a terminal state.

Should retries with the same upload ID return the existing committed asset rather than create a second one?
```

## Bad questions

Avoid:

```text
What edge cases should we support?
```

```text
What do you want the error handling to be?
```

```text
Please answer these 17 questions before I continue.
```

These push QA reasoning back onto the user.

## Decision ledger

After each answer, record:

```text
Decision ID: D-001
Context: upload interrupted after server has accepted chunks
Decision: resume automatically on next launch
Reason: reduce retransmission and perceived data loss
Affected areas: local persistence, upload API, UI state, tests, telemetry
New risks introduced: stale/expired upload session on resume
```

IDs are optional in lightweight reviews but useful for deep reviews.

## Re-run after decisions

A decision can create new states. Re-run the relevant lenses.

Example:

```text
Decision: auto-resume upload
```

New QA questions may include:

- What if credentials expired before resume?
- What if the server discarded the upload session?
- What if the user deleted the local source file?
- What if the user switched accounts?

Do not blindly recurse forever. Stop when new branches are low-risk, defined, or ordinary test obligations.

## Ordering

Ask in this order:

1. P0 unresolved decisions;
2. P1 unresolved decisions;
3. decisions that unlock several downstream branches;
4. P2 only when they materially affect design or acceptance criteria;
5. avoid grilling P3 polish unless explicitly requested.

By default, ask only unresolved P0/P1 decisions. Ask a P2 decision only when it materially changes architecture, a public contract, or irreversible behavior. Otherwise apply the recommended default and record it as an assumption.

## User says “use your judgment”

Choose the recommended default, mark it as an assumption/decision, and continue. Do not keep asking for confirmation.

## User stops the review

Return what is known so far, including unresolved P0/P1 decisions and residual risks. Never discard the decision ledger.
