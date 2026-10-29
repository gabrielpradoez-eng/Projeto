import streamlit as st
from views.presentation import apply_theme

st.set_page_config(page_title="FilaSmart | Totem", page_icon=":material/touch_app:")
apply_theme()

page = st.navigation(
    [
        st.Page("app_pages/totem.py", title="Totem", icon=":material/touch_app:"),
        st.Page(
            "app_pages/tracking.py",
            title="Acompanhar senha",
            icon=":material/pending_actions:",
        ),
    ],
    position="top",
)
page.run()
