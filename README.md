# FilaSmart — Manual de uso

## 1. Apresentação

O **FilaSmart** é um aplicativo web para organizar filas e atendimentos presenciais por serviço e guichê. O cliente retira uma senha, acompanha sua posição e conversa com o atendente quando chega sua vez. A equipe chama as senhas e conclui os atendimentos; o administrador configura a operação e consulta os indicadores.

A solução busca reduzir a desorganização das filas, a falta de informação durante a espera e a dificuldade de acompanhar os resultados do atendimento.

**Público-alvo:** clientes, profissionais de atendimento e gestores de estabelecimentos com atendimento presencial, como assistências técnicas, salões e centrais de serviços. O exemplo deste manual utiliza uma assistência técnica.

O projeto tem finalidade acadêmica. A interface utiliza Streamlit e os dados e regras de negócio são mantidos no Xano. As especificações e mudanças são organizadas com OpenSpec.

## 2. Acesso ao aplicativo

**Acesse:** [https://filasmarttech.streamlit.app/](https://filasmarttech.streamlit.app/)

É necessário ter conexão com a internet e um navegador atualizado. O aplicativo pode ser utilizado no computador ou no celular, sem instalar um programa.

1. Abra o endereço publicado.
2. Se já possui uma conta do FilaSmart, selecione **Entrar**, informe **E-mail** e **Senha** e clique em **Entrar**.
3. Se ainda não possui conta, siga o cadastro descrito na seção 5.1.
4. Após a verificação da conta, o aplicativo apresenta apenas as áreas permitidas para seu perfil.

**Resultado esperado:** seu nome e perfil aparecem na navegação, junto das funcionalidades autorizadas.

No computador, use o menu lateral. Em telas menores, utilize o seletor **Navegar para** apresentado no conteúdo. Para encerrar a sessão, clique em **Sair**. Sair não cancela uma senha já emitida. Recarregar a página pode exigir novo login.

As contas das plataformas GitHub, Streamlit e Xano não substituem a conta do FilaSmart. O cadastro público cria somente clientes. O acesso de atendente depende de liberação administrativa; o de administrador é provisionado pelo responsável pelo sistema. Não há credenciais administrativas públicas neste manual.

Se a hospedagem apresentar uma tela de suspensão por inatividade, utilize a opção de reativação disponível e aguarde o carregamento. Em caso de perda de acesso, procure o responsável pelo sistema: não há recuperação de senha pela interface atual.

## 3. Perfis de usuários

O perfil é verificado pelo servidor após o login. O usuário não escolhe suas permissões no formulário de acesso.

| Perfil | Responsabilidade | Áreas e permissões |
| --- | --- | --- |
| **Cliente** | Solicitar um serviço e acompanhar sua vez. | **Cliente**, **Acompanhar senha** e **Painel TV**. Emite senha, baixa comprovante e utiliza o chat do próprio atendimento quando chamado. Não administra serviços, equipe ou relatórios. |
| **Atendente** | Realizar os atendimentos autorizados para seu vínculo de trabalho. | **Administração**, com o painel operacional, e **Painel TV**. Seleciona a fila autorizada, chama a próxima senha, conversa com o cliente do atendimento e finaliza o serviço. Não libera outros atendentes nem consulta relatórios administrativos. |
| **Administrador** | Configurar a operação e acompanhar seus resultados. | **Administração**, **Relatórios**, **Totem**, **Cliente**, **Acompanhar senha** e **Painel TV**. Libera atendentes e administra o catálogo habilitado para a instalação. O painel de chamadas operacionais é utilizado pela conta de atendente. |

O **Totem** é um modo de emissão de senhas, não um perfil selecionável no cadastro público. No portal publicado, sua área é disponibilizada ao administrador. A referência do comprovante permite acompanhar uma senha, mas não concede acesso ao chat.

## 4. Funcionalidades

- Cadastro de clientes e login com verificação de perfil.
- Liberação administrativa de atendentes por estabelecimento e guichê.
- Escolha de serviço, emissão de senha e download do comprovante.
- Acompanhamento de status, posição e espera estimada, quando disponíveis.
- Chamada da próxima senha e conclusão do atendimento pela equipe.
- Chat privado entre o cliente e o atendente responsável durante o atendimento chamado.
- Painel TV com senha, destino/guichê, chamadas recentes, opção de som e modo apresentação.
- Emissão de senhas pelo Totem.
- Cadastro e edição de serviços e filas, com duração estimada e abertura/fechamento de filas, quando o catálogo está habilitado.
- Relatórios por período, estabelecimento, serviço e fila, com volumes, tempos médios, status, atividade diária e detalhamento.
- Interface adaptada para navegação em computadores e celulares.

## 5. Manual de utilização

### 5.1. Criar uma conta e entrar

1. Na tela inicial, abra a aba **Criar conta**.
2. Preencha **Nome completo** e **E-mail de cadastro**.
3. Em **Crie uma senha**, informe uma senha de 10 a 128 caracteres.
4. Repita a mesma senha em **Confirme a senha**.
5. Clique em **Criar conta** e aguarde a confirmação.
6. Abra **Entrar** e utilize o e-mail e a senha cadastrados.

**Resultado esperado:** uma conta de cliente é criada e, após o login, sua área de atendimento é liberada. Se houver uma mensagem de validação, corrija os campos indicados antes de reenviar. Criar outra conta não recupera uma senha esquecida.

### 5.2. Cliente: escolher o serviço e emitir a senha

1. Entre com sua conta de cliente e abra **Cliente**.
2. No campo **Serviço**, selecione o atendimento desejado. A opção mostra o serviço e a fila correspondente.
3. Clique uma vez em **Emitir senha** e aguarde a confirmação.
4. Confira o número apresentado em **Sua senha**.
5. Clique em **Baixar comprovante** e guarde o arquivo para consultar a referência de acompanhamento.
6. Acompanhe o **Status**, a **Posição na fila** e a **Espera estimada**, quando apresentados.

**Resultado esperado:** o sistema confirma a emissão e inclui a senha na fila escolhida. Enquanto aguarda, o status é `aguardando`. Ao ser chamada, a senha passa a `chamado`, e a tela orienta o cliente a verificar o guichê.

A atualização é periódica, aproximadamente a cada 30 segundos, podendo demorar mais em caso de falha ou limitação de consultas. A espera é uma estimativa, não uma garantia de horário.

O botão **Iniciar novo atendimento** aparece após a emissão de uma senha e limpa o acompanhamento local e permite iniciar outra solicitação; não cancela uma senha já emitida. Guarde o comprovante antes de utilizar essa opção.

### 5.3. Cliente: acompanhar uma senha pelo comprovante

1. Após entrar no portal, abra **Acompanhar senha**.
2. Copie do comprovante a **Referência de acompanhamento**. Ela é diferente do número da senha.
3. Cole a referência no campo com esse nome e clique em **Acompanhar**.
4. Confira o serviço, a fila, o status e a data da última atualização.
5. Se necessário, utilize **Atualizar agora**, sem realizar cliques repetidos.

**Resultado esperado:** os dados da senha correspondente são apresentados enquanto a referência estiver disponível. Após o encerramento ou a indisponibilidade da referência, a tela informa que o acompanhamento não está disponível.

Trate a referência como informação de acesso ao acompanhamento. Ela não permite ler ou enviar mensagens do chat.

### 5.4. Cliente e atendente: trocar mensagens

**Pré-requisito:** a senha deve ter sido emitida pela conta de cliente e chamada pelo atendente responsável. O chat precisa estar habilitado na instalação.

1. O cliente mantém sua sessão em **Cliente**.
2. O atendente abre **Administração** e seleciona a fila do atendimento chamado.
3. Ambos localizam **Chat do atendimento**, identificado pela senha e pelo guichê.
4. Digite a mensagem em **Escreva uma mensagem** e clique no botão de envio com a seta.
5. Aguarde a atualização da outra sessão para conferir o recebimento e a resposta.

**Resultado esperado:** as mensagens aparecem na mesma conversa para os dois participantes autorizados. Antes da chamada, o cliente recebe a orientação de que o chat abre quando sua senha for chamada. Depois da conclusão, a interface deixa de disponibilizar a conversa.

O chat exibe até 50 mensagens, com limite de 500 caracteres por mensagem. Não envia anexos nem notificações por WhatsApp, SMS ou push. Senhas emitidas pelo Totem não recebem chat de cliente.

### 5.5. Atendente: chamar e concluir um atendimento

**Pré-requisito:** conta liberada pelo administrador, com estabelecimento e guichê definidos.

1. Entre com a conta de atendente e abra **Administração**.
2. Em **Fila sob sua responsabilidade**, selecione a fila a atender.
3. Clique em **Atualizar filas** para consultar o estado da operação.
4. Confira **Senhas aguardando** e verifique se já existe uma senha em atendimento.
5. Quando disponível, clique em **Chamar próxima senha**.
6. Confira a **Senha em atendimento** e realize o atendimento no guichê. Utilize o chat para orientar o cliente, se necessário.
7. Ao terminar o serviço, clique em **Finalizar atendimento atual**.
8. Confira o encerramento antes de chamar a próxima senha.

**Resultado esperado:** a chamada seleciona a próxima senha elegível da fila, registra o atendimento e informa o destino ao cliente/painel. A conclusão encerra esse atendimento e seu chat.

Se não há senhas aguardando, **Chamar próxima senha** fica desabilitado. Se há atendimento ativo na fila, conclua-o antes de chamar outro. **Finalizar atendimento atual** fica desabilitado quando não há atendimento ativo.

### 5.6. Administrador: liberar um atendente

1. Peça ao profissional para criar sua própria conta pela aba **Criar conta**.
2. Entre com uma conta administrativa e abra **Administração**.
3. Na seção **Cadastrar atendente**, informe o **E-mail da conta do atendente**, igual ao utilizado no cadastro.
4. Selecione o **Estabelecimento do atendente** e informe o **Guichê de atendimento**.
5. Confira os dados e marque **Confirmo a liberação desta conta para atender neste estabelecimento**.
6. Clique em **Cadastrar atendente**.
7. Oriente o profissional a sair e entrar novamente com a mesma conta e senha.

**Resultado esperado:** após a confirmação e o novo login, a conta passa a utilizar as funcionalidades de atendente no vínculo autorizado.

Essa operação é destinada a uma conta de cliente existente, sem vínculo anterior de atendimento. Contas administrativas e técnicas não são convertidas pelo formulário. O profissional deve definir a própria senha; não é necessário compartilhá-la com o administrador.

### 5.7. Administrador: cadastrar ou editar serviços e filas

**Pré-requisito:** catálogo habilitado pelo responsável pela instalação.

**Serviço** é o atendimento oferecido (ex.: avaliação técnica). **Fila** organiza as senhas que aguardam esse atendimento (ex.: recepção técnica). Os nomes podem ser iguais, mas representam conceitos diferentes. Quando existe um único estabelecimento autorizado, ele aparece como informação fixa; com mais de um, escolha o desejado.

1. Abra **Administração** e localize **Serviços e filas da empresa**.
2. Para criar, selecione **Novo serviço e fila** no campo **Serviço e fila**.
3. Escolha o **Estabelecimento do serviço**.
4. Preencha **Nome do serviço**, **Duração estimada (minutos)** e **Nome da fila**.
5. Selecione o **Estado da fila**: `aberta` ou `fechada`.
6. Clique em **Salvar serviço e fila** e aguarde a confirmação.
7. Para editar, escolha uma opção existente em **Serviço e fila**, ajuste os campos permitidos e salve novamente.

**Resultado esperado:** a criação registra um serviço e uma fila. As alterações confirmadas passam a compor o catálogo da instalação.

Fechar uma fila pausa sua operação disponível e preserva senhas e histórico. Editar um serviço afeta suas filas vinculadas. A edição não transfere o serviço para outro estabelecimento. A interface atual não oferece exclusão de histórico nem criação de várias filas para um serviço existente pelo mesmo formulário.

### 5.8. Administrador: consultar relatórios

1. Abra **Relatórios**.
2. Em **Filtros do relatório**, selecione o **Estabelecimento**.
3. Escolha um **Serviço** e, quando houver várias filas, uma **Fila**, ou mantenha as opções de todos. Se o serviço possui uma única fila, o aplicativo a utiliza automaticamente e mostra seu nome. Um único estabelecimento autorizado também aparece como informação fixa.
4. Defina **Data inicial (UTC)** e **Data limite (UTC)**.
5. Clique em **Gerar relatório**.
6. Consulte senhas emitidas, chamadas, atendimentos concluídos, percentual de senhas do período concluídas, espera média e duração média.
7. Observe o status dos tickets, o gráfico de **Atividade diária** e o **Detalhamento por serviço e fila**.
8. Para outra consulta, altere os filtros e clique novamente em **Gerar relatório**.

**Resultado esperado:** os indicadores refletem o período e o escopo solicitados. Se não houver eventos ou amostras, o aplicativo informa essa condição.

A data final não entra na consulta. Por exemplo, de **25/11/2026** até **26/11/2026** consulta o dia 25 em UTC. UTC e horário de São Paulo são diferentes; considere essa diferença ao analisar um dia de operação. O percentual de senhas do período concluídas se refere ao conjunto de senhas emitidas no período; chamadas e conclusões no período podem incluir senhas emitidas anteriormente.

### 5.9. Funcionalidades complementares: Totem e Painel TV

| Área | Como utilizar | Resultado esperado |
| --- | --- | --- |
| **Totem** — administrador no portal publicado | Escolha o **Serviço**, clique em **Emitir senha**, baixe o comprovante e utilize **Acompanhar minha senha**. Para outra pessoa, guarde o comprovante e use **Iniciar novo atendimento**. | Senha confirmada e referência para acompanhamento. A nova sessão não cancela a senha anterior. Não há chat vinculado à identidade do cliente nessa modalidade. |
| **Painel TV** — perfis autorizados | Abra **Painel TV**, ajuste **Atualizar a cada** e, se desejar, **Ativar som** e **Modo apresentação**. | Exibição da senha chamada, destino/guichê e chamadas recentes. Sem chamada, aparece a orientação de espera. O som depende das permissões de reprodução do navegador. |

No plano gratuito, prefira intervalos maiores de atualização do Painel TV e evite deixar várias telas de consulta abertas desnecessariamente.

### 5.10. Situações alternativas e recuperação

| Situação | O que fazer | Resultado esperado |
| --- | --- | --- |
| Nenhuma fila disponível | Aguarde a abertura ou procure o responsável pelo estabelecimento. | A emissão só pode prosseguir com uma fila disponível. |
| Login não confirmado ou sessão expirada | Confira as credenciais; se solicitado, entre novamente. Se a verificação estiver temporariamente indisponível, aguarde e utilize **Tentar novamente** quando apresentado. | A navegação protegida só é liberada com a sessão verificada. |
| HTTP 429 ou excesso de consultas | Aguarde o intervalo indicado; ele pode ser de 30 segundos ou maior. Evite atualizar várias abas repetidamente. | As consultas podem ser retomadas após a liberação do serviço. A capacidade não é ampliada por novas tentativas. |
| Emissão, chamada, conclusão ou envio sem confirmação | Confira o estado da senha ou a conversa antes de repetir. Se não puder confirmar, procure o responsável. | Evitar duplicar uma operação que pode já ter sido processada. |
| Informação desatualizada | Observe a data da última atualização e o aviso de falha. Não trate um dado antigo como confirmação atual. | O usuário identifica quando está vendo o último resultado confirmado. |
| Relatório vazio | Confira período, estabelecimento, serviço e fila e gere a consulta novamente. | Exibição de dados existentes ou mensagem de ausência de eventos. |

## 6. Exemplos de utilização

### Cenário: assistência técnica de aparelhos

O catálogo de exemplo da demonstração inclui os serviços abaixo. O administrador pode adaptá-los; nomes, disponibilidade, números de senha e indicadores podem mudar com o uso.

| Serviço | Aplicação no cenário |
| --- | --- |
| **Entrega de aparelho** | Receber o equipamento do cliente para atendimento. |
| **Avaliação técnica e orçamento** | Atender o cliente interessado na avaliação e no orçamento. |
| **Retirada de aparelho reparado** | Organizar a entrega de um equipamento cujo reparo já terminou. |

**Jornada completa de exemplo:**

1. O cliente entra no FilaSmart e escolhe **Entrega de aparelho**.
2. Clica em **Emitir senha**, anota o número gerado e baixa o comprovante.
3. O atendente entra em outra sessão, seleciona a fila **Entrega de aparelho**, atualiza a consulta e chama a próxima senha.
4. Quando a senha desse cliente for chamada, o atendente envia: “Sua senha foi chamada. Pode vir ao Guichê 1.”
5. O cliente recebe a mensagem e responde: “Recebi a chamada. Estou indo ao guichê.”
6. Após receber o aparelho, o atendente finaliza o atendimento.
7. O cliente vê o acompanhamento encerrado, e o chat deixa de estar disponível.
8. O administrador gera um relatório filtrando **Entrega de aparelho** e um período que inclua essa operação.

**Resultado esperado:** a solicitação percorre emissão, espera, chamada, comunicação e conclusão, com registros disponíveis para os indicadores administrativos. O número emitido é determinado pelo sistema; **Guichê 1** é apenas o exemplo do vínculo utilizado.

Para uma apresentação, prepare previamente uma conta de cliente, uma conta de atendente liberada e uma conta administrativa. Utilize sessões independentes de navegador para manter os perfis separados e não exponha senhas na gravação. As contas administrativas devem ser obtidas com o responsável pelo projeto.

**Caminhos alternativos:** sem senhas aguardando, o botão de chamada fica desabilitado; uma consulta administrativa sem eventos apresenta mensagem de ausência de dados. Não é necessário apagar registros para demonstrar esses estados.

## 7. Limitações conhecidas

- **Capacidade do Xano:** o plano utilizado pode responder HTTP 429. Há controle de intervalo entre chamadas e pausa após limitação, mas isso não garante operação com muitos usuários simultâneos. A capacidade e os testes de carga continuam pendentes.
- **Atualização periódica:** acompanhamento e chat consultam aproximadamente a cada 30 segundos; falhas podem ampliar a pausa. Não há atualização instantânea garantida. A orientação de atualização apresentada nas telas corresponde ao agendamento de 30 segundos.
- **Disponibilidade:** a hospedagem Streamlit Community Cloud pode suspender o aplicativo por inatividade. Não há garantia de disponibilidade contínua.
- **Chat:** somente texto, até 500 caracteres por mensagem e até 50 mensagens visíveis. Não há anexos, WhatsApp, SMS, push ou consulta da conversa encerrada pela interface. A conclusão bloqueia o acesso ao chat, mas não apaga automaticamente as mensagens armazenadas.
- **Acesso:** sem recuperação de senha pelo portal, escolha pública de perfil ou cadastro público de administrador. Atendentes precisam de liberação administrativa. Referências antigas de acompanhamento podem ficar indisponíveis.
- **Gestão de registros:** não há exclusão de histórico ou cancelamento de senha pelo cliente na interface descrita. **Iniciar novo atendimento** e **Sair** não cancelam senhas.
- **Catálogo:** a criação pelo formulário gera um serviço com uma fila; a edição do serviço afeta filas vinculadas. O catálogo depende de ativação e permissões da instalação.
- **Escopo entregue:** avaliação de satisfação, notificações externas, logotipo personalizado, horários automáticos e cobrança por assinatura não fazem parte dos fluxos implementados neste portal.
- **Outras empresas:** o modelo é uma instalação independente por empresa, com aplicativo, Xano, configurações e usuários próprios. Não há provisionamento automático nem SaaS compartilhado. A primeira instalação comercial, capacidade, backups/restauração e monitoramento ainda precisam de validação.
- **Dados de demonstração:** o ambiente acadêmico pode conter registros de apresentações anteriores. Seus indicadores não representam a operação de uma empresa real. Não insira dados pessoais sensíveis para testar o aplicativo.

---

<details>
<summary><strong>Informações técnicas para manutenção e desenvolvimento</strong></summary>

### Estrutura e documentação

| Caminho ou guia | Finalidade |
| --- | --- |
| `app.py` | Entrada do portal unificado publicado. |
| `views/` e `assets/` | Telas, componentes e apresentação visual. |
| `backend_queue.py`, `portal_session.py` e `*_client.py` | Operações, sessão e integração com APIs. |
| `xano/` | Exports das tabelas, APIs e funções; precisam ser publicados no Xano. |
| `tests/` | Testes Python e contratos. |
| `openspec/specs/` | Especificações vigentes. |
| `openspec/changes/` e `archive/` | Mudanças em acompanhamento e histórico. |
| [Acesso e permissões](docs/access-control.md) · [Cadastro](docs/account-registration.md) · [Chat](docs/service-chat.md) | Detalhes dos fluxos e registros de validação. |
| [Modelo de domínio](docs/domain-model.md) · [Visão do projeto](docs/project-overview.md) | Contexto técnico; objetivos históricos não equivalem a funcionalidades entregues. |
| [Deploy](docs/streamlit-deploy.md) · [Importação Xano](docs/xano-import-order.md) · [Instalação por empresa](docs/company-installation.md) | Configuração e operação. |
| [Fluxo OpenSpec](docs/openspec-workflow.md) · [Revisão de 24/11/2026](docs/review-2026-11-24.md) · [Concorrência](docs/queue-concurrency-validation.md) | Processo, evidências e pendências. |

### Executar localmente

Pré-requisito: Python 3.11 ou superior, além de uma instalação Xano configurada.

```bash
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Copie `.streamlit/secrets.toml.example` para `.streamlit/secrets.toml` e preencha os valores conforme o [guia de deploy](docs/streamlit-deploy.md). Não versione o arquivo real de Secrets.

```bash
streamlit run app.py
```

No deploy existente, `app.py` utiliza a branch `codex/streamlit-deployment-preparation`. Atualizar o GitHub não publica automaticamente exports no Xano.

As seções de configuração são `[xano]`, `[tv_display]`, `[analytics]` e `[company]`. Em novas instalações, chat e catálogo devem ser ativados somente após publicação e validação de seus endpoints. Consulte os guias antes de alterar `service_chat_enabled` ou `catalog_enabled`. Não publique tokens, senhas nem contas técnicas.

### Testes e OpenSpec

```bash
python -m pip install pytest
python -m pytest -q
npm ci --ignore-scripts
npm run spec:list
npm run spec:validate
```

Node.js 20.19+ é necessário somente para a ferramenta OpenSpec; o CI utiliza Node 24 e a CLI está fixada em 1.15.0. Leia [AGENTS.md](AGENTS.md) e o [fluxo OpenSpec](docs/openspec-workflow.md) antes de desenvolver. O OpenSpec organiza especificações e mudanças; não exige mover a aplicação para dentro dessa pasta.

A revisão de 24/11/2026 registrou 253 testes Python aprovados e 28 itens OpenSpec válidos em modo estrito. Esses números são evidências daquela revisão, não uma nova execução causada por esta atualização documental. Testes locais não substituem publicação e testes no Xano, validação do deploy ou testes de carga.

O transporte limita chamadas por host no mesmo processo Streamlit e aguarda após HTTP 429. Isso reduz rajadas, sem aumentar o limite do serviço nem controlar outros consumidores da API. Mutações não são repetidas automaticamente.

As cargas de desenvolvimento são exclusivas de ambiente descartável, com configuração separada. Não as utilize para operar uma instalação real. Limpeza de dados no Xano é uma ação independente da atualização deste README.

</details>

*Manual revisado em 25/11/2026 para a apresentação acadêmica. As limitações acima descrevem a versão entregue, e não uma garantia de prontidão comercial.*
