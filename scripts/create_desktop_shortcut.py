# -*- coding: utf-8 -*-
import os
import subprocess

tools_dir = r"C:\Tools\caw"
bat_path = os.path.join(tools_dir, "Iniciar_Caw.bat")
ico_path = os.path.join(tools_dir, "caw.ico")
exe_path = os.path.join(tools_dir, "caw.exe")

# 1. Criar o Iniciar_Caw.bat
bat_content = """@echo off
title Caw - Web Terminal Multiplexer
color 0A
echo ========================================================
echo   CAW - Web Terminal Multiplexer para Agentes de IA
echo ========================================================
echo.
echo  [+] Servidor iniciando em http://localhost:8080
echo  [+] Abrindo navegador padrao...
echo.
timeout /t 2 /nobreak >nul
start http://localhost:8080
"%~dp0caw.exe"
"""

with open(bat_path, "w", encoding="utf-8") as f:
    f.write(bat_content)

print(f"Script de inicialização criado em: {bat_path}")

# 2. Criar o atalho no Desktop do Usuário
ps_script = f"""
$WshShell = New-Object -ComObject WScript.Shell
$DesktopPath = [System.Environment]::GetFolderPath('Desktop')
$ShortcutPath = Join-Path -Path $DesktopPath -ChildPath 'Caw Web Terminal.lnk'
$Shortcut = $WshShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = '{bat_path}'
$Shortcut.WorkingDirectory = '{tools_dir}'
$Shortcut.IconLocation = '{ico_path}, 0'
$Shortcut.Description = 'Iniciar o Caw - Web Terminal Multiplexer para Agentes de IA'
$Shortcut.Save()
Write-Host "Atalho criado com sucesso em: $ShortcutPath"
"""

ps_file = os.path.join(tools_dir, "create_shortcut.ps1")
with open(ps_file, "w", encoding="utf-8") as f:
    f.write(ps_script)

res = subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", ps_file], capture_output=True, text=True)
print(res.stdout)
if res.stderr:
    print("Aviso:", res.stderr)
