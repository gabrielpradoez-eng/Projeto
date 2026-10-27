from __future__ import annotations

from collections.abc import Callable

import streamlit as st

from backend_queue import (
    AccessDeniedError,
    InvalidQueueStateError,
    QueueBackend,
)


def render_admin_view(
    backend: QueueBackend,
    admin_login_defaults: Callable[[], tuple[str, str]],
) -> None:
    st.header("Núcleo operacional")

    if "user" not in st.session_state:
        st.session_state.user = None

    user = st.session_state.user
    with st.sidebar:
        st.header("Autenticação")
        if user is None:
            admin_email, admin_password = admin_login_defaults()
            email = st.text_input("E-mail", value=admin_email)
            password = st.text_input("Senha", type="password", value=admin_password)
            if st.button("Entrar"):
                try:
                    with st.spinner("Validando credenciais..."):
                        user_data = backend.authenticate(email, password)
                    st.session_state.user = user_data
                    st.session_state.authToken = user_data["authToken"]
                    st.session_state.user_id = user_data["user_id"]
                    st.rerun()
                except AccessDeniedError as exc:
                    st.error(str(exc))
        else:
            st.write(f"Usuário: {user.get('name', 'N/A')}")
            st.write(f"Perfil: {user.get('role', 'N/A')}")
            if st.button("Sair"):
                st.session_state.user = None
                st.session_state.pop("authToken", None)
                st.session_state.pop("user_id", None)
                st.rerun()

    if user is None:
        st.info("Faça login para acessar o núcleo da operação da fila.")
        return

    if user.get("role") not in {"admin", "attendant", "user"}:
        st.error("Perfil inválido.")
        return

    if user.get("role") == "admin":
        st.info("Consulte os indicadores na visão Relatórios. Os cadastros devem ser feitos no workspace Xano.")
        return
    if user.get("role") != "attendant":
        st.info("Utilize a visão Cliente para emitir e acompanhar sua senha.")
        return

    st.subheader("Painel do atendente")
    st.button("Atualizar filas")
    try:
        rows = backend.get_attendant_dashboard(token=user["authToken"])
    except (AccessDeniedError, InvalidQueueStateError) as exc:
        st.error(str(exc))
        return
    if not rows:
        st.info("Nenhuma fila disponível para este atendente.")
        return
    queues = {row["id"]: row for row in rows}
    queue_id = st.selectbox(
        "Fila sob sua responsabilidade", options=list(queues),
        format_func=lambda value: queues[value]["nome"], key="attendant_queue_id",
    )
    queue = queues[queue_id]
    st.metric("Senhas aguardando", queue["total_aguardando"])
    current = queue.get("em_atendimento")
    if current:
        st.write(f"Senha em atendimento: {current.get('numero', current.get('id'))}")
    else:
        st.info("Nenhuma senha em atendimento nesta fila.")

    if st.button("Chamar próxima senha", disabled=current is not None):
        try:
            backend.call_next_token(queue_id, user["id"], token=user["authToken"])
            st.rerun()
        except (AccessDeniedError, InvalidQueueStateError) as exc:
            st.error(str(exc))
    if st.button("Finalizar atendimento atual", disabled=not current):
        try:
            backend.complete_service(current["id"], user["id"], token=user["authToken"])
            st.rerun()
        except (AccessDeniedError, InvalidQueueStateError) as exc:
            st.error(str(exc))
    st.caption("Filas e estado do atendimento consultados no Xano.")
