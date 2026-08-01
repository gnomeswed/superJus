# BRIEFING — 2026-07-03T16:22:00-03:00

## Mission
Propose an implementation strategy and clean architecture for scripts/tjrj_scraper_auto.py, identifying reusable logic in existing scripts and integrating a demo mode fallback.

## 🔒 My Identity
- Archetype: Explorer
- Roles: Investigator, Software Architect
- Working directory: c:\Projetos\Super Analista Jurídico\.agents\teamwork_preview_explorer_m1_1\
- Original parent: d8b46abd-3dde-490f-b620-105d1059c544
- Milestone: M1 Scraping Strategy Analysis

## 🔒 Key Constraints
- Read-only investigation — do NOT implement
- Code-only network mode (no external web scraping/requests during execution)
- Strictly follow Handoff Protocol and BRIEFING updates
- Propose clean architecture for scripts/tjrj_scraper_auto.py and write analysis.md

## Current Parent
- Conversation ID: d8b46abd-3dde-490f-b620-105d1059c544
- Updated: 2026-07-03T16:22:00-03:00

## Investigation State
- **Explored paths**:
    *   `PROJECT.md` — Contains the service contract for `scrape_process_documents`.
    *   `scripts/court_scraper.py` — Analyzed for sanitization and input validation.
    *   `scripts/tjrj_extractor.py` — Analyzed for Playwright session setups and iframe selector scripts.
    *   `Clientes/Lucas_Freitas/Caso_Principal/documentos_processo/` — Mock document folder containing 27 items.
- **Key findings**:
    *   The scraper needs to remove `ctypes.windll.user32.MessageBoxW` and run headless.
    *   Input entry and search must be automated instead of waiting on the user.
    *   In demo mode, if offline/blocked or if process number is `0011857-95.2024.8.19.0002`, the scraper must copy the 27 mock files to the target directory.
- **Unexplored areas**:
    *   Dynamic CAPTCHA solving mechanism if headless mode gets flagged in live environments.

## Key Decisions Made
- Reused sanitization from `court_scraper.py` and evaluation selectors from `tjrj_extractor.py`.
- Proposed a layered modular architecture (Orchestration, Validation, Scraper Engine, Fallback Provider, Utilities) in `analysis.md` and `handoff.md`.

## Artifact Index
- `c:\Projetos\Super Analista Jurídico\.agents\teamwork_preview_explorer_m1_1\analysis.md` — Scraping Analysis and Implementation Plan
- `c:\Projetos\Super Analista Jurídico\.agents\teamwork_preview_explorer_m1_1\handoff.md` — 5-Component Handoff Report
- `c:\Projetos\Super Analista Jurídico\.agents\teamwork_preview_explorer_m1_1\progress.md` — Heartbeat and progress update
