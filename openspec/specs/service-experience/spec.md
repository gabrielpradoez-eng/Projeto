# service-experience Specification

## Purpose
Organizar emissão, comprovantes e apresentação visual para orientar clientes e operação durante o atendimento.

## Requirements

### Requirement: Emissão consciente
Após confirmação de emissão, o Totem MUST desabilitar a emissão nesta sessão até o cliente iniciar novo atendimento. Reiniciar a sessão MUST limpar o comprovante anterior sem cancelar a senha no backend.

#### Scenario: Nova emissão na mesma sessão
- **WHEN** a sessão já tem uma senha confirmada
- **THEN** a emissão permanece bloqueada até reinício explícito; a senha no backend não é cancelada.

### Requirement: Comprovante privado
O cliente MUST poder baixar texto com número, serviço, fila e referência da sua senha. O comprovante MUST NOT conter credenciais de integração nem aparecer no painel TV.

#### Scenario: Download do comprovante
- **WHEN** um cliente baixa o comprovante da própria senha
- **THEN** o arquivo contém sua referência sem credenciais e não aparece no painel TV.

### Requirement: Apresentação acessível
As telas MUST manter rótulos, foco de teclado e disposição responsiva. Horários válidos MUST ser apresentados no fuso America/Sao_Paulo, sem alterar o valor persistido no backend. Valores inválidos MUST ser apresentados como indisponíveis.

#### Scenario: Horário local legível
- **WHEN** um horário válido é exibido em tela responsiva
- **THEN** o valor é apresentado no fuso de São Paulo sem modificar o dado persistido.

### Requirement: TV em destaque
O modo apresentação MUST ampliar a chamada sem desativar atualizações ou alertas. A opção de sair do modo MUST continuar visível.

#### Scenario: Entrada e saída de apresentação
- **WHEN** o usuário ativa e depois encerra o modo apresentação da TV
- **THEN** a chamada é ampliada durante o modo e as atualizações continuam ativas.

### Requirement: Corporate responsive portal
O portal SHALL apresentar identidade empresarial consistente e adaptar o conteúdo à largura disponível, com formulários legíveis e controles acionáveis por toque.

#### Scenario: Narrow screen
- **WHEN** a largura disponível é de até 900 pixels
- **THEN** a navegação entre áreas autorizadas e a saída ficam disponíveis no conteúdo, sem depender da abertura da barra lateral.

#### Scenario: Small phone
- **WHEN** a largura é de até 640 pixels
- **THEN** colunas de conteúdo e métricas empilham, campos mantêm texto legível e botões oferecem pelo menos 44 pixels de altura.

### Requirement: Navigation state remains authorized and consistent
As navegações de desktop e celular MUST compartilhar a área selecionada e mostrar somente opções do perfil verificado.

#### Scenario: Switch using mobile navigation
- **WHEN** o usuário seleciona outra área autorizada pelo seletor da página
- **THEN** a seleção da barra lateral acompanha a mudança e o conteúdo correto é exibido.

#### Scenario: Identity changes
- **WHEN** a sessão expira ou o perfil perde uma permissão
- **THEN** o seletor móvel não permite acesso à área anterior nem mostra conteúdo protegido sem verificação.
