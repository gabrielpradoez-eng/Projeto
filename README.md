# FilaSmart

Sistema de gestão de filas e atendimentos com **Streamlit** na interface e **Xano** nas regras de negócio e persistência. O desenvolvimento é organizado pelo [OpenSpec](https://openspec.dev/).

[Aplicação publicada](https://filasmarttech.streamlit.app/) · [Visão do projeto](docs/project-overview.md) · [Modelo de domínio](docs/domain-model.md) · [Fluxo OpenSpec](docs/openspec-workflow.md)

## Organização do projeto

```text
Projeto/
├── README.md                        # Apresentação e execução
├── AGENTS.md                        # Regras para agentes de desenvolvimento
├── app.py                           # Entrada do deploy Streamlit
├── analytics_app.py                 # Entrada independente de relatórios
├── kiosk_app.py                     # Entrada independente do totem
├── tv_display_app.py                # Entrada independente da TV
├── backend_queue.py                 # Adaptador das operações Xano
├── portal_session.py                # Identidade e sessão do portal
├── *_client.py                      # Clientes HTTP por integração
├── streamlit_xano.py                # Configuração das integrações
├── views/                           # Interfaces e componentes
├── app_pages/                       # Entradas auxiliares
├── assets/                          # Estilos e recursos visuais
├── xano/                            # Exports de tabelas, APIs e funções
├── tests/                           # Testes Python e contratos
├── scripts/                         # Utilitários de operação
├── docs/                            # Guias de arquitetura, deploy e operação
├── openspec/
│   ├── config.yaml                  # Contexto, schema e regras do projeto
│   ├── specs/                       # Contratos vigentes por capacidade
│   │   ├── account-registration/spec.md
│   │   ├── analytics-and-reports/spec.md
│   │   ├── core-queue-ops/spec.md
│   │   ├── project-review/spec.md
│   │   ├── service-experience/spec.md
│   │   ├── totem-customer-tracking/spec.md
│   │   ├── tv-display-panel/spec.md
│   │   ├── unified-streamlit-experience/spec.md
│   │   └── verified-role-navigation/spec.md
│   └── changes/
│       ├── atendimento-chat/        # Mudança em acompanhamento
│       │   ├── .openspec.yaml
│       │   ├── proposal.md
│       │   ├── design.md
│       │   ├── tasks.md
│       │   └── specs/atendimento-chat/spec.md
│       ├── ...                      # Demais mudanças no índice do guia
│       └── archive/                 # Histórico preservado por data e nome
│           ├── ...
│           ├── 2026-10-30-project-review-presentation/
│           └── 2026-10-30-service-experience-refresh/
├── .streamlit/                      # Configuração e modelo de Secrets
├── .github/workflows/               # Validação e preparação do Copilot
├── requirements.txt                 # Dependências Python de produção
├── package.json                     # CLI OpenSpec de desenvolvimento
└── package-lock.json                # Versões reproduzíveis da ferramenta
```

O OpenSpec organiza especificações e mudanças; não determina a arquitetura dos módulos da aplicação. Os pontos de entrada Python conservam os caminhos utilizados no deploy. O guia contém o [índice completo das mudanças](docs/openspec-workflow.md#situação-das-mudanças).

## Executar localmente

Pré-requisitos: Python 3.11 ou superior. Node.js é necessário somente para trabalhar com OpenSpec.

```bash
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Copie `.streamlit/secrets.toml.example` para `.streamlit/secrets.toml` e configure seu Xano conforme o [guia de deploy](docs/streamlit-deploy.md). O arquivo real de Secrets não deve ser versionado.

```bash
streamlit run app.py
```

## Testar

```bash
python -m pip install pytest
python -m pytest -q
```

A revisão de **23/11/2026** aprovou **238 testes Python** e **24 itens OpenSpec em modo estrito**. Consulte a [revisão atual](docs/review-2026-11-23.md) e a [auditoria histórica](docs/project-audit.md). Testes locais não substituem execução dos exports no Xano, testes de carga ou validação em produção. A emissão, chamada e conclusão simultâneas têm [registro de validação no Xano](docs/queue-concurrency-validation.md).

## Trabalhar com OpenSpec

Pré-requisito: Node.js **20.19+**; o CI utiliza Node 24. A versão **1.15.0** da CLI está fixada no lockfile e é exclusiva do ambiente de desenvolvimento.

```bash
npm ci --ignore-scripts
npm run spec:list
npm run spec:validate
npx --no-install openspec new change nome-da-mudanca
npx --no-install openspec status --change nome-da-mudanca
npx --no-install openspec instructions proposal --change nome-da-mudanca
```

Cada mudança funcional contém proposta, desenho técnico, tarefas e deltas com requisitos e cenários. Mudanças exclusivamente documentais ou de ferramentas podem declarar `skip_specs: true`, como permite o OpenSpec. Ao concluir a implementação e as verificações, o arquivamento sincroniza os deltas com as especificações vigentes:

```bash
npx --no-install openspec validate nome-da-mudanca --strict
npx --no-install openspec archive nome-da-mudanca
```

O workflow [OpenSpec validation](.github/workflows/openspec-validation.yml) executa validação estrita em pushes e pull requests que alterem as especificações ou a configuração da ferramenta. Consulte o [guia completo](docs/openspec-workflow.md) antes de arquivar uma entrega.

## Funcionalidades e documentação

- [Acesso e perfis](docs/access-control.md): cliente, atendente e administrador com identidade verificada no Xano.
- [Cadastro de clientes e atendentes](docs/account-registration.md): cliente cria sua conta; administrador libera o vínculo de atendimento por estabelecimento e guichê.
- Totem, comprovante e acompanhamento de senha; painel operacional; chamadas na TV e relatórios.
- [Importação dos exports Xano](docs/xano-import-order.md) e [deploy no Streamlit](docs/streamlit-deploy.md).
- [Revisão e dados de apresentação](docs/project-review-presentation.md).

## Situação atual e operação

- **Cliente:** o titular criou uma conta e o login com perfil Cliente foi confirmado no portal em 23/11/2026.
- **Atendente:** login e operação de chamada confirmados. A liberação de nova conta e o novo login como Atendente foram confirmados em 23/11/2026; veja o [checklist de cadastro](openspec/changes/archive/2026-11-23-account-registration/tasks.md).
- **Chat:** troca de mensagens confirmada entre cliente e atendente no site, na senha 8 / Guichê 1. As duas mensagens foram vistas nas duas sessões. Essa evidência não equivale a teste de carga.
- **GitHub e deploy:** `main` contém a documentação principal; a implantação `filasmarttech` usa `codex/streamlit-deployment-preparation` e `app.py`. Um push Python não publica exports no Xano. As duas branches podem ter históricos diferentes; compare o conteúdo antes de integrar.
- **Limites conhecidos:** houve respostas HTTP 429 do Xano durante o teste. O chat passou a consultar a cada 30 segundos para reduzir requisições; múltiplas telas e usuários ainda podem exceder a capacidade do serviço. Em recusa ou timeout, confira o estado antes de repetir emissão, chamada ou envio.
- **Hospedagem:** o Streamlit Community Cloud pode suspender o aplicativo por inatividade; a tela de suspensão permite reativá-lo. Disponibilidade contínua e capacidade para vários usuários precisam de validação própria.

O CI inclui [testes Python](.github/workflows/python-tests.yml) e [validação OpenSpec](.github/workflows/openspec-validation.yml). Resultados locais e evidências de runtime estão separados no [relatório atual](docs/review-2026-11-23.md).

## Configuração e deploy

O modelo [.streamlit/secrets.toml.example](.streamlit/secrets.toml.example) lista os campos necessários. Configure valores reais somente no arquivo local ignorado pelo Git ou nos Secrets do Streamlit:

| Seção | Finalidade |
| --- | --- |
| `[xano]` | URLs de autenticação, API de filas, acompanhamento e conta técnica do totem |
| `[tv_display]` | Feed de chamadas e credencial restrita do display |
| `[analytics]` | URLs de autenticação, opções e relatório administrativo |
| `[xano_seed]` | Provisionamento exclusivo de teste; não habilitar seed em produção |

O modelo deixa `service_chat_enabled = false`. Após publicar e validar os três exports do chat, configure `true` em `[xano]`; `false` sempre desativa a interface. Quando a chave não existe, o código ativa automaticamente apenas para a API de filas validada do FilaSmart. Consulte [chat](docs/service-chat.md), [ordem de importação](docs/xano-import-order.md) e [deploy](docs/streamlit-deploy.md).

Contas Xano/Streamlit não são contas do portal. O cadastro público cria somente clientes; o administrador habilita atendentes. Não publique senhas, tokens ou o arquivo real de Secrets. Recuperação de acesso depende do responsável pelo sistema, conforme [controle de acesso](docs/access-control.md).

## Interface empresarial e acesso pelo celular

A versão 2026.10.30.2 traz tema empresarial, cabeçalhos compactos e formulários consistentes. Até 900px, o seletor Navegar para e a saída ficam no conteúdo. Até 640px, colunas e métricas empilham e botões usam a largura disponível. Filtros de relatórios ficam no conteúdo do portal. A navegação permanece restrita ao perfil verificado. A interface foi confirmada no Streamlit. A revisão de novembro ajusta o espaço abaixo da barra fixa em telas estreitas. Veja as [evidências e limites](docs/corporate-responsive-interface.md) e a [mudança OpenSpec](openspec/changes/archive/2026-11-11-corporate-responsive-interface/tasks.md).

## Chat de atendimento

O chat privado abre após a chamada para o cliente e o atendente responsável, mostra até 50 mensagens de até 500 caracteres e deixa de permitir acesso ao finalizar o atendimento. Não há anexos, WhatsApp, SMS ou notificações push. Consulte a [ativação e os testes de implantação](docs/service-chat.md).
