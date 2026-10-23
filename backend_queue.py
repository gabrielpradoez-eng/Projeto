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
            self.base_url = st.secrets["xano"]["base_url"].rstrip("/")
        except (KeyError, FileNotFoundError):
            self.base_url = "https://x8ki-letl-twmt.n7.xano.io/api:-8IXPb-r"

        # Armazenamento em memória para dados de cadastro local/múltipla leitura
        self.users: Dict[int, UserRecord] = {
            1: UserRecord(1, "Admin FilaSmart", "admin@filasmart.com", "senha123", "admin", 1),
            2: UserRecord(2, "Atendente Geral", "atendente@filasmart.com", "atendente123", "attendant", 1),
            3: UserRecord(3, "Cliente Teste", "cliente@filasmart.com", "cliente123", "user"),
        }

        self.establishments: Dict[int, EstablishmentRecord] = {
            1: EstablishmentRecord(1, "Filial Centro"),
            2: EstablishmentRecord(2, "Filial Norte"),
        }

        self.services: Dict[int, ServiceRecord] = {
            1: ServiceRecord(1, 1, "Atendimento Geral", 10),
            2: ServiceRecord(2, 1, "Financeiro", 15),
        }

        self.queues: Dict[int, QueueRecord] = {
            1: QueueRecord(1, 1, "Fila Geral", "open"),
            2: QueueRecord(2, 2, "Fila Financeiro", "open"),
        }

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
        url = f"{self.base_url}/auth/login"
        payload = {
            "email": email,
            "field_value": email,
            "password": password,
        }

        try:
            response = requests.post(url, json=payload, timeout=10)

            if response.status_code == 200:
                data = response.json()
                auth_token = data.get("authToken")
                user_id = data.get("user_id")
                if not isinstance(auth_token, str) or not auth_token or not isinstance(user_id, int):
                    raise AccessDeniedError("Resposta de autenticação inválida.")

                user_record = next(
                    (u for u in self.users.values() if u.email.strip().lower() == email.strip().lower()),
                    None
                )

                if user_record:
                    user_dict = user_record.to_public_dict()
                else:
                    user_dict = {
                        "id": 1,
                        "name": email.split("@")[0].title(),
                        "email": email,
                        "role": "admin",
                        "establishment_id": 1,
                    }

                user_dict["id"] = user_id
                user_dict["user_id"] = user_id
                user_dict["authToken"] = auth_token
                self._record_log(user_dict["id"], "login", {"email": email})
                return user_dict
            elif response.status_code in (400, 401, 403, 404):
                raise AccessDeniedError("Credenciais inválidas ou usuário não cadastrado.")
            else:
                raise AccessDeniedError(f"Erro na autenticação ({response.status_code}): {response.text}")

        except requests.exceptions.RequestException as exc:
            raise AccessDeniedError(f"Erro de conexão com o Xano: {str(exc)}")

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
                    number=res_data.get("number", ticket_id),
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
                    number=senha_info.get("number", 1) if isinstance(senha_info, dict) else 1,
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

    def get_attendant_dashboard(self, token: Optional[str] = None) -> Dict[str, Any]:
        """Endpoint: GET /attendant/dashboard"""
        url = f"{self.base_url}/attendant/dashboard"
        try:
            response = requests.get(url, headers=self._get_headers(token), timeout=10)
            if response.status_code == 200:
                return response.json()
            return {}
        except Exception:
            return {}

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
