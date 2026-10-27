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
                raise AccessDeniedError(f"Erro na autenticação ({response.status_code}): {response.text}")

        except (requests.exceptions.RequestException, ValueError):
            raise AccessDeniedError("Não foi possível autenticar no Xano.") from None

    def emit_ticket(self, queue_id: int, user_id: int, token: Optional[str] = None) -> Dict[str, Any]:
        """Endpoint: POST /join -> {"fila_id": int}"""
        url = f"{self.base_url}/join"
        payload = {"fila_id": int(queue_id)}

        try:
            response = requests.post(
                url,
                json=payload,
                headers=self._get_headers(token),
                timeout=10
            )

            if response.status_code == 200:
                res_data = response.json()
                ticket_id = res_data.get("id", self._next_ticket_id)
                self._next_ticket_id += 1

                ticket = TicketRecord(
                    id=ticket_id,
                    queue_id=queue_id,
                    user_id=user_id,
                    number=res_data.get("numero", res_data.get("number", ticket_id)),
                    status=res_data.get("status", "waiting"),
                    created_at=self._now(),
                )
                self.tickets[ticket_id] = ticket
                self._record_log(user_id, "join_queue", {"ticket_id": ticket_id, "queue_id": queue_id})
                return ticket.to_dict()
            else:
                raise InvalidQueueStateError(f"Erro ao emitir senha ({response.status_code}): {response.text}")

        except requests.exceptions.RequestException as exc:
            raise InvalidQueueStateError(f"Erro de conexão ao emitir senha: {str(exc)}")

    def call_next_token(self, queue_id: int, attendant_id: int, token: Optional[str] = None) -> Dict[str, Any]:
        """Endpoint: POST /call_next -> {"fila_id": int}"""
        url = f"{self.base_url}/call_next"
        payload = {"fila_id": int(queue_id)}

        try:
            response = requests.post(
                url,
                json=payload,
                headers=self._get_headers(token),
                timeout=10
            )

            if response.status_code == 200:
                res_data = response.json()
                senha_info = res_data.get("senha", {})

                ticket_id = senha_info.get("id", 1) if isinstance(senha_info, dict) else 1
                ticket = TicketRecord(
                    id=ticket_id,
                    queue_id=queue_id,
                    user_id=attendant_id,
                    number=senha_info.get("numero", senha_info.get("number", ticket_id)) if isinstance(senha_info, dict) else ticket_id,
                    status="called",
                    called_at=self._now(),
                )
                self.tickets[ticket_id] = ticket
                self._record_log(attendant_id, "call_next", {"queue_id": queue_id, "response": res_data})
                return ticket.to_dict()
            elif response.status_code in (400, 404):
                raise InvalidQueueStateError("Não há senhas aguardando ou fila inválida.")
            elif response.status_code in (401, 403):
                raise AccessDeniedError("O atendente não tem autorização para chamar esta fila.")
            else:
                raise InvalidQueueStateError(f"Erro ao chamar senha ({response.status_code}): {response.text}")

        except requests.exceptions.RequestException as exc:
            raise InvalidQueueStateError(f"Erro de conexão ao chamar próxima senha: {str(exc)}")

    def complete_service(self, ticket_id: int, attendant_id: int, token: Optional[str] = None) -> Dict[str, Any]:
        """Endpoint: POST /complete -> {"senha_id": int}"""
        ticket = self.tickets.get(ticket_id)
        if ticket is not None and ticket.status != "called":
            raise InvalidQueueStateError("A senha não está em atendimento.")

        url = f"{self.base_url}/complete"
        payload = {"senha_id": int(ticket_id)}

        try:
            response = requests.post(
                url,
                json=payload,
                headers=self._get_headers(token),
                timeout=10
            )

            if response.status_code == 200:
                res_data = response.json()
                if ticket_id in self.tickets:
                    self.tickets[ticket_id].status = "completed"
                    self.tickets[ticket_id].completed_at = self._now()
                self._record_log(attendant_id, "complete_service", {"ticket_id": ticket_id})
                return {"id": ticket_id, "number": ticket_id, "status": "completed"}
            else:
                raise InvalidQueueStateError(f"Erro ao finalizar atendimento ({response.status_code}): {response.text}")

        except requests.exceptions.RequestException as exc:
            raise InvalidQueueStateError(f"Erro de conexão ao finalizar atendimento: {str(exc)}")

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
                or (row.get("em_atendimento") is not None and not isinstance(row["em_atendimento"], dict))
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
