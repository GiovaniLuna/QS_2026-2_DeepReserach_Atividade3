#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parte C — Métrica automática simples (F1 lexical por tokens)
Qualidade de Software — Atividade 3 (2026.2) — Equipe 06

Calcula o F1 lexical entre a resposta gerada e a referência humana, e aplica o
limiar tau registrado em configuracao-metrica.json.

A normalização, a tokenização e o limiar são fixados ANTES da bateria e não
podem ser alterados depois de ver os resultados.

Uso:
    python3 f1_lexical.py --autoteste
    python3 f1_lexical.py --entrada entrada/pares.jsonl --saida resultados/f1
"""

import argparse
import csv
import json
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
CONFIG = RAIZ / "configuracao-metrica.json"

# Token = sequência de caracteres de palavra (letras, dígitos, sublinhado), Unicode.
# Dígitos entram como tokens de propósito: é o que permite distinguir "10/11"
# de "11/11", exemplo de limitação citado no próprio enunciado.
PADRAO_TOKEN = re.compile(r"\w+", re.UNICODE)


def carregar_config():
    with open(CONFIG, encoding="utf-8") as f:
        return json.load(f)


def tokenizar(texto):
    """NFC -> casefold -> tokens de palavra. Ordem fixa, declarada na Parte C."""
    if texto is None:
        return []
    texto = unicodedata.normalize("NFC", str(texto))
    texto = texto.casefold()
    return PADRAO_TOKEN.findall(texto)


def f1_lexical(resposta, referencia):
    """
    Retorna (p, r, f1, observacao).

    f1 é None quando a referência não tem tokens: nesse caso o caso precisa ser
    corrigido, e o script não inventa score (regra do enunciado).
    """
    tok_resp = tokenizar(resposta)
    tok_ref = tokenizar(referencia)

    if not tok_ref:
        return None, None, None, "REFERENCIA SEM TOKENS - corrigir o caso antes de pontuar"

    if not tok_resp:
        return 0.0, 0.0, 0.0, "resposta vazia"

    comuns = sum((Counter(tok_resp) & Counter(tok_ref)).values())

    if comuns == 0:
        return 0.0, 0.0, 0.0, "sem sobreposicao de tokens"

    p = comuns / len(tok_resp)
    r = comuns / len(tok_ref)
    return p, r, 2 * p * r / (p + r), ""


def sinal_automatico(f1, tau):
    if f1 is None:
        return "indefinido"
    return "aprova" if f1 >= tau else "reprova"


def ler_entrada(caminho):
    """Aceita JSONL (uma linha por saída) ou JSON com lista."""
    texto = Path(caminho).read_text(encoding="utf-8").strip()
    if not texto:
        return []
    if texto.lstrip().startswith("["):
        return json.loads(texto)
    return [json.loads(linha) for linha in texto.splitlines() if linha.strip()]


def processar(registros, tau):
    linhas = []
    for reg in registros:
        p, r, f1, obs = f1_lexical(reg.get("resposta"), reg.get("referencia"))
        linhas.append({
            "caso": reg.get("caso", ""),
            "versao": reg.get("versao", ""),
            "tokens_resposta": len(tokenizar(reg.get("resposta"))),
            "tokens_referencia": len(tokenizar(reg.get("referencia"))),
            "precisao": None if p is None else round(p, 4),
            "revocacao": None if r is None else round(r, 4),
            "f1_lexical": None if f1 is None else round(f1, 4),
            "sinal_automatico": sinal_automatico(f1, tau),
            "observacao": obs,
        })
    return linhas


def gravar(linhas, destino):
    destino = Path(destino)
    destino.parent.mkdir(parents=True, exist_ok=True)

    csv_path = destino.with_suffix(".csv")
    with open(csv_path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(linhas[0].keys()), delimiter=";")
        w.writeheader()
        for linha in linhas:
            w.writerow({k: ("" if v is None else v) for k, v in linha.items()})

    json_path = destino.with_suffix(".json")
    json_path.write_text(json.dumps(linhas, ensure_ascii=False, indent=2), encoding="utf-8")
    return csv_path, json_path


def resumo_por_versao(linhas, tau):
    """Média de F1 e taxa de aprovação automática por versão, denominador explícito."""
    versoes = {}
    for linha in linhas:
        versoes.setdefault(linha["versao"], []).append(linha)

    saida = []
    for versao in sorted(versoes):
        grupo = versoes[versao]
        validos = [l["f1_lexical"] for l in grupo if l["f1_lexical"] is not None]
        aprovados = sum(1 for l in grupo if l["sinal_automatico"] == "aprova")
        saida.append({
            "versao": versao,
            "n_saidas": len(grupo),
            "n_pontuadas": len(validos),
            "f1_medio": round(sum(validos) / len(validos), 4) if validos else None,
            "aprovacao_automatica": f"{aprovados}/{len(grupo)}",
            "tau": tau,
        })
    return saida


# ──────────────────────────── verificação do script ────────────────────────────

def autoteste():
    """
    Roda os pares de verificação com valor esperado calculado à mão.
    Serve para provar que o script está correto ANTES das 12 saídas existirem.
    """
    casos = json.loads((RAIZ / "exemplos" / "casos-de-verificacao.json").read_text(encoding="utf-8"))
    falhas = 0

    print(f"{'caso':<34} {'esperado':>10} {'obtido':>10}   resultado")
    print("-" * 74)
    for caso in casos:
        _, _, f1, obs = f1_lexical(caso["resposta"], caso["referencia"])
        esperado = caso["f1_esperado"]

        if esperado is None:
            ok = f1 is None
            mostra_e, mostra_o = "None", "None" if f1 is None else f"{f1:.4f}"
        else:
            ok = f1 is not None and abs(f1 - esperado) < 1e-9
            mostra_e = f"{esperado:.4f}"
            mostra_o = "None" if f1 is None else f"{f1:.4f}"

        if not ok:
            falhas += 1
        print(f"{caso['descricao']:<34} {mostra_e:>10} {mostra_o:>10}   {'OK' if ok else 'FALHOU'}")

    print("-" * 74)
    if falhas:
        print(f"{falhas} verificacao(oes) falharam.")
        return 1
    print(f"Todas as {len(casos)} verificacoes passaram.")
    return 0


def main():
    ap = argparse.ArgumentParser(description="F1 lexical por tokens — Parte C")
    ap.add_argument("--entrada", help="JSONL ou JSON com caso, versao, resposta, referencia")
    ap.add_argument("--saida", default="resultados/f1", help="prefixo dos arquivos de saida")
    ap.add_argument("--autoteste", action="store_true", help="roda os pares de verificacao")
    args = ap.parse_args()

    if args.autoteste:
        return autoteste()

    if not args.entrada:
        ap.error("informe --entrada ou use --autoteste")

    config = carregar_config()
    tau = config["tau"]

    registros = ler_entrada(args.entrada)
    if not registros:
        print("Entrada vazia.", file=sys.stderr)
        return 1

    linhas = processar(registros, tau)
    csv_path, json_path = gravar(linhas, args.saida)

    print(f"tau = {tau}  (registrado em {config['registrado_em']})")
    print(f"{len(linhas)} saidas processadas\n")

    for r in resumo_por_versao(linhas, tau):
        f1m = "—" if r["f1_medio"] is None else f"{r['f1_medio']:.4f}"
        print(f"  versao {r['versao']}: F1 medio {f1m} | aprovacao automatica {r['aprovacao_automatica']}")

    pendentes = [l for l in linhas if l["f1_lexical"] is None]
    if pendentes:
        print(f"\n  ATENCAO: {len(pendentes)} caso(s) sem referencia valida, nao pontuados:")
        for l in pendentes:
            print(f"    {l['caso']} / {l['versao']} — {l['observacao']}")

    print(f"\ngravado: {csv_path}\n         {json_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())