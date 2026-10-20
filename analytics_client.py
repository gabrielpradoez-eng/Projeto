from __future__ import annotations

import json
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from xano_client import XanoConfigurationError, XanoRequestError


def _request_json(
    method: str,
    url: str,
    payload: dict[str, Any] | None,
    *,
    timeout: float,
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
        with urlopen(request, timeout=timeout) as response:
            body = response.read()
    except HTTPError as exc:
        error = XanoRequestError("O serviço Xano recusou a solicitação analítica.")
        error.status_code = exc.code
        raise error from None
    except (URLError, TimeoutError, OSError):
        raise XanoRequestError("Não foi possível conectar ao serviço Xano.") from None

    try:
        return json.loads(body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        raise XanoRequestError("O serviço Xano retornou JSON inválido.") from None


class AnalyticsClient:
    def __init__(
        self,
        *,
        options_url: str,
        report_url: str,
        auth_token: str,
        timeout: float = 10.0,
    ) -> None:
        self._options_url = options_url
        self._report_url = report_url
        self._auth_token = auth_token
        self._timeout = timeout

    @staticmethod
    def authenticate(
        login_url: str, email: str, password: str, *, timeout: float = 10.0
    ) -> str:
        response = _request_json(
            "POST",
            login_url,
            {"email": email, "password": password},
            timeout=timeout,
        )
        token = response.get("authToken") if isinstance(response, dict) else None
        if not isinstance(token, str) or not token:
            raise XanoConfigurationError("A autenticação Xano não retornou um token válido.")
        return token

    def list_options(self) -> dict[str, Any]:
        result = self._authorized_request("GET", self._options_url)
        if not isinstance(result, dict):
            raise XanoRequestError("O serviço Xano retornou opções inválidas.")
        if not isinstance(result.get("estabelecimentos"), list) or not isinstance(
            result.get("filas"), list
        ):
            raise XanoRequestError("O serviço Xano retornou opções inválidas.")
        return result

    def fetch_report(self, filters: dict[str, Any]) -> dict[str, Any]:
        result = self._authorized_request("POST", self._report_url, filters)
        if not isinstance(result, dict):
            raise XanoRequestError("O serviço Xano retornou um relatório inválido.")
        required = ("summary", "daily", "breakdown", "generated_at", "filters")
        if any(key not in result for key in required):
            raise XanoRequestError("O serviço Xano retornou um relatório inválido.")
        if not isinstance(result["summary"], dict) or not isinstance(
            result["daily"], list
        ) or not isinstance(result["breakdown"], list):
            raise XanoRequestError("O serviço Xano retornou um relatório inválido.")
        return result

    def _authorized_request(
        self, method: str, url: str, payload: dict[str, Any] | None = None
    ) -> Any:
        return _request_json(
            method,
            url,
            payload,
            timeout=self._timeout,
            token=self._auth_token,
        )