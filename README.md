# Equipe 06 — DeepResearch

**Disciplina:** Qualidade de Software — AV3 (2026.2)
**Escopo:** Métricas automáticas versus avaliação humana (GQM) e versionamento de sistemas generativos

## Projeto analisado

| | |
|---|---|
| Repositório | https://github.com/Alibaba-NLP/DeepResearch |
| Organização | Alibaba-NLP / Tongyi Lab |
| Licença | Apache-2.0 |
| Modelo | Tongyi-DeepResearch-30B-A3B (30,5B totais / 3,3B ativados, contexto de 128K) |

## Integrantes

| Nº | Nome | Matrícula |
|---|---|---|
| 01 | Brenno Phelipe Silva dos Santos | 202400050750 |
| 02 | Daniel José Silva Trindade | 202200059698 |
| 03 | Emilly Kathellen de Jesus Oliveira | 202400050830 |
| 04 | Filipe de Carvalho Godoy | 202100115408 |
| 05 | Giovani Barros Luna Gomes | 202400050885 |
| 06 | Lais Santos de Sousa | 202100115364 |
| 07 | Thiago Mecena Silva | 202100045840 |

## Vídeo da atividade

**URL:** https://youtu.be/Kisnk8dgzX8?is=3-YPPr7Oef5DyiyE

Detalhes de gravação e participantes em [`VIDEO.md`](VIDEO.md).

## Contribuição Individual

- **Brenno Phelipe Silva dos Santos** (202400050750): Parte D — Avaliação Humana Principal (R1). Registro da regra binária de falha crítica (0/1); condução da avaliação humana das 12 saídas (Versão A e B) sob a rubrica tridimensional (Correção, Relevância e Suporte); documentação de evidências e justificativas breves com base nas fontes oficiais do DeepResearch; preparação da infraestrutura e template de consenso para a revisão independente de R2; consolidação dos artefatos da Parte D em Markdown e CSV. 
- **Daniel José Silva Trindade** (202200059698): Execução dos prompt e versionamento, junto com comparação das versões A e B.
- **Emilly Kathellen de Jesus Oliveira** (202400050830): Parte D — Segunda revisão R2 e consenso 
- **Filipe de Carvalho Godoy** (202100115408): Parte C — métrica automática. Definição e pré-registro da métrica (F1 lexical por tokens), da normalização NFC/casefold, da tokenização, do tratamento de casos de borda e do limiar τ = 0,5, versionados antes da execução da bateria. Implementação do script de cálculo e da suíte de verificação com 10 pares de valor calculado manualmente. Cálculo do F1 e do sinal automático das 12 saídas. Declaração prévia da limitação da métrica, com previsão registrada antes da bateria de que abstenções corretas e concisas seriam reprovadas pelo sinal automático — confirmada no CT05. 
- **Giovani Barros Luna Gomes** (202400050885): Criação e estruturação do repositório no GitHub; elaboração da Parte E (comparação entre métrica automática e avaliação humana) e redação da Parte F (ciclo de vida, manifestos e rastreabilidade). 
- **Lais Santos de Sousa** (202100115364): Elaboração do plano GQM (objetivo, perguntas norteadoras Q1 e Q2, e medidas com fórmulas e limitações); definição prévia do limiar do sinal automático (=0,5) e dos critérios de avanço e bloqueio para a avaliação experimental das Versões A e B.R 
- **Thiago Mecena Silva** (202100045840): Preparação do conjunto de 6 casos de teste (CT01 a CT06), definição dos critérios de validação e elaboração das Referências Curtas de Ouro (gabarito humano) para o experimento GQM de comparação entre as Versões A e B. 

## Entregáveis (Prazo: 11/11/2026)

- [x] **Relatório técnico em PDF:** Contribuição dos integrantes, recorte/GQM, método, tabela/gráfico, análise de divergência ou caso-limite, versionamento/diagrama, decisão experimental, limitações e referências.
- [x] **Atualização do repositório:** Criação do repositório, `README.md` atualizado e referências recuperáveis das versões A e B.
- [x] **Arquivos de dados e métricas:** Arquivos das 6 perguntas/referências, 12 saídas brutas, tabela da métrica automática (F1) e 12 anotações humanas de R1 (com template preparado para as 4 revisões de R2 e consenso).
- [x] **Planejamento e versionamento:** Manifesto curto por versão, tabela do plano GQM e critério experimental de decisão.
- [x] **Apresentação:** Slides e Vídeo com participação de todos. URL do vídeo deve constar neste README, no relatório e no arquivo `VIDEO.md` (ou `video.txt`).

**Apresentação:** 12/11/2026
