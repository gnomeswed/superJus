## Challenge Summary

**Overall risk assessment**: LOW

## Challenges

### [Low] Challenge 1: Live TJRJ Portal Changes

- Assumption challenged: Stability of TJRJ public portal page structure and HTML selectors.
- Attack scenario: TJRJ upgrades their portal, changing selectors like `iframe#mainframe` or `.mostrar-todos`.
- Blast radius: Playwright automated scraping fails to locate elements, returning an empty list of documents.
- Mitigation: The implementation includes an offline `DEMO_MODE` fallback and logs the failure gracefully, ensuring the application doesn't crash.

### [Low] Challenge 2: DeepSeek API Outage

- Assumption challenged: Constant availability of DeepSeek API.
- Attack scenario: DeepSeek is down or the network is blocked.
- Blast radius: AI-based timeline analysis throws an exception.
- Mitigation: Code catches exceptions and falls back to a robust heuristic regex parser (`_read_file_content` -> date extraction -> judge regex matching).

## Stress Test Results

- Empty files input -> Checked if the parser crashes -> Ignored correctly -> PASS
- Non-UTF-8 CP1252 encoded document -> Checked if the decoder fails ->cp1252 fallback loads it -> PASS
- String truncation -> Input > 100KB -> Truncated to 100KB with `[TRUNCATED]` suffix -> PASS

## Unchallenged Areas

- Live Captcha handling — reason not challenged: Requires manual captcha resolution or advanced AI solver, which is outside the scope of simple automated scraping flow.
