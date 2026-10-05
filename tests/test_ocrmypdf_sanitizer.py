# -*- coding: utf-8 -*-
"""
Testes unitários e de integração para o pipeline de OCRmyPDF do SuperJus.
Valida detecção de PDFs escaneados, execução de OCR em português,
preservação de layout, criação de backups e relatórios.
"""

import os
import shutil
import tempfile
import pytest
from PIL import Image, ImageDraw

from scripts.ocrmypdf_sanitizer import (
    setup_tesseract_environment,
    analyze_pdf,
    OCRSanitizer,
    generate_reports,
)


@pytest.fixture
def temp_workspace():
    tmp_dir = tempfile.mkdtemp(prefix="superjus_ocr_test_")
    yield tmp_dir
    shutil.rmtree(tmp_dir, ignore_errors=True)


def test_tesseract_environment():
    """Verifica se Tesseract, idioma português e OCRmyPDF estão devidamente configurados."""
    env = setup_tesseract_environment()
    assert env["tesseract_found"] is True, "Tesseract não foi localizado no Windows."
    assert env["has_por"] is True, "Idioma português (por) não disponível no Tesseract."
    assert env["ocrmypdf_available"] is True, "OCRmyPDF não está disponível."
    assert env["pytesseract_available"] is True, "PyTesseract não está disponível."


def test_analyze_pure_scan_vs_text_pdf(temp_workspace):
    """Testa a classificação precisa entre PDF escaneado (imagem pura) e digital com texto."""
    # 1. Gerar PDF escaneado (imagem pura, sem texto vetorial)
    img = Image.new("RGB", (800, 600), color="white")
    draw = ImageDraw.Draw(img)
    draw.text((50, 50), "POLICIA CIVIL DO ESTADO DO RIO DE JANEIRO", fill="black")
    draw.text((50, 90), "INQUERITO POLICIAL N. 0023013-51.2021.8.19.0078", fill="black")
    draw.text((50, 130), "DEPOIMENTO DE TESTEMUNHA ESCRIVAO CARIMBO PROTOCOLO", fill="black")

    scanned_pdf_path = os.path.join(temp_workspace, "inquerito_escaneado.pdf")
    img.save(scanned_pdf_path, "PDF", resolution=150.0)

    analysis_scanned = analyze_pdf(scanned_pdf_path, threshold_chars_per_page=40)
    assert analysis_scanned["classification"] == "PURE_SCAN"
    assert analysis_scanned["needs_ocr"] is True
    assert analysis_scanned["pages_with_text"] == 0
    assert analysis_scanned["total_chars"] == 0

    # 2. Executar OCR e verificar se vira pesquisável preservando integridade
    sanitizer = OCRSanitizer(language="por", create_backup=True)
    res = sanitizer.process_file(scanned_pdf_path, dry_run=False)

    assert res["status"] == "SUCCESS"
    assert res["chars_after"] > 50
    assert res["chars_added"] > 50
    assert res["backup_path"] is not None
    assert os.path.isfile(res["backup_path"])

    # 3. Reanalisar o PDF processado - agora deve ser ALREADY_SEARCHABLE
    analysis_after = analyze_pdf(scanned_pdf_path, threshold_chars_per_page=40)
    assert analysis_after["classification"] == "ALREADY_SEARCHABLE"
    assert analysis_after["needs_ocr"] is False
    assert analysis_after["pages_with_text"] == 1


def test_reports_generation(temp_workspace):
    """Valida a geração de relatórios JSON e Markdown."""
    env = setup_tesseract_environment()
    dummy_results = [
        {
            "file_path": "teste1.pdf",
            "file_name": "teste1.pdf",
            "relative_path": "Cliente_A/teste1.pdf",
            "status": "SUCCESS",
            "classification": "PURE_SCAN",
            "chars_before": 0,
            "chars_after": 250,
            "chars_added": 250,
            "total_pages": 1,
            "duration_seconds": 1.2,
        },
        {
            "file_path": "teste2.pdf",
            "file_name": "teste2.pdf",
            "relative_path": "Cliente_B/teste2.pdf",
            "status": "ALREADY_SEARCHABLE",
            "classification": "ALREADY_SEARCHABLE",
            "chars_before": 1500,
            "chars_after": 1500,
            "chars_added": 0,
            "total_pages": 2,
            "duration_seconds": 0.1,
        },
    ]

    report_dir = os.path.join(temp_workspace, "relatorios")
    json_path, md_path = generate_reports(dummy_results, env, report_dir, dry_run=False)

    assert os.path.isfile(json_path)
    assert os.path.isfile(md_path)

    with open(md_path, "r", encoding="utf-8") as f:
        md_text = f.read()
        assert "Relatório de OCR Automatizado" in md_text
        assert "Cliente_A/teste1.pdf" in md_text
        assert "PURE_SCAN" in md_text
