from pathlib import Path

from streamlit.testing.v1 import AppTest

from xano_client import (
    QueueUnavailableError,
    TrackingUnavailableError,
    XanoRequestError,
)


class FakeXanoClient:
    def __init__(self, *, track_result=None, track_error=None, issue_error=None):
        self.track_result = track_result or {
            "numero": 5,
            "servico": "Atendimento geral",
            "fila": "Fila principal",
            "status": "aguardando",
            "posicao": 2,
            "tempo_estimado_min": 10,
            "atualizado_at": "2026-10-06T12:00:00Z",
        }
        self.track_error = track_error
        self.issue_error = issue_error
        self.list_calls = 0
        self.issued_queue_ids = []
        self.tracked_references = []

    def list_queues(self):
        self.list_calls += 1
        return [{
            "fila_id": 9,
            "fila_nome": "Fila principal",
            "servico_id": 4,
            "servico_nome": "Atendimento geral",
            "tempo_estimado_min": 5,
        }]

    def issue_ticket(self, queue_id):
        self.issued_queue_ids.append(queue_id)
        if self.issue_error:
            raise self.issue_error
        return {"numero": 22, "referencia_rastreamento": "issued-reference"}

    def track_ticket(self, reference):
        self.tracked_references.append(reference)
        if self.track_error:
            raise self.track_error
        return self.track_result


def kiosk_app(fake_client):
    app = AppTest.from_file(
        Path(__file__).resolve().parents[1] / "kiosk_app.py", default_timeout=10
    )
    app.session_state["_xano_client_override"] = fake_client
    return app.run()


def test_totem_lists_backend_options_and_confirms_issue():
    fake_client = FakeXanoClient()
    app = kiosk_app(fake_client)

    assert not app.exception
    assert fake_client.list_calls == 1
    assert app.selectbox[0].value == 9
    app.button[1].click().run()

    assert not app.exception
    assert fake_client.issued_queue_ids == [9]
    assert app.session_state["ticket_number"] == 22
    assert app.session_state["ticket_reference"] == "issued-reference"


def test_tracking_page_displays_backend_status_and_position():
    fake_client = FakeXanoClient()
    app = kiosk_app(fake_client)
    app.session_state["tracking_active"] = True
    app.session_state["ticket_reference"] = "customer-reference"
    app.switch_page("app_pages/tracking.py").run()

    assert not app.exception
    assert fake_client.tracked_references == ["customer-reference"]
    assert "Atendimento geral" in str([item.value for item in app.markdown])
    assert str([item.value for item in app.metric]).find("2") >= 0


def test_closed_queue_rejection_does_not_show_a_ticket_confirmation():
    fake_client = FakeXanoClient(issue_error=QueueUnavailableError())
    app = kiosk_app(fake_client)
    app.button[1].click().run()

    assert not app.exception
    assert app.warning
    assert "deixou de estar disponível" in app.warning[0].value
    assert "ticket_reference" not in app.session_state


def test_invalid_reference_ends_tracking_without_leaking_reference():
    fake_client = FakeXanoClient(track_error=TrackingUnavailableError())
    app = kiosk_app(fake_client)
    app.session_state["tracking_active"] = True
    app.session_state["ticket_reference"] = "private-reference"
    app.switch_page("app_pages/tracking.py").run()

    assert not app.exception
    assert app.session_state["tracking_ended"] is True
    assert "encerrado" in str([item.value for item in app.info]).lower()
    visible_text = str(
        [
            item.value
            for collection in (app.markdown, app.caption, app.info, app.warning, app.error)
            for item in collection
        ]
    )
    assert "private-reference" not in visible_text


def test_temporary_failure_keeps_last_confirmed_data_and_marks_it_stale():
    fake_client = FakeXanoClient(track_error=XanoRequestError("network"))
    app = kiosk_app(fake_client)
    app.session_state["tracking_active"] = True
    app.session_state["ticket_reference"] = "private-reference"
    app.session_state["tracking_result"] = fake_client.track_result
    app.switch_page("app_pages/tracking.py").run()

    assert not app.exception
    assert "desconhecido" in str([item.value for item in app.warning]).lower()
    assert "Última atualização confirmada" in str([item.value for item in app.caption])


def test_new_totem_session_clears_previous_customer_data():
    fake_client = FakeXanoClient()
    app = kiosk_app(fake_client)
    app.session_state["ticket_reference"] = "previous-reference"
    app.session_state["ticket_number"] = 21
    app.session_state["tracking_result"] = fake_client.track_result
    app.button[0].click().run()

    assert not app.exception
    assert "ticket_reference" not in app.session_state
    assert "ticket_number" not in app.session_state
    assert "tracking_result" not in app.session_state