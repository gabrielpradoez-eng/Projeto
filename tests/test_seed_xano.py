from __future__ import annotations

import json
import re
from pathlib import Path
import sys
from unittest.mock import Mock, patch
from urllib.error import URLError

import pytest

from scripts.seed_xano import (
    SeedConfigurationError,
    SeedRequestError,
    SeedSettings,
    seed,
)
from scripts import seed_xano


ROOT = Path(__file__).resolve().parents[1]
TEST_SECRET = "x" * 40


class FakeResponse:
    def __init__(self, payload):
        self.body = json.dumps(payload).encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return False

    def read(self):
        return self.body


def valid_settings(**overrides):
    values = {
        "endpoint_url": "https://test-workspace.xano.io/api:queue/setup/seed",
        "environment": "test",
        "bootstrap_secret": TEST_SECRET,
        "admin_password": "local-test-password",
    }
    values.update(overrides)
    return SeedSettings(**values)


def valid_response(**credentials):
    result_credentials = {
        "atendente1_password": None,
        "atendente2_password": None,
        "totem_password": None,
        "tv_display": None,
    }
    result_credentials.update(credentials)
    return {
        "estabelecimento": "Matriz",
        "usuarios": [
            "admin@filasmart.com",
            "atendente1@filasmart.com",
            "atendente2@filasmart.com",
            "totem@filasmart.com",
        ],
        "filas": ["Atendimento Geral", "Preferencial"],
        "credenciais_unica_vez": result_credentials,
    }


def test_seed_requires_explicit_confirmation_before_network():
    opener = Mock()

    with pytest.raises(SeedConfigurationError, match="--confirm-test-target"):
        seed(valid_settings(), confirmed_test_target=False, opener=opener)

    opener.assert_not_called()


@pytest.mark.parametrize(
    "settings",
    [
        valid_settings(environment="production"),
        valid_settings(endpoint_url="http://test-workspace.xano.io/setup/seed"),
        valid_settings(bootstrap_secret="<configure-out-of-band>"),
    ],
)
def test_seed_settings_fail_closed_for_production_or_placeholders(settings):
    with pytest.raises(SeedConfigurationError):
        SeedSettings.from_secrets(
            {
                "xano_seed": {
                    "endpoint_url": settings.endpoint_url,
                    "environment": settings.environment,
                    "bootstrap_secret": settings.bootstrap_secret,
                    "admin_password": settings.admin_password,
                }
            }
        )


def test_seed_posts_fixed_fixture_credentials_and_validates_one_time_response():
    result = valid_response(
        atendente1_password="one-time-attendant-password",
        atendente2_password="another-one-time-password",
        totem_password="one-time-totem-password",
        tv_display="one-time-display-credential",
    )
    requests = []

    def fake_urlopen(request, timeout):
        requests.append((request, timeout))
        return FakeResponse(result)

    actual = seed(
        valid_settings(),
        confirmed_test_target=True,
        opener=fake_urlopen,
    )

    assert actual == result
    request, timeout = requests[0]
    assert request.method == "POST"
    assert timeout == 10.0
    assert json.loads(request.data) == {
        "bootstrap_secret": TEST_SECRET,
        "admin_password": "local-test-password",
    }
    assert request.full_url == valid_settings().endpoint_url


def test_seed_rejects_invalid_response_without_exposing_response_details():
    result = valid_response()
    result["estabelecimento"] = "Unexpected private payload"

    with pytest.raises(SeedRequestError, match="resposta de provisionamento inválida") as error:
        seed(
            valid_settings(),
            confirmed_test_target=True,
            opener=lambda *_args, **_kwargs: FakeResponse(result),
        )

    assert "Unexpected private payload" not in str(error.value)
    assert TEST_SECRET not in str(error.value)


def test_seed_rejects_non_string_credentials_from_response():
    result = valid_response(totem_password={"secret": "not-a-string"})

    with pytest.raises(SeedRequestError, match="resposta de provisionamento inválida"):
        seed(
            valid_settings(),
            confirmed_test_target=True,
            opener=lambda *_args, **_kwargs: FakeResponse(result),
        )


def test_seed_sanitizes_transport_errors():
    with pytest.raises(SeedRequestError, match="Não foi possível conectar") as error:
        seed(
            valid_settings(),
            confirmed_test_target=True,
            opener=Mock(side_effect=URLError(TEST_SECRET)),
        )

    assert TEST_SECRET not in str(error.value)


def test_import_manifest_classifies_every_existing_xano_export():
    manifest = (ROOT / "docs" / "xano-import-order.md").read_text(encoding="utf-8")
    listed_exports = set(re.findall(r"`(xano/[^`]+\.xs)`", manifest))
    actual_exports = {
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "xano").rglob("*.xs")
    }

    assert len(actual_exports) == 42
    assert listed_exports == actual_exports
    assert "stats_GET.xs" in manifest
    assert "Não disponibilize a versão pública/sem escopo" in manifest


def test_importable_auth_and_queue_exports_have_no_empty_table_references():
    excluded = {
        "xano/addon/user.xs",
        "xano/ai/agent/xano_example_agent.xs",
        "xano/ai/tool/search_xano_docs.xs",
        "xano/function/quick_start/enforce_role.xs",
        "xano/workspace/gabriels_workspace.xs",
    }
    for path in (ROOT / "xano").rglob("*.xs"):
        relative = path.relative_to(ROOT).as_posix()
        if relative in excluded:
            continue
        source = path.read_text(encoding="utf-8")
        assert not re.search(r"\bdb\.(?:get|add|edit|query)\s+\"\"", source), relative
        assert not re.search(r"\btable\s*=\s*\"\"", source), relative
        assert not re.search(r"\bauth\s*=\s*\"\"", source), relative


def test_signup_role_matches_user_schema_enum_and_stats_require_scope():
    signup = (
        ROOT / "xano" / "api" / "authentication" / "auth" / "signup_POST.xs"
    ).read_text(encoding="utf-8")
    users_table = (ROOT / "xano" / "table" / "usuarios.xs").read_text(
        encoding="utf-8"
    )
    stats = (
        ROOT / "xano" / "api" / "queue_management" / "stats_GET.xs"
    ).read_text(encoding="utf-8")

    assert 'role      : "usuario"' in signup
    assert 'values = ["admin", "atendente", "usuario", "totem"]' in users_table
    assert 'auth = "usuarios"' in stats
    assert '$auth.role == "admin"' in stats
    assert '$auth.role == "atendente"' in stats
    assert "$atendente.estabelecimento_id == $servico.estabelecimento_id" in stats


def test_seed_endpoint_fails_closed_before_writing_and_returns_only_one_time_secrets():
    endpoint = (
        ROOT / "xano" / "api" / "queue_management" / "setup" / "seed_POST.xs"
    ).read_text(encoding="utf-8")
    response = endpoint.split("response =", 1)[1]
    first_write = endpoint.index("db.add estabelecimentos")

    for required_guard in (
        '$env.$xano_environment == "test"',
        '$env.$seed_enabled == "true"',
        "$input.bootstrap_secret == $env.$seed_secret",
    ):
        assert endpoint.index(required_guard) < first_write
    assert '"admin@filasmart.com"' in endpoint
    assert '"atendente1@filasmart.com"' in endpoint
    assert '"atendente2@filasmart.com"' in endpoint
    assert '"totem@filasmart.com"' in endpoint
    assert '"Atendimento Geral"' in endpoint
    assert '"Preferencial"' in endpoint
    assert "$tv_credential|sha256" in endpoint
    assert "password: $input.admin_password" in endpoint
    assert "password: $atendente1_password" in endpoint
    assert "password: $atendente2_password" in endpoint
    assert "password: $totem_password" in endpoint
    assert "bootstrap_secret" not in response
    assert "admin_password" not in response
    assert "credential_hash" not in response
    assert "credenciais_unica_vez" in response


def test_seed_endpoint_reuses_fixture_records_instead_of_creating_duplicates():
    endpoint = (
        ROOT / "xano" / "api" / "queue_management" / "setup" / "seed_POST.xs"
    ).read_text(encoding="utf-8")
    entities = (
        ("estabelecimentos", '"Matriz"'),
        ("usuarios", '"admin@filasmart.com"'),
        ("usuarios", '"atendente1@filasmart.com"'),
        ("usuarios", '"atendente2@filasmart.com"'),
        ("atendentes", "$atendente1.id"),
        ("atendentes", "$atendente2.id"),
        ("servicos", '"Atendimento Geral"'),
        ("filas", '"Atendimento Geral"'),
        ("servicos", '"Preferencial"'),
        ("filas", '"Preferencial"'),
        ("usuarios", '"totem@filasmart.com"'),
        ("tv_displays", "$estabelecimento.id"),
    )

    for table, stable_key in entities:
        query = re.search(
            rf"db\.query {table} \{{\s*where = [^\n]*{re.escape(stable_key)}",
            endpoint,
        )
        assert query is not None, (table, stable_key)
        query_position = query.start()
        add_position = endpoint.find(f"db.add {table}", query_position)
        assert query_position < add_position, (table, stable_key)
    assert endpoint.count("if ($admin_existente == null)") == 1
    assert endpoint.count("if ($atendente1_existente == null)") == 1
    assert endpoint.count("if ($atendente2_existente == null)") == 1
    assert endpoint.count("if ($totem_existente == null)") == 1
    assert endpoint.count("if ($display_existente == null)") == 1
    display_query = endpoint.index("db.query tv_displays")
    display_write = endpoint.index("db.add tv_displays")
    assert display_query < display_write
    assert "$db.tv_displays.estabelecimento_id == $estabelecimento.id" in endpoint
    assert "$db.tv_displays.ativo == true" in endpoint
    assert "$tv_credential|sha256" in endpoint


def test_password_reset_exports_store_only_token_hash_and_authenticate_users():
    generate = (
        ROOT / "xano" / "function" / "quick_start" / "generate_magic_link.xs"
    ).read_text(encoding="utf-8")
    exchange = (
        ROOT
        / "xano"
        / "api"
        / "authentication"
        / "reset"
        / "magic_link_login_POST.xs"
    ).read_text(encoding="utf-8")
    user_schema = (ROOT / "xano" / "table" / "usuarios.xs").read_text(
        encoding="utf-8"
    )

    assert "json password_reset?" in user_schema
    assert "value = $token|sha256" in generate
    assert '|set:"token":$token_hash' in generate
    assert "value = $input.magic_token|sha256" in exchange
    assert "$magic_token_hash == $user.password_reset.token" in exchange
    assert 'table = "usuarios"' in exchange


def test_streamlit_secret_template_uses_placeholders_and_local_file_is_ignored():
    example = (ROOT / ".streamlit" / "secrets.toml.example").read_text(
        encoding="utf-8"
    )
    gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")

    assert "[xano]" in example
    assert "[tv_display]" in example
    assert "[analytics]" in example
    assert "[xano_seed]" in example
    assert 'bootstrap_secret = "<configure-out-of-band>"' in example
    assert 'admin_password = "<local-test-only-password>"' in example
    assert 'credential = "<configure-local-display-credential>"' in example
    assert "<workspace>" in example
    assert ".streamlit/secrets.toml" in gitignore


def test_main_only_prints_server_generated_one_time_credentials(tmp_path, capsys):
    config = tmp_path / "secrets.toml"
    config.write_text(
        '\n'.join(
            [
                "[xano_seed]",
                'endpoint_url = "https://test-workspace.xano.io/api:queue/setup/seed"',
                'environment = "test"',
                f'bootstrap_secret = "{TEST_SECRET}"',
                'admin_password = "local-test-password"',
            ]
        ),
        encoding="utf-8",
    )
    response = valid_response(totem_password="one-time-password")

    with patch.object(
        sys,
        "argv",
        ["seed_xano.py", "--config", str(config), "--confirm-test-target"],
    ), patch.object(
        seed_xano, "urlopen", return_value=FakeResponse(response)
    ) as mocked_urlopen:
        exit_code = seed_xano.main()

    output = capsys.readouterr().out
    mocked_urlopen.assert_called_once()
    assert mocked_urlopen.call_args.kwargs == {"timeout": 10.0}
    assert exit_code == 0
    assert "one-time-password" in output
    assert TEST_SECRET not in output
    assert "local-test-password" not in output
