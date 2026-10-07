import pytest

from backend_queue import QueueBackend, AccessDeniedError, QueueNotFoundError, InvalidQueueStateError


def test_authenticate_user_success_and_role_restriction():
    backend = QueueBackend()
    user = backend.authenticate("admin@fila.com", "admin123")
    assert user["role"] == "admin"

    with pytest.raises(AccessDeniedError):
        backend.call_next_token(queue_id=1, attendant_id=999)


def test_emit_ticket_uses_next_number_and_queue_state():
    backend = QueueBackend()
    user = backend.authenticate("cliente@fila.com", "cliente123")
    ticket = backend.emit_ticket(queue_id=1, user_id=user["id"])
    assert ticket["status"] == "waiting"
    assert ticket["number"] == 1

    with pytest.raises(InvalidQueueStateError):
        backend.emit_ticket(queue_id=999, user_id=user["id"])


def test_call_next_and_complete_requires_establishment_scope_and_status():
    backend = QueueBackend()
    user = backend.authenticate("atendente@fila.com", "atendente123")
    ticket = backend.emit_ticket(queue_id=1, user_id=backend.authenticate("cliente@fila.com", "cliente123")["id"])

    called = backend.call_next_token(queue_id=1, attendant_id=user["id"])
    assert called["status"] == "called"

    completed = backend.complete_service(ticket_id=ticket["id"], attendant_id=user["id"])
    assert completed["status"] == "completed"

    with pytest.raises(InvalidQueueStateError):
        backend.complete_service(ticket_id=ticket["id"], attendant_id=user["id"])
