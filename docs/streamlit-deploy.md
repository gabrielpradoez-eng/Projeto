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

- A administração mantém cadastros, senhas e logs em memória na sessão, além de fazer chamadas para alguns endpoints. É necessário integrar essas operações e suas leituras ao Xano e validar os fluxos entre sessões.
- Configure as credenciais e permissões das contas e do painel de TV no Xano e teste cada perfil e operação.
- Valide a instalação, os testes e os fluxos completos no ambiente de destino antes de tratar o deploy como pronto.
