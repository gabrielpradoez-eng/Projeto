- [x] Conferir HEAD 11b5119 e três checks aprovados.
- [x] Integrar PR #1 na main: merge e12a1ee3c2d6207c1fd56878a07aa68b23927130 confirmado no GitHub.
- [x] Confirmar versão 2026.10.30.1 no About do site publicado.
- [x] Examinar documentação oficial sobre transações e bloqueio de registros.
- [x] Validar formulário administrativo em sessão autenticada: login admin confirmado, estabelecimento/guichê carregados e envio sem confirmação bloqueado.
- [ ] Concluir cadastro positivo com senha definida pelo titular e liberação pelo administrador.
- [ ] Executar concorrência real em ambiente Xano acessível; console redirecionou para login.
- [ ] Finalizar verificações dependentes de autenticação e atualizar evidências.

## Histórico do bloqueio de acesso anterior

O formulário seguro de autenticação administrativa expirou no transporte sem resultado confirmado. A aba não estava mais disponível após a espera. A verificação em uma nova aba do domínio correto apresentou login, sem sinal de sessão autenticada. Não houve criação de conta ou concessão de acesso nessa tentativa. O console Xano também exige novo login.

## Continuação autenticada

O formulário seguro foi concluído e o portal confirmou perfil Administrador. A tela Cadastrar atendente carregou Central de Atendimento — Demonstração e bloqueou envio sem confirmação de liberação. Relatórios usaram a mesma sessão e retornaram 17 emissões, 16 chamadas e 16 conclusões. Nenhuma conta foi criada ou promovida. O acesso ao console Xano permanece pendente de login.
