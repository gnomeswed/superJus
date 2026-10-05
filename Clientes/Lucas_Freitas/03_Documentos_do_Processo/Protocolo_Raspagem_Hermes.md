# 🛠️ PROTOCOLO DE RASPAGEM PROCESSUAL E EXTRAÇÃO NA ÍNTEGRA PARA O HERMES AGENT

## 📌 Visão Geral
Este guia define o protocolo técnico padronizado para que o **Hermes Agent** (e demais agentes como CommandCode e OpenCode) realize consultas processuais no portal do **TJRJ**, extraia movimentações e capture a **íntegra de todas as decisões, sentenças e mandados** via Playwright Headless sem falhas de iframe ou timeout.

---

## ⚙️ 1. Ambiente e Requisitos Obrigatórios
- **Diretório Raiz:** `c:\Projetos\superJus`
- **Interpretador Python Obrigatório:** `C:\Users\Administrator\AppData\Local\Programs\Python\Python312\python.exe`
- **Codificação PowerShell Obrigatória:** `$env:PYTHONIOENCODING="utf-8"` (evita falhas de encoding CP1252 com acentos e emojis).

---

## 🔍 2. Estratégia Resiliente de Navegação no TJRJ
- **URL Base:** `https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica`
- **Timeout da Página:** 45.000ms (`timeout=45000`)
- **Modo de Espera:** `wait_until="domcontentloaded"`
- **Garantia de Iframe:** Usar sempre `page.wait_for_selector("iframe#mainframe", timeout=30000)` antes de chamar `.content_frame()` para prevenir o erro `'NoneType' object has no attribute 'content_frame'`.

---

## 🤖 3. Código Padrão de Raspagem (Exemplo em Playwright Python)

```python
import time, sys, os
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")

nproc = "0011857-95.2024.8.19.0002" # Processo de Lucas de Souza Freitas

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
    ctx = browser.new_context(viewport={"width": 1280, "height": 900})
    page = ctx.new_page()

    page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=45000, wait_until="domcontentloaded")
    page.wait_for_selector("iframe#mainframe", timeout=30000)
    real_frame = page.query_selector("iframe#mainframe").content_frame()

    # Preencher numeroProcesso
    real_frame.evaluate(f"""() => {{
        const inp = Array.from(document.querySelectorAll('input')).find(i => i.name === 'numeroProcesso' || i.id === 'numeroProcesso');
        if (inp) {{
            inp.value = '{nproc}';
            inp.dispatchEvent(new Event('input', {{ bubbles: true }}));
            inp.dispatchEvent(new Event('change', {{ bubbles: true }}));
        }}
    }}""")

    # Clicar Pesquisar
    real_frame.evaluate("""() => {
        const btn = Array.from(document.querySelectorAll('button')).find(b => b.offsetWidth > 0 && b.textContent.toLowerCase().includes('pesquisar'));
        if (btn) btn.click();
    }""")
    time.sleep(10)

    # Clicar Todos os Movimentos
    real_frame.evaluate("""() => {
        const btn = Array.from(document.querySelectorAll('a, button, span')).find(b => b.textContent && b.textContent.includes('Todos') && b.textContent.includes('Movimentos'));
        if (btn) btn.click();
    }""")
    time.sleep(4)

    # Iterar sobre modais de decisão na íntegra
    links_count = real_frame.evaluate("""() => {
        const links = Array.from(document.querySelectorAll('a, button, span, div'));
        return links.filter(l => l.textContent && (l.textContent.includes('Ver Íntegra') || l.textContent.includes('Visualizar Ato'))).length;
    }""")

    for idx in range(links_count):
        real_frame.evaluate(f"""(i) => {{
            const links = Array.from(document.querySelectorAll('a, button, span, div')).filter(l => l.textContent && (l.textContent.includes('Ver Íntegra') || l.textContent.includes('Visualizar Ato')));
            if (links[i]) links[i].click();
        }}""", idx)
        time.sleep(4)

        # Capturar modal
        modal_text = real_frame.evaluate("""() => {
            const modals = Array.from(document.querySelectorAll('.modal-body, .ui-dialog-content, div[role="dialog"]'));
            return modals.length > 0 ? modals.map(m => m.innerText.trim()).join('\n\n') : document.body.innerText;
        }""")
```

---

## 📂 4. Taxonomia Obrigatória de Armazenamento
Os arquivos baixados e processados devem ser gravados estritamente na pasta do cliente:
- `Clientes/[Nome_Sobrenome]/01_Dados_do_Cliente/case_meta.json`
- `Clientes/[Nome_Sobrenome]/02_Movimentacoes_Individuais/YYYY-MM-DD_NN_Nome_Movimento.md`
- `Clientes/[Nome_Sobrenome]/03_Documentos_do_Processo/Decisoes_na_Integra/`
- `Clientes/[Nome_Sobrenome]/04_Analises_e_Estrategias/`
- `Clientes/[Nome_Sobrenome]/05_Processos_Anteriores/`
