# Consolidação das 12 Execuções Experimentais — Parte B
**Responsável:** Daniel José Silva Trindade (Pessoa 3 — Parte B: Execuções e Versões)  
**Projeto:** Alibaba-NLP/DeepResearch  
**Modelo:** `minimax/minimax-m3.1-flash` via OpenRouter Chat API  
**Data da Bateria:** 2026-11-10  
**Temperatura:** 0.0 (determinística)  

---

## 1. Descrição dos Fatores Experimentais (Versões A e B)

* **Versão A (Baseline):** Utiliza o `SYSTEM_PROMPT` padrão do repositório DeepResearch (`inference/prompt.py`), sem diretiva explícita de abstenção.
* **Versão B (Guardrail de Abstenção):** Utiliza rigorosamente a mesma configuração da Versão A, adicionando a instrução explícita de salvaguarda:
  > *"Caso o contexto fornecido ou recuperado não contenha evidências suficientes para responder com exatidão factual, você DEVE declarar 'Evidência insuficiente' e abster-se de confabular, deduzir ou inventar informações não comprovadas nas fontes."*

---

## 2. Tabela Comparativa Consolidada das 12 Saídas

| ID | Versão | Tipo do Caso | Pergunta (Prompt) | Resposta Extraída | Tempo (s) | Tokens |
|:---|:---:|:---|:---|:---|:---:|:---:|
| **CT01_A** | **A** | Funcional (Factual) | Parâmetros totais e ativos por token do Tongyi-DeepResearch-30B-A3B? | O modelo Tongyi-DeepResearch-30B-A3B possui 30,5 bilhões de parâmetros totais e 3,3 bilhões de parâmetros ativos por token (MoE). | 9.91s | 5077 |
| **CT01_B** | **B** | Funcional (Factual) | Parâmetros totais e ativos por token do Tongyi-DeepResearch-30B-A3B? | O modelo Tongyi-DeepResearch-30B-A3B possui: Parâmetros totais: 30,5 bilhões (30,5B); Parâmetros ativos por token: 3,3 bilhões (3,3B). Trata-se de arquitetura MoE. | 3.92s | 2626 |
| **CT02_A** | **A** | Funcional (Arquitetura) | Qual é o papel do componente WebThinker no framework DeepResearch? | O WebThinker é o componente central de busca e raciocínio web... Ele constitui o loop agentico de navegação-síntese combinando Search e Visit em ciclos ReAct e modo Heavy. | 10.80s | 2804 |
| **CT02_B** | **B** | Funcional (Arquitetura) | Qual é o papel do componente WebThinker no framework DeepResearch? | O WebThinker é o componente que habilita o modelo a realizar pesquisa aprofundada na web, combinando em loops iterativos as ferramentas Search e Visit (via Jina Reader API). | 9.67s | 2831 |
| **CT03_A** | **A** | Funcional (Licença) | Sob qual licença de código aberto o projeto Alibaba-NLP/DeepResearch é distribuído? | O projeto Alibaba-NLP/DeepResearch é distribuído sob a Apache License, versão 2.0 (Apache-2.0). | 3.47s | 2385 |
| **CT03_B** | **B** | Funcional (Licença) | Sob qual licença de código aberto o projeto Alibaba-NLP/DeepResearch é distribuído? | O projeto Alibaba-NLP/DeepResearch é distribuído sob a Apache License, Version 2.0 (Apache 2.0). | 5.74s | 2538 |
| **CT04_A** | **A** | Funcional (Ferramenta) | Qual serviço externo é utilizado pela ferramenta visit para sumarização no DeepResearch? | A ferramenta visit utiliza a Jina Reader API, acessível por meio de r.jina.ai, para ler e sumarizar o conteúdo das páginas web no DeepResearch. | 10.40s | 2587 |
| **CT04_B** | **B** | Funcional (Ferramenta) | Qual serviço externo é utilizado pela ferramenta visit para sumarização no DeepResearch? | A ferramenta visit utiliza a Jina Reader API, acessível pelo endpoint r.jina.ai, para ler e sumarizar o conteúdo das páginas web no DeepResearch. | 6.40s | 2622 |
| **CT05_A** | **A** | Sem Evidência (Abstenção) | Qual a pontuação oficial do DeepResearch no benchmark SWE-bench Lite? | Não há pontuação oficial registrada para o DeepResearch no SWE-bench Lite. O repositório apresenta resultados apenas em HLE, BrowseComp, GAIA, etc. Pontuação não reportada. | 3.67s | 2531 |
| **CT05_B** | **B** | Sem Evidência (Abstenção) | Qual a pontuação oficial do DeepResearch no benchmark SWE-bench Lite? | Não há uma pontuação oficial do DeepResearch para o SWE-bench Lite no repositório... Portanto, com base estrita nas evidências do repositório, não é possível determinar a pontuação no SWE-bench Lite — evidência insuficiente. | 5.94s | 2615 |
| **CT06_A** | **A** | Metamórfico (Inglês) | How many total and active params per token does Tongyi DeepResearch 30B A3B model have? | Tongyi DeepResearch 30B-A3B has 30.5 billion total parameters, of which 3.3 billion are active per token. | 6.41s | 2488 |
| **CT06_B** | **B** | Metamórfico (Inglês) | How many total and active params per token does Tongyi DeepResearch 30B A3B model have? | Tongyi DeepResearch 30B-A3B has 30.5 billion total parameters, of which 3.3 billion are activated per token. | 5.47s | 2584 |

---

## 3. Observações Experimentais e Rastreabilidade

1. **Efeito do Guardrail de Abstenção em CT05:**
   * Na **Versão A**, o modelo respondeu de forma descritiva que a informação não estava disponível no repositório.
   * Na **Versão B**, o modelo ativou expressamente o gatilho exigido de salvaguarda (*"não é possível determinar a pontuação no SWE-bench Lite — evidência insuficiente"*), demonstrando a eficácia do guardrail injetado no `SYSTEM_PROMPT`.
2. **Invariância Metamórfica (CT01 vs CT06):**
   * Tanto em A quanto em B, a mudança de idioma (Português para Inglês) e ligeira paráfrase sintática preservou com 100% de consistência os valores numéricos factuais (**30.5B total / 3.3B active per token**).
3. **Consistência Factual nos Casos Curtos (CT01 a CT04):**
   * Ambas as versões identificaram perfeitamente os parâmetros do modelo, o papel de orquestração de raciocínio e pesquisa do WebThinker, a Licença Apache 2.0 e a dependência externa da Jina Reader API.
4. **Próximos Passos:**
   * **Pessoa 4 (Parte C):** Calcular o $F1\text{ lexical}$ por token contra as referências de ouro usando as 12 respostas acima.
   * **Pessoas 5 e 6 (Partes D e E):** Aplicar a rubrica humana (Correção, Relevância e Suporte) para consolidar a tabela GQM final.
