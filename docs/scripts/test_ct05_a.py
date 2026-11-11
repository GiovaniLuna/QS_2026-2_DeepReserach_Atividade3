import os, sys
sys.path.append("/home/daniel/Downloads/atividade3")
from scripts.test_react_loop import run_agent_loop
from versoes.versao_A.prompt import SYSTEM_PROMPT as SYS_A

ans, raw, rounds, elapsed, tok = run_agent_loop(SYS_A, "Com base estrita no repositório, qual é a pontuação oficial obtida pelo DeepResearch no benchmark SWE-bench Lite?")
print("RESULTADO CT05_A:")
print("Resposta extraída:", ans)
print("Rounds:", rounds, "Elapsed:", elapsed, "Tokens:", tok)
