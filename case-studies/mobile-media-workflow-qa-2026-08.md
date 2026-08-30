# Case study: applying qa-grilling to a mobile media workflow

[日本語](mobile-media-workflow-qa-2026-08.ja.md)

This is a public, edited record of applying `qa-grilling` to a mobile app that captures, imports, and uploads media. The source project, internal environments, implementation identifiers, and account details are intentionally omitted.

## Purpose

The review looked beyond the happy path for a failure chain like this:

```text
an operation fails or is interrupted
  → the screen or process ends
  → state becomes unknown or the source is lost
  → retry is impossible, duplicates appear, or ownership is mixed
```

## Review profile

| Item | Details |
|---|---|
| Review depth | `standard` |
| Interaction | `interactive` for high-risk decisions |
| Main lenses | state, persistence, retry, lifecycle, ownership, idempotency, cache, observability |
| Domain packs | mobile, media, files/imports, offline/sync, API/distributed |
| Skill | `qa-grilling v1.0.0` |

The repository name, commits, PR numbers, internal distribution details, backend identifiers, and local paths are intentionally excluded from this record.

## Behavior model

### Actors and dependencies

- User: captures, imports, retries, discards, and chooses whether to delete source media.
- Mobile app: manages local files, processing state, durable work, and cache.
- External media: the source of imported data and a possible deletion target.
- Authentication, remote storage, and database: sources of truth for ownership, media, and metadata.
- OS-managed background work: resumes work beyond the screen or process lifetime.

### States and transitions

```text
captured / imported
  → local copy or durable queue
  → processing / uploading
  → completed
       → explicit deletion, or keep
  → failed / retryable
       → retry with the same logical identity, or explicit discard
```

### Invariants

- An unconfirmed source remains until retry or explicit discard.
- Source deletion requires confirmed success and an explicit user action.
- Work does not start for a previous owner after the authenticated owner changes.
- Retrying one logical operation does not intentionally create another result.
- The cache returns complete data only and excludes expired or empty entries.
- Temporary failures and slow dependencies cannot make the entire screen wait forever.

## Findings and decisions

| Finding | Type / priority | Decision | Change summary |
|---|---|---|---|
| F-001 | DEFECT / P1 | D-001 | Retain source media after failure or interruption; offer retry and explicit discard |
| F-002 | DEFECT / P1 | D-002 | Persist state and ownership so work can resume safely beyond the screen |
| F-003 | DEFECT / P2 | D-003 | Keep the logical operation identity stable across retries |
| F-004 | DEFECT / P2 | D-004 | Store cache entries atomically and handle expiry, capacity, and empty data |
| F-005 | MISSING_RULE / P2 | D-005 | Bound listener recovery, pagination, large reads, and concurrency |
| F-006 | TEST_OBLIGATION / P2 | A-001 | Pin failure, retry, deletion, recovery, and ownership boundaries with tests |

### F-001/F-002: durability and recovery

When work belongs only to a screen, errors, backgrounding, process termination, and network loss can orphan the “uploading” state. Deleting the source first turns the failure into unrecoverable data loss.

After the change, a failed operation remains visible and the user can retry or explicitly discard it while the source is retained. OS-managed background work and durable state separate screen lifetime from operation lifetime.

### F-003: ownership and idempotency

Resume can happen after the authenticated owner has changed. Retrying with a new identifier can create a second result for the same media.

The updated design retains the owner and logical operation identity, checks ownership before starting, and reuses the same identity on retry.

### F-004/F-005: cache and dependency boundaries

A direct cache write can expose partial data. A listener that ends temporarily, an unbounded read, or unlimited concurrency can produce an empty screen, an indefinite wait, or excessive resource use.

The updated design writes a complete temporary file before moving it into the cache, checks expiry/capacity/empty data, and bounds reconnects, pagination, and concurrency.

## Decision ledger

| ID | Decision | Reason |
|---|---|---|
| D-001 | Do not delete source media before confirmed success | Avoid unrecoverable loss |
| D-002 | Persist state and ownership | Survive OS lifecycle and account switching |
| D-003 | Reuse the logical identity on retry | Avoid duplicate results |
| D-004 | Store cache entries atomically | Prevent partial reads |
| D-005 | Bound recovery, pagination, and concurrency | Limit transient-failure and large-data impact |

## Before and after

| Area | Before | After |
|---|---|---|
| Failure | Source and state handling were unclear | Retention, visibility, retry, explicit discard |
| Lifecycle | Screen and operation lifetime were coupled | Durable state and OS-managed work separate them |
| Ownership | Resume boundary was implicit | Ownership is checked before work starts |
| Retry | Could create a duplicate logical result | Reuses the logical identity |
| Cache | Partial writes and empty entries had weak boundaries | Atomic store plus expiry/capacity/empty checks |
| Dependencies | End, large reads, and unlimited concurrency lacked rules | Bounded retry, pagination, and concurrency |

## Acceptance criteria

```text
AC-001: A failed or interrupted operation retains its source for retry or explicit discard.
AC-002: Source deletion occurs only after confirmed success and explicit user action.
AC-003: Work can resume safely from durable state after the screen or process ends.
AC-004: A retry reuses the logical identity and does not intentionally create a duplicate.
AC-005: Cache reads return complete data only and exclude expired or empty entries.
AC-006: Recovery, read volume, and concurrency are bounded during transient failure or large data.
AC-007: Local, device/E2E, CI, release, and blocked evidence remain separate.
```

## Test obligations

- T-001: Source retention after failure, timeout, cancellation, backgrounding, and process termination.
- T-002: Retry, discard, post-success deletion, and deletion failure recovery.
- T-003: Account switching, expired authentication, owner mismatch, and same-identity retry.
- T-004: Duplicate names, malformed input, empty data, expiry, capacity, and atomic store.
- T-005: Listener end, reconnect limits, pagination, empty/delayed data, large data, and concurrency limits.
- T-006: Real-device external media, OS lifecycle, network loss, and background recovery.

## Evidence coverage

| Evidence | Verification class | Status |
|---|---|---|
| Structural checks, unit tests, and diff checks | static/local | pass |
| Supported-device external media and lifecycle checks | live-host/device/E2E | blocked / unverified |
| Main-branch automated checks | CI | environment-dependent; local pass is not a substitute |
| Post-distribution real-environment and production traffic | release/production | not verified |

## Residual risks

- Real-device media, permissions, and background limits are not proven by local tests.
- Authentication, remote storage, or OS changes can leave retry outcomes unknown.
- Long-lived queued work, device capacity, and operational manual recovery require separate monitoring.
- Production configuration and post-distribution behavior must not be inferred from local or CI results.

## Adoption judgment

`qa-grilling` was useful because it started from failure events and invariants rather than a happy-path checklist, then connected the gaps to implementation and verification work.

This public version preserves the method and evidence shape needed for adoption decisions while omitting identifying project and internal information. The case study itself is not device, CI, release, or production proof; those gates remain separate.
