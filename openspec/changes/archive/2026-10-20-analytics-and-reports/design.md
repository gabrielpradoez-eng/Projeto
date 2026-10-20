## Context

See `proposal.md` for motivation and `specs/analytics-and-reports/spec.md` for the behavior contract. Xano already exposes `queue_management/stats`, but it is unauthenticated, queue-scoped, and calculates an average from only the latest 20 called tickets. `attendant/dashboard` is authenticated for attendants and returns operational queue state rather than administrative reports. Canonical source fields exist in `senhas` (`created_at`, `chamado_at`, `concluido_at`, `status`) and `atendimentos` (`estabelecimento_id`, `started_at`, `ended_at`). The cancellation status has no event timestamp or cancellation route.

## Goals / Non-Goals

**Goals:**
- Provide period-comparable, establishment-scoped reports with definitions tied to canonical Xano timestamps.
- Keep authorization, aggregation, averages, rates, grouping, and ordering in Xano.
- Have Streamlit submit filters and render one consistent Xano response without deriving business metrics locally.
- Make incomplete samples and empty periods explicit.

**Non-Goals:**
- Reusing or broadening the current unauthenticated `stats` endpoint.
- Introducing a data warehouse, scheduled snapshots, predictive analytics, or customer-level drill-down.
- Adding a cancellation workflow or claiming a historical cancellation date absent from the domain model.

## Decisions

1. **Use authenticated analytics endpoints and backend-provided filter options.** Add an options endpoint that returns only establishments available to a global admin or the bound establishment plus its services/queues for a scoped admin. Add one POST report endpoint accepting an authorized `estabelecimento_id`, UTC `period_start` and `period_end`, and optional `servico_id`/`fila_id`. Require `auth = "usuarios"` and `role == "admin"` on both. If the authenticated admin has an `estabelecimento_id`, enforce it and reject any different ID; a global admin must select an establishment from authorized options. Validate the range (`period_start < period_end`) and validate optional service/queue membership in that same establishment. Do not reuse the public display feed or unauthenticated queue stats endpoint.

2. **Return one response envelope for a consistent filter snapshot.** The endpoint returns `generated_at`, the accepted UTC range and filters, a summary object, chronological daily buckets, service/queue breakdown rows, and a current-status distribution for tickets emitted in the selected cohort. A single request avoids mismatched periods or filters between independently refreshed cards and charts. Xano caps the bucket range/maximum report span and the number of grouping rows to protect query cost; rejected over-limit ranges receive a clear validation error rather than a partial or client-truncated report.

3. **Use event time for event counts and state the cohort semantics separately.** Count emissions by `senhas.created_at`, calls by `senhas.chamado_at`, and completions by `senhas.concluido_at`, each in `[period_start, period_end)`. Calculate wait duration from `chamado_at - created_at` for tickets called in the range, and service duration from `atendimentos.ended_at - started_at` for attendances ended in the range. Ignore records missing either timestamp; return both the mean and sample count, with mean `null` and count `0` when there are no samples. The current status distribution is a separate cohort metric based on tickets emitted in the range and their status when queried; its completion rate is current completed tickets divided by emitted tickets in that cohort. Since no cancellation timestamp exists, do not label cancelled cohort tickets as cancellations that occurred in the requested period.

4. **Keep transformations in Xano, visualization in Streamlit.** Xano applies establishment/service/queue filters, date bucketing, grouping, units conversion, averages, rate calculation and stable ordering. Streamlit loads filter options from the authorized options endpoint, sends the selected filters and renders returned values. It may format durations and labels for readability but must not recalculate, regroup, or reorder report data. Use a form to submit a coherent filter set and bounded caching only for option lists, never report results.

5. **Treat dates as UTC boundaries.** Inputs are ISO-8601 UTC timestamps; the start is inclusive and end exclusive. The UI presents the selected UTC interval clearly, avoiding ambiguous local-day boundaries until establishment timezone support exists.

6. **Return aggregated fields only.** Response rows contain period bucket, service/queue labels, counts, averages, sample counts and cohort distribution. Do not return ticket IDs, customer IDs, user names, contact fields, attendant names or raw event logs.

## Risks / Trade-offs

- [The current `stats` endpoint is unauthenticated and can leak cross-scope counts] → Leave it out of the new UI and use a new role-checked, establishment-scoped endpoint; consider separately deprecating the old endpoint in a later change.
- [Large date ranges or high-cardinality filters can make Xano queries expensive] → Enforce a maximum period and bounded grouping results in Xano; validate indexes/query plans with representative data before production.
- [Averages can be misleading with small or incomplete samples] → Return sample counts, exclude incomplete pairs, and render null distinctly from zero.
- [Cancellation period cannot be inferred from current status] → Report cancellation only as current cohort status until a cancellation event timestamp is introduced.
- [UTC reporting may not align with local business days] → Label UTC boundaries in the UI; add timezone-aware reporting only when establishment timezone data is modeled.

## Migration Plan

1. Implement and validate the authenticated Xano report contract and authorization using representative establishments, services, queues and timestamp edge cases.
2. Add a server-side Streamlit client/configuration for the endpoint and an admin report view that submits the filter form.
3. Add mocked contract and Streamlit tests for date boundaries, scope rejection, no data, incomplete samples, cohort status, series ordering and privacy.
4. Deploy the Xano endpoint before enabling the Streamlit report view; smoke-test a bounded UTC interval in a non-production establishment.
5. Roll back by disabling the new report view/endpoint; existing queue and attendant operations remain unchanged.