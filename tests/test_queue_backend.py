from unittest.mock import Mock
from types import SimpleNamespace

import pytest

from backend_queue import AccessDeniedError, InvalidQueueStateError, QueueBackend


@pytest.fixture(autouse=True)
def configured_xano(monkeypatch):
    monkeypatch.setattr("backend_queue.st.secrets", {
        "xano": {
            "base_url": "https://xano.invalid/api:queues",
            "login_url": "https://xano.invalid/api:auth/auth/login",
        }
    })


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


def ticket_payload(status="aguardando", *, number=23, ticket_id=57):
    return {"id": ticket_id, "numero": number, "fila_id": 1, "usuario_id": 3, "status": status}


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
        {"authToken": "server-token", "user_id": "invalid"},
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
            response(200, ticket_payload(number=1, ticket_id=1)),
            response(400),
        ]
    )
    monkeypatch.setattr("backend_queue.requests.post", post)

    user = backend.authenticate("cliente@filasmart.com", "cliente123")
    ticket = backend.emit_ticket(queue_id=1, user_id=user["id"], token=user["authToken"])
    assert ticket["status"] == "waiting"
    assert ticket["number"] == 1

    with pytest.raises(InvalidQueueStateError):
        backend.emit_ticket(queue_id=999, user_id=user["id"], token=user["authToken"])


def test_call_next_and_complete_requires_establishment_scope_and_status(monkeypatch):
    backend = QueueBackend()
    post = Mock(
        side_effect=[
            response(200, login_payload(2, "atendente", email="staff@example.com", establishment_id=1)),
            response(200, login_payload(3, "usuario", email="client@example.com")),
            response(200, ticket_payload(number=1, ticket_id=1)),
            response(200, {"senha": ticket_payload("chamado", number=1, ticket_id=1)}),
            response(200, {"senha": ticket_payload("concluido", number=1, ticket_id=1)}),
            response(400),
        ]
    )
    monkeypatch.setattr("backend_queue.requests.post", post)

    attendant = backend.authenticate("atendente@filasmart.com", "atendente123")
    client = backend.authenticate("cliente@filasmart.com", "cliente123")
    ticket = backend.emit_ticket(queue_id=1, user_id=client["id"], token=client["authToken"])

    called = backend.call_next_token(
        queue_id=1,
        attendant_id=attendant["id"],
        token=attendant["authToken"],
    )
    assert called["status"] == "called"

    completed = backend.complete_service(
        ticket_id=ticket["id"],
        attendant_id=attendant["id"], token=attendant["authToken"],
    )
    assert completed["status"] == "completed"

    with pytest.raises(InvalidQueueStateError):
        backend.complete_service(
            ticket_id=ticket["id"],
            attendant_id=attendant["id"], token=attendant["authToken"],
        )


def test_legacy_login_confirms_identity_using_me_and_separate_api_groups(monkeypatch):
    backend = QueueBackend()
    post = Mock(return_value=response(200, {"authToken": "token", "user_id": 42}))
    get = Mock(return_value=response(200, login_payload(42, "atendente")["user"]))
    monkeypatch.setattr("backend_queue.requests.post", post)
    monkeypatch.setattr("backend_queue.requests.get", get)
    assert backend.authenticate("staff@example.invalid", "password")["id"] == 42
    assert post.call_args.args[0] == "https://xano.invalid/api:auth/auth/login"
    assert get.call_args.args[0] == "https://xano.invalid/api:auth/auth/me"
    assert get.call_args.kwargs["headers"]["Authorization"] == "Bearer token"


def test_legacy_login_rejects_identity_mismatch(monkeypatch):
    backend = QueueBackend()
    monkeypatch.setattr("backend_queue.requests.post", Mock(return_value=response(200, {"authToken": "token", "user_id": 42})))
    monkeypatch.setattr("backend_queue.requests.get", Mock(return_value=response(200, login_payload(43, "admin")["user"])))
    with pytest.raises(AccessDeniedError):
        backend.authenticate("staff@example.invalid", "password")
    assert backend.logs == []


def test_dashboard_reads_shared_state_and_rejects_permission_failure(monkeypatch):
    backend = QueueBackend()
    rows = [{"id": 9, "nome": "Fila real", "total_aguardando": 3, "em_atendimento": {"id": 57, "numero": 23}}]
    get = Mock(side_effect=[response(200, rows), response(403)])
    monkeypatch.setattr("backend_queue.requests.get", get)
    assert backend.get_attendant_dashboard("token") == rows
    assert get.call_args.args[0] == "https://xano.invalid/api:queues/attendant/dashboard"
    with pytest.raises(AccessDeniedError):
        backend.get_attendant_dashboard("token")


def test_call_next_uses_actual_xano_number(monkeypatch):
    backend = QueueBackend()
    monkeypatch.setattr("backend_queue.requests.post", Mock(return_value=response(200, {"senha": ticket_payload("chamado")})))
    assert backend.call_next_token(1, 42, "token")["number"] == 23


@pytest.mark.parametrize("payload", [{}, {"senha": {}}, {"senha": {"id": 57}}, {"senha": ticket_payload("aguardando")}])
def test_call_next_rejects_incomplete_or_wrong_status_without_inventing_ticket(monkeypatch, payload):
    backend = QueueBackend()
    monkeypatch.setattr("backend_queue.requests.post", Mock(return_value=response(200, payload)))
    with pytest.raises(InvalidQueueStateError):
        backend.call_next_token(1, 2, "token")
    assert backend.tickets == {}


def test_operation_errors_do_not_expose_response_body(monkeypatch):
    backend = QueueBackend()
    rejected = response(500)
    rejected.text = "password=private-secret Bearer sensitive-token"
    monkeypatch.setattr("backend_queue.requests.post", Mock(return_value=rejected))
    with pytest.raises(InvalidQueueStateError) as error:
        backend.call_next_token(1, 2, "token")
    assert "private-secret" not in str(error.value)
    assert "sensitive-token" not in str(error.value)


def test_timeout_does_not_retry_mutation_or_confirm_success(monkeypatch):
    import requests
    backend = QueueBackend()
    post = Mock(side_effect=requests.Timeout("sensitive-url"))
    monkeypatch.setattr("backend_queue.requests.post", post)
    with pytest.raises(InvalidQueueStateError, match="Atualize o painel"):
        backend.call_next_token(1, 2, "token")
    assert post.call_count == 1
    assert not backend.tickets


def test_completion_after_new_session_uses_remote_response(monkeypatch):
    backend = QueueBackend()
    monkeypatch.setattr("backend_queue.requests.post", Mock(return_value=response(200, {"senha": ticket_payload("concluido")})))
    assert backend.complete_service(57, 2, "token")["number"] == 23


def test_mutation_requires_token_before_sending_request(monkeypatch):
    backend = QueueBackend()
    post = Mock()
    monkeypatch.setattr("backend_queue.requests.post", post)
    with pytest.raises(AccessDeniedError):
        backend.call_next_token(1, 2)
    post.assert_not_called()


@pytest.mark.parametrize("change", [{"status": []}, {"fila_id": 999}, {"id": True}, {"numero": 0}])
def test_call_next_rejects_malformed_or_unrelated_ticket(monkeypatch, change):
    backend = QueueBackend()
    ticket = {**ticket_payload("chamado"), **change}
    monkeypatch.setattr("backend_queue.requests.post", Mock(return_value=response(200, {"senha": ticket})))
    with pytest.raises(InvalidQueueStateError):
        backend.call_next_token(1, 2, "token")
    assert not backend.tickets


def test_dashboard_rejects_current_ticket_without_identity(monkeypatch):
    backend = QueueBackend()
    monkeypatch.setattr("backend_queue.requests.get", Mock(return_value=response(200, [
        {"id": 9, "nome": "Fila", "total_aguardando": 0, "em_atendimento": {"numero": 23}}
    ])))
    with pytest.raises(InvalidQueueStateError, match="Resposta inválida"):
        backend.get_attendant_dashboard("token")
