from datetime import date
from pathlib import Path
from unittest.mock import patch

from streamlit.testing.v1 import AppTest

from xano_client import XanoRequestError


class FakeAnalyticsClient:
    def __init__(self, *, report=None, report_error=None, options_error=None):
        self.options = {
            "estabelecimentos": [{"id": 42, "nome": "Unidade Central"}],
            "filas": [
                {
                    "estabelecimento_id": 42,
                    "estabelecimento_nome": "Unidade Central",
                    "servico_id": 7,
                    "servico_nome": "Atendimento geral",
                    "fila_id": 13,
                    "fila_nome": "Fila principal",
                },
                {
                    "estabelecimento_id": 42,
                    "estabelecimento_nome": "Unidade Central",
                    "servico_id": 8,
                    "servico_nome": "Retirada",
                    "fila_id": 14,
                    "fila_nome": "Fila de retirada",
                }
            ],
        }
        self.report = report or {
            "generated_at": "2026-10-16T15:00:00Z",
            "filters": {
                "period_start": "2026-10-01T00:00:00Z",
                "period_end": "2026-10-08T00:00:00Z",
            },
            "summary": {
                "emitidas": 17,
                "chamadas": 12,
                "concluidas": 10,
                "espera_media_minutos": 8.5,
                "espera_amostras": 12,
                "duracao_media_minutos": 6.0,
                "duracao_amostras": 10,
                "taxa_conclusao_coorte_pct": 58.8,
                "coorte_status": {
                    "aguardando": 2,
                    "chamado": 3,
                    "concluido": 10,
                    "cancelado": 2,
                },
            },
            "daily": [
                {
                    "bucket_start": "2026-10-01T00:00:00Z",
                    "emitidas": 17,
                    "chamadas": 12,
                    "concluidas": 10,
                }
            ],
            "breakdown": [
                {
                    "servico_nome": "Atendimento geral",
                    "fila_nome": "Fila principal",
                    "emitidas": 17,
                    "chamadas": 12,
                    "concluidas": 10,
                    "espera_media_minutos": 8.5,
                    "espera_amostras": 12,
                    "duracao_media_minutos": 6.0,
                    "duracao_amostras": 10,
                    "coorte_aguardando": 2,
                    "coorte_chamado": 3,
                    "coorte_concluido": 10,
                    "coorte_cancelado": 2,
                }
            ],
        }
        self.report_error = report_error
        self.options_error = options_error
        self.requested_filters = []
        self.options_requests = 0

    def list_options(self):
        self.options_requests += 1
        if self.options_error:
            raise self.options_error
        return self.options

    def fetch_report(self, filters):
        self.requested_filters.append(filters)
        if self.report_error:
            raise self.report_error
        return self.report


def analytics_app(fake_client):
    app_path = Path(__file__).resolve().parents[1] / "analytics_app.py"
    app = AppTest.from_file(app_path, default_timeout=20)
    app.session_state["analytics_auth_token"] = "session-admin-token"
    app.session_state["_analytics_client_override"] = fake_client
    return app.run()


def test_admin_filter_form_sends_utc_range_and_selected_ids_to_xano():
    fake = FakeAnalyticsClient()
    app = analytics_app(fake)
    app.date_input(key="analytics_period_start").set_value(date(2026, 10, 1))
    app.date_input(key="analytics_period_end").set_value(date(2026, 10, 8))
    app.selectbox(key="analytics_service_id").select(7)
    app.selectbox(key="analytics_queue_id").select(13)
    app.button[1].click().run()

    assert not app.exception
    assert fake.requested_filters == [
        {
            "estabelecimento_id": 42,
            "period_start": "2026-10-01T00:00:00Z",
            "period_end": "2026-10-08T00:00:00Z",
            "servico_id": 7,
            "fila_id": 13,
        }
    ]
    assert [metric.value for metric in app.metric][:3] == ["17", "12", "10"]
    assert "8.5 min" in str([metric.value for metric in app.metric])


def test_report_is_not_requested_before_admin_submits_authorized_options():
    fake = FakeAnalyticsClient()
    app = analytics_app(fake)

    assert not app.exception
    assert fake.options_requests == 1
    assert fake.requested_filters == []
    assert app.selectbox(key="analytics_establishment_id").options == [
        "Unidade Central"
    ]


def test_queue_choices_are_limited_to_the_selected_service():
    fake = FakeAnalyticsClient()
    app = analytics_app(fake)
    app.selectbox(key="analytics_service_id").select(7)
    app.button[1].click().run()

    assert not app.exception
    assert app.selectbox(key="analytics_queue_id").options == [
        "Todas as filas",
        "Atendimento geral · Fila principal",
    ]
    assert fake.requested_filters[0]["servico_id"] == 7
    assert fake.requested_filters[0]["fila_id"] in (None, 13)


def test_no_sample_average_is_rendered_as_missing_not_zero():
    report = FakeAnalyticsClient().report
    report["summary"]["espera_media_minutos"] = None
    report["summary"]["espera_amostras"] = 0
    fake = FakeAnalyticsClient(report=report)
    app = analytics_app(fake)
    app.button[1].click().run()

    assert not app.exception
    assert "Sem amostras" in str([metric.value for metric in app.metric])
    assert "Amostras de espera: 0" in str([item.value for item in app.caption])


def test_zero_average_is_rendered_as_zero_and_empty_report_is_explicit():
    report = FakeAnalyticsClient().report
    report["summary"].update(
        emitidas=0,
        chamadas=0,
        concluidas=0,
        espera_media_minutos=0,
        espera_amostras=1,
        duracao_media_minutos=0,
        duracao_amostras=1,
        taxa_conclusao_coorte_pct=None,
        coorte_status={
            "aguardando": 0,
            "chamado": 0,
            "concluido": 0,
            "cancelado": 0,
        },
    )
    report["daily"] = []
    report["breakdown"] = []
    fake = FakeAnalyticsClient(report=report)
    app = analytics_app(fake)
    app.button[1].click().run()

    assert not app.exception
    metric_values = [metric.value for metric in app.metric]
    assert "0 min" in metric_values
    assert "Sem dados" in metric_values
    assert "Sem eventos para os filtros e período selecionados." in str(
        [item.value for item in app.info]
    )
    assert "Não há linhas de detalhamento" in str(
        [item.value for item in app.info]
    )


def test_report_failure_does_not_render_mock_or_previous_metrics():
    fake = FakeAnalyticsClient(report_error=XanoRequestError("transport detail"))
    app = analytics_app(fake)
    app.button[1].click().run()

    assert not app.exception
    assert "Não foi possível gerar o relatório" in str([item.value for item in app.error])
    assert not app.metric
    assert "transport detail" not in str([item.value for item in app.error])


def test_invalid_utc_range_clears_previous_report_and_does_not_call_xano():
    fake = FakeAnalyticsClient()
    app = analytics_app(fake)
    app.date_input(key="analytics_period_start").set_value(date(2026, 10, 9))
    app.date_input(key="analytics_period_end").set_value(date(2026, 10, 8))
    app.button[1].click().run()

    assert not app.exception
    assert fake.requested_filters == []
    assert "A data inicial deve ser anterior" in str([item.value for item in app.error])
    assert not app.metric


def test_options_service_failure_shows_sanitized_error_without_report():
    fake = FakeAnalyticsClient(options_error=XanoRequestError("private transport detail"))
    app = analytics_app(fake)

    assert not app.exception
    assert "Não foi possível carregar as opções analíticas" in str(
        [item.value for item in app.error]
    )
    assert "private transport detail" not in str([item.value for item in app.error])
    assert not app.metric
    assert fake.requested_filters == []


def test_missing_xano_configuration_is_reported_without_metrics():
    app_path = Path(__file__).resolve().parents[1] / "analytics_app.py"
    app = AppTest.from_file(app_path, default_timeout=10)
    app.session_state["analytics_auth_token"] = "session-admin-token"
    with patch("streamlit.secrets", {}):
        app.run()

    assert not app.exception
    assert "integração analítica com Xano não está configurada" in str(
        [item.value for item in app.error]
    )
    assert not app.metric


def test_empty_authorized_establishment_options_stop_before_report_form():
    fake = FakeAnalyticsClient()
    fake.options["estabelecimentos"] = []
    app = analytics_app(fake)

    assert not app.exception
    assert "Nenhum estabelecimento está disponível" in str(
        [item.value for item in app.info]
    )
    assert not app.selectbox
    assert fake.requested_filters == []


def test_breakdown_renders_only_aggregated_fields_in_backend_order():
    report = FakeAnalyticsClient().report
    report["breakdown"] = [
        {
            "servico_nome": "Retirada",
            "fila_nome": "Fila B",
            "emitidas": 2,
            "chamadas": 1,
            "concluidas": 1,
            "cliente_nome": "Dado pessoal",
            "ticket_id": 901,
        },
        {
            "servico_nome": "Atendimento geral",
            "fila_nome": "Fila A",
            "emitidas": 1,
            "chamadas": 1,
            "concluidas": 0,
        },
    ]
    app = analytics_app(FakeAnalyticsClient(report=report))
    app.button[1].click().run()

    assert not app.exception
    rendered_rows = app.table[0].value
    assert list(rendered_rows["fila_nome"]) == ["Fila B", "Fila A"]
    assert "Dado pessoal" not in str(rendered_rows)
    assert "ticket_id" not in str(rendered_rows)


def test_login_page_is_rendered_without_session_token():
    app_path = Path(__file__).resolve().parents[1] / "analytics_app.py"
    app = AppTest.from_file(app_path, default_timeout=20).run()

    assert not app.exception
    assert "Relatórios de atendimento" in str([item.value for item in app.title])
    assert len(app.text_input) == 2
    assert not app.metric