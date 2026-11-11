# QUALIDADE DE SOFTWARE - ATIVIDADE 3 (ESCOPO REDUZIDO)
## Relatório Técnico Consolidado: Parte A (GQM)

**Projeto Analisado:** Alibaba-NLP/Deep Research  
**Modelo / Provedor:** `minimax/minimax-m3.1-flash:free` (via OpenRouter Chat API)  

---

## 1. Parte A: Plano GQM (Goal-Question-Metric)

### 1.1 Objetivo GQM (Goal)
Melhorar a fidelidade factual e a segurança de respostas fundamentadas em fontes no fluxo de busca do DeepResearch ao introduzir um *guardrail* explícito de abstenção e tratamento de conflitos no prompt do sistema.

### 1.2 Perguntas Norteadoras (Questions)
* **Q1 (Avaliação Humana):** A Versão B (com prompt otimizado contendo o guardrail de abstenção) atende melhor à tarefa de pesquisa documental em cenários complexos (como ausência de evidência ou casos funcionais) do que o baseline (Versão A)?
* **Q2 (Sinal Automático):** Até que ponto a métrica automática de $F1\text{ lexical}$ concorda com a decisão humana final de aprovação nas 12 saídas experimentais?

### 1.3 Medidas e Métricas (Metrics)
| Medida | Unidade | Fórmula / Denominador | Limitação Declarada |
| :--- | :--- | :--- | :--- |
| **1. F1 Lexical Automático** | Proporcional $[0, 1]$ | $P = \frac{\text{tokens comuns}}{\text{tokens resposta}}$, $R = \frac{\text{tokens comuns}}{\text{tokens referência}}$, $F_1 = \frac{2 \cdot P \cdot R}{P + R}$ (Denominador: 12 saídas) | Uma paráfrase correta ou variação de vocabulário pode resultar em $F1$ baixo, penalizando falsamente saídas corretas. |
| **2. Taxa de Aprovação Humana** | Proporcional $[0, 1]$ | $\frac{\text{Saídas com notas } 2 \text{ em Correção, Relevância e Suporte e sem falha crítica}}{\text{Total de saídas evaluadas (6 por versão / 12 total)}}$ | Sujeita à subjetividade humana na aplicação da rubrica e possíveis vieses dos avaliadores ($R1$ e $R2$). |
| **3. Concordância Auto-Humano** | Razão de concordância | $\frac{\text{Número de decisões coincidentes (Sinal Automático } F_1 \ge \tau \text{ = Decisão Humana Final)}}{\text{Total de saídas (Denominador: 12)}}$ | O limiar fixo $\tau = 0.5$ é uma simplificação didática e pode não capturar nuances semânticas sutis. |

### 1.4 Critérios Prévios e Limiar
* **Limiar do Sinal Automático ($\tau$):** Fixado aprioristicamente em $\tau = 0.5$. O sinal automático aprova a resposta se $F_1 \ge 0.5$.
* **Condição de Bloqueio:** Incidência de falha crítica (nota 0 ou 1 grave, como alucinação de dados sensíveis ou confabulação no caso de abstenção) resulta no bloqueio automático da adoção da Versão B.

---
