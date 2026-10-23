from unittest.mock import Mock
from types import SimpleNamespace

import pytest

from backend_queue import AccessDeniedError, InvalidQueueStateError, QueueBackend


def response(status_code, payload=None):
    result = Mock(status_code=status_code, text="")
    result.json.return_value = payload or {}
    return result


def test_admin_login_defaults_read_xano_seed_settings(monkeypatch):
    import app

    monkeypatch.setattr(
        app,
        "st",
        SimpleNamespace(
            secrets={
                "xano_seed": {
                    "admin_email": "admin@example.invalid",
                    "admin_password": "test-password",
                }
            }
        ),
    )

    assert app._admin_login_defaults() == (
        "admin@example.invalid",
        "test-password",
    )


def test_admin_login_defaults_are_blank_when_secrets_are_unavailable(monkeypatch):
    import app

    monkeypatch.setattr(app, "st", SimpleNamespace(secrets={}))

    assert app._admin_login_defaults() == ("", "")


def test_authenticate_user_success_and_role_restriction(monkeypatch):
    backend = QueueBackend()
    admin_user_id = 42
    post = Mock(
        side_effect=[
            response(200, {"authToken": "admin-token", "user_id": admin_user_id}),
            response(403),
        ]
    )
    monkeypatch.setattr("backend_queue.requests.post", post)

    user = backend.authenticate("admin@filasmart.com", "senha123")
    assert user["role"] == "admin"
    assert user["user_id"] == admin_user_id
    assert user["id"] == admin_user_id
    assert post.call_args_list[0].kwargs["json"] == {
        "email": "admin@filasmart.com",
        "field_value": "admin@filasmart.com",
        "password": "senha123",
    }

    with pytest.raises(AccessDeniedError):
        backend.call_next_token(queue_id=1, attendant_id=999, token=user["authToken"])


def test_emit_ticket_uses_next_number_and_queue_state(monkeypatch):
    backend = QueueBackend()
    post = Mock(
        side_effect=[
            response(200, {"authToken": "client-token", "user_id": 3}),
            response(200, {"id": 1, "number": 1, "status": "waiting"}),
            response(400),
        ]
    )
    monkeypatch.setattr("backend_queue.requests.post", post)

    user = backend.authenticate("cliente@filasmart.com", "cliente123")
    ticket = backend.emit_ticket(queue_id=1, user_id=user["id"])
    assert ticket["status"] == "waiting"
    assert ticket["number"] == 1

    with pytest.raises(InvalidQueueStateError):
        backend.emit_ticket(queue_id=999, user_id=user["id"])


def test_call_next_and_complete_requires_establishment_scope_and_status(monkeypatch):
    backend = QueueBackend()
    post = Mock(
        side_effect=[
            response(200, {"authToken": "attendant-token", "user_id": 2}),
            response(200, {"authToken": "client-token", "user_id": 3}),
            response(200, {"id": 1, "number": 1, "status": "waiting"}),
            response(200, {"senha": {"id": 1, "number": 1}}),
            response(200),
        ]
    )
    monkeypatch.setattr("backend_queue.requests.post", post)

    attendant = backend.authenticate("atendente@filasmart.com", "atendente123")
    client = backend.authenticate("cliente@filasmart.com", "cliente123")
    ticket = backend.emit_ticket(queue_id=1, user_id=client["id"])

    called = backend.call_next_token(
        queue_id=1,
        attendant_id=attendant["id"],
        token=attendant["authToken"],
    )
    assert called["status"] == "called"

    completed = backend.complete_service(
        ticket_id=ticket["id"],
        attendant_id=attendant["id"],
    )
    assert completed["status"] == "completed"

    with pytest.raises(InvalidQueueStateError):
        backend.complete_service(
            ticket_id=ticket["id"],
            attendant_id=attendant["id"],
        )
