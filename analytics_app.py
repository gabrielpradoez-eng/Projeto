from __future__ import annotations

from datetime import date, datetime, time, timedelta, timezone
from typing import Any

import streamlit as st

from streamlit_xano import analytics_login, get_analytics_client
from xano_client import XanoClientError, XanoConfigurationError


st.set_page_config(
    page_title="FilaSmart | Relatórios",
    page_icon=":material/analytics:",
    layout="wide",
    initial_sidebar_state="expanded",
)


def _utc_midnight(value: date) -> str:
    return datetime.combine(value, time.min, tzinfo=timezone.utc).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )


def _show_login() -> None:
    st.title("Relatórios de atendimento")
    st.caption("Acesse com sua conta administrativa do Xano.")
    with st.form("analytics_login_form"):
        email = st.text_input("E-mail", autocomplete="username")
        password = st.text_input("Senha", type="password", autocomplete="current-password")
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
        st.error("Não foi possível autenticar. Verifique as credenciais ou a configuração Xano.")


def _report_form(options: dict[str, Any]) -> tuple[bool, dict[str, Any] | None]:
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

    with st.sidebar:
        st.header("Filtros")
        with st.form("analytics_filters"):
            establishment_id = st.selectbox(
                "Estabelecimento",
                options=list(establishment_by_id),
                format_func=lambda item_id: establishment_by_id[item_id]["nome"],
                key="analytics_establishment_id",
            )
            period_start = st.date_input(
                "Data inicial (UTC)",
                value=default_start,
                key="analytics_period_start",
            )
            period_end = st.date_input(
                "Data final exclusiva (UTC)",
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
            service_id = st.selectbox(
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
            queue_id = st.selectbox(
                "Fila",
                options=queue_choices,
                format_func=lambda item_id: (
                    "Todas as filas"
                    if item_id is None
                    else f"{queue_by_id[item_id]['servico_nome']} · {queue_by_id[item_id]['fila_nome']}"
                ),
                key="analytics_queue_id",
            )
            submitted = st.form_submit_button("Gerar relatório", type="primary")

    if not submitted:
        return False, None
    if period_start >= period_end:
        st.error("A data inicial deve ser anterior à data final exclusiva.")
        return True, None

    return True, {
        "estabelecimento_id": establishment_id,
        "period_start": _utc_midnight(period_start),
        "period_end": _utc_midnight(period_end),
        "servico_id": service_id,
        "fila_id": queue_id,
    }


def _render_report(report: dict[str, Any]) -> None:
    summary = report["summary"]
    has_events = any(
        summary.get(key, 0) > 0 for key in ("emitidas", "chamadas", "concluidas")
    )
    st.caption(
        f"Período UTC: {report['filters']['period_start']} até "
        f"{report['filters']['period_end']} (fim exclusivo) · "
        f"Gerado: {report['generated_at']}"
    )

    with st.container(horizontal=True):
        st.metric("Senhas emitidas", summary.get("emitidas", 0), border=True)
        st.metric("Senhas chamadas", summary.get("chamadas", 0), border=True)
        st.metric("Atendimentos concluídos", summary.get("concluidas", 0), border=True)
        completion_rate = summary.get("taxa_conclusao_coorte_pct")
        st.metric(
            "Conclusão da coorte",
            f"{completion_rate}%" if completion_rate is not None else "Sem dados",
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
            f"{service_average} min" if service_average is not None else "Sem amostras",
            border=True,
        )
        st.caption(f"Amostras de duração: {summary.get('duracao_amostras', 0)}")

    cohort = summary.get("coorte_status", {})
    st.subheader("Status atual dos tickets emitidos no período")
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
            daily,
            x="bucket_start",
            y=["emitidas", "chamadas", "concluidas"],
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
        st.table(
            [
                {key: row.get(key) for key in breakdown_columns}
                for row in report["breakdown"]
            ]
        )
    else:
        st.info("Não há linhas de detalhamento para este relatório.")


if not st.session_state.get("analytics_auth_token"):
    _show_login()
    st.stop()

st.title("Relatórios de atendimento")
with st.container(horizontal=True, horizontal_alignment="right"):
    st.caption("Métricas calculadas pelo Xano")
    if st.button("Sair", icon=":material/logout:"):
        st.session_state.pop("analytics_auth_token", None)
        st.session_state.pop("analytics_report", None)
        st.rerun()

try:
    analytics_client = get_analytics_client()
    with st.spinner("Carregando filtros autorizados..."):
        analytics_options = analytics_client.list_options()
except XanoConfigurationError as exc:
    st.error(str(exc))
    st.stop()
except XanoClientError as exc:
    if getattr(exc, "status_code", None) == 403:
        st.error("Esta conta não tem permissão administrativa para consultar relatórios.")
    else:
        st.error("Não foi possível carregar as opções analíticas do Xano.")
    st.stop()

submitted, filters = _report_form(analytics_options)
if submitted:
    st.session_state.pop("analytics_report", None)
    if filters is not None:
        try:
            with st.spinner("Consultando relatório no Xano..."):
                st.session_state.analytics_report = analytics_client.fetch_report(filters)
        except XanoClientError:
            st.error("Não foi possível gerar o relatório. Tente novamente ou reduza o período.")

report = st.session_state.get("analytics_report")
if report is None:
    st.info("Selecione os filtros e gere um relatório.")
else:
    _render_report(report)