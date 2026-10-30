## Context

Formalização documental da entrega descrita em [proposal.md](proposal.md). O histórico e as pendências permanecem em [tasks.md](tasks.md).

## Decisions

- Componentes envolvidos: `portal_session.py`, `views/registration_view.py`, `backend_queue.py` e endpoints `auth/signup` e `admin/attendants`.
- O Xano mantém regras de autorização, persistência e estado; a interface valida respostas e apresenta o resultado canônico.
- Credenciais permanecem fora de arquivos versionados e da documentação pública.
- A normalização OpenSpec não altera endpoints, dados ou comportamento da aplicação.

## Verification

Os cenários de `specs/` documentam aceitação; `tasks.md` registra evidências e limitações da entrega. Este documento foi completado retrospectivamente em 29/10/2026 e não constitui nova validação operacional.
