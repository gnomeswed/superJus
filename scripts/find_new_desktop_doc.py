# -*- coding: utf-8 -*-
import os
import json
import time

desktop_dir = r"C:\Users\Administrator\Desktop"

files_info = []
now = time.time()

for fname in os.listdir(desktop_dir):
    fpath = os.path.join(desktop_dir, fname)
    if os.path.isfile(fpath):
        mtime = os.path.getmtime(fpath)
        files_info.append({
            "name": fname,
            "path": fpath,
            "mtime": mtime,
            "mtime_str": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mtime)),
            "age_seconds": round(now - mtime, 1),
            "size": os.path.getsize(fpath)
        })

files_info.sort(key=lambda x: x["mtime"], reverse=True)

print("Top 10 arquivos mais recentes na Área de Trabalho:")
for f in files_info[:10]:
    print(f" - {f['name']} ({f['size']} bytes) | Modificado: {f['mtime_str']} ({f['age_seconds']}s atrás)")
