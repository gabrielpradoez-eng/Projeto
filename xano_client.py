from __future__ import annotations

import json
import threading
import time
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


class XanoClientError(Exception):
    """Base error for Xano API requests."""


class XanoConfigurationError(XanoClientError):
    """Raised when required server-side Xano settings are missing."""


class XanoRequestError(XanoClientError):
    """Raised when Xano is unavailable or returns an unexpected response."""


class TrackingUnavailableError(XanoClientError):
    """Raised when a tracking reference is invalid, expired, or revoked."""


class QueueUnavailableError(XanoClientError):
    """Raised when a queue cannot accept a ticket at confirmation time."""


class XanoClient:
    def __init__(
        self,
        *,
        login_url: str,
        queues_url: str,
        issue_url: str,
        tracking_url: str,
        email: str,
        password: str,
        timeout: float = 8.0,
    ) -> None:
        self._login_url = login_url
        self._queues_url = queues_url
        self._issue_url = issue_url
        self._tracking_url = tracking_url
        self._email = email
        self._password = password
        self._timeout = timeout
        self._token: str | None = None
        self._token_expires_at = 0.0
        self._token_lock = threading.Lock()

    def list_queues(self) -> list[dict[str, Any]]:
        result = self._authorized_request("GET", self._queues_url)
        if not isinstance(result, list):
            raise XanoRequestError("Resposta inválida do serviço de filas.")
        return result

    def issue_ticket(self, queue_id: int) -> dict[str, Any]:
        try:
            result = self._authorized_request(
                "POST", self._issue_url, {"fila_id": queue_id}
            )
        except XanoRequestError as exc:
            if getattr(exc, "status_code", None) in {400, 404, 422}:
                raise QueueUnavailableError from None
            raise
        if not isinstance(result, dict):
            raise XanoRequestError("Resposta inválida do serviço de emissão.")
        return result

    def track_ticket(self, reference: str) -> dict[str, Any]:
        try:
            result = self._authorized_request(
                "POST", self._tracking_url, {"referencia": reference}
            )
        except XanoRequestError as exc:
            if getattr(exc, "status_code", None) == 404:
                raise TrackingUnavailableError from None
            raise
        if not isinstance(result, dict):
            raise XanoRequestError("Resposta inválida do serviço de acompanhamento.")
        return result

    def _authorized_request(
        self, method: str, url: str, payload: dict[str, Any] | None = None
    ) -> Any:
        token = self._get_token()
        try:
            return self._request(method, url, payload, token)
        except XanoRequestError as exc:
            if getattr(exc, "status_code", None) != 401:
                raise
            self._invalidate_token()
            return self._request(method, url, payload, self._get_token())

    def _get_token(self) -> str:
        with self._token_lock:
            if self._token and time.monotonic() < self._token_expires_at:
                return self._token

            response = self._request(
                "POST",
                self._login_url,
                {"email": self._email, "password": self._password},
            )
            token = response.get("authToken") if isinstance(response, dict) else None
            if not isinstance(token, str) or not token:
                raise XanoRequestError("Autenticação do Totem falhou.")
            self._token = token
            self._token_expires_at = time.monotonic() + 23 * 60 * 60
            return token

    def _invalidate_token(self) -> None:
        with self._token_lock:
            self._token = None
            self._token_expires_at = 0.0

    def _request(
        self,
        method: str,
        url: str,
        payload: dict[str, Any] | None = None,
        token: str | None = None,
    ) -> Any:
        headers = {"Accept": "application/json"}
        data = None
        if payload is not None:
            headers["Content-Type"] = "application/json"
            data = json.dumps(payload).encode("utf-8")
        if token:
            headers["Authorization"] = f"Bearer {token}"

        request = Request(url, data=data, headers=headers, method=method)
        try:
            with urlopen(request, timeout=self._timeout) as response:
                body = response.read()
        except HTTPError as exc:
            error = XanoRequestError("O serviço Xano recusou a solicitação.")
            error.status_code = exc.code
            raise error from None
        except (URLError, TimeoutError, OSError):
            raise XanoRequestError("Não foi possível conectar ao serviço Xano.") from None

        try:
            return json.loads(body.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            raise XanoRequestError("O serviço Xano retornou uma resposta inválida.") from None