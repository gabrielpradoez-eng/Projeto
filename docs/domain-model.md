# Modelo de Domínio — FilaSmart

## Visão Geral das Entidades

```text
Estabelecimento
   │
   ├── Usuário (Cliente / Atendente / Administrador)
   │
   ├── Serviço (Geral, Preferencial, Financeiro, etc.)
   │      │
   │      └── Fila
   │            │
   │            └── Senha ─── Notificação
   │                  │
   └── Atendimento ───┘ (vincula Atendente + Senha + Guichê)