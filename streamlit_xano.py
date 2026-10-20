from __future__ import annotations

import streamlit as st

from analytics_client import AnalyticsClient
from xano_client import DisplayFeedClient, XanoClient, XanoConfigurationError


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


@st.cache_resource(show_spinner=False)
def _cached_display_client(feed_url: str, credential: str) -> DisplayFeedClient:
    return DisplayFeedClient(feed_url=feed_url, credential=credential)


def get_display_feed_client() -> DisplayFeedClient:
    test_client = st.session_state.get("_display_feed_client_override")
    if test_client is not None:
        return test_client

    try:
        settings = st.secrets["tv_display"]
        feed_url = settings["feed_url"]
        credential = settings["credential"]
    except (KeyError, FileNotFoundError):
        raise XanoConfigurationError(
            "O feed Xano do painel TV não está configurado neste ambiente."
        ) from None

    return _cached_display_client(feed_url, credential)


def analytics_login(email: str, password: str) -> str:
    try:
        login_url = st.secrets["analytics"]["login_url"]
    except (KeyError, FileNotFoundError):
        raise XanoConfigurationError(
            "A autenticação analítica com Xano não está configurada neste ambiente."
        ) from None
    return AnalyticsClient.authenticate(login_url, email, password)


def get_analytics_client(auth_token: str | None = None) -> AnalyticsClient:
    test_client = st.session_state.get("_analytics_client_override")
    if test_client is not None:
        return test_client

    try:
        settings = st.secrets["analytics"]
        token = auth_token or st.session_state.get("analytics_auth_token")
        if not token:
            raise XanoConfigurationError("Entre com uma conta administradora do Xano.")
        return AnalyticsClient(
            options_url=settings["options_url"],
            report_url=settings["report_url"],
            auth_token=token,
        )
    except XanoConfigurationError:
        raise
    except (KeyError, FileNotFoundError):
        raise XanoConfigurationError(
            "A integração analítica com Xano não está configurada neste ambiente."
        ) from None