# -*- coding: utf-8 -*-
import time, os, sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

def consultar_termo(p, termo, label):
    print(f"\n=======================================================")
    print(f"🏛️ STJ: {label} (Termo de Busca: {termo})")
    print(f"=======================================================")
    browser = p.chromium.launch(
        headless=True,
        args=["--disable-blink-features=AutomationControlled", "--no-sandbox", "--disable-dev-shm-usage"]
    )
    ctx = browser.new_context(
        viewport={"width": 1366, "height": 900},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        locale="pt-BR"
    )
    ctx.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined});")
    page = ctx.new_page()
    
    # Busca genérica
    url = f"https://processo.stj.jus.br/processo/pesquisa/?aplicacao=processos.ea&tipoPesquisa=tipoPesquisaGenerica&termo={termo}"
    try:
        print(f">> Acessando: {url}")
        page.goto(url, wait_until="domcontentloaded", timeout=45000)
        time.sleep(6)
        
        title = page.title()
        print(f">> Título: {title}")
        
        # Obter texto
        txt = page.inner_text("body")
        lines = [l.strip() for l in txt.splitlines() if l.strip()]
        print(f">> Linhas no corpo da página: {len(lines)}")
        
        # Verificar se caiu em página de erro ou se encontrou resultados
        if any("página não encontrada" in l.lower() for l in lines[:10]):
            print(">> [ALERTA] Bloqueio ou página não encontrada pelo CSID.")
        else:
            print(">> [SUCESSO] Página de resultados capturada:")
            for l in lines[:45]:
                print(f"    • {l}")
                
            # Salvar print
            page.screenshot(path=f"c:/Projetos/superJus/stj_busca_{termo}.png")
            with open(f"c:/Projetos/superJus/stj_busca_{termo}.txt", "w", encoding="utf-8") as f:
                f.write(txt)
                
    except Exception as e:
        print(f"Erro ao consultar {termo}: {e}")
    finally:
        browser.close()

def main():
    with sync_playwright() as p:
        # 1. HC 1.116.750
        consultar_termo(p, "1116750", "HC 1.116.750/RJ (Júlio Pereira Marcos)")
        # 2. RHC 244.132
        consultar_termo(p, "244132", "RHC 244.132/RJ (Júlio Pereira Marcos)")

if __name__ == "__main__":
    main()
