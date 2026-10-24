from unittest.mock import Mock
from types import SimpleNamespace

import pytest

from backend_queue import AccessDeniedError, InvalidQueueStateError, QueueBackend


def response(status_code, payload=None):
    result = Mock(status_code=status_code, text="")
    result.json.return_value = payload or {}
    return result


def login_payload(user_id, role, *, email="remote@example.com", establishment_id=None):
    return {
        "authToken": "server-token",
        "user": {
            "id": user_id,
            "name": "Remote User",
            "email": email,
            "role": role,
            "estabelecimento_id": establishment_id,
        },
    }


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
            response(200, login_payload(admin_user_id, "admin")),
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
        "password": "senha123",
    }

    with pytest.raises(AccessDeniedError):
        backend.call_next_token(queue_id=1, attendant_id=999, token=user["authToken"])


@pytest.mark.parametrize(
    ("remote_role", "expected_role"),
    [
        ("admin", "admin"),
        ("atendente", "attendant"),
        ("usuario", "user"),
    ],
)
def test_authenticate_uses_remote_identity_and_maps_xano_roles(
    monkeypatch, remote_role, expected_role
):
    backend = QueueBackend()
    post = Mock(
        return_value=response(
            200,
            login_payload(
                987,
                remote_role,
                email="not-in-local-samples@example.com",
                establishment_id=24,
            ),
        )
    )
    monkeypatch.setattr("backend_queue.requests.post", post)

    user = backend.authenticate("submitted@example.com", "password")

    assert user == {
        "id": 987,
        "user_id": 987,
        "name": "Remote User",
        "email": "not-in-local-samples@example.com",
        "role": expected_role,
        "establishment_id": 24,
        "authToken": "server-token",
    }


@pytest.mark.parametrize(
    "payload",
    [
        {"authToken": "server-token", "user_id": 42},
        {
            "authToken": "server-token",
            "user": {
                "id": 42,
                "name": "Remote User",
                "email": "remote@example.com",
                "role": "unknown",
            },
        },
        login_payload(True, "admin"),
        {
            "authToken": "server-token",
            "user": {
                "id": 42,
                "name": "Remote User",
                "role": "admin",
            },
        },
        login_payload(42, ["admin"]),
    ],
)
def test_authenticate_rejects_malformed_remote_identity(monkeypatch, payload):
    backend = QueueBackend()
    monkeypatch.setattr(
        "backend_queue.requests.post",
        Mock(return_value=response(200, payload)),
    )

    with pytest.raises(AccessDeniedError, match="Resposta de autenticação inválida"):
        backend.authenticate("remote@example.com", "password")

    assert backend.logs == []


def test_emit_ticket_uses_next_number_and_queue_state(monkeypatch):
    backend = QueueBackend()
    post = Mock(
        side_effect=[
            response(200, login_payload(3, "usuario", email="client@example.com")),
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
            response(200, login_payload(2, "atendente", email="staff@example.com", establishment_id=1)),
            response(200, login_payload(3, "usuario", email="client@example.com")),
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
