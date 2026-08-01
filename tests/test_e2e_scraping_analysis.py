import unittest
import os
import re
import shutil
import tempfile
import json
import urllib.request
import urllib.error
import time
from unittest.mock import patch, MagicMock

# Ensure playwright modules are mockable even if not installed
import sys
if 'playwright' not in sys.modules:
    sys.modules['playwright'] = MagicMock()
if 'playwright.sync_api' not in sys.modules:
    playwright_mock = MagicMock()
    playwright_mock.sync_playwright = MagicMock()
    sys.modules['playwright.sync_api'] = playwright_mock

# ══════════════════════════════════════════════════════════════
# CONTRACT IMPORTS
# ══════════════════════════════════════════════════════════════
from scripts.tjrj_scraper_auto import scrape_process_documents
from scripts.process_and_timeline import generate_timeline_and_summary


# ══════════════════════════════════════════════════════════════
# MOCK HELPER CLASSES
# ══════════════════════════════════════════════════════════════
class MockResponse:
    def __init__(self, data, code=200):
        self.data = data
        self.code = code
    def read(self):
        return self.data
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

class MockElement:
    def __init__(self, text="", tag=""):
        self._text = text
        self._tag = tag
    def inner_text(self):
        return self._text
    def query_selector_all(self, selector):
        return [self]
    def closest(self, selector):
        return self
    def query_selector(self, selector):
        return self
    def fill(self, value):
        pass
    def click(self):
        pass
    def select_option(self, value):
        pass
    def wait_for_selector(self, selector, timeout=0):
        return self

class MockFrame:
    def query_selector(self, selector):
        return MockElement()
    def query_selector_all(self, selector):
        return [MockElement("original ver integra", "button")]
    def wait_for_selector(self, selector, timeout=0):
        return MockElement()
    def evaluate(self, script, *args):
        if "descricaoDetalhadaModal" in script:
            return "Depoimento do processo contendo autoria e materialidade de Lucas Freitas."
        return {"date": "03/07/2026", "tipo": "Decisao"}

class MockPage:
    def goto(self, url, **kwargs):
        pass
    def query_selector(self, selector):
        class FakeIframe:
            def content_frame(self):
                return MockFrame()
        return FakeIframe()
    def wait_for_selector(self, selector, timeout=0):
        class FakeIframe:
            def content_frame(self):
                return MockFrame()
        return FakeIframe()

class MockBrowserContext:
    def new_page(self):
        return MockPage()

class MockBrowser:
    def new_context(self, *args, **kwargs):
        return MockBrowserContext()
    def close(self):
        pass

class MockPlaywright:
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
    @property
    def chromium(self):
        class FakeChromium:
            def launch(self, *args, **kwargs):
                return MockBrowser()
        return FakeChromium()

class MockChoiceMessage:
    def __init__(self, content):
        self.content = content

class MockChoice:
    def __init__(self, content):
        self.message = MockChoiceMessage(content)

class MockCompletionsResponse:
    def __init__(self, content):
        self.choices = [MockChoice(content)]

class MockCompletions:
    def __init__(self, content):
        self.content = content
        self.last_calls = []
    def create(self, *args, **kwargs):
        self.last_calls.append(kwargs)
        return MockCompletionsResponse(self.content)

class MockChat:
    def __init__(self, content):
        self.completions = MockCompletions(content)

class MockOpenAIClient:
    def __init__(self, api_key=None, base_url=None, content="Mocked LLM Content"):
        self.chat = MockChat(content)


# ══════════════════════════════════════════════════════════════
# TEST SUITE
# ══════════════════════════════════════════════════════════════
class TestE2EScrapingAnalysis(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.original_env = os.environ.copy()
        os.environ["DEEPSEEK_API_KEY"] = "mock-key"
        os.environ["DEMO_MODE"] = "False"
        os.environ["INTEGRITY_MODE"] = "production"

    def tearDown(self):
        shutil.rmtree(self.test_dir)
        os.environ.clear()
        os.environ.update(self.original_env)

    # ══════════════════════════════════════════════════════════
    # TIER 1: FEATURE COVERAGE - SCRAPING (1-5)
    # ══════════════════════════════════════════════════════════

    @patch('urllib.request.urlopen')
    @patch('playwright.sync_api.sync_playwright')
    def test_scrape_valid_cnj_format(self, mock_playwright, mock_urlopen):
        mock_urlopen.return_value = MockResponse(b'{"hits": {"hits": [{"_source": {"classe": {"nome": "HC"}}}]}}')
        mock_playwright.return_value = MockPlaywright()
        
        files = scrape_process_documents("0029845-67.2026.8.19.0000", self.test_dir)
        self.assertTrue(len(files) > 0)
        self.assertTrue(any(f.endswith("datajud_metadata.json") for f in files))

    @patch('urllib.request.urlopen')
    def test_scrape_datajud_api_success(self, mock_urlopen):
        mock_urlopen.return_value = MockResponse(b'{"hits": {"hits": [{"_source": {"numeroProcesso": "00298456720268190000", "classe": {"nome": "Habeas Corpus"}}}]}}')
        files = scrape_process_documents("0029845-67.2026.8.19.0000", self.test_dir)
        meta_file = os.path.join(self.test_dir, "datajud_metadata.json")
        self.assertTrue(os.path.exists(meta_file))
        with open(meta_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(data["classe"]["nome"], "Habeas Corpus")

    @patch('playwright.sync_api.sync_playwright')
    def test_scrape_playwright_extraction(self, mock_playwright):
        mock_playwright.return_value = MockPlaywright()
        files = scrape_process_documents("0029845-67.2026.8.19.0000", self.test_dir)
        playwright_file = os.path.join(self.test_dir, "extracted_playwright.txt")
        self.assertTrue(os.path.exists(playwright_file))
        with open(playwright_file, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("Lucas Freitas", content)

    def test_scrape_save_dir_creation(self):
        new_dir = os.path.join(self.test_dir, "nested", "new_save_dir")
        os.environ["DEMO_MODE"] = "True"
        files = scrape_process_documents("0029845-67.2026.8.19.0000", new_dir)
        self.assertTrue(os.path.exists(new_dir))
        self.assertTrue(len(files) > 0)

    def test_scrape_demo_fallback_trigger(self):
        os.environ["DEMO_MODE"] = "True"
        files = scrape_process_documents("0029845-67.2026.8.19.0000", self.test_dir)
        self.assertTrue(any("Decisao" in f for f in files))
        self.assertTrue(any("Denuncia" in f for f in files))

    # ══════════════════════════════════════════════════════════
    # TIER 1: FEATURE COVERAGE - ANALYSIS (6-10)
    # ══════════════════════════════════════════════════════════

    @patch('openai.OpenAI')
    def test_analysis_single_txt_file(self, mock_openai):
        mock_client = MockOpenAIClient(content="Resumo de teste. Magistrado: Dr. Ronaldo")
        mock_openai.return_value = mock_client
        
        txt_file = os.path.join(self.test_dir, "doc.txt")
        with open(txt_file, "w", encoding="utf-8") as f:
            f.write("Fatos ocorridos no dia 10/05/2026.")
            
        out_report = os.path.join(self.test_dir, "report.json")
        result = generate_timeline_and_summary(txt_file, out_report)
        
        self.assertEqual(result["judge"], "Dr. Ronaldo")
        self.assertTrue(os.path.exists(out_report))

    @patch('openai.OpenAI')
    def test_analysis_single_pdf_file(self, mock_openai):
        mock_client = MockOpenAIClient(content="Resumo PDF. Magistrado: Dra. Ana")
        mock_openai.return_value = mock_client
        
        pdf_file = os.path.join(self.test_dir, "doc.pdf")
        from fpdf import FPDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", size=12)
        pdf.multi_cell(0, 10, "Denúncia oferecida em 10/05/2026. Magistrado: Dra. Ana")
        pdf.output(pdf_file)
            
        out_report = os.path.join(self.test_dir, "report.json")
        result = generate_timeline_and_summary(pdf_file, out_report)
        self.assertEqual(result["judge"], "Dra. Ana")

    @patch('openai.OpenAI')
    def test_analysis_single_html_file(self, mock_openai):
        mock_client = MockOpenAIClient(content="Resumo HTML. Magistrado: Dr. Carlos")
        mock_openai.return_value = mock_client
        
        html_file = os.path.join(self.test_dir, "doc.html")
        with open(html_file, "w", encoding="utf-8") as f:
            f.write("<html><body><p>Processo de 10/05/2026</p></body></html>")
            
        out_report = os.path.join(self.test_dir, "report.json")
        result = generate_timeline_and_summary(html_file, out_report)
        self.assertEqual(result["judge"], "Dr. Carlos")

    @patch('openai.OpenAI')
    def test_analysis_timeline_sorting(self, mock_openai):
        # We return three dates in LLM response
        mock_client = MockOpenAIClient(content="Movimentações: 15/05/2026, 02/05/2026, 10/05/2026")
        mock_openai.return_value = mock_client
        
        txt_file = os.path.join(self.test_dir, "doc.txt")
        with open(txt_file, "w", encoding="utf-8") as f:
            f.write("Processamento completo.")
            
        out_report = os.path.join(self.test_dir, "report.json")
        result = generate_timeline_and_summary(txt_file, out_report)
        
        timeline_dates = [t["date"] for t in result["timeline"]]
        self.assertEqual(timeline_dates, ["02/05/2026", "10/05/2026", "15/05/2026"])

    @patch('openai.OpenAI')
    def test_analysis_deepseek_integration(self, mock_openai):
        mock_client = MockOpenAIClient(content="Mocked LLM Content")
        mock_openai.return_value = mock_client
        
        txt_file = os.path.join(self.test_dir, "doc.txt")
        with open(txt_file, "w", encoding="utf-8") as f:
            f.write("Dados de entrada.")
            
        out_report = os.path.join(self.test_dir, "report.json")
        generate_timeline_and_summary(txt_file, out_report)
        
        # Verify client parameters
        mock_openai.assert_called_with(api_key="mock-key", base_url="https://api.deepseek.com")
        self.assertEqual(mock_client.chat.completions.last_calls[0]["model"], "deepseek-chat")
        self.assertEqual(mock_client.chat.completions.last_calls[0]["temperature"], 0.3)
        self.assertEqual(mock_client.chat.completions.last_calls[0]["max_tokens"], 2000)

    # ══════════════════════════════════════════════════════════
    # TIER 2: BOUNDARY & CORNER CASES - SCRAPING (11-15)
    # ══════════════════════════════════════════════════════════

    def test_scrape_invalid_cnj_number(self):
        with self.assertRaises(ValueError):
            scrape_process_documents("invalid-number", self.test_dir)
        with self.assertRaises(ValueError):
            scrape_process_documents("0029845-67.2026.8.19.000a", self.test_dir)

    @patch('urllib.request.urlopen')
    def test_scrape_datajud_empty_response(self, mock_urlopen):
        mock_urlopen.return_value = MockResponse(b'{"hits": {"hits": []}}')
        # We ensure it doesn't fail, but returns fallback files if empty, or handled
        # If demo mode is false and Datajud is empty, returns files extracted via other methods
        # let's verify it handles it gracefully
        files = scrape_process_documents("0029845-67.2026.8.19.0000", self.test_dir)
        self.assertTrue(isinstance(files, list))

    @patch('urllib.request.urlopen')
    def test_scrape_network_http_error(self, mock_urlopen):
        # HTTP 403 Forbidden
        req = urllib.request.Request("https://test.com")
        mock_urlopen.side_effect = urllib.error.HTTPError(
            "https://api-publica.datajud.cnj.jus.br/", 403, "Forbidden", {}, None
        )
        files = scrape_process_documents("0029845-67.2026.8.19.0000", self.test_dir)
        self.assertEqual(files, [])

    @patch('playwright.sync_api.sync_playwright')
    def test_scrape_playwright_timeout(self, mock_playwright):
        # Trigger Playwright timeout
        mock_playwright.side_effect = RuntimeError("Timeout waiting for element")
        files = scrape_process_documents("0029845-67.2026.8.19.0000", self.test_dir)
        self.assertEqual(files, [])

    def test_scrape_read_only_save_dir(self):
        # We mock save_dir path as non-writable
        with patch('os.access', return_value=False):
            with self.assertRaises(PermissionError):
                scrape_process_documents("0029845-67.2026.8.19.0000", self.test_dir)

    # ══════════════════════════════════════════════════════════
    # TIER 2: BOUNDARY & CORNER CASES - ANALYSIS (16-20)
    # ══════════════════════════════════════════════════════════

    @patch('openai.OpenAI')
    def test_analysis_huge_file_token_limit(self, mock_openai):
        mock_client = MockOpenAIClient(content="Resumo")
        mock_openai.return_value = mock_client
        
        # Write large content (120KB)
        huge_file = os.path.join(self.test_dir, "huge.txt")
        with open(huge_file, "w", encoding="utf-8") as f:
            f.write("A" * 120000)
            
        out_report = os.path.join(self.test_dir, "report.json")
        generate_timeline_and_summary(huge_file, out_report)
        
        # Assert input text in prompt was truncated
        user_prompt = mock_client.chat.completions.last_calls[0]["messages"][1]["content"]
        self.assertTrue(len(user_prompt) <= 110000)
        self.assertIn("[TRUNCATED]", user_prompt)

    @patch('openai.OpenAI')
    def test_analysis_empty_or_corrupt_files(self, mock_openai):
        mock_client = MockOpenAIClient(content="Valid process.")
        mock_openai.return_value = mock_client
        
        # 1. Empty file
        empty_file = os.path.join(self.test_dir, "empty.txt")
        open(empty_file, "w").close()
        
        # 2. Corrupt PDF file
        corrupt_pdf = os.path.join(self.test_dir, "corrupt.pdf")
        with open(corrupt_pdf, "wb") as f:
            f.write(b"not-pdf-header-corrupt-file")
            
        # 3. Valid file
        valid_file = os.path.join(self.test_dir, "valid.txt")
        with open(valid_file, "w", encoding="utf-8") as f:
            f.write("Fatos no dia 02/05/2026.")
            
        out_report = os.path.join(self.test_dir, "report.json")
        # Run analysis on the directory containing all three
        result = generate_timeline_and_summary(self.test_dir, out_report)
        # Should process without crash, ignoring corrupt/empty ones
        self.assertTrue(os.path.exists(out_report))

    def test_analysis_missing_llm_key(self):
        # Clear DeepSeek API key
        if "DEEPSEEK_API_KEY" in os.environ:
            del os.environ["DEEPSEEK_API_KEY"]
            
        txt_file = os.path.join(self.test_dir, "doc.txt")
        with open(txt_file, "w", encoding="utf-8") as f:
            f.write("Fatos no dia 12/03/2026. Juiz do caso é Dr. Pedro.")
            
        out_report = os.path.join(self.test_dir, "report.json")
        result = generate_timeline_and_summary(txt_file, out_report)
        
        # Verify heuristics kicked in
        self.assertIn("Heuristic", result["summary"])
        self.assertEqual(result["judge"], "Juiz Heurístico")
        self.assertEqual(result["timeline"][0]["date"], "12/03/2026")

    @patch('openai.OpenAI')
    def test_analysis_missing_document_metadata(self, mock_openai):
        mock_client = MockOpenAIClient(content="Documento sem nenhuma data informada.")
        mock_openai.return_value = mock_client
        
        txt_file = os.path.join(self.test_dir, "no_data.txt")
        with open(txt_file, "w", encoding="utf-8") as f:
            f.write("Apenas texto puro sem metadados e sem datas.")
            
        out_report = os.path.join(self.test_dir, "report.json")
        result = generate_timeline_and_summary(txt_file, out_report)
        self.assertEqual(result["timeline"][0]["date"], "sem_data")

    @patch('openai.OpenAI')
    def test_analysis_output_path_write_failure(self, mock_openai):
        mock_openai.return_value = MockOpenAIClient()
        txt_file = os.path.join(self.test_dir, "doc.txt")
        with open(txt_file, "w", encoding="utf-8") as f:
            f.write("Fatos.")
            
        # Unwritable output path directory
        invalid_output = "/nonexistent_directory_xxx/report.json"
        with self.assertRaises((OSError, FileNotFoundError)):
            generate_timeline_and_summary(txt_file, invalid_output)

    # ══════════════════════════════════════════════════════════
    # TIER 3: CROSS-FEATURE COMBINATIONS (21-25)
    # ══════════════════════════════════════════════════════════

    @patch('urllib.request.urlopen')
    @patch('playwright.sync_api.sync_playwright')
    @patch('openai.OpenAI')
    def test_combo_successful_scrape_to_analysis(self, mock_openai, mock_playwright, mock_urlopen):
        mock_urlopen.return_value = MockResponse(b'{"hits": {"hits": [{"_source": {"classe": {"nome": "HC"}}}]}}')
        mock_playwright.return_value = MockPlaywright()
        mock_openai.return_value = MockOpenAIClient(content="Processado. Magistrado: Dr. Marcos")
        
        # 1. Scrape
        scraped_files = scrape_process_documents("0029845-67.2026.8.19.0000", self.test_dir)
        
        # 2. Analyze
        out_report = os.path.join(self.test_dir, "timeline.json")
        result = generate_timeline_and_summary(self.test_dir, out_report)
        
        self.assertEqual(result["judge"], "Dr. Marcos")
        self.assertTrue(os.path.exists(out_report))

    @patch('openai.OpenAI')
    def test_combo_partial_scrape_to_analysis(self, mock_openai):
        mock_openai.return_value = MockOpenAIClient(content="Analise de 3 arquivos.")
        
        # Simulate scraper outputting 3 files
        for i in range(3):
            with open(os.path.join(self.test_dir, f"doc_{i}.txt"), "w", encoding="utf-8") as f:
                f.write(f"Movimento {i} em 0{i+1}/05/2026")
                
        out_report = os.path.join(self.test_dir, "report.json")
        result = generate_timeline_and_summary(self.test_dir, out_report)
        self.assertTrue(os.path.exists(out_report))

    @patch('openai.OpenAI')
    def test_combo_mixed_format_scrape_to_analysis(self, mock_openai):
        mock_openai.return_value = MockOpenAIClient(content="Integracao de formatos.")
        
        # Write TXT
        with open(os.path.join(self.test_dir, "doc1.txt"), "w", encoding="utf-8") as f:
            f.write("Fato 1: 01/05/2026")
        # Write HTML
        with open(os.path.join(self.test_dir, "doc2.html"), "w", encoding="utf-8") as f:
            f.write("<p>Fato 2: 02/05/2026</p>")
        # Write PDF
        pdf_file = os.path.join(self.test_dir, "doc3.pdf")
        from fpdf import FPDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", size=12)
        pdf.multi_cell(0, 10, "Denúncia oferecida em 10/05/2026.")
        pdf.output(pdf_file)
            
        out_report = os.path.join(self.test_dir, "report.json")
        result = generate_timeline_and_summary(self.test_dir, out_report)
        self.assertTrue(os.path.exists(out_report))

    @patch('openai.OpenAI')
    def test_combo_empty_scrape_to_analysis(self, mock_openai):
        # Clean empty directory
        empty_dir = os.path.join(self.test_dir, "empty")
        os.makedirs(empty_dir)
        
        out_report = os.path.join(self.test_dir, "report.json")
        result = generate_timeline_and_summary(empty_dir, out_report)
        self.assertEqual(result["timeline"][0]["date"], "sem_data")

    @patch('urllib.request.urlopen')
    @patch('openai.OpenAI')
    def test_combo_concurrent_scrape_and_analysis(self, mock_openai, mock_urlopen):
        mock_urlopen.return_value = MockResponse(b'{"hits": {"hits": []}}')
        mock_openai.return_value = MockOpenAIClient(content="Processado")
        
        dir1 = os.path.join(self.test_dir, "proc1")
        dir2 = os.path.join(self.test_dir, "proc2")
        
        # Run process 1
        scrape_process_documents("0029845-67.2026.8.19.0000", dir1)
        generate_timeline_and_summary(dir1, os.path.join(dir1, "report.json"))
        
        # Run process 2
        scrape_process_documents("0029845-67.2026.8.19.0000", dir2)
        generate_timeline_and_summary(dir2, os.path.join(dir2, "report.json"))
        
        # Assert directory isolation
        self.assertTrue(os.path.exists(os.path.join(dir1, "report.json")))
        self.assertTrue(os.path.exists(os.path.join(dir2, "report.json")))

    # ══════════════════════════════════════════════════════════
    # TIER 4: REAL-WORLD APPLICATION SCENARIOS (26-30)
    # ══════════════════════════════════════════════════════════

    @patch('urllib.request.urlopen')
    @patch('openai.OpenAI')
    def test_scenario_client_intake_triage(self, mock_openai, mock_urlopen):
        mock_urlopen.return_value = MockResponse(b'{"hits": {"hits": []}}')
        
        # Triage summary output from DeepSeek
        triage_md = """## 1. Resumo dos Fatos
Paciente preso em flagrante.
## 2. Possível Tipificação Criminal
Receptação - Art 180 CP.
## 3. Alertas de Nulidade ou Abuso Policial
Policial realizou busca domiciliar sem mandado.
## 4. Estratégia de Defesa Inicial Sugerida
Impetrar Habeas Corpus visando relaxamento da prisão.
"""
        mock_openai.return_value = MockOpenAIClient(content=triage_md)
        
        # Scrape and Triage
        scraped_files = scrape_process_documents("0029845-67.2026.8.19.0000", self.test_dir)
        out_report = os.path.join(self.test_dir, "triage_report.md")
        generate_timeline_and_summary(self.test_dir, out_report)
        
        self.assertTrue(os.path.exists(out_report))
        with open(out_report, "r", encoding="utf-8") as f:
            report_content = f.read()
        self.assertIn("Tipificação Criminal", report_content)
        self.assertIn("Estratégia de Defesa", report_content)

    def test_scenario_offline_demo_full_pipeline(self):
        # Enforce offline demo mode
        os.environ["DEMO_MODE"] = "True"
        if "DEEPSEEK_API_KEY" in os.environ:
            del os.environ["DEEPSEEK_API_KEY"]
            
        scraped = scrape_process_documents("0029845-67.2026.8.19.0000", self.test_dir)
        self.assertTrue(len(scraped) > 0)
        
        out_report = os.path.join(self.test_dir, "offline_timeline.json")
        result = generate_timeline_and_summary(self.test_dir, out_report)
        
        self.assertTrue(os.path.exists(out_report))
        self.assertEqual(result["judge"], "Juiz Heurístico")
        self.assertEqual(result["timeline"][0]["date"], "02/05/2026")

    @patch('openai.OpenAI')
    def test_scenario_contradiction_detection_pipeline(self, mock_openai):
        # LLM output flags a contradiction
        mock_openai.return_value = MockOpenAIClient(
            content="Contradição: Testemunha A diz que viu às 10h, Testemunha B diz que viu às 15h."
        )
        
        with open(os.path.join(self.test_dir, "depoimento1.txt"), "w", encoding="utf-8") as f:
            f.write("Depoimento A: vi o veículo às 10:00 da manhã.")
        with open(os.path.join(self.test_dir, "depoimento2.txt"), "w", encoding="utf-8") as f:
            f.write("Depoimento B: vi o veículo às 15:00 da tarde.")
            
        out_report = os.path.join(self.test_dir, "report.json")
        result = generate_timeline_and_summary(self.test_dir, out_report)
        self.assertTrue(len(result["contradictions"]) > 0)

    @patch('openai.OpenAI')
    def test_scenario_judge_profile_lawsuit_strategy(self, mock_openai):
        mock_openai.return_value = MockOpenAIClient(
            content="Magistrado: Dr. Humberto Martins. Recomendações: Focar na nulidade da busca pessoal."
        )
        
        with open(os.path.join(self.test_dir, "sentenca.txt"), "w", encoding="utf-8") as f:
            f.write("Juízo prolator: Dr. Humberto Martins")
            
        out_report = os.path.join(self.test_dir, "report.json")
        result = generate_timeline_and_summary(self.test_dir, out_report)
        self.assertEqual(result["judge"], "Dr. Humberto Martins")
        self.assertIn("Magistrado", result["summary"])

    @patch('openai.OpenAI')
    def test_scenario_high_load_chronology(self, mock_openai):
        mock_openai.return_value = MockOpenAIClient(content="Processado sob alta carga.")
        
        start_time = time.time()
        # Generate 35 document files with distinct dates
        for i in range(1, 36):
            # Dates: 01/01/2026 to 04/01/2026, cycling
            day = (i % 28) + 1
            month = (i % 12) + 1
            with open(os.path.join(self.test_dir, f"doc_{i:02d}.txt"), "w", encoding="utf-8") as f:
                f.write(f"Movimento {i} ocorrido em {day:02d}/{month:02d}/2026")
                
        out_report = os.path.join(self.test_dir, "heavy_report.json")
        result = generate_timeline_and_summary(self.test_dir, out_report)
        elapsed = time.time() - start_time
        
        # Verify correctness and budget time (must be fast under mock)
        self.assertTrue(os.path.exists(out_report))
        self.assertTrue(elapsed < 5.0)

    # ══════════════════════════════════════════════════════════
    # ADVERSARIAL TESTS - HARDENING TIER 5
    # ══════════════════════════════════════════════════════════

    def test_adversarial_filename_truncation(self):
        from scripts.tjrj_scraper_auto import _sanitize
        long_name = "Decisao_de_pronuncia_e_desclassificacao_para_outro_crime_de_competencia_de_outro_juizo_competente_e_remessa_de_autos_de_processo_criminal_longo.txt"
        sanitized = _sanitize(long_name)
        self.assertTrue(sanitized.endswith(".txt"))
        self.assertLessEqual(len(sanitized), 120)
        
        # Test that process_and_timeline reads it
        fpath = os.path.join(self.test_dir, sanitized)
        with open(fpath, "w", encoding="utf-8") as f:
            f.write("Fato ocorrido em 12/12/2025.")
            
        out_report = os.path.join(self.test_dir, "report.json")
        res = generate_timeline_and_summary(self.test_dir, out_report)
        self.assertEqual(res["timeline"][0]["date"], "12/12/2025")

    def test_adversarial_heuristic_judge_uppercase(self):
        # 1. All-caps name
        txt_file = os.path.join(self.test_dir, "doc1.txt")
        with open(txt_file, "w", encoding="utf-8") as f:
            f.write("Sentença proferida pelo Juiz de Direito DR. MARCOS SILVA na data de 12/03/2026.")
            
        if "DEEPSEEK_API_KEY" in os.environ:
            del os.environ["DEEPSEEK_API_KEY"]
            
        out_report = os.path.join(self.test_dir, "report1.json")
        res = generate_timeline_and_summary(txt_file, out_report)
        self.assertEqual(res["judge"], "MARCOS SILVA")

        # 2. Standard initials (Marcos Silva)
        txt_file2 = os.path.join(self.test_dir, "doc2.txt")
        with open(txt_file2, "w", encoding="utf-8") as f:
            f.write("Magistrado Dr. Marcos Silva determinou a busca.")
            
        out_report2 = os.path.join(self.test_dir, "report2.json")
        res2 = generate_timeline_and_summary(txt_file2, out_report2)
        self.assertEqual(res2["judge"], "Marcos Silva")

    @patch('openai.OpenAI')
    def test_adversarial_llm_judge_dot(self, mock_openai):
        mock_client = MockOpenAIClient(content="O processo foi conduzido pelo Magistrado: Dr. Ronaldo.")
        mock_openai.return_value = mock_client
        
        txt_file = os.path.join(self.test_dir, "doc.txt")
        with open(txt_file, "w", encoding="utf-8") as f:
            f.write("Conteúdo")
            
        out_report = os.path.join(self.test_dir, "report.json")
        res = generate_timeline_and_summary(txt_file, out_report)
        self.assertEqual(res["judge"], "Dr. Ronaldo")

    @patch('openai.OpenAI')
    def test_adversarial_llm_api_failure_fallback(self, mock_openai):
        # Force OpenAI to raise an exception
        mock_openai.side_effect = Exception("API is down")
        
        txt_file = os.path.join(self.test_dir, "doc.txt")
        with open(txt_file, "w", encoding="utf-8") as f:
            f.write("Magistrado Dr. Roberto de Souza proferiu despacho em 15/04/2026.")
            
        out_report = os.path.join(self.test_dir, "report.json")
        # Should not crash, should fall back to heuristic
        res = generate_timeline_and_summary(txt_file, out_report)
        self.assertEqual(res["judge"], "Roberto de Souza")
        self.assertEqual(res["timeline"][0]["date"], "15/04/2026")

    @patch('playwright.sync_api.sync_playwright')
    def test_adversarial_short_document_no_timeout(self, mock_playwright):
        class ShortMockFrame(MockFrame):
            def evaluate(self, script, *args):
                if "descricaoDetalhadaModal" in script:
                    return "Cumpra-se."  # 10 chars
                return {"date": "03/07/2026", "tipo": "Despacho"}
                
        class ShortMockPage(MockPage):
            def query_selector(self, selector):
                class FakeIframe:
                    def content_frame(self):
                        return ShortMockFrame()
                return FakeIframe()
                
        class ShortMockBrowserContext(MockBrowserContext):
            def new_page(self):
                return ShortMockPage()
                
        class ShortMockBrowser(MockBrowser):
            def new_context(self, *args, **kwargs):
                return ShortMockBrowserContext()
                
        class ShortMockPlaywright(MockPlaywright):
            @property
            def chromium(self):
                class FakeChromium:
                    def launch(self, *args, **kwargs):
                        return ShortMockBrowser()
                return FakeChromium()
                
        mock_playwright.return_value = ShortMockPlaywright()
        
        start_time = time.time()
        files = scrape_process_documents("0029845-67.2026.8.19.0000", self.test_dir)
        elapsed = time.time() - start_time
        
        # Verify it doesn't hang for 15 seconds
        self.assertLess(elapsed, 5.0)
        
        # Verify document was saved successfully
        playwright_file = os.path.join(self.test_dir, "extracted_playwright.txt")
        self.assertTrue(os.path.exists(playwright_file))
        with open(playwright_file, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("Cumpra-se.", content)

    @patch('playwright.sync_api.sync_playwright')
    def test_adversarial_consecutive_identical_documents(self, mock_playwright):
        class IdenticalMockFrame(MockFrame):
            def __init__(self):
                self.calls = 0
            def query_selector_all(self, selector):
                return [MockElement("original ver integra", "button"), MockElement("original ver integra", "button")]
            def evaluate(self, script, *args):
                if "descricaoDetalhadaModal" in script:
                    return "Mesmo conteudo"
                if "app-movimento" in script:
                    self.calls += 1
                    return {"date": "03/07/2026", "tipo": f"Decisao_{self.calls}"}
                return {}
                
        class IdenticalMockPage(MockPage):
            def query_selector(self, selector):
                class FakeIframe:
                    def content_frame(self):
                        return IdenticalMockFrame()
                return FakeIframe()
                
        class IdenticalMockBrowserContext(MockBrowserContext):
            def new_page(self):
                return IdenticalMockPage()
                
        class IdenticalMockBrowser(MockBrowser):
            def new_context(self, *args, **kwargs):
                return IdenticalMockBrowserContext()
                
        class IdenticalMockPlaywright(MockPlaywright):
            @property
            def chromium(self):
                class FakeChromium:
                    def launch(self, *args, **kwargs):
                        return IdenticalMockBrowser()
                return FakeChromium()
                
        mock_playwright.return_value = IdenticalMockPlaywright()
        
        start_time = time.time()
        files = scrape_process_documents("0029845-67.2026.8.19.0000", self.test_dir)
        elapsed = time.time() - start_time
        
        # Verify it doesn't hang for 15 seconds on the second one
        self.assertLess(elapsed, 5.0)
        
        playwright_file = os.path.join(self.test_dir, "extracted_playwright.txt")
        self.assertTrue(os.path.exists(playwright_file))
        with open(playwright_file, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("Mesmo conteudo\n\nMesmo conteudo", content)

    def test_adversarial_non_utf8_encoding(self):
        txt_file = os.path.join(self.test_dir, "doc_latin1.txt")
        content = "Juíza de Direito Dra. Cláudia proferiu a decisão em 20/06/2026."
        with open(txt_file, "w", encoding="cp1252") as f:
            f.write(content)
            
        if "DEEPSEEK_API_KEY" in os.environ:
            del os.environ["DEEPSEEK_API_KEY"]
            
        out_report = os.path.join(self.test_dir, "report.json")
        res = generate_timeline_and_summary(txt_file, out_report)
        self.assertEqual(res["judge"], "Cláudia")

    @patch('shutil.copy2')
    @patch('os.listdir')
    @patch('os.path.exists')
    def test_adversarial_playwright_fallback_lucas_errors(self, mock_exists, mock_listdir, mock_copy):
        mock_exists.return_value = True
        mock_listdir.side_effect = PermissionError("Access Denied")
        
        from scripts.tjrj_scraper_auto import run_fallback_lucas
        res = run_fallback_lucas(self.test_dir)
        self.assertEqual(res, [])

    @patch('playwright.sync_api.sync_playwright')
    def test_adversarial_playwright_form_submission_failure(self, mock_playwright):
        class FailFrame(MockFrame):
            def query_selector(self, selector):
                return None
            def evaluate(self, script, *args):
                if "submit" in script:
                    raise Exception("JS submit failed")
                return {}
                
        class FailPage(MockPage):
            def query_selector(self, selector):
                class FakeIframe:
                    def content_frame(self):
                        return FailFrame()
                return FakeIframe()
                
        class FailBrowserContext(MockBrowserContext):
            def new_page(self):
                return FailPage()
                
        class FailBrowser(MockBrowser):
            def new_context(self, *args, **kwargs):
                return FailBrowserContext()
                
        class FailPlaywright(MockPlaywright):
            @property
            def chromium(self):
                class FakeChromium:
                    def launch(self, *args, **kwargs):
                        return FailBrowser()
                return FakeChromium()
                
        mock_playwright.return_value = FailPlaywright()
        
        files = scrape_process_documents("0029845-67.2026.8.19.0000", self.test_dir)
        self.assertEqual(files, [])

    @patch('urllib.request.urlopen')
    def test_adversarial_datajud_exceptions(self, mock_urlopen):
        mock_urlopen.side_effect = urllib.error.URLError("DNS resolution failed")
        files = scrape_process_documents("0029845-67.2026.8.19.0000", self.test_dir)
        self.assertEqual(files, [])

    @patch('openai.OpenAI')
    def test_adversarial_api_token_waste_empty_content(self, mock_openai):
        empty_dir = os.path.join(self.test_dir, "empty")
        os.makedirs(empty_dir)
        
        with open(os.path.join(empty_dir, "empty.txt"), "w") as f:
            pass
            
        out_report = os.path.join(self.test_dir, "report.json")
        res = generate_timeline_and_summary(empty_dir, out_report)
        
        mock_openai.assert_not_called()
        self.assertEqual(res["timeline"][0]["date"], "sem_data")

    def test_adversarial_playwright_fallback_lucas_demo(self):
        os.environ["DEMO_MODE"] = "True"
        mock_lucas_dir = os.path.join(self.test_dir, "Lucas_Freitas_Mock")
        os.makedirs(mock_lucas_dir)
        with open(os.path.join(mock_lucas_dir, "lucas_doc1.txt"), "w") as f:
            f.write("Documento do Lucas Freitas")
            
        with patch('scripts.tjrj_scraper_auto.DEFAULT_LUCAS_MOCK_DIR', mock_lucas_dir):
            files = scrape_process_documents("0011857-95.2024.8.19.0002", self.test_dir)
            self.assertTrue(len(files) > 0)
            self.assertTrue(any(f.endswith("lucas_doc1.txt") for f in files))


if __name__ == "__main__":
    unittest.main()
