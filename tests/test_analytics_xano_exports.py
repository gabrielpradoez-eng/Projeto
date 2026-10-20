from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_export(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def test_analytics_options_require_admin_and_limit_establishment_scope():
    source = read_export("xano/api/queue_management/analytics/options_GET.xs")

    assert 'auth = "usuarios"' in source
    assert '$auth.role == "admin"' in source
    assert "$auth.estabelecimento_id == null" in source
    assert "$db.estabelecimentos.id == $auth.estabelecimento_id" in source
    assert "$db.servicos.estabelecimento_id == $estabelecimento.id" in source
    assert "$db.filas.servico_id == $servico.id" in source


def test_analytics_options_return_only_filter_labels_and_ids():
    source = read_export("xano/api/queue_management/analytics/options_GET.xs")
    response = source.split("response =", 1)[1]

    assert "estabelecimentos: $estabelecimentos_options" in response
    assert "filas            : $filas_options" in response
    assert "password" not in response
    assert "email" not in response
    assert "usuario_id" not in response


def test_analytics_report_validates_admin_scope_and_utc_range():
    source = read_export("xano/api/queue_management/analytics/report_POST.xs")

    assert 'auth = "usuarios"' in source
    assert '$auth.role == "admin"' in source
    assert "$auth.estabelecimento_id == $input.estabelecimento_id" in source
    assert "$input.period_start < $input.period_end" in source
    assert "$period_ms <= 2678400000" in source
    assert "$db.servicos.estabelecimento_id == $input.estabelecimento_id" in source
    assert "$input.servico_id == null" in source
    assert "$input.fila_id == null" in source
    assert "$filas.items|count <= 100" in source


def test_analytics_report_uses_canonical_event_timestamps_and_duration_formulas():
    source = read_export("xano/api/queue_management/analytics/report_POST.xs")

    assert "$db.senhas.created_at >= $input.period_start" in source
    assert "$db.senhas.created_at < $input.period_end" in source
    assert "$db.senhas.chamado_at >= $input.period_start" in source
    assert "$db.senhas.chamado_at < $input.period_end" in source
    assert "$db.senhas.concluido_at >= $input.period_start" in source
    assert "$db.senhas.concluido_at < $input.period_end" in source
    assert "($$.chamado_at|to_ms) - ($$.created_at|to_ms)" in source
    assert "($$.ended_at|to_ms) - ($$.started_at|to_ms)" in source


def test_analytics_report_returns_samples_null_means_and_cohort_denominator():
    source = read_export("xano/api/queue_management/analytics/report_POST.xs")

    assert ": null" in source
    assert "espera_amostras" in source
    assert "duracao_amostras" in source
    assert "$total_issued > 0" in source
    assert "$cohort_completed_total / $total_issued" in source
    assert "coorte_cancelado" in source


def test_analytics_report_daily_buckets_are_computed_by_xano_for_each_event():
    source = read_export("xano/api/queue_management/analytics/report_POST.xs")

    assert "var $day_offsets" in source
    assert "var $daily_series" in source
    assert "$input.period_start|add_secs_to_timestamp:($day_offset * 86400)" in source
    assert "$db.senhas.created_at >= $bucket_start && $db.senhas.created_at < $bucket_end" in source
    assert "$db.senhas.chamado_at >= $bucket_start && $db.senhas.chamado_at < $bucket_end" in source
    assert "$db.senhas.concluido_at >= $bucket_start && $db.senhas.concluido_at < $bucket_end" in source
    assert "daily       : $daily_series" in source


def test_analytics_breakdown_returns_backend_means_and_sample_counts():
    source = read_export("xano/api/queue_management/analytics/report_POST.xs")

    assert "espera_media_minutos  : $queue_wait_average_minutes" in source
    assert "duracao_media_minutos : $queue_service_average_minutes" in source
    assert "espera_media_minutos: $$.espera_media_minutos" in source
    assert "duracao_media_minutos: $$.duracao_media_minutos" in source
    assert "espera_amostras     : $$.espera_amostras" in source
    assert "duracao_amostras    : $$.duracao_amostras" in source
    response = source.split("response =", 1)[1]
    assert "espera_total_ms" not in response
    assert "duracao_total_ms" not in response


def test_analytics_response_is_aggregated_and_backend_ordered():
    source = read_export("xano/api/queue_management/analytics/report_POST.xs")
    response = source.split("response =", 1)[1]

    assert 'sort = {nome: "asc"}' in source
    assert "value = [0, 1, 2, 3, 4, 5, 6" in source
    assert "daily       : $daily_series" in response
    for individual_field in (
        "ticket_id",
        "senha_id",
        "usuario_id",
        "email",
        "telefone",
        "atendente_nome",
    ):
        assert individual_field not in response