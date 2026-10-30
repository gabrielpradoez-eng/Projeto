import pytest

from views.presentation import format_timestamp, ticket_receipt


@pytest.mark.parametrize("value", ["2026-10-28T18:35:28.244000Z", 1793212528244])
def test_timestamp_uses_sao_paulo_instead_of_utc(value):
    assert format_timestamp(value) == "28/10/2026 às 15:35:28"


@pytest.mark.parametrize("value", [None, "", "invalid", 0, -1, True, float("inf")])
def test_invalid_timestamp_has_readable_fallback(value):
    assert format_timestamp(value) == "Horário indisponível"


def test_receipt_includes_customer_reference_and_instructions_without_public_url():
    receipt = ticket_receipt(22, "customer-reference", "Retirada", "Fila 1")
    assert "Senha: 22" in receipt
    assert "Serviço: Retirada" in receipt
    assert "Fila: Fila 1" in receipt
    assert "Referência de acompanhamento: customer-reference" in receipt
    assert "Acompanhar senha" in receipt
    assert "http" not in receipt
