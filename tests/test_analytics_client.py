import json
from unittest.mock import patch

from analytics_client import AnalyticsClient


class FakeResponse:
    def __init__(self, payload):
        self.body = json.dumps(payload).encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return False

    def read(self):
        return self.body


def test_individual_admin_login_token_authorizes_options_and_report_requests():
    requests = []
    report_filters = {
        "estabelecimento_id": 4,
        "period_start": "2026-10-01T00:00:00Z",
        "period_end": "2026-10-08T00:00:00Z",
        "servico_id": None,
        "fila_id": None,
    }
    report = {
        "summary": {"emitidas": 3},
        "daily": [],
        "breakdown": [],
        "generated_at": "2026-10-08T00:00:00Z",
        "filters": report_filters,
    }
    responses = [
        {"authToken": "admin-token"},
        {"estabelecimentos": [{"id": 4, "nome": "Centro"}], "filas": []},
        report,
    ]

    def fake_urlopen(request, timeout):
        requests.append(request)
        assert timeout == 10.0
        return FakeResponse(responses.pop(0))

    with patch("analytics_client.urlopen", side_effect=fake_urlopen):
        token = AnalyticsClient.authenticate(
            "https://xano.invalid/login",
            "report-admin@example.invalid",
            "user-password",
        )
        client = AnalyticsClient(
            options_url="https://xano.invalid/analytics/options",
            report_url="https://xano.invalid/analytics/report",
            auth_token=token,
        )
        assert client.list_options()["estabelecimentos"][0]["id"] == 4
        assert client.fetch_report(report_filters) == report

    assert len(requests) == 3
    assert requests[1].get_header("Authorization") == "Bearer admin-token"
    assert requests[2].get_header("Authorization") == "Bearer admin-token"
    assert json.loads(requests[0].data.decode("utf-8")) == {
        "email": "report-admin@example.invalid",
        "password": "user-password",
    }
    assert json.loads(requests[2].data.decode("utf-8")) == report_filters
    assert "server-secret" not in requests[2].full_url
    assert "user-password" not in requests[2].full_url