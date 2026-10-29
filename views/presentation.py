from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

import streamlit as st


def apply_theme() -> None:
    styles = (Path(__file__).resolve().parents[1] / "assets" / "styles.css").read_text()
    st.markdown(f"<style>{styles}</style>", unsafe_allow_html=True)


def render_brand() -> None:
    st.markdown(
        '<div class="fs-brand"><span class="fs-mark">F</span>'
        '<div><strong>FilaSmart</strong><small>GESTÃO DE ATENDIMENTO</small></div></div>',
        unsafe_allow_html=True,
    )


_VIEW_COPY = {
    "Totem": ("AUTOATENDIMENTO", "Seu atendimento começa aqui.", "Escolha o serviço, retire sua senha e acompanhe cada etapa."),
    "Cliente": ("ÁREA DO CLIENTE", "Mais tranquilidade para esperar.", "Retire sua senha e consulte o andamento sem sair desta tela."),
    "Acompanhar senha": ("MINHA SENHA", "Saiba quando é a sua vez.", "Consulte a posição e o status da sua senha com atualização automática."),
    "Painel TV": ("PAINEL DE CHAMADAS", "Fique de olho na sua vez.", "Confira a última senha chamada e dirija-se ao guichê indicado."),
    "Administração": ("CENTRAL DE OPERAÇÕES", "Um atendimento mais organizado.", "Acesse sua conta para consultar filas e conduzir os atendimentos."),
    "Relatórios": ("INTELIGÊNCIA DA OPERAÇÃO", "Transforme dados em decisões.", "Explore volume, espera e conclusão dos atendimentos por período."),
}


def render_intro(view: str) -> None:
    eyebrow, title, description = _VIEW_COPY[view]
    st.markdown(
        f'<section class="fs-hero"><div><span class="fs-eyebrow">{eyebrow}</span>'
        f'<h1>{title}</h1><p>{description}</p></div>'
        '<div class="fs-hero-art" aria-hidden="true"><span>01</span><span>02</span>'
        '<span>✓</span></div></section>',
        unsafe_allow_html=True,
    )


def format_timestamp(value: object) -> str:
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
        return parsed.astimezone(ZoneInfo("America/Sao_Paulo")).strftime("%d/%m/%Y às %H:%M:%S")
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
