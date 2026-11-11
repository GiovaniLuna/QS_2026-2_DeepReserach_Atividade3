import urllib.request, json, time, re

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
MODEL_NAME = "minimax/minimax-m3.1-flash"

REPO_FACTS = """
[Fonte Oficial: Alibaba-NLP/DeepResearch - Repositório GitHub Oficial]
1. Modelo Tongyi-DeepResearch-30B-A3B:
   Possui 30,5 bilhões de parâmetros totais e 3,3 bilhões de parâmetros ativos por token (MoE). Contexto de 128K.
2. WebThinker:
   Capacita Large Reasoning Models (LRMs) a executarem ciclos iterativos de raciocínio e pesquisa profunda na web combinando search e visit.
3. Licença:
   Licença de código aberto Apache 2.0 (Apache License, Version 2.0, January 2004).
4. Ferramenta Visit e TOOL_MAP:
   A ferramenta visit utiliza a API do serviço externo Jina (Jina Reader API) para leitura e sumarização do conteúdo de páginas web.
5. Benchmarks oficiais reportados:
   Humanity's Last Exam (HLE), BrowseComp, BrowseComp-ZH, WebWalkerQA, xbench-DeepSearch, FRAMES, SimpleQA e GAIA.
   O repositório NÃO apresenta métricas ou pontuações referentes ao benchmark SWE-bench Lite.
"""

def execute_chat(messages):
    payload = json.dumps({
        "model": MODEL_NAME,
        "messages": messages,
        "temperature": 0.0,
        "max_tokens": 1000
    }).encode("utf-8")
    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=payload,
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        msg = data["choices"][0]["message"]
        content = msg.get("content") or ""
        reasoning = msg.get("reasoning") or ""
        usage = data.get("usage", {})
        return content, reasoning, usage

def run_agent_loop(system_prompt, question):
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": question}
    ]
    total_tokens = 0
    start_t = time.time()
    
    for round_idx in range(1, 4):
        content, reasoning, usage = execute_chat(messages)
        total_tokens += usage.get("total_tokens", 0)
        
        # Se veio tag de resposta final
        if "<answer>" in content and "</answer>" in content:
            ans = content.split("<answer>")[1].split("</answer>")[0].strip()
            return ans, content, round_idx, time.time() - start_t, total_tokens
            
        # Se chamou ferramenta (ou gerou tool_call)
        if "<tool_call>" in content or "search" in content or "visit" in content or not content.strip():
            # Fornece a observação da ferramenta simulada com base no repositório oficial
            tool_obs = f"<tool_response>\nInformações recuperadas do repositório oficial Alibaba-NLP/DeepResearch:\n{REPO_FACTS.strip()}\n</tool_response>"
            messages.append({"role": "assistant", "content": content if content.strip() else "[Invocando ferramentas de busca/leitura...]"})
            messages.append({"role": "user", "content": f"{tool_obs}\nCom base nas informações recuperadas acima, forneça a resposta definitiva dentro das tags <answer></answer>."})
            time.sleep(1)
            continue
        else:
            # Resposta direta
            return content.strip(), content, round_idx, time.time() - start_t, total_tokens
            
    return content.strip(), content, round_idx, time.time() - start_t, total_tokens

# Teste com CT01 e CT05
from versoes.versao_B.prompt import SYSTEM_PROMPT as SYS_B
ans, raw, rounds, elapsed, tok = run_agent_loop(SYS_B, "Com base estrita no repositório, qual é a pontuação oficial obtida pelo DeepResearch no benchmark SWE-bench Lite?")
print("RESULTADO CT05_B:")
print("Resposta extraída:", ans)
print("Rounds:", rounds, "Elapsed:", elapsed, "Tokens:", tok)
