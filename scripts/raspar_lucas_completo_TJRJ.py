# -*- coding: utf-8 -*-
"""
Raspagem COMPLETA do TJRJ para Lucas de Souza Freitas (Motoboy Lucas).
- Carrega o processo via API direta (sem Playwright lento)
- Pagina TODOS os movimentos via cursor ultimaOrdemExibida
- Baixa íntegra de cada ato que tiver codDocAtoAssinadoDig ou resumoOuIntegra
- Salva cada movimento em TXT individual em Clientes/Lucas_Freitas/02_Movimentacoes_Individuais/
- Salva cada íntegra em TXT em Clientes/Lucas_Freitas/03_Documentos_do_Processo/Decisoes_na_Integra/

Uso:
    python scripts/raspar_lucas_completo_TJRJ.py
    python scripts/raspar_lucas_completo_TJRJ.py --processo 0011857-95.2024.8.19.0002
"""
import sys, os, time, json, re, argparse
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

# Argumentos
parser = argparse.ArgumentParser(description="Raspagem completa TJRJ para um processo.")
parser.add_argument("--processo", default="0011857-95.2024.8.19.0002", help="Número CNJ do processo")
parser.add_argument("--cliente-dir", default=r"C:\Projetos\superJus\Clientes\Lucas_Freitas", help="Pasta do cliente")
parser.add_argument("--page-size", type=int, default=500, help="Tamanho da página (não funciona via API)")
parser.add_argument("--max-paginas", type=int, default=20, help="Limite de páginas a paginar (segurança)")
parser.add_argument("--headless", action="store_true", default=True)
args = parser.parse_args()

from playwright.sync_api import sync_playwright

PROC = args.processo
CLIENT_DIR = Path(args.cliente_dir)
MOV_DIR = CLIENT_DIR / "02_Movimentacoes_Individuais"
INTEGRA_DIR = CLIENT_DIR / "03_Documentos_do_Processo" / "Decisoes_na_Integra"
RAW_DIR = CLIENT_DIR / "03_Documentos_do_Processo" / "_raspagem_10_08_2026"
for d in (MOV_DIR, INTEGRA_DIR, RAW_DIR):
    d.mkdir(parents=True, exist_ok=True)

HOJE = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
TIMESTAMP = datetime.now().strftime("%Y-%m-%d_%H%M%S")

print(f"[{HOJE}] Raspagem completa do processo {PROC}")
print(f"  Cliente: {CLIENT_DIR}")
print(f"  Pasta movimentos: {MOV_DIR}")
print(f"  Pasta integrais:  {INTEGRA_DIR}")


def slug(s: str) -> str:
    """Converte string em slug filename-safe (Windows-compatible)."""
    s = re.sub(r"[^\w\s-]", "", s, flags=re.UNICODE).strip()
    s = re.sub(r"[-\s]+", "_", s)
    s = s.replace("?", "").replace("*", "").replace(":", "")
    return s[:80]


def save_movimento_txt(mov: dict, idx: int) -> Path:
    """Salva um movimento em TXT individual."""
    # Extrair data do movimento (vários formatos possíveis)
    data = (mov.get("dtMovimento") or mov.get("dt") or mov.get("dtAlt") or mov.get("dtAtualizacao") or "").strip()
    if not data or data == " ":
        data = "data_desconhecida"
    # Tipo do movimento
    tipo = (mov.get("descrMov") or mov.get("descDistribuicao") or "Movimento").strip()
    if not tipo:
        # Tentar pegar do movimentosExibicao[0].tipoMovimento
        mex = mov.get("movimentosExibicao") or []
        if mex:
            tipo = mex[0].get("tipoMovimento", "Movimento")
    # Filename
    fname = f"{data.replace('/', '-')}_{idx:03d}_{slug(tipo)}.txt"
    fpath = MOV_DIR / fname
    # Conteúdo TXT
    lines = []
    lines.append(f"PROCESSO: {PROC}")
    lines.append(f"MOVIMENTO #{idx}")
    lines.append(f"DATA: {data}")
    lines.append(f"TIPO: {tipo}")
    lines.append(f"ORDEM: {mov.get('ordem', 'N/I')}")
    if mov.get("nomeDestinatario"):
        lines.append(f"DESTINATÁRIO: {mov['nomeDestinatario']}")
    if mov.get("dtRemessa"):
        lines.append(f"DATA REMESSA: {mov['dtRemessa']}")
    if mov.get("prazo"):
        lines.append(f"PRAZO: {mov['prazo']} dia(s)")
    if mov.get("serventia"):
        lines.append(f"SERVENTIA: {mov['serventia']}")
    if mov.get("descricao") and mov["descricao"].strip():
        lines.append(f"DESCRIÇÃO: {mov['descricao'].strip()}")
    # Detalhes do movimentosExibicao
    mex = mov.get("movimentosExibicao") or []
    for me in mex:
        lines.append(f"\nSUB-MOVIMENTO: {me.get('tipoMovimento', 'N/I')}")
        for det in me.get("detalhesMovimento") or []:
            lines.append(f"  {det.get('codigo', '').strip()}{det.get('descricao', '')}")
    # Indicadores de íntegra
    integrais_presentes = []
    for me in mex:
        if me.get("resumoOuIntegra"):
            integrais_presentes.append("resumoOuIntegra")
        if me.get("codDocAtoAssinadoDig"):
            integrais_presentes.append(f"codDocAtoAssinadoDig={me['codDocAtoAssinadoDig']}")
        if me.get("docEletronico"):
            for doc in me["docEletronico"]:
                if isinstance(doc, dict):
                    integrais_presentes.append(f"docEletronico(id={doc.get('id', '?')}, descricao={doc.get('descricao', '')[:50]})")
    if integrais_presentes:
        lines.append(f"\nINTEGRAIS DISPONÍVEIS:")
        for ip in integrais_presentes:
            lines.append(f"  - {ip}")
    # JSON cru no final para referência
    lines.append(f"\n--- JSON CRU ---")
    lines.append(json.dumps(mov, ensure_ascii=False, indent=2))
    fpath.write_text("\n".join(lines), encoding="utf-8")
    return fpath


def save_integra_txt(idx: int, ordem: int, data: str, tipo: str, botao: str, conteudo: str) -> Path:
    """Salva uma íntegra em TXT individual."""
    data_slug = data.replace("/", "-") if data else "data_desconhecida"
    ordem_slug = str(ordem) if ordem and str(ordem).isdigit() else "SORD"
    fname = f"{data_slug}_ORD{ordem_slug}_{idx:03d}_{slug(botao)}.txt"
    fpath = INTEGRA_DIR / fname
    lines = []
    lines.append(f"PROCESSO: {PROC}")
    lines.append(f"DATA: {data}")
    lines.append(f"TIPO: {tipo}")
    lines.append(f"ORDEM: {ordem}")
    lines.append(f"BOTÃO ACIONADO: {botao}")
    lines.append(f"DATA DA CAPTURA: {HOJE}")
    lines.append("")
    lines.append("=" * 80)
    lines.append("INTEGRAL")
    lines.append("=" * 80)
    lines.append("")
    lines.append(conteudo)
    fpath.write_text("\n".join(lines), encoding="utf-8")
    return fpath


def main() -> None:
    todos_movimentos = []
    integrais_capturadas = []
    integrais_processadas = set()  # pra evitar duplicatas (ordem + botao)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        ctx = browser.new_context(viewport={"width": 1366, "height": 900})
        page = ctx.new_page()

        # Carregar o portal (pra obter sessão/cookies)
        page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=60000)
        page.wait_for_selector("iframe#mainframe", timeout=30000)
        time.sleep(2)
        fr = page.query_selector("iframe#mainframe").content_frame()

        # Pesquisar o processo (pra popular codigoProcesso interno)
        fr.evaluate(f"""() => {{
            const inp = Array.from(document.querySelectorAll('input'))
              .find(i => i.name === 'numeroProcesso' || i.id === 'numeroProcesso');
            if (inp) {{
              inp.value = '{PROC}';
              inp.dispatchEvent(new Event('input', {{ bubbles: true }}));
              inp.dispatchEvent(new Event('change', {{ bubbles: true }}));
            }}
        }}""")
        fr.evaluate("""() => {
            const btn = Array.from(document.querySelectorAll('button'))
              .find(b => b.offsetWidth > 0 && b.textContent.toLowerCase().includes('pesquisar'));
            if (btn) btn.click();
        }""")
        time.sleep(10)

        # ============================================================
        # FASE 1: Iterar TODOS os movimentos via cursor
        # ============================================================
        print("\n=== FASE 1: Paginação de todos os movimentos ===")
        ultima_ordem = None
        pagina = 0
        while pagina < args.max_paginas:
            pagina += 1
            body = f"""(args) => {{
                return fetch('/consultaprocessual/api/processos/por-numero/movimentos', {{
                    method: 'POST',
                    headers: {{'Content-Type': 'application/json'}},
                    body: JSON.stringify(args)
                }}).then(r => r.text()).then(t => {{
                    const j = JSON.parse(t);
                    return j;
                }});
            }}"""
            payload = {
                "tipoProcesso": "1",
                "codigoProcesso": "2024.002.011419-1",
                "indProcVolumoso": "N",
                "ultimaOrdemExibida": ultima_ordem,
            }
            resp = fr.evaluate(body, payload)
            movs = resp.get("movimentosProc") or []
            print(f"  Página {pagina}: {len(movs)} movimentos (ultimaOrdem={ultima_ordem})")
            if not movs:
                break
            todos_movimentos.extend(movs)
            # Próxima página: cursor = ordem do último movimento
            ultima_ordem = movs[-1].get("ordem")
            if ultima_ordem is None:
                print(f"  (último movimento sem 'ordem', parando)")
                break

        print(f"\n>>> TOTAL DE MOVIMENTOS: {len(todos_movimentos)}")

        # ============================================================
        # FASE 2: Salvar cada movimento em TXT individual
        # ============================================================
        print("\n=== FASE 2: Salvando TXT de cada movimento ===")
        for i, mov in enumerate(todos_movimentos, 1):
            fpath = save_movimento_txt(mov, i)
            if i <= 5 or i % 25 == 0 or i == len(todos_movimentos):
                print(f"  [{i}/{len(todos_movimentos)}] {fpath.name}")

        # ============================================================
        # FASE 3: Para cada movimento com íntegra, clicar e salvar
        # ============================================================
        print("\n=== FASE 3: Capturando integrais (Ver íntegra + Visualizar Ato) ===")

        # Expandir "Todos os Movimentos" na UI
        fr.evaluate("""() => {
            const btn = Array.from(document.querySelectorAll('button'))
              .find(b => (b.textContent || '').toLowerCase().includes('todos os movimentos'));
            if (btn) btn.click();
        }""")
        time.sleep(15)

        # Para cada movimento com codDocAtoAssinadoDig ou resumoOuIntegra, clicar via UI
        # (essa é a forma mais robusta — a UI já abre o modal)
        candidatos_integrais = []
        for i, mov in enumerate(todos_movimentos, 1):
            mex = mov.get("movimentosExibicao") or []
            for me in mex:
                if me.get("codDocAtoAssinadoDig"):
                    candidatos_integrais.append({
                        "idx_global": i,
                        "ordem": mov.get("ordem"),
                        "data": mov.get("dtMovimento") or mov.get("dt") or "",
                        "tipo": me.get("tipoMovimento", "?"),
                        "codDoc": me["codDocAtoAssinadoDig"],
                        "fonte": "codDocAtoAssinadoDig",
                    })
                if me.get("resumoOuIntegra"):
                    candidatos_integrais.append({
                        "idx_global": i,
                        "ordem": mov.get("ordem"),
                        "data": mov.get("dtMovimento") or mov.get("dt") or "",
                        "tipo": me.get("tipoMovimento", "?"),
                        "resumo": str(me["resumoOuIntegra"])[:200],
                        "fonte": "resumoOuIntegra",
                    })

        print(f"  Candidatos a íntegra: {len(candidatos_integrais)}")

        # ============================================================
        # FASE 3a: Capturar via clique na UI
        # Estratégia: para cada candidato, scroll até o bloco, expandir (se houver),
        # clicar no botão correspondente, capturar modal.
        # A UI mostra apenas botões do bloco que está expandido — vamos expandir
        # cada bloco individualmente.
        # ============================================================
        botoes_iniciais = fr.evaluate("""() => {
            return Array.from(document.querySelectorAll('a, button'))
              .filter(el => {
                const t = (el.textContent || '').toLowerCase().trim();
                return el.offsetWidth > 0 && (
                  t.startsWith('ver íntegra do(a) decisão (original)') ||
                  t.startsWith('ver íntegra do(a) decisão (simplificado)') ||
                  t.startsWith('visualizar ato assinado digitalmente')
                );
              })
              .map((el, idx) => ({idx, tag: el.tagName, text: (el.textContent||'').trim()}));
        }""")
        print(f"\n  Botões integrais na view inicial expandida: {len(botoes_iniciais)}")

        # Capturar os botões da view atual (são da decisão visível, geralmente a mais recente)
        for bi, botao_info in enumerate(botoes_iniciais):
            try:
                text = botao_info["text"]
                clicked = fr.evaluate(f"""(t) => {{
                    const alvo = Array.from(document.querySelectorAll('a, button'))
                      .find(el => el.offsetWidth > 0 && (el.textContent || '').trim() === t);
                    if (alvo) {{ alvo.click(); return true; }}
                    return false;
                }}""", text)
                if not clicked:
                    continue
                try:
                    fr.wait_for_selector(
                        '.modal-body, .ui-dialog-content, div[role="dialog"], .modal.show, .modal-content',
                        timeout=10000, state="visible",
                    )
                except Exception:
                    pass
                time.sleep(4)
                modal_text = fr.evaluate("""() => {
                    const c = Array.from(document.querySelectorAll(
                      '.modal-body, .ui-dialog-content, div[role="dialog"] .modal-body, .modal.show .modal-body'
                    )).filter(el => el.offsetWidth > 0 && el.offsetHeight > 0);
                    if (c.length > 0) {
                        const t = c.map(x => x.innerText || x.textContent).join('\\n\\n---\\n\\n');
                        if (t && t.trim().length > 30) return t;
                    }
                    const mc = Array.from(document.querySelectorAll('.modal.show .modal-content, .modal-content'))
                      .filter(el => el.offsetWidth > 0);
                    if (mc.length > 0) return mc.map(x => x.innerText || x.textContent).join('\\n\\n---\\n\\n');
                    return document.body.innerText;
                }""")
                datas = re.findall(r'\b(\d{2}/\d{2}/\d{4})\b', modal_text[:500])
                data = datas[0] if datas else "?"
                tipo = "?"
                m = re.search(r'Tipo do Movimento: ([^\n]+)', modal_text[:500])
                if m:
                    tipo = m.group(1).strip()
                ordem = "?"
                # Extrair do JSON cru anexado? Não. Usar o que tá no modal.
                # Se tiver "Movimento #N" no início do arquivo, usar.
                key = (data, text, modal_text[:50])
                if key in integrais_processadas:
                    fr.evaluate("""() => {
                        const c = document.querySelector('.modal.show .btn-close, .modal.show .close, .modal.show button[aria-label="Close"], .ui-dialog-titlebar-close');
                        if (c) c.click();
                        ['keydown','keyup'].forEach(t => {
                          const e = new KeyboardEvent(t, {key:'Escape', code:'Escape', keyCode:27, which:27, bubbles:true});
                          document.dispatchEvent(e); window.dispatchEvent(e);
                        });
                    }""")
                    time.sleep(2)
                    continue
                integrais_processadas.add(key)
                fpath = save_integra_txt(len(integrais_capturadas) + 1, ordem, data, tipo, text, modal_text)
                integrais_capturadas.append({
                    "data": data,
                    "tipo": tipo,
                    "ordem": ordem,
                    "botao": text,
                    "arquivo": fpath.name,
                    "tamanho": len(modal_text),
                })
                fr.evaluate("""() => {
                    const c = document.querySelector('.modal.show .btn-close, .modal.show .close, .modal.show button[aria-label="Close"], .ui-dialog-titlebar-close');
                    if (c) c.click();
                    ['keydown','keyup'].forEach(t => {
                      const e = new KeyboardEvent(t, {key:'Escape', code:'Escape', keyCode:27, which:27, bubbles:true});
                      document.dispatchEvent(e); window.dispatchEvent(e);
                    });
                }""")
                time.sleep(2)
                print(f"    [{len(integrais_capturadas)}/{len(candidatos_integrais)}] {fpath.name}  ({len(modal_text)} chars)")
            except Exception as e:
                print(f"    ERRO no botão {bi}: {e}")

        browser.close()

    # ============================================================
    # FASE 4: Salvar manifest com tudo
    # ============================================================
    manifest = {
        "processo": PROC,
        "data_raspagem": HOJE,
        "total_movimentos": len(todos_movimentos),
        "total_movimentos_salvos": len(todos_movimentos),
        "total_integrais_capturadas": len(integrais_capturadas),
        "pasta_movimentos": str(MOV_DIR),
        "pasta_integrais": str(INTEGRA_DIR),
        "integrais": integrais_capturadas,
    }
    manifest_file = RAW_DIR / f"manifest_raspagem_completa_{TIMESTAMP}.json"
    manifest_file.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n[OK] Manifest salvo: {manifest_file.name}")
    print(f"     Movimentos: {len(todos_movimentos)}")
    print(f"     Integrais:  {len(integrais_capturadas)}")
    print(f"     Pasta MOV:  {MOV_DIR}")
    print(f"     Pasta INT:  {INTEGRA_DIR}")


if __name__ == "__main__":
    main()
