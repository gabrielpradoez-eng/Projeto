import pytest


@pytest.fixture(autouse=True)
def no_real_network_delays(monkeypatch):
    # Transport behavior is tested separately with an injected fake clock.
    import xano_transport
    monkeypatch.setattr(xano_transport._gate, "wait", lambda host: None)
    monkeypatch.setattr(xano_transport._gate, "limited", lambda *args: None)
