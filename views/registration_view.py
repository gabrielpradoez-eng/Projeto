from __future__ import annotations

import streamlit as st

from backend_queue import AccessDeniedError, InvalidQueueStateError
from streamlit_xano import get_analytics_client
from xano_client import XanoClientError


def render_attendant_registration(backend, user: dict) -> None:
    if user.get("role") != "admin":
        return
    st.subheader("Cadastrar atendente")
    st.write("O profissional deve criar sua conta na tela inicial. Depois, informe o mesmo e-mail para liberar o atendimento.")
    try:
        options = get_analytics_client(auth_token=user["authToken"]).list_options()
    except XanoClientError:
        st.warning("Não foi possível carregar os estabelecimentos. Tente novamente.")
        return
    establishments = {row["id"]: row["nome"] for row in options["estabelecimentos"]}
    if not establishments:
        st.info("Nenhum estabelecimento disponível para cadastro.")
        return
    with st.form("attendant_registration", clear_on_submit=True):
        email = st.text_input("E-mail da conta do atendente", autocomplete="off")
        establishment = st.selectbox("Estabelecimento do atendente", options=list(establishments), format_func=establishments.get)
        destination = st.text_input("Guichê de atendimento", max_chars=80, placeholder="Ex.: Guichê 02")
        confirmed = st.checkbox("Confirmo a liberação desta conta para atender neste estabelecimento")
        submitted = st.form_submit_button("Cadastrar atendente", type="primary")
    if not submitted:
        return
    if not confirmed:
        st.warning("Confirme a liberação de acesso antes de cadastrar.")
        return
    try:
        backend.register_attendant(email, establishment, destination, token=user["authToken"])
    except (AccessDeniedError, InvalidQueueStateError) as exc:
        st.error(str(exc))
        st.caption("Confira se a conta já foi criada e ainda é de cliente. Contas com vínculo anterior não são alteradas.")
        return
    st.success("Atendente cadastrado. O profissional pode entrar com a senha que já utiliza; se estiver conectado, deve sair e entrar novamente.")
