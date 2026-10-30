from streamlit.testing.v1 import AppTest


def test_customer_sees_actionable_message_without_debug_payload():
    app = AppTest.from_string('''
import streamlit as st
from views.issue_error import render_ticket_issue_error
from xano_client import QueueUnavailableError
st.session_state.user = {"role": "user"}
render_ticket_issue_error(QueueUnavailableError(
    status_code=400, api_code="INTERNAL_DEBUG_CODE", api_message="Fila fechada.",
    api_body='{"internal_debug": "details"}'
))
''').run()
    assert not app.exception
    assert app.warning[0].value == "Fila fechada."
    assert not app.code
    assert not app.error
    assert not app.expander
