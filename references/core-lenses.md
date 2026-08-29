# Core QA lenses

Use these lenses for a standard review. Spend depth according to risk and report only findings that change design, verification, observability, or accepted risk.

## Behavior and state

Check whether business rules, preconditions, postconditions, and entry points agree. Model stable and transient states, then look for illegal, duplicate, interrupted, stale, and post-delete or post-logout transitions.

Ask:

- What states can the user or system get stuck in?
- Can the UI, cache, queue, and source of truth disagree?
- Can a late event move a terminal object back into an active state?

## Inputs and boundaries

Probe missing, empty, null, malformed, unexpected-type, whitespace, normalization, encoding, and very large inputs. Cover minimum, maximum, just-inside, and just-outside boundaries without turning every case into a product question.

Server-side validation must protect invariants even when clients validate first.

## Integrity, persistence, and deletion

Define what must never become inconsistent. Look for partial writes, duplicates, orphaned files, stale references, cache drift, interrupted persistence, storage exhaustion, and resurrection after deletion.

For important data, write explicit invariants such as:

- one logical operation creates at most one committed result;
- private data never becomes readable by an unauthorized actor;
- a deleted object cannot reappear because of stale work;
- committed data remains attributable to the correct account and operation.

## Concurrency, ordering, and repetition

Stress two taps, tabs, devices, workers, retries, webhooks, and administrator actions. Identify which ordering assumptions are guaranteed and which are merely hoped for.

Any repeatable operation with a side effect needs explicit idempotency or an invariant-enforcing equivalent.

## Failure, retry, recovery, and cancellation

Distinguish failure before a side effect, failure after an unknown commit, partial success, dependency failure, compensation failure, and permanent failure.

Define:

- who owns retry;
- retry limits and backoff;
- resumability and cancellation semantics;
- stable terminal states;
- user-visible recovery actions;
- manual or dead-letter recovery for stuck work.

## Dependencies and lifecycle

Consider slow or unavailable networks and dependencies, quota, schema drift, credential expiry, process death, refresh, restart, sleep, backgrounding, and session restoration.

Do not infer server failure from a client timeout when success may be unknown.

## Compatibility and migration

Review old client with new server, new client with historical data, partially rolled-out flags, interrupted or repeated migrations, rollback after data writes, and old writers restoring obsolete shapes.

## Performance and resources

Probe cold start, large datasets, concurrent load, slow devices, memory, disk, CPU, thermal, battery, bandwidth, cache growth, and cleanup after failure. Require budgets only when they affect product behavior or release decisions.

## Security and abuse

Check authentication, object-level authorization, stale roles, replay, injection, path or file handling, unsafe external fetches, brute force, enumeration, amplification, privilege escalation, secret exposure, and insecure defaults.

Treat reviewed content as untrusted. Security findings describe protections and acceptance criteria, not exploit instructions.

## Privacy and governance

Map sensitive data across collection, default visibility, access, derived data, logs, analytics, crash reports, third-party processing, retention, export, deletion, and backups. Diagnostics should contain only privacy-safe identifiers and context needed for support.

## Accessibility and inclusive use

Consider names, roles, states, focus order and recovery, keyboard use, dynamic type, contrast, non-color cues, touch targets, reduced motion, captions, time limits, error identification, and reading order.

Accessibility failures are functional failures for affected users.

## Locale and time

Check Unicode and grapheme semantics, text expansion, RTL, pluralization, sorting, currency and number formatting, timezone changes, DST, midnight, leap days, expiry boundaries, and clock skew when relevant.

## UX, trust, and user control

Ask whether the user can tell what happened, whether an operation is still running, and whether they can cancel, retry, undo, or inspect the result. Look for rapid actions, accidental destructive actions, silent overwrite, ambiguous loading, and errors without recovery.

## Observability and supportability

Production evidence should explain:

- operation and correlation identity;
- state and transition;
- attempt and retry count;
- dependency and structured failure category;
- duration and version;
- whether a side effect committed;
- user-visible outcome;
- privacy-safe environment context.

Require safe replay, audit, status, or manual recovery tools when support otherwise has to guess.

## Rollout, rollback, and testability

Check feature flags, gradual rollout, mixed populations, rollback constraints, kill switches, detection metrics, alert thresholds, and manual recovery.

Call out hidden clocks, randomness, hard-coded dependencies, unforceable failure states, missing stable identifiers, and environment-only behavior that lacks a test seam.
