# -*- coding: utf-8 -*-
import os
import sys
import subprocess

sys.stdout.reconfigure(encoding='utf-8')

print("=== CRIANDO ATALHO NO DESKTOP DEDICADO DO DEEPSEEK HARNESS ===")

desktop_path = r"C:\Users\Administrator\Desktop"
launcher_script = r"C:\Projetos\superJus\scripts\deepseek_harness_gui.py"
pythonw_exe = os.path.join(os.path.dirname(sys.executable), "pythonw.exe")
shortcut_target = os.path.join(desktop_path, "DeepSeek Harness.lnk")

vbs_file = r"C:\Projetos\superJus\scripts\make_lnk.vbs"
vbs_content = f'Set WshShell = CreateObject("WScript.Shell")\n' \
              f'Set Shortcut = WshShell.CreateShortcut("{shortcut_target}")\n' \
              f'Shortcut.TargetPath = "{pythonw_exe}"\n' \
              f'Shortcut.Arguments = "{launcher_script}"\n' \
              f'Shortcut.WorkingDirectory = "C:\\Projetos\\superJus"\n' \
              f'Shortcut.Description = "DeepSeek Harness Control Center"\n' \
              f'Shortcut.IconLocation = "C:\\Windows\\System32\\shell32.dll, 14"\n' \
              f'Shortcut.Save\n'

with open(vbs_file, "w", encoding="ascii") as f:
    f.write(vbs_content)

print(f"✅ VBScript limpo gerado em: {vbs_file}")

res = subprocess.run(f'cscript //Nologo "{vbs_file}"', shell=True, capture_output=True, text=True)

if res.returncode == 0:
    print(f"✨ ÍCONE DO DEEPSEEK HARNESS CRIADO NA ÁREA DE TRABALHO!\n📍 {shortcut_target}")
else:
    print(f"Erro no VBScript: {res.stderr}")

print("=== FINALIZADO ===")
