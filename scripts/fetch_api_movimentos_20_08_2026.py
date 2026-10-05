# -*- coding: utf-8 -*-
import os, sys, time, json
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')
OUT_DIR = r"C:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos\Caso_Principal\documentos_processo\_varredura_20_08_2026"
os.makedirs(OUT_DIR, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=['--disable-blink-features=AutomationControlled', '--no-sandbox'])
    ctx = browser.new_context(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    page = ctx.new_page()
    page.goto('https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica', timeout=45000, wait_until='domcontentloaded')
    time.sleep(3)
    
    # 1. Principal 0023013-51.2021.8.19.0078
    res = page.evaluate('''async () => {
        try {
            const resp = await fetch('/consultaprocessual/api/processos/por-numero/movimentos', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({tipoProcesso: 1, codigoProcesso: '2021.078.023002-1', indProcVolumoso: 'N', ultimaOrdemExibida: null})
            });
            return await resp.json();
        } catch(e) {
            return {error: e.message};
        }
    }''')
    
    print('Principal - Total movimentos:', len(res) if isinstance(res, list) else type(res))
    if isinstance(res, list):
        out_file = os.path.join(OUT_DIR, 'movimentos_principal_20_08_2026.json')
        with open(out_file, 'w', encoding='utf-8') as f:
            json.dump(res, f, ensure_ascii=False, indent=2)
        print('Salvo em:', out_file)
        print('\n=== ÚLTIMOS 5 MOVIMENTOS DO PRINCIPAL ===')
        for m in res[:5]:
            print(f"Ordem {m.get('ordem')}: {m.get('descrMov')} em {m.get('dtMovimento')} / Juntada: {m.get('dtJuntada')}")
            for sub in m.get('movimentosExibicao', []):
                print(f"  -> {sub.get('tipoMovimento')}: {sub.get('detalhesMovimento')}")
                
    # 2. Apenso 0001140-87.2024.8.19.0078 (numero antigo 2024.078.001140-X ou busca por CNJ na api)
    res_apenso = page.evaluate('''async () => {
        try {
            const resp = await fetch('/consultaprocessual/api/processos/por-numero/movimentos', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({tipoProcesso: 1, codigoProcesso: '2024.078.001140-6', indProcVolumoso: 'N', ultimaOrdemExibida: null})
            });
            return await resp.json();
        } catch(e) {
            return {error: e.message};
        }
    }''')
    print('\nApenso - Total movimentos:', len(res_apenso) if isinstance(res_apenso, list) else type(res_apenso))
    if isinstance(res_apenso, list):
        out_file = os.path.join(OUT_DIR, 'movimentos_apenso_20_08_2026.json')
        with open(out_file, 'w', encoding='utf-8') as f:
            json.dump(res_apenso, f, ensure_ascii=False, indent=2)
        for m in res_apenso[:3]:
            print(f"Apenso Ordem {m.get('ordem')}: {m.get('descrMov')} em {m.get('dtMovimento')}")

    browser.close()
