Set WshShell = CreateObject("WScript.Shell")
Set Shortcut = WshShell.CreateShortcut("C:\Users\Administrator\Desktop\DeepSeek Harness.lnk")
Shortcut.TargetPath = "C:\Users\Administrator\AppData\Local\Programs\Python\Python312\pythonw.exe"
Shortcut.Arguments = "C:\Projetos\superJus\scripts\deepseek_harness_gui.py"
Shortcut.WorkingDirectory = "C:\Projetos\superJus"
Shortcut.Description = "DeepSeek Harness Control Center"
Shortcut.IconLocation = "C:\Windows\System32\shell32.dll, 14"
Shortcut.Save
