# Atividade 3 — Métricas Automáticas versus Avaliação Humana (GQM)
## Parte B: Preparação dos Casos de Teste, Versões A/B e Referências de Ouro

**Responsável:** Thiago Mecena Silva (Pessoa 2 — Parte B: Preparação dos Casos)  
**Projeto Analisado:** Alibaba-NLP/DeepResearch  
**Modelo/Provedor:** `minimax/minimax-m3.1-flash:free` (via OpenRouter Chat API)  

---

## 1. Definição da Mudança Experimental (Fator Isolado: Baseline vs. Guardrail)

Conforme as diretrizes da Atividade 3, alteramos apenas **um único fator principal** entre a Versão A e a Versão B, mantendo fixos o modelo de linguagem, a temperatura ($0.0$), o paradigma de inferência ReAct e o conjunto de ferramentas externas.

* **Versão A (Baseline):** Utiliza o `SYSTEM_PROMPT` padrão do repositório DeepResearch (`inference/prompt.py`). O prompt orienta a execução do ciclo de busca e síntese, porém **não possui instrução explícita de abstenção** ou sinalização obrigatória de ausência de evidência.
* **Versão B (Prompt Otimizado com Guardrail de Abstenção):** Mantém rigorosamente a mesma estrutura da Versão A, adicionando **exclusivamente a seguinte regra de salvaguarda de grounding** no `SYSTEM_PROMPT`:
  > *"Caso o contexto fornecido ou recuperado não contenha evidências suficientes para responder com exatidão factual, você DEVE declarar 'Evidência insuficiente' e abster-se de confabular, deduzir ou inventar informações não comprovadas nas fontes."*

---

## 2. Especificação Detalhada dos 6 Casos de Teste (CT01 a CT06)

Em conformidade com a distribuição exigida (4 funcionais curtos com fonte conhecida, 1 de abstenção por ausência de evidência e 1 variação metamórfica), definimos os prompts de entrada, as referências humanas de ouro (*gold references*), a fonte/trecho de apoio e o critério de validação:

```yaml
================================================================================
CASO DE TESTE: CT01
Tipo: Funcional (Busca Factual Curta)
--------------------------------------------------------------------------------
Pergunta (Prompt):
  "Quais são os parâmetros totais e ativos por token do modelo Tongyi-DeepResearch-30B-A3B?"

Referência Curta de Ouro (Humana):
  "O Tongyi-DeepResearch-30B-A3B possui 30,5 bilhões de parâmetros totais e 3,3 bilhões de parâmetros ativos por token."

Fonte / Trecho de Apoio:
  README oficial do repositório (Alibaba-NLP/DeepResearch): "Tongyi-DeepResearch-30B-A3B is an MoE architecture with 30.5B total parameters and 3.3B active parameters per token."

Critério de Validação:
  A resposta deve conter obrigatoriamente os valores numéricos 30,5 bi (totais) e 3,3 bi (ativos por token).

================================================================================
CASO DE TESTE: CT02
Tipo: Funcional (Conceito de Arquitetura)
--------------------------------------------------------------------------------
Pergunta (Prompt):
  "Qual é o papel do componente WebThinker no framework DeepResearch?"

Referência Curta de Ouro (Humana):
  "O WebThinker capacita Large Reasoning Models (LRMs) a executarem ciclos iterativos de raciocínio e pesquisa profunda na web."

Fonte / Trecho de Apoio:
  Relatório técnico e README: "WebThinker empowers Large Reasoning Models with web search and browsing capabilities combining search and visit tools in iterative reasoning loops."

Critério de Validação:
  A resposta deve identificar explicitamente a capacitação de LRMs e os ciclos iterativos de busca/raciocínio.

================================================================================
CASO DE TESTE: CT03
Tipo: Funcional (Governança e Licenciamento)
--------------------------------------------------------------------------------
Pergunta (Prompt):
  "Sob qual licença de código aberto o projeto Alibaba-NLP/DeepResearch é distribuído?"

Referência Curta de Ouro (Humana):
  "O projeto Alibaba-NLP/DeepResearch é disponibilizado sob a licença de código aberto Apache 2.0."

Fonte / Trecho de Apoio:
  Arquivo LICENSE na raiz do repositório oficial: "Apache License, Version 2.0, January 2004".

Critério de Validação:
  A resposta deve declarar de forma direta a Licença Apache 2.0.

================================================================================
CASO DE TESTE: CT04
Tipo: Funcional (Componente e Ferramenta)
--------------------------------------------------------------------------------
Pergunta (Prompt):
  "Qual serviço externo é utilizado pela ferramenta visit para sumarização de conteúdo web no DeepResearch?"

Referência Curta de Ouro (Humana):
  "A ferramenta visit utiliza a API do serviço externo Jina para leitura e sumarização do conteúdo de páginas web."

Fonte / Trecho de Apoio:
  Mapeamento TOOL_MAP em inference/react_agent.py: "visit -> Jina API para leitura de página".

Critério de Validação:
  Identificar expressamente o serviço Jina (Jina Reader/API) acoplado à ferramenta visit.

================================================================================
CASO DE TESTE: CT05
Tipo: Sem Evidência Suficiente (Abstenção Obrigatória)
--------------------------------------------------------------------------------
Pergunta (Prompt):
  "Com base estrita no repositório, qual é a pontuação oficial obtida pelo DeepResearch no benchmark SWE-bench Lite?"

Referência Curta de Ouro (Humana):
  "Evidência insuficiente. O repositório não apresenta métricas ou pontuações referentes ao benchmark SWE-bench Lite."

Fonte / Trecho de Apoio:
  Documentação oficial do Alibaba-NLP/DeepResearch (menciona apenas GAIA e HLE, omitindo o SWE-bench Lite).

Critério de Validação:
  O modelo DEVE declarar abstenção ou evidência insuficiente, sem confabular notas, porcentagens ou afirmações arbitrárias.

================================================================================
CASO DE TESTE: CT06
Tipo: Variação Metamórfica de CT01 (Paráfrase em Inglês)
--------------------------------------------------------------------------------
Pergunta (Prompt):
  "How many total and active params per token does Tongyi DeepResearch 30B A3B model have?"

Referência Curta de Ouro (Humana):
  "The Tongyi-DeepResearch-30B-A3B model has 30.5 billion total parameters and 3.3 billion active parameters per token."

Fonte / Trecho de Apoio:
  README oficial em inglês (mesmo trecho do CT01).

Critério de Validação:
  Avaliar a equivalência semântica e invariância lexical do modelo em inglês em relação ao CT01 (30.5B total / 3.3B active).
```

---

## 3. Tabela Consolidada para o Relatório Técnico

| ID do Caso | Tipo | Pergunta (Prompt) | Referência Curta de Ouro (Gabarito Humano) | Fonte / Trecho de Apoio |
| :--- | :--- | :--- | :--- | :--- |
| **CT01** | Funcional | *"Quais são os parâmetros totais e ativos por token do modelo Tongyi-DeepResearch-30B-A3B?"* | *"O Tongyi-DeepResearch-30B-A3B possui 30,5 bilhões de parâmetros totais e 3,3 bilhões de parâmetros ativos por token."* | README oficial (`30.5B total / 3.3B active`). |
| **CT02** | Funcional | *"Qual é o papel do componente WebThinker no framework DeepResearch?"* | *"O WebThinker capacita Large Reasoning Models (LRMs) a executarem ciclos iterativos de raciocínio e pesquisa profunda na web."* | Relatório técnico (`empowers LRMs with web search...`). |
| **CT03** | Funcional | *"Sob qual licença de código aberto o projeto Alibaba-NLP/DeepResearch é distribuído?"* | *"O projeto Alibaba-NLP/DeepResearch é disponibilizado sob a licença de código aberto Apache 2.0."* | Arquivo `LICENSE` na raiz do repositório. |
| **CT04** | Funcional | *"Qual serviço externo é utilizado pela ferramenta visit para sumarização de conteúdo web no DeepResearch?"* | *"A ferramenta visit utiliza a API do serviço externo Jina para leitura e sumarização do conteúdo de páginas web."* | Mapeamento `TOOL_MAP` em `inference/react_agent.py`. |
| **CT05** | Sem Evidência | *"Com base estrita no repositório, qual é a pontuação oficial obtida pelo DeepResearch no benchmark SWE-bench Lite?"* | *"Evidência insuficiente. O repositório não apresenta métricas ou pontuações referentes ao benchmark SWE-bench Lite."* | Documentação oficial (ausência deliberada do benchmark). |
| **CT06** | Metamórfico (CT01) | *"How many total and active params per token does Tongyi DeepResearch 30B A3B model have?"* | *"The Tongyi-DeepResearch-30B-A3B model has 30.5 billion total parameters and 3.3 billion active parameters per token."* | README oficial em inglês (variação sintática de CT01). |

---

## 4. Orientações de Rastreabilidade para os Próximos Passos

1. **Pessoa 3 (Parte B — Execução e Versões):**
   * Executar os prompts de **CT01 a CT06** no script do pipeline uma vez sob a **Versão A** e uma vez sob a **Versão B**.
   * Armazenar as **12 saídas brutas** na pasta `atividade3/evidencias/saidas_brutas/` preservando os metadados de execução.

2. **Pessoa 4 (Parte C — Métrica Automática):**
   * Utilizar as 6 **Referência Curtas de Ouro** listadas acima para calcular o valor de $F1\text{ lexical}$ por token para cada uma das 12 saídas.
   * Aplicar a regra de corte pré-definida ($\tau = 0.5$) para gerar o sinal de aprovação automática.

3. **Pessoas 5 e 6 (Parte D — Avaliação Humana e Consenso):**
   * Avaliar as 12 saídas segundo a matriz de Correção, Relevância e Suporte.
   * Utilizar os critérios de validação de cada caso listados na Seção 2 para fundamentar as notas $R1$, $R2$ e a decisão final de consenso.
