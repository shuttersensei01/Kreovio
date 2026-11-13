# Architecture

Kreovio is a Python modular monolith. Modules own their business services and communicate through those services; HTTP, Celery, MCP and AI are thin entry points.

Tenant-owned MongoDB documents carry `workspace_id`. Repositories receive a workspace context and scope every operation. Platform data is explicitly separate. Money is integer minor units plus ISO currency; times are UTC and services receive a clock.

Mutations of commercial, booking, approval and permission data produce audit records. Price packages are versioned and quotations retain immutable snapshots. Explicit state-machine tables govern inquiry, quotation, booking and follow-up transitions.

MongoDB runs as a replica set for transactions. Booking confirmation rechecks availability within a transaction. Human-only operations are excluded from AI tooling. Client messages remain untrusted data, and encrypted secrets and redacted structured logs protect sensitive data.

The initial collections are platform (`users`, `workspaces`, `workspace_members`) and tenant-owned CRM, catalogue, quote, booking, follow-up, analytics, audit and integration collections defined in the build brief. Their indexes begin with `workspace_id`; startup and tests create indexes idempotently.

