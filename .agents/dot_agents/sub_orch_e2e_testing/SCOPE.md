# Scope: E2E Testing Track

## Architecture
- Public files:
  - `TEST_INFRA.md` (project root) - Defines the testing strategy and case inventory.
  - `TEST_READY.md` (project root) - Tells other tracks that the E2E test suite is complete, and how to run it.
- Code files:
  - `tests/test_e2e_scraping_analysis.py` - Holds all the E2E tests for the web scraping and analysis logic (Tiers 1-4).
  - A test runner or CLI commands to run the test suite.

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| 1 | Test Design & Infra | Analyze ORIGINAL_REQUEST.md and write TEST_INFRA.md | None | DONE |
| 2 | Test Implementation | Implement tests/test_e2e_scraping_analysis.py with Tiers 1-4 | Milestone 1 | DONE |
| 3 | Verification | Run and verify all E2E test cases locally | Milestone 2 | DONE |
| 4 | Finalize & Publish | Create TEST_READY.md and report to parent | Milestone 3 | DONE |

## Interface Contracts
- The test suite must run using standard python test execution tools (e.g. `python -m unittest tests/test_e2e_scraping_analysis.py` or similar).
- Features to test:
  1. Scraping: download process document (PDF/HTML) using process number, saving locally.
  2. Processing & Analysis: process downloaded document, generate timeline and summary markdown/json.
