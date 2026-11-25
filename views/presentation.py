from __future__ import annotations

from datetime import datetime, timezone
from collections.abc import Callable
from pathlib import Path
from zoneinfo import ZoneInfo

import streamlit as st
from html import escape
from company_settings import company_settings


def apply_theme() -> None:
    settings = company_settings()
    styles = (Path(__file__).resolve().parents[1] / "assets" / "styles.css").read_text()
    st.markdown(f"<style>{styles} :root {{ --primary-color: {settings['primary_color']}; }} .fs-mark {{ background: {settings['primary_color']}; color: white; }}</style>", unsafe_allow_html=True)


def render_brand() -> None:
    name = escape(company_settings()["name"])
    initial = escape(company_settings()["name"][0].upper())
    st.markdown(
        f'<div class="fs-brand"><span class="fs-mark">{initial}</span>'
        f'<div><strong>{name}</strong><small>GESTÃO DE ATENDIMENTO</small></div></div>',
        unsafe_allow_html=True,
    )


_VIEW_COPY = {
    "Totem": ("AUTOATENDIMENTO", "Retire sua senha", "Selecione um serviço e acompanhe o atendimento com seu comprovante."),
    "Cliente": ("ÁREA DO CLIENTE", "Meu atendimento", "Emita sua senha e acompanhe a posição na fila em um único lugar."),
    "Acompanhar senha": ("ACOMPANHAMENTO", "Acompanhe sua senha", "Consulte o status e a posição na fila. As informações são atualizadas automaticamente."),
    "Painel TV": ("OPERAÇÃO", "Painel de chamadas", "Confira a senha chamada e o guichê de atendimento."),
    "Administração": ("GESTÃO", "Central de operações", "Gerencie os acessos da equipe e consulte os indicadores da operação em Relatórios."),
    "Relatórios": ("ANÁLISE", "Indicadores de atendimento", "Consulte volume, tempo de espera e conclusão por período, serviço ou fila."),
}


def _select_mobile_view() -> None:
    st.session_state["app_view"] = st.session_state["mobile_view"]


def render_mobile_navigation(allowed_views: tuple[str, ...], *, on_logout: Callable[[], None]) -> None:
    # Both widgets are built after identity verification. Synchronize before creating
    # the mobile widget, so sidebar changes and role downgrades cannot leave it stale.
    st.session_state["mobile_view"] = st.session_state["app_view"]
    with st.container(key="mobile_navigation"):
        st.selectbox("Navegar para", options=allowed_views, key="mobile_view",
                     on_change=_select_mobile_view)
        st.button("Encerrar sessão", on_click=on_logout, icon=":material/logout:",
                  use_container_width=True, key="mobile_logout")


def render_intro(view: str, *, role: str = "") -> None:
    eyebrow, title, description = _VIEW_COPY[view]
    if view == "Administração" and role == "attendant":
        eyebrow, title, description = ("OPERAÇÃO", "Central de atendimento",
            "Selecione sua fila, chame a próxima senha e acompanhe o atendimento atual.")
    st.markdown(
        f'<section class="fs-hero"><div><span class="fs-eyebrow">FILASMART / {eyebrow}</span>'
        f'<h1>{title}</h1><p>{description}</p></div>'
        '<span class="fs-workspace-label">GESTÃO DE ATENDIMENTO</span></section>',
        unsafe_allow_html=True,
    )


def format_timestamp(value: object, *, zone: str = "America/Sao_Paulo") -> str:
    try:
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            if value <= 0:
                return "Horário indisponível"
            parsed = datetime.fromtimestamp(value / 1000, tz=timezone.utc)
        elif isinstance(value, str) and value.strip():
            parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
            if parsed.tzinfo is None:
                parsed = parsed.replace(tzinfo=timezone.utc)
        else:
            return "Horário indisponível"
        return parsed.astimezone(ZoneInfo(zone)).strftime("%d/%m/%Y às %H:%M:%S")
    except (ValueError, TypeError, OverflowError, OSError):
        return "Horário indisponível"


def ticket_receipt(number: object, reference: str, service: str, queue: str) -> str:
    return (
        f"FILASMART — COMPROVANTE DE SENHA\n\nSenha: {number}\n"
        f"Serviço: {service}\nFila: {queue}\n\n"
        f"Referência de acompanhamento: {reference}\n\n"
        "Abra a opção Acompanhar senha no aplicativo e informe a referência.\n"
        "Guarde este comprovante. A referência permite consultar sua senha.\n"
        "Aguarde a chamada e dirija-se ao guichê indicado no painel.\n"
    )


def render_receipt(number: object, reference: str, service: str, queue: str, *, key: str) -> None:
    st.download_button(
        "Baixar comprovante", data=ticket_receipt(number, reference, service, queue),
        file_name="filasmart-comprovante.txt", mime="text/plain; charset=utf-8",
        on_click="ignore", icon=":material/download:", key=key,
    )


def render_status_guidance(status: str) -> None:
    messages = {
        "aguardando": "Sua senha está na fila. Aguarde a chamada no painel; a posição pode mudar conforme o atendimento.",
        "chamado": "É a sua vez! Confira o guichê no painel de chamadas e dirija-se ao atendimento.",
        "em_atendimento": "Seu atendimento está em andamento.",
        "concluido": "Atendimento concluído. Obrigado pela visita!",
        "cancelado": "Esta senha foi cancelada. Procure a equipe se precisar de ajuda.",
    }
    if status in messages:
        st.info(messages[status])


def select_or_show(label, options, *, format_func, key, container=None, help=None):
    """Present authorized single choices without an unnecessary input widget."""
    area = container if container is not None else st
    options = list(options)
    if not options:
        st.session_state.pop(key, None)
        area.caption(f"{label}: nenhuma opção disponível")
        return None
    if st.session_state.get(key) not in options:
        st.session_state[key] = options[0]
    if len(options) == 1:
        st.session_state[key] = options[0]
        area.text(f"{label}: {format_func(options[0])}")
        return options[0]
    return area.selectbox(label, options, format_func=format_func, key=key, help=help)
