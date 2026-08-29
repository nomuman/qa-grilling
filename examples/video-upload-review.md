# Example: video upload design review

## Input

```text
Users can select a video up to 500 MB.
The app compresses it and uploads it in the background.
On success the video appears in the user's timeline.
```

## First pass model

```text
select
  ↓
validate
  ↓
compress
  ↓
queued
  ↓
uploading
  ├─ retrying
  ├─ paused/interrupted ?
  ├─ failed
  └─ committed
        ↓
     timeline-visible
```

Potential invariants:

- one user action must not create multiple committed videos;
- a committed video must belong to the correct account;
- a video must not appear as successfully posted before the server commit is known;
- a failed temporary upload must not leak indefinitely in local storage.

## High-value findings

### P1 — Missing interruption semantics

**Type:** MISSING_RULE

The feature says “background upload” but does not define process death, OS suspension, device reboot, or app upgrade while work is in flight.

This affects local persistence, server upload sessions, UI state, and tests.

This deserves grilling.

### P1 — Unknown-success duplicate risk

**Type:** AMBIGUITY

Scenario:

```text
client uploads final chunk
→ server commits video
→ response is lost
→ client times out
→ client retries
```

Without idempotency, the retry can create a duplicate post.

Recommended default: reuse a stable upload ID as the idempotency key until a terminal server state is confirmed.

This deserves grilling if the API contract does not already define it.

### P1 — Account switch during queued upload

**Type:** MISSING_RULE

A background task may survive after logout/account switch. The design must guarantee that queued content cannot be committed to the wrong account.

### P2 — Storage pressure during compression

**Type:** TEST_OBLIGATION or MISSING_RULE depending on implementation

Compression can temporarily require substantial extra local storage. Verify behavior when temporary storage cannot be allocated and guarantee cleanup after failure.

### P2 — Thermal / memory risk

**Type:** TEST_OBLIGATION

Large video compression + upload should be exercised on slower / lower-memory devices and during repeated uploads. This does not require a product decision unless explicit limits or throttling behavior are needed.

## Grilling turn example

```text
An upload can be committed by the server even if the client never receives the success response. Retrying without a stable identity can therefore create a duplicate video.

Recommended default: assign an upload ID before transfer and make all retries with that ID idempotent.

Should the server return the existing committed video when it receives a retry for an already-committed upload ID?
```

## Resulting acceptance criteria example

```text
Given an upload has already been committed for upload_id X
When the client repeats the commit request with upload_id X
Then the server returns the existing committed asset
And no second timeline item is created.
```

## Observability example

Useful structured fields:

- upload_id
- user/account ID in privacy-safe internal form
- local state
- server state
- attempt count
- resume offset
- compression duration
- upload duration
- network category
- structured failure reason
- app version

Do not log media contents, auth tokens, or unnecessary sensitive metadata.
