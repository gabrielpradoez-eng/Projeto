from pathlib import Path
from unittest.mock import Mock

import pytest
from streamlit.testing.v1 import AppTest
from backend_queue import QueueBackend, InvalidQueueStateError


def backend():
    service = QueueBackend()
    service.login_url = "https://xano.invalid/auth/login"
    service.base_url = "https://xano.invalid/queue"
    return service


@pytest.mark.parametrize("name,email,password", [(" ", "a@b.com", "long-password"), ("Ana", "invalid", "long-password"), ("Ana", "a@b.com", "short"), ("Ana", "a@b.com", "x" * 129)])
def test_invalid_customer_fields_never_reach_network(monkeypatch, name, email, password):
    post = Mock()
    monkeypatch.setattr("backend_queue.requests.post", post)
    with pytest.raises(InvalidQueueStateError):
        backend().register_customer(name, email, password)
    post.assert_not_called()


def test_signup_normalizes_identity_and_never_submits_a_role(monkeypatch):
    response = Mock(status_code=200)
    response.json.return_value = {"user_id": 12, "authToken": "ignored-token"}
    post = Mock(return_value=response)
    monkeypatch.setattr("backend_queue.requests.post", post)
    assert backend().register_customer(" Ana ", " ANA@EXAMPLE.COM ", "long-password") == 12
    assert post.call_args.args == ("https://xano.invalid/auth/signup",)
    assert post.call_args.kwargs["json"] == {"name": "Ana", "email": "ana@example.com", "password": "long-password"}


@pytest.mark.parametrize("body", [{}, {"user_id": True}, {"user_id": -1}, []])
def test_signup_does_not_confirm_malformed_success(monkeypatch, body):
    response = Mock(status_code=200)
    response.json.return_value = body
    monkeypatch.setattr("backend_queue.requests.post", Mock(return_value=response))
    with pytest.raises(InvalidQueueStateError):
        backend().register_customer("Ana", "ana@example.com", "long-password")


def test_registration_password_mismatch_clears_secrets_and_never_creates_session():
    service = Mock()
    app = AppTest.from_string('''
import streamlit as st
from portal_session import render_customer_registration
render_customer_registration()
''')
    app.session_state.backend = service
    app.run()
    app.text_input(key="signup_name").set_value("Ana")
    app.text_input(key="signup_email").set_value("ana@example.com")
    app.text_input(key="signup_password").set_value("long-password")
    app.text_input(key="signup_confirmation").set_value("different-password")
    app.button[0].click().run()
    assert not app.exception
    assert app.error
    service.register_customer.assert_not_called()
    assert not app.session_state["signup_password"]
    assert not app.session_state["signup_confirmation"]
    assert "authToken" not in app.session_state


def test_successful_signup_requires_explicit_login_and_clears_password():
    service = Mock()
    service.register_customer.return_value = 12
    app = AppTest.from_string('''
import streamlit as st
from portal_session import render_customer_registration
render_customer_registration()
''')
    app.session_state.backend = service
    app.run()
    for key, value in {"signup_name": "Ana", "signup_email": "ana@example.com", "signup_password": "long-password", "signup_confirmation": "long-password"}.items():
        app.text_input(key=key).set_value(value)
    app.button[0].click().run()
    assert not app.exception
    assert app.success
    assert "authToken" not in app.session_state
    assert not app.session_state["signup_password"]


def test_attendant_signup_uses_actor_token_without_password_or_role_input(monkeypatch):
    service = backend()
    service._operation_request = Mock(return_value={"id": 12, "role": "atendente", "estabelecimento_id": 1})
    service.register_attendant(" ANA@EXAMPLE.COM ", 1, " Guichê 02 ", token="admin-session")
    service._operation_request.assert_called_once_with("admin/attendants", {"email": "ana@example.com", "estabelecimento_id": 1, "destino_label": "Guichê 02"}, "admin-session")


def test_attendant_endpoint_rejects_ineligible_accounts_before_atomic_writes():
    source = (Path(__file__).parents[1] / "xano/api/queue_management/admin/attendants_POST.xs").read_text()
    assert 'auth = "usuarios"' in source
    assert source.index('$actor.role == "admin"') < source.index("db.transaction")
    assert source.index("$actor.estabelecimento_id == $input.estabelecimento_id") < source.index("db.transaction")
    assert source.index('$candidate.role == "usuario"') < source.index("db.add atendentes")
    assert source.index("$existing == null") < source.index("db.add atendentes")
    assert source.index("db.transaction") < source.index("db.add atendentes") < source.index("db.edit usuarios")
    assert "password" not in source.split("response =", 1)[1]
