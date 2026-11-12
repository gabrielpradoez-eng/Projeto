"""Chat privado durante um atendimento em andamento."""
from __future__ import annotations

import streamlit as st

from backend_queue import AccessDeniedError, InvalidQueueStateError
from portal_session import fragment_access_allowed


_VALIDATED_QUEUE_API = "https://x8ki-letl-twmt.n7.xano.io/api:queue-management"


def service_chat_enabled() -> bool:
    try:
        settings = st.secrets.get("xano", {})
    except FileNotFoundError:
        return False
    if "service_chat_enabled" in settings:
        return settings["service_chat_enabled"] is True
    base_url = settings.get("base_url", "")
    return isinstance(base_url, str) and base_url.rstrip("/") == _VALIDATED_QUEUE_API


def render_service_chat(backend, user: dict, *, ticket_id: int = 0) -> None:
    customer = user["role"] == "user"
    view = "Cliente" if customer else "Administração"
    managed = bool(st.session_state.get("_portal_managed"))

    @st.fragment(run_every="8s")
    def chat() -> None:
        if managed and not fragment_access_allowed(view):
            return
        st.subheader("Chat do atendimento")
        try:
            state = backend.get_service_chat(ticket_id, token=user["authToken"])
        except AccessDeniedError:
            st.info("Esta conversa não está disponível para sua conta.")
            return
        except InvalidQueueStateError:
            st.warning("Não foi possível carregar a conversa. O painel tentará atualizar em instantes.")
            return

        active = state["atendimento"]
        if active is None:
            st.caption("O chat abre quando a sua senha for chamada.")
            return
        st.caption(f"Senha {active['numero']} · {active.get('guiche') or 'Atendimento em andamento'}")
        if not state["mensagens"]:
            st.info("Ainda não há mensagens. Escreva abaixo para iniciar a conversa.")
        else:
            with st.container(height=300, border=True):
                for message in reversed(state["mensagens"]):
                    mine = message["remetente_id"] == user["id"]
                    with st.chat_message("user" if mine else "assistant"):
                        st.caption("Você" if mine else ("Atendente" if customer else "Cliente"))
                        # st.text renders literal content, including Markdown and HTML.
                        st.text(message["mensagem"])

        submitted = st.chat_input("Escreva uma mensagem", max_chars=500,
                                  key=f"service_chat_{active['senha_id']}")
        if submitted and submitted.strip():
            try:
                backend.send_service_message(active["senha_id"], submitted, token=user["authToken"])
            except (AccessDeniedError, InvalidQueueStateError):
                st.error("Não foi possível confirmar o envio. Confira a conversa antes de tentar novamente.")
            else:
                st.rerun()

    chat()
