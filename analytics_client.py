from __future__ import annotations

import json
import math
from datetime import datetime, timezone
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


def _valid_id(value: Any) -> bool:
    return type(value) is int and value > 0


def _valid_count(value: Any) -> bool:
    return type(value) is int and value >= 0


def _valid_label(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _valid_timestamp(value: Any) -> bool:
    if type(value) in (int, float):
        try:
            return value > 0 and math.isfinite(value) and datetime.fromtimestamp(value / 1000, tz=timezone.utc).year >= 1970
        except (OverflowError, ValueError, OSError):
            return False
    if not isinstance(value, str):
        return False
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).tzinfo is not None
    except ValueError:
        return False


def _validate_metrics(row: Any) -> None:
    invalid = not isinstance(row, dict) or any(
        not _valid_count(row.get(key)) for key in ("emitidas", "chamadas", "concluidas")
    )
    if invalid:
        raise XanoRequestError("O serviço Xano retornou métricas inválidas.")
    for key in ("espera_amostras", "duracao_amostras", "coorte_aguardando", "coorte_chamado", "coorte_concluido", "coorte_cancelado"):
        if key in row and not _valid_count(row[key]):
            raise XanoRequestError("O serviço Xano retornou métricas inválidas.")
    for key in ("espera_media_minutos", "duracao_media_minutos", "taxa_conclusao_coorte_pct"):
        value = row.get(key)
        if value is not None and (
            type(value) not in (int, float) or (type(value) is float and not math.isfinite(value)) or value < 0
            or (key == "taxa_conclusao_coorte_pct" and value > 100)
        ):
            raise XanoRequestError("O serviço Xano retornou métricas inválidas.")
    if "coorte_status" in row:
        cohort = row["coorte_status"]
        if not isinstance(cohort, dict) or any(
            not _valid_count(value) for value in cohort.values()
        ):
            raise XanoRequestError("O serviço Xano retornou métricas inválidas.")


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
        establishments = result["estabelecimentos"]
        queues = result["filas"]
        ids = set()
        for row in establishments:
            if (not isinstance(row, dict) or not _valid_id(row.get("id"))
                or row["id"] in ids or not _valid_label(row.get("nome"))):
                raise XanoRequestError("O serviço Xano retornou opções inválidas.")
            ids.add(row["id"])
        queue_ids = set()
        for row in queues:
            if (not isinstance(row, dict)
                or any(not _valid_id(row.get(key)) for key in ("estabelecimento_id", "servico_id", "fila_id"))
                or row["estabelecimento_id"] not in ids or row["fila_id"] in queue_ids
                or any(not _valid_label(row.get(key)) for key in ("servico_nome", "fila_nome"))):
                raise XanoRequestError("O serviço Xano retornou opções inválidas.")
            queue_ids.add(row["fila_id"])
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
        returned_filters = result["filters"]
        if (not isinstance(returned_filters, dict)
            or not _valid_timestamp(result["generated_at"])
            or any(not _valid_timestamp(returned_filters.get(key)) for key in ("period_start", "period_end"))
            or not _valid_id(returned_filters.get("estabelecimento_id"))
            or returned_filters["estabelecimento_id"] != filters.get("estabelecimento_id")):
            raise XanoRequestError("O serviço Xano retornou um relatório inválido.")
        for key in ("servico_id", "fila_id"):
            raw = returned_filters.get(key)
            actual, expected = raw or None, filters.get(key) or None
            if (raw is not None and (type(raw) is not int or raw < 0)) or actual != expected:
                raise XanoRequestError("O serviço Xano retornou um relatório inválido.")
        _validate_metrics(result["summary"])
        for row in result["daily"]:
            _validate_metrics(row)
            if not _valid_timestamp(row.get("bucket_start")):
                raise XanoRequestError("O serviço Xano retornou um relatório inválido.")
        for row in result["breakdown"]:
            _validate_metrics(row)
            if any(not _valid_label(row.get(key)) for key in ("servico_nome", "fila_nome")):
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