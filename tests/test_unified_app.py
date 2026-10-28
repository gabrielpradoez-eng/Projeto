import io
import json
from pathlib import Path
from unittest.mock import patch
from urllib.error import HTTPError

from streamlit.testing.v1 import AppTest

from xano_client import QueueUnavailableError, XanoClient, XanoRequestError
from views.issue_error import render_ticket_issue_error


class FakeResponse:
    def __init__(self, payload):
        self.body = json.dumps(payload).encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return False

    def read(self):
        return self.body


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


def test_admin_login_does_not_display_local_sample_users(monkeypatch):
    import app as unified_app_module

    class LocalSamples:
        users = {
            1: type(
                "SampleUser",
                (),
                {
                    "name": "Sample Admin",
                    "role": "admin",
                    "email": "sample-admin@example.invalid",
                },
            )()
        }

    monkeypatch.setattr(
        unified_app_module, "_admin_login_defaults", lambda: ("", "")
    )
    app = unified_app(
        app_view="Administração",
        backend=LocalSamples(),
    ).run()

    assert not app.exception
    assert any(field.label == "E-mail" for field in app.text_input)
    assert any(field.label == "Senha" for field in app.text_input)
    rendered_text = " ".join(str(element.value) for element in app.markdown)
    assert "Usuários de exemplo" not in rendered_text
    assert "sample-admin@example.invalid" not in rendered_text


def test_admin_view_stores_authenticated_xano_identity(monkeypatch):
    import app as unified_app_module
    from backend_queue import QueueBackend

    backend = QueueBackend()
    backend.authenticate = lambda _email, _password: {
        "id": 987,
        "user_id": 987,
        "name": "Remote Admin",
        "email": "admin@example.com",
        "role": "admin",
        "establishment_id": None,
        "authToken": "remote-auth-token",
    }
    monkeypatch.setattr(
        unified_app_module, "_admin_login_defaults", lambda: ("", "")
    )
    app = unified_app(
        app_view="Administração",
        backend=backend,
    ).run()

    next(field for field in app.text_input if field.label == "E-mail").set_value(
        "admin@example.com"
    )
    next(field for field in app.text_input if field.label == "Senha").set_value(
        "test-password"
    )
    next(button for button in app.button if button.label == "Entrar").click().run()

    assert not app.exception
    assert app.session_state["user"]["id"] == 987
    assert app.session_state["user"]["role"] == "admin"
    assert app.session_state["authToken"] == "remote-auth-token"
    assert app.session_state["user_id"] == 987


def test_admin_view_does_not_create_session_from_invalid_xano_identity(monkeypatch):
    import app as unified_app_module
    from backend_queue import AccessDeniedError, QueueBackend

    backend = QueueBackend()

    def reject_login(_email, _password):
        raise AccessDeniedError("Resposta de autenticação inválida.")

    backend.authenticate = reject_login
    monkeypatch.setattr(
        unified_app_module, "_admin_login_defaults", lambda: ("", "")
    )
    app = unified_app(
        app_view="Administração",
        backend=backend,
    ).run()

    next(field for field in app.text_input if field.label == "E-mail").set_value(
        "admin@example.com"
    )
    next(field for field in app.text_input if field.label == "Senha").set_value(
        "test-password"
    )
    next(button for button in app.button if button.label == "Entrar").click().run()

    assert not app.exception
    assert app.session_state["user"] is None
    assert "authToken" not in app.session_state
    assert "Resposta de autenticação inválida." in str(
        [item.value for item in app.error]
    )


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


def test_totem_issue_posts_the_xano_contract_and_renders_confirmed_ticket():
    requests = []
    responses = [
        {"authToken": "totem-token", "user_id": 19},
        [
            {
                "fila_id": 9,
                "fila_nome": "Fila principal",
                "servico_id": 4,
                "servico_nome": "Atendimento geral",
            }
        ],
        [
            {
                "fila_id": 9,
                "fila_nome": "Fila principal",
                "servico_id": 4,
                "servico_nome": "Atendimento geral",
            }
        ],
        {
            "numero": 23,
            "status": "aguardando",
            "referencia_rastreamento": "opaque-reference",
            "expira_at": "2026-10-24T12:00:00Z",
        },
    ]

    def fake_urlopen(request, timeout):
        requests.append(request)
        assert timeout == 8.0
        return FakeResponse(responses.pop(0))

    client = XanoClient(
        login_url="https://xano.invalid/auth/login",
        queues_url="https://xano.invalid/totem/queues",
        issue_url="https://xano.invalid/totem/issue",
        tracking_url="https://xano.invalid/tracking",
        email="totem@example.invalid",
        password="local-test-password",
    )
    app = unified_app(_xano_client_override=client)

    with patch("xano_client.urlopen", side_effect=fake_urlopen):
        app.run()
        app.button[1].click().run()

    assert not app.exception
    assert len(requests) == 4
    login_request, first_queue_request, queue_request, issue_request = requests
    assert login_request.full_url.endswith("/auth/login")
    assert json.loads(login_request.data.decode("utf-8")) == {
        "email": "totem@example.invalid",
        "field_value": "totem@example.invalid",
        "password": "local-test-password",
    }
    assert first_queue_request.full_url.endswith("/totem/queues")
    assert queue_request.full_url.endswith("/totem/queues")
    assert issue_request.full_url.endswith("/totem/issue")
    assert issue_request.get_method() == "POST"
    assert issue_request.get_header("Authorization") == "Bearer totem-token"
    assert json.loads(issue_request.data.decode("utf-8")) == {"fila_id": 9}
    assert app.session_state["ticket_number"] == 23
    assert app.session_state["ticket_reference"] == "opaque-reference"
    assert "Senha confirmada: 23" in str([item.value for item in app.success])


def test_totem_shows_xano_status_and_message_when_ticket_issue_is_rejected():
    requests = []
    queue_response = [
        {
            "fila_id": 9,
            "fila_nome": "Fila principal",
            "servico_id": 4,
            "servico_nome": "Atendimento geral",
        }
    ]

    def fake_urlopen(request, timeout):
        requests.append(request)
        if request.full_url.endswith("/auth/login"):
            return FakeResponse({"authToken": "totem-token", "user_id": 19})
        if request.full_url.endswith("/totem/queues"):
            return FakeResponse(queue_response)
        raise HTTPError(
            request.full_url,
            400,
            "Bad Request",
            hdrs=None,
            fp=io.BytesIO(
                b'{"code":"ERROR_CODE_INPUT_ERROR",'
                b'"message":"Esta fila est\\u00e1 fechada no momento."}'
            ),
        )

    client = XanoClient(
        login_url="https://xano.invalid/auth/login",
        queues_url="https://xano.invalid/totem/queues",
        issue_url="https://xano.invalid/totem/issue",
        tracking_url="https://xano.invalid/tracking",
        email="totem@example.invalid",
        password="local-test-password",
    )
    app = unified_app(_xano_client_override=client)
    with patch("xano_client.urlopen", side_effect=fake_urlopen):
        app.run()
        app.button[1].click().run()

    assert not app.exception
    issue_request = requests[-1]
    assert issue_request.full_url.endswith("/totem/issue")
    assert json.loads(issue_request.data.decode("utf-8")) == {"fila_id": 9}
    assert any(
        "HTTP 400" in item.value
        and "Esta fila está fechada no momento." in item.value
        for item in app.error
    )
    assert "ERROR_CODE_INPUT_ERROR" in str([item.value for item in app.code])
    assert "Esta fila está fechada no momento." in str(
        [item.value for item in app.code]
    )
    assert "ticket_reference" not in app.session_state


def test_public_client_view_issues_and_tracks_ticket_with_server_side_xano_client():
    requests = []
    queues = [
        {
            "fila_id": 9,
            "fila_nome": "Fila principal",
            "servico_id": 4,
            "servico_nome": "Atendimento geral",
        }
    ]

    def fake_urlopen(request, timeout):
        requests.append(request)
        if request.full_url.endswith("/auth/login"):
            return FakeResponse({"authToken": "server-totem-token", "user_id": 19})
        if request.full_url.endswith("/totem/queues"):
            return FakeResponse(queues)
        if request.full_url.endswith("/totem/issue"):
            return FakeResponse(
                {
                    "numero": 24,
                    "status": "aguardando",
                    "referencia_rastreamento": "private-tracking-reference",
                }
            )
        if request.full_url.endswith("/tracking"):
            return FakeResponse(
                {
                    "numero": 24,
                    "fila": "Fila principal",
                    "servico": "Atendimento geral",
                    "status": "aguardando",
                    "posicao": 2,
                    "tempo_estimado_min": 10,
                    "atualizado_at": "2026-10-23T20:00:00Z",
                }
            )
        raise AssertionError(f"Unexpected Xano URL: {request.full_url}")

    client = XanoClient(
        login_url="https://xano.invalid/auth/login",
        queues_url="https://xano.invalid/totem/queues",
        issue_url="https://xano.invalid/totem/issue",
        tracking_url="https://xano.invalid/tracking",
        email="totem@example.invalid",
        password="local-test-password",
    )
    app = unified_app(
        app_view="Cliente",
        _xano_client_override=client,
        authToken="admin-token-must-not-be-used",
    )

    with patch("xano_client.urlopen", side_effect=fake_urlopen):
        app.run()
        assert app.radio(key="app_view").value == "Cliente"
        assert "Cliente" in app.radio(key="app_view").options
        next(
            button for button in app.button if button.label == "Emitir senha"
        ).click().run()

        assert not app.exception
        assert app.session_state["client_ticket_number"] == 24
        assert app.session_state["client_ticket_reference"] == (
            "private-tracking-reference"
        )
        assert app.session_state["client_tracking_result"]["posicao"] == 2
        assert app.session_state["authToken"] == "admin-token-must-not-be-used"
        assert "2" in str([metric.value for metric in app.metric])

        rendered = str(
            [
                element.value
                for collection in (
                    app.title,
                    app.header,
                    app.subheader,
                    app.markdown,
                    app.caption,
                    app.info,
                    app.warning,
                    app.error,
                )
                for element in collection
            ]
        )
        assert "private-tracking-reference" not in rendered
        assert "local-test-password" not in rendered

        login_request = next(
            request for request in requests if request.full_url.endswith("/auth/login")
        )
        issue_request = next(
            request for request in requests if request.full_url.endswith("/totem/issue")
        )
        tracking_request = next(
            request for request in requests if request.full_url.endswith("/tracking")
        )
        assert json.loads(login_request.data.decode("utf-8")) == {
            "email": "totem@example.invalid",
            "field_value": "totem@example.invalid",
            "password": "local-test-password",
        }
        assert issue_request.get_method() == "POST"
        assert issue_request.get_header("Authorization") == "Bearer server-totem-token"
        assert json.loads(issue_request.data.decode("utf-8")) == {"fila_id": 9}
        assert tracking_request.get_method() == "POST"
        assert tracking_request.get_header("Authorization") == "Bearer server-totem-token"
        assert json.loads(tracking_request.data.decode("utf-8")) == {
            "referencia": "private-tracking-reference"
        }
        assert all("private-tracking-reference" not in request.full_url for request in requests)

        next(
            button
            for button in app.button
            if button.label == "Iniciar novo atendimento"
        ).click().run()

    assert not app.exception
    assert "client_ticket_reference" not in app.session_state
    assert "client_ticket_number" not in app.session_state
    assert "client_tracking_result" not in app.session_state
    assert "Emitir senha" in str([button.label for button in app.button])


def test_public_client_view_reports_xano_issue_rejection_without_confirming_ticket():
    queues = [
        {
            "fila_id": 9,
            "fila_nome": "Fila principal",
            "servico_id": 4,
            "servico_nome": "Atendimento geral",
        }
    ]

    def fake_urlopen(request, timeout):
        if request.full_url.endswith("/auth/login"):
            return FakeResponse({"authToken": "server-totem-token", "user_id": 19})
        if request.full_url.endswith("/totem/queues"):
            return FakeResponse(queues)
        raise HTTPError(
            request.full_url,
            400,
            "Bad Request",
            hdrs=None,
            fp=io.BytesIO(
                b'{"code":"ERROR_CODE_INPUT_ERROR",'
                b'"message":"Esta fila est\\u00e1 fechada no momento."}'
            ),
        )

    client = XanoClient(
        login_url="https://xano.invalid/auth/login",
        queues_url="https://xano.invalid/totem/queues",
        issue_url="https://xano.invalid/totem/issue",
        tracking_url="https://xano.invalid/tracking",
        email="totem@example.invalid",
        password="local-test-password",
    )
    app = unified_app(app_view="Cliente", _xano_client_override=client)

    with patch("xano_client.urlopen", side_effect=fake_urlopen):
        app.run()
        next(
            button for button in app.button if button.label == "Emitir senha"
        ).click().run()

    assert not app.exception
    assert any(
        "HTTP 400" in item.value
        and "Esta fila está fechada no momento." in item.value
        for item in app.error
    )
    assert "ERROR_CODE_INPUT_ERROR" in str([item.value for item in app.code])
    assert "Esta fila está fechada no momento." in str(
        [item.value for item in app.code]
    )
    assert not app.success
    assert "client_ticket_reference" not in app.session_state


def test_ticket_issue_error_shows_clear_fallback_when_xano_body_is_empty():
    error = QueueUnavailableError(status_code=404)
    with (
        patch("views.issue_error.st.error") as show_error,
        patch("views.issue_error.st.caption") as show_caption,
    ):
        render_ticket_issue_error(error)

    show_error.assert_called_once_with("Xano recusou a emissão (HTTP 404)")
    show_caption.assert_called_once_with(
        "O Xano não forneceu detalhes adicionais no corpo da resposta."
    )


def test_public_client_view_retains_last_confirmed_tracking_result_on_temporary_error():
    class TemporaryTrackingFailureClient:
        def __init__(self):
            self.tracking_calls = 0

        def list_queues(self):
            return [
                {
                    "fila_id": 9,
                    "fila_nome": "Fila principal",
                    "servico_id": 4,
                    "servico_nome": "Atendimento geral",
                }
            ]

        def issue_ticket(self, queue_id):
            assert queue_id == 9
            return {
                "numero": 25,
                "referencia_rastreamento": "opaque-reference",
            }

        def track_ticket(self, reference):
            assert reference == "opaque-reference"
            self.tracking_calls += 1
            if self.tracking_calls > 1:
                raise XanoRequestError("temporarily unavailable")
            return {
                "status": "aguardando",
                "posicao": 3,
                "tempo_estimado_min": 12,
                "atualizado_at": "2026-10-23T20:00:00Z",
            }

    client = TemporaryTrackingFailureClient()
    app = unified_app(
        app_view="Cliente",
        _xano_client_override=client,
        authToken="admin-token",
    )

    app.run()
    next(
        button for button in app.button if button.label == "Emitir senha"
    ).click().run()
    confirmed_result = app.session_state["client_tracking_result"]
    assert confirmed_result["posicao"] == 3

    app.run()

    assert not app.exception
    assert app.session_state["client_tracking_result"] == confirmed_result
    assert any("última atualização confirmada" in item.value for item in app.warning)
    assert app.session_state["client_ticket_reference"] == "opaque-reference"
    assert app.session_state["authToken"] == "admin-token"


def test_public_client_view_clears_previous_session_when_no_queues_are_available():
    class EmptyQueueClient:
        def list_queues(self):
            return []

    app = unified_app(
        app_view="Cliente",
        _xano_client_override=EmptyQueueClient(),
        client_queue_id=9,
        client_ticket_reference="old-reference",
        client_ticket_number=26,
        client_tracking_result={"status": "aguardando"},
    ).run()

    assert not app.exception
    assert "Não há filas disponíveis" in str([item.value for item in app.info])
    assert not any(button.label == "Emitir senha" for button in app.button)
    assert "client_ticket_reference" not in app.session_state
    assert "client_ticket_number" not in app.session_state
    assert "client_tracking_result" not in app.session_state


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


def test_attendant_completes_remote_ticket_after_starting_a_new_session():
    from unittest.mock import Mock
    from backend_queue import QueueBackend

    backend = QueueBackend()
    remote_rows = [{"id": 9, "nome": "Fila remota", "total_aguardando": 2,
                    "em_atendimento": {"id": 57, "numero": 23}}]
    backend.get_attendant_dashboard = Mock(side_effect=[remote_rows, remote_rows, []])
    backend.complete_service = Mock(return_value={"id": 57, "number": 23, "status": "completed"})
    app = unified_app(app_view="Administração", backend=backend, user={
        "id": 42, "user_id": 42, "name": "Atendente", "role": "attendant", "authToken": "operation-token"
    }).run()
    assert not app.exception
    assert any("23" in str(item.value) for item in app.markdown)
    assert not next(button for button in app.button if button.label == "Finalizar atendimento atual").disabled
    next(button for button in app.button if button.label == "Finalizar atendimento atual").click().run()
    assert not app.exception
    backend.complete_service.assert_called_once_with(57, 42, token="operation-token")
    assert not backend.tickets


def test_admin_form_does_not_prefill_server_bootstrap_credentials():
    app = unified_app(app_view="Administração", backend=object())
    app.secrets["xano_seed"] = {
        "admin_email": "private-admin@example.invalid",
        "admin_password": "private-bootstrap-test-value",
    }
    app.run()
    assert not app.exception
    assert all(field.value == "" for field in app.text_input)
    assert all("private-bootstrap-test-value" not in str(element.value) for element in app.markdown)
