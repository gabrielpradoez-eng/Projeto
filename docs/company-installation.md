# Instalação independente por empresa

## Modelo de entrega

Cada empresa deve receber aplicativo Streamlit, workspace/instância Xano, Secrets, usuários e dados próprios. A configuração nunca é escolhida por um parâmetro do cliente. Não compartilhar a conta técnica, a credencial da TV ou o endpoint de seed entre instalações. Uma filial é um estabelecimento dentro da instalação; uma empresa diferente deve usar outra instalação.

## Provisionamento

1. Criar o workspace dedicado e importar tabelas e APIs na [ordem documentada](xano-import-order.md). Exportar os recursos não publica automaticamente endpoints.
2. Provisionar o estabelecimento e um administrador no backend por procedimento controlado. Não entregar a carga de demonstração nem senhas padrão a clientes. Desabilitar o seed após o provisionamento e manter as variáveis restritas.
3. Criar um aplicativo Streamlit apontando para `app.py` e preencher Secrets com os endpoints e credenciais desse workspace. Não reutilizar as URLs da demonstração para outra empresa.
4. Definir `[company].name` e `primary_color` (hexadecimal de seis dígitos). A identificação aparece no login, barra lateral e título. Ajustar também `primaryColor` em `.streamlit/config.toml` para os controles nativos; a configuração da empresa colore a marca. Logotipo personalizado e horários automáticos não estão implementados nesta entrega.
5. Publicar `POST admin/catalog`. Testar criação, edição, fechamento, reabertura, preservação das senhas e rejeição de alteração por cliente/atendente ou fora do escopo. Depois ativar `catalog_enabled = true`. O modelo para novas instalações mantém o padrão desativado; o catálogo já foi ativado e testado na demonstração.
6. Em Administração, cadastrar serviços e filas; escolher uma fila existente para editar. A edição do serviço afeta todas as filas já vinculadas a ele. O estabelecimento não pode ser transferido pela edição. Não há exclusão de histórico. A criação produz um serviço e uma fila; criação de várias filas para um serviço existente é uma evolução futura.
7. O profissional cria sua conta e o administrador libera o guichê pelo formulário existente. Cadastrar credencial restrita para o painel TV.
8. Confirmar emissão, chamada, mensagens e conclusão na instalação nova antes de entregá-la.

## Operação e suporte

Definir responsável por cada instalação, canal de suporte e rotina de atualização. Antes de cada atualização, registrar a versão do aplicativo e a versão dos exports e preparar uma cópia recuperável dos dados. Combinar retenção de mensagens com a empresa e validar restauração; esse procedimento não cria backups automaticamente. Definir monitoramento de disponibilidade, erros HTTP 429 e tempo de resposta. Dimensionar hospedagem e Xano com testes controlados de carga antes de assumir capacidade ou SLA.

Não há cobrança automática, gestão de assinaturas, instalação automática de novas empresas nem garantia de operação contínua nesta entrega. O teste acadêmico e os testes locais não certificam prontidão comercial. As pendências estão no [checklist](../openspec/changes/company-install/tasks.md).

## Validação na instalação de demonstração

Em 24/11/2026, o endpoint #4136989 foi criado e executado no Xano: leitura administrativa retornou o catálogo; criação gerou o serviço 5 e fila 5, Orientação cadastral, mantida fechada; edição alterou a duração de 15 para 20 minutos; estabelecimento inexistente foi rejeitado; perfil cliente recebeu acesso negado. A configuração company foi salva no Streamlit. Após atualizar a implantação, o administrador abriu o formulário e salvou a duração em 15 minutos pelo site, com mensagem de sucesso; a fila permaneceu fechada. Nenhuma instalação de uma empresa real foi provisionada.
