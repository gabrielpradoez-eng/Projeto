## Why

Duas emissões reais disparadas em paralelo na fila 4 reproduziram uma corrida: uma criou a senha número 4 e a outra falhou por índice único. A seleção da próxima senha também ocorre fora da transação e pode reutilizar a mesma senha entre requisições concorrentes.

## What Changes

Serializar alocação, chamada e conclusão pelo registro da fila dentro da transação; reler estado após adquirir o bloqueio. Serializar cadastro de atendente pela conta candidata. Preservar guardas de perfil/estabelecimento e contratos externos.

## Capabilities

### Modified Capabilities
- `core-queue-ops`: mutações concorrentes respeitam exclusão por recurso e estado canônico.

## Impact

Exports Xano e validação de runtime. Sem novas contas, credenciais ou exclusões. Testes limitados à fila de informações da demonstração, previamente sem espera e sem atendimento ativo.

## Non-goals

Não prometer resistência a carga ilimitada; não alterar o plano Xano nem tocar na senha anterior aguardando na fila 1.
