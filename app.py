from __future__ import annotations

import streamlit as st

from backend_queue import QueueBackend
from views.admin_view import render_admin_view
from views.analytics_view import render_analytics_view
from views.client_view import render_client_view
from views.display_view import render_display_view
from views.totem_view import render_tracking_view, render_totem_view


APPLICATION_VIEWS = (
    "Totem",
    "Cliente",
    "Acompanhar senha",
    "Painel TV",
    "Administração",
    "Relatórios",
)


def _admin_login_defaults() -> tuple[str, str]:
    # Bootstrap credentials must never be sent to an unauthenticated browser.
    return "", ""


def _initialize_session() -> None:
    if "backend" not in st.session_state:
        st.session_state.backend = QueueBackend()
    st.session_state.setdefault("user", None)
    st.session_state.setdefault("app_view", "Totem")


def main() -> None:
    st.set_page_config(
        page_title="FilaSmart",
        page_icon="⏱️",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    _initialize_session()
    st.title("FilaSmart")
    st.caption("Atendimento, acompanhamento e gestão em uma única interface.")

    with st.sidebar:
        st.header("Navegação")
        selected_view = st.radio(
            "Visão",
            options=APPLICATION_VIEWS,
            key="app_view",
            label_visibility="collapsed",
        )

    if selected_view == "Totem":
        render_totem_view(centralized=True)
    elif selected_view == "Cliente":
        render_client_view()
    elif selected_view == "Acompanhar senha":
        render_tracking_view(centralized=True)
    elif selected_view == "Painel TV":
        render_display_view()
    elif selected_view == "Administração":
        backend: QueueBackend = st.session_state.backend
        render_admin_view(backend, _admin_login_defaults)
    elif selected_view == "Relatórios":
        render_analytics_view()


if __name__ == "__main__":
    main()
