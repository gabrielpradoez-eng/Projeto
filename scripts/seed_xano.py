from __future__ import annotations

import argparse
import json
import sys
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen


class SeedConfigurationError(Exception):
    pass


class SeedRequestError(Exception):
    pass


@dataclass(frozen=True)
class SeedSettings:
    endpoint_url: str
    environment: str
    bootstrap_secret: str
    admin_password: str

    @classmethod
    def from_secrets(cls, secrets: dict[str, Any]) -> "SeedSettings":
        try:
            values = secrets["xano_seed"]
            settings = cls(
                endpoint_url=values["endpoint_url"],
                environment=values["environment"],
                bootstrap_secret=values["bootstrap_secret"],
                admin_password=values["admin_password"],
            )
        except (KeyError, TypeError):
            raise SeedConfigurationError(
                "A seção [xano_seed] está ausente ou incompleta."
            ) from None

        if any(
            not isinstance(value, str)
            for value in (
                settings.endpoint_url,
                settings.environment,
                settings.bootstrap_secret,
                settings.admin_password,
            )
        ):
            raise SeedConfigurationError(
                "Os valores de [xano_seed] devem ser textos."
            )

        try:
            parsed_url = urlparse(settings.endpoint_url)
            hostname = parsed_url.hostname
        except ValueError:
            raise SeedConfigurationError(
                "A URL do endpoint de seed é inválida."
            ) from None
        if (
            settings.environment != "test"
            or parsed_url.scheme != "https"
            or hostname is None
            or not hostname.endswith(".xano.io")
            or parsed_url.username is not None
            or parsed_url.password is not None
            or parsed_url.query
            or parsed_url.fragment
            or not parsed_url.path.endswith("/setup/seed")
            or "<" in settings.endpoint_url
            or ">" in settings.endpoint_url
        ):
            raise SeedConfigurationError(
                "O destino deve ser um endpoint HTTPS de seed em workspace Xano de teste."
            )
        if len(settings.bootstrap_secret) < 32 or "<" in settings.bootstrap_secret:
            raise SeedConfigurationError(
                "Configure um segredo de bootstrap aleatório com pelo menos 32 caracteres."
            )
        if len(settings.admin_password) < 8 or "<" in settings.admin_password:
            raise SeedConfigurationError(
                "Configure uma senha local de teste com pelo menos 8 caracteres."
            )
        return settings


def load_settings(path: Path) -> SeedSettings:
    try:
        with path.open("rb") as secrets_file:
            secrets = tomllib.load(secrets_file)
    except OSError:
        raise SeedConfigurationError(
            "Não foi possível ler o arquivo local de secrets."
        ) from None
    except tomllib.TOMLDecodeError:
        raise SeedConfigurationError(
            "O arquivo local de secrets possui TOML inválido."
        ) from None
    return SeedSettings.from_secrets(secrets)


def seed(
    settings: SeedSettings,
    *,
    confirmed_test_target: bool,
    opener: Callable[..., Any] | None = None,
) -> dict[str, Any]:
    settings = SeedSettings.from_secrets(
        {
            "xano_seed": {
                "endpoint_url": settings.endpoint_url,
                "environment": settings.environment,
                "bootstrap_secret": settings.bootstrap_secret,
                "admin_password": settings.admin_password,
            }
        }
    )
    if not confirmed_test_target:
        raise SeedConfigurationError(
            "Confirme o destino descartável com --confirm-test-target."
        )
    if settings.environment != "test":
        raise SeedConfigurationError("Seed permitido somente em ambiente test.")

    request = Request(
        settings.endpoint_url,
        data=json.dumps(
            {
                "bootstrap_secret": settings.bootstrap_secret,
                "admin_password": settings.admin_password,
            }
        ).encode("utf-8"),
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        if opener:
            with opener(request, timeout=10.0) as response:
                response_body = response.read()
        else:
            with urlopen(request, timeout=10.0) as response:
                response_body = response.read()
    except HTTPError:
        raise SeedRequestError(
            "O Xano recusou o provisionamento. Verifique o ambiente e a autorização."
        ) from None
    except (URLError, TimeoutError, OSError):
        raise SeedRequestError(
            "Não foi possível conectar ao endpoint de provisionamento Xano."
        ) from None

    try:
        result = json.loads(response_body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        raise SeedRequestError(
            "O endpoint de provisionamento retornou JSON inválido."
        ) from None

    credentials = result.get("credenciais_unica_vez") if isinstance(result, dict) else None

    if (
        not isinstance(result, dict)
        or result.get("estabelecimento") != "Matriz"
        or not isinstance(credentials, dict)
        or any(value is not None and not isinstance(value, str) for value in credentials.values())
    ):
        raise SeedRequestError(
            "O endpoint Xano retornou uma resposta de provisionamento inválida."
        )
    return result


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Provisiona fixtures FilaSmart apenas em um workspace Xano de teste."
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=Path(".streamlit/secrets.toml"),
        help="Arquivo local de configuração (padrão: .streamlit/secrets.toml).",
    )
    parser.add_argument(
        "--confirm-test-target",
        action="store_true",
        help="Confirma que o workspace Xano configurado é descartável e não produtivo.",
    )
    args = parser.parse_args()

    try:
        settings = load_settings(args.config)
        result = seed(settings, confirmed_test_target=args.confirm_test_target)
    except (SeedConfigurationError, SeedRequestError) as exc:
        print(str(exc), file=sys.stderr)
        return 1

    print("Fixture Matriz provisionado ou já existente.")
    print("Contas: admin@filasmart.com, atendente1@filasmart.com,")
    print("        atendente2@filasmart.com, totem@filasmart.com")
    print("Filas: Atendimento Geral, Preferencial")
    credentials = result["credenciais_unica_vez"]
    for name, value in credentials.items():
        if value is not None:
            print(f"Credencial de uso único ({name}): {value}")
    print("Salve as credenciais exibidas em armazenamento local seguro.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())