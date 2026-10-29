from __future__ import annotations

import time

import streamlit as st

from backend_queue import AccessDeniedError, SessionVerificationUnavailable


ROLE_VIEWS = {
    "user": ("Cliente", "Acompanhar senha", "Painel TV"),
    "attendant": ("Administração", "Painel TV"),
    "admin": ("Administração", "Relatórios", "Totem", "Cliente", "Acompanhar senha", "Painel TV"),
}
ROLE_LABELS = {"user": "Cliente", "attendant": "Atendente", "admin": "Administrador"}


def logout() -> None:
    st.session_state.clear()


def verify_current_session(*, force: bool = False) -> dict:
    user = st.session_state.get("user")
    token = st.session_state.get("authToken")
    if not isinstance(user, dict) or not token or user.get("role") not in ROLE_VIEWS:
        raise AccessDeniedError("Entre para continuar.")
    now = time.monotonic()
    if force or now - st.session_state.get("_portal_verified_at", 0) >= 60:
        verified = st.session_state.backend.verify_session(token, user.get("id"))
        if verified.get("role") not in ROLE_VIEWS or verified.get("authToken") != token:
            raise AccessDeniedError("Perfil sem acesso ao aplicativo.")
        if verified["role"] != user["role"]:
            for key in ("analytics_auth_token", "analytics_report", "tv_last_snapshot", "tv_last_event_key"):
                st.session_state.pop(key, None)
        st.session_state.user = verified
        st.session_state["_portal_verified_at"] = now
        user = verified
    return user


def fragment_access_allowed(view: str) -> bool:
    try:
        user = verify_current_session()
    except AccessDeniedError:
        logout()
        st.rerun()
        return False
    except SessionVerificationUnavailable:
        st.warning("Não foi possível verificar a sessão. A atualização está pausada; tente novamente.")
        return False
    if view not in ROLE_VIEWS[user["role"]]:
        st.rerun()
        return False
    return True


def submit_login() -> None:
    email = str(st.session_state.get("portal_email", "")).strip()
    password = st.session_state.pop("portal_password", "")
    backend = st.session_state.backend
    if not email or not password:
        st.session_state["portal_login_error"] = "Informe e-mail e senha para continuar."
        return
    try:
        claimed = backend.authenticate(email, password)
        verified = backend.verify_session(claimed["authToken"], claimed["id"])
        if verified.get("role") not in ROLE_VIEWS:
            raise AccessDeniedError("Perfil sem acesso.")
    except (AccessDeniedError, SessionVerificationUnavailable):
        st.session_state["portal_login_error"] = "Não foi possível entrar. Verifique suas credenciais e tente novamente."
        return
    # A new identity never inherits the previous customer's ticket or report.
    st.session_state.clear()
    st.session_state.backend = backend
    st.session_state.user = verified
    st.session_state.authToken = verified["authToken"]
    st.session_state.user_id = verified["id"]
    st.session_state["app_view"] = ROLE_VIEWS[verified["role"]][0]
    st.session_state["_portal_verified_at"] = time.monotonic()
    st.session_state["_portal_just_logged_in"] = True


def render_login() -> None:
    st.markdown(
        '<section class="fs-hero"><div><span class="fs-eyebrow">BEM-VINDO AO FILASMART</span>'
        '<h1>Seu atendimento, em um só lugar.</h1>'
        '<p>Entre para acessar sua área e acompanhar o que importa.</p></div></section>',
        unsafe_allow_html=True,
    )
    form_column, help_column = st.columns([1.25, 1], gap="large")
    with form_column:
        with st.form("portal_login", clear_on_submit=True):
            st.subheader("Entre para continuar")
            st.caption("Use o e-mail e a senha da sua conta cadastrada.")
            st.text_input("E-mail", key="portal_email", autocomplete="username")
            st.text_input("Senha", key="portal_password", type="password", autocomplete="current-password")
            st.form_submit_button("Entrar", type="primary", on_click=submit_login, use_container_width=True)
        if st.session_state.get("portal_login_error"):
            st.error(st.session_state["portal_login_error"])
    with help_column:
        st.subheader("Um espaço para cada perfil")
        st.write("**Cliente** · Retire sua senha e acompanhe o atendimento.")
        st.write("**Atendente** · Organize a fila e conduza os atendimentos.")
        st.write("**Administrador** · Acesse a operação e os relatórios.")
        st.caption("Seu acesso é definido pela conta cadastrada. Se precisar de cadastro ou recuperação de senha, procure o responsável pelo estabelecimento.")
