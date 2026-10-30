from pathlib import Path
from unittest.mock import Mock

import pytest
from streamlit.testing.v1 import AppTest

from backend_queue import AccessDeniedError, QueueBackend, SessionVerificationUnavailable
from portal_session import ROLE_VIEWS


def identity(role="user", token="verified-token", user_id=31):
    return {"id": user_id, "user_id": user_id, "name": "Conta verificada",
            "email": "account@example.invalid", "role": role, "authToken": token}


class IdentityBackend:
    def __init__(self, role="user"):
        self.profile = identity(role)
        self.authenticate = Mock(return_value=dict(self.profile))
        self.verify_session = Mock(side_effect=lambda *_: dict(self.profile))
        self.get_attendant_dashboard = Mock(return_value=[])


class NoContentClient:
    def __init__(self):
        self.calls = 0

    def list_queues(self):
        self.calls += 1
        return []

    def fetch_snapshot(self):
        self.calls += 1
        return {"current_call": None, "history": [], "snapshot_at": "2026-10-29T15:00:00Z"}


def portal(backend=None, signed_in=False, **values):
    app = AppTest.from_file(Path(__file__).resolve().parents[1] / "app.py", default_timeout=10)
    backend = backend or IdentityBackend()
    app.session_state["backend"] = backend
    if signed_in:
        app.session_state["user"] = dict(backend.profile)
        app.session_state["authToken"] = backend.profile["authToken"]
    for key, value in values.items():
        app.session_state[key] = value
    return app


def login(app):
    app.run()
    next(field for field in app.text_input if field.label == "E-mail").set_value("account@example.invalid")
    next(field for field in app.text_input if field.label == "Senha").set_value("test-password")
    next(button for button in app.button if button.label == "Entrar").click().run()
    return app


def test_anonymous_session_cannot_render_any_feature_or_request_backend_data():
    source = NoContentClient()
    backend = IdentityBackend()
    app = portal(backend, app_view="Relatórios", analytics_auth_token="old-admin-token",
                 _xano_client_override=source, _display_feed_client_override=source).run()
    assert not app.exception
    assert not app.radio
    assert not app.metric
    assert not app.get("download_button")
    assert {button.label for button in app.button} == {"Entrar", "Criar conta"}
    assert source.calls == 0
    backend.verify_session.assert_not_called()


@pytest.mark.parametrize("role", ["user", "attendant", "admin"])
def test_login_confirms_remote_identity_and_shows_only_profile_views(monkeypatch, role):
    source = NoContentClient()
    monkeypatch.setattr("views.client_view.get_xano_client", lambda: source)
    backend = IdentityBackend(role)
    app = login(portal(backend, ticket_reference="previous-customer-reference",
                       analytics_report={"private": "old-report"}))
    assert not app.exception
    assert tuple(app.radio(key="app_view").options) == ROLE_VIEWS[role]
    assert app.radio(key="app_view").value == ROLE_VIEWS[role][0]
    backend.verify_session.assert_called_once_with("verified-token", 31)
    assert "ticket_reference" not in app.session_state
    assert "analytics_report" not in app.session_state
    assert "portal_password" not in app.session_state
    assert not app.text_input


def test_remote_role_overrides_a_privileged_login_claim(monkeypatch):
    monkeypatch.setattr("views.client_view.get_xano_client", lambda: NoContentClient())
    backend = IdentityBackend("user")
    backend.authenticate.return_value = identity("admin")
    app = login(portal(backend))
    assert not app.exception
    assert "Administração" not in app.radio(key="app_view").options
    assert "Relatórios" not in app.radio(key="app_view").options
    assert app.session_state["user"]["role"] == "user"


def test_invalid_login_never_creates_a_session_or_displays_internal_details():
    backend = IdentityBackend()
    backend.authenticate.side_effect = AccessDeniedError("private-service-error")
    app = login(portal(backend))
    assert not app.exception
    assert not app.radio
    assert app.session_state["user"] is None
    assert "authToken" not in app.session_state
    assert "private-service-error" not in str([item.value for item in app.error])
    backend.verify_session.assert_not_called()


def test_expired_session_erases_private_state_and_returns_to_login():
    backend = IdentityBackend("admin")
    backend.verify_session.side_effect = AccessDeniedError("expired")
    source = NoContentClient()
    app = portal(backend, signed_in=True, app_view="Painel TV",
                 _display_feed_client_override=source, ticket_reference="private-reference",
                 analytics_auth_token="private-token", tv_last_snapshot={"private": True}).run()
    assert not app.exception
    assert not app.radio
    assert source.calls == 0
    for key in ("authToken", "ticket_reference", "analytics_auth_token", "tv_last_snapshot"):
        assert key not in app.session_state


def test_identity_service_outage_blocks_content_without_destroying_session():
    backend = IdentityBackend("admin")
    backend.verify_session.side_effect = SessionVerificationUnavailable("temporarily unavailable")
    source = NoContentClient()
    app = portal(backend, signed_in=True, app_view="Painel TV",
                 _display_feed_client_override=source).run()
    assert not app.exception
    assert not app.radio
    assert source.calls == 0
    assert app.warning
    assert app.session_state["authToken"] == "verified-token"


def test_profile_downgrade_blocks_stale_admin_selection_and_clears_report():
    backend = IdentityBackend("admin")
    app = portal(backend, signed_in=True, app_view="Relatórios", analytics_report={"private": True},
                 analytics_auth_token="stale-admin-token", _xano_client_override=NoContentClient())
    backend.profile = identity("user")
    app.run()
    assert not app.exception
    assert app.radio(key="app_view").value == "Cliente"
    assert "Relatórios" not in app.radio(key="app_view").options
    assert "analytics_report" not in app.session_state
    assert "analytics_auth_token" not in app.session_state


def test_logout_clears_customer_and_admin_state():
    app = portal(IdentityBackend("admin"), signed_in=True, app_view="Administração",
                 ticket_reference="private-reference", client_ticket_reference="other-private-reference",
                 analytics_report={"private": True}, analytics_auth_token="report-token").run()
    next(button for button in app.button if button.label == "Sair").click().run()
    assert not app.exception
    assert not app.radio
    for key in ("authToken", "ticket_reference", "client_ticket_reference", "analytics_report", "analytics_auth_token"):
        assert key not in app.session_state


def test_tv_scheduled_refresh_stops_before_fetch_when_session_is_revoked():
    backend = IdentityBackend("admin")
    feed = NoContentClient()
    app = AppTest.from_string('''
import streamlit as st
from unittest.mock import patch
from views.display_view import render_display_view
from backend_queue import AccessDeniedError

captured = []
def capture_fragment(**kwargs):
    def decorate(fn):
        captured.append(fn)
        return fn
    return decorate
class StopRefresh(Exception):
    pass
feed = st.session_state._display_feed_client_override
backend = st.session_state.backend
with patch.object(st, "fragment", capture_fragment):
    render_display_view()
st.session_state._portal_verified_at = 0
backend.verify_session.side_effect = AccessDeniedError("revoked")
with patch("portal_session.st.rerun", side_effect=StopRefresh):
    try:
        captured[0]()
    except StopRefresh:
        pass
st.write(f"Feed requests: {feed.calls}")
''', default_timeout=10)
    for key, value in {"backend": backend, "user": backend.profile, "authToken": "verified-token",
                       "_portal_managed": True, "_display_feed_client_override": feed}.items():
        app.session_state[key] = value
    app.run()
    assert not app.exception
    assert feed.calls == 1
    assert "authToken" not in app.session_state


@pytest.mark.parametrize("status", [401, 403, 404])
def test_canonical_verification_rejects_expired_token(monkeypatch, status):
    backend = QueueBackend()
    backend.me_url = "https://xano.invalid/auth/me"
    monkeypatch.setattr("backend_queue.requests.get", Mock(return_value=Mock(status_code=status)))
    with pytest.raises(AccessDeniedError):
        backend.verify_session("expired-token", 31)


@pytest.mark.parametrize("remote_role,role", [("usuario", "user"), ("atendente", "attendant"), ("admin", "admin")])
def test_canonical_verification_maps_profile_and_uses_only_the_supplied_token(monkeypatch, remote_role, role):
    backend = QueueBackend()
    backend.me_url = "https://xano.invalid/auth/me"
    response = Mock(status_code=200)
    response.json.return_value = {"id": 31, "name": "Remote User", "email": "u@example.invalid", "role": remote_role}
    get = Mock(return_value=response)
    monkeypatch.setattr("backend_queue.requests.get", get)
    verified = backend.verify_session("session-specific-token", 31)
    assert verified["role"] == role
    assert verified["id"] == 31
    assert verified["authToken"] == "session-specific-token"
    assert get.call_args.kwargs["headers"]["Authorization"] == "Bearer session-specific-token"
    assert get.call_args.kwargs["timeout"] == 10


@pytest.mark.parametrize("profile", [
    {"id": True, "name": "User", "email": "u@example.invalid", "role": "admin"},
    {"id": 32, "name": "User", "email": "u@example.invalid", "role": "admin"},
    {"id": 31, "name": "User", "email": "u@example.invalid", "role": ["admin"]},
    {"id": 31, "name": "User", "email": "u@example.invalid", "role": "totem"},
])
def test_canonical_verification_rejects_mismatched_or_unsupported_identity(monkeypatch, profile):
    backend = QueueBackend()
    backend.me_url = "https://xano.invalid/auth/me"
    response = Mock(status_code=200)
    response.json.return_value = profile
    monkeypatch.setattr("backend_queue.requests.get", Mock(return_value=response))
    with pytest.raises(AccessDeniedError):
        backend.verify_session("token", 31)


@pytest.mark.parametrize("role", ["user", "attendant", "admin"])
def test_mobile_navigation_uses_verified_profile_and_switches_both_menus(monkeypatch, role):
    source = NoContentClient()
    monkeypatch.setattr("views.client_view.get_xano_client", lambda: source)
    app = portal(IdentityBackend(role), signed_in=True,
                 _display_feed_client_override=source).run()
    assert not app.exception
    assert app.selectbox(key="mobile_view").options == list(ROLE_VIEWS[role])
    app.selectbox(key="mobile_view").select("Painel TV").run()
    assert not app.exception
    assert app.radio(key="app_view").value == "Painel TV"
    assert source.calls >= 1
    first_view = ROLE_VIEWS[role][0]
    app.radio(key="app_view").set_value(first_view).run()
    assert not app.exception
    assert app.selectbox(key="mobile_view").value == first_view


def test_mobile_logout_clears_session_and_removes_navigation(monkeypatch):
    monkeypatch.setattr("views.client_view.get_xano_client", lambda: NoContentClient())
    app = portal(IdentityBackend(), signed_in=True).run()
    app.button(key="mobile_logout").click().run()
    assert not app.exception
    assert "authToken" not in app.session_state
    assert not app.radio
    assert not any(widget.key == "mobile_view" for widget in app.selectbox)


def test_mobile_selection_cannot_survive_profile_downgrade(monkeypatch):
    backend = IdentityBackend("admin")
    backend.profile = identity("user")
    monkeypatch.setattr("views.client_view.get_xano_client", lambda: NoContentClient())
    app = portal(backend, signed_in=True, app_view="Relatórios", mobile_view="Relatórios").run()
    assert not app.exception
    assert app.selectbox(key="mobile_view").value == "Cliente"
    assert "Relatórios" not in app.selectbox(key="mobile_view").options
