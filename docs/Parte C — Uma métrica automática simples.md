# Atividade 3 — Métricas Automáticas versus Avaliação Humana (GQM)
## Parte C: Métrica Automática Simples (F1 Lexical por Tokens)

**Responsável:** Filipe de Carvalho Godoy (Pessoa 4 — Parte C)
**Projeto Analisado:** Alibaba-NLP/DeepResearch
**Modelo/Provedor:** `minimax/minimax-m3.1-flash` (via OpenRouter Chat API), temperatura 0.0

> Normalização, tokenização, tratamento de casos de borda e o limiar **τ** foram fixados e versionados em [`atividade3/metrica/configuracao-metrica.json`](../atividade3/metrica/configuracao-metrica.json) **em 10/11/2026, antes da execução da bateria**. O enunciado proíbe ajustar o limiar após observar os resultados; o registro datado é a evidência de que isso não ocorreu.

---

## 1. Definição da Métrica

F1 lexical por tokens entre o texto gerado e a referência curta de ouro definida na Parte B.

```
P_tokens   = tokens_em_comum / tokens_da_resposta
R_tokens   = tokens_em_comum / tokens_da_referencia
F1_lexical = 2 * P_tokens * R_tokens / (P_tokens + R_tokens)
```

| Propriedade | Valor |
|---|---|
| Unidade | Adimensional, no intervalo [0, 1] |
| Denominador | 1 valor por saída — **6 por versão**, 12 no total |
| Regra do sinal | Automático **aprova** se `F1_lexical ≥ τ` |
| **Limiar τ** | **0,5** |

### 1.1 Justificativa do limiar τ = 0,5

Valor didático indicado no enunciado. A equipe não dispõe de conjunto de calibração próprio que sustente outro número: escolher um valor diferente sem dado que o justifique seria arbitrário, e ajustá-lo após observar os resultados violaria a regra de pré-registro — que é precisamente o objeto de avaliação desta atividade.

---

## 2. Normalização e Tokenização

Ordem fixa: **NFC → casefold → tokenização**.

| Etapa | Decisão adotada |
|---|---|
| Normalização Unicode | NFC |
| Caixa | `casefold()` |
| Token | `\w+` com flag UNICODE |
| Dígitos | Contam como token |
| Acentos | **Preservados** (`casefold` não remove acento) |
| Interseção | **Multiconjuntos** — a repetição é contabilizada |

**Dígitos como token.** Permite distinguir `10/11` de `11/11` — exemplo de limitação citado no próprio enunciado. Determinante nesta bateria: CT01 e CT06 dependem dos valores 30,5 e 3,3.

**Interseção de multiconjuntos.** Em `"11 11"` contra `"10 11"` a interseção vale 1, não 2: cada ocorrência da referência só pode ser casada uma vez. Conjuntos simples inflariam o escore de respostas repetitivas.

**Marcação Markdown.** As saídas do modelo contêm `**negrito**` e listas. Os asteriscos e hifens não são caracteres de palavra e, portanto, não geram token — nenhum pré-processamento adicional foi necessário.

---

## 3. Casos de Borda

| Situação | Tratamento |
|---|---|
| Resposta vazia | F1 = 0 |
| Resposta apenas com pontuação | F1 = 0 (não gera token) |
| Nenhuma sobreposição | F1 = 0 |
| **Referência sem tokens** | **Não pontuar** — sinal `indefinido`; caso precisa ser corrigido |

Nenhum desses casos ocorreu na bateria: as 12 saídas e as 6 referências têm tokens válidos.

---

## 4. Verificação do Script

Dez pares com valor esperado calculado manualmente, em [`exemplos/casos-de-verificacao.json`](../atividade3/metrica/exemplos/casos-de-verificacao.json). Todos passam.

| Verificação | F1 esperado | O que demonstra |
|---|---|---|
| Textos idênticos | 1,0000 | Caso trivial |
| Sem sobreposição | 0,0000 | Regra de borda |
| Sobreposição parcial | 0,8571 | Aritmética: P = 3/4, R = 3/3 |
| Resposta vazia | 0,0000 | Regra de borda |
| Resposta só com pontuação | 0,0000 | Tokenização |
| Referência sem tokens | — | Não inventa escore |
| Caixa e acento | 1,0000 | `casefold` operante |
| Acento decomposto (NFD) | 1,0000 | **Normalização NFC é necessária** — sem ela, resultado 0 |
| Repetição `11 11` vs `10 11` | 0,5000 | Interseção de multiconjuntos |
| Paráfrase correta | 0,1818 | **Limitação central da métrica** |

```bash
cd atividade3/metrica
python3 f1_lexical.py --autoteste
```

---

## 5. Resultados

Campo utilizado como resposta: `resposta_extraida` dos arquivos em `docs/evidencias/saidas_brutas/`. O campo `saida_bruta_final` foi descartado para o cálculo porque inclui as marcações `<answer>`, que gerariam o token espúrio `answer` em todas as saídas.

| Caso | Versão | Tokens resp. | Tokens ref. | P | R | F1 | Sinal (τ = 0,5) |
|---|---|---|---|---|---|---|---|
| CT01 | A | 74 | 21 | 0,257 | 0,905 | **0,4000** | reprova |
| CT01 | B | 32 | 21 | 0,594 | 0,905 | **0,7170** | aprova |
| CT02 | A | 163 | 18 | 0,061 | 0,556 | **0,1105** | reprova |
| CT02 | B | 152 | 18 | 0,066 | 0,556 | **0,1176** | reprova |
| CT03 | A | 17 | 16 | 0,647 | 0,688 | **0,6667** | aprova |
| CT03 | B | 17 | 16 | 0,647 | 0,688 | **0,6667** | aprova |
| CT04 | A | 26 | 19 | 0,500 | 0,684 | **0,5778** | aprova |
| CT04 | B | 25 | 19 | 0,480 | 0,632 | **0,5455** | aprova |
| CT05 | A | 52 | 15 | 0,154 | 0,533 | **0,2388** | reprova |
| CT05 | B | 55 | 15 | 0,164 | 0,600 | **0,2571** | reprova |
| CT06 | A | 19 | 20 | 0,842 | 0,800 | **0,8205** | aprova |
| CT06 | B | 19 | 20 | 0,789 | 0,750 | **0,7692** | aprova |

### 5.1 Agregado por versão (denominador 6)

| Versão | F1 médio | Aprovação automática |
|---|---|---|
| A (baseline) | **0,4690** | **3/6** |
| B (guardrail de abstenção) | **0,5122** | **4/6** |

A diferença de F1 médio entre as versões é de **+0,0432**, concentrada quase inteiramente em um único caso.

### 5.2 Variação por caso

| Caso | A | B | Δ |
|---|---|---|---|
| CT01 | 0,4000 | 0,7170 | **+0,3170** |
| CT02 | 0,1105 | 0,1176 | +0,0071 |
| CT03 | 0,6667 | 0,6667 | 0,0000 |
| CT04 | 0,5778 | 0,5455 | −0,0323 |
| CT05 | 0,2388 | 0,2571 | +0,0183 |
| CT06 | 0,8205 | 0,7692 | −0,0513 |

Dos seis casos, o ganho vem de **CT01 isoladamente** (+0,3170). Em dois casos a Versão B pontua pior, e em um empata. Como a precisão de CT01 sobe de 0,257 para 0,594 enquanto a revocação permanece em 0,905, o ganho decorre de a Versão B ter respondido de forma mais curta — 32 tokens contra 74 — e não de ter acertado algo que a Versão A errou: ambas contêm os valores corretos.

Isso significa que a mudança de F1 médio entre as versões é, em boa medida, mudança de verbosidade. Avaliar se houve ganho de qualidade é atribuição da Parte D, e a comparação entre os dois sinais é objeto da Parte E.

---

## 6. Limitação Declarada e sua Confirmação Empírica

O F1 lexical mede **sobreposição de vocabulário, não adequação factual**.

### 6.1 Previsão registrada antes da bateria

Antes de qualquer execução, aplicando o script à referência de ouro do CT05, registrou-se a seguinte previsão:

| Resposta hipotética no CT05 | P | R | F1 | Sinal |
|---|---|---|---|---|
| `"Evidência insuficiente."` — correta e concisa | 1,000 | 0,133 | 0,2353 | reprova |
| Abstenção que repete o vocabulário da referência | 1,000 | 1,000 | 1,0000 | aprova |
| Confabulação plausível (`"obteve 42,8% no SWE-bench Lite"`) | 0,368 | 0,467 | 0,4118 | reprova |

E a conclusão registrada: *"Se a Versão B produzir abstenções curtas no CT05, deve-se esperar divergência automático–humano nesse caso."*

### 6.2 O que de fato ocorreu

Ambas as versões abstiveram-se corretamente no CT05, e a Versão B empregou textualmente a expressão exigida:

> **CT05_B:** *"Não há uma pontuação oficial do DeepResearch para o SWE-bench Lite registrada no repositório. […] com base estrita nas evidências do repositório, não é possível determinar a pontuação no SWE-bench Lite — evidência insuficiente."*

Ambas foram **reprovadas** pelo sinal automático: F1 = 0,2388 e 0,2571, bem abaixo de τ = 0,5. A revocação é razoável (0,533 e 0,600), mas a precisão desaba (0,154 e 0,164) porque as respostas enumeram os benchmarks efetivamente presentes no repositório — informação correta e pertinente, ausente da referência curta.

A previsão registrada em 6.1 confirmou-se. A métrica reprovou as duas únicas respostas da bateria que exercitam o comportamento-alvo da mudança experimental.

### 6.3 Segunda manifestação: penalização por verbosidade (CT02)

O CT02 é o menor par de escores da bateria (0,1105 e 0,1176) por razão análoga. A resposta tem 163 tokens contra uma referência de 18, e a revocação de 0,556 indica que mais da metade do conteúdo esperado está presente. A precisão de 0,061 reflete apenas que o modelo acrescentou contexto adicional.

A métrica não distingue conteúdo adicional correto de conteúdo adicional incorreto: ambos reduzem a precisão igualmente.

### 6.4 Consequência para a leitura dos resultados

O sinal automático desta bateria é fortemente influenciado pelo **comprimento da resposta**. Entre as 12 saídas, as três de maior F1 (CT06 A/B e CT01 B) têm entre 19 e 32 tokens, e as três de menor F1 (CT02 A/B e CT05 A) têm entre 52 e 163. O sinal automático **não substitui** a avaliação humana da Parte D; a comparação entre ambos é o objeto do experimento.

---

## 7. Execução e Reprodução

```bash
cd atividade3/metrica
python3 f1_lexical.py --autoteste
python3 f1_lexical.py --entrada entrada/pares.jsonl --saida resultados/f1
```

| Artefato | Caminho |
|---|---|
| Script | [`atividade3/metrica/f1_lexical.py`](../atividade3/metrica/f1_lexical.py) |
| Configuração pré-registrada | [`atividade3/metrica/configuracao-metrica.json`](../atividade3/metrica/configuracao-metrica.json) |
| Verificação do script | [`atividade3/metrica/exemplos/casos-de-verificacao.json`](../atividade3/metrica/exemplos/casos-de-verificacao.json) |
| Entrada (12 saídas + referências) | [`atividade3/metrica/entrada/pares.jsonl`](../atividade3/metrica/entrada/pares.jsonl) |
| Resultado | [`atividade3/metrica/resultados/f1.csv`](../atividade3/metrica/resultados/f1.csv) · [`f1.json`](../atividade3/metrica/resultados/f1.json) |

---

## 8. Dependências e Entregas

| Direção | Parte | Item | Situação |
|---|---|---|---|
| Recebe | B (preparação) | 6 referências de ouro | recebido |
| Recebe | B (execução) | 12 saídas brutas | recebido |
| Entrega | A (GQM) | Fórmula, unidade, denominador e limitação do F1 | entregue |
| Entrega | E (comparação) | `resultados/f1.csv` — F1 e sinal automático das 12 saídas |

**Restrição de cegamento.** O enunciado determina ocultar versão e escores durante a avaliação humana. O arquivo `resultados/f1.csv` **não deve ser compartilhado com R1 e R2 antes do encerramento das anotações** — caso contrário, a concordância automático–humano deixa de medir concordância independente.