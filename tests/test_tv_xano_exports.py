from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_export(relative_path):
    return (ROOT / relative_path).read_text(encoding="utf-8")


def test_display_feed_validates_hash_active_state_and_establishment_scope():
    source = read_export("xano/api/queue_management/tv/feed_POST.xs")

    assert "$input.credential|sha256" in source
    assert "$display.ativo" in source
    assert "$db.atendimentos.estabelecimento_id == $display.estabelecimento_id" in source
    assert "event_key" in source
    assert "credential_hash" not in source.split("response =", 1)[1]


def test_display_feed_orders_history_in_xano_and_limits_it_to_five():
    source = read_export("xano/api/queue_management/tv/feed_POST.xs")

    assert 'sort = {id: "desc"}' in source
    assert "per_page: 5" in source
    assert "foreach ($chamadas_recentes.items)" in source


def test_admin_provisioning_returns_raw_credential_but_stores_only_hash():
    source = read_export("xano/api/queue_management/tv/register_POST.xs")

    assert '$auth.role == "admin"' in source
    assert "$credential|sha256" in source
    assert "credential: $credential" in source
    assert "credential_hash: $credential" not in source


def test_call_operation_persists_public_snapshot_without_client_identity():
    source = read_export("xano/api/queue_management/call_next_POST.xs")
    attendance_data = source.split("db.add atendimentos", 1)[1].split("} as $atendimento", 1)[0]

    assert "estabelecimento_id: $atendente.estabelecimento_id" in attendance_data
    assert "numero_senha: $senha_atualizada.numero" in attendance_data
    assert "destino_label:" in attendance_data
    assert "display_event_key: $display_event_key" in attendance_data
    assert "usuario_id:" not in attendance_data