## ADDED Requirements
### Requirement: Orçamento compartilhado de chamadas remotas
O aplicativo MUST espaçar chamadas ao mesmo host Xano entre clientes do mesmo processo e pausar novas chamadas após HTTP 429, sem repetir mutações automaticamente.
#### Scenario: Clientes simultâneos
- **WHEN** portal e acompanhamento consultam o mesmo host
- **THEN** os inícios das chamadas respeitam intervalo mínimo de 2,5 segundos
#### Scenario: Limite remoto atingido
- **WHEN** o Xano retorna HTTP 429
- **THEN** o processo pausa chamadas seguintes por pelo menos 30 segundos e não reenvia a operação
