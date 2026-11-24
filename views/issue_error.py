from __future__ import annotations

import streamlit as st

from xano_client import QueueUnavailableError, XanoClientError


def render_ticket_issue_error(
    error: XanoClientError, *, fallback_message: str | None = None
) -> None:
    status_code = getattr(error, "status_code", None)
    api_message = getattr(error, "api_message", None)

    if status_code is None:
        message = api_message or fallback_message or str(error)
        if isinstance(error, QueueUnavailableError):
            st.warning(message)
        else:
            st.error(message)
        return

    message = api_message or fallback_message or (
        "A fila selecionada não está disponível para emissão."
        if isinstance(error, QueueUnavailableError)
        else "Não foi possível confirmar a emissão. Confira o atendimento antes de solicitar outra senha."
    )
    if isinstance(error, QueueUnavailableError):
        st.warning(message)
    else:
        st.error(message)
