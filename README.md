# FilaSmart — Manual de uso

## 1. Apresentação

O **FilaSmart** é um aplicativo web para organizar filas e atendimentos presenciais. Ele permite escolher um serviço, emitir uma senha, acompanhar a chamada e conversar com o atendente durante o atendimento.

A solução busca reduzir a desorganização na recepção, a falta de informação sobre a espera e a dificuldade de coordenar chamadas. Destina-se a estabelecimentos com atendimento por ordem de chegada, como assistências técnicas e centrais de atendimento. O cenário desta apresentação é uma assistência técnica.

## 2. Acesso ao aplicativo

**Acesse: [FilaSmart publicado](https://filasmarttech.streamlit.app/).**

1. Abra o link no computador ou celular.
2. Na aba **Entrar**, informe o e-mail e a senha da sua conta.
3. Clique em **Entrar**. O menu será apresentado conforme seu perfil.
4. Se ainda não tem conta, use **Criar conta**. Toda conta pública começa como cliente.
5. Para trabalhar como atendente, solicite a liberação ao administrador. Não é necessário criar outra senha.
6. Ao terminar, use **Sair**, especialmente em computadores compartilhados.

Contas do Xano e do Streamlit não são contas do aplicativo. Não existem credenciais públicas de demonstração neste documento. Se o aplicativo estiver suspenso por inatividade, use a opção de reativação apresentada pelo Streamlit e aguarde.

## 3. Perfis de usuários

| Perfil | Responsabilidade e permissões |
| --- | --- |
| Cliente | Criar sua conta, emitir e acompanhar sua senha, conversar com o atendente responsável quando for chamado e visualizar o painel TV disponível no portal. Não administra serviços ou equipe. |
| Atendente | Consultar as filas autorizadas do estabelecimento, chamar a próxima senha, conversar com o cliente chamado e finalizar o atendimento. Não recebe o catálogo administrativo nem os relatórios do administrador. |
| Administrador | Liberar atendentes por estabelecimento e guichê; manter serviços e filas quando o catálogo estiver habilitado; consultar relatórios. Possui também acesso às áreas de cliente, acompanhamento, totem e TV. |
| Totem e display | Integrações técnicas configuradas pelo responsável pela instalação; não são perfis liberados pelo cadastro público. |

A autorização das operações é verificada no Xano. Um endereço de acompanhamento não concede acesso ao chat privado.

## 4. Funcionalidades

- Cadastro de clientes e entrada com verificação de perfil.
- Catálogo de serviços com filas disponíveis para emissão.
- Emissão de senha, comprovante para download e acompanhamento de status e posição.
- Operação do atendente: consulta de filas, chamada e finalização.
- Chat privado durante o atendimento chamado.
- Painel TV para chamadas, conforme configuração da instalação.
- Administração de serviços, duração estimada e abertura/fechamento de filas.
- Liberação de atendentes por estabelecimento e guichê.
- Relatórios administrativos com filtros de período, estabelecimento, serviço e fila.
- Interface adaptada a telas menores e controle compartilhado das chamadas ao Xano.

## 5. Manual de utilização

### 5.1 Criar uma conta

1. Na tela inicial, abra **Criar conta**.
2. Preencha nome completo, e-mail, senha e confirmação.
3. Use uma senha de 10 a 128 caracteres e confirme o cadastro em **Criar conta**.
4. Após a confirmação, abra **Entrar** e use os dados cadastrados.

**Resultado esperado:** acesso inicial com perfil Cliente. O cadastro não concede privilégios administrativos ou de atendente. Se o e-mail já estiver cadastrado, tente entrar; em caso de dificuldade, procure o responsável pelo sistema.

### 5.2 Cliente: escolher serviço e emitir senha

1. Entre como cliente e abra **Cliente**.
2. No campo **Serviço**, escolha, por exemplo, **Entrega de aparelho · Entrega de aparelho**.
3. Clique uma vez em **Emitir senha** e aguarde a confirmação.
4. Confira o número e a posição exibidos. Use **Baixar comprovante** para guardar a referência de acompanhamento.
5. Acompanhe a atualização automática. Quando o status mudar para **chamado**, confira o guichê indicado e dirija-se ao atendimento.

**Resultado esperado:** senha registrada na fila escolhida e acompanhamento individual disponível. O número é gerado pelo sistema; não deve ser presumido antes da emissão.

**Caminho alternativo:** a área **Acompanhar senha** permite consultar uma referência válida já emitida, conforme os campos apresentados. Guarde a referência como informação privada.

### 5.3 Atendente: chamar e finalizar

1. Entre com uma conta previamente liberada pelo administrador.
2. Na área **Administração**, encontre o **Painel do atendente**.
3. Selecione **Fila sob sua responsabilidade**.
4. Clique em **Atualizar filas** para consultar o estado confirmado.
5. Havendo senhas aguardando e nenhum atendimento ativo, clique em **Chamar próxima senha**.
6. Confira o número em atendimento e o guichê.
7. Após concluir o serviço ao cliente, clique em **Finalizar atendimento atual**.
8. Confira que não há mais atendimento ativo nessa fila antes de chamar outra senha.

**Resultado esperado:** a senha passa de aguardando para chamada; após finalizar, deixa de aparecer como atendimento ativo. A fila vazia mantém a chamada desabilitada. A finalização também encerra o acesso ao chat daquele atendimento.

### 5.4 Cliente e atendente: conversar durante o atendimento

1. O atendente deve chamar a senha antes de iniciar a conversa.
2. Ambos localizam **Chat do atendimento** nas respectivas áreas.
3. Digite em **Escreva uma mensagem** e use o botão de envio.
4. Aguarde a atualização da outra sessão para confirmar a entrega.
5. O destinatário responde pelo mesmo campo.

**Resultado esperado:** mensagens identificadas como **Você**, **Cliente** ou **Atendente**, conforme a sessão. O chat apresenta até 50 mensagens de até 500 caracteres, sem anexos. Antes da chamada não há conversa disponível; após a finalização, o acesso se encerra.

### 5.5 Administrador: liberar um atendente

1. Peça ao profissional que crie sua conta pelo cadastro público.
2. Entre como administrador e abra **Administração → Cadastrar atendente**.
3. Informe **E-mail da conta do atendente**, selecione o estabelecimento e preencha **Guichê de atendimento**.
4. Marque a confirmação de liberação e clique em **Cadastrar atendente**.
5. Oriente o profissional a sair e entrar novamente.

**Resultado esperado:** a conta passa a operar como atendente no vínculo autorizado. Contas com vínculo anterior não são alteradas por esse formulário. O primeiro administrador depende do provisionamento pelo responsável; não pode ser escolhido no cadastro público.

### 5.6 Administrador: manter serviços e filas

1. Em **Administração**, localize **Serviços e filas da empresa**. Essa seção depende da ativação do catálogo na instalação.
2. Em **Serviço e fila**, escolha um registro existente ou **Novo serviço e fila**.
3. Para criar, selecione o estabelecimento, informe nome do serviço, duração estimada em minutos e nome da fila.
4. Defina **Estado da fila** como aberta ou fechada.
5. Clique em **Salvar serviço e fila** e aguarde a confirmação.
6. Para editar, selecione o registro, ajuste os campos permitidos e salve novamente.

**Resultado esperado:** o catálogo atualizado aparece no sistema. Uma fila aberta pode ser oferecida na emissão; uma fechada deixa de ser uma opção disponível ao cliente. Fechar não exclui o histórico. Não há exclusão definitiva de registros pelo catálogo. A duração é a estimativa do atendimento, não o prazo de execução de um reparo.

### 5.7 Administrador: consultar relatórios

1. Abra **Relatórios**.
2. Em **Filtros do relatório**, escolha estabelecimento, serviço e fila, ou mantenha as opções de todos os serviços/filas.
3. Informe **Data inicial (UTC)** e **Data final exclusiva (UTC)**. Para incluir um dia inteiro, use o dia seguinte como data final.
4. Execute a consulta pelo botão do formulário.
5. Confira os indicadores e visualizações para o período escolhido.

**Resultado esperado:** relatório limitado ao escopo e às datas selecionadas. Um período sem atendimentos pode não produzir indicadores preenchidos; isso não significa falha. As datas dos filtros usam UTC, enquanto os horários de acompanhamento são apresentados no horário de São Paulo.

### 5.8 Situações alternativas e uso no celular

- **Fila vazia:** selecione outra fila ou aguarde novos clientes; não é possível chamar uma senha inexistente.
- **Fila fechada:** o administrador deve abrir a fila quando houver condições de atendimento.
- **HTTP 429 ou atualização indisponível:** aguarde a pausa aplicada pelo aplicativo. Evite várias abas atualizando e não clique repetidamente. Confira o estado antes de repetir emissão, chamada, envio ou finalização.
- **Referência encerrada/indisponível:** confira o comprovante. Após a conclusão, o acompanhamento pode informar que foi encerrado.
- **Celular:** utilize o seletor **Navegar para** quando aparecer no lugar do menu lateral. Os recursos continuam limitados ao perfil autenticado.
- **Problema de acesso:** confirme e-mail e perfil com o responsável. A versão entregue não oferece recuperação automática de senha.

## 6. Exemplos de utilização

### Assistência técnica — cenário cadastrado

Estabelecimento: **Central de Atendimento**.

| Serviço | Duração estimada do atendimento | Uso |
| --- | ---: | --- |
| Entrega de aparelho | 10 min | Recepção do aparelho e registro da solicitação. |
| Avaliação técnica e orçamento | 20 min | Conversa inicial para avaliação e orientação de orçamento. |
| Retirada de aparelho reparado | 5 min | Conferência e entrega do aparelho ao cliente. |

Esses nomes representam categorias da fila. A versão atual não possui módulo de ordem de serviço, controle do reparo, estoque ou pagamentos.

**Exemplo completo:** o cliente entra, escolhe Entrega de aparelho e emite a senha. O atendente da mesma fila chama a próxima pessoa no Guichê 1. A chamada aparece ao cliente, os dois trocam mensagens e o atendente finaliza. A fila volta a ficar sem atendimento ativo e o chat é encerrado.

Em **25/11/2026**, esse percurso foi confirmado no aplicativo publicado com duas sessões, incluindo mensagens nos dois sentidos e finalização, sem HTTP 429 visível no teste. Isso não equivale a teste de carga.

**Apresentação acadêmica:** consulte o [roteiro de gravação de 5 minutos](docs/roteiro-video-5-minutos.md). Ele é um guia para gravar o aplicativo real, não um vídeo já produzido.

## 7. Limitações conhecidas

- O plano gratuito Xano tem capacidade limitada; houve HTTP 429 em uso anterior. O espaçamento de chamadas e as pausas reduzem rajadas, mas não garantem ausência de erros com maior demanda.
- Acompanhamento e chat usam consultas periódicas, em geral a cada 30 segundos; não são atualizações instantâneas. Ações podem aguardar o orçamento de chamadas.
- O controle de tráfego é compartilhado dentro do mesmo processo. Outros processos e acessos externos também consomem a capacidade remota.
- O Streamlit Community Cloud pode suspender a aplicação por inatividade. Reinicializações podem encerrar sessões.
- Chat somente durante o atendimento chamado; sem WhatsApp, SMS, push ou anexos.
- Cadastro público cria somente clientes. Administrador e configurações técnicas dependem do responsável pela instalação.
- Catálogo permite criar/editar e abrir/fechar filas; não oferece exclusão definitiva no portal.
- Implantação para outra empresa é independente, com configurações, usuários e workspace próprios. Não há SaaS compartilhado ou cobrança por assinatura.
- Não estão implementados agendamento, triagem de urgência, ordem de serviço, pagamentos, estoque, avaliação completa de satisfação ou recuperação automática de senha.
- Capacidade com muitos usuários, backups/restauração, monitoramento e prontidão comercial ainda precisam de validação específica.

---

## Documentação técnica e manutenção

As instruções abaixo destinam-se a quem instala e mantém o sistema. Para utilizar o site publicado, siga o manual acima.

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

A validação acumulada até **25/11/2026** aprovou **253 testes Python** e **29 itens OpenSpec em modo estrito**. Consulte a [revisão atual](docs/review-2026-11-24.md) e a [auditoria histórica](docs/project-audit.md). Testes locais não substituem execução dos exports no Xano, testes de carga ou validação em produção. A emissão, chamada e conclusão simultâneas têm [registro de validação no Xano](docs/queue-concurrency-validation.md).

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

O CI inclui [testes Python](.github/workflows/python-tests.yml) e [validação OpenSpec](.github/workflows/openspec-validation.yml). Resultados locais e evidências de runtime estão separados no [relatório atual](docs/review-2026-11-24.md).

## Configuração e deploy

O modelo [.streamlit/secrets.toml.example](.streamlit/secrets.toml.example) lista os campos necessários. Configure valores reais somente no arquivo local ignorado pelo Git ou nos Secrets do Streamlit:

| Seção | Finalidade |
| --- | --- |
| `[xano]` | URLs de autenticação, API de filas, acompanhamento e conta técnica do totem |
| `[tv_display]` | Feed de chamadas e credencial restrita do display |
| `[analytics]` | URLs de autenticação, opções e relatório administrativo |
| `[company]` | Nome, cor da marca e ativação explícita do catálogo administrativo |


O modelo deixa `service_chat_enabled = false`. Após publicar e validar os três exports do chat, configure `true` em `[xano]`; `false` sempre desativa a interface. Quando a chave não existe, o código ativa automaticamente apenas para a API de filas validada do FilaSmart. Consulte [chat](docs/service-chat.md), [ordem de importação](docs/xano-import-order.md) e [deploy](docs/streamlit-deploy.md).

Contas Xano/Streamlit não são contas do portal. O cadastro público cria somente clientes; o administrador habilita atendentes. Não publique senhas, tokens ou o arquivo real de Secrets. Recuperação de acesso depende do responsável pelo sistema, conforme [controle de acesso](docs/access-control.md).

## Interface empresarial e acesso pelo celular

A versão 2026.10.30.2 traz tema empresarial, cabeçalhos compactos e formulários consistentes. Até 900px, o seletor Navegar para e a saída ficam no conteúdo. Até 640px, colunas e métricas empilham e botões usam a largura disponível. Filtros de relatórios ficam no conteúdo do portal. A navegação permanece restrita ao perfil verificado. A interface foi confirmada no Streamlit. A revisão de novembro ajusta o espaço abaixo da barra fixa em telas estreitas. Veja as [evidências e limites](docs/corporate-responsive-interface.md) e a [mudança OpenSpec](openspec/changes/archive/2026-11-11-corporate-responsive-interface/tasks.md).

## Chat de atendimento

O chat privado abre após a chamada para o cliente e o atendente responsável, mostra até 50 mensagens de até 500 caracteres e deixa de permitir acesso ao finalizar o atendimento. Não há anexos, WhatsApp, SMS ou notificações push. Consulte a [ativação e os testes de implantação](docs/service-chat.md).

## Configuração para outras empresas

O modelo adotado é **uma instalação independente por empresa**, com aplicativo, workspace Xano, Secrets e usuários próprios. Não é um SaaS compartilhado.

O catálogo administrativo está publicado e foi testado no Xano e na demonstração Streamlit. Administradores podem criar serviço e fila, editar nomes e duração estimada e abrir/fechar filas, preservando os registros históricos. Depois de salvar, a interface seleciona a fila confirmada e atualiza os dados sem repetir a escrita. Guichês usam o cadastro administrativo de atendentes.

Configuração opcional nos Secrets:

```toml
[company]
name = "Minha empresa"
primary_color = "#2457A7"
catalog_enabled = true
```

Ative o catálogo somente após publicar e testar `POST admin/catalog` no workspace de destino. O modelo de Secrets mantém essa opção desativada por padrão. A cor configura a marca; ajuste também `primaryColor` em `.streamlit/config.toml` para os controles nativos. A criação atual produz um serviço com uma fila; editar o serviço afeta suas filas vinculadas.

Consulte o [guia de instalação](docs/company-installation.md), a [ordem de importação](docs/xano-import-order.md) e o [checklist](openspec/changes/company-install/tasks.md). A demonstração não comprova prontidão comercial. Ainda faltam provisionar a primeira empresa real e validar capacidade, backups/restauração e monitoramento. Logotipo personalizado, horários automáticos e cobrança por assinatura não fazem parte da implementação atual.

## Operação sem dados de desenvolvimento

As telas não exibem painel técnico nem corpo de resposta da API. O modelo operacional de Secrets contém somente integrações e personalização; a carga de fixtures fica em `scripts/seed-secrets.toml.example`, exclusiva de workspace descartável e executada manualmente com `--config`. Não use a carga de testes na operação. A suíte de testes é mantida para evitar regressões. A remoção de registros de teste já persistidos no Xano é independente do deploy e exige identificação e confirmação antes de exclusão definitiva.

### Controle de chamadas ao Xano

O transporte compartilha um intervalo mínimo de 2,5 segundos por host entre sessões e clientes do mesmo processo Streamlit. Após HTTP 429, novas chamadas aguardam pelo menos 30 segundos (ou Retry-After numérico maior). Operações não são repetidas automaticamente. Acompanhamento de senhas consulta a cada 30 segundos. Isso reduz rajadas no plano gratuito; não aumenta sua capacidade. Outros processos e consultas externas ainda podem consumir o limite. Testes: 253 aprovados; OpenSpec: 29 itens válidos. Duas sessões (cliente e atendente) concluíram o fluxo no deploy em 25/11/2026 sem HTTP 429 visível. Testes de carga permanecem pendentes.
