# -*- coding: utf-8 -*-
import os, sys, pathlib, importlib.util, json
ROOT = pathlib.Path(__file__).resolve().parents[1]
fail=0
def ok(m): print(f"[OK] {m}")
def warn(m): print(f"[AVISO] {m}")
def err(m):
    global fail; fail+=1; print(f"[ERRO] {m}")

print(f"Root: {ROOT}")
print(f"Python: {sys.version}")
if not (ROOT/"core"/"app.py").exists(): err("core/app.py ausente")
else: ok("core/app.py")
if not (ROOT/"Clientes").exists(): warn("Clientes/ ausente ou fora do repo")
else: ok("Clientes/ existe")
for name in ["streamlit","pypdf","bs4","playwright"]:
    print(f" - check {name}: ", end="")
    print("ok" if importlib.util.find_spec(name) else "ausente")
if not os.getenv("DATAJUD_API_KEY"): warn("DATAJUD_API_KEY ausente (DataJud não vai funcionar)")
else: ok("DATAJUD_API_KEY presente")
if os.getenv("TELEGRAM_BOT_TOKEN"): ok("TELEGRAM_BOT_TOKEN presente")
if not (ROOT/".venv").exists(): warn(".venv ausente — crie com: py -3.11 -m venv .venv")
# compile
import subprocess
r=subprocess.run([sys.executable,"-m","compileall","core","scripts","tests"], cwd=str(ROOT))
if r.returncode!=0: err("compileall falhou")
else: ok("compileall ok")
if fail: print(f"\n{fail} erro(s)"); sys.exit(1)
print("\nPronto. Sugestão: pip install -r requirements.txt; python -m playwright install chromium")
