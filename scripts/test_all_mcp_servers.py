# -*- coding: utf-8 -*-
import json
import subprocess
import sys
import os

sys.stdout.reconfigure(encoding="utf-8")

config = json.load(open(r"C:\Users\Administrator\.gemini\config\mcp_config.json", encoding="utf-8"))

init_req = json.dumps({
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
        "protocolVersion": "2024-11-05",
        "capabilities": {},
        "clientInfo": {"name": "test-client", "version": "1.0.0"}
    }
}) + "\n"

results = {}

for name, srv in config.get("mcpServers", {}).items():
    cmd = [srv["command"]] + srv.get("args", [])
    env = os.environ.copy()
    env.update(srv.get("env", {}))
    print(f"\n==========================================")
    print(f"TESTANDO SERVIDOR: {name}")
    print(f"Comando: {' '.join(cmd)}")
    print(f"==========================================")
    try:
        proc = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            env=env
        )
        stdout, stderr = proc.communicate(input=init_req, timeout=10)
        lines = [l for l in stdout.splitlines() if l.strip()]
        first_line = lines[0] if lines else "VAZIO"
        is_json = False
        try:
            parsed = json.loads(first_line)
            if "result" in parsed or "jsonrpc" in parsed:
                is_json = True
        except Exception:
            pass
            
        if is_json:
            print(f"[OK] Resposta JSON-RPC valida recebida!")
            results[name] = "OK"
        else:
            print(f"[FALHA] STDOUT NAO EH JSON PURO!")
            print(f"Primeira linha: {repr(first_line[:150])}")
            if len(lines) > 1:
                print(f"Segunda linha: {repr(lines[1][:150])}")
            if stderr:
                print(f"STDERR: {repr(stderr.strip()[:300])}")
            results[name] = f"FALHA: {first_line[:100]}"
    except subprocess.TimeoutExpired:
        proc.kill()
        print(f"[TIMEOUT] Nao respondeu em 10s")
        results[name] = "TIMEOUT"
    except Exception as e:
        print(f"[ERRO] Falha ao iniciar: {e}")
        results[name] = f"ERRO: {e}"

print("\n\n" + "="*50)
print("RESUMO DE DIAGNOSTICO:")
for k, v in results.items():
    print(f"  {k}: {v}")
print("="*50)
