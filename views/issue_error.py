from __future__ import annotations

import streamlit as st

from xano_client import QueueUnavailableError, XanoClientError


def render_ticket_issue_error(
    error: XanoClientError, *, fallback_message: str | None = None
) -> None:
    status_code = getattr(error, "status_code", None)
    api_code = getattr(error, "api_code", None)
    api_message = getattr(error, "api_message", None)
    api_body = getattr(error, "api_body", None)

    if status_code is None:
        message = api_message or fallback_message or str(error)
        if isinstance(error, QueueUnavailableError):
            st.warning(message)
        else:
            st.error(message)
        return

    prefix = (
        "Xano recusou a emissão"
        if isinstance(error, QueueUnavailableError)
        else "Falha na emissão no Xano"
    )
    details = f"{prefix} (HTTP {status_code})"
    if api_code:
        details += f" · Código: {api_code}"
    if api_message:
        details += f": {api_message}"
    st.error(details)

    if api_body:
        language = "json" if api_body.lstrip().startswith(("{", "[")) else "text"
        st.code(api_body, language=language)
    else:
        st.caption("O Xano não forneceu detalhes adicionais no corpo da resposta.")
