import io
import json
import logging
from urllib.error import HTTPError
from unittest.mock import patch

import pytest

from xano_client import QueueUnavailableError, TrackingUnavailableError, XanoClient, XanoRequestError


class FakeResponse:
    def __init__(self, payload):
        self._body = json.dumps(payload).encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return False

    def read(self):
        return self._body


def make_client():
    return XanoClient(
        login_url="https://xano.invalid/login",
        queues_url="https://xano.invalid/queues",
        issue_url="https://xano.invalid/issue",
        tracking_url="https://xano.invalid/tracking",
        email="totem@example.invalid",
        password="server-only-password",
    )


@pytest.mark.parametrize("payload", [{}, {"numero": True, "referencia_rastreamento": "ref"},
                                      {"numero": 1, "referencia_rastreamento": " "},
                                      {"numero": 1, "referencia_rastreamento": "ref", "status": "cancelado"}])
def test_invalid_issue_confirmation_is_not_accepted(payload):
    with patch("xano_client.urlopen", side_effect=[FakeResponse({"authToken": "token"}), FakeResponse(payload)]):
        with pytest.raises(XanoRequestError, match="emissão"):
            make_client().issue_ticket(1)


@pytest.mark.parametrize("rows", [[{}], [{"fila_id": True, "fila_nome": "Fila", "servico_nome": "Geral"}],
                                  [{"fila_id": 1, "fila_nome": "Fila", "servico_nome": "Geral"}] * 2])
def test_invalid_or_duplicate_queue_is_rejected_before_rendering(rows):
    with patch("xano_client.urlopen", side_effect=[FakeResponse({"authToken": "token"}), FakeResponse(rows)]):
        with pytest.raises(XanoRequestError, match="filas"):
            make_client().list_queues()


@pytest.mark.parametrize("changes", [{"numero": True}, {"fila": ""}, {"posicao": True}, {"status": "unknown"}])
def test_invalid_tracking_response_is_rejected_before_rendering(changes):
    payload = {"numero": 1, "fila": "Fila principal", "servico": "Atendimento geral",
               "status": "aguardando", "posicao": 1, "atualizado_at": 1793280000000}
    payload.update(changes)
    with patch("xano_client.urlopen", side_effect=[FakeResponse({"authToken": "token"}), FakeResponse(payload)]):
        with pytest.raises(XanoRequestError, match="acompanhamento"):
            make_client().track_ticket("private-reference")


def test_login_is_cached_and_requests_use_bearer_token():
    requests = []
    responses = [
        {"authToken": "server-token"},
        [{"fila_id": 7, "fila_nome": "Geral", "servico_nome": "Atendimento geral"}],
        {"numero": 12, "referencia_rastreamento": "opaque-reference"},
    ]

    def fake_urlopen(request, timeout):
        requests.append(request)
        assert timeout == 8.0
        return FakeResponse(responses.pop(0))

    with patch("xano_client.urlopen", side_effect=fake_urlopen):
        client = make_client()
        assert client.list_queues()[0]["fila_id"] == 7
        assert client.issue_ticket(7)["numero"] == 12

    assert len(requests) == 3
    login_payload = json.loads(requests[0].data.decode("utf-8"))
    assert login_payload == {
        "email": "totem@example.invalid",
        "field_value": "totem@example.invalid",
        "password": "server-only-password",
    }
    assert requests[1].get_header("Authorization") == "Bearer server-token"
    assert requests[2].get_header("Authorization") == "Bearer server-token"


def test_tracking_reference_is_sent_in_post_body_not_url():
    requests = []
    responses = [
        {"authToken": "server-token"},
        {"numero": 12, "status": "aguardando", "posicao": 2, "fila": "Geral", "servico": "Atendimento geral", "atualizado_at": 1793280000000},
    ]

    def fake_urlopen(request, timeout):
        requests.append(request)
        return FakeResponse(responses.pop(0))

    with patch("xano_client.urlopen", side_effect=fake_urlopen):
        result = make_client().track_ticket("secret-reference")

    tracking_request = requests[1]
    assert result["posicao"] == 2
    assert tracking_request.get_method() == "POST"
    assert "secret-reference" not in tracking_request.full_url
    assert json.loads(tracking_request.data.decode("utf-8")) == {
        "referencia": "secret-reference"
    }


def test_tracking_404_becomes_generic_unavailable_error():
    def fake_urlopen(request, timeout):
        if request.full_url.endswith("/login"):
            return FakeResponse({"authToken": "server-token"})
        raise HTTPError(
            request.full_url,
            404,
            "not found",
            hdrs=None,
            fp=io.BytesIO(b"reference secret-reference was not found"),
        )

    with patch("xano_client.urlopen", side_effect=fake_urlopen):
        with pytest.raises(TrackingUnavailableError) as error:
            make_client().track_ticket("secret-reference")

    assert "secret-reference" not in str(error.value)


def test_ticket_issue_404_becomes_queue_unavailable_error():
    def fake_urlopen(request, timeout):
        if request.full_url.endswith("/login"):
            return FakeResponse({"authToken": "server-token"})
        raise HTTPError(request.full_url, 404, "closed", hdrs=None, fp=io.BytesIO())

    with patch("xano_client.urlopen", side_effect=fake_urlopen):
        with pytest.raises(QueueUnavailableError):
            make_client().issue_ticket(4)


def test_ticket_issue_preserves_structured_xano_error_without_exposing_secrets():
    body = json.dumps(
        {
            "code": "ERROR_CODE_INPUT_ERROR",
            "message": "Fila encerrada para emissão.",
            "accessToken": "response-secret-token",
        }
    ).encode("utf-8")

    def fake_urlopen(request, timeout):
        if request.full_url.endswith("/login"):
            return FakeResponse({"authToken": "server-token"})
        raise HTTPError(
            request.full_url,
            400,
            "bad request",
            hdrs=None,
            fp=io.BytesIO(body),
        )

    with patch("xano_client.urlopen", side_effect=fake_urlopen):
        with pytest.raises(QueueUnavailableError) as error:
            make_client().issue_ticket(4)

    assert error.value.status_code == 400
    assert error.value.api_code == "ERROR_CODE_INPUT_ERROR"
    assert error.value.api_message == "Fila encerrada para emissão."
    assert "Fila encerrada para emissão." in error.value.api_body
    assert "response-secret-token" not in error.value.api_body
    assert "[REDACTED]" in error.value.api_body


@pytest.mark.parametrize(
    ("response_body", "expected_body", "expected_message"),
    [
        (b"Xano validation failed", "Xano validation failed", "Xano validation failed"),
        (b"token=hidden-value", "token=[REDACTED]", "token=[REDACTED]"),
        (b"", None, None),
    ],
)
def test_ticket_issue_preserves_non_json_or_empty_error_body(
    response_body, expected_body, expected_message
):
    def fake_urlopen(request, timeout):
        if request.full_url.endswith("/login"):
            return FakeResponse({"authToken": "server-token"})
        raise HTTPError(
            request.full_url,
            422,
            "unprocessable",
            hdrs=None,
            fp=io.BytesIO(response_body),
        )

    with patch("xano_client.urlopen", side_effect=fake_urlopen):
        with pytest.raises(QueueUnavailableError) as error:
            make_client().issue_ticket(4)

    assert error.value.status_code == 422
    assert error.value.api_body == expected_body
    assert error.value.api_message == expected_message


def test_ticket_issue_logs_endpoint_and_status_without_query_or_credentials(caplog):
    requests = []
    client = XanoClient(
        login_url="https://xano.invalid/login",
        queues_url="https://xano.invalid/queues",
        issue_url="https://xano.invalid/issue?api_key=private-query-key",
        tracking_url="https://xano.invalid/tracking",
        email="totem@example.invalid",
        password="test-password",
    )

    def fake_urlopen(request, timeout):
        requests.append(request)
        if request.full_url.endswith("/login"):
            return FakeResponse({"authToken": "server-token"})
        raise HTTPError(
            request.full_url,
            400,
            "bad request",
            hdrs=None,
            fp=io.BytesIO(b'{"code":"QUEUE_CLOSED","message":"closed"}'),
        )

    with patch("xano_client.urlopen", side_effect=fake_urlopen):
        with caplog.at_level(logging.WARNING, logger="xano_client"):
            with pytest.raises(QueueUnavailableError):
                client.issue_ticket(4)

    assert "method=POST path=/issue status=400 api_code=QUEUE_CLOSED" in caplog.text
    assert "private-query-key" not in caplog.text
    assert "server-token" not in caplog.text
    assert "totem@example.invalid" not in caplog.text
    issue_request = requests[-1]
    assert issue_request.get_method() == "POST"
    assert json.loads(issue_request.data.decode("utf-8")) == {"fila_id": 4}
