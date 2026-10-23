import streamlit as st

from views.analytics_view import render_analytics_view


st.set_page_config(
    page_title="FilaSmart | Relatórios",
    page_icon=":material/analytics:",
    layout="wide",
    initial_sidebar_state="expanded",
)

render_analytics_view()
