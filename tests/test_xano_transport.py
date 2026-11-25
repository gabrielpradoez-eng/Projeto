from unittest.mock import Mock
from urllib.error import HTTPError
import pytest
from xano_transport import RequestGate, paced_request


def test_sessions_share_budget_and_hosts_are_independent():
    now = [0.0]
    def sleep(delay):
        now[0] += delay
    gate = RequestGate(clock=lambda: now[0], sleep=sleep)
    gate.wait("xano")
    gate.wait("other")
    for _ in range(9):
        gate.wait("xano")
    assert now[0] == 22.5
    gate.limited("xano", "45")
    gate.wait("xano")
    assert now[0] == 67.5


def test_429_does_not_replay_mutation(monkeypatch):
    gate = Mock()
    monkeypatch.setattr("xano_transport._gate", gate)
    response = Mock(status_code=429, headers={"Retry-After": "40"})
    send = Mock(return_value=response)
    assert paced_request(send, "https://xano.io/chat", json={"mensagem": "Oi"}) is response
    send.assert_called_once()
    gate.limited.assert_called_once_with("xano.io", "40")


def test_urllib_429_updates_same_budget(monkeypatch):
    gate = Mock()
    monkeypatch.setattr("xano_transport._gate", gate)
    error = HTTPError("https://xano.io/feed",429,"limited",{"Retry-After":"35"},None)
    send = Mock(side_effect=error)
    with pytest.raises(HTTPError):
        paced_request(send,"https://xano.io/feed")
    gate.limited.assert_called_once_with("xano.io", "35")
    send.assert_called_once()
