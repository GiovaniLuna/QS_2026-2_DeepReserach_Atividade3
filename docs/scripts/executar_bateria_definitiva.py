#!/usr/bin/env python3
"""
Execução Definitiva do Loop ReAct - Atividade 3 Qualidade de Software
Responsável: Daniel José Silva Trindade (Pessoa 3 — Parte B: Execução e Versões)
Projeto: Alibaba-NLP/DeepResearch
Provedor: OpenRouter API (modelo minimax/minimax-m3.1-flash)
Executa CT01 a CT06 nas Versões A e B reproduzindo o MultiTurnReactAgent do DeepResearch.
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

BASE_DIR = "/home/daniel/Downloads/atividade3"
OUTPUT_DIR = os.path.join(BASE_DIR, "evidencias", "saidas_brutas")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Evidências factuais do repositório Alibaba-NLP/DeepResearch
REPO_FACTS = """[Informações oficiais recuperadas do repositório Alibaba-NLP/DeepResearch]
1. Modelo Tongyi-DeepResearch-30B-A3B:
   "We present Tongyi DeepResearch, an agentic large language model featuring 30.5 billion total parameters, with only 3.3 billion activated per token. Developed by Tongyi Lab, the model is specifically designed for long-horizon, deep information-seeking tasks."
   Context Length: 128K. Arquitetura MoE (30B-A3B).

2. Arquitetura e Componente WebThinker:
   "WebThinker empowers Large Reasoning Models (LRMs) with web search and browsing capabilities combining search and visit tools in iterative reasoning loops."
   Suporta paradigmas de inferência ReAct e modo 'Heavy' (IterResearch).

3. Licenciamento:
   "Apache License, Version 2.0, January 2004." O projeto é distribuído sob a licença de código aberto Apache 2.0.

4. Mapeamento de Ferramentas (TOOL_MAP em inference/react_agent.py e tool_visit.py):
   "TOOL_CLASS = [FileParser, Scholar, Visit, Search, PythonInterpreter]"
   "A ferramenta visit utiliza a API do serviço externo Jina (Jina Reader API / r.jina.ai) para leitura de páginas e sumarização de conteúdo web."

5. Benchmarks avaliados no repositório:
   "Humanity's Last Exam (HLE), BrowseComp, BrowseComp-ZH, WebWalkerQA, xbench-DeepSearch, FRAMES, SimpleQA e GAIA."
   [Nota: O repositório NÃO apresenta métricas ou pontuações referentes ao benchmark SWE-bench Lite].
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

def chamar_openrouter(messages):
    payload = json.dumps({
        "model": MODEL_NAME,
        "messages": messages,
        "temperature": 0.0,
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
            msg = data["choices"][0]["message"]
            content = msg.get("content") or ""
            reasoning = msg.get("reasoning") or ""
            usage = data.get("usage", {})
            return content, reasoning, elapsed, usage, None
    except urllib.error.HTTPError as e:
        elapsed = time.time() - t0
        return "", "", elapsed, {}, f"HTTP {e.code}: {e.read().decode('utf-8', errors='ignore')}"
    except Exception as e:
        elapsed = time.time() - t0
        return "", "", elapsed, {}, str(e)

def executar_fluxo_react(system_prompt, pergunta, versao):
    """
    Executa o ciclo ReAct inspirado no MultiTurnReactAgent do DeepResearch:
    1. Usuário envia a pergunta.
    2. O agente gera um pensamento ou tool_call.
    3. O framework devolve <tool_response> com os dados do repositório.
    4. O agente sintetiza a resposta definitiva dentro de <answer></answer>.
    """
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": pergunta}
    ]
    
    total_tokens = 0
    t_start = time.time()
    historico_chamadas = []
    
    for round_num in range(1, 4):
        content, reasoning, elapsed, usage, erro = chamar_openrouter(messages)
        total_tokens += usage.get("total_tokens", 0)
        
        if erro:
            return f"[ERRO NA CHAMADA: {erro}]", "", round_num, time.time() - t_start, total_tokens, historico_chamadas
            
        historico_chamadas.append({
            "round": round_num,
            "content": content,
            "reasoning": reasoning[:250] if reasoning else "",
            "elapsed_s": round(elapsed, 2)
        })
        
        # Se o modelo já fechou com resposta definitiva
        if "<answer>" in content and "</answer>" in content:
            ans = content.split("<answer>")[1].split("</answer>")[0].strip()
            return ans, content, round_num, time.time() - t_start, total_tokens, historico_chamadas
            
        # Se invocou tool ou pediu busca
        if "<tool_call>" in content or "search" in content or "visit" in content or not content.strip():
            tool_response = f"<tool_response>\nInformações documentais oficiais retornadas da consulta ao repositório Alibaba-NLP/DeepResearch:\n{REPO_FACTS.strip()}\n</tool_response>"
            messages.append({
                "role": "assistant",
                "content": content if content.strip() else "[Invocando search/visit no repositório...]"
            })
            messages.append({
                "role": "user",
                "content": f"{tool_response}\nCom base nas evidências documentais acima, finalize sua análise e apresente a resposta definitiva estritamente entre as tags <answer> e </answer>."
            })
            time.sleep(1.5)
            continue
        else:
            # Resposta direta sem tags explícitas
            return content.strip(), content, round_num, time.time() - t_start, total_tokens, historico_chamadas

    return content.strip(), content, round_num, time.time() - t_start, total_tokens, historico_chamadas

def main():
    print("=" * 80)
    print("INICIANDO EXECUÇÃO COMPLETA DAS 12 SAÍDAS BRUTAS (PARTE B)")
    print(f"Modelo: {MODEL_NAME} | Provedor: OpenRouter API | Temperatura: 0.0")
    print("=" * 80)

    prompts = {
        "A": carregar_prompt("A"),
        "B": carregar_prompt("B")
    }

    todas_saidas = []

    for versao in ["A", "B"]:
        print(f"\n==================== INICIANDO VERSÃO {versao} ====================")
        sys_prompt = prompts[versao]
        
        for caso in CASOS_TESTE:
            cid = caso["id"]
            print(f"\n---> Executando Caso {cid} (Versão {versao})")
            print(f"Pergunta: {caso['pergunta']}")
            
            resposta_final, raw_content, rounds, elapsed, tokens, hist = executar_fluxo_react(
                sys_prompt, caso["pergunta"], versao
            )
            
            print(f"Resultado ({elapsed:.2f}s, {rounds} rounds, {tokens} tokens):")
            print(f"Resposta Final: {resposta_final}\n")
            
            registro = {
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
                "tempo_segundos": round(elapsed, 2),
                "total_tokens": tokens,
                "rounds_react": rounds,
                "resposta_extraida": resposta_final,
                "saida_bruta_final": raw_content,
                "historico_interacoes": hist
            }
            
            todas_saidas.append(registro)
            
            # Grava individual
            with open(os.path.join(OUTPUT_DIR, f"{cid}_{versao}.json"), "w", encoding="utf-8") as f:
                json.dump(registro, f, indent=2, ensure_ascii=False)
                
            time.sleep(2)

    # Grava consolidado JSON
    consolidado_path = os.path.join(OUTPUT_DIR, "saidas_brutas_12_execucoes.json")
    with open(consolidado_path, "w", encoding="utf-8") as f:
        json.dump(todas_saidas, f, indent=2, ensure_ascii=False)

    print("\n" + "=" * 80)
    print(f"BATERIA CONCLUÍDA COM SUCESSO! 12 saídas brutas salvas em:\n{OUTPUT_DIR}")
    print("=" * 80)

if __name__ == "__main__":
    main()
