# -*- coding: utf-8 -*-
"""Reinicia o gateway do Hermes com segurança (fora do processo do gateway)."""
import subprocess, time, os, sys

sys.stdout.reconfigure(encoding="utf-8")

# 1. Mata o gateway atual (PID 4256 se existir)
ps = subprocess.run(
    ["powershell", "-Command",
     "Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like '*hermes_cli.main gateway*' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }"],
    capture_output=True, text=True, timeout=60
)
print("Kill gateway:", ps.stdout.strip() or "OK (nenhum erro)")

time.sleep(3)

# 2. Religa via scheduled task
rt = subprocess.run(
    ["powershell", "-Command", "schtasks /Run /TN 'Hermes_Gateway'"],
    capture_output=True, text=True, timeout=60
)
print("SchTasks:", rt.stdout.strip() or rt.stderr.strip() or "OK")

time.sleep(15)

# 3. Verifica status
st = subprocess.run(["hermes", "gateway", "status"], capture_output=True, text=True, timeout=60,
                    env={**os.environ, "PATH": os.environ.get("PATH", "")})
print("=== STATUS ===")
print(st.stdout[-600:] if st.stdout else st.stderr[-400:])
