"""Process-wide pacing shared by portal, kiosk, reports and display clients."""
import threading
import time
from urllib.error import HTTPError
from urllib.parse import urlsplit


class RequestGate:
    def __init__(self, interval=2.5, clock=time.monotonic, sleep=time.sleep):
        self.interval, self.clock, self.sleep = interval, clock, sleep
        self.lock = threading.Lock()
        self.next_at = {}

    def wait(self, host):
        with self.lock:
            delay = self.next_at.get(host, 0) - self.clock()
            if delay > 0:
                self.sleep(delay)
            self.next_at[host] = self.clock() + self.interval

    def limited(self, host, retry_after=None):
        try:
            delay = max(30, float(retry_after))
        except (TypeError, ValueError):
            delay = 30
        # Ignore malformed infinite values; avoid a permanently blocked process.
        if not 0 < delay < 3600:
            delay = 30
        with self.lock:
            self.next_at[host] = max(self.next_at.get(host, 0), self.clock() + delay)


_gate = RequestGate()


def paced_request(send, url_or_request, **kwargs):
    url = getattr(url_or_request, "full_url", url_or_request)
    host = urlsplit(url).netloc
    _gate.wait(host)
    try:
        response = send(url_or_request, **kwargs)
    except HTTPError as error:
        if error.code == 429:
            _gate.limited(host, error.headers.get("Retry-After") if error.headers else None)
        raise
    if getattr(response, "status_code", None) == 429:
        _gate.limited(host, response.headers.get("Retry-After"))
    # Never replay mutations: an ambiguous outcome must be checked by the user.
    return response
