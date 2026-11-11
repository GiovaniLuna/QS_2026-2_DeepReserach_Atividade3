# Atividade 3 — Métricas Automáticas versus Avaliação Humana
## Parte E: Comparação, Interpretação e Síntese dos Resultados

**Responsável:** [Nome do Responsável]  
**Projeto:** Alibaba-NLP/DeepResearch  

---

## 1. Tabela Consolidada (Auto vs. Humano)

| Caso | Versão | F1 | Sinal Auto | Notas (C/R/S/FC) | Decisão Humana | Auto x Humano | Justificativa Sintética |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **CT01** | A | 0,40 | Reprova | (2, 2, 1, 0) | **Reprovado** | ✅ Igual | F1 baixo (verbosidade). Humano reprova por suporte (invenção). |
| **CT01** | B | 0,71 | Aprova | (2, 2, 2, 0) | **Aprovado** | ✅ Igual | Resposta exata e concisa. |
| **CT02** | A | 0,11 | Reprova | (1, 1, 2, 0) | **Reprovado** | ✅ Igual | F1 baixo (verbosidade). Humano reprova por fuga ao tema/idioma. |
| **CT02** | B | 0,11 | Reprova | (1, 2, 2, 0) | **Reprovado** | ✅ Igual | F1 baixo (verbosidade). Humano reprova por erro de idioma. |
| **CT03** | A | 0,66 | Aprova | (2, 2, 2, 0) | **Aprovado** | ✅ Igual | Acerto exato (Licença Apache). |
| **CT03** | B | 0,66 | Aprova | (2, 2, 2, 0) | **Aprovado** | ✅ Igual | Acerto exato (Licença Apache). |
| **CT04** | A | 0,57 | Aprova | (2, 2, 2, 0) | **Aprovado** | ✅ Igual | Acerto exato (Jina API). |
| **CT04** | B | 0,54 | Aprova | (2, 2, 2, 0) | **Aprovado** | ✅ Igual | Acerto exato (Jina API). |
| **CT05** | A | 0,23 | Reprova | (2, 2, 2, 0) | **Aprovado** | ❌ Diverge | F1 reprova verbosidade. Humano aprova abstenção correta. |
| **CT05** | B | 0,25 | Reprova | (2, 2, 2, 0) | **Aprovado** | ❌ Diverge | F1 reprova verbosidade. Humano aprova abstenção explícita. |
| **CT06** | A | 0,82 | Aprova | (2, 2, 2, 0) | **Aprovado** | ✅ Igual | Tradução exata de CT01. |
| **CT06** | B | 0,76 | Aprova | (2, 2, 2, 0) | **Aprovado** | ✅ Igual | Tradução exata de CT01. |

---

## 2. Métricas Agregadas e Concordâncias

*   **F1 Lexical Médio (denominador 6):** Versão A = 0,4690 | Versão B = **0,5122**
*   **Aprovação Humana Final (denominador 6):** Versão A = 4/6 (66,7%) | Versão B = **5/6 (83,3%)**
*   **Concordância Automático–Humano:** **10/12 (83,3%)**
*   **Concordância R1–R2 (apenas nos 4 casos revisados, pré-consenso):** **2/4 (50,0%)**

---

## 3. Análise de Divergência Automática–Humana

As únicas divergências ocorreram nos casos **CT05_A e CT05_B**. 

*   **A falha da máquina:** A métrica F1 Lexical reprovou ambas as saídas ($F1 \approx 0.25$) porque os modelos geraram respostas longas para explicar o contexto antes de se absterem. Como o gabarito era curto (15 palavras), a *Precisão* despencou, punindo a verbosidade.
*   **A visão humana:** Os avaliadores aprovaram com nota máxima, pois o modelo não inventou dados e cumpriu a diretriz de abstenção por falta de evidência (a Versão B inclusive usou a frase exata exigida). 
*   **Conclusão:** A divergência confirma que paráfrases ou justificativas longas derrubam o F1, evidenciando a limitação da métrica automática.

---

## 4. Visualização de Decisão (12 Casos)

```text
[ APROVADO POR AMBOS ] ████████████████████ 6 casos (50%)
[ REPROVADO POR AMBOS] ██████████           3 casos (25%)
[ DIVERGÊNCIA: Auto Reprova / Humano Aprova ] ██████ 2 casos (17%) - Efeito Verbosidade (CT05)
[ DIVERGÊNCIA: Auto Aprova / Humano Reprova ] 0 casos (0%)
```

---

## 5. Conclusão Final (Decisão GQM)

1.  **Sucesso do Fator Experimental:** A introdução do *guardrail* (Versão B) aumentou a aprovação humana de 66,7% para 83,3% e forçou a abstenção exata exigida no caso sem evidência.
2.  **Limitação da Métrica:** O F1 Lexical mostrou-se insuficiente para julgar a qualidade factual, punindo respostas corretas apenas por serem extensas.

**Veredito:** O prompt otimizado (**Versão B**) atendeu melhor aos requisitos de segurança e precisão documental, justificando sua adoção definitiva em relação ao baseline.
