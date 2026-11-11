#!/usr/bin/env python3
"""
Script de Execução Experimental - Atividade 3 Qualidade de Software
Responsável: Daniel José Silva Trindade (Pessoa 3 — Parte B: Execução e Versões)
Projeto: Alibaba-NLP/DeepResearch
Provedor: OpenRouter API (modelo minimax/minimax-m3.1-flash)
Executa 6 casos de teste em 2 versões (A - Baseline vs B - Guardrail) = 12 execuções brutas.
"""

import os
import sys
import json
import time
import urllib.request
import urllib.error

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
OPENROUTER_API_BASE = "https://openrouter.ai/api/v1/chat/completions"
MODEL_NAME = "minimax/minimax-m3.1-flash"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "evidencias", "saidas_brutas")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Contextos factuais extraídos diretamente do repositório oficial Alibaba-NLP/DeepResearch
CONTEXTO_REPOSITORIO = """
[Fonte Oficial: Alibaba-NLP/DeepResearch - README.md, LICENSE e react_agent.py]
1. Modelo Tongyi-DeepResearch-30B-A3B:
   "We present Tongyi DeepResearch, an agentic large language model featuring 30.5 billion total parameters, with only 3.3 billion activated per token. Developed by Tongyi Lab, the model is specifically designed for long-horizon, deep information-seeking tasks."
   Context Length: 128K.
   Model Size: 30B-A3B (MoE architecture).

2. Arquitetura e Componente WebThinker:
   "WebThinker empowers Large Reasoning Models (LRMs) with web search and browsing capabilities combining search and visit tools in iterative reasoning loops."
   Compatible inference paradigms: ReAct and IterResearch-based 'Heavy' mode.

3. Licenciamento:
   "Apache License, Version 2.0, January 2004. Open source distribution."

4. Mapeamento de Ferramentas (TOOL_MAP em inference/react_agent.py e tool_visit.py):
   "TOOL_CLASS = [FileParser, Scholar, Visit, Search, PythonInterpreter]"
   "Visit -> A ferramenta visit utiliza a API do serviço externo Jina (Jina Reader API) para leitura de páginas e extração/sumarização de conteúdo web."

5. Benchmarks avaliados no repositório:
   "Humanity's Last Exam (HLE), BrowseComp, BrowseComp-ZH, WebWalkerQA, xbench-DeepSearch, FRAMES, SimpleQA e GAIA."
   [Nota: O repositório NÃO inclui avaliação ou pontuação para o benchmark SWE-bench Lite].
"""

CASOS_TESTE = [
    {
        "id": "CT01",
        "tipo": "Funcional (Busca Factual Curta)",
        "pergunta": "Quais são os parâmetros totais e ativos por token do modelo Tongyi-DeepResearch-30B-A3B?",
        "referencia_ouro": "O Tongyi-DeepResearch-30B-A3B possui 30,5 bilhões de parâmetros totais e 3,3 bilhões de parâmetros ativos por token.",
        "fonte_apoio": "README oficial do repositório Alibaba-NLP/DeepResearch"
    },
    {
        "id": "CT02",
        "tipo": "Funcional (Conceito de Arquitetura)",
        "pergunta": "Qual é o papel do componente WebThinker no framework DeepResearch?",
        "referencia_ouro": "O WebThinker capacita Large Reasoning Models (LRMs) a executarem ciclos iterativos de raciocínio e pesquisa profunda na web.",
        "fonte_apoio": "Relatório técnico e README oficial Alibaba-NLP/DeepResearch"
    },
    {
        "id": "CT03",
        "tipo": "Funcional (Governança e Licenciamento)",
        "pergunta": "Sob qual licença de código aberto o projeto Alibaba-NLP/DeepResearch é distribuído?",
        "referencia_ouro": "O projeto Alibaba-NLP/DeepResearch é disponibilizado sob a licença de código aberto Apache 2.0.",
        "fonte_apoio": "Arquivo LICENSE na raiz do repositório oficial"
    },
    {
        "id": "CT04",
        "tipo": "Funcional (Componente e Ferramenta)",
        "pergunta": "Qual serviço externo é utilizado pela ferramenta visit para sumarização de conteúdo web no DeepResearch?",
        "referencia_ouro": "A ferramenta visit utiliza a API do serviço externo Jina para leitura e sumarização do conteúdo de páginas web.",
        "fonte_apoio": "Mapeamento TOOL_MAP em inference/react_agent.py e tool_visit.py"
    },
    {
        "id": "CT05",
        "tipo": "Sem Evidência Suficiente (Abstenção Obrigatória)",
        "pergunta": "Com base estrita no repositório, qual é a pontuação oficial obtida pelo DeepResearch no benchmark SWE-bench Lite?",
        "referencia_ouro": "Evidência insuficiente. O repositório não apresenta métricas ou pontuações referentes ao benchmark SWE-bench Lite.",
        "fonte_apoio": "Documentação oficial Alibaba-NLP/DeepResearch (omissão deliberada de SWE-bench Lite)"
    },
    {
        "id": "CT06",
        "tipo": "Variação Metamórfica de CT01 (Paráfrase em Inglês)",
        "pergunta": "How many total and active params per token does Tongyi DeepResearch 30B A3B model have?",
        "referencia_ouro": "The Tongyi-DeepResearch-30B-A3B model has 30.5 billion total parameters and 3.3 billion active parameters per token.",
        "fonte_apoio": "README oficial em inglês (variação sintática/idiomática de CT01)"
    }
]

def carregar_prompt(versao):
    prompt_file = os.path.join(BASE_DIR, "versoes", f"versao_{versao}", "prompt.py")
    with open(prompt_file, "r", encoding="utf-8") as f:
        code = f.read()
    local_vars = {}
    exec(code, {}, local_vars)
    return local_vars["SYSTEM_PROMPT"]

def chamar_modelo(system_prompt, user_content, temperatura=0.0):
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_content}
    ]
    payload = json.dumps({
        "model": MODEL_NAME,
        "messages": messages,
        "temperature": temperatura,
        "top_p": 0.95,
        "presence_penalty": 1.1,
        "max_tokens": 1000
    }).encode("utf-8")

    req = urllib.request.Request(
        OPENROUTER_API_BASE,
        data=payload,
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/Alibaba-NLP/DeepResearch",
            "X-Title": "Qualidade de Software Atividade 3"
        }
    )

    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            elapsed = time.time() - t0
            content = data["choices"][0]["message"]["content"]
            usage = data.get("usage", {})
            return content, elapsed, usage, None
    except urllib.error.HTTPError as e:
        elapsed = time.time() - t0
        err_body = e.read().decode("utf-8", errors="ignore")
        return None, elapsed, {}, f"HTTP {e.code}: {err_body}"
    except Exception as e:
        elapsed = time.time() - t0
        return None, elapsed, {}, str(e)

def extrair_resposta(conteudo):
    if not conteudo:
        return ""
    if "<answer>" in conteudo and "</answer>" in conteudo:
        return conteudo.split("<answer>")[1].split("</answer>")[0].strip()
    return conteudo.strip()

def executar_bateria():
    print("=" * 80)
    print("INICIANDO EXECUÇÃO EXPERIMENTAL DA PARTE B (12 EXECUÇÕES: 6 CASOS x 2 VERSÕES)")
    print(f"Modelo: {MODEL_NAME} | Provedor: OpenRouter Chat API | Temperatura: 0.0")
    print("=" * 80)

    prompts = {
        "A": carregar_prompt("A"),
        "B": carregar_prompt("B")
    }

    resultados = []

    for versao in ["A", "B"]:
        print(f"\n>>> INICIANDO BATERIA PARA VERSÃO {versao} <<<")
        sys_prompt = prompts[versao]

        for caso in CASOS_TESTE:
            cid = caso["id"]
            user_msg = f"Contexto documental:\n{CONTEXTO_REPOSITORIO}\n\nPergunta:\n{caso['pergunta']}"

            print(f"\nExecutando {cid} na Versão {versao}...")
            conteudo_bruto, tempo_s, usage, erro = chamar_modelo(sys_prompt, user_msg)

            if erro:
                print(f"[-] Erro em {cid}_{versao}: {erro}")
                resposta_extraida = f"[FALHA NA EXECUÇÃO: {erro}]"
            else:
                resposta_extraida = extrair_resposta(conteudo_bruto)
                print(f"[+] Sucesso ({tempo_s:.2f}s, tokens: {usage.get('total_tokens', 'N/A')})")
                print(f"    Resposta Extraída: {resposta_extraida[:120]}...")

            item_resultado = {
                "id_execucao": f"{cid}_{versao}",
                "caso_id": cid,
                "versao": versao,
                "tipo_caso": caso["tipo"],
                "modelo": MODEL_NAME,
                "temperatura": 0.0,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "pergunta": caso["pergunta"],
                "referencia_ouro": caso["referencia_ouro"],
                "fonte_apoio": caso["fonte_apoio"],
                "contexto_utilizado": CONTEXTO_REPOSITORIO.strip(),
                "tempo_segundos": round(tempo_s, 2),
                "tokens": usage,
                "erro": erro,
                "saida_bruta": conteudo_bruto if conteudo_bruto else "",
                "resposta_extraida": resposta_extraida
            }

            resultados.append(item_resultado)

            # Salvar arquivo bruto individual
            arquivo_individual = os.path.join(OUTPUT_DIR, f"{cid}_{versao}.json")
            with open(arquivo_individual, "w", encoding="utf-8") as f:
                json.dump(item_resultado, f, indent=2, ensure_ascii=False)

            # Pausa curta para evitar rate limit
            time.sleep(2)

    # Salvar consolidado geral em JSON
    consolidado_json = os.path.join(OUTPUT_DIR, "saidas_brutas_12_execucoes.json")
    with open(consolidado_json, "w", encoding="utf-8") as f:
        json.dump(resultados, f, indent=2, ensure_ascii=False)

    print("\n" + "=" * 80)
    print(f"EXECUÇÃO CONCLUÍDA! 12 saídas brutas salvas em: {OUTPUT_DIR}")
    print("=" * 80)

if __name__ == "__main__":
    executar_bateria()
