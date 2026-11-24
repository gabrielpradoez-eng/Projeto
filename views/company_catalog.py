"""Manutenção do catálogo; autorização definitiva no Xano."""
import streamlit as st
from backend_queue import AccessDeniedError, InvalidQueueStateError
from company_settings import company_settings
from streamlit_xano import get_analytics_client
from xano_client import XanoClientError


def render_company_catalog(backend, user):
    if user.get('role') != 'admin' or not company_settings()['catalog_enabled']:
        return
    st.subheader('Serviços e filas da empresa')
    saved_id = st.session_state.pop('_company_catalog_saved_id', None)
    if saved_id is not None:
        st.session_state['company_catalog_selection'] = saved_id
        st.success('Catálogo salvo. Dados confirmados atualizados.')
    try:
        rows = backend.company_catalog(token=user['authToken'])
        options = get_analytics_client(auth_token=user['authToken']).list_options()
    except (AccessDeniedError, InvalidQueueStateError, XanoClientError):
        st.warning('Não foi possível consultar o catálogo. Confira a implantação e tente novamente.')
        return
    sites = {r['id']: r['nome'] for r in options['estabelecimentos']}
    if not sites:
        st.info('Cadastre o estabelecimento no provisionamento inicial.')
        return
    valid_ids = [0] + [r['fila_id'] for r in rows]
    if st.session_state.get('company_catalog_selection', 0) not in valid_ids:
        st.session_state['company_catalog_selection'] = 0
    selected = st.selectbox('Serviço e fila', valid_ids,
        format_func=lambda k: 'Novo serviço e fila' if k == 0 else next(
            f"{r['estabelecimento_nome']} · {r['servico_nome']} · {r['fila_nome']} ({r['status']})"
            for r in rows if r['fila_id'] == k), key='company_catalog_selection')
    row = next((r for r in rows if r['fila_id'] == selected), None)
    if row and row['estabelecimento_id'] not in sites:
        st.warning('O estabelecimento não está mais disponível. Atualize a página.')
        return
    with st.form(f'company_catalog_{selected}'):
        site = st.selectbox('Estabelecimento do serviço', list(sites), format_func=sites.get,
            index=list(sites).index(row['estabelecimento_id']) if row else 0, disabled=bool(row))
        name = st.text_input('Nome do serviço', value=row['servico_nome'] if row else '', max_chars=100)
        minutes = st.number_input('Duração estimada (minutos)', min_value=1, max_value=1440,
            value=row['tempo_estimado'] if row else 10, step=1)
        queue = st.text_input('Nome da fila', value=row['fila_nome'] if row else '', max_chars=100)
        status = st.selectbox('Estado da fila', ['aberta', 'fechada'], index=1 if row and row['status']=='fechada' else 0)
        st.caption('Fechar uma fila pausa a operação disponível para ela; as senhas e o histórico são preservados. Alterar um serviço afeta todas as filas vinculadas a ele.')
        submitted = st.form_submit_button('Salvar serviço e fila')
    if not submitted:
        return
    if not name.strip() or not queue.strip():
        st.warning('Informe o nome do serviço e da fila.')
        return
    try:
        saved_rows = backend.company_catalog(token=user['authToken'], payload={'acao':'salvar', 'fila_id':selected,
            'estabelecimento_id':site, 'servico_nome':name.strip(), 'fila_nome':queue.strip(),
            'tempo_estimado':int(minutes), 'status':status})
    except (AccessDeniedError, InvalidQueueStateError):
        st.error('Não foi possível confirmar a alteração. Consulte o catálogo antes de tentar novamente.')
        return
    new_ids = [r['fila_id'] for r in saved_rows if r['fila_id'] not in valid_ids]
    st.session_state['_company_catalog_saved_id'] = selected or (new_ids[0] if len(new_ids) == 1 else 0)
    st.rerun()
