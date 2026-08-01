# -*- coding: utf-8 -*-
import urllib.request
import os
import subprocess
import time

download_url = "https://github.com/04mg/caw/releases/download/0.2.1/caw-windows-amd64.exe"
target_dir = r"C:\Tools\caw"
os.makedirs(target_dir, exist_ok=True)

target_exe = os.path.join(target_dir, "caw.exe")

print(f"Baixando caw.exe de {download_url}...")
req = urllib.request.Request(download_url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req) as resp, open(target_exe, "wb") as out:
    out.write(resp.read())

print(f"Download concluído! Tamanho do arquivo: {os.path.getsize(target_exe)} bytes")

# Testar execução do caw version
try:
    res = subprocess.run([target_exe, "version"], capture_output=True, text=True, timeout=10)
    print("Versão do Caw instalada com sucesso:")
    print(res.stdout)
except Exception as e:
    print(f"Aviso na verificação de versão: {e}")
