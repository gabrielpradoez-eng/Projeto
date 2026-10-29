from __future__ import annotations

import streamlit as st

from streamlit_xano import get_xano_client
from views.issue_error import render_ticket_issue_error
from views.presentation import format_timestamp, render_receipt, render_status_guidance
from xano_client import (
    QueueUnavailableError,
    TrackingUnavailableError,
    XanoClientError,
)


_CUSTOMER_SESSION_KEYS = (
    "ticket_reference",
    "ticket_number",
    "tracking_result",
    "tracking_active",
    "tracking_ended",
    "tracking_input",
    "ticket_service",
    "ticket_queue",
)


def start_new_session() -> None:
    for key in _CUSTOMER_SESSION_KEYS:
        st.session_state.pop(key, None)


def _return_to_totem(centralized: bool) -> None:
    start_new_session()
    if centralized:
        st.session_state["app_view"] = "Totem"
        return
    st.switch_page("app_pages/totem.py")


def _open_tracking() -> None:
    st.session_state["app_view"] = "Acompanhar senha"


def _render_issued_ticket(*, centralized: bool) -> None:
    st.divider()
    st.subheader(f"Sua senha: {st.session_state.ticket_number}")
    st.caption("Senha já emitida nesta sessão. Para outra pessoa, use Iniciar novo atendimento.")
    st.caption("Iniciar novo atendimento limpa este aparelho; não cancela a senha emitida.")
    render_receipt(
        st.session_state.ticket_number, st.session_state.ticket_reference,
        st.session_state.get("ticket_service", "—"),
        st.session_state.get("ticket_queue", "—"), key="totem_receipt",
    )
    st.write("Referência de acompanhamento")
    st.code(st.session_state.ticket_reference, language=None)
    if centralized:
        st.button(
            "Acompanhar minha senha", icon=":material/pending_actions:",
            on_click=_open_tracking,
        )
    else:
        st.page_link(
            "app_pages/tracking.py", label="Acompanhar minha senha",
            icon=":material/pending_actions:",
        )


def render_totem_view(*, centralized: bool = False) -> None:
    if not st.session_state.get("ticket_reference"):
        st.markdown(
            '<div class="fs-steps"><div class="fs-step"><b>1</b><strong>Escolha o serviço</strong>'
            '<p>Selecione o atendimento de que você precisa.</p></div>'
            '<div class="fs-step"><b>2</b><strong>Retire sua senha</strong>'
            '<p>Baixe e guarde seu comprovante.</p></div>'
            '<div class="fs-step"><b>3</b><strong>Acompanhe sua vez</strong>'
            '<p>Consulte o andamento e aguarde a chamada.</p></div></div>',
            unsafe_allow_html=True,
        )
    st.header("Retire sua senha")

    if st.button("Iniciar novo atendimento", icon=":material/restart_alt:"):
        start_new_session()
        st.rerun()

    if st.session_state.get("ticket_reference"):
        st.button("Emitir senha", type="primary", icon=":material/confirmation_number:", disabled=True)
        _render_issued_ticket(centralized=centralized)
        return

    try:
        with st.spinner("Carregando filas disponíveis..."):
            client = get_xano_client()
            queues = client.list_queues()
    except XanoClientError as exc:
        st.error(str(exc))
        return

    if not queues:
        st.info("Não há filas disponíveis para emissão neste momento.")
        return

    queue_by_id = {item["fila_id"]: item for item in queues}
    if st.session_state.get("totem_queue_id") not in queue_by_id:
        st.session_state["totem_queue_id"] = next(iter(queue_by_id))
    selected_queue_id = st.selectbox(
        "Serviço",
        options=list(queue_by_id),
        format_func=lambda queue_id: (
            f"{queue_by_id[queue_id]['servico_nome']} · "
            f"{queue_by_id[queue_id]['fila_nome']}"
        ),
        key="totem_queue_id",
    )

    if st.button(
        "Emitir senha", type="primary", icon=":material/confirmation_number:",
        disabled=bool(st.session_state.get("ticket_reference")),
    ) and not st.session_state.get("ticket_reference"):
        try:
            with st.spinner("Solicitando a emissão da senha..."):
                issued = client.issue_ticket(selected_queue_id)
        except QueueUnavailableError as exc:
            render_ticket_issue_error(
                exc,
                fallback_message=(
                    "A fila selecionada deixou de estar disponível. Selecione outra."
                ),
            )
        except XanoClientError as exc:
            render_ticket_issue_error(exc)
        else:
            st.session_state.ticket_number = issued["numero"]
            st.session_state.ticket_reference = issued["referencia_rastreamento"]
            st.session_state.ticket_service = queue_by_id[selected_queue_id]["servico_nome"]
            st.session_state.ticket_queue = queue_by_id[selected_queue_id]["fila_nome"]
            st.session_state.tracking_active = True
            st.session_state.tracking_ended = False
            st.session_state.tracking_result = None
            st.success(f"Senha confirmada: {issued['numero']}")

    if st.session_state.get("ticket_reference"):
        _render_issued_ticket(centralized=centralized)


def render_tracking_view(*, centralized: bool = False) -> None:
    st.header("Acompanhe sua senha")

    if st.session_state.get("tracking_ended"):
        st.info("Este acompanhamento foi encerrado ou a referência não está disponível.")
        st.button(
            "Iniciar novo atendimento", icon=":material/restart_alt:",
            on_click=_return_to_totem, args=(centralized,),
        )
        return

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
        return

    @st.fragment(run_every="15s")
    def render_tracking() -> None:
        reference = st.session_state.get("ticket_reference")
        if not st.session_state.get("tracking_active") or not reference:
            return

        if st.session_state.get("tracking_ended"):
            st.info(
                "Este acompanhamento foi encerrado ou a referência não está disponível."
            )
            return

        st.button("Atualizar agora", icon=":material/refresh:")
        try:
            with st.spinner("Atualizando o acompanhamento..."):
                client = get_xano_client()
                result = client.track_ticket(reference)
        except TrackingUnavailableError:
            st.session_state.tracking_ended = True
            st.session_state.tracking_active = False
            st.session_state.tracking_result = None
            st.info(
                "Este acompanhamento foi encerrado ou a referência não está disponível."
            )
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
            st.caption(f"Última atualização confirmada: {format_timestamp(result['atualizado_at'])}")

        st.session_state.tracking_result = result
        st.subheader(f"Senha {result['numero']}")
        st.write(f"{result['servico']} · {result['fila']}")
        render_status_guidance(result["status"])
        status_col, position_col, wait_col = st.columns(3)
        with status_col:
            st.metric("Status", result["status"])
        if result.get("posicao") is not None:
            with position_col:
                st.metric("Posição na fila", result["posicao"])
            estimate = result.get("tempo_estimado_min")
            with wait_col:
                st.metric(
                    "Espera estimada",
                    f"{estimate} min" if estimate is not None else "—",
                )
        st.caption(f"Atualizado: {format_timestamp(result['atualizado_at'])} · horário de São Paulo")
        st.caption("Atualização automática a cada 15 segundos. A estimativa pode variar.")

    render_tracking()

    st.button(
        "Encerrar e iniciar novo atendimento", icon=":material/close:",
        on_click=_return_to_totem, args=(centralized,),
    )
