# Métrica automática — Parte C

Implementação do F1 lexical por tokens. Documentação completa em
[`docs/Parte C — Uma métrica automática simples.md`](../../docs/Parte%20C%20—%20Uma%20métrica%20automática%20simples.md).

| Arquivo | Função |
|---|---|
| `f1_lexical.py` | Script da métrica |
| `configuracao-metrica.json` | τ, normalização e casos de borda — **registrado em 10/11/2026, antes da bateria** |
| `exemplos/casos-de-verificacao.json` | 10 pares com valor calculado à mão |
| `entrada/pares.jsonl` | 12 pares resposta + referência, um por linha (6 casos × 2 versões) |
| `resultados/` | Saída do script |

```bash
python3 f1_lexical.py --autoteste
python3 f1_lexical.py --entrada entrada/pares.jsonl --saida resultados/f1
```
