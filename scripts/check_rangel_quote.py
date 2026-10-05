import urllib.request
import urllib.parse
import re

url = "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote('"Paulo Rangel" "ribanceira"')
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
try:
    with urllib.request.urlopen(req, timeout=12) as r:
        html = r.read().decode("utf-8", errors="ignore")
        m = re.findall(r'<a class="result__snippet[^"]*"[^>]*>(.*?)</a>', html, re.DOTALL)
        print("Encontrados:", len(m))
        for s in m[:3]:
            print("Snippet:", re.sub(r'<.*?>', '', s).strip())
except Exception as e:
    print("Erro:", e)
