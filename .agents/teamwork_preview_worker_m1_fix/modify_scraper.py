# modify_scraper.py
import os

scraper_path = r"c:\Projetos\Super Analista Jurídico\scripts\tjrj_scraper_auto.py"

with open(scraper_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

output = []
in_scraping = False
start_idx = -1
end_idx = -1

# Let's locate the exact indices for run_playwright_scraping
for idx, line in enumerate(lines):
    if "def run_playwright_scraping(" in line:
        start_idx = idx
    if start_idx != -1 and "def run_fallback_lucas(" in line:
        end_idx = idx
        break

print(f"run_playwright_scraping is between lines {start_idx + 1} and {end_idx + 1}")

# We will modify the lines between start_idx and end_idx
func_lines = lines[start_idx:end_idx]

# Let's trace from "with sync_playwright() as p:"
p_line_idx = -1
for idx, line in enumerate(func_lines):
    if "with sync_playwright() as p:" in line:
        p_line_idx = idx
        break

print(f"with sync_playwright() line index relative to function: {p_line_idx}")

# Inside the function lines:
# Lines before and including:
#         ctx = browser.new_context(viewport={"width": 1280, "height": 800})
# will remain the same.
# We insert "        try:"
# Then we indent all lines starting from:
#         page = ctx.new_page()
# up to the end of the "with" block (just before the return statement).
# The return statement is at 4 spaces indentation: "    return saved_files"
# Let's find where the return statement is.
ret_line_idx = -1
for idx in range(len(func_lines) - 1, -1, -1):
    if "return saved_files" in func_lines[idx]:
        ret_line_idx = idx
        break

print(f"return saved_files line index: {ret_line_idx}")

new_func_lines = []
for idx, line in enumerate(func_lines):
    if idx < p_line_idx + 3: # Up to browser = ... and ctx = ...
        new_func_lines.append(line)
    elif idx == p_line_idx + 3: # This is page = ctx.new_page()
        new_func_lines.append("        try:\n")
        new_func_lines.append("            " + line.strip() + "\n")
    elif idx > p_line_idx + 3 and idx < ret_line_idx:
        # Indent line by 4 extra spaces if it is not empty, else keep it empty
        if line.strip():
            # Calculate current leading space
            leading = len(line) - len(line.lstrip())
            new_func_lines.append("    " + line)
        else:
            new_func_lines.append(line)
    elif idx == ret_line_idx:
        new_func_lines.append("        finally:\n")
        new_func_lines.append("            ctx.close()\n")
        new_func_lines.append("            browser.close()\n")
        new_func_lines.append("\n")
        new_func_lines.append(line)
    else:
        new_func_lines.append(line)

# Let's rebuild the file
new_lines = lines[:start_idx] + new_func_lines + lines[end_idx:]

with open(scraper_path, "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print("Scraper successfully modified!")
