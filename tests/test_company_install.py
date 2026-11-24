from unittest.mock import Mock
import pytest
from streamlit.testing.v1 import AppTest
from company_settings import company_settings
from backend_queue import QueueBackend, InvalidQueueStateError


def test_company_name_is_literal_and_color_is_validated(monkeypatch):
    monkeypatch.setattr('company_settings.st.secrets', {'company':{'name':'<b>Empresa</b>', 'primary_color':'red; display:none', 'catalog_enabled':'true'}})
    assert company_settings()['primary_color'] == '#2457A7'
    assert not company_settings()['catalog_enabled']
    app = AppTest.from_string('from views.presentation import render_brand; render_brand()').run()
    assert not app.exception
    assert '&lt;b&gt;Empresa&lt;/b&gt;' in app.markdown[0].value


def test_catalog_rejects_malformed_response_and_does_not_retry(monkeypatch):
    monkeypatch.setattr('backend_queue.st.secrets', {'xano':{'base_url':'https://xano.invalid/api:q'}})
    backend = QueueBackend()
    post = Mock(return_value=Mock(status_code=200,json=lambda:{'filas':[{'fila_id':True}]}))
    monkeypatch.setattr('backend_queue.requests.post',post)
    with pytest.raises(InvalidQueueStateError):backend.company_catalog(token='test')
    assert post.call_count==1
    assert post.call_args.kwargs['headers']['Authorization']=='Bearer test'


def test_catalog_hidden_from_non_admin_and_until_activated(monkeypatch):
    app=AppTest.from_string('''
import streamlit as st
from views.company_catalog import render_company_catalog
render_company_catalog(st.session_state.backend, {'role':'attendant'})
''')
    backend=Mock()
    app.session_state['backend']=backend
    app.run()
    assert not app.exception and not app.form
    backend.company_catalog.assert_not_called()


def test_admin_catalog_form_sends_trimmed_values(monkeypatch):
    monkeypatch.setattr('views.company_catalog.company_settings',lambda:{'catalog_enabled':True})
    client=Mock()
    client.list_options.return_value={'estabelecimentos':[{'id':1,'nome':'Empresa'}]}
    monkeypatch.setattr('views.company_catalog.get_analytics_client',lambda **kw:client)
    backend=Mock()
    backend.company_catalog.return_value=[]
    app=AppTest.from_string('''
import streamlit as st
from views.company_catalog import render_company_catalog
render_company_catalog(st.session_state.backend, {'role':'admin','authToken':'admin-test'})
''')
    app.session_state['backend']=backend
    app.run()
    app.text_input[0].set_value(' Consulta ')
    app.text_input[1].set_value(' Recepção ')
    app.button[0].click().run()
    assert not app.exception and app.success
    sent=next(c.kwargs for c in backend.company_catalog.call_args_list if 'payload' in c.kwargs)
    assert sent['payload']['servico_nome']=='Consulta'
    assert sent['payload']['fila_nome']=='Recepção'
    assert sent['payload']['estabelecimento_id']==1


def test_catalog_export_requires_admin_and_verifies_queue_site_before_writes():
    from pathlib import Path
    source=Path('xano/api/queue_management/admin/catalog_POST.xs').read_text()
    assert 'auth = "usuarios"' in source
    assert source.index('$actor.role == "admin"') < source.index('db.transaction')
    assert source.index('$service.estabelecimento_id == $site.id') < source.index('db.edit servicos')
    assert '$actor.estabelecimento_id == $input.estabelecimento_id' in source
    assert 'db.delete' not in source
    assert 'lock = true' in source


@pytest.mark.parametrize('value', [None, 'Empresa', 42, []])
def test_malformed_company_section_keeps_safe_defaults(monkeypatch, value):
    monkeypatch.setattr('company_settings.st.secrets', {'company':value})
    assert company_settings()['name'] == 'FilaSmart'
    assert company_settings()['catalog_enabled'] is False


def test_catalog_refreshes_after_creation_without_repeating_write(monkeypatch):
    monkeypatch.setattr('views.company_catalog.company_settings',lambda:{'catalog_enabled':True})
    client=Mock()
    client.list_options.return_value={'estabelecimentos':[{'id':1,'nome':'Empresa'}]}
    monkeypatch.setattr('views.company_catalog.get_analytics_client',lambda **kw:client)
    row={'fila_id':5,'servico_id':5,'estabelecimento_id':1,'estabelecimento_nome':'Empresa',
         'servico_nome':'Consulta','fila_nome':'Recepção','tempo_estimado':10,'status':'aberta'}
    backend=Mock()
    persisted = []
    def catalog(**kwargs):
        if 'payload' in kwargs:
            persisted[:] = [row]
        return list(persisted)
    backend.company_catalog.side_effect = catalog
    app=AppTest.from_string('''
import streamlit as st
from views.company_catalog import render_company_catalog
render_company_catalog(st.session_state.backend, {'role':'admin','authToken':'admin-test'})
''')
    app.session_state['backend']=backend
    app.run()
    app.text_input[0].set_value('Consulta')
    app.text_input[1].set_value('Recepção')
    app.button[0].click().run()
    assert not app.exception
    assert app.session_state['company_catalog_selection']==5
    assert len([c for c in backend.company_catalog.call_args_list if 'payload' in c.kwargs])==1
    assert app.success


def test_removed_queue_selection_is_reset_before_rendering(monkeypatch):
    monkeypatch.setattr('views.company_catalog.company_settings',lambda:{'catalog_enabled':True})
    client=Mock()
    client.list_options.return_value={'estabelecimentos':[{'id':1,'nome':'Empresa'}]}
    monkeypatch.setattr('views.company_catalog.get_analytics_client',lambda **kw:client)
    backend=Mock()
    backend.company_catalog.return_value=[]
    app=AppTest.from_string('''
import streamlit as st
from views.company_catalog import render_company_catalog
render_company_catalog(st.session_state.backend, {'role':'admin','authToken':'admin-test'})
''')
    app.session_state['backend']=backend
    app.session_state['company_catalog_selection']=987
    app.run()
    assert not app.exception
    assert app.session_state['company_catalog_selection']==0
    backend.company_catalog.assert_called_once_with(token='admin-test')
