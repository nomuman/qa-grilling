# QA lens catalog

This catalog is a source of hypotheses, not a checklist to print verbatim.

Use every core family as a mental scan, then spend depth where the system and risk justify it.

## 1. Functional correctness

Check whether stated business behavior is internally consistent.

Look for:

- contradictory rules;
- missing preconditions/postconditions;
- actions that can succeed without satisfying required conditions;
- derived values that can disagree with source data;
- hidden coupling between features;
- behavior that differs depending on entry point.

## 2. State and transition validity

Model stable and transient states explicitly.

Probe:

- unreachable states;
- reachable but unspecified states;
- illegal transitions;
- transitions triggered twice;
- transitions interrupted halfway;
- UI state diverging from server state;
- stale transient states that never resolve;
- transitions after delete/logout/expiry.

Useful question: **What states can the user or system get stuck in?**

## 3. Inputs and validation

Consider:

- null / missing / empty;
- malformed values;
- unexpected types;
- whitespace and normalization;
- encoding;
- very long values;
- unsupported combinations;
- client validation vs server validation;
- trusted vs untrusted sources.

Validation must protect invariants, not merely improve form UX.

## 4. Boundaries and equivalence classes

Use classic boundary analysis intentionally:

- minimum;
- minimum - 1;
- minimum + 1;
- maximum;
- maximum - 1;
- maximum + 1;
- zero;
- one;
- empty;
- typical representative values.

Check semantic boundaries too: first/last page, first/last day, before/after expiry, free/paid tier, permission granted/denied.

## 5. Data integrity

Ask what must never become inconsistent.

Probe:

- partial writes;
- duplicate records;
- orphaned records/files;
- stale references;
- denormalized values drifting apart;
- client/server disagreement;
- cache/source-of-truth disagreement;
- deletion propagation;
- restore behavior.

Write invariants for high-risk data.

## 6. Persistence and durability

Consider:

- crash during save;
- transaction boundaries;
- fsync/commit assumptions;
- local cache corruption;
- storage quota exhaustion;
- schema evolution;
- recovery after restart;
- persistence of transient states that should not survive restart.

## 7. Concurrency and race conditions

Look for:

- two taps;
- two tabs/windows;
- two devices;
- client + background job;
- admin + user action;
- webhook + client retry;
- read-modify-write races;
- stale optimistic updates;
- lost updates;
- conflicting locks.

Ask which ordering assumptions are actually guaranteed.

## 8. Idempotency and repetition

Any operation that can retry should define repeat semantics.

Check:

- duplicate POST/submission;
- double payment;
- duplicate notification;
- repeated webhook;
- retry after timeout where success status is unknown;
- replay after reconnect;
- repeated destructive action.

Prefer explicit idempotency keys or invariant-enforcing design for irreversible side effects.

## 9. Failure and partial failure

Do not treat failure as a boolean.

Consider:

- fail before side effect;
- side effect succeeds but response fails;
- one of several side effects fails;
- compensation fails;
- dependency A succeeds, dependency B fails;
- retry succeeds after earlier partial success;
- user navigates away during recovery.

Ask whether the system can explain what happened and reach a stable state.

## 10. Retry and recovery

Check:

- retry ownership: client, server, queue, OS;
- retry limits and backoff;
- retry storms;
- retry after authentication expiry;
- resumability;
- cancellation of retries;
- user-visible status;
- permanent vs transient errors;
- dead-letter/manual recovery path.

## 11. Cancellation and interruption

Probe cancellation at every expensive/long-running step.

What happens when:

- user presses cancel;
- user navigates back;
- process is killed;
- OS suspends work;
- request is cancelled but server work continues;
- cancellation arrives after completion.

Cancellation semantics should be explicit when side effects matter.

## 12. Network and distributed behavior

Consider:

- offline at start;
- offline midway;
- very slow connection;
- DNS failure;
- TLS failure;
- connection switch Wi-Fi ↔ cellular;
- captive portal;
- proxy/VPN differences;
- packet loss;
- server timeout;
- client timeout shorter than server execution;
- eventual consistency;
- clock skew;
- duplicate/reordered messages.

Never infer server failure from a client timeout without considering unknown success.

## 13. External dependencies

For every third party or platform service, ask:

- what if it is slow/down;
- what if response schema changes;
- what if quota is exceeded;
- what if credentials expire;
- what if it returns partial or stale data;
- what if a webhook is duplicated/delayed/missing;
- what behavior is owned locally vs externally.

## 14. Lifecycle

Relevant to apps, browsers, workers, and long-running processes.

Check:

- foreground/background;
- process kill;
- restart;
- browser refresh;
- tab close/reopen;
- sleep/wake;
- device reboot;
- session restoration;
- OS reclaiming resources;
- background execution limits.

## 15. Compatibility

Consider:

- old client ↔ new server;
- new client ↔ old/stale data;
- API version mismatch;
- unsupported OS/browser/device;
- feature-flag mismatch;
- cached old frontend assets;
- partially rolled-out backend;
- mixed-version multi-device use.

## 16. Migration

Review both forward and backward movement.

Check:

- schema migration on real historical data;
- partial migration;
- interrupted migration;
- repeated migration;
- rollback after data shape changed;
- old clients writing old format;
- migration ordering across services;
- defaults for newly required fields.

## 17. Performance and latency

Check UX and system behavior under:

- cold start;
- large datasets;
- slow device;
- slow backend;
- repeated navigation;
- concurrent load;
- long lists;
- expensive serialization/deserialization;
- N+1 calls;
- excessive polling.

Define meaningful budgets when performance is a product requirement.

## 18. Memory and resource use

Probe:

- large images/video/audio;
- buffering entire files;
- duplicated in-memory representations;
- leaked controllers/listeners;
- long sessions;
- cache growth;
- background accumulation;
- low-memory devices.

## 19. CPU, thermal, battery and bandwidth

Especially for mobile/media/location/background work.

Look for:

- sustained encoding/decoding;
- tight polling loops;
- retry storms;
- unnecessary wakeups;
- frequent GPS use;
- repeated compression;
- uploads over cellular;
- background activity after user intent has ended.

## 20. Storage and quotas

Consider:

- disk nearly full;
- temporary-file growth;
- cache eviction;
- database limits;
- cloud quota;
- per-user quota;
- cleanup after failed operations;
- duplicate local/remote copies.

## 21. Authentication

Check:

- session expiry during operation;
- refresh token failure;
- logout while background work continues;
- account switching;
- revoked sessions;
- reauthentication for sensitive actions;
- anonymous → authenticated migration.

## 22. Authorization

Do not assume hidden UI is authorization.

Check every object and action for:

- ownership;
- role changes;
- stale permissions;
- direct-object access;
- shared-resource revocation;
- server-side enforcement;
- background jobs using outdated authorization context.

## 23. Security and abuse

Use risk-appropriate threat thinking.

Consider:

- injection;
- unsafe deserialization;
- path/file handling;
- SSRF-style external fetches;
- replay;
- brute force/rate abuse;
- resource amplification;
- enumeration;
- malicious file/content input;
- privilege escalation;
- secret exposure;
- insecure defaults.

Do not turn QA review into exploit instructions; focus on requirements and protections.

## 24. Privacy and data governance

Map sensitive data through its lifecycle.

Check:

- collection necessity;
- default visibility;
- access scope;
- retention;
- deletion;
- export;
- logs/analytics/crash reports;
- screenshots/previews/notifications;
- third-party processing;
- account switching;
- backups and derived data.

Ask whether diagnostics accidentally contain content, tokens, IDs, location, or other sensitive fields.

## 25. Accessibility

Consider:

- screen reader names/roles/states;
- keyboard navigation;
- focus order and focus recovery;
- dynamic type / text scaling;
- contrast and non-color cues;
- touch target size;
- reduced motion;
- captions/transcripts where relevant;
- time limits;
- error identification;
- logical reading order.

Accessibility failures are functional failures for affected users.

## 26. Internationalization and localization

Check:

- text expansion;
- RTL where supported;
- pluralization;
- number/currency formatting;
- sorting/collation;
- Unicode normalization;
- locale-sensitive case conversion;
- addresses/names not fitting local assumptions.

## 27. Date, time and timezone

Probe:

- DST transitions;
- midnight;
- leap day;
- timezone change;
- user timezone vs server timezone;
- locale calendar/formatting;
- clock skew;
- expired-at boundary;
- scheduled jobs around DST;
- historical timezone rules where relevant.

Use absolute instants internally where appropriate and make display semantics explicit.

## 28. UX and human error

Check what happens when users behave reasonably but not ideally.

Consider:

- rapid taps;
- back navigation;
- accidental destructive action;
- unclear loading state;
- no feedback after action;
- action remains enabled while pending;
- retry without explanation;
- silent overwrite;
- dead-end screen;
- error message without recovery action;
- destructive default selection.

## 29. Expectation, trust and user control

A technically correct system can still fail the user.

Ask:

- Does the outcome match what the user reasonably expects?
- Is it obvious what the system did?
- Can the user tell whether an operation is still running?
- Can they undo, cancel, retry, or inspect the result where appropriate?
- Does the system act autonomously without making that clear?
- Could success still leave the user anxious that data was lost, shared, charged, or changed?
- Does an error make recovery feel possible?

Treat surprise, ambiguity, and loss of control as quality risks when they affect behavior or trust.

## 30. Destructive actions and reversibility

For delete, overwrite, send, publish, charge, revoke, reset:

- what is irreversible;
- confirmation quality;
- undo window;
- duplicate action;
- stale target;
- partial completion;
- auditability;
- recovery/support path.

## 31. Observability and diagnostics

For every meaningful failure, ask whether production evidence can answer:

- what operation failed;
- which state it was in;
- which attempt/retry;
- client/server correlation;
- dependency and error category;
- elapsed time;
- whether side effect committed;
- user-visible outcome;
- app/service version;
- privacy-safe environment context.

Prefer structured reason codes over free-text logs.

## 32. Supportability

Can support or operators help a user without guessing?

Consider:

- stable operation IDs;
- user-visible reference IDs for severe failures;
- audit events;
- safe replay/recovery tools;
- status visibility;
- clear distinction between local and server state.

## 33. Rollout and rollback

Check:

- feature flags;
- gradual rollout;
- mixed populations;
- old/new data formats;
- rollback after writes;
- config propagation delay;
- kill switch;
- metrics required to detect regression;
- behavior when flag changes mid-session.

## 34. Analytics and experimentation

Check:

- event fires once vs multiple times;
- semantics match across platforms;
- failed actions are distinguishable from completed actions;
- exposure event timing;
- assignment stability;
- experiment interaction;
- privacy of event parameters;
- analytics failure does not block product behavior.

## 35. Testability

A design that cannot be deterministically exercised is expensive to verify.

Look for:

- hidden clocks/randomness;
- hard-coded external dependencies;
- no way to force failure states;
- background timing that cannot be controlled;
- missing stable identifiers;
- unobservable internal state required for diagnosis;
- environment-only behavior with no test seam.

Recommend test seams where they materially reduce risk.

## 36. Operations and maintenance

Consider:

- job replay;
- queue backlog;
- poison messages;
- stuck work;
- manual intervention;
- config mistakes;
- secret/key rotation;
- backup/restore;
- maintenance windows;
- deploy while work is in flight.

## 37. Content and moderation

When users or models create content, consider:

- empty/huge content;
- unsafe or prohibited content handling;
- reporting/blocking;
- visibility changes;
- deleted content in caches/previews;
- moderation delay;
- appeals/admin actions;
- generated-content labeling when needed.

## 38. Dependency and contract drift

Check whether assumptions are encoded or merely hoped for.

Probe:

- enum additions;
- optional field becomes missing;
- response ordering changes;
- unknown status codes;
- webhook schema evolution;
- SDK behavior differences;
- version pinning and deprecation.

## How to use this file

Do not tell the user “I checked 38 lenses.”

Instead:

1. build the behavior model;
2. activate the relevant lenses;
3. report only findings that change design, tests, observability, or accepted risk;
4. prioritize the small number that deserve human attention.
