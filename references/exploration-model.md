# Exploration model: Feature × Quality × Event

The purpose of this model is to generate useful QA hypotheses without relying on a fixed checklist.

A review starts from the behavior model, then deliberately crosses three dimensions.

## 1. Feature

A feature is any meaningful operation, state, data flow, or user journey.

Examples:

- create
- edit
- delete
- restore
- submit
- retry
- cancel
- upload
- download
- sync
- login
- logout
- refresh token
- grant permission
- revoke permission
- pay
- refund
- notify
- import
- export
- migrate

Decompose only as far as useful. “Checkout” may be enough for a simple review; a risky payment flow may need authorize/capture/refund/reconcile separately.

## 2. Quality

A quality is a property that should remain true while the feature operates.

Examples:

- correctness
- consistency
- integrity
- durability
- reliability
- availability
- recoverability
- idempotency
- ordering
- security
- privacy
- performance
- efficiency
- accessibility
- usability
- predictability
- user control
- trust
- observability
- supportability
- compatibility

## 3. Event

An event is a condition that stresses that quality property.

Use events such as:

- minimum / maximum boundary
- just below / just above boundary
- empty / missing / null
- malformed input
- stale input
- duplicate action
- rapid repetition
- concurrent action
- reordered event
- timeout
- cancellation
- partial success
- partial failure
- dependency outage
- slow dependency
- reconnect
- process kill
- background / foreground transition
- permission revoked
- authentication expires
- device restart
- clock/timezone change
- migration from old version
- rollback to old version
- resource exhaustion
- quota/rate limit
- very large data
- very old data
- data deleted elsewhere
- user changes account
- admin changes policy

## How to use the matrix

Do not enumerate the Cartesian product. Select combinations based on the architecture, user journey, blast radius, and historical risk.

Ask:

1. Which features have irreversible or expensive side effects?
2. Which qualities matter most for those features?
3. Which events can plausibly break those qualities?
4. Can two individually safe events combine into a dangerous failure chain?

Examples:

```text
payment.capture × idempotency × client timeout
→ Did the charge succeed even though the client thinks it failed?

profile.delete × recoverability × network interruption
→ Can the user end in a half-deleted account state?

sync.update × integrity × concurrent action
→ Which version wins if two devices edit before either syncs?

push.send × privacy × account change
→ Can a notification for the previous account appear after logout/login?

AI.generate × trust × retry
→ Can the same user action silently produce materially different output after an automatic retry?
```

## Failure chains

Single-edge analysis is not enough for high-risk systems. Look for chains:

```text
network timeout
→ client retries
→ request is not idempotent
→ duplicate server-side object
→ downstream notification sent twice
```

or:

```text
app backgrounded
→ OS suspends work
→ local state says “uploading”
→ server expires session
→ app resumes
→ UI never leaves “uploading”
```

When a chain crosses multiple components, record the invariant that should break the chain.

## Invariant-first exploration

For critical behavior, define an invariant and try to violate it.

Examples:

- `charge_count(order_id) <= 1`
- `unauthorized_read(private_asset) == impossible`
- `committed_upload(upload_id) is unique`
- `deleted_item cannot be resurrected by stale sync`

Then search for events, retries, races, migrations, and partial failures that could violate the invariant.

This is often more effective than listing UI-level test cases.
