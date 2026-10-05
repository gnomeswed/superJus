# -*- coding: utf-8 -*-
"""
Ensina ao Hermes Agent (e demais agentes) o protocolo completo de verificação
de andamentos e estimativa de prazos para o caso Júlio Pereira Marcos.
Persiste a instrução no banco memU SQLite compartilhado.
"""
import sys
import os
import subprocess

sys.stdout.reconfigure(encoding="utf-8")

title = "instrucao_hermes_verificacao_andamentos_julio.md"
description = "Guia completo de procedimentos para Hermes Agent verificar andamentos e prazos de Julio Pereira Marcos no TJRJ e STJ"

content = """# Guia de Atuação para Hermes Agent - Verificação de Andamentos e Prazos (Júlio Pereira Marcos)

## 1. Visão Geral da Causa
- **Cliente:** Júlio Pereira Marcos
- **Ação Penal 1ª Instância (Búzios):** `0023013-51.2021.8.19.0078` (2ª Vara Criminal)
- **Habeas Corpus TJRJ (2ª Instância):** `0029845-67.2026.8.19.0000` (7ª Câmara)
- **RHC STJ (3ª Instância):** `HC 1.116.750 / RJ (2026/0311210-7)` (6ª Turma - Rel. Min. Og Fernandes)

---

## 2. Como Executar a Checagem de Andamentos em Tempo Real

Quando o advogado perguntar se mudou algo no processo do Júlio ou pedir atualização:

1. **Checar TJRJ (1ª Instância Búzios e 2ª Instância HC):**
   - Execute o comando: `C:\\Users\\Administrator\\AppData\\Local\\Programs\\Python\\Python312\\python.exe scripts/check_all_julio_live_now.py`
   - O resultado será salvo em `c:\\Projetos\\superJus\\julio_verificacao_<data>.txt`.

2. **Como Interpretar a 'Localização na Serventia' no TJRJ:**
   - **"Retorno da Conclusão ao Juiz":** O processo está no gabinete do Juiz Dr. Danilo Marques Borges aguardando despacho/decisão.
   - **"Processamento":** O Juiz já despachou/decidiu. Os autos voltaram ao Cartório da 2ª Vara para digitação de expediente (mandado, ofício, certidão) e remessa para publicação.
   - **Janela de Publicação:** Quando entra em "Processamento", a publicação oficial no DJERJ ocorre em 24h a 72h úteis.

3. **Checar RHC no STJ:**
   - Execute o comando: `C:\\Users\\Administrator\\AppData\\Local\\Programs\\Python\\Python312\\python.exe scripts/read_stj_stealth.py`
   - Se os autos estiverem no MPF (Ministério Público Federal), a estimativa de parecer é de 5 a 10 dias úteis.

---

## 3. Como Responder sobre a Previsão de Prazos

- **Para Búzios (em 'Processamento'):** Informar que a expedição/publicação do despacho ocorre em 24h a 72h úteis (1 a 3 dias úteis).
- **Para o STJ (no MPF):** Informar que o parecer da Subprocuradoria leva de 5 a 10 dias úteis e o julgamento de mérito na 6ª Turma ocorre na 2ª quinzena do mês.

---

## 4. Persistência de Novos Achados
Sempre que detectar uma nova movimentação ou publicação, grave no memU com:
`python scripts/memu_store.py --name "andamento_julio_<data>.md" --track memory --description "Nova movimentação Júlio" --content "..."`
"""

temp_file = "temp_instrucao_hermes.md"
with open(temp_file, "w", encoding="utf-8") as f:
    f.write(content)

print("Gravando instrucao do Hermes no banco memU SQLite...")
env = os.environ.copy()
env["PYTHONIOENCODING"] = "utf-8"

try:
    cmd = [
        "python", "scripts/memu_store.py",
        "--name", title,
        "--track", "memory",
        "--description", description,
        "--content-file", temp_file
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", env=env)
    print(res.stdout)
    if res.returncode == 0:
        print("SUCESSO: Instrução do Hermes sincronizada com o banco memU!")
    else:
        print(f"Erro ao gravar: {res.stderr}")
finally:
    if os.path.exists(temp_file):
        os.unlink(temp_file)
