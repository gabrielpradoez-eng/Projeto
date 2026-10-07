## Context

See `proposal.md` for motivation and `specs/totem-customer-tracking/spec.md` for the behavior contract. The existing `app.py` is a single-page Streamlit prototype backed by `QueueBackend` in memory. Xano already has an authenticated `join` endpoint and an aggregate `stats` endpoint, but no public Totem identity, eligible-queue listing, or individual ticket-tracking contract. The installed Streamlit version is 1.65.0.

## Goals / Non-Goals

**Goals:**
- Add a public Streamlit experience for ticket issuance and customer tracking without replacing the existing operational prototype.
- Keep eligibility, authorization, ticket creation, status transitions, queue position, and wait estimate authoritative in Xano.
- Keep kiosk and tracking credentials out of page code, logs, URLs, and public responses; prevent one kiosk customer from seeing a previous customer's tracking session.
- Keep the UI responsive while tracking refreshes periodically.

**Non-Goals:**
- Migrating the existing attendant/admin prototype or its in-memory test backend to Xano as part of this change.
- Real-time push delivery, mobile-native clients, public call panels, printing hardware, or a new queue-priority policy.

## Decisions

1. **Use a dedicated public Streamlit entry point with native multipage navigation.** Add a public app entry point and `app_pages/` pages for the Totem and customer tracking; keep the existing `app.py` operational prototype intact. Streamlit 1.65 supports `st.navigation`/`st.Page`, which avoids mixing the public kiosk flow with the existing login-gated admin/attendant screen. A unified refactor of `app.py` was considered but would unnecessarily broaden this change and risk the already-tested operational flow.

2. **Add a small Xano API client as an integration adapter, not a domain backend.** The adapter sends requests and maps transport/API errors only. Store the Xano base URL and kiosk service credential in server-side Streamlit secrets; do not send the service credential to browser widgets or expose it in error messages. Use bounded request timeouts and do not cache customer-specific tracking responses.

3. **Extend Xano with explicit kiosk and tracking contracts.** Provide an authorized list of eligible services/queues, an issuance operation that revalidates eligibility and atomically creates the ticket, and a lookup that accepts an opaque tracking reference. The existing `join` endpoint authenticates a user and must not be made anonymously callable by simply removing auth. Add a restricted `totem` user role linked to one establishment and authorize Totem endpoints only for that role and scope. Persist a hash of a cryptographically random tracking reference in a separate access record linked to the ticket, with revocation/expiry support; never expose internal ticket or user IDs as the bearer reference.

4. **Calculate all tracking values and enforce reference lifetime in Xano.** For a waiting ticket, Xano calculates position using the queue's canonical ordering among tickets still waiting and returns the estimate only when it can derive one from backend data. The reference is denied as soon as the ticket reaches `concluido` and no later than 24 hours after issuance. The UI displays returned values; it does not count tickets, estimate time, or infer state transitions. The current aggregate `stats` response is not sufficient for this individual lookup.

5. **Refresh only the tracking region.** Use a Streamlit fragment with a conservative 15-second interval for tracking requests, plus an explicit refresh control. Keep the opaque reference in per-session state, not in query parameters or server cache. Starting a new Totem interaction clears prior ticket/reference/result state. On transport failure, show the last confirmed result as stale and label current status unknown rather than replacing it with a guessed value.

6. **Keep the public response minimal.** The tracking API returns only ticket display number, service/queue label, status, nullable position and nullable estimate, and the response timestamp. It does not return customer identity, contact details, attendant identity, or other tickets. Invalid and unauthorized references share a generic response.

## Risks / Trade-offs

- [A kiosk credential could be extracted if it is embedded in browser-visible code or assets] → Keep calls server-side in Streamlit and load the credential from deployment secrets; limit its Xano permissions to listing eligible queues and issuing tickets.
- [A bearer tracking reference can be shared or photographed] → Generate it with high entropy, store only its hash, scope it to one ticket, return minimal data, and support expiration/revocation.
- [A completed or old ticket reference may remain usable] → Xano denies it as soon as the ticket status is `concluido` and denies all references after 24 hours from issuance, whichever happens first.
- [The current queue-number selection in Xano may not be concurrency-safe] → Verify atomic issuance under concurrent kiosk requests and enforce uniqueness/serialization in Xano before deployment; do not compensate in Streamlit.
- [Polling can increase Xano request volume] → Poll only while a customer tracking screen is active, use a 15-second interval, and stop refreshing when status is terminal or the page is left.
- [The repository prototype does not yet call Xano from Streamlit] → Keep this change's adapter contract explicit and test against mocked HTTP responses; treat live Xano credential/configuration as deployment prerequisites.

## Migration Plan

1. Add the Xano kiosk listing, issuance, tracking access record, and tracking lookup with scoped authorization; verify the response contracts and concurrent issuance.
2. Add the server-side Streamlit API adapter and the dedicated public entry point/pages, configured through deployment secrets.
3. Validate API error handling, reference isolation, session reset, and periodic refresh using mocked backend responses and Streamlit `AppTest` where practical.
4. Deploy Xano support before exposing the public Streamlit app, then configure secrets and smoke-test issuance and tracking in a non-production queue.
5. Roll back by removing the public app entry point from deployment; retain issued ticket records and disable/revoke kiosk credentials or tracking references in Xano as needed. The existing `app.py` remains available throughout.
