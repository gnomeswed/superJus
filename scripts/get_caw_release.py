# -*- coding: utf-8 -*-
import urllib.request
import json
import os

url = "https://api.github.com/repos/04mg/caw/releases/latest"
headers = {"User-Agent": "Mozilla/5.0"}

req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode('utf-8'))
    print(f"Latest Release Tag: {data.get('tag_name')}")
    print("Assets:")
    for asset in data.get('assets', []):
        print(f"  - {asset['name']}: {asset['browser_download_url']} ({asset['size']} bytes)")
except Exception as e:
    print(f"Erro ao buscar release: {e}")
