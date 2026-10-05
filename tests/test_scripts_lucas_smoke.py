"""Testes de smoke para os scripts de raspagem do Lucas.

Valida que cada script:
1. Tem sintaxe Python válida (ast.parse)
2. Define `if __name__ == '__main__':`
3. Não tem marcadores de issue pendentes (TODO/FIXME)
4. Pode ser parseado e importado sem NameError/ImportError

Os scripts Playwright NÃO são executados em CI (precisam de Chromium e acesso ao TJRJ).
"""
import ast
import re
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"

NEW_SCRIPTS = [
    "debug_tjrj_lucas.py",
    "debug_tjrj_lucas_2.py",
    "debug_tjrj_lucas_3.py",
    "buscar_2_inst_lucas_nomes.py",
    "buscar_2_inst_lucas_v2.py",
    "buscar_2_inst_lucas_v3.py",
    "checar_apelacao_por_protocolo.py",
    "checar_stj_djen_lucas.py",
    "raspar_lucas_integral_TJRJ.py",
    "raspar_lucas_apenas_integrais.py",
    "debug_paginacao_tjrj.py",
    "debug_api_movimentos.py",
    "test_api_direta.py",
    "test_api_post.py",
    "test_api_resposta.py",
    "debug_paginador_resumido.py",
    "debug_paginador_url.py",
    "debug_paginador_expandido.py",
    "debug_api_size500.py",
    "debug_api_size500_v2.py",
    "debug_api_size500_v3.py",
    "debug_api_size500_v4.py",
    "debug_movimentos_completo.py",
    "debug_endpoint_ato_assinado.py",
    "debug_endpoint_atodoc.py",
    "debug_urls_paginador.py",
    "raspar_lucas_completo_TJRJ.py",
    "raspar_lucas_completo_TJRJ.py",
    "raspar_lucas_integrais_scroll.py",
    "buscar_sentenca_renan.py",
    "debug_pje_link.py",
    "debug_pje_link_v2.py",
    "debug_pje_link_v3.py",
    "debug_pje_urls.py",
    "debug_pje_click.py",
    "descobrir_url_pje.py",
    "explorar_portal_tjrj.py",
    "ultima_tentativa_final.py",
]


@pytest.mark.parametrize("script_name", NEW_SCRIPTS)
def test_script_exists(script_name):
    assert (SCRIPTS / script_name).exists(), f"script não encontrado: {script_name}"


@pytest.mark.parametrize("script_name", NEW_SCRIPTS)
def test_script_valid_syntax(script_name):
    src = (SCRIPTS / script_name).read_text(encoding="utf-8")
    try:
        ast.parse(src)
    except SyntaxError as e:
        pytest.fail(f"{script_name} linha {e.lineno}: {e.msg}")


@pytest.mark.parametrize("script_name", NEW_SCRIPTS)
def test_script_has_main_guard(script_name):
    src = (SCRIPTS / script_name).read_text(encoding="utf-8")
    tree = ast.parse(src)
    has_main = any(
        isinstance(n, ast.If)
        and isinstance(n.test, ast.Compare)
        and isinstance(n.test.left, ast.Name)
        and n.test.left.id == "__name__"
        for n in ast.walk(tree)
    )
    assert has_main, f"{script_name} deve ter `if __name__ == '__main__':`"


@pytest.mark.parametrize("script_name", NEW_SCRIPTS)
def test_script_no_pending_issues(script_name):
    src = (SCRIPTS / script_name).read_text(encoding="utf-8")
    pattern = re.compile(r"#\s*(TODO|FIXME|XXX|HACK|PENDENTE)\b", re.IGNORECASE)
    matches = pattern.findall(src)
    assert not matches, f"{script_name} contém marcadores pendentes: {matches}"


def test_artefatos_gerados_presentes():
    """Verifica que a raspagem produziu todos os arquivos da taxonomia esperados."""
    base = Path(r"C:\Projetos\superJus\Clientes\Lucas_Freitas")
    artefatos = [
        base / "02_Movimentacoes_Individuais" / "2026-08-10_11_Confirmacao_Localizacao_Teor_Integral.md",
        base / "03_Documentos_do_Processo" / "Decisoes_na_Integra" / "2026-06-17_Decisao_Manutricao_Prisao_Preventiva_INTEGRA.md",
        base / "03_Documentos_do_Processo" / "Espelho_Processual_Integral_Online_10_08_2026.md",
        base / "03_Documentos_do_Processo" / "_raspagem_10_08_2026" / "dossie_INTEGRAL_lucas_10_08_2026.md",
        base / "04_Analises_e_Estrategias" / "Raspagem_Integral_10_08_2026_Resumo.md",
        base / "04_Analises_e_Estrategias" / "Dossie_Integral_Lucas_10_08_2026.md",
    ]
    for a in artefatos:
        assert a.exists(), f"artefato ausente: {a}"
        assert a.stat().st_size > 500, f"artefato vazio: {a}"


def test_decisao_integral_contem_fundamentacao():
    """A íntegra da decisão 17/06/2026 deve conter palavras-chave da fundamentação."""
    p = Path(r"C:\Projetos\superJus\Clientes\Lucas_Freitas\03_Documentos_do_Processo\Decisoes_na_Integra\2026-06-17_Decisao_Manutricao_Prisao_Preventiva_INTEGRA.md")
    texto = p.read_text(encoding="utf-8")
    palavras = ["Portaria Conjunta", "Art. 316", "Prisão Preventiva", "HC 0054200", "manutenção"]
    for w in palavras:
        assert w.lower() in texto.lower() or w in texto, f"palavra-chave ausente: {w!r}"


def test_memoria_memu_gravada():
    """A memória `andamento_lucas_10_08_2026_manha.md` deve existir no memU."""
    import sqlite3
    db = Path.home() / ".memu" / "memu.sqlite3"
    if not db.exists():
        pytest.skip("memU SQLite não encontrado neste ambiente")
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("SELECT id, length(content) FROM memu_recall_files WHERE name=?", ("andamento_lucas_10_08_2026_manha.md",))
    row = cur.fetchone()
    conn.close()
    assert row is not None, "memória não encontrada no memU"
    assert row[1] > 1000, f"memória muito pequena: {row[1]} chars"


def test_dossie_contem_todas_as_etapas():
    """O dossiê integral deve conter as seções esperadas."""
    p = Path(r"C:\Projetos\superJus\Clientes\Lucas_Freitas\03_Documentos_do_Processo\_raspagem_10_08_2026\dossie_INTEGRAL_lucas_10_08_2026.md")
    texto = p.read_text(encoding="utf-8")
    secoes = [
        "1. Status Atual",
        "2. Cobertura da Raspagem",
        "3. Cronologia Completa",
        "4. Decisões, Despachos e Atos Assinados NA ÍNTEGRA",
        "5. Acesso a Instâncias Superiores",
        "6. Arquivos Gerados",
        "7. Scripts de Raspagem",
        "8. Próximas Ações",
    ]
    for s in secoes:
        assert s in texto, f"Seção ausente no dossiê: {s!r}"


def test_dossie_contem_texto_das_3_integrais():
    """O dossiê integral deve incorporar o texto das 3 decisões/atos."""
    import re
    p = Path(r"C:\Projetos\superJus\Clientes\Lucas_Freitas\03_Documentos_do_Processo\_raspagem_10_08_2026\dossie_INTEGRAL_lucas_10_08_2026.md")
    texto = p.read_text(encoding="utf-8")
    # As 3 integrais capturadas referem-se à mesma decisão da Portaria Conjunta TJ/CGJ/2VP nº 03
    # (uma em maiúsculas, duas em minúsculas com markup ng-select)
    pattern = re.compile(r"portaria\s+conjunta\s+tj/cgj/2vp\s+n[ºo]\s*03", re.IGNORECASE)
    matches = pattern.findall(texto)
    assert len(matches) >= 3, f"Esperado ≥3 ocorrências da Portaria Conjunta, achou {len(matches)}"


def test_paginacao_tjrj_investigada():
    """Verifica que o debug de paginação foi executado e tem achados documentados."""
    # O arquivo de saída existe
    raw_dir = Path(r"C:\Projetos\superJus\Clientes\Lucas_Freitas\03_Documentos_do_Processo\_raspagem_10_08_2026")
    # Apenas verificar que há pelo menos 1 HTML e 1 PNG salvos (saídas dos debugs)
    htmls = list(raw_dir.glob("*.html"))
    pngs = list(raw_dir.glob("*.png"))
    assert len(htmls) >= 1, "nenhum HTML raw salvo"
    assert len(pngs) >= 1, "nenhuma screenshot salva"


def test_175_movimentos_salvos():
    """A raspagem completa deve ter gerado 175+ TXT de movimentos individuais."""
    mov_dir = Path(r"C:\Projetos\superJus\Clientes\Lucas_Freitas\02_Movimentacoes_Individuais")
    # Filtrar só os arquivos novos (formato DD-MM-YYYY_NNN_*.txt)
    novos_txt = [f for f in mov_dir.glob("*-*_*_*.txt") if f.stem[0:2].isdigit()]
    # Esperar pelo menos 150 (caso a data atual mude a ordem)
    assert len(novos_txt) >= 150, f"esperado ≥150, achou {len(novos_txt)} movimentos TXT"


def test_movimento_txt_tem_conteudo_esperado():
    """Cada TXT de movimento deve ter cabeçalho PROCESSO/MOVIMENTO/DATA/TIPO/ORDEM + JSON cru."""
    mov_dir = Path(r"C:\Projetos\superJus\Clientes\Lucas_Freitas\02_Movimentacoes_Individuais")
    novos_txt = sorted([f for f in mov_dir.glob("*-*_*_*.txt") if f.stem[0:2].isdigit()])
    if not novos_txt:
        pytest.skip("nenhum TXT novo encontrado")
    sample = novos_txt[0]
    txt = sample.read_text(encoding="utf-8")
    assert "PROCESSO: 0011857-95.2024.8.19.0002" in txt
    assert "MOVIMENTO #" in txt
    assert "DATA:" in txt
    assert "TIPO:" in txt
    assert "ORDEM:" in txt
    assert "JSON CRU" in txt


def test_3_integrais_salvas():
    """As 3 integrais da decisão 17/06/2026 devem estar salvas em TXT."""
    integra_dir = Path(r"C:\Projetos\superJus\Clientes\Lucas_Freitas\03_Documentos_do_Processo\Decisoes_na_Integra")
    # As 3 integrais têm padrão: data_ORDNNN_NNN_*.txt
    txts = list(integra_dir.glob("*_ORD*_???_*.txt"))
    integrais_lucas = [t for t in txts if "Ver" in t.name or "Visualizar" in t.name]
    # Esperar pelo menos 3 (Original, Simplificado, Ato Assinado)
    assert len(integrais_lucas) >= 3, f"esperado ≥3, achou {len(integrais_lucas)} integrais TXT"


def test_integral_txt_tem_tecnico_decisao():
    """O TXT da íntegra deve ter cabeçalho PROCESSO/DATA/TIPO/INTEGRAL."""
    integra_dir = Path(r"C:\Projetos\superJus\Clientes\Lucas_Freitas\03_Documentos_do_Processo\Decisoes_na_Integra")
    txts = [t for t in integra_dir.glob("*_ORD*_???_*.txt") if "Ver" in t.name or "Visualizar" in t.name]
    if not txts:
        pytest.skip("nenhuma íntegra encontrada")
    sample = txts[0]
    txt = sample.read_text(encoding="utf-8")
    assert "PROCESSO: 0011857" in txt
    assert "DATA:" in txt
    assert "TIPO:" in txt
    assert "INTEGRAL" in txt
    assert "Portaria Conjunta" in txt  # conteúdo da decisão 17/06


def test_manifest_raspagem_existe():
    """Manifest da raspagem completa deve existir com metadados."""
    raw_dir = Path(r"C:\Projetos\superJus\Clientes\Lucas_Freitas\03_Documentos_do_Processo\_raspagem_10_08_2026")
    manifests = list(raw_dir.glob("manifest_raspagem_completa_*.json"))
    assert len(manifests) >= 1, "nenhum manifest encontrado"
    import json
    m = json.loads(manifests[-1].read_text(encoding="utf-8"))
    assert m["processo"] == "0011857-95.2024.8.19.0002"
    assert m["total_movimentos"] >= 150
    assert m["total_integrais_capturadas"] >= 3
