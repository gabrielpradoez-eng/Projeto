"""Configuração de uma instalação independente; nunca seleciona empresa pelo navegador."""
import re
from collections.abc import Mapping
import streamlit as st


def company_settings():
    try:
        config = st.secrets.get('company', {})
    except FileNotFoundError:
        config = {}
    if not isinstance(config, Mapping):
        config = {}
    name = config.get('name', 'FilaSmart')
    if not isinstance(name, str) or not name.strip():
        name = 'FilaSmart'
    color = config.get('primary_color', '#2457A7')
    if not isinstance(color, str) or not re.fullmatch(r'#[0-9a-fA-F]{6}', color):
        color = '#2457A7'
    return {'name': name.strip()[:80], 'primary_color': color,
            'catalog_enabled': config.get('catalog_enabled') is True}
