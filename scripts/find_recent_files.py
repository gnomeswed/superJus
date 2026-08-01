# -*- coding: utf-8 -*-
import os
import time

search_dirs = [
    r"C:\Users\Administrator\Desktop",
    r"C:\Users\Administrator\Downloads",
    r"C:\Users\Administrator\Documents"
]

now = time.time()
recent_files = []

for d in search_dirs:
    if os.path.exists(d):
        for root, dirs, files in os.walk(d):
            for f in files:
                fpath = os.path.join(root, f)
                try:
                    mtime = os.path.getmtime(fpath)
                    age_hours = (now - mtime) / 3600.0
                    if age_hours <= 12:  # modificados nas últimas 12 horas
                        recent_files.append({
                            "name": f,
                            "path": fpath,
                            "age_minutes": round((now - mtime) / 60.0, 1),
                            "size": os.path.getsize(fpath)
                        })
                except Exception:
                    pass

recent_files.sort(key=lambda x: x["age_minutes"])
print(f"Arquivos modificados recentemente (total: {len(recent_files)}):")
for item in recent_files[:15]:
    print(f" - {item['path']} ({item['size']} bytes) | {item['age_minutes']} min atrás")
