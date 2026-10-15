# ADR 0002 — Fonte de verdade e governança do projeto VYRA

**Status:** Proposed  
**Date:** 2026-10-15  
**Scope:** VYRA / ArqTech Labs  
**Related ADR:** [ADR 0001 — Initial Architecture](0001-initial-architecture.md)

> Esta ADR registra uma proposta de governança. Ela não representa aceitação automática nem autorização para treinar modelos, alterar datasets ou executar etapas de processamento.

## 1. Contexto

O projeto VYRA possui artefatos, planos e componentes desenvolvidos em momentos diferentes. Antes de avançar para novos treinos ou ampliar os datasets, é necessário consolidar o estado conhecido, preservar o histórico e distinguir fatos verificados de informações declaradas.

Este documento complementa a ADR 0001 existente. Não a substitui e não altera os gates já estabelecidos no repositório.

## 2. Princípios de evidência

Toda afirmação relevante sobre o estado do projeto deve ser identificada como uma das seguintes:

- **Declarado:** informação relatada em documentação, conversa, plano ou configuração, ainda sem confirmação independente no ambiente atual.
- **Verificado:** informação sustentada por evidência identificável, como arquivo lido, comando executado, teste, hash, inventário ou resultado de auditoria.
- **Pendente:** informação necessária que ainda não foi obtida ou validada.

Um plano não prova execução; a presença de um arquivo não prova sua validade; e uma métrica isolada não comprova reprodutibilidade.

## 3. Decisões propostas

### D1 — Roadmap mestre

Manter um único **VYRA Master Roadmap** como índice central de fases, dependências, gates, decisões e estado atual. Consolidar os planos anteriores sem apagar seu histórico: documentos anteriores devem ser preservados e referenciados quando forem relevantes.

O roadmap deve distinguir claramente:
- estado atual verificado;
- estado declarado;
- decisões aceitas e propostas;
- bloqueios e dependências;
- próximos passos autorizados;
- critérios objetivos de conclusão.

### D2 — Separação entre VYRA e MPE

O MPE permanece um repositório/componente separado. A integração deve ocorrer por contratos e interfaces documentadas, sem duplicar silenciosamente responsabilidades ou fundir repositórios apenas por conveniência.

As fronteiras entre componentes devem definir entradas, saídas, versões, proveniência, tratamento de erros e compatibilidade.

### D3 — Bloqueio de treino até a qualificação

**Nenhum novo treino deve começar** até que os dados, divisões, pesos, configuração e critérios de avaliação relevantes tenham sido inspecionados e aprovados.

Uma baseline oficial de YOLO11 só poderá ser executada após:
1. inventário dos datasets e das suas origens;
2. validação da estrutura e da correspondência entre imagens e anotações;
3. verificação das classes e da ontologia;
4. revisão de duplicatas e risco de vazamento entre divisões;
5. confirmação dos conjuntos de treino, validação e teste;
6. identificação e integridade dos pesos iniciais;
7. congelamento da configuração e das sementes aplicáveis;
8. definição de métricas e critérios de aceitação;
9. registro de hashes, versões e proveniência.

A existência de YOLO11 no ambiente ou de caixas de detecção funcionando não constitui, por si só, autorização para treinar.

### D4 — Fase 1: Data Engine mínimo

Após a conclusão da Fase 0, a primeira implementação deve ser pequena, testável e orientada por contratos. O escopo proposto inclui:
- contratos e esquemas versionados;
- testes automatizados dos contratos;
- catálogo dos dados e artefatos já existentes;
- ontologia inicial de classes, explicitamente versionada;
- documentação de proveniência;
- adaptador que reproduza os principais números da auditoria VYRA-01.

A implementação deve preservar os artefatos e gates existentes. Não deve introduzir pipelines pesados ou dependências de treino antes de sua necessidade estar demonstrada.

### D5 — Frames-chave como referências candidatas

Frames-chave podem ser tratados como **candidatos** a referências confiáveis, mas não devem ser considerados ground truth automaticamente. Antes de servirem como referência de avaliação, devem ter anotação, origem, contexto, licença e proveniência validados.

### D6 — Tratamento de quase duplicatas

O relatório de auditoria indicou **384 pares de quase duplicatas** como item a investigar [declarado até validação do relatório original].

Cada par deve ser analisado e receber uma decisão documentada, por exemplo: manter, remover de uma divisão específica, agrupar ou marcar para revisão. Não remover automaticamente arquivos com base apenas na semelhança visual.

Nenhum arquivo de validação ou teste deve ser apagado ou movido automaticamente. Qualquer alteração de partição precisa considerar a origem dos dados e o risco de vazamento entre conjuntos.

### D7 — Separação entre observação, estimativa e medição

Os resultados devem distinguir explicitamente:
- **Observado:** diretamente visível ou extraído da fonte;
- **Estimado:** inferido por um modelo ou heurística, com incerteza adequada;
- **Medido:** obtido de sensor ou fonte de medição identificável.

Condições como umidade, temperatura e vento não devem ser apresentadas como medições obtidas apenas de uma imagem. Esses valores exigem sensores ou fontes externas apropriadas; a imagem pode, no máximo, sustentar inferências visuais limitadas, claramente rotuladas como estimativas.

## 4. Plano de fases proposto

### Fase 0 — Auditoria confiável

Objetivo: estabelecer uma linha de base factual sem modificar os dados, os pesos ou o código auditado.

Entregáveis previstos:
- `INITIAL_AUDIT.md`
- `REPOSITORY_INVENTORY.md`
- `DATA_INVENTORY.md`
- `CAPABILITY_MATRIX.md`
- `audit_coverage.json`

Critérios:
- escopo e raízes examinadas documentados;
- cobertura e limitações explicitadas;
- erros e caminhos não examinados reportados;
- estado Git registrado quando disponível;
- nenhum treino ou alteração nos conjuntos de dados;
- diretório de saída claramente separado das raízes auditadas.

A auditoria V2 pode ser usada como auditoria preliminar. Seus relatórios não devem ser interpretados como aprovação definitiva se houver cobertura parcial ou limitações conhecidas. A auditoria é somente de leitura em relação às fontes; ela ainda pode montar o Drive e escrever relatórios no diretório de saída.

### Fase 1 — Data Engine mínimo

Implementar contratos, esquemas, testes, catálogo das fontes existentes, ontologia inicial e adaptador para reproduzir os números da auditoria de referência. Exigir testes e revisão antes de avançar.

### Fase 2 — Qualificação de datasets

Validar proveniência, licenças, estrutura, rótulos, frames-chave e divisões. Investigar os pares de quase duplicatas individualmente. Cada dataset e tarefa deve receber um estado explícito: `PASS`, `REVIEW` ou `FAIL`, acompanhado das evidências e justificativas.

### Fase 3 — Baseline YOLO11

Somente depois dos gates anteriores, executar uma baseline controlada com configuração congelada, sementes registradas, manifesto de hashes e checkpoints reproduzíveis. Registrar métricas globais e por classe, incluindo classes ausentes na validação ou no teste. Não sobrescrever pesos ou checkpoints previamente aprovados.

### Fase 4+ — Expansões por tarefa

Cada expansão deve ter fonte de dados adequada, contrato, proveniência, métrica, baseline e critérios de aceitação próprios. Não presumir que uma única mistura de datasets valida todas as tarefas ou modalidades.

## 5. Preservação e persistência

- GitHub é a fonte de verdade lógica para código, documentação, contratos, configurações, manifestos, auditorias e decisões versionadas.
- Google Drive ou armazenamento de objetos pode guardar datasets grandes, rasters, pesos e outros artefatos volumosos.
- Os artefatos externos devem ser referenciados por identificadores estáveis e hashes quando aplicável.
- Não apagar ou reorganizar dados, pesos, checkpoints ou documentação histórica durante a auditoria.
- Alterações futuras devem ser pequenas, rastreáveis e acompanhadas de testes e evidências.

## 6. Critérios de saída da Fase 0

A Fase 0 só pode ser considerada concluída quando:
1. os relatórios forem gerados e revisados;
2. a cobertura for suficiente para as decisões pretendidas, ou as lacunas forem aceitas explicitamente;
3. o estado dos repositórios e os artefatos relevantes estiverem documentados;
4. declarações críticas forem separadas de fatos verificados;
5. não houver alterações inadvertidas nas fontes auditadas;
6. os bloqueios e as decisões pendentes estiverem registrados.

Gerar relatórios, por si só, não significa que a Fase 0 passou.

## 7. Decisões em aberto

- **Estrutura de implementação:** decidir, com base na auditoria, se a próxima etapa deve usar um repositório novo ou uma branch do repositório existente. Não criar uma arquitetura paralela antes dessa decisão.
- **Uso de datasets:** definir os critérios para uso comercial versus pesquisa e registrar as licenças e restrições de cada fonte antes da adoção.
- **Aceitação desta ADR:** manter o status como `Proposed` até que a decisão seja explicitamente confirmada.

## 8. Consequências esperadas

Se aceita, esta ADR reduz a ambiguidade sobre o estado real do projeto, protege artefatos já existentes e impede que o avanço para treinamento seja baseado apenas em declarações, demos visuais ou inventários incompletos.

Até a aceitação explícita, este documento é uma proposta de governança e não altera automaticamente o fluxo operacional.
