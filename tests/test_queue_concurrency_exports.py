from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / 'xano/api/queue_management'


def transaction(path):
    return (ROOT / path).read_text().split('db.transaction', 1)[1]


def test_number_allocation_locks_queue_before_reading_last_ticket():
    for path in ['join_POST.xs', 'totem/issue_POST.xs']:
        source = transaction(path)
        assert source.index('db.get filas') < source.index('lock = true') < source.index('db.query senhas')
        assert '$locked_queue.status == "aberta"' in source
        assert source.index('$locked_queue.status') < source.index('db.add senhas')


def test_call_next_selects_waiting_ticket_only_after_lock_and_active_check():
    source = transaction('call_next_POST.xs')
    assert source.index('lock = true') < source.index('as $active_ticket') < source.index('as $proxima_senha') < source.index('db.edit senhas')
    assert 'precondition ($active_ticket == null)' in source
    assert '$locked_service.estabelecimento_id == $atendente.estabelecimento_id' in source


def test_completion_rechecks_current_state_and_owner_after_lock():
    full = (ROOT / 'complete_POST.xs').read_text()
    assert '$atendimento.ended_at == 0' in full.split('db.transaction', 1)[0]
    source = transaction('complete_POST.xs')
    assert source.index('lock = true') < source.index('as $current_senha') < source.index('as $current_atendimento') < source.index('db.edit senhas')
    assert '$current_senha.status == "chamado"' in source
    assert '$current_atendimento.atendente_id == $atendente.id' in source
    assert 'field_value = $current_atendimento.id' in source


def test_attendant_registration_locks_candidate_before_granting_access():
    source = transaction('admin/attendants_POST.xs')
    assert source.index('db.get usuarios') < source.index('lock = true') < source.index('db.add atendentes')
