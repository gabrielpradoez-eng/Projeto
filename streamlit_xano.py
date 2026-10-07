from __future__ import annotations

import streamlit as st

from xano_client import XanoClient, XanoConfigurationError


@st.cache_resource(show_spinner=False)
def _cached_client(
    login_url: str,
    queues_url: str,
    issue_url: str,
    tracking_url: str,
    email: str,
    password: str,
) -> XanoClient:
    return XanoClient(
        login_url=login_url,
        queues_url=queues_url,
        issue_url=issue_url,
        tracking_url=tracking_url,
        email=email,
        password=password,
    )


def get_xano_client() -> XanoClient:
    test_client = st.session_state.get("_xano_client_override")
    if test_client is not None:
        return test_client

    try:
        settings = st.secrets["xano"]
        values = {
            "login_url": settings["login_url"],
            "queues_url": settings["queues_url"],
            "issue_url": settings["issue_url"],
            "tracking_url": settings["tracking_url"],
            "email": settings["totem_email"],
            "password": settings["totem_password"],
        }
    except (KeyError, FileNotFoundError):
        raise XanoConfigurationError(
            "A integração com Xano não está configurada neste ambiente."
        ) from None

    return _cached_client(**values)