from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import requests
import streamlit as st


class QueueSmartError(Exception):
    """Base class for domain validation errors."""


class AccessDeniedError(QueueSmartError):
    """Raised when a user does not have permission for a given action."""


class SessionVerificationUnavailable(QueueSmartError):
    """Raised when the identity service cannot currently verify a session."""


class InvalidQueueStateError(QueueSmartError):
    """Raised when a queue or ticket is not in a valid state for the requested action."""


class QueueNotFoundError(InvalidQueueStateError):
    """Raised when a queue or entity cannot be found."""


@dataclass
class UserRecord:
    id: int
    name: str
    email: str
    password: str
    role: str
    establishment_id: Optional[int] = None

    def to_public_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "role": self.role,
            "establishment_id": self.establishment_id,
        }


@dataclass
class EstablishmentRecord:
    id: int
    name: str

    def to_dict(self) -> Dict[str, Any]:
        return {"id": self.id, "name": self.name}


@dataclass
class ServiceRecord:
    id: int
    establishment_id: int
    name: str
    estimated_minutes: int

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "establishment_id": self.establishment_id,
            "name": self.name,
            "estimated_minutes": self.estimated_minutes,
        }


@dataclass
class QueueRecord:
    id: int
    service_id: int
    name: str
    status: str = "open"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "service_id": self.service_id,
            "name": self.name,
            "status": self.status,
        }


@dataclass
class TicketRecord:
    id: int
    queue_id: int
    user_id: int
    number: int
    status: str = "waiting"
    created_at: Optional[str] = None
    called_at: Optional[str] = None
    completed_at: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "queue_id": self.queue_id,
            "user_id": self.user_id,
            "number": self.number,
            "status": self.status,
            "created_at": self.created_at,
            "called_at": self.called_at,
            "completed_at": self.completed_at,
        }


class QueueBackend:
    """Backend domain service conectando a interface em Streamlit aos endpoints reais do Xano."""

    def __init__(self) -> None:
        try:
            settings = st.secrets["xano"]
        except (KeyError, FileNotFoundError):
            settings = {}
        self.base_url = settings.get("base_url", "").rstrip("/")
        self.login_url = settings.get("login_url", "")
        self.me_url = settings.get("me_url", "")
        if not self.me_url and self.login_url.endswith("/auth/login"):
            self.me_url = self.login_url.removesuffix("/auth/login") + "/auth/me"

        # Estruturas locais legadas não são fontes de dados da interface operacional.
        self.users: Dict[int, UserRecord] = {}
        self.establishments: Dict[int, EstablishmentRecord] = {}
        self.services: Dict[int, ServiceRecord] = {}
        self.queues: Dict[int, QueueRecord] = {}

        self.tickets: Dict[int, TicketRecord] = {}
        self.logs: List[Dict[str, Any]] = []
        self._next_ticket_id = 1

    def _get_headers(self, token: Optional[str] = None) -> Dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        return headers

    def _now(self) -> str:
        return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    def _record_log(self, user_id: int, action: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        self.logs.append({
            "user_id": user_id,
            "action": action,
            "metadata": metadata or {},
            "created_at": self._now(),
        })

    def authenticate(self, email: str, password: str) -> Dict[str, Any]:
        """Endpoint: POST /auth/login"""
        url = self.login_url
        payload = {"email": email, "password": password}
        if not self.login_url:
            raise AccessDeniedError("Configure [xano].login_url para autenticação.")

        try:
            response = requests.post(url, json=payload, timeout=10)

            if response.status_code == 200:
                data = response.json()
                if not isinstance(data, dict):
                    raise AccessDeniedError("Resposta de autenticação inválida.")

                auth_token = data.get("authToken")
                remote_user = data.get("user")
                if (
                    remote_user is None
                    and isinstance(auth_token, str)
                    and auth_token.strip()
                    and type(data.get("user_id")) is int
                    and data["user_id"] > 0
                ):
                    if not self.me_url:
                        raise AccessDeniedError("Configure login_url e me_url do Xano.")
                    identity_response = requests.get(
                        self.me_url,
                        headers=self._get_headers(auth_token.strip()),
                        timeout=10,
                    )
                    if identity_response.status_code != 200:
                        raise AccessDeniedError("Não foi possível confirmar o usuário no Xano.")
                    remote_user = identity_response.json()
                    if not isinstance(remote_user, dict) or remote_user.get("id") != data["user_id"]:
                        raise AccessDeniedError("Resposta de autenticação inválida.")
                if (
                    not isinstance(auth_token, str)
                    or not auth_token.strip()
                    or not isinstance(remote_user, dict)
                ):
                    raise AccessDeniedError("Resposta de autenticação inválida.")

                user_id = remote_user.get("id")
                name = remote_user.get("name")
                user_email = remote_user.get("email")
                remote_role = remote_user.get("role")
                establishment_id = remote_user.get("estabelecimento_id")
                role_mapping = {
                    "admin": "admin",
                    "atendente": "attendant",
                    "usuario": "user",
                }
                role = (
                    role_mapping.get(remote_role)
                    if isinstance(remote_role, str)
                    else None
                )

                if (
                    type(user_id) is not int
                    or user_id <= 0
                    or not isinstance(name, str)
                    or not name.strip()
                    or not isinstance(user_email, str)
                    or not user_email.strip()
                    or role is None
                    or (
                        establishment_id is not None
                        and type(establishment_id) is not int
                    )
                ):
                    raise AccessDeniedError("Resposta de autenticação inválida.")

                user_dict = {
                    "id": user_id,
                    "user_id": user_id,
                    "name": name,
                    "email": user_email,
                    "role": role,
                    "establishment_id": establishment_id,
                    "authToken": auth_token.strip(),
                }
                self._record_log(user_id, "login", {"email": user_email})
                return user_dict
            elif response.status_code in (400, 401, 403, 404):
                raise AccessDeniedError("Credenciais inválidas ou usuário não cadastrado.")
            else:
                raise AccessDeniedError(f"Falha na autenticação do Xano (HTTP {response.status_code}).")

        except (requests.exceptions.RequestException, ValueError):
            raise AccessDeniedError("Não foi possível autenticar no Xano.") from None

    def verify_session(self, token: str, expected_user_id: int) -> Dict[str, Any]:
        """Confirm identity and current role using the canonical Xano auth/me endpoint."""
        if not isinstance(token, str) or not token.strip() or type(expected_user_id) is not int:
            raise AccessDeniedError("Sessão inválida. Entre novamente.")
        if not self.me_url:
            raise SessionVerificationUnavailable("A verificação de sessão não está configurada.")
        try:
            response = requests.get(self.me_url, headers=self._get_headers(token), timeout=10)
            if response.status_code in (401, 403, 404):
                raise AccessDeniedError("Sessão expirada ou acesso revogado. Entre novamente.")
            if response.status_code != 200:
                raise SessionVerificationUnavailable("Não foi possível verificar sua sessão agora.")
            profile = response.json()
        except (requests.exceptions.RequestException, ValueError):
            raise SessionVerificationUnavailable("Não foi possível verificar sua sessão agora.") from None
        if not isinstance(profile, dict):
            raise AccessDeniedError("Sessão inválida. Entre novamente.")
        role = {"admin": "admin", "atendente": "attendant", "usuario": "user"}.get(
            profile.get("role") if isinstance(profile.get("role"), str) else ""
        )
        if (
            type(profile.get("id")) is not int or profile["id"] != expected_user_id
            or profile["id"] <= 0 or role is None
            or not isinstance(profile.get("name"), str) or not profile["name"].strip()
            or not isinstance(profile.get("email"), str) or not profile["email"].strip()
        ):
            raise AccessDeniedError("Sessão inválida ou perfil sem acesso ao aplicativo.")
        return {
            "id": profile["id"], "user_id": profile["id"], "name": profile["name"],
            "email": profile["email"], "role": role,
            "establishment_id": profile.get("estabelecimento_id"), "authToken": token,
        }

    def _operation_request(self, path: str, payload: dict, token: Optional[str]) -> dict:
        if not self.base_url:
            raise InvalidQueueStateError("Configure [xano].base_url para o grupo Queue Management.")
        if not token:
            raise AccessDeniedError("Entre novamente para realizar esta operação.")
        try:
            response = requests.post(
                f"{self.base_url}/{path}", json=payload,
                headers=self._get_headers(token), timeout=10,
            )
            if response.status_code in (401, 403):
                raise AccessDeniedError("O Xano não autorizou esta operação. Entre novamente ou confira suas permissões.")
            if response.status_code != 200:
                raise InvalidQueueStateError(f"O Xano recusou a operação (HTTP {response.status_code}). Atualize o painel antes de tentar novamente.")
            data = response.json()
            if not isinstance(data, dict):
                raise InvalidQueueStateError("Resposta inválida da operação no Xano.")
            return data
        except (requests.RequestException, ValueError):
            raise InvalidQueueStateError("Não foi possível confirmar a operação. Atualize o painel antes de tentar novamente.") from None

    def _confirmed_ticket(self, data: dict, expected_status: str, *, queue_id: int | None = None, ticket_id: int | None = None) -> TicketRecord:
        statuses = {"aguardando": "waiting", "chamado": "called", "concluido": "completed"}
        if not isinstance(data, dict):
            raise InvalidQueueStateError("Resposta inválida de senha no Xano.")
        expected_id, expected_queue = ticket_id, queue_id
        ticket_id = data.get("id")
        number = data.get("numero", data.get("number"))
        queue_id = data.get("fila_id", data.get("queue_id"))
        user_id = data.get("usuario_id", data.get("user_id"))
        raw_status = data.get("status")
        status = statuses.get(raw_status, raw_status) if isinstance(raw_status, str) else None
        if (
            any(type(value) is not int or value <= 0 for value in (ticket_id, number, queue_id, user_id))
            or status != expected_status
            or (expected_id is not None and ticket_id != expected_id)
            or (expected_queue is not None and queue_id != expected_queue)
        ):
            raise InvalidQueueStateError("Resposta inválida de senha no Xano. Atualize o painel para confirmar o estado.")
        ticket = TicketRecord(
            id=ticket_id, number=number, queue_id=queue_id, user_id=user_id,
            status=status, created_at=data.get("created_at"),
            called_at=data.get("chamado_at"), completed_at=data.get("concluido_at"),
        )
        self.tickets[ticket.id] = ticket
        return ticket

    def emit_ticket(self, queue_id: int, user_id: int, token: Optional[str] = None) -> Dict[str, Any]:
        data = self._operation_request("join", {"fila_id": int(queue_id)}, token)
        return self._confirmed_ticket(data, "waiting", queue_id=queue_id).to_dict()

    def call_next_token(self, queue_id: int, attendant_id: int, token: Optional[str] = None) -> Dict[str, Any]:
        data = self._operation_request("call_next", {"fila_id": int(queue_id)}, token)
        return self._confirmed_ticket(data.get("senha"), "called", queue_id=queue_id).to_dict()

    def complete_service(self, ticket_id: int, attendant_id: int, token: Optional[str] = None) -> Dict[str, Any]:
        # O estado atual e a autorização são validados pelo Xano, inclusive após troca de sessão.
        data = self._operation_request("complete", {"senha_id": int(ticket_id)}, token)
        return self._confirmed_ticket(data.get("senha"), "completed", ticket_id=ticket_id).to_dict()

    def get_attendant_dashboard(self, token: Optional[str] = None) -> list[dict]:
        """Leia o estado compartilhado da operação no Xano a cada atualização."""
        if not self.base_url:
            raise InvalidQueueStateError("Configure [xano].base_url para o grupo Queue Management.")
        try:
            response = requests.get(
                f"{self.base_url}/attendant/dashboard",
                headers=self._get_headers(token), timeout=10,
            )
            if response.status_code in (401, 403):
                raise AccessDeniedError("O Xano não autorizou o acesso às filas deste atendente.")
            if response.status_code != 200:
                raise InvalidQueueStateError(f"Não foi possível consultar as filas (HTTP {response.status_code}).")
            rows = response.json()
            if not isinstance(rows, list) or any(
                not isinstance(row, dict) or type(row.get("id")) is not int
                or not isinstance(row.get("nome"), str)
                or type(row.get("total_aguardando")) is not int
                or (row.get("em_atendimento") is not None and (
                    not isinstance(row["em_atendimento"], dict)
                    or type(row["em_atendimento"].get("id")) is not int
                    or row["em_atendimento"]["id"] <= 0
                    or type(row["em_atendimento"].get("numero")) is not int
                    or row["em_atendimento"]["numero"] <= 0
                ))
                for row in rows
            ):
                raise InvalidQueueStateError("Resposta inválida do painel de atendimento.")
            return rows
        except (requests.RequestException, ValueError):
            raise InvalidQueueStateError("Não foi possível consultar o painel do Xano.") from None

    def register_establishment(self, name: str) -> Dict[str, Any]:
        if not name or not name.strip():
            raise InvalidQueueStateError("Nome do estabelecimento é obrigatório.")
        new_id = len(self.establishments) + 1
        est = EstablishmentRecord(new_id, name.strip())
        self.establishments[new_id] = est
        return est.to_dict()

    def register_service(self, establishment_id: int, name: str, estimated_minutes: int) -> Dict[str, Any]:
        if not name or not name.strip():
            raise InvalidQueueStateError("Nome do serviço é obrigatório.")
        new_id = len(self.services) + 1
        srv = ServiceRecord(new_id, establishment_id, name.strip(), estimated_minutes)
        self.services[new_id] = srv
        return srv.to_dict()

    def register_queue(self, service_id: int, name: str, status: str = "open") -> Dict[str, Any]:
        if not name or not name.strip():
            raise InvalidQueueStateError("Nome da fila é obrigatório.")
        new_id = len(self.queues) + 1
        q = QueueRecord(new_id, service_id, name.strip(), status)
        self.queues[new_id] = q
        return q.to_dict()

    def list_logs(self) -> List[Dict[str, Any]]:
        return list(self.logs)

    def list_queues_for_establishment(self, establishment_id: int) -> List[Dict[str, Any]]:
        rows: List[Dict[str, Any]] = []
        for queue in self.queues.values():
            service = self.services.get(queue.service_id)
            if service and service.establishment_id == establishment_id:
                rows.append({
                    "id": queue.id,
                    "name": queue.name,
                    "status": queue.status,
                    "service": service.name,
                    "waiting": len([t for t in self.tickets.values() if t.queue_id == queue.id and t.status == "waiting"]),
                    "called": len([t for t in self.tickets.values() if t.queue_id == queue.id and t.status == "called"]),
                })
        return rows
