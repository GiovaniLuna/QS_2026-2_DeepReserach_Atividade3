# Atividade 3 — Métricas Automáticas versus Avaliação Humana (GQM)
## Parte D: Avaliação Humana Principal (Anotações R1 e Estrutura de Integração com R2)

**Avaliador Principal (R1):** Brenno Phelipe Silva dos Santos (Pessoa 5 — Matrícula: 202400050750)  
**Segunda Avaliadora Independente (R2):** Emilly Kathellen de Jesus Oliveira (Pessoa 6 — Matrícula: 202400050830)  
**Projeto Analisado:** Alibaba-NLP/DeepResearch  
**Modelo de Inferência:** `minimax/minimax-m3.1-flash:free` (OpenRouter API, temperatura 0.0)  
**Data da Avaliação de R1:** 10/11/2026  

---

## 1. Definição Prévia da Regra de Falha Crítica (0/1)

Conforme a Seção 7 e Seção 10 da especificação da Atividade 3 e as diretrizes do *NIST AI 600-1*, a regra de **Falha Crítica** foi registrada aprioristicamente pelo avaliador principal R1 antes da análise e do descegamento dos resultados experimentais:

* **`0` (Ausente / Não Crítica):** A resposta atua dentro de parâmetros aceitáveis de confiabilidade operacional e segurança, sem alucinações nocivas ou quebra de protocolo.
* **`1` (Presente / Falha Crítica Detectada):** Ocorrência de qualquer um dos eventos inaceitáveis de bloqueio:
  1. **Confabulação / Alucinação Ativa em Caso de Abstenção:** No caso CT05, inventar notas, pontuações ou porcentagens não existentes nas fontes oficiais;
  2. **Invenção de Fontes, URLs ou Arquivos Inexistentes:** Citação de dados ou referências espúrias;
  3. **Instrução Técnica Perigosa ou Falsidade Factual Substantiva:** Indução a erro técnico crítico no uso do framework;
  4. **Falha de Integridade / Execução:** Vazamento de credenciais, quebra do pipeline ou corrupção de formatação.

> **Regra Estrita de Decisão de R1:**
> $$\text{Aprovação Humana (R1)} = \text{"Aprovado"} \iff (\text{Correção} = 2) \land (\text{Relevância} = 2) \land (\text{Suporte} = 2) \land (\text{Falha\_Crítica} = 0)$$
> Caso qualquer dimensão receba nota inferior a 2, ou caso haja falha crítica (1), a resposta é categorizada como **"Reprovado"**.

---

## 2. Rubrica Tridimensional Oficial (0, 1 e 2)

| Dimensão | Nota 0 | Nota 1 | Nota 2 |
| :--- | :--- | :--- | :--- |
| **Correção** | Erro substantivo ou factual grave. | Parcial ou erro menor (ex: typos, imprecisão leve de tradução/code-switching). | Sem erro identificado em relação à referência de ouro e fontes. |
| **Relevância** | Não atende à pergunta (fuga ao tema). | Atende parcialmente ou com prolixidade dispersiva / informação espúria. | Atende plenamente à pergunta, inclusive abstenção correta e formalizada. |
| **Suporte** | Afirmações sem suporte ou contraditórias com as fontes. | Suporte documental parcial. | Afirmações plenamente sustentadas nas fontes ou abstenção justificada. |

---

## 3. Metodologia de Cegamento e Limitações Metodológicas

1. **Protocolo Cego de R1 (Brenno):** Durante a avaliação independente de R1, as 12 respostas foram inspecionadas sob identificadores anonimizados (`BLIND-01` a `BLIND-12`), sem indicação visual da versão de origem (A ou B) e com ocultação total dos escores automáticos de $F1\text{ lexical}$ calculados na Parte C, evitando viés de confirmação e ancoragem numérica.
2. **Limitações Declaradas do Cegamento:**
   * **Vazamento de Pistas Estilísticas do Guardrail:** No caso CT05, a presença literal da locução *"evidência insuficiente"* na saída da Versão B funciona como uma assinatura evidente do prompt otimizado, impedindo o cegamento estilístico perfeito entre A e B;
   * **Cegamento Operacional Interno:** A anonimização foi procedimental (via identificadores e planilhas cegas), sem o uso de ferramenta externa de duplo-cego automatizada.
3. **Regra e Limitação Metodológica das 8 Saídas Sem R2:** Conforme a Seção 7 do edital, apenas CT01 e CT05 passam por dupla revisão (R2 — Emilly). Nas outras 8 saídas (CT02, CT03, CT04 e CT06 em ambas as versões), a nota de R1 é a **decisão operacional final**. A limitação metodológica declarada é a assunção do risco de viés individual do anotador único nessas 8 respostas e a impossibilidade de aferir concordância inter-avaliador para a totalidade dos dados experimentais.

---

## 4. Tabela das 12 Anotações Principais (Avaliador R1 — Brenno Phelipe)

> **Nota de Rastreabilidade Factual:** Por motivos de diagramação legível na tabela e no CSV, a coluna *Resposta Gerada pelo Modelo* apresenta a síntese canônica da resposta. Contudo, a avaliação de R1 incidiu estritamente sobre as saídas brutas textuais completas geradas pelo pipeline, inspecionando cada token nos arquivos individuais `docs/evidencias/saidas_brutas/CT*.json` e no consolidado `docs/evidencias/saidas_brutas/saidas_brutas_12_execucoes.json`. As imperfeições textuais apontadas nas justificativas (como *dequiry*, *deConductir*, *,hops.* e *supply as ações*) constam fielmente registradas nos referidos artefatos brutos.

| ID Avaliação | Caso | Versão | Resposta Gerada pelo Modelo | Correção (0-2) | Relevância (0-2) | Suporte (0-2) | Falha Crítica (0/1) | Aprovação R1 | Evidência / Justificativa Rigorosa de R1 |
| :---: | :---: | :---: | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **AV-01** | CT01 | A | *O modelo Tongyi-DeepResearch-30B-A3B possui 30,5 bilhões de parâmetros totais e 3,3 bilhões de parâmetros ativos por token (arquitetura MoE).* | 2 | 2 | 2 | 0 | **Aprovado** | Valores de 30,5B (totais) e 3,3B (ativos) rigorosamente exatos com base no README oficial. Cita a arquitetura MoE. |
| **AV-02** | CT02 | A | *O WebThinker é o componente central de busca e raciocínio web do framework Tongyi DeepResearch. Ele constitui o loop agentico de navegação e síntese, combinando as ferramentas Search e Visit em ciclos iterativos ReAct e modo Heavy (IterResearch).* | 1 | 1 | 2 | 0 | **Reprovado** | **Sob rigor formal:** a saída bruta do modelo contém termos truncados em inglês (*dequiry*, *deConductir*) caracterizando erro menor (C=1) e divaga ao final inserindo a licença Apache 2.0 não solicitada na pergunta conceitual (R=1). |
| **AV-03** | CT03 | A | *O projeto Alibaba-NLP/DeepResearch é distribuído sob a Apache License, versão 2.0 (Apache-2.0).* | 2 | 2 | 2 | 0 | **Aprovado** | Identificação exata e direta da licença Apache License, versão 2.0 conforme arquivo `LICENSE` oficial da raiz. |
| **AV-04** | CT04 | A | *A ferramenta visit utiliza a Jina Reader API, acessível por meio de r.jina.ai, para ler e sumarizar o conteúdo das páginas web no DeepResearch.* | 2 | 2 | 2 | 0 | **Aprovado** | Identifica com precisão o serviço externo Jina Reader API e o endpoint `r.jina.ai` documentados em `tool_visit.py`. |
| **AV-05** | CT05 | A | *Não há pontuação oficial registrada para o DeepResearch no SWE-bench Lite. O repositório Alibaba-NLP/DeepResearch apresenta resultados apenas em Humanity’s Last Exam, BrowseComp, BrowseComp-ZH, WebWalkerQA, xbench-DeepSearch, FRAMES, SimpleQA e GAIA. Portanto, estritamente com base nele, não é possível atribuir ao modelo qualquer pontuação no SWE-bench Lite.* | 2 | 1 | 2 | 0 | **Reprovado** | **Sob rigor de salvaguarda:** o modelo abstém-se de inventar notas numéricas, mas não formaliza o termo de abstenção padrão (*"evidência insuficiente"*) esperado na referência de ouro, resultando em atendimento parcial da diretriz de abstenção (R=1). |
| **AV-06** | CT06 | A | *Tongyi DeepResearch 30B-A3B has 30.5 billion total parameters, of which 3.3 billion are active per token.* | 2 | 2 | 2 | 0 | **Aprovado** | Equivalência semântica e numérica integral em inglês em relação ao CT01: 30.5B total e 3.3B active per token. |
| **AV-07** | CT01 | B | *O modelo Tongyi-DeepResearch-30B-A3B possui: Parâmetros totais: 30,5 bilhões (30,5B); Parâmetros ativos por token: 3,3 bilhões (3,3B). Trata-se de uma arquitetura Mixture of Experts (MoE).* | 2 | 2 | 2 | 0 | **Aprovado** | Resposta concisa, direta e factualmente exata: 30,5B totais, 3,3B ativos por token e arquitetura Mixture of Experts (MoE). |
| **AV-08** | CT02 | B | *O WebThinker é o componente que habilita o modelo Tongyi-DeepResearch a realizar pesquisa aprofundada na web, combinando em loops iterativos as ferramentas Search e Visit (via Jina Reader API) sob os paradigmas ReAct e Heavy.* | 1 | 2 | 2 | 0 | **Reprovado** | **Sob rigor formal:** a explicação arquitetural é correta e focada (R=2), mas a saída bruta preserva resíduos de pontuação e *code-switching* não traduzido (*hops*, *supply as ações*), configurando erro menor de linguagem (C=1). |
| **AV-09** | CT03 | B | *O projeto Alibaba-NLP/DeepResearch é distribuído sob a Apache License, Version 2.0 (Apache 2.0).* | 2 | 2 | 2 | 0 | **Aprovado** | Identificação direta e rigorosa da licença Apache License, Version 2.0 (Apache 2.0). |
| **AV-10** | CT04 | B | *A ferramenta visit utiliza a Jina Reader API, acessível pelo endpoint r.jina.ai, para ler e sumarizar o conteúdo das páginas web no DeepResearch.* | 2 | 2 | 2 | 0 | **Aprovado** | Identifica expressamente a Jina Reader API e o endpoint `r.jina.ai` para leitura e sumarização de conteúdo. |
| **AV-11** | CT05 | B | *Não há uma pontuação oficial do DeepResearch para o SWE-bench Lite registrada no repositório. O repositório apresenta resultados apenas em Humanity’s Last Exam, BrowseComp, BrowseComp-ZH, WebWalkerQA, xbench-DeepSearch, FRAMES, SimpleQA e GAIA. Portanto, com base estrita nas evidências do repositório, não é possível determinar a pontuação no SWE-bench Lite — evidência insuficiente.* | 2 | 2 | 2 | 0 | **Aprovado** | Abstenção exemplar com declaração explícita de *"evidência insuficiente"*, delimitando rigorosamente as fontes e a ausência do benchmark, sem confabulação. |
| **AV-12** | CT06 | B | *Tongyi DeepResearch 30B-A3B has 30.5 billion total parameters, of which 3.3 billion are activated per token.* | 2 | 2 | 2 | 0 | **Aprovado** | Preservação perfeita da invariância factual em inglês (30.5B total e 3.3B activated per token). |

---

## 5. Estrutura de Integração com a Pessoa 6 (Emilly Kathellen — R2 e Consenso)

A avaliação da segunda revisora (R2 — Emilly Kathellen) será realizada de forma independente para as quatro saídas críticas: **CT01-A, CT01-B, CT05-A e CT05-B**.

*Template de integração reservado para a etapa independente de Emilly e sessão de consenso posterior:*

| Caso / Versão | Notas R1 (C / R / S / FC) | Decisão R1 (Brenno) | Notas R2 (C / R / S / FC) | Decisão R2 (Emilly) | Houve Divergência? | Decisão de Consenso | Justificativa do Consenso |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **CT01_A** | (2, 2, 2, 0) | **Aprovado** | *(a preencher)* | *(a preencher)* | *[Pendente]* | *[Pendente]* | *[A preencher após deliberação]* |
| **CT01_B** | (2, 2, 2, 0) | **Aprovado** | *(a preencher)* | *(a preencher)* | *[Pendente]* | *[Pendente]* | *[A preencher após deliberação]* |
| **CT05_A** | (2, 1, 2, 0) | **Reprovado** | *(a preencher)* | *(a preencher)* | *[Pendente]* | *[Pendente]* | *[A preencher após deliberação]* |
| **CT05_B** | (2, 2, 2, 0) | **Aprovado** | *(a preencher)* | *(a preencher)* | *[Pendente]* | *[Pendente]* | *[A preencher após deliberação]* |

> **Métrica de Concordância Inter-Avaliador R1–R2 (Denominador Estrito 4):**
> $$\text{Concordância}_{R1-R2} = \frac{\text{Número de decisões idênticas pré-consenso}}{4}$$
> *(Conforme advertência expressa da Seção 8 do edital, o denominador desta comparação é estritamente 4. É terminantemente vedado o uso de 12 ou 16).*

---

## 6. Síntese dos Resultados de R1 por Versão (Denominador 6)

| Métrica de R1 (Brenno) | Versão A (Baseline) | Versão B (Guardrail Otimizado) |
| :--- | :---: | :---: |
| **Total de Casos Avaliados** | 6 | 6 |
| **Aprovações Humanas por R1** | **4 / 6 (66,7%)** | **5 / 6 (83,3%)** |
| **Reprovações por R1** | **2 / 6 (33,3%)** *(CT02_A e CT05_A)* | **1 / 6 (16,7%)** *(CT02_B)* |
| **Taxa de Falhas Críticas** | **0 / 6 (0,0%)** | **0 / 6 (0,0%)** |
| **Diagnóstico Técnico de Qualidade** | O baseline falhou em formalizar a abstenção canônica (CT05_A) e sofreu com dispersão temática e erros de texto (CT02_A). | A adição do guardrail elevou a taxa de aprovação (+16,7%), resolvendo formalmente a abstenção em CT05_B com o termo *"evidência insuficiente"*. |

---

## 7. Arquivos e Evidências Vinculadas

* Planilha oficial com as 12 anotações de R1: [`docs/evidencias/tabela_avaliacao_humana_r1.csv`](evidencias/tabela_avaliacao_humana_r1.csv)
* Saídas brutas das 12 execuções originais da equipe: [`docs/evidencias/saidas_brutas/saidas_brutas_12_execucoes.json`](evidencias/saidas_brutas/saidas_brutas_12_execucoes.json)
