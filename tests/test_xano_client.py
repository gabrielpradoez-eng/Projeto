import io
import json
from urllib.error import HTTPError
from unittest.mock import patch

import pytest

from xano_client import QueueUnavailableError, TrackingUnavailableError, XanoClient


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


def test_login_is_cached_and_requests_use_bearer_token():
    requests = []
    responses = [
        {"authToken": "server-token"},
        [{"fila_id": 7, "fila_nome": "Geral"}],
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
        "password": "server-only-password",
    }
    assert requests[1].get_header("Authorization") == "Bearer server-token"
    assert requests[2].get_header("Authorization") == "Bearer server-token"


def test_tracking_reference_is_sent_in_post_body_not_url():
    requests = []
    responses = [
        {"authToken": "server-token"},
        {"numero": 12, "status": "aguardando", "posicao": 2},
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