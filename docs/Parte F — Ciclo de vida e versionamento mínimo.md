# Atividade 3 — Métricas Automáticas versus Avaliação Humana (GQM)
## Parte F: Ciclo de Vida, Versionamento e Conclusão Experimental  

---

## 1. Ciclo de Vida, Rastreabilidade e Fluxo de Execução

Para garantir a validade científica do experimento e a auditoria das métricas, o processo de controle de qualidade do *DeepResearch* seguiu um ciclo de vida estrito, linear e rastreável. Como a ferramenta principal de versionamento adotada foi o Git (via GitHub), não houve necessidade de implantação de pipelines complexos de MLOps; a rastreabilidade foi garantida pelo isolamento de artefatos em *commits* e diretórios específicos.

A regra fundamental de **não-sobrescrita** foi rigorosamente aplicada: nenhuma nota consolidada substituiu a saída bruta original gerada pela IA, e nenhum consenso sobrescreveu as avaliações humanas individuais. 

O experimento obedeceu ao seguinte fluxo metodológico:

*   **1. Objetivo:** Melhorar a fidelidade factual e a segurança das respostas fundamentadas em fontes no fluxo de busca do *DeepResearch*, introduzindo um *guardrail* explícito de abstenção e tratamento de conflitos no *prompt* do sistema.
*   **2. Versão A (Baseline):** Estabelecimento do grupo de controle. O *prompt* original do sistema foi congelado e preservado no repositório. Essa etapa foi essencial para permitir a comprovação matemática e comparativa de qualquer melhoria na qualidade do software.
*   **3. Mudança B (Guardrail):** Isolamento de uma única variável. Criou-se uma nova versão do sistema contendo a injeção do *guardrail* ativado diretamente no *System Prompt* (a instrução restritiva obrigando a declaração de "evidência insuficiente" em caso de ausência de dados explícitos).
*   **4. Execução:** Rodada de testes na infraestrutura de inferência. Os 6 casos de teste (CT01 a CT06) foram submetidos às Versões A e B sob condições idênticas de temperatura (0.0) na API, gerando 12 artefatos de saída em formato JSON (as respostas brutas do modelo).
*   **5. Avaliação:** Medição comparativa baseada na metodologia GQM. As 12 saídas passaram pelo script de avaliação automática (F1 Lexical) e, posteriormente, foram submetidas à auditoria humana de duplo cego (avaliadores R1 e R2), julgando os critérios de Correção, Relevância, Suporte e Falhas Críticas.
*   **6. Decisão e Acompanhamento:** Veredito baseado em dados. Constatou-se a aprovação da Versão B em virtude do aumento da segurança factual e mitigação de alucinações. O acompanhamento contínuo é garantido pelo versionamento em repositório: caso ocorra regressão funcional, a equipe tem o caminho rastreável para efetuar um *rollback* imediato para o código da Versão A.

### 1.1. O Mecanismo de Segurança (Ativação do Guardrail)

Durante o fluxo, a ativação do *guardrail* não ocorreu via parâmetros de código rígido, mas por meio da Engenharia de Prompts na Versão B. A restrição foi declarada de forma clara e imperativa nas instruções de base. 

Ao utilizar o mecanismo de atenção (*attention mechanism*) intrínseco aos Grandes Modelos de Linguagem (LLMs), a IA calcula o peso semântico das instruções. Quando a Versão B impôs que o modelo estava "terminantemente proibido de deduzir" e deveria "abster-se obrigatoriamente", o modelo compreendeu a alta penalização de desobedecer à trava. Isso ficou provado no **CT05**, onde a IA ativou o protocolo de segurança perfeitamente, recusando-se a inventar dados e admitindo a limitação da documentação fonte, neutralizando o risco de confabulação.

**Cadeia de Rastreabilidade (Exemplo - Caso CT05_B):**
1. **Caso / Fonte:** `docs/Parte B — Seis casos, duas versões e 12 saídas.md` (CT05 - SWE-bench Lite)
2. **Saída Original (Imutável):** `evidencias/saidas_brutas/CT05_B.json`
3. **Nota Automática:** F1 = 0,2571
4. **Avaliação Humana (R1/R2):** Nota (2, 2, 2, 0) em `tabela_avaliacao_humana.csv`
5. **Decisão Final:** Aprovado ➔ Adoção da Versão B.

---

## 2. Manifestos de Versão

A gestão das versões foi registrada de forma estática para garantir auditoria, preservando a Versão A e a Versão B em pastas identificáveis no repositório.

### Manifesto: Versão A (Baseline)
- **Código / Commit:** `versoes/versao_A/` (Commit inicial do experimento)
- **Prompt:** Instrução de sistema padrão do agente React.
- **Modelo e Parâmetros:** `minimax/minimax-m3.1-flash:free` (OpenRouter) | Temp: 0.0 | Max Tokens: 1000.
- **Fonte / Contexto:** Repositório oficial Alibaba-NLP/DeepResearch.
- **Casos e Referências:** CT01 a CT06 documentados na Parte B.
- **Rubrica e Limiar:** F1 Lexical ($\tau = 0.5$); Avaliação Humana (Correção 2, Relevância 2, Suporte 2, Falha Crítica 0).
- **Resultados:** F1 Médio 0,4690 | Aprovação Humana 66,7%.

### Manifesto: Versão B (Guardrail Otimizado)
- **Código / Commit:** `versoes/versao_B/`
- **Mudança Principal (Prompt):** Injeção do guardrail: *"Caso o contexto não contenha evidências [...] declare 'Evidência insuficiente' e abstenha-se..."*
- **Modelo e Parâmetros:** Idênticos à Versão A.
- **Fonte, Casos e Rubrica:** Idênticos à Versão A.
- **Resultados:** F1 Médio 0,5122 | Aprovação Humana 83,3%.

---

## 3. Decisão Experimental e Questões de Análise

Conforme definido aprioristicamente na Parte D, o critério de avanço exigia nota máxima nas dimensões humanas e nenhuma falha crítica (alucinação perigosa). Com base nos resultados, a equipe decidiu **levar a Versão B à próxima etapa**. Reconhece-se, contudo, que uma amostragem de 6 casos em um *framework* experimental não demonstra risco zero para implantação em produção plena.

**Respostas de Análise Crítica:**

**A) A mudança B melhorou a qualidade humana ou apenas a métrica automática?**
A mudança B melhorou substancialmente a **qualidade humana e a segurança factual** (elevando a aprovação de 66,7% para 83,3%). A métrica automática (F1) subiu levemente, mas foi incapaz de captar o real ganho de confiabilidade gerado pela abstenção correta.

**B) Qual saída mostra melhor o limite do F1 e qual evidência sustenta a avaliação?**
A saída **CT05 (Versões A e B)** expõe perfeitamente o limite do F1. A métrica automática reprovou ambas as respostas (F1 ~0,25) porque os textos eram longos (verbosidade). A evidência que sustenta a avaliação é a análise humana, que comprovou que o modelo se absteve corretamente, não alucinou dados e, no caso B, cravou a frase exigida ("evidência insuficiente"). O F1 puniu uma explicação correta apenas pelo seu tamanho.

**C) É possível reconstruir uma saída usando o manifesto? Qual parte não foi congelável?**
Sim, o manifesto permite a reconstrução teórica do experimento cruzando os prompts preservados nas pastas com a temperatura 0.0. A limitação (**parte não congelável**) reside no modelo fornecido via OpenRouter API (`minimax-m3.1-flash:free`). Não possuímos o *hash* dos pesos internos do modelo, o que significa que o provedor pode realizar atualizações silenciosas (patches de alinhamento) na nuvem, impedindo um congelamento absoluto da revisão de infraestrutura.

**D) Que sinal acompanhar depois e como voltar a A se surgir um problema?**
Na próxima etapa, deve-se monitorar a **taxa de falsos negativos humanos** (casos em que o modelo tem a informação no contexto, mas se recusa a responder por excesso de cautela do guardrail). Caso a Versão B cause regressão funcional sistêmica, o *rollback* para a Versão A é trivial: basta reverter o commit do repositório que aponta para o prompt da `versao_A` e reativar o baseline, visto que ambas as parametrizações estão isoladas em pastas distintas.
