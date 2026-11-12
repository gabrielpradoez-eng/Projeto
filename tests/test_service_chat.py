from unittest.mock import Mock

import pytest
from streamlit.testing.v1 import AppTest

from backend_queue import AccessDeniedError, InvalidQueueStateError, QueueBackend
from views.service_chat import service_chat_enabled


ACTIVE = {"senha_id": 19, "numero": 6, "guiche": "Guichê 1"}
LITERAL = "<img src=x> [link](https://example.invalid)"
VALIDATED_API = "https://x8ki-letl-twmt.n7.xano.io/api:queue-management"


@pytest.mark.parametrize(("settings", "expected"), [
    ({"base_url": VALIDATED_API + "/"}, True),
    ({"base_url": VALIDATED_API, "service_chat_enabled": False}, False),
    ({"base_url": VALIDATED_API + "-outro"}, False),
    ({"base_url": "https://xano.invalid/api:queues", "service_chat_enabled": True}, True),
    ({}, False),
])
def test_chat_activation_defaults_to_validated_api_and_respects_override(monkeypatch, settings, expected):
    monkeypatch.setattr("views.service_chat.st.secrets", {"xano": settings})
    assert service_chat_enabled() is expected


def chat_app(backend):
    app = AppTest.from_string("""
import streamlit as st
from views.service_chat import render_service_chat
render_service_chat(st.session_state.backend, {"role":"user","id":7,"authToken":"client-token"})
""")
    app.session_state["backend"] = backend
    return app.run()


def test_chat_opens_on_call_and_closes_when_backend_reports_no_active_service():
    backend = Mock()
    backend.get_service_chat.return_value = {"atendimento": None, "mensagens": []}
    app = chat_app(backend)
    assert not app.exception and not app.chat_input
    backend.get_service_chat.return_value = {
        "atendimento": ACTIVE, "mensagens": [{"remetente_id": 10, "mensagem": LITERAL}],
    }
    app.run()
    assert app.chat_input and app.text[0].value == LITERAL
    app.chat_input[0].set_value("Mensagem de teste").run()
    assert not app.exception
    backend.send_service_message.assert_called_once_with(19, "Mensagem de teste", token="client-token")
    backend.get_service_chat.return_value = {"atendimento": None, "mensagens": []}
    app.run()
    assert not app.chat_input and not app.text


def test_access_denied_removes_previous_messages_and_disables_sending():
    backend = Mock()
    backend.get_service_chat.side_effect = AccessDeniedError("denied")
    app = chat_app(backend)
    assert not app.exception and not app.chat_input and not app.text
    backend.send_service_message.assert_not_called()


def test_client_refuses_cross_ticket_response_and_invalid_outgoing_message(monkeypatch):
    monkeypatch.setattr("backend_queue.st.secrets", {"xano": {"base_url": "https://xano.invalid/api:queues"}})
    backend = QueueBackend()
    post = Mock(return_value=Mock(status_code=200, json=lambda: {
        "atendimento": ACTIVE, "mensagens": [],
    }))
    monkeypatch.setattr("backend_queue.requests.post", post)
    with pytest.raises(InvalidQueueStateError):
        backend.get_service_chat(20, token="session-token")
    assert post.call_args.kwargs["headers"]["Authorization"] == "Bearer session-token"
    with pytest.raises(InvalidQueueStateError):
        backend.send_service_message(19, "x" * 501, token="session-token")
    assert post.call_count == 1
