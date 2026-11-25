## Context
A instância gratuita limita chamadas. A verificação de identidade permanece obrigatória.
## Decisions
Compartilhar gate por host entre threads do mesmo processo; espaçar inícios de chamadas em 2,5 segundos. HTTP 429 impõe pausa mínima de 30 segundos, respeitando Retry-After numérico. Não repetir requisições automaticamente, em especial emissão, envio e finalização.
## Risks
Outros processos e chamadas externas continuam consumindo o limite remoto. O gate não aumenta a capacidade do plano. Sob concorrência, ações podem aguardar e a interface pode ficar mais lenta. Verificação com múltiplos usuários no deploy permanece pendente.
