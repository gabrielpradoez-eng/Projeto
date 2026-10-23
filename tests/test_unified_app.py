from pathlib import Path

from streamlit.testing.v1 import AppTest

from xano_client import XanoRequestError


class FakeTotemClient:
    def __init__(self):
        self.list_calls = 0

    def list_queues(self):
        self.list_calls += 1
        return [
            {
                "fila_id": 9,
                "fila_nome": "Fila principal",
                "servico_id": 4,
                "servico_nome": "Atendimento geral",
            }
        ]


class FakeDisplayClient:
    def __init__(self):
        self.fetch_calls = 0

    def fetch_snapshot(self):
        self.fetch_calls += 1
        return {
            "current_call": None,
            "history": [],
            "snapshot_at": "2026-10-23T12:00:00Z",
        }


class FakeAnalyticsClient:
    def __init__(self, options_error=None):
        self.options_requests = 0
        self.options_error = options_error

    def list_options(self):
        self.options_requests += 1
        if self.options_error:
            raise self.options_error
        return {"estabelecimentos": [], "filas": []}


def unified_app(**session_values):
    app = AppTest.from_file(
        Path(__file__).resolve().parents[1] / "app.py", default_timeout=10
    )
    for key, value in session_values.items():
        app.session_state[key] = value
    return app


def test_navigation_renders_only_the_selected_view_and_preserves_session_state():
    totem_client = FakeTotemClient()
    display_client = FakeDisplayClient()
    app = unified_app(
        _xano_client_override=totem_client,
        _display_feed_client_override=display_client,
        authToken="admin-jwt",
        user_id=42,
        establishment_id=7,
        totem_queue_id=9,
    ).run()

    assert not app.exception
    assert totem_client.list_calls == 1
    assert display_client.fetch_calls == 0
    assert app.session_state["authToken"] == "admin-jwt"
    assert app.session_state["user_id"] == 42
    assert app.session_state["establishment_id"] == 7
    assert app.session_state["totem_queue_id"] == 9

    app.radio(key="app_view").set_value("Painel TV").run()

    assert not app.exception
    assert totem_client.list_calls == 1
    assert display_client.fetch_calls == 1
    assert "Aguardando a próxima chamada" in str([item.value for item in app.info])
    assert app.session_state["authToken"] == "admin-jwt"
    assert app.session_state["user_id"] == 42
    assert app.session_state["establishment_id"] == 7
    assert app.session_state["totem_queue_id"] == 9


def test_analytics_view_preserves_separate_authentication_tokens():
    analytics_client = FakeAnalyticsClient()
    app = unified_app(
        app_view="Relatórios",
        authToken="operations-jwt",
        analytics_auth_token="analytics-jwt",
        _analytics_client_override=analytics_client,
    ).run()

    assert not app.exception
    assert analytics_client.options_requests == 1
    assert app.session_state["authToken"] == "operations-jwt"
    assert app.session_state["analytics_auth_token"] == "analytics-jwt"
    assert "analytics_report" not in app.session_state
    assert "Nenhum estabelecimento está disponível" in str(
        [item.value for item in app.info]
    )


def test_analytics_view_reports_backend_permission_denial_without_metrics():
    forbidden = XanoRequestError("forbidden")
    forbidden.status_code = 403
    analytics_client = FakeAnalyticsClient(options_error=forbidden)
    app = unified_app(
        app_view="Relatórios",
        analytics_auth_token="non-admin-token",
        _analytics_client_override=analytics_client,
    ).run()

    assert not app.exception
    assert "não tem permissão administrativa" in str(
        [item.value for item in app.error]
    )
    assert not app.metric
