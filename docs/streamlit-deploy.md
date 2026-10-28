# Preparação para deploy do FilaSmart

O ponto de entrada da aplicação unificada é `app.py`. As dependências de execução estão em `requirements.txt`.

Para executar localmente após instalar as dependências:

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

Configure os segredos do Streamlit seguindo `.streamlit/secrets.toml.example`. No Streamlit Community Cloud, use as configurações de Secrets da aplicação; localmente, use `.streamlit/secrets.toml`, que é ignorado pelo Git. Não publique credenciais nem envie o arquivo de segredos ao repositório.

Os endereços de login, filas, emissão, acompanhamento, painel de TV e relatórios devem apontar para os endpoints reais do workspace Xano. O painel de administração também usa `[xano].base_url`; a URL de autenticação e a URL dos endpoints de filas podem pertencer a grupos de API diferentes, e é necessário conferir o contrato antes da implantação.

Antes de importar os componentes do Xano, consulte `docs/xano-import-order.md` e confirme as correções e restrições de segurança indicadas. Use inicialmente um workspace de teste, sem dados reais. Não habilite o endpoint de seed em produção.

## Pendências antes do uso completo

- O painel de atendentes consulta `attendant/dashboard` para ler filas e o atendimento atual no Xano. Cadastros devem ser mantidos no console Xano até existir uma API administrativa com autorização adequada. A interface não oferece mais os cadastros temporários da sessão.
- Configure `login_url` do grupo Authentication e `base_url` do grupo Queue Management. O login legado com `authToken` e `user_id` é confirmado por `auth/me` (ou `me_url` explícita).
- Configure as credenciais e permissões das contas e do painel de TV no Xano e teste cada perfil e operação.
- Valide a instalação, os testes e os fluxos completos no ambiente de destino antes de tratar o deploy como pronto.

## Verificações antes de aplicar os exports

Os exports atualizados de `complete` e `call_next` incluem guardas de permissão e estado. Os exports de autenticação e reset limitam a auditoria a IDs, evitando registrar o objeto inteiro do usuário. Essas alterações de XanoScript não são aplicadas ao servidor por um commit no GitHub: valide-as no workspace antes de publicar.

Os testes Python usam respostas simuladas, incluindo finalização após troca de sessão, timeout sem repetir mutações e respostas incompletas. Eles não validam a execução do XanoScript nem concorrência real. Antes de usar com público, teste chamadas simultâneas para confirmar ausência de senha duplicada e de dois atendimentos da mesma senha; uma transação isoladamente não demonstra essa garantia.


## Validação de runtime em 28/10/2026

Exports de autenticação, autorização e operações corrigidos foram publicados no Xano. Em dados identificados como teste, foram validados: emissão pelo cliente, chamada pelo atendente, finalização com status concluido e horário de encerramento, rejeição de finalização repetida, rejeição de administrador na finalização, painel sem atendimento ativo após encerramento, filtros administrativos e relatório com uma senha emitida/chamada/concluída. O relatório também passou sem os filtros opcionais de serviço/fila.

Os horários de atendimento de teste atravessaram duas sessões; a duração longa exibida no relatório corresponde a esse intervalo, não a uma simulação de atendimento normal.

Os fluxos positivos de Totem/TV ainda dependem de perfis/credenciais próprios; não foram considerados aprovados apenas por compilação. O deploy Streamlit ainda não foi executado.


### Revisão adicional de acesso e inicialização

O formulário administrativo permanece vazio mesmo quando Secrets de bootstrap estão presentes. O provisionamento de TV valida o estabelecimento autorizado antes de criar a credencial. Os endpoints Totem/issue e TV/register rejeitaram o perfil de cliente no runtime.

Com uma segunda senha aguardando, stats incluía chamado_at=0 e produzia média negativa. O filtro agora exige timestamp positivo; o teste real confirmou uma pessoa aguardando e média de 4,1 minutos da senha já chamada. A segunda senha está identificada como dado de teste e permanece aguardando.

Validação local atual: 119 testes passaram, compilação Python e git diff --check passaram, health do Streamlit respondeu HTTP 200 e as seis visões abriram sem exceções sem Secrets configurados (exibindo o estado de configuração ausente). Isso não substitui login e operação ponta a ponta contra Xano. As correções de stats e TV/register foram publicadas. Os testes positivos Totem/TV aguardam autorização específica para as identidades técnicas e credenciais de display.


### Testes positivos de Totem e TV concluídos

Após autorização específica do usuário, foram criados uma identidade técnica Totem e um display de teste, ambos restritos ao estabelecimento de teste. A identidade não recebeu senha de login; tokens internos do console foram usados nos testes. As credenciais de display e rastreamento não foram incluídas no repositório.

Totem/queues retornou apenas a fila autorizada. Totem/issue emitiu a senha 3, cujo rastreamento mostrou inicialmente posição 2 e previsão de 10 minutos. A chamada atendeu a senha 2 antes da 3; após finalizar a 2, o rastreamento da 3 mudou para posição 1 e previsão zero. Ao chamar a 3, o rastreamento mostrou chamado sem posição/previsão, e o feed da TV mostrou a 3 como atual, com 2 e 1 no histórico.

A finalização da 3 gravou o horário de revogação no banco e invalidou a referência no primeiro bloqueio do rastreamento. O export de finalização agora inclui timestamps de revogação vazios representados por null ou zero. Todas as três senhas de teste estão concluídas.

Validação local atual: 120 testes, compilação Python e git diff --check aprovados. Os testes no console Xano não substituem login com senha pela aplicação Streamlit. Para deploy, ainda são necessárias a conta Streamlit e a configuração privada das credenciais operacionais; a identidade técnica de teste não está pronta para login com senha.
