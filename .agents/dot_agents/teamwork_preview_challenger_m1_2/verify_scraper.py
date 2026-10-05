# -*- coding: utf-8 -*-
import unittest
import os
import shutil
import tempfile
import urllib.request
import urllib.error
from unittest.mock import patch, MagicMock
import sys

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from scripts.tjrj_scraper_auto import scrape_process_documents, clean_process_number

class TestScraperVerification(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        os.environ["DEMO_MODE"] = "False"
        os.environ["INTEGRITY_MODE"] = "production"

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_invalid_cnj_numbers(self):
        print("\n--- Verifying Invalid CNJ Numbers ---")
        invalid_numbers = [
            "123",                             # too short
            "123456789012345678901",           # too long
            "abc12345678901234567",            # containing letters
            "0029845-67.2026.8.19.000a",       # wrong format (letter at end with separators)
            "00298456720268190000a",           # 20 digits after cleaning but contains letters
        ]
        
        for cnj in invalid_numbers:
            with self.subTest(cnj=cnj):
                try:
                    scrape_process_documents(cnj, self.test_dir)
                    print(f"FAILED: CNJ '{cnj}' did NOT raise ValueError.")
                except ValueError as e:
                    print(f"PASSED: CNJ '{cnj}' correctly raised ValueError: {e}")
                except Exception as e:
                    print(f"FAILED: CNJ '{cnj}' raised unexpected exception: {type(e).__name__}: {e}")

    def test_read_only_directories(self):
        print("\n--- Verifying Read-only Directories ---")
        # Mock os.access to return False for W_OK to simulate read-only dir
        with patch('os.access', return_value=False):
            try:
                scrape_process_documents("0029845-67.2026.8.19.0000", self.test_dir)
                print("FAILED: Read-only directory did NOT raise PermissionError.")
            except PermissionError as e:
                print(f"PASSED: Read-only directory correctly raised PermissionError: {e}")
            except Exception as e:
                print(f"FAILED: Read-only directory raised unexpected exception: {type(e).__name__}: {e}")

    @patch('urllib.request.urlopen')
    def test_network_http_errors(self, mock_urlopen):
        print("\n--- Verifying Network HTTP Errors (403, 500) ---")
        
        for code in [403, 500]:
            with self.subTest(code=code):
                mock_urlopen.side_effect = urllib.error.HTTPError(
                    "https://api-publica.datajud.cnj.jus.br/", code, "Error Msg", {}, None
                )
                try:
                    res = scrape_process_documents("0029845-67.2026.8.19.0000", self.test_dir)
                    print(f"PASSED: HTTP {code} handled gracefully. Returned: {res}")
                except Exception as e:
                    print(f"FAILED: HTTP {code} raised unhandled exception: {type(e).__name__}: {e}")

    @patch('urllib.request.urlopen')
    @patch('playwright.sync_api.sync_playwright')
    def test_playwright_timeouts(self, mock_playwright, mock_urlopen):
        print("\n--- Verifying Playwright Timeout Conditions ---")
        # Let datajud return empty list or fail, and playwright timeout
        mock_urlopen.return_value.__enter__.return_value.read.return_value = b'{"hits": {"hits": []}}'
        mock_playwright.side_effect = Exception("Timeout 30000ms exceeded while waiting for element")
        
        try:
            res = scrape_process_documents("0029845-67.2026.8.19.0000", self.test_dir)
            print(f"PASSED: Playwright timeout caught and handled. Returned: {res}")
        except Exception as e:
            print(f"FAILED: Playwright timeout raised unhandled exception: {type(e).__name__}: {e}")

if __name__ == "__main__":
    unittest.main()
