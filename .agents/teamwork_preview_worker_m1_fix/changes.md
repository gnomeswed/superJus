# Changes Applied

## File: `scripts/tjrj_scraper_auto.py`

### 1. Corrected Environment Handling Logic
- **Problem:** The previous environment handling logic forced `demo_mode` to `True` if `INTEGRITY_MODE` was `"demo"`, even if the test suite explicitly set `DEMO_MODE = "False"`.
- **Solution:** Modified the environment variable checks to respect `DEMO_MODE` first, falling back to `INTEGRITY_MODE` only if `DEMO_MODE` is not explicitly set in the environment.
- **Code Change:**
  ```python
  # Old:
  integrity_mode = os.environ.get("INTEGRITY_MODE", "demo")
  demo_mode = os.environ.get("DEMO_MODE") == "True" or integrity_mode == "demo"

  # New:
  demo_env = os.environ.get("DEMO_MODE")
  if demo_env is not None:
      demo_mode = demo_env == "True"
  else:
      demo_mode = os.environ.get("INTEGRITY_MODE", "demo") == "demo"
  ```

### 2. Wrapped Playwright Browser & Context in `try...finally` to Prevent Resource Leaks
- **Problem:** When running the scraper flow, the Chromium browser context and browser processes were not explicitly closed, potentially leaking system resources upon completion or failure.
- **Solution:** Initialized `ctx = None` and wrapped all page actions inside a `try...finally` block. In the `finally` block, we explicitly close the browser context and browser process.
- **Code Structure:**
  ```python
  with sync_playwright() as p:
      browser = p.chromium.launch(headless=True)
      ctx = None
      try:
          ctx = browser.new_context(viewport={"width": 1280, "height": 800})
          page = ctx.new_page()
          # ... scraping flow ...
      finally:
          if ctx is not None:
              ctx.close()
          browser.close()
  ```
