# -*- coding: utf-8 -*-
"""Reinicia o 9router (node) para recarregar conexões novas."""
import subprocess, time, sys, os

sys.stdout.reconfigure(encoding="utf-8")

# Mata o 9router server (custom-server.js)
ps = subprocess.run(
    ["powershell", "-NoProfile", "-Command",
     "Get-CimInstance Win32_Process | Where-Object { $_.Name -eq 'node.exe' -and $_.CommandLine -like '*custom-server.js*' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }"],
    capture_output=True, text=True, timeout=60
)
print("Kill 9router server:", ps.stdout.strip() or "OK")

time.sleep(3)

# Relança via o binário do 9router (startup.bat)
rt = subprocess.run(
    ["cmd", "/c", "start", "/min", "", "C:\\Users\\Administrator\\AppData\\Local\\hermes\\node\\node.exe",
     "C:\\Users\\Administrator\\AppData\\Local\\hermes\\node\\node_modules\\9router\\app\\custom-server.js"],
    capture_output=True, text=True, timeout=30
)
print("Relançado")

time.sleep(12)

# Verifica porta
chk = subprocess.run(["netstat", "-ano"], capture_output=True, text=True, timeout=30)
portas = [l for l in chk.stdout.splitlines() if ":20128" in l and "LISTENING" in l]
print("PORTA 20128:", portas[:2] if portas else "NÃO ABRIU")

# Testa API
try:
    import urllib.request
    with urllib.request.urlopen("http://127.0.0.1:20128/v1/models", timeout=15) as r:
        body = r.read().decode()
        print("API OK, bytes:", len(body))
except Exception as e:
    print("API ERRO:", e)
