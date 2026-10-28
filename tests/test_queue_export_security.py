from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_completion_checks_attendant_and_scope_before_any_write():
    source = (ROOT / "xano/api/queue_management/complete_POST.xs").read_text()
    guards = source.split("db.transaction", 1)[0]
    assert '$actor.role == "atendente"' in guards
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


def test_authorization_loads_role_from_database_instead_of_auth_context():
    sources = list((ROOT / "xano/api").rglob("*.xs"))
    checked = 0
    for path in sources:
        source = path.read_text()
        assert "$auth.role" not in source
        assert "$auth.estabelecimento_id" not in source
        if "$actor.role" in source:
            checked += 1
            assert source.index("db.get usuarios") < source.index("$actor.role")
            assert 'field_value = $auth.id' in source
            assert 'output = ["id", "role", "estabelecimento_id"]' in source
    assert checked == 9


def test_non_paginated_queries_are_iterated_as_arrays():
    for relative, names in {
        "complete_POST.xs": ["rastreamentos"],
        "attendant/dashboard_GET.xs": ["filas", "servicos"],
        "totem/queues_GET.xs": ["filas"],
        "analytics/options_GET.xs": ["estabelecimentos", "servicos", "filas"],
    }.items():
        source = (ROOT / "xano/api/queue_management" / relative).read_text()
        for name in names:
            assert f"${name}.items" not in source


def test_attendant_dashboard_limits_services_before_loading_queues():
    source = (ROOT / "xano/api/queue_management/attendant/dashboard_GET.xs").read_text()
    assert "$db.servicos.estabelecimento_id == $atendente.estabelecimento_id" in source
    assert "$db.filas.servico_id == $servico.id" in source
    assert "join =" not in source


def test_join_queries_reference_their_declared_aliases():
    for relative in ["analytics/report_POST.xs", "totem/queues_GET.xs", "totem/issue_POST.xs"]:
        source = (ROOT / "xano/api/queue_management" / relative).read_text()
        assert "$db.servicos." not in source
        assert "$db.servico.estabelecimento_id" in source
    report = (ROOT / "xano/api/queue_management/analytics/report_POST.xs").read_text()
    assert "$db.senha.fila_id == $fila.id" in report
    assert "servico_nome: $db.servico.nome" in report
    assert "$input.servico_id == 0" in report
    assert "$input.fila_id == 0" in report
