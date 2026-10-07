from __future__ import annotations

from typing import Any

import streamlit as st

from streamlit_xano import get_display_feed_client
from tv_sound import notification_tone
from xano_client import XanoClientError


st.set_page_config(
    page_title="FilaSmart | Painel de chamadas",
    page_icon=":material/campaign:",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.header("Painel de chamadas", anchor=False)
st.toggle("Ativar som", key="tv_sound_enabled")


def _validate_snapshot(snapshot: dict[str, Any]) -> None:
    current_call = snapshot.get("current_call")
    if current_call is not None and not isinstance(current_call, dict):
        raise ValueError("Snapshot de chamada inválido.")
    if not isinstance(snapshot.get("history"), list):
        raise ValueError("Histórico de chamadas inválido.")
    if not isinstance(snapshot.get("snapshot_at"), str):
        raise ValueError("Horário do snapshot inválido.")


@st.fragment(run_every="5s")
def render_call_feed() -> None:
    st.session_state.setdefault("tv_last_event_key", None)
    st.session_state.setdefault("tv_has_initial_snapshot", False)
    st.session_state.setdefault("tv_last_snapshot", None)

    snapshot_is_stale = False
    try:
        snapshot = get_display_feed_client().fetch_snapshot()
        _validate_snapshot(snapshot)
    except (XanoClientError, ValueError):
        snapshot = st.session_state.get("tv_last_snapshot")
        if snapshot is None:
            st.error("Painel temporariamente indisponível. Tentando reconectar…")
            return
        snapshot_is_stale = True
        st.warning(
            f"Conexão indisponível. Exibindo snapshot desatualizado de {snapshot['snapshot_at']}."
        )

    is_stale = snapshot_is_stale
    previous_snapshot = st.session_state.get("tv_last_snapshot")
    if not is_stale:
        current_call = snapshot.get("current_call")
        event_key = current_call.get("event_key") if current_call else None
        previous_call = previous_snapshot.get("current_call") if previous_snapshot else None
        previous_key = previous_call.get("event_key") if previous_call else None
        if not st.session_state.tv_has_initial_snapshot:
            st.session_state.tv_has_initial_snapshot = True
        elif event_key and event_key != previous_key:
            st.session_state.tv_last_event_key = event_key
        st.session_state.tv_last_snapshot = snapshot

    current_call = snapshot.get("current_call")
    event_key = current_call.get("event_key") if current_call else None
    should_signal = bool(
        not is_stale
        and event_key
        and event_key == st.session_state.get("tv_last_event_key")
        and previous_snapshot is not None
        and previous_snapshot.get("current_call", {}).get("event_key") != event_key
    )

    if should_signal:
        st.success("Nova chamada")
        if st.session_state.get("tv_sound_enabled"):
            st.audio(
                notification_tone(),
                autoplay=True,
                alt="Alerta sonoro de nova chamada",
                width=220,
            )

    current_column, history_column = st.columns([2.4, 1], gap="large")
    with current_column:
        with st.container(border=True):
            st.subheader("Senha chamada")
            if current_call is None:
                st.info("Aguardando a próxima chamada")
            else:
                st.metric("Senha", str(current_call.get("numero", "—")))
                st.markdown(f"### {current_call.get('destino') or 'Guichê não informado'}")
                st.caption(f"Chamada: {current_call.get('chamado_at', '—')}")

    with history_column:
        st.subheader("Chamadas recentes")
        history = snapshot.get("history", [])[:5]
        if not history:
            st.caption("Nenhuma chamada anterior")
        else:
            for call in history:
                with st.container(border=True):
                    st.markdown(f"**Senha {call.get('numero', '—')}**")
                    st.write(call.get("destino") or "Guichê não informado")
                    st.caption(call.get("chamado_at", "—"))

    st.caption(f"Atualização do Xano: {snapshot['snapshot_at']}")


render_call_feed()