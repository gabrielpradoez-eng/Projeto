import streamlit as st

from streamlit_xano import get_xano_client
from xano_client import (
    TrackingUnavailableError,
    XanoClientError,
)


st.header("Acompanhe sua senha")

if st.session_state.get("tracking_ended"):
    st.info("Este acompanhamento foi encerrado ou a referência não está disponível.")
    if st.button("Iniciar novo atendimento", icon=":material/restart_alt:"):
        for key in (
            "ticket_reference",
            "ticket_number",
            "tracking_result",
            "tracking_active",
            "tracking_ended",
            "tracking_input",
        ):
            st.session_state.pop(key, None)
        st.switch_page("app_pages/totem.py")
    st.stop()

if not st.session_state.get("tracking_active"):
    with st.form("tracking_reference_form"):
        reference = st.text_input(
            "Referência de acompanhamento",
            type="password",
            autocomplete="off",
        )
        submitted = st.form_submit_button(
            "Acompanhar", type="primary", icon=":material/search:"
        )
    if submitted:
        if reference.strip():
            st.session_state.ticket_reference = reference.strip()
            st.session_state.tracking_active = True
            st.session_state.tracking_ended = False
            st.session_state.tracking_result = None
            st.rerun()
        st.warning("Informe a referência de acompanhamento.")
    st.stop()


@st.fragment(run_every="15s")
def render_tracking() -> None:
    if st.session_state.get("tracking_ended"):
        st.info("Este acompanhamento foi encerrado ou a referência não está disponível.")
        return

    st.button("Atualizar agora", icon=":material/refresh:")
    try:
        client = get_xano_client()
        result = client.track_ticket(st.session_state.ticket_reference)
    except TrackingUnavailableError:
        st.session_state.tracking_ended = True
        st.session_state.tracking_active = False
        st.session_state.tracking_result = None
        st.info("Este acompanhamento foi encerrado ou a referência não está disponível.")
        return
    except XanoClientError:
        previous = st.session_state.get("tracking_result")
        if previous is None:
            st.warning("Não foi possível consultar o estado atual da senha.")
            return
        st.warning(
            "Estado atual desconhecido. Abaixo está a última atualização confirmada."
        )
        result = previous
        st.caption(f"Última atualização confirmada: {result['atualizado_at']}")

    st.session_state.tracking_result = result
    st.subheader(f"Senha {result['numero']}")
    st.write(f"{result['servico']} · {result['fila']}")
    st.metric("Status", result["status"])
    if result.get("posicao") is not None:
        st.metric("Posição na fila", result["posicao"])
        estimate = result.get("tempo_estimado_min")
        st.metric("Espera estimada", f"{estimate} min" if estimate is not None else "—")
    st.caption(f"Atualizado: {result['atualizado_at']}")


render_tracking()

if st.button("Encerrar e iniciar novo atendimento", icon=":material/close:"):
    for key in (
        "ticket_reference",
        "ticket_number",
        "tracking_result",
        "tracking_active",
        "tracking_ended",
        "tracking_input",
    ):
        st.session_state.pop(key, None)
    st.switch_page("app_pages/totem.py")