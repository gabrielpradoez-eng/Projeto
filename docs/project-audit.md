# Revisão de consistência — 30/10/2026

## Resultado

A revisão partiu do commit `2ea5e099b28cbfd17940f90ba123f0fce5c4148e`, na branch `codex/streamlit-deployment-preparation`. A árvore local estava idêntica ao GitHub antes das correções. A `main` continua em `885fe723663baebe76bdf93b6ffd0fdb2d3e9a73`; o PR #1 permanece aberto e em rascunho, sem merge. Código publicado na branch não significa atualização da main nem publicação dos exports no Xano.

## Problemas encontrados e corrigidos

| Achado | Correção e evidência |
|---|---|
| Cliente analítico aceitava opções malformadas | IDs, rótulos, duplicatas e vínculos são verificados antes de renderizar relatórios ou cadastro de atendentes. |
| Relatórios podiam apresentar valores inválidos | Verificação de filtros, datas, linhas, contagens, médias finitas e percentual, mantendo timestamps numéricos do Xano e médias nulas. |
| Relatório anterior permanecia em cache após mudança de opções | Regressões reproduziram três falhas antes da correção. Alteração de catálogo ou falha ao carregar opções limpa o cache; reordenação isolada preserva relatório válido. |
| Seletores mantinham estabelecimento/serviço removidos | Redefinição antes de instanciar widgets. O cliente não recalcula nem reordena os indicadores de negócio. |
| Documentação de acesso, cadastro e deploy desatualizada | Evidências posteriores foram incorporadas sem apagar o histórico; cadastro não é apresentado como recuperação de senha. |
| Modelo de domínio com bloco Markdown sem fechamento | Diagrama Mermaid e explicação dos vínculos atuais. |
| Specs ainda descreviam a visão de cliente como pública sem esclarecer a sessão | Contratos do portal, sessão compartilhada e emissão alinhados à implementação; navegação verificada sincronizada e arquivada. |
| CI não executava a suíte Python | Novo workflow `Python tests`, sem Secrets e com permissão somente de leitura. |

A implementação não alterou endpoints, perfis, senhas nem dados do Xano. Versão identificadora das correções do portal: **2026.10.30.1**.

## Verificações

- Baseline: 190 testes aprovados. Após correções: **220 testes aprovados**.
- OpenSpec 1.15.0: **21 itens válidos em modo estrito**, com 8 specs vigentes e 13 mudanças em acompanhamento.
- `openspec doctor`: raiz saudável, sem referências quebradas.
- Compilação Python e `git diff --check` aprovados; links relativos da documentação conferidos.
- Nenhum arquivo real `secrets.toml`, `.env`, chave privada ou token GitHub identificado pelos padrões examinados entre os arquivos versionados. Essa checagem não equivale a auditoria exaustiva de segredos ou segurança.
- No commit inicial `2ea5e09`, o conector GitHub confirmou sucesso de `OpenSpec validation` (run 41004282733) e `Copilot Setup Steps` (run 41004282734). Os resultados do novo workflow devem ser consultados no commit desta revisão; evidência local não é apresentada como execução remota.

## Site publicado

Em 30/10/2026, o About confirmou **2026.10.29.6**. A sessão anônima exibiu apenas login/cadastro e orientações. A aba Criar conta apresentou nome, e-mail, senha e confirmação; envio vazio foi rejeitado antes da criação de conta. A revisão anterior registrou login administrativo positivo, relatório com os dados de demonstração, painel TV e logout.

Não foram criadas credenciais nesta revisão. O formulário administrativo de cadastro de atendentes e a criação positiva de conta/vínculo ainda precisam de verificação com o titular e o administrador. A confirmação da nova versão 2026.10.30.1 no runtime é independente do push no GitHub.

## Pendências mantidas

- Cadastro positivo de cliente e liberação de atendente pelo administrador.
- Testes reais de concorrência de emissão, chamada e cadastro de vínculo; transação e testes de respostas simuladas não demonstram ausência de corrida entre requisições simultâneas.
- Validação em workspace Xano descartável e revisão do cadastro administrativo, conforme checklists ainda abertos.
- Integração da branch na `main` pelo PR; nenhum merge foi realizado nesta revisão.

Os objetivos de notificações externas e satisfação não são tratados como fluxos completos já disponíveis. A implementação atual utiliza Streamlit e consultas REST periódicas, não uma integração publicada com Reflex ou WebSockets.
