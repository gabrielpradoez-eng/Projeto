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
