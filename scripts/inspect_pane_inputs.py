# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup

with open(r"C:\Projetos\Super Analista Jurídico\por_nome_pane.html", "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f.read(), "html.parser")

print("=== INPUTS ENCONTRADOS EM #porNome ===")
for inp in soup.find_all("input"):
    print(f"ID: {inp.get('id')} | Name: {inp.get('name')} | Placeholder: {inp.get('placeholder')} | Type: {inp.get('type')}")

print("\n=== BUTTONS ENCONTRADOS EM #porNome ===")
for btn in soup.find_all("button"):
    print(f"ID: {btn.get('id')} | Text: {btn.text.strip()} | Class: {btn.get('class')}")
