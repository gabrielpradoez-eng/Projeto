from __future__ import annotations

import streamlit as st

from backend_queue import (
    AccessDeniedError,
    InvalidQueueStateError,
    QueueBackend,
    QueueNotFoundError,
)


def main() -> None:
    if "backend" not in st.session_state:
        st.session_state.backend = QueueBackend()

    backend: QueueBackend = st.session_state.backend

    st.set_page_config(page_title="FilaSmart", page_icon="⏱️")
    st.title("FilaSmart — Núcleo operacional")

    if "user" not in st.session_state:
        st.session_state.user = None

    user = st.session_state.user

    with st.sidebar:
        st.header("Autenticação")
        if user is None:
            email = st.text_input("E-mail", value="admin@fila.com")
            password = st.text_input("Senha", type="password", value="admin123")
            if st.button("Entrar"):
                try:
                    user = backend.authenticate(email, password)
                    st.session_state.user = user
                    st.rerun()
                except AccessDeniedError as exc:
                    st.error(str(exc))
        else:
            st.write(f"Usuário: {user['name']}")
            st.write(f"Perfil: {user['role']}")
            if st.button("Sair"):
                st.session_state.user = None
                st.rerun()

    if user is None:
        st.info("Faça login para acessar o núcleo da operação da fila.")
        st.subheader("Usuários de exemplo")
        for record in backend.users.values():
            st.write(f"- {record.name} ({record.role}) — {record.email}")
        return

    if user["role"] not in {"admin", "attendant", "user"}:
        st.error("Perfil inválido.")
        return

    establishments = backend.establishments
    services = backend.services
    queues = backend.queues

    main_tabs = st.tabs(["Cadastros", "Cliente", "Atendente", "Logs"])

    with main_tabs[0]:
        st.subheader("Estabelecimentos")
        with st.form("new_establishment"):
            name = st.text_input("Nome do estabelecimento")
            submitted = st.form_submit_button("Cadastrar estabelecimento")
            if submitted:
                try:
                    created = backend.register_establishment(name)
                    st.success(f"Estabelecimento criado: {created['name']}")
                    st.rerun()
                except InvalidQueueStateError as exc:
                    st.error(str(exc))

        st.table({"ID": [item.id for item in establishments.values()], "Nome": [item.name for item in establishments.values()]})

        st.subheader("Serviços")
        selected_establishment = st.selectbox("Estabelecimento", options=list(establishments.keys()), format_func=lambda value: establishments[value].name)
        with st.form("new_service"):
            service_name = st.text_input("Nome do serviço")
            estimated_minutes = st.number_input("Tempo estimado (minutos)", min_value=1, max_value=180, value=10)
            submitted_service = st.form_submit_button("Cadastrar serviço")
            if submitted_service:
                try:
                    created = backend.register_service(selected_establishment, service_name, int(estimated_minutes))
                    st.success(f"Serviço criado: {created['name']}")
                    st.rerun()
                except (QueueNotFoundError, InvalidQueueStateError) as exc:
                    st.error(str(exc))

        service_rows = [
            {"ID": service.id, "Estabelecimento": establishments[service.establishment_id].name, "Nome": service.name, "Tempo estimado": service.estimated_minutes}
            for service in services.values()
        ]
        st.table(service_rows)

        st.subheader("Filas")
        selected_service = st.selectbox("Serviço", options=list(services.keys()), format_func=lambda value: services[value].name)
        with st.form("new_queue"):
            queue_name = st.text_input("Nome da fila")
            queue_status = st.selectbox("Status inicial", options=["open", "closed"])
            submitted_queue = st.form_submit_button("Cadastrar fila")
            if submitted_queue:
                try:
                    created = backend.register_queue(selected_service, queue_name, queue_status)
                    st.success(f"Fila criada: {created['name']}")
                    st.rerun()
                except (QueueNotFoundError, InvalidQueueStateError) as exc:
                    st.error(str(exc))

        queue_rows = [
            {"ID": queue.id, "Serviço": services[queue.service_id].name, "Nome": queue.name, "Status": queue.status}
            for queue in queues.values()
        ]
        st.table(queue_rows)

    with main_tabs[1]:
        st.subheader("Emitir senha")
        queue_choice = st.selectbox("Selecione a fila", options=list(queues.keys()), format_func=lambda value: f"{queues[value].name} ({services[queues[value].service_id].name})")
        if st.button("Gerar senha"):
            try:
                ticket = backend.emit_ticket(queue_choice, user["id"])
                st.success(f"Senha emitida: {ticket['number']} — status {ticket['status']}")
                st.rerun()
            except (QueueNotFoundError, InvalidQueueStateError) as exc:
                st.error(str(exc))

        st.subheader("Senhas recentes")
        recent_tickets = [
            {
                "ID": item.id,
                "Número": item.number,
                "Fila": queues[item.queue_id].name,
                "Status": item.status,
                "Criação": item.created_at,
            }
            for item in sorted(backend.tickets.values(), key=lambda ticket: ticket.number, reverse=True)[:10]
        ]
        st.table(recent_tickets)

    with main_tabs[2]:
        st.subheader("Painel do atendente")
        attendant_establishment = user.get("establishment_id")
        if user["role"] != "attendant":
            st.warning("Este painel é exclusivo para atendentes.")
        else:
            establishment_queues = backend.list_queues_for_establishment(attendant_establishment)
            if not establishment_queues:
                st.info("Nenhuma fila disponível para este estabelecimento.")
            else:
                queue_id = st.selectbox(
                    "Fila sob sua responsabilidade",
                    options=[item["id"] for item in establishment_queues],
                    format_func=lambda value: next(item["name"] for item in establishment_queues if item["id"] == value),
                )
                if st.button("Chamar próxima senha"):
                    try:
                        ticket = backend.call_next_token(queue_id, user["id"])
                        st.success(f"Senha chamada: {ticket['number']} — status {ticket['status']}")
                        st.rerun()
                    except (AccessDeniedError, QueueNotFoundError, InvalidQueueStateError) as exc:
                        st.error(str(exc))

                st.subheader("Status da fila")
                for item in establishment_queues:
                    if item["id"] == queue_id:
                        st.write(item)
                        break

                tickets_in_queue = [
                    {
                        "ID": item.id,
                        "Número": item.number,
                        "Status": item.status,
                        "Usuário": item.user_id,
                        "Chamado em": item.called_at,
                    }
                    for item in backend.tickets.values()
                    if item.queue_id == queue_id
                ]
                st.table(sorted(tickets_in_queue, key=lambda item: item["Número"]))

                if st.button("Finalizar atendimento atual"):
                    queue_ticket = next(
                        (item for item in sorted(backend.tickets.values(), key=lambda ticket: ticket.number) if item.queue_id == queue_id and item.status == "called"),
                        None,
                    )
                    if queue_ticket is None:
                        st.warning("Nenhuma senha chamada para finalizar neste momento.")
                    else:
                        try:
                            result = backend.complete_service(queue_ticket.id, user["id"])
                            st.success(f"Atendimento finalizado para a senha {result['number']}")
                            st.rerun()
                        except (AccessDeniedError, QueueNotFoundError, InvalidQueueStateError) as exc:
                            st.error(str(exc))

    with main_tabs[3]:
        st.subheader("Histórico de eventos")
        logs = backend.list_logs()
        if not logs:
            st.info("Ainda não há eventos registrados.")
        else:
            st.table([
                {"Ação": item["action"], "Usuário": item["user_id"], "Momento": item["created_at"], "Dados": str(item["metadata"])}
                for item in logs[-20:]
            ])

    st.caption("As regras de negócio e validações da fila são centralizadas no backend do Xano e consumidas pela interface em Streamlit.")


if __name__ == "__main__":
    main()
