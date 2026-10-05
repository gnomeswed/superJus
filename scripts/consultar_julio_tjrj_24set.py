# -*- coding: utf-8 -*-
import sys
import json
import time
import urllib.request
import ssl

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

HEADERS_TJRJ = {
    "Content-Type": "application/json",
    "Origin": "https://www3.tjrj.jus.br",
    "Referer": "https://www3.tjrj.jus.br/consultaprocessual/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
}

URL_NUM_UNICA = "https://www3.tjrj.jus.br/consultaprocessual/api/processos/por-numeracao-unica"
URL_MOVS = "https://www3.tjrj.jus.br/consultaprocessual/api/processos/por-numero/movimentos"

procs = [
    {
        "cnj": "0023013-51.2021.8.19.0078",
        "tipo": 1,
        "cod_antigo": "2021.078.023002-1",
        "desc": "Ação Penal Principal Desmembrada - 2ª Vara de Búzios",
        "instancia": "1ª Instância"
    },
    {
        "cnj": "0001140-87.2024.8.19.0078",
        "tipo": 1,
        "cod_antigo": "2024.078.001138-0",
        "desc": "Recurso em Sentido Estrito / Apenso - Búzios",
        "instancia": "1ª Instância"
    },
    {
        "cnj": "0022975-39.2021.8.19.0078",
        "tipo": 1,
        "cod_antigo": "2021.078.022964-0",
        "desc": "Processo Originário / Co-réus - Búzios",
        "instancia": "1ª Instância"
    },
    {
        "cnj": "0029845-67.2026.8.19.0000",
        "tipo": 2,
        "cod_antigo": "2026.059.10770",
        "desc": "2ª Instância TJRJ (HC 7ª Câmara Criminal e ROC 2ª Vice-Presidência)",
        "instancia": "2ª Instância"
    }
]

print("=== CONSULTA DIRETA TJRJ ONLINE (24/09/2026) ===", flush=True)

results = {}

for p in procs:
    cnj = p["cnj"]
    tipo = p["tipo"]
    cod_antigo = p["cod_antigo"]
    print(f"\n[+] Consultando {cnj} ({p['desc']})...", flush=True)

    # Cadastro
    payload_cad = json.dumps({"tipoProcesso": str(tipo), "codigoProcesso": cnj}).encode("utf-8")
    req_cad = urllib.request.Request(URL_NUM_UNICA, data=payload_cad, headers=HEADERS_TJRJ)
    cad_info = {}
    try:
        with urllib.request.urlopen(req_cad, timeout=15, context=ctx) as r:
            res_cad = json.loads(r.read().decode("utf-8"))
            if isinstance(res_cad, list) and len(res_cad) > 0:
                cad_info = res_cad[0]
                print(f"    Classe: {cad_info.get('classe')} | Serventia: {cad_info.get('descricaoServentia')} | Fase: {cad_info.get('faseAtual', cad_info.get('ultimoMovimento'))}", flush=True)
            else:
                print(f"    Resposta cadastro vazia ou inesperada: {res_cad}", flush=True)
    except Exception as e:
        print(f"    Erro cadastro {cnj}: {e}", flush=True)

    # Movimentos
    payload_mov = json.dumps({
        "tipoProcesso": tipo,
        "codigoProcesso": cod_antigo,
        "indProcVolumoso": "N",
        "ultimaOrdemExibida": None
    }).encode("utf-8")
    req_mov = urllib.request.Request(URL_MOVS, data=payload_mov, headers=HEADERS_TJRJ)
    mov_list = []
    try:
        with urllib.request.urlopen(req_mov, timeout=20, context=ctx) as r:
            mov_raw = json.loads(r.read().decode("utf-8"))
            mov_list = mov_raw.get("movimentosProc", [])
            print(f"    Total de movimentos: {len(mov_list)}", flush=True)
            if mov_list:
                print("    --- Últimos 3 movimentos: ---", flush=True)
                for m in mov_list[:3]:
                    dt_mov = m.get('dtMovimento', m.get('dtJuntada', ''))
                    descr = m.get('descrMov', '')
                    ordem = m.get('ordem', '')
                    exibs = []
                    for ex in m.get('movimentosExibicao', []):
                        for det in ex.get('detalhesMovimento', []):
                            if isinstance(det, dict):
                                exibs.append(f"{det.get('codigo', '')}{det.get('descricao', '')}")
                            elif isinstance(det, str):
                                exibs.append(det)
                    exib_txt = f" ({'; '.join(exibs)})" if exibs else ""
                    print(f"    * [Ordem {ordem}] {dt_mov} - {descr}{exib_txt}", flush=True)
    except Exception as e:
        print(f"    Erro movimentos {cnj}: {e}", flush=True)

    results[cnj] = {
        "cad_info": cad_info,
        "total_movimentos": len(mov_list),
        "movimentos": mov_list
    }

# Save snapshot
with open(r"c:\Projetos\superJus\tmp_tjrj_24set.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("\n=== CONCLUÍDO COM SUCESSO! ===", flush=True)
