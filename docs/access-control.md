# Acesso ao FilaSmart

O aplicativo unificado publicado abre na tela de login. Use uma conta do sistema, cadastrada na tabela `usuarios` do Xano. A conta usada para administrar a plataforma Xano ou o deploy Streamlit não cria automaticamente uma conta no aplicativo.

| Perfil no Xano | Área liberada |
| --- | --- |
| `usuario` | Cliente, Acompanhar senha e Painel TV |
| `atendente` | Administração (operação de atendimento) e Painel TV |
| `admin` | Administração, Relatórios, Totem, Cliente, Acompanhar senha e Painel TV |

O perfil é obtido pelo servidor em `auth/me`; não existe escolha de perfil no formulário. Contas técnicas do Totem não são contas de acesso ao portal. Cadastro e recuperação de senha são feitos pelo responsável pelo estabelecimento. Esta mudança não cria contas nem altera permissões de registros existentes.

Após login, os relatórios utilizam o token administrativo da mesma sessão. O núcleo de atendimento usa o token do atendente, e o Xano continua validando o vínculo e o estado de cada operação. A emissão de senhas mantém o serviço de Totem configurado no servidor; esta mudança não migra a titularidade histórica das senhas para a conta do portal.

Cada navegação completa confirma novamente a sessão. Durante atualizações automáticas, a confirmação remota é repetida em até 60 segundos. Token inválido, usuário removido ou perfil não reconhecido bloqueiam a navegação e limpam a sessão. Indisponibilidade temporária de verificação pausa o acesso até que a confirmação seja possível.

O botão Sair limpa os tokens e os dados locais de atendimento, relatórios e TV. Isso encerra a sessão do navegador; não cancela senhas emitidas nem revoga globalmente tokens de outros dispositivos. Recarregar o navegador pode solicitar novo login, pois a sessão não é persistida em cookies próprios ou armazenamento local.

Os scripts independentes de demonstração, como `kiosk_app.py`, não são rotas do deploy unificado `app.py`. O controle de acesso descrito aqui refere-se ao aplicativo publicado com esse entrypoint.

Validação da implementação: 163 testes automatizados, incluindo navegação por perfil, logout, verificação canônica, expiração e fragmentos após revogação. O teste positivo com credenciais reais depende de uma conta de aplicativo existente.
