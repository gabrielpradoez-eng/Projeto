from __future__ import annotations

import json
import logging
import re
import threading
import time
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen


logger = logging.getLogger(__name__)
_MAX_API_ERROR_BODY_BYTES = 4096
_SENSITIVE_API_KEY = re.compile(
    r"(?:token|password|secret|authorization|credential|api[_-]?key)", re.IGNORECASE
)
_BEARER_VALUE = re.compile(r"(?i)(\bbearer\s+)[A-Za-z0-9._~+/-]+=*")
_SENSITIVE_TEXT_VALUE = re.compile(
    r"(?i)(\b(?:access[_-]?token|refresh[_-]?token|token|password|secret|"
    r"authorization|credential|api[_-]?key)\b\s*[:=]\s*)([^\s,;\"']+)"
)


class XanoClientError(Exception):
    """Base error for Xano API requests."""


class XanoConfigurationError(XanoClientError):
    """Raised when required server-side Xano settings are missing."""


class XanoRequestError(XanoClientError):
    """Raised when Xano is unavailable or returns an unexpected response."""

    def __init__(
        self,
        message: str,
        *,
        status_code: int | None = None,
        api_message: str | None = None,
        api_code: str | None = None,
        api_body: str | None = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.api_message = api_message
        self.api_code = api_code
        self.api_body = api_body


class TrackingUnavailableError(XanoClientError):
    """Raised when a tracking reference is invalid, expired, or revoked."""


class QueueUnavailableError(XanoClientError):
    """Raised when a queue cannot accept a ticket at confirmation time."""

    def __init__(
        self,
        message: str = "A fila selecionada não está disponível.",
        *,
        status_code: int | None = None,
        api_message: str | None = None,
        api_code: str | None = None,
        api_body: str | None = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.api_message = api_message
        self.api_code = api_code
        self.api_body = api_body


def _redact_api_value(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: (
                "[REDACTED]"
                if _SENSITIVE_API_KEY.search(str(key))
                else _redact_api_value(item)
            )
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [_redact_api_value(item) for item in value]
    if isinstance(value, str):
        value = _BEARER_VALUE.sub(r"\1[REDACTED]", value)
        return _SENSITIVE_TEXT_VALUE.sub(r"\1[REDACTED]", value)
    return value


def _api_error_details(
    error: HTTPError,
) -> tuple[str | None, str | None, str | None]:
    try:
        raw_body = error.read(_MAX_API_ERROR_BODY_BYTES + 1)
    except OSError:
        return None, None, None
    was_truncated = len(raw_body) > _MAX_API_ERROR_BODY_BYTES
    body = raw_body[:_MAX_API_ERROR_BODY_BYTES].decode("utf-8", errors="replace")
    if not body:
        return None, None, None

    try:
        payload = json.loads(body)
    except json.JSONDecodeError:
        safe_body = _redact_api_value(body)
        message = safe_body[:500]
        return (
            f"{safe_body}{'… [truncado]' if was_truncated else ''}",
            None,
            message,
        )
    if isinstance(payload, dict):
        message = payload.get("message")
        code = payload.get("code")
        safe_payload = _redact_api_value(payload)
        safe_body = json.dumps(safe_payload, ensure_ascii=False)
        if was_truncated:
            safe_body += "… [truncado]"
        safe_message = _redact_api_value(message)
        return (
            safe_body,
            code[:200] if isinstance(code, str) else None,
            safe_message[:500]
            if isinstance(safe_message, str) and safe_message
            else None,
        )
    safe_body = _redact_api_value(body)
    return (
        f"{safe_body}{'… [truncado]' if was_truncated else ''}",
        None,
        None,
    )


class DisplayFeedClient:
    def __init__(
        self, *, feed_url: str, credential: str, timeout: float = 5.0
    ) -> None:
        self._feed_url = feed_url
        self._credential = credential
        self._timeout = timeout

    def fetch_snapshot(self) -> dict[str, Any]:
        result = self._request(
            "POST",
            self._feed_url,
            {"credential": self._credential},
            timeout=self._timeout,
        )
        if not isinstance(result, dict):
            raise XanoRequestError("O feed de chamadas retornou uma resposta inválida.")

        current_call = result.get("current_call")
        history = result.get("history")
        if current_call is not None and not isinstance(current_call, dict):
            raise XanoRequestError("O feed de chamadas retornou uma resposta inválida.")
        if not isinstance(history, list) or not isinstance(result.get("snapshot_at"), str):
            raise XanoRequestError("O feed de chamadas retornou uma resposta inválida.")
        return result

    def _request(
        self,
        method: str,
        url: str,
        payload: dict[str, Any],
        *,
        timeout: float,
    ) -> Any:
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        request = Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method=method,
        )
        try:
            with urlopen(request, timeout=timeout) as response:
                body = response.read()
        except HTTPError as exc:
            error = XanoRequestError("O feed de chamadas recusou a solicitação.")
            error.status_code = exc.code
            raise error from None
        except (URLError, TimeoutError, OSError):
            raise XanoRequestError("Não foi possível atualizar o painel de chamadas.") from None

        try:
            return json.loads(body.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            raise XanoRequestError("O feed de chamadas retornou uma resposta inválida.") from None


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
                raise QueueUnavailableError(
                    status_code=exc.status_code,
                    api_message=exc.api_message,
                    api_code=exc.api_code,
                    api_body=exc.api_body,
                ) from None
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
                {
                    "email": self._email,
                    "field_value": self._email,
                    "password": self._password,
                },
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
            api_body, api_code, api_message = _api_error_details(exc)
            path = urlsplit(url).path or "/"
            logged_api_code = (
                re.sub(r"[^A-Za-z0-9_.-]", "_", api_code)[:100]
                if api_code
                else "-"
            )
            logger.warning(
                "Xano request failed: method=%s path=%s status=%d api_code=%s",
                method,
                path,
                exc.code,
                logged_api_code,
            )
            error = XanoRequestError(
                "O serviço Xano recusou a solicitação.",
                status_code=exc.code,
                api_message=api_message,
                api_code=api_code,
                api_body=api_body,
            )
            raise error from None
        except (URLError, TimeoutError, OSError):
            raise XanoRequestError("Não foi possível conectar ao serviço Xano.") from None

        try:
            return json.loads(body.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            raise XanoRequestError("O serviço Xano retornou uma resposta inválida.") from None