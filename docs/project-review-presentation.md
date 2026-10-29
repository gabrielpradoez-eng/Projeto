# Revisão e dados de apresentação — 29/10/2026

## Correções aplicadas

- O acompanhamento e o comprovante do cliente não dependem mais de nova consulta ao catálogo de filas.
- Filas removidas da resposta autorizada deixam de causar seleção obsoleta no painel do atendente.
- Confirmações de emissão, opções de fila e respostas de acompanhamento passam por validações de estrutura, tipos e valores antes de renderizar.
- O painel rejeita IDs e contagens inválidas. A TV ordena chamadas pelo horário, com ID como desempate, e identifica o serviço para distinguir números repetidos entre filas.
- Erros de clientes têm mensagens de ação; payloads e códigos técnicos ficam recolhidos para administradores.

## Dados no Xano

O estabelecimento foi identificado como **Central de Atendimento — Demonstração**. O catálogo contém Atendimento geral, Suporte técnico, Retirada de documentos e Informações e cadastro, cada um com fila aberta e estimativa própria.

A rotina interna `prepare_presentation` foi salva e executada manualmente no console, sem endpoint público. A simulação inicial encontrou cinco senhas e quatro atendimentos. A carga criou 12 senhas concluídas e seus atendimentos, distribuídos por serviço e data. Os quatro fixtures antigos de atendimento foram normalizados e tiveram os rótulos de teste substituídos. O registro anterior à carga fora desses fixtures foi preservado.

Resultado confirmado: quatro serviços, quatro filas, 17 senhas e 16 atendimentos. Uma segunda execução manteve as contagens e retornou lista de criação vazia. Não foram criadas contas, credenciais, referências ativas de rastreamento ou notificações externas. Não houve exclusão de registros.

O feed TV foi atualizado e publicado no Xano. Dados sintéticos destinam-se à apresentação, não a indicadores de uma operação real.

## Escopo da verificação

Foram revisados os fluxos implementados de login/perfis, emissão, acompanhamento, atendimento, TV, relatórios e seus contratos. A suíte automatizada cobre regressões e validações. A revisão não substitui auditoria formal de segurança nem teste de carga. Login positivo no portal com credenciais reais e concorrência de emissão continuam dependendo de validação operacional específica.
