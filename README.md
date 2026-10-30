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
│   │   ├── analytics-and-reports/spec.md
│   │   ├── core-queue-ops/spec.md
│   │   ├── project-review/spec.md
│   │   ├── service-experience/spec.md
│   │   ├── totem-customer-tracking/spec.md
│   │   ├── tv-display-panel/spec.md
│   │   └── unified-streamlit-experience/spec.md
│   └── changes/
│       ├── account-registration/    # Exemplo de mudança em acompanhamento
│       │   ├── .openspec.yaml
│       │   ├── proposal.md
│       │   ├── design.md
│       │   ├── tasks.md
│       │   └── specs/account-registration/spec.md
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

A reorganização foi verificada com **190 testes aprovados**, **20 itens OpenSpec válidos em modo estrito** e links locais conferidos. Os testes não substituem a validação dos exports no runtime do Xano nem testes de carga.

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

**Situação do cadastro:** código e endpoints publicados; a última verificação do site ainda registrava a versão 2026.10.29.5. A confirmação da versão 2026.10.29.6 e do cadastro positivo permanece registrada em [tasks.md](openspec/changes/account-registration/tasks.md). A reorganização de pastas não conclui essas verificações operacionais.
