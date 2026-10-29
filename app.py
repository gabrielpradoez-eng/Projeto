"""Ponto de entrada unificado do FilaSmart no Streamlit Community Cloud."""

from __future__ import annotations

import streamlit as st

from backend_queue import AccessDeniedError, QueueBackend, SessionVerificationUnavailable
from portal_session import ROLE_LABELS, ROLE_VIEWS, logout, render_login, verify_current_session
from views.admin_view import render_admin_view
from views.analytics_view import render_analytics_view
from views.client_view import render_client_view
from views.display_view import render_display_view
from views.totem_view import render_tracking_view, render_totem_view
from views.presentation import apply_theme, render_brand, render_intro


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


def main() -> None:
    st.set_page_config(
        page_title="FilaSmart",
        page_icon="⏱️",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={"About": "FilaSmart · versão 2026.10.29.6"},
    )
    _initialize_session()
    apply_theme()
    st.session_state["_portal_managed"] = True

    with st.sidebar:
        render_brand()

    if st.session_state.get("user") is None:
        render_login()
        return
    try:
        user = verify_current_session(
            force=not st.session_state.pop("_portal_just_logged_in", False)
        )
    except AccessDeniedError:
        logout()
        st.rerun()
        return
    except SessionVerificationUnavailable:
        st.warning("Não foi possível verificar sua sessão. Tente novamente para continuar.")
        st.button("Tentar novamente")
        st.button("Sair", on_click=logout)
        return

    allowed_views = ROLE_VIEWS[user["role"]]
    if st.session_state.get("app_view") not in allowed_views:
        st.session_state["app_view"] = allowed_views[0]
    with st.sidebar:
        st.write(user["name"])
        st.caption(ROLE_LABELS[user["role"]])
        st.button("Sair", on_click=logout, icon=":material/logout:", use_container_width=True)
        st.divider()
        st.caption("SEU ESPAÇO DE ATENDIMENTO")
        selected_view = st.radio(
            "Visão",
            options=allowed_views,
            key="app_view",
            label_visibility="collapsed",
        )
        st.divider()
        with st.expander("Como funciona", icon=":material/help_outline:"):
            st.write("1. Escolha o serviço e retire sua senha no Totem.")
            st.write("2. Guarde o comprovante para acompanhar a posição.")
            st.write("3. Confira o guichê no Painel TV quando for chamado.")
        st.caption("FilaSmart · Atendimento com mais clareza")

    if not (selected_view == "Painel TV" and st.session_state.get("tv_presentation_mode")):
        render_intro(selected_view)

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
        render_admin_view(backend, _admin_login_defaults, centralized=True)
    elif selected_view == "Relatórios":
        render_analytics_view(centralized=True)


if __name__ == "__main__":
    main()
