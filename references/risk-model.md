# Risk model

qa-grilling uses risk to decide where to spend attention and which unresolved decision to ask first.

Do not pretend risk is exact mathematics. Use factors to reason consistently, then assign a human-readable priority.

## Factors

### Severity
What happens if the failure occurs?

Consider money, data, privacy, security, safety, blocked journeys, trust, accessibility, and operational cost.

### Likelihood
How plausible is the triggering condition in normal or stressed use?

High-frequency user actions, retries, flaky networks, and common lifecycle events deserve more weight than exotic theoretical states.

### Ambiguity
How undefined is the intended behavior?

An implementation team is more likely to diverge when multiple interpretations are reasonable.

### Blast radius
How many users, records, services, or downstream effects can one failure touch?

### Irreversibility
Can the system or user recover automatically? Can support repair it? Is the side effect permanent?

### Detectability
Would the team know the failure happened before users report it? Can they determine whether the side effect committed?

Low detectability increases risk.

## Priority

### P0 — Catastrophic
Examples:

- unauthorized exposure of private data;
- charging customers multiple times;
- irreversible broad data deletion/corruption;
- severe security boundary failure;
- system-wide outage caused by routine behavior.

P0 unresolved design decisions should normally block implementation.

### P1 — Major
Examples:

- core journey becomes unusable;
- important data can be lost or corrupted for a subset of users;
- unrecoverable stuck state;
- common lifecycle/network event breaks the feature;
- accessibility failure blocks a meaningful user group;
- failure cannot be diagnosed and has expensive support impact.

### P2 — Meaningful
Examples:

- recoverable edge-case failure;
- confusing retry/recovery UX;
- moderate performance or battery regression;
- low-frequency compatibility issue;
- non-blocking accessibility degradation.

### P3 — Minor
Examples:

- small inconsistency;
- low-impact polish issue;
- rare scenario with easy recovery and clear diagnostics.

## Tie breakers

When two findings have similar impact, prioritize the one that:

1. affects an invariant;
2. changes architecture/data model/API contract;
3. has irreversible side effects;
4. crosses system boundaries;
5. is hard to detect after release;
6. unlocks several other decisions.

## Risk is contextual

Do not assign P0 because a category sounds scary. A “security” finding can be P3; a UX ambiguity can be P1 if it causes users to delete or publish the wrong thing.

Always explain the concrete consequence.

Untrusted or hostile content is not automatically a P0/P1 vulnerability. Establish a reachable path through available authority, tools, data, and side effects before assigning high priority. When the design already removes that authority, preserve the case as a security test obligation or lower-priority hardening requirement unless evidence shows bypass is possible.
