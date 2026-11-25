# interface-clarity Specification

## Purpose
Orientar clientes, atendentes e administradores com seleções contextuais, conceitos claros e relatórios legíveis, preservando autorização e regras do backend.

## Requirements

### Requirement: Escolhas contextuais preservam escopo
A interface MUST apresentar estabelecimento único como informação e manter seleção quando houver múltiplos autorizados.

#### Scenario: Estabelecimento único
- **WHEN** a resposta autorizada contém um estabelecimento
- **THEN** seu nome é exibido como informação e seu ID é usado sem solicitar escolha.

#### Scenario: Alteração de catálogo autorizado
- **WHEN** uma opção anterior desaparece ou novas opções são apresentadas
- **THEN** a seleção é validada contra o catálogo atual sem permitir ID removido.

### Requirement: Fila analítica acompanha o serviço
A interface MUST atualizar filas ao escolher serviço e selecionar automaticamente a única fila desse serviço, sem consultar métricas até Gerar relatório.

#### Scenario: Serviço com fila única
- **WHEN** um serviço específico tem uma fila autorizada
- **THEN** a fila aparece como informação e seu ID é enviado no próximo relatório solicitado.

#### Scenario: Serviço com múltiplas filas
- **WHEN** um serviço tem várias filas autorizadas
- **THEN** o administrador pode escolher uma fila ou todas, sem manter seleção de outro serviço.

### Requirement: Conceitos e datas compreensíveis
A interface MUST explicar serviço e fila, mostrar horários legíveis e explicar a taxa de senhas concluídas e o limite final UTC exclusivo sem recalcular agregados.

#### Scenario: Relatório apresentado
- **WHEN** um relatório válido é exibido
- **THEN** período, geração, gráfico e tabela usam rótulos legíveis preservando dados, ordem e semântica UTC.

### Requirement: Reinício exige atendimento local
Cliente e Totem MUST oferecer Iniciar novo atendimento somente após existência de referência local.

#### Scenario: Antes da emissão
- **WHEN** a sessão não tem referência de senha
- **THEN** o botão de reinício não aparece.

#### Scenario: Reinício com comprovante
- **WHEN** há referência local e o usuário reinicia
- **THEN** os dados locais são limpos sem cancelar a senha no backend.
