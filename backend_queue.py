from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


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


@dataclass
class AttendanceRecord:
    id: int
    ticket_id: int
    attendant_id: int
    started_at: str
    ended_at: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "ticket_id": self.ticket_id,
            "attendant_id": self.attendant_id,
            "started_at": self.started_at,
            "ended_at": self.ended_at,
        }


class QueueBackend:
    """Backend domain service representing the Xano business rules for the queue core."""

    def __init__(self) -> None:
        self._next_user_id = 5
        self._next_establishment_id = 3
        self._next_service_id = 3
        self._next_queue_id = 3
        self._next_ticket_id = 1
        self._next_attendance_id = 1

        self.users: Dict[int, UserRecord] = {
            1: UserRecord(1, "Admin FilaSmart", "admin@fila.com", "admin123", "admin", 1),
            2: UserRecord(2, "Atendente Geral", "atendente@fila.com", "atendente123", "attendant", 1),
            3: UserRecord(3, "Cliente Teste", "cliente@fila.com", "cliente123", "user"),
            4: UserRecord(4, "Atendente Filial", "atendente2@fila.com", "atendente456", "attendant", 2),
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
        self.attendances: Dict[int, AttendanceRecord] = {}
        self.logs: List[Dict[str, Any]] = []

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
        for user in self.users.values():
            if user.email == email and user.password == password:
                self._record_log(user.id, "login", {"email": email})
                return user.to_public_dict()
        raise AccessDeniedError("Credenciais inválidas.")

    def register_establishment(self, name: str) -> Dict[str, Any]:
        if not name or not name.strip():
            raise InvalidQueueStateError("Nome do estabelecimento é obrigatório.")
        new_id = self._next_establishment_id
        self._next_establishment_id += 1
        establishment = EstablishmentRecord(new_id, name.strip())
        self.establishments[new_id] = establishment
        self._record_log(1, "create_establishment", {"establishment_id": new_id, "name": establishment.name})
        return establishment.to_dict()

    def register_service(self, establishment_id: int, name: str, estimated_minutes: int) -> Dict[str, Any]:
        if establishment_id not in self.establishments:
            raise QueueNotFoundError("Estabelecimento não encontrado.")
        if not name or not name.strip():
            raise InvalidQueueStateError("Nome do serviço é obrigatório.")
        if estimated_minutes <= 0:
            raise InvalidQueueStateError("Tempo estimado deve ser maior que zero.")

        new_id = self._next_service_id
        self._next_service_id += 1
        service = ServiceRecord(new_id, establishment_id, name.strip(), estimated_minutes)
        self.services[new_id] = service
        self._record_log(1, "create_service", {"service_id": new_id, "establishment_id": establishment_id})
        return service.to_dict()

    def register_queue(self, service_id: int, name: str, status: str = "open") -> Dict[str, Any]:
        if service_id not in self.services:
            raise QueueNotFoundError("Serviço não encontrado.")
        if not name or not name.strip():
            raise InvalidQueueStateError("Nome da fila é obrigatório.")
        if status not in {"open", "closed"}:
            raise InvalidQueueStateError("Status da fila inválido.")

        new_id = self._next_queue_id
        self._next_queue_id += 1
        queue = QueueRecord(new_id, service_id, name.strip(), status)
        self.queues[new_id] = queue
        self._record_log(1, "create_queue", {"queue_id": new_id, "service_id": service_id})
        return queue.to_dict()

    def get_queue(self, queue_id: int) -> QueueRecord:
        if queue_id not in self.queues:
            raise QueueNotFoundError(f"Fila {queue_id} não encontrada.")
        return self.queues[queue_id]

    def _ensure_attendant(self, attendant_id: int) -> UserRecord:
        attendant = self.users.get(attendant_id)
        if attendant is None or attendant.role != "attendant":
            raise AccessDeniedError("Apenas atendentes ativos podem executar esta ação.")
        return attendant

    def emit_ticket(self, queue_id: int, user_id: int) -> Dict[str, Any]:
        queue = self.get_queue(queue_id)
        if queue.status != "open":
            raise InvalidQueueStateError("Esta fila está fechada no momento.")

        next_number = 1
        for ticket in self.tickets.values():
            if ticket.queue_id == queue_id and ticket.number >= next_number:
                next_number = ticket.number + 1

        ticket_id = self._next_ticket_id
        self._next_ticket_id += 1
        ticket = TicketRecord(
            id=ticket_id,
            queue_id=queue_id,
            user_id=user_id,
            number=next_number,
            status="waiting",
            created_at=self._now(),
        )
        self.tickets[ticket_id] = ticket
        self._record_log(user_id, "join_queue", {"ticket_id": ticket_id, "queue_id": queue_id, "number": next_number})
        return ticket.to_dict()

    def call_next_token(self, queue_id: int, attendant_id: int) -> Dict[str, Any]:
        attendant = self._ensure_attendant(attendant_id)
        queue = self.get_queue(queue_id)
        service = self.services.get(queue.service_id)
        if service is None:
            raise QueueNotFoundError("Serviço da fila não encontrado.")
        if service.establishment_id != attendant.establishment_id:
            raise AccessDeniedError("Você não tem permissão para atender esta fila.")

        waiting = sorted(
            [ticket for ticket in self.tickets.values() if ticket.queue_id == queue_id and ticket.status == "waiting"],
            key=lambda item: item.number,
        )
        if not waiting:
            raise InvalidQueueStateError("Não há senhas aguardando nesta fila.")

        ticket = waiting[0]
        ticket.status = "called"
        ticket.called_at = self._now()

        attendance_id = self._next_attendance_id
        self._next_attendance_id += 1
        attendance = AttendanceRecord(
            id=attendance_id,
            ticket_id=ticket.id,
            attendant_id=attendant_id,
            started_at=self._now(),
        )
        self.attendances[attendance_id] = attendance
        self._record_log(attendant_id, "call_next", {"ticket_id": ticket.id, "queue_id": queue_id})
        return ticket.to_dict()

    def complete_service(self, ticket_id: int, attendant_id: int) -> Dict[str, Any]:
        ticket = self.tickets.get(ticket_id)
        if ticket is None:
            raise QueueNotFoundError("Senha não encontrada.")
        if ticket.status != "called":
            raise InvalidQueueStateError("Esta senha não está em atendimento ou já foi finalizada.")

        attendance = next(
            (item for item in self.attendances.values() if item.ticket_id == ticket_id and item.attendant_id == attendant_id and item.ended_at is None),
            None,
        )
        if attendance is None:
            raise AccessDeniedError("Atendimento não encontrado para este atendente.")

        ticket.status = "completed"
        ticket.completed_at = self._now()
        attendance.ended_at = ticket.completed_at
        self._record_log(attendant_id, "complete_service", {"ticket_id": ticket_id, "queue_id": ticket.queue_id})
        return ticket.to_dict()

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
                    "waiting": len([ticket for ticket in self.tickets.values() if ticket.queue_id == queue.id and ticket.status == "waiting"]),
                    "called": len([ticket for ticket in self.tickets.values() if ticket.queue_id == queue.id and ticket.status == "called"]),
                })
        return rows
