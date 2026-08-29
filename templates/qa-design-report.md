# QA Design Report

Use this template selectively. Remove sections that do not add value.

## Scope

- Feature / change:
- Artifacts reviewed:
- Review depth:
- Main invariants:

## Behavior model

### Actors

### States and transitions

### Data / source of truth

### Side effects

### External dependencies

## Risk summary

| Priority | Finding | Type | Consequence | Evidence / trigger |
|---|---|---|---|---|
| P0/P1/P2/P3 |  | DEFECT / AMBIGUITY / MISSING_RULE / TEST_OBLIGATION / OBSERVABILITY_GAP / ACCEPTED_RISK |  |  |

Keep this table short. Put detail below only for findings that need it.

## Critical findings

### [ID] Finding title

- Priority:
- Type:
- Scenario:
- Why it matters:
- Current evidence:
- Recommended change:
- Verification:

## Decision ledger

| ID | Decision | Reason | Affected areas | New risk / follow-up |
|---|---|---|---|---|
| D-001 |  |  |  |  |

## Unresolved decisions

List only decisions that still require human/product/design judgment.

## Spec changes

Write these as statements suitable for copying into the product/technical specification.

- 

## Acceptance criteria

Prefer externally meaningful behavior.

```text
Given ...
When ...
Then ...
```

Do not force Given/When/Then if a concise invariant is clearer.

## Test obligations

Group by risk and behavior.

### Must verify before release

- 

### Regression coverage

- 

### Exploratory / environment-dependent

- 

Avoid enumerating a combinatorial matrix unless the combinations truly carry distinct risk.

## Observability requirements

For important operations, consider:

- stable operation / correlation ID;
- state transition;
- attempt / retry count;
- structured failure reason;
- dependency status;
- whether side effect committed;
- duration;
- app/service version;
- privacy-safe environment context.

## Residual risks

| Risk | Why accepted | Mitigation | Revisit trigger |
|---|---|---|---|
|  |  |  |  |

## Release notes / rollout checks

Only include when relevant:

- feature flag / rollout percentage;
- rollback constraint;
- monitoring metric;
- alert threshold;
- compatibility requirement;
- manual recovery procedure.
