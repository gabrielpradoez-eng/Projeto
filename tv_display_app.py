import streamlit as st

from views.display_view import render_display_view
from views.presentation import apply_theme


st.set_page_config(
    page_title="FilaSmart | Painel de chamadas",
    page_icon=":material/campaign:",
    layout="wide",
    initial_sidebar_state="collapsed",
)

apply_theme()
render_display_view()
