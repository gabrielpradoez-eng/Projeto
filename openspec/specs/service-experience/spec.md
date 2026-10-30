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
