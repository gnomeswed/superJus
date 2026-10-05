import time
import sys
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

print("Iniciando teste com espera ativa pelos seletores Angular...")
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=90000)
    print("Aguardando botão Pesquisar...")
    btn = page.wait_for_selector('button:has-text("Pesquisar")', timeout=60000)
    print("Botão Pesquisar encontrado com sucesso!")
    
    # Preencher e pesquisar
    inp = page.wait_for_selector('input[placeholder*="número do processo"]', timeout=30000)
    inp.fill("0023013-51.2021.8.19.0078")
    print("Processo preenchido!")
    btn.click()
    print("Pesquisar clicado! Aguardando iframe...")
    
    frame_el = page.wait_for_selector('iframe#mainframe', timeout=60000)
    print("Iframe encontrado! Aguardando conteúdo...")
    time.sleep(5)
    frame = frame_el.content_frame()
    
    # Aguardar que o iframe tenha texto do processo
    frame.wait_for_selector('text="0023013-51.2021.8.19.0078"', timeout=60000)
    print("Processo carregado dentro do iframe!")
    print("Texto parcial do iframe:")
    print(frame.inner_text("body")[:600])
    
    browser.close()
print("Teste concluído com sucesso!")
