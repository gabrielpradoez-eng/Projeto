import streamlit as st

from streamlit_xano import get_xano_client
from xano_client import QueueUnavailableError, XanoClientError


def start_new_session() -> None:
    for key in (
        "ticket_reference",
        "ticket_number",
        "tracking_result",
        "tracking_active",
        "tracking_ended",
        "tracking_input",
    ):
        st.session_state.pop(key, None)


st.header("Retire sua senha")

if st.button("Iniciar novo atendimento", icon=":material/restart_alt:"):
    start_new_session()
    st.rerun()

try:
    client = get_xano_client()
    queues = client.list_queues()
except XanoClientError as exc:
    st.error(str(exc))
    st.stop()

if not queues:
    st.info("Não há filas disponíveis para emissão neste momento.")
    st.stop()

queue_by_id = {item["fila_id"]: item for item in queues}
selected_queue_id = st.selectbox(
    "Serviço",
    options=list(queue_by_id),
    format_func=lambda queue_id: (
        f"{queue_by_id[queue_id]['servico_nome']} · "
        f"{queue_by_id[queue_id]['fila_nome']}"
    ),
)

if st.button("Emitir senha", type="primary", icon=":material/confirmation_number:"):
    try:
        issued = client.issue_ticket(selected_queue_id)
    except QueueUnavailableError:
        st.warning("A fila selecionada deixou de estar disponível. Selecione outra.")
    except XanoClientError as exc:
        st.error(str(exc))
    else:
        st.session_state.ticket_number = issued["numero"]
        st.session_state.ticket_reference = issued["referencia_rastreamento"]
        st.session_state.tracking_active = True
        st.session_state.tracking_ended = False
        st.session_state.tracking_result = None
        st.rerun()

if st.session_state.get("ticket_reference"):
    st.divider()
    st.subheader(f"Sua senha: {st.session_state.ticket_number}")
    st.write("Referência de acompanhamento")
    st.code(st.session_state.ticket_reference, language=None)
    st.page_link(
        "app_pages/tracking.py",
        label="Acompanhar minha senha",
        icon=":material/pending_actions:",
    )