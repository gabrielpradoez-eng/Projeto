# Project Overview — FilaSmart (Sistema de Gestão de Filas e Atendimentos)

## 1. Visão Geral
O **FilaSmart** é uma plataforma completa para gestão, controle e acompanhamento de filas e atendimentos presenciais em tempo real. O sistema integra a emissão de senhas (via totem/presencial ou mobile), chamadas em painéis públicos, gestão de atendimento por atendentes/guichês e acompanhamento do status da senha pelo próprio usuário via dispositivo móvel.

## 2. Problema
Filas presenciais desorganizadas geram insatisfação dos clientes, falta de previsibilidade de tempo de espera, dificuldades na gestão de atendimento por parte dos atendentes e ausência de métricas para a gestão dos estabelecimentos.

## 3. Objetivos
- Organizar a entrada e o fluxo de passageiros/clientes por tipo de serviço (Geral, Preferencial, Financeiro, Suporte, Retirada).
- Oferecer transparência ao usuário, permitindo o acompanhamento do status e posição na fila via app/mobile.
- Agilizar o trabalho dos atendentes e otimizar a chamada de senhas por guichês.
- Coletar métricas operacionais (tempo médio de espera, total de atendimentos e nível de satisfação).

## 4. Público-alvo e Usuários
- **Usuários / Clientes:** Pessoas que retiram senhas e aguardam o atendimento (presencialmente ou acompanhando via celular).
- **Atendentes / Funcionários:** Responsáveis por chamar as senhas, realizar o atendimento e finalizar/encaminhar os casos.
- **Administradores / Gestores:** Responsáveis por monitorar dashboards, configurar serviços, gerenciar filas, usuários e visualizar relatórios.

## 5. Escopo Inicial
- **Totem de Autoatendimento:** Interface para seleção de serviços e emissão/retirada de senhas.
- **Painel de Chamadas:** Tela pública exibindo a chamada atual (senha + guichê) e a lista de próximas chamadas.
- **Painel de Atendimento (Gestão do Atendente):** Interface para o funcionário chamar a próxima senha, iniciar e finalizar atendimentos.
- **Acompanhamento Mobile ("Minha Senha"):** Exibição da senha ativa, posição na fila, tempo estimado e linha do tempo do status.
- **Dashboard Administrativo:** Visão consolidada de filas ativas, atendimentos realizados, tempo médio e satisfação.

## 6. Principais Funcionalidades
- Emissão de senhas categorizadas (Geral, Preferencial, Financeiro, Suporte Técnico, Retirada/Entrega).
- Fila em tempo real e atualização de posições.
- Notificações de chamada para o usuário.
- Controle de chamadas por guichê.
- Histórico e registro do tempo de duração de cada atendimento.
- Avaliação de satisfação ao término do atendimento.

## 7. Arquitetura e Princípios de Desenvolvimento
- **Comunicação em Tempo Real:** Atualizações instantâneas no Painel de Chamadas e no App Mobile (via WebSockets/Server-Sent Events/Push).
- **Separação de Camadas:** Regras de transição de status da senha e controle de filas centralizados no Backend.
- **Idioma:** Documentação e artefatos em português brasileiro (pt-BR).