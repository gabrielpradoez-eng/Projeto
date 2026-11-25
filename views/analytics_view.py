from __future__ import annotations

import json
from datetime import date, datetime, time, timedelta, timezone
from typing import Any

import streamlit as st

from streamlit_xano import analytics_login, get_analytics_client
from xano_client import XanoClientError, XanoConfigurationError
from views.presentation import format_timestamp, select_or_show


def _utc_midnight(value: date) -> str:
    return datetime.combine(value, time.min, tzinfo=timezone.utc).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )


def _show_login() -> None:
    st.title("Relatórios de atendimento")
    st.caption("Acesse com sua conta administrativa do Xano.")
    with st.form("analytics_login_form"):
        email = st.text_input("E-mail", autocomplete="username")
        password = st.text_input(
            "Senha", type="password", autocomplete="current-password"
        )
        submitted = st.form_submit_button("Entrar", type="primary")
    if not submitted:
        return
    try:
        st.session_state.analytics_auth_token = analytics_login(email.strip(), password)
        st.session_state.pop("analytics_report", None)
        st.rerun()
    except XanoConfigurationError as exc:
        st.error(str(exc))
    except XanoClientError:
        st.error(
            "Não foi possível autenticar. Verifique as credenciais ou a configuração Xano."
        )


def _report_form(options: dict[str, Any], *, centralized: bool = False) -> tuple[bool, dict[str, Any] | None]:
    establishments = options["estabelecimentos"]
    queue_options = options["filas"]
    if not establishments:
        st.session_state.pop("analytics_report", None)
        st.info("Nenhum estabelecimento está disponível para esta conta.")
        return False, None

    establishment_by_id = {item["id"]: item for item in establishments}
    utc_today = datetime.now(timezone.utc).date()
    default_start = utc_today - timedelta(days=6)
    default_end = utc_today + timedelta(days=1)

    if st.session_state.get("analytics_establishment_id") not in establishment_by_id:
        st.session_state["analytics_establishment_id"] = next(iter(establishment_by_id))
        st.session_state.pop("analytics_report", None)
    filter_area = st.expander("Filtros do relatório", expanded=True) if centralized else st.sidebar
    with filter_area:
        st.caption("Defina o período e o escopo da consulta.")
        with st.container():
            scope_column, period_column = st.columns(2, gap="medium")
            establishment_id = select_or_show(
                "Estabelecimento",
                options=list(establishment_by_id),
                container=scope_column,
                format_func=lambda item_id: establishment_by_id[item_id]["nome"],
                key="analytics_establishment_id",
            )
            period_start = period_column.date_input(
                "Data inicial (UTC)",
                value=default_start,
                key="analytics_period_start",
            )
            period_end = period_column.date_input(
                "Data limite (UTC)",
                help="O relatório inclui a data inicial e termina antes desta data. Para incluir o dia 25, escolha 26 como limite.",
                value=default_end,
                key="analytics_period_end",
            )

            services_by_id: dict[int, str] = {}
            eligible_queues = []
            for item in queue_options:
                if item["estabelecimento_id"] == establishment_id:
                    services_by_id.setdefault(item["servico_id"], item["servico_nome"])
                    eligible_queues.append(item)

            service_choices: list[int | None] = [None, *services_by_id]
            if st.session_state.get("analytics_service_id") not in service_choices:
                st.session_state["analytics_service_id"] = None
                st.session_state.pop("analytics_report", None)
            service_id = scope_column.selectbox(
                "Serviço",
                options=service_choices,
                format_func=lambda item_id: (
                    "Todos os serviços" if item_id is None else services_by_id[item_id]
                ),
                key="analytics_service_id",
            )

            service_queues = [
                item
                for item in eligible_queues
                if service_id is None or item["servico_id"] == service_id
            ]
            queue_choices: list[int | None] = [
                None,
                *[item["fila_id"] for item in service_queues],
            ]
            if st.session_state.get("analytics_queue_id") not in queue_choices:
                st.session_state["analytics_queue_id"] = None
            queue_by_id = {item["fila_id"]: item for item in service_queues}
            queue_id = select_or_show(
                "Fila",
                options=[service_queues[0]["fila_id"]] if service_id is not None and len(service_queues) == 1 else queue_choices,
                container=scope_column,
                format_func=lambda item_id: (
                    "Todas as filas"
                    if item_id is None
                    else f"{queue_by_id[item_id]['servico_nome']} · "
                    f"{queue_by_id[item_id]['fila_nome']}"
                ),
                key="analytics_queue_id",
            )
            st.caption("Período em UTC: a data inicial é incluída; a data limite não é incluída. Para consultar um dia, use o dia seguinte como limite. UTC difere do horário de São Paulo.")
            submitted = st.button("Gerar relatório", type="primary")

    if not submitted:
        return False, None
    if period_start >= period_end:
        st.error("A data inicial deve ser anterior à data limite (não incluída).")
        return True, None

    return True, {
        "estabelecimento_id": establishment_id,
        "period_start": _utc_midnight(period_start),
        "period_end": _utc_midnight(period_end),
        "servico_id": service_id,
        "fila_id": queue_id,
    }


def _chart_day(value):
    # Display conversion only; backend order and aggregated values are unchanged.
    try:
        return datetime.strptime(format_timestamp(value, zone="UTC"), "%d/%m/%Y às %H:%M:%S").date()
    except ValueError:
        return None


def _render_report(report: dict[str, Any]) -> None:
    summary = report["summary"]
    has_events = any(
        summary.get(key, 0) > 0 for key in ("emitidas", "chamadas", "concluidas")
    )
    st.caption(
        f"Período consultado: {format_timestamp(report['filters']['period_start'], zone='UTC')} UTC "
        f"até {format_timestamp(report['filters']['period_end'], zone='UTC')} UTC (limite não incluído). "
        f"Gerado em {format_timestamp(report['generated_at'])} · horário de São Paulo."
    )

    with st.container(horizontal=True):
        st.metric("Senhas emitidas", summary.get("emitidas", 0), border=True)
        st.metric("Senhas chamadas", summary.get("chamadas", 0), border=True)
        st.metric("Atendimentos concluídos", summary.get("concluidas", 0), border=True)
        completion_rate = summary.get("taxa_conclusao_coorte_pct")
        st.metric(
            "Senhas do período concluídas",
            f"{completion_rate}%" if completion_rate is not None else "Sem dados",
            help="Percentual das senhas emitidas no período que já estão concluídas, mesmo que a conclusão tenha ocorrido depois. Não é a divisão dos eventos de conclusão pelas emissões do período.",
            border=True,
        )

    with st.container(horizontal=True):
        wait_average = summary.get("espera_media_minutos")
        st.metric(
            "Espera média",
            f"{wait_average} min" if wait_average is not None else "Sem amostras",
            border=True,
        )
        st.caption(f"Amostras de espera: {summary.get('espera_amostras', 0)}")
        service_average = summary.get("duracao_media_minutos")
        st.metric(
            "Duração média",
            f"{service_average} min"
            if service_average is not None
            else "Sem amostras",
            border=True,
        )
        st.caption(f"Amostras de duração: {summary.get('duracao_amostras', 0)}")

    cohort = summary.get("coorte_status", {})
    st.subheader("Situação atual das senhas emitidas no período")
    with st.container(horizontal=True):
        st.metric("Aguardando", cohort.get("aguardando", 0), border=True)
        st.metric("Chamados", cohort.get("chamado", 0), border=True)
        st.metric("Concluídos", cohort.get("concluido", 0), border=True)
        st.metric("Cancelados", cohort.get("cancelado", 0), border=True)

    if not has_events:
        st.info("Sem eventos para os filtros e período selecionados.")

    daily = report["daily"]
    st.subheader("Atividade diária")
    if daily and has_events:
        st.line_chart(
            [{"Dia (UTC)": _chart_day(row["bucket_start"]),
              "Emitidas": row["emitidas"], "Chamadas": row["chamadas"], "Concluídas": row["concluidas"]} for row in daily],
            x="Dia (UTC)",
            y=["Emitidas", "Chamadas", "Concluídas"],
            alt="Volume diário de senhas emitidas, chamadas e concluídas",
        )
    elif not daily and has_events:
        st.info("Sem eventos para os filtros e período selecionados.")

    st.subheader("Detalhamento por serviço e fila")
    if report["breakdown"]:
        breakdown_columns = (
            "servico_nome",
            "fila_nome",
            "emitidas",
            "chamadas",
            "concluidas",
            "espera_media_minutos",
            "espera_amostras",
            "duracao_media_minutos",
            "duracao_amostras",
            "coorte_aguardando",
            "coorte_chamado",
            "coorte_concluido",
            "coorte_cancelado",
        )
        labels = dict(zip(breakdown_columns, (
            "Serviço", "Fila", "Emitidas", "Chamadas", "Concluídas", "Espera média (min)",
            "Senhas usadas na média de espera", "Duração média (min)", "Atendimentos usados na média de duração",
            "Do período: aguardando", "Do período: chamadas", "Do período: concluídas", "Do período: canceladas",
        )))
        st.table(
            [
                {labels[key]: row.get(key) for key in breakdown_columns}
                for row in report["breakdown"]
            ]
        )
    else:
        st.info("Não há linhas de detalhamento para este relatório.")


def render_analytics_view(*, centralized: bool = False) -> None:
    if centralized:
        user = st.session_state.get("user") or {}
        if user.get("role") != "admin" or not st.session_state.get("authToken"):
            st.error("Esta conta não tem permissão administrativa para consultar relatórios.")
            return
        st.session_state.analytics_auth_token = st.session_state["authToken"]
    if not st.session_state.get("analytics_auth_token"):
        _show_login()
        return

    st.title("Relatórios de atendimento")
    with st.container(horizontal=True, horizontal_alignment="right"):
        st.caption("Métricas calculadas pelo Xano")
        if not centralized and st.button("Sair", icon=":material/logout:"):
            st.session_state.pop("analytics_auth_token", None)
            st.session_state.pop("analytics_report", None)
            st.rerun()

    try:
        analytics_client = get_analytics_client()
        with st.spinner("Carregando filtros autorizados..."):
            analytics_options = analytics_client.list_options()
    except XanoConfigurationError as exc:
        st.session_state.pop("analytics_report", None)
        st.error(str(exc))
        return
    except XanoClientError as exc:
        st.session_state.pop("analytics_report", None)
        if getattr(exc, "status_code", None) == 403:
            st.error(
                "Esta conta não tem permissão administrativa para consultar relatórios."
            )
        else:
            st.error("Não foi possível carregar as opções analíticas do Xano.")
        return

    # Ignore ordering, but discard reports when labels, identities or allowed scope change.
    signature = tuple(
        (key, tuple(sorted(json.dumps(row, sort_keys=True) for row in analytics_options[key])))
        for key in ("estabelecimentos", "filas")
    )
    if st.session_state.get("analytics_options_signature") != signature:
        st.session_state.pop("analytics_report", None)
    st.session_state["analytics_options_signature"] = signature
    submitted, filters = _report_form(analytics_options, centralized=centralized)
    if submitted:
        st.session_state.pop("analytics_report", None)
        if filters is not None:
            try:
                with st.spinner("Consultando relatório no Xano..."):
                    st.session_state.analytics_report = (
                        analytics_client.fetch_report(filters)
                    )
            except XanoClientError:
                st.error(
                    "Não foi possível gerar o relatório. Tente novamente ou reduza o período."
                )

    report = st.session_state.get("analytics_report")
    if report is None:
        st.info("Selecione os filtros e gere um relatório.")
    else:
        _render_report(report)
