from __future__ import annotations

import streamlit as st

from streamlit_xano import get_xano_client
from views.issue_error import render_ticket_issue_error
from views.presentation import format_timestamp, render_receipt, render_status_guidance
from portal_session import fragment_access_allowed
from xano_client import (
    QueueUnavailableError,
    TrackingUnavailableError,
    XanoClientError,
)


_CLIENT_SESSION_KEYS = (
    "client_queue_id",
    "client_ticket_reference",
    "client_ticket_number",
    "client_tracking_result",
    "client_tracking_ended",
    "client_ticket_service",
    "client_ticket_queue",
)


def start_new_client_session() -> None:
    for key in _CLIENT_SESSION_KEYS:
        st.session_state.pop(key, None)


def _render_tracking(client) -> None:
    managed_session = bool(st.session_state.get("_portal_managed"))

    @st.fragment(run_every="15s")
    def refresh_tracking() -> None:
        if managed_session and not fragment_access_allowed("Cliente"):
            return
        reference = st.session_state.get("client_ticket_reference")
        if not reference or st.session_state.get("client_tracking_ended"):
            st.info("Este acompanhamento foi encerrado ou não está disponível.")
            return

        try:
            with st.spinner("Atualizando o status da senha..."):
                result = client.track_ticket(reference)
        except TrackingUnavailableError:
            st.session_state["client_tracking_ended"] = True
            st.session_state.pop("client_tracking_result", None)
            st.info("Este acompanhamento foi encerrado ou não está disponível.")
            return
        except XanoClientError:
            result = st.session_state.get("client_tracking_result")
            if result is None:
                st.error("Não foi possível atualizar o status da senha.")
                return
            st.warning(
                "Status atual desconhecido. Exibindo a última atualização confirmada."
            )
            st.caption(f"Última atualização confirmada: {format_timestamp(result['atualizado_at'])}")
        else:
            st.session_state["client_tracking_result"] = result

        st.subheader(f"Sua senha: {st.session_state['client_ticket_number']}")
        render_status_guidance(result["status"])
        st.metric("Status", result["status"])
        if result.get("posicao") is not None:
            st.metric("Posição na fila", result["posicao"])
        if result.get("tempo_estimado_min") is not None:
            st.metric("Espera estimada", f"{result['tempo_estimado_min']} min")
        st.caption(f"Atualizado: {format_timestamp(result['atualizado_at'])} · horário de São Paulo")

    refresh_tracking()


def render_client_view() -> None:
    st.header("Atendimento do cliente")

    if st.button("Iniciar novo atendimento", icon=":material/restart_alt:"):
        start_new_client_session()

    if st.session_state.get("client_ticket_reference"):
        render_receipt(
            st.session_state["client_ticket_number"], st.session_state["client_ticket_reference"],
            st.session_state.get("client_ticket_service", "—"),
            st.session_state.get("client_ticket_queue", "—"), key="client_receipt",
        )
        try:
            client = get_xano_client()
        except XanoClientError:
            st.warning("Não foi possível atualizar agora. Seu comprovante continua disponível.")
            return
        _render_tracking(client)
        return

    try:
        with st.spinner("Carregando filas disponíveis..."):
            client = get_xano_client()
            queues = client.list_queues()
    except XanoClientError as exc:
        st.error(str(exc))
        return

    if not queues:
        start_new_client_session()
        st.info("Não há filas disponíveis para emissão neste momento.")
        return

    queue_by_id = {item["fila_id"]: item for item in queues}
    if st.session_state.get("client_queue_id") not in queue_by_id:
        st.session_state["client_queue_id"] = next(iter(queue_by_id))

    if not st.session_state.get("client_ticket_reference"):
        selected_queue_id = st.selectbox(
            "Serviço",
            options=list(queue_by_id),
            format_func=lambda queue_id: (
                f"{queue_by_id[queue_id]['servico_nome']} · "
                f"{queue_by_id[queue_id]['fila_nome']}"
            ),
            key="client_queue_id",
        )

        if st.button(
            "Emitir senha", type="primary", icon=":material/confirmation_number:"
        ):
            try:
                with st.spinner("Solicitando a emissão da senha..."):
                    issued = client.issue_ticket(selected_queue_id)
            except QueueUnavailableError as exc:
                render_ticket_issue_error(
                    exc,
                    fallback_message="A fila selecionada não está disponível.",
                )
                return
            except XanoClientError as exc:
                render_ticket_issue_error(exc)
                return

            number = issued.get("numero")
            reference = issued.get("referencia_rastreamento")
            if number is None or not isinstance(reference, str) or not reference:
                st.error("O Xano retornou uma confirmação de emissão inválida.")
                return

            st.session_state["client_ticket_number"] = number
            st.session_state["client_ticket_reference"] = reference
            st.session_state["client_ticket_service"] = queue_by_id[selected_queue_id]["servico_nome"]
            st.session_state["client_ticket_queue"] = queue_by_id[selected_queue_id]["fila_nome"]
            st.session_state.pop("client_tracking_result", None)
            st.session_state.pop("client_tracking_ended", None)
            st.success(f"Senha emitida: {number}")

    if st.session_state.get("client_ticket_reference"):
        render_receipt(
            st.session_state["client_ticket_number"], st.session_state["client_ticket_reference"],
            st.session_state.get("client_ticket_service", "—"),
            st.session_state.get("client_ticket_queue", "—"), key="client_receipt",
        )
        _render_tracking(client)
