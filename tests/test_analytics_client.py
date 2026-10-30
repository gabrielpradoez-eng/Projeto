import copy
import json
from unittest.mock import Mock, patch

import pytest

from analytics_client import AnalyticsClient
from xano_client import XanoRequestError


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
        "summary": {"emitidas": 3, "chamadas": 2, "concluidas": 1},
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

def analytics_client_with_response(payload):
    client = AnalyticsClient(options_url="https://xano.invalid/options", report_url="https://xano.invalid/report", auth_token="admin-token")
    client._authorized_request = Mock(return_value=payload)
    return client


VALID_OPTIONS = {
    "estabelecimentos": [{"id": 1, "nome": "Unidade"}],
    "filas": [{"estabelecimento_id": 1, "servico_id": 2, "servico_nome": "Serviço", "fila_id": 3, "fila_nome": "Fila"}],
}


@pytest.mark.parametrize("section,row", [
    ("estabelecimentos", None),
    ("estabelecimentos", {"nome": "Sem ID"}),
    ("estabelecimentos", {"id": True, "nome": "ID booleano"}),
    ("estabelecimentos", {"id": 1, "nome": " "}),
    ("filas", {"fila_id": 3}),
    ("filas", {"estabelecimento_id": 99, "servico_id": 2, "servico_nome": "Serviço", "fila_id": 3, "fila_nome": "Fila"}),
])
def test_malformed_options_are_rejected_before_any_widget(section, row):
    payload = copy.deepcopy(VALID_OPTIONS)
    payload[section] = [row]
    with pytest.raises(XanoRequestError):
        analytics_client_with_response(payload).list_options()


@pytest.mark.parametrize("section", ["estabelecimentos", "filas"])
def test_duplicate_option_identities_are_rejected(section):
    payload = copy.deepcopy(VALID_OPTIONS)
    payload[section].append(copy.deepcopy(payload[section][0]))
    with pytest.raises(XanoRequestError):
        analytics_client_with_response(payload).list_options()


def valid_report():
    return {
        "filters": {"estabelecimento_id": 1, "period_start": 1790812800000, "period_end": 1791417600000},
        "generated_at": 1791417600000,
        "summary": {"emitidas": 3, "chamadas": 2, "concluidas": 1, "espera_media_minutos": None, "duracao_media_minutos": 0, "taxa_conclusao_coorte_pct": 33.3},
        "daily": [{"bucket_start": 1790812800000, "emitidas": 3, "chamadas": 2, "concluidas": 1}],
        "breakdown": [{"servico_nome": "Serviço", "fila_nome": "Fila", "emitidas": 3, "chamadas": 2, "concluidas": 1}],
    }


@pytest.mark.parametrize("section,key,value", [
    ("summary", "emitidas", -1),
    ("summary", "chamadas", "2"),
    ("summary", "concluidas", True),
    ("summary", "espera_media_minutos", float("nan")),
    ("summary", "duracao_media_minutos", float("inf")),
    ("summary", "taxa_conclusao_coorte_pct", 101),
    ("summary", "coorte_status", []),
    ("summary", "espera_amostras", -1),
    ("filters", "period_start", None),
    ("filters", "estabelecimento_id", 99),
    ("filters", "servico_id", 99),
    ("filters", "fila_id", False),
    ("filters", "period_end", float("nan")),
])
def test_invalid_report_values_are_not_presented_as_metrics(section, key, value):
    payload = valid_report()
    payload[section][key] = value
    with pytest.raises(XanoRequestError):
        analytics_client_with_response(payload).fetch_report({"estabelecimento_id": 1})


@pytest.mark.parametrize("collection,row", [("daily", "invalid"), ("daily", {"emitidas": 1, "chamadas": 1, "concluidas": 0}), ("breakdown", None), ("breakdown", {"emitidas": 1, "chamadas": 1, "concluidas": 0})])
def test_malformed_report_rows_are_rejected(collection, row):
    payload = valid_report()
    payload[collection] = [row]
    with pytest.raises(XanoRequestError):
        analytics_client_with_response(payload).fetch_report({"estabelecimento_id": 1})


def test_numeric_xano_timestamps_and_null_or_zero_averages_are_preserved():
    payload = valid_report()
    assert analytics_client_with_response(payload).fetch_report({"estabelecimento_id": 1}) == payload
