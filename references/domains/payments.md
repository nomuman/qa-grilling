# Payments

Activate for charges, orders, subscriptions, refunds, and other transactions.

Require idempotency for authorize, capture, and refund. Consider client timeout after charge, delayed or reordered webhooks, payment without order, order without payment, currency and minor units, rounding, authentication retries, partial refunds, cancellation races, renewals, reconciliation, receipts versus backend truth, and an auditable support path.

Reconcile money from authoritative provider and server records, not UI state.
