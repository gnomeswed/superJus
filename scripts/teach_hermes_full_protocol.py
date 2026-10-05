# -*- coding: utf-8 -*-
"""
Persiste no memU o Protocolo Completo Passo a Passo de Consulta de Processos
do Júlio Pereira Marcos para o Hermes Agent.
"""
import subprocess
import json
import sys
import os

sys.stdout.reconfigure(encoding="utf-8")

guia_hermes = """# 📘 Protocolo de Atuação e Passo a Passo de Consulta — Caso Júlio Pereira Marcos (Para o Hermes Agent)

Este documento instrui o **Hermes Agent** a realizar a checagem completa e contínua dos processos de **Júlio Pereira Marcos** ("Julião"), interpretar os status cartorários e persistir novidades na memória do sistema.

---

## 📌 1. Mapeamento de Processos e Instâncias

| Instância | Órgão Julgador | Número do Processo | Objeto / Função |
| :--- | :--- | :--- | :--- |
| **1ª Instância** | 2ª Vara Criminal de Búzios | `0023013-51.2021.8.19.0078` | Ação Penal Desmembrada (Tráfico / Associação) |
| **2ª Instância** | 7ª Câmara Criminal TJRJ | `0029845-67.2026.8.19.0000` | Habeas Corpus de Origem (Denegado) |
| **3ª Instância** | 6ª Turma do STJ | `HC 1.116.750 / RJ (2026/0311210-7)` | Recurso Ordinário em HC (Rel. Min. Og Fernandes) |

---

## 🛠️ 2. Passo a Passo de Execução da Consulta (Flow Completo)

### Passo 1: Resgatar o Histórico Prévio no memU
Antes de rodar qualquer script, verifique o último estado registrado no banco de memória:
```bash
python scripts/memu_retrieve.py "Júlio Pereira Marcos"
```

### Passo 2: Executar a Consulta ao Vivo no TJRJ (1ª e 2ª Instâncias)
Execute o script de automação com o interpretador Python 3.12 (com suporte a Playwright):
```bash
C:\\Users\\Administrator\\AppData\\Local\\Programs\\Python\\Python312\\python.exe scripts/verificar_julio_11_08_2026.py
```
* **O que ele faz:** Acessa o portal de consulta pública do TJRJ via headless browser, contorna o `iframe#mainframe`, preenche os números dos processos e extrai o texto do corpo da página (salvando o log em `verificacao_live_<data>.txt`).

### Passo 3: Extrair a Matriz de Movimentos Detalhadas via API Interna do TJRJ
Para obter a lista completa de movimentações com datas de juntada, nome de juízes e despachos sem depender de parsing de HTML:
```bash
C:\\Users\\Administrator\\AppData\\Local\\Programs\\Python\\Python312\\python.exe scripts/movimentos_julio_11_08_2026.py
```
* **O que ele faz:** Realiza um `fetch` direto na API rest `/consultaprocessual/api/processos/por-numero/movimentos` com o número interno do processo (`2021.078.023002-1`), gerando um JSON estruturado com todos os 55+ movimentos em `movimentos_julio_11_08_2026.json`.

### Passo 4: Verificar a Tramitação do RHC no STJ / DJEN
Para checar o status do Recurso Ordinário na 6ª Turma do STJ:
```bash
C:\\Users\\Administrator\\AppData\\Local\\Programs\\Python\\Python312\\python.exe scripts/read_stj_stealth.py
```
ou via DJEN (Diário de Justiça Eletrônico Nacional):
```bash
python scripts/djen_consulta_hc_stj.py --via-jina
```

---

## 🔍 3. Como Decodificar os Status Cartorários no TJRJ

Ao ler a `"Localização na Serventia"` nos autos de Búzios, aplique a seguinte lógica de previsão para o advogado:

1. **`"Conclusão ao Juiz"` / `"Retorno da Conclusão"`:**
   - **Significado:** Autos estão no gabinete do Juiz Dr. Danilo Marques Borges para proferir decisão ou despacho.
   - **Expectativa:** Aguardando assinatura e devolução ao cartório.
2. **`"Processamento"`:**
   - **Significado:** O Juiz já despachou/decidiu. Os autos retornaram ao Cartório da 2ª Vara para digitação de expediente, expedição de mandados/ofícios ou envio para publicação.
   - **Previsão de Publicação no DJERJ:** Entre **24h e 72h úteis** (1 a 3 dias úteis).
3. **`"Juntada - Documento"` / `"Juntada - Petição"`:**
   - **Significado:** Entrada de documento externo (peça da defesa, resposta do MP ou informação de órgão de segurança).

---

## 💾 4. Gravar Novos Aprendizados no memU
Sempre que detectar alteração de status ou nova publicação, grave no banco SQLite compartilhado:
```bash
C:\\Users\\Administrator\\AppData\\Local\\Programs\\Python\\Python312\\python.exe scripts/memu_store.py --name "andamento_julio_<data>" --track "Julio_Pereira_Marcos_Caso_Principal" --description "Descrição do andamento" --content "Conteúdo em JSON ou texto"
```
"""

temp_file = "temp_guia_hermes_protocolo.md"
with open(temp_file, "w", encoding="utf-8") as f:
    f.write(guia_hermes)

cmd = [
    sys.executable,
    "scripts/memu_store.py",
    "--name", "guia_protocolo_consulta_julio_hermes.md",
    "--track", "skill",
    "--description", "Passo a passo mestre de consulta e interpretação cartorária dos processos de Júlio Pereira Marcos para Hermes Agent",
    "--content-file", temp_file
]

res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
print("STDOUT:", res.stdout)
print("STDERR:", res.stderr)

if os.path.exists(temp_file):
    os.unlink(temp_file)
