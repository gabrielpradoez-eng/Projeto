import json
from pathlib import Path
from unittest.mock import patch

from streamlit.testing.v1 import AppTest

from views.display_view import REFRESH_INTERVALS_SECONDS, _refresh_interval
from xano_client import DisplayFeedClient, XanoRequestError


class FakeResponse:
    def __init__(self, payload):
        self.body = json.dumps(payload).encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return False

    def read(self):
        return self.body


class FakeDisplayClient:
    def __init__(self, snapshots):
        self.snapshots = list(snapshots)

    def fetch_snapshot(self):
        result = self.snapshots.pop(0)
        if isinstance(result, Exception):
            raise result
        return result


def snapshot(event_key, number, history=None):
    current_call = None
    if event_key is not None:
        current_call = {
            "event_key": event_key,
            "numero": number,
            "destino": "Guichê 2",
            "chamado_at": "2026-10-06T10:00:00Z",
        }
    return {
        "current_call": current_call,
        "history": history or [],
        "snapshot_at": "2026-10-06T10:00:00Z",
    }


def display_app(fake_client):
    app_path = Path(__file__).resolve().parents[1] / "tv_display_app.py"
    app = AppTest.from_file(app_path, default_timeout=10)
    app.session_state["_display_feed_client_override"] = fake_client
    return app.run()


def test_feed_client_sends_scoped_credential_in_post_body_not_url():
    requests = []
    expected = snapshot("event-1", 31)

    def fake_urlopen(request, timeout):
        requests.append(request)
        assert timeout == 5.0
        return FakeResponse(expected)

    with patch("xano_client.urlopen", side_effect=fake_urlopen):
        result = DisplayFeedClient(
            feed_url="https://xano.invalid/tv/feed",
            credential="display-secret",
        ).fetch_snapshot()

    assert result == expected
    request = requests[0]
    assert request.get_method() == "POST"
    assert "display-secret" not in request.full_url
    assert json.loads(request.data.decode("utf-8")) == {"credential": "display-secret"}


def test_initial_snapshot_renders_current_and_backend_order_without_new_call_alert():
    older = {
        "event_key": "event-old",
        "numero": 29,
        "destino": "Guichê 1",
        "chamado_at": "2026-10-06T09:58:00Z",
    }
    app = display_app(FakeDisplayClient([snapshot("event-current", 31, [older])]))

    assert not app.exception
    assert [metric.value for metric in app.metric] == ["31"]
    assert not app.success
    rendered = str([item.value for item in app.markdown])
    assert rendered.index("Senha 29") < rendered.index("Guichê 1")


def test_new_event_is_signaled_once_and_duplicate_poll_is_not_signaled_again():
    fake = FakeDisplayClient(
        [
            snapshot("event-1", 31),
            snapshot("event-2", 32),
            snapshot("event-2", 32),
        ]
    )
    app = display_app(fake)
    assert not app.success

    app.run()
    assert not app.exception
    assert [item.value for item in app.success] == ["Nova chamada"]

    app.run()
    assert not app.exception
    assert not app.success


def test_audio_alert_requires_explicit_activation_and_plays_once_for_new_event():
    fake = FakeDisplayClient(
        [snapshot("event-1", 31), snapshot("event-2", 32), snapshot("event-2", 32)]
    )
    app = display_app(fake)
    app.toggle(key="tv_sound_enabled").set_value(True).run()

    assert not app.exception
    assert [item.value for item in app.success] == ["Nova chamada"]
    audio_elements = app.get("audio")
    assert len(audio_elements) == 1
    assert audio_elements[0].proto.autoplay is True

    app.run()
    assert not app.exception
    assert not app.success
    assert not app.get("audio")


def test_empty_snapshot_renders_empty_call_and_history():
    app = display_app(FakeDisplayClient([snapshot(None, None)]))

    assert not app.exception
    assert "Aguardando a próxima chamada" in str([item.value for item in app.info])
    assert "Nenhuma chamada anterior" in str([item.value for item in app.caption])


def test_history_is_truncated_to_five_without_reordering_backend_items():
    history = [
        {
            "event_key": f"history-{index}",
            "numero": 40 - index,
            "destino": f"Guichê {index}",
            "chamado_at": f"2026-10-06T09:{index:02d}:00Z",
        }
        for index in range(6)
    ]
    app = display_app(FakeDisplayClient([snapshot("current", 50, history)]))

    assert not app.exception
    rendered = str([item.value for item in app.markdown])
    for expected_number in range(40, 35, -1):
        assert f"Senha {expected_number}" in rendered
    assert "Senha 35" not in rendered
    assert rendered.index("Senha 40") < rendered.index("Senha 39")


def test_temporary_feed_failure_keeps_last_snapshot_visibly_stale():
    fake = FakeDisplayClient(
        [snapshot("event-1", 31), XanoRequestError("private transport detail")]
    )
    app = display_app(fake)
    app.run()

    assert not app.exception
    assert [metric.value for metric in app.metric] == ["31"]
    assert "desatualizado" in str([item.value for item in app.warning]).lower()
    assert "private transport detail" not in str([item.value for item in app.warning])


def test_successful_reused_snapshot_is_not_misclassified_as_stale():
    same_snapshot = snapshot("event-1", 31)
    app = display_app(FakeDisplayClient([same_snapshot, same_snapshot]))
    app.run()

    assert not app.exception
    assert not app.warning
    assert [metric.value for metric in app.metric] == ["31"]


def test_refresh_interval_uses_allowed_presets_and_defaults_invalid_values():
    assert REFRESH_INTERVALS_SECONDS == (3, 5, 10, 15, 30, 60)
    assert _refresh_interval(5).total_seconds() == 5
    assert _refresh_interval(30).total_seconds() == 30
    assert _refresh_interval(7).total_seconds() == 5


def test_changing_refresh_interval_preserves_snapshot_and_does_not_repeat_alert():
    fake = FakeDisplayClient(
        [
            snapshot("event-1", 31),
            snapshot("event-2", 32),
            snapshot("event-2", 32),
        ]
    )
    app = display_app(fake)
    assert app.selectbox(key="tv_refresh_interval_seconds").value == 5

    app.run()
    assert [item.value for item in app.success] == ["Nova chamada"]
    assert [metric.value for metric in app.metric] == ["32"]

    app.selectbox(key="tv_refresh_interval_seconds").set_value(10).run()

    assert not app.exception
    assert app.session_state["tv_refresh_interval_seconds"] == 10
    assert app.session_state["tv_last_snapshot"]["current_call"]["event_key"] == "event-2"
    assert [metric.value for metric in app.metric] == ["32"]
    assert not app.success

def test_feed_client_normalizes_real_xano_millisecond_timestamps():
    data = snapshot("event-ms", 4)
    data["snapshot_at"] = 1793212528244
    data["current_call"]["chamado_at"] = 1793212528244
    data["history"] = [dict(data["current_call"], numero=3)]
    with patch("xano_client.urlopen", return_value=FakeResponse(data)):
        result = DisplayFeedClient(feed_url="https://xano.invalid/tv/feed", credential="test").fetch_snapshot()
    assert result["snapshot_at"] == "2026-10-28T18:35:28.244000Z"
    assert result["current_call"]["chamado_at"] == result["snapshot_at"]
    assert result["history"][0]["chamado_at"] == result["snapshot_at"]
    assert not display_app(FakeDisplayClient([result])).exception


def test_display_handles_first_call_after_empty_snapshot():
    client = FakeDisplayClient([snapshot(None, None), snapshot("first-event", 4)])
    app = display_app(client)
    app.run()
    assert not app.exception
    assert any(item.value == "Nova chamada" for item in app.success)


def test_feed_client_rejects_invalid_snapshot_timestamps():
    for invalid in [None, False, 0, -1, float("inf"), ""]:
        data = snapshot(None, None)
        data["snapshot_at"] = invalid
        with patch("xano_client.urlopen", return_value=FakeResponse(data)):
            try:
                DisplayFeedClient(feed_url="https://xano.invalid/tv/feed", credential="test").fetch_snapshot()
            except XanoRequestError:
                pass
            else:
                raise AssertionError(f"accepted invalid timestamp: {invalid!r}")
