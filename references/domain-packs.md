# Domain packs

Activate packs based on the system under review. Packs add domain-specific failure hypotheses to the core QA lenses.

Do not apply every pack to every feature.

## Mobile

Additional concerns:

- foreground/background transitions;
- process death and restoration;
- OS background execution limits;
- permission grant/deny/revoke while running;
- app upgrade/downgrade behavior;
- deep links and multiple entry points;
- device storage pressure;
- low-memory devices;
- orientation/window-size changes where relevant;
- interrupted install/update;
- notification tap into stale state;
- account switch with local cached data;
- battery, thermal and cellular data impact;
- platform differences between iOS/Android.

## Web

Additional concerns:

- refresh/back/forward navigation;
- multiple tabs;
- stale cached assets;
- cookie/session expiry;
- CSRF protections where applicable;
- browser storage disabled/full;
- service worker/cache version mismatch;
- browser compatibility;
- responsive layouts and zoom;
- keyboard/focus behavior;
- duplicate form submission;
- optimistic UI after server rejection.

## API / distributed systems

Additional concerns:

- client timeout vs server success;
- idempotency;
- retries at several layers;
- request ordering;
- eventual consistency;
- pagination stability;
- duplicate/reordered webhook delivery;
- rate limits and quotas;
- schema evolution;
- partial dependency failure;
- clock skew;
- correlation IDs;
- backwards compatibility;
- exactly-once assumptions that are not actually guaranteed.

## Offline / sync

Additional concerns:

- source of truth;
- mutation queue/outbox semantics;
- conflict resolution policy;
- same item edited on two devices;
- delete vs edit conflict;
- stale item resurrection;
- retry ordering;
- dependency between queued operations;
- authentication expiry while queued;
- account switch with queued writes;
- media/file availability during delayed sync;
- local migration while unsynced work exists;
- sync cursor invalidation;
- clock-based conflict errors.

Write explicit invariants for deletion and ownership.

## Media / camera / audio / video

Additional concerns:

- large files;
- codec/container/device differences;
- metadata orientation/rotation;
- corrupt/truncated files;
- duration/resolution/frame-rate extremes;
- memory pressure from decode/encode;
- temporary storage requirements;
- compression quality and repeated recompression;
- background interruption;
- upload resume;
- local source deleted before completion;
- thumbnail/preview mismatch;
- audio route changes;
- camera/mic permission changes;
- hardware unavailable/in use by another app;
- thermal/battery impact;
- metadata/privacy leakage;
- server-side transcoding partial failure.

## Notifications / background work

Additional concerns:

- duplicate scheduling;
- device reboot;
- timezone/DST changes;
- notification permission revoked;
- app/account state changed after scheduling;
- stale private content appearing on lock screen;
- foreground vs background behavior;
- deep link target no longer exists;
- job execution delayed by OS;
- server sends after user opts out;
- badge/count consistency;
- notification tap repeated.

## Payments / transactions

Additional concerns:

- idempotency for authorize/capture/refund;
- client timeout after charge;
- webhook delayed/duplicated/out of order;
- payment succeeds but order creation fails;
- order created but payment fails;
- currency/minor unit handling;
- rounding;
- retry after 3DS/authentication;
- refund partial/full semantics;
- cancellation race;
- subscription renewal state;
- reconciliation jobs;
- user-visible receipt vs backend truth;
- support/audit trail.

Money movement should be reconciled from authoritative provider/server records, not UI state.

## AI / LLM

Additional concerns:

- nondeterministic output;
- hallucinated facts;
- prompt injection through user or retrieved content;
- unsafe tool/action execution;
- model/provider timeout;
- retry produces materially different output;
- partial streaming response;
- stale retrieval context;
- citation/source mismatch;
- data sent to model provider;
- sensitive content in prompts/logs;
- model/version change;
- fallback-model behavior;
- confidence communicated poorly;
- user cannot distinguish suggestion from committed action;
- autonomous action without meaningful confirmation;
- evaluation coverage for known failure classes.

For AI actions with side effects, separate **generation** from **authorization/commit**.

## Location / sensors

Additional concerns:

- permission denied/revoked;
- approximate vs precise location;
- sensor unavailable;
- stale reading;
- low accuracy;
- background limitations;
- rapid movement;
- indoor/no-GPS conditions;
- clock errors;
- battery impact;
- spoofed/synthetic readings when trust matters;
- privacy/retention;
- location shown/shared after account change.

## Authentication / account lifecycle

Additional concerns:

- signup interrupted;
- email/phone verification expiry;
- duplicate accounts;
- login from several devices;
- password reset race;
- SSO identity mapping;
- account linking/unlinking;
- logout with in-flight work;
- deletion while background work exists;
- data export/delete semantics;
- account switch and cached private data;
- role/permission changes during session.

## Analytics / experiments

Additional concerns:

- exposure event occurs at correct moment;
- assignment persists as intended;
- user can move between anonymous/authenticated IDs;
- event duplication after retry/navigation;
- offline buffering and resend;
- experiment interaction;
- old/new event schema;
- analytics payload privacy;
- analytics outage must not break product behavior;
- metrics can distinguish failure from abandonment.

## Files and imports

Additional concerns:

- unsupported/mislabeled MIME types;
- extension vs actual content;
- corrupt archives;
- decompression bombs/resource amplification;
- huge file count;
- duplicate filenames;
- filename Unicode/path semantics;
- partial import;
- rollback/retry;
- imported ownership/permissions;
- metadata privacy;
- export round-trip fidelity.

## Search / indexing

Additional concerns:

- indexing delay;
- deleted/private item remains searchable;
- permission changes lag index;
- stale result opens missing object;
- pagination while index changes;
- locale/tokenization differences;
- empty/huge query;
- ranking regression;
- partial reindex;
- source of truth vs index disagreement.

## How to activate packs

Infer packs from the feature. It is normal to combine them.

Example:

```text
Mobile video upload with background retry
→ Mobile + Media + API + Offline/Sync (if queued) + Privacy
```

Select the smallest set that covers the actual architecture.
