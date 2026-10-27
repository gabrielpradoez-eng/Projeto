from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_completion_checks_attendant_and_scope_before_any_write():
    source = (ROOT / "xano/api/queue_management/complete_POST.xs").read_text()
    guards = source.split("db.transaction", 1)[0]
    assert '$auth.role == "atendente"' in guards
    assert "$atendente.ativo" in guards
    assert "$atendimento.atendente_id == $atendente.id" in guards
    assert "$atendimento.estabelecimento_id == $atendente.estabelecimento_id" in guards
    assert "$atendimento.ended_at == null" in guards
    assert "$senha != null" in guards


def test_authentication_audit_does_not_log_password_bearing_records():
    for relative in ["auth/login_POST.xs", "auth/signup_POST.xs", "reset/update_password_POST.xs", "reset/magic_link_login_POST.xs"]:
        source = (ROOT / "xano/api/authentication" / relative).read_text()
        assert "metadata: $user" not in source
        assert "metadata: {usuario_id:" in source
