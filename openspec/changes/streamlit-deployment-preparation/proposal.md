## Why

O deploy do FilaSmart precisa instalar as dependências da aplicação e orientar a configuração do Xano sem incluir segredos no repositório.

## What Changes

- Declarar as dependências necessárias ao Streamlit.
- Documentar o ponto de entrada, as configurações e as limitações conhecidas da integração.

## Impact

Não altera regras de negócio nem publica a aplicação ou o Xano. A integração completa depende de um workspace Xano configurado e de validação em ambiente de teste.
