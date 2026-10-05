# -*- coding: utf-8 -*-
"""
SUPERJUS CLI — DISPARO RÁPIDO DO DEBATE ADVERSARIAL JURÍDICO ("LAWYER VS. LAWYER")
"""
import sys
import subprocess
from pathlib import Path

ENGINE_SCRIPT = Path(r"c:\Projetos\superJus\.agents\skills\debate_juridico_multiagente\scripts\debate_adversarial_engine.py")

def main():
    if not ENGINE_SCRIPT.exists():
        print(f"Erro: Script do motor não encontrado em {ENGINE_SCRIPT}")
        sys.exit(1)
    
    cmd = [sys.executable, str(ENGINE_SCRIPT)] + sys.argv[1:]
    sys.exit(subprocess.call(cmd))

if __name__ == "__main__":
    main()
