## Context

See `proposal.md` for motivation and `specs/tv-display-panel/spec.md` plus `specs/core-queue-ops/spec.md` for behavior contracts. The repository has a login-protected `call_next` operation that changes `senhas.status` and creates an `atendimentos` record. `attendant/dashboard` is also authenticated and returns operational fields unsuitable for public display. The existing Streamlit/Xano integration from Change 2 provides a pattern for server-side REST access, while no TV display entry point or public call-feed endpoint currently exists.

## Goals / Non-Goals

**Goals:**
- Deliver a dedicated, read-only Streamlit display entry point for a TV/browser, with clear visual hierarchy at large resolutions and graceful smaller-screen layout.
- Keep call selection, state, destination, and history ordering authoritative in Xano.
- Return a minimal, scope-authorized public snapshot without customer or staff identity data.
- Poll efficiently and distinguish the last confirmed snapshot from connectivity state.
- Avoid repeated alerts for a single call and remain useful when browser audio is blocked or disabled.

**Non-Goals:**
- Changing attendant call controls or queue priority rules.
- Adding push/WebSocket delivery in this change; polling is the selected transport.
- Admin editing of display settings, audio-device provisioning, or multiple custom themes.

## Decisions

1. **Use a dedicated Streamlit display entry point.** Add a display-specific entry point rather than exposing or adapting the authenticated attendant dashboard. This keeps public display code read-only and independent of the Totem/customer app. Use a full-width page configuration and responsive Streamlit layout; avoid coupling display startup to user login.

2. **Add a purpose-built Xano snapshot contract.** A display registration stores a hash of a high-entropy bearer credential and its establishment scope; the endpoint accepts the credential in a POST body, resolves its scope server-side, and denies inactive or invalid registrations. It returns a single snapshot containing a stable public call-event key, ticket number, destination label, call timestamp, recent call list already sorted newest-first by Xano, and a server-generated snapshot timestamp. Xano orders records by its internal attendance ID to break ties, but never returns that ID. Return empty current-call/history values explicitly. Never reuse the attendant dashboard response or return customer identity, attendant identity, internal row IDs, credential hashes, or unrelated queue data.

3. **Make publication derive from the same canonical call records.** Extend the attendant record with an optional public destination label (guichê/sala), then snapshot the ticket number, establishment scope, destination label, and a generated public event key into the attendance record within the existing Xano call transaction. The feed reads these snapshots, so later attendant edits cannot rewrite historical call cards. Xano owns current-call selection and ordering; Streamlit only renders the provided snapshot. A missing destination is rendered as “Guichê não informado” rather than exposing attendant identifiers.

4. **Poll in an isolated Streamlit fragment.** Poll at a configurable conservative interval (initial default: 5 seconds) inside `st.fragment(run_every=...)`, with bounded HTTP timeout and no cache for current-call snapshots. A valid response replaces the last confirmed snapshot. On request failure, retain the prior snapshot only as visibly stale and show connection status; on initial failure, render an unavailable state. Recover automatically on the next valid response.

5. **Deduplicate visual and audio alerts by backend event identifier.** Store the last observed call/event key in per-session state. Signal only when the backend reports a different, valid current-call key; repeated polling of the same event updates the display without replay. On the first successful poll, render current state without treating an already-active call as newly observed. For subsequent calls, show a brief visual emphasis and render a short generated WAV tone with native `st.audio(autoplay=True)` only when an explicit Streamlit “Ativar som” toggle is enabled. The browser still decides whether autoplay is permitted; visual signaling remains sufficient when disabled or blocked.

6. **Support real and mocked Xano contracts through one adapter boundary.** A server-side API client reads display endpoint and credential from Streamlit secrets. Tests inject a fake client returning snapshots and transport errors through that boundary, while live deployment points the same adapter at the Xano endpoint. No mock data is bundled as a production fallback; missing configuration is presented as an unavailable feed rather than fabricated calls.

## Risks / Trade-offs

- [Browser autoplay policy blocks audio] → Require an explicit sound activation control and make visual emphasis the reliable fallback.
- [A public feed leaks operational or personal information] → Use a dedicated response allowlist, display-scoped credentials, and tests asserting prohibited fields are absent.
- [Polling creates unnecessary backend load] → Keep a 5-second initial interval configurable per deployment, return a bounded recent history, and use a single fragment request per display session.
- [Event identity or current-call semantics differ from the attendant workflow] → Derive the feed from canonical Xano attendance/ticket records and verify behavior across call, completion, and next-call transitions before deployment.
- [Streamlit fragments do not provide frame-perfect real-time delivery] → Document polling latency as expected behavior; push transport remains a future option if operational requirements demand it.

## Migration Plan

1. Define and implement Xano display credential/scope, attendant destination label, canonical call-event snapshots, and minimal feed response.
2. Validate output ordering, payload privacy, and transitions against representative Xano data before deploying a public URL.
3. Add the Streamlit display entry point, API adapter, large-screen presentation, polling and sound activation behavior.
4. Add mocked contract and Streamlit tests for initial/empty state, changed and unchanged call identifiers, network failure, recovery, audio-disabled mode, and scope rejection.
5. Configure display secrets, deploy Xano support first, then launch the Streamlit display on the TV browser and verify with a non-production establishment.
6. Roll back by withdrawing the display entry point or revoking its Xano display credential; attendant calling remains unchanged.

