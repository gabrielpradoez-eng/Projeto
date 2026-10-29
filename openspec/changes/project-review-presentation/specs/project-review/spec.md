## ADDED Requirements
### Requirement: Estado confirmado preservado
Um cliente com senha confirmada MUST continuar podendo baixar o comprovante e consultar o acompanhamento sem depender do catálogo de filas. Respostas inválidas MUST NOT gerar confirmação de emissão nem quebrar a renderização.

### Requirement: Seleção operacional válida
Se a fila selecionada deixar de existir na resposta autorizada do atendente, a interface MUST selecionar uma opção válida antes de instanciar o widget. IDs inválidos e contagens negativas MUST ser rejeitados.

### Requirement: Histórico de chamadas correto
O feed MUST ordenar por horário de chamada e usar ID apenas como desempate. A TV MUST identificar o serviço quando informado pelo backend para distinguir senhas com o mesmo número em filas diferentes.

### Requirement: Dados de demonstração seguros
A preparação MUST usar transação, precondições de escopo e chaves idempotentes. MUST NOT criar credenciais, mudar perfis ou excluir registros. Repetir a execução MUST manter as contagens e não duplicar histórico. O estabelecimento MUST estar identificado como demonstração.

### Requirement: Mensagens adequadas ao perfil
O cliente MUST receber mensagens de erro úteis sem payloads ou códigos internos. Diagnósticos técnicos sanitizados MUST ficar em área recolhida e restrita à interface administrativa.
