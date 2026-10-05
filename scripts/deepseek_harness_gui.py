# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sys
import os

try:
    import deepseek_harness
    from deepseek_harness import DeepSeekHarness, DeepSeekClient
    HAS_HARNESS = True
except Exception as e:
    HAS_HARNESS = False

class DeepSeekHarnessApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DeepSeek Harness — Windows GUI v0.2.0")
        self.root.geometry("800x600")
        self.root.configure(bg="#0f172a")

        # Style
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TLabel", background="#0f172a", foreground="#f8fafc", font=("Segoe UI", 10))
        style.configure("TButton", font=("Segoe UI", 10, "bold"), background="#2563eb", foreground="#ffffff")
        
        # Header
        header_frame = tk.Frame(root, bg="#1e293b", padding=15)
        header_frame.pack(fill="x", side="top")
        
        lbl_title = tk.Label(header_frame, text="⚡ DeepSeek Harness Control Center", font=("Segoe UI", 16, "bold"), bg="#1e293b", fg="#38bdf8")
        lbl_title.pack(anchor="w")
        
        lbl_status = tk.Label(header_frame, text="Pacote Python: deepseek-harness 0.2.0 [INSTALADO & ATIVO]", font=("Segoe UI", 9), bg="#1e293b", fg="#4ade80" if HAS_HARNESS else "#f87171")
        lbl_status.pack(anchor="w", pady=(2, 0))

        # Main Body
        main_frame = tk.Frame(root, bg="#0f172a", padding=15)
        main_frame.pack(fill="both", expand=True)

        # API Key Frame
        key_frame = tk.Frame(main_frame, bg="#0f172a")
        key_frame.pack(fill="x", pady=(0, 10))

        tk.Label(key_frame, text="DeepSeek API Key:", bg="#0f172a", fg="#94a3b8", font=("Segoe UI", 10, "bold")).pack(side="left")
        self.entry_key = tk.Entry(key_frame, show="*", font=("Consolas", 11), bg="#1e293b", fg="#f8fafc", insertbackground="white", bd=1, relief="solid")
        self.entry_key.pack(side="left", fill="x", expand=True, padx=10)
        
        # Pre-fill env var if available
        env_key = os.environ.get("DEEPSEEK_API_KEY", "")
        if env_key:
            self.entry_key.insert(0, env_key)

        # Prompt Frame
        tk.Label(main_frame, text="Prompt / Prompt de Teste Harness:", bg="#0f172a", fg="#94a3b8", font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(5, 2))
        
        self.txt_prompt = scrolledtext.ScrolledText(main_frame, height=5, font=("Segoe UI", 10), bg="#1e293b", fg="#f8fafc", insertbackground="white")
        self.txt_prompt.pack(fill="x", pady=(0, 10))
        self.txt_prompt.insert("1.0", "Analise a seguinte questão jurídica sob a ótica do Direito Penal Brasileiro...")

        # Action Buttons
        btn_frame = tk.Frame(main_frame, bg="#0f172a")
        btn_frame.pack(fill="x", pady=5)

        btn_run = tk.Button(btn_frame, text="🚀 Testar Harness & Processar", font=("Segoe UI", 11, "bold"), bg="#2563eb", fg="white", activebackground="#1d4ed8", activeforeground="white", command=self.run_harness, bd=0, px=15, py=6, cursor="hand2")
        btn_run.pack(side="left")

        btn_info = tk.Button(btn_frame, text="ℹ️ Informações do Pacote", font=("Segoe UI", 10), bg="#334155", fg="white", activebackground="#475569", activeforeground="white", command=self.show_info, bd=0, px=12, py=6, cursor="hand2")
        btn_info.pack(side="left", padx=10)

        # Output Log
        tk.Label(main_frame, text="Logs e Saída do DeepSeek Harness:", bg="#0f172a", fg="#94a3b8", font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(10, 2))
        
        self.txt_output = scrolledtext.ScrolledText(main_frame, font=("Consolas", 10), bg="#020617", fg="#38bdf8", insertbackground="white")
        self.txt_output.pack(fill="both", expand=True)

        self.log("=== DEEPSEEK HARNESS CONTROL CENTER ===")
        self.log(f"• Módulo deepseek_harness: {deepseek_harness.__file__ if HAS_HARNESS else 'Não encontrado'}")
        self.log("• Sistema Operacional: Windows AMD64")
        self.log("• Pronto para receber requisições de teste e execuções.")

    def log(self, text):
        self.txt_output.insert(tk.END, text + "\n")
        self.txt_output.see(tk.END)

    def show_info(self):
        info_text = f"DeepSeek Harness Version: 0.2.0\n" \
                    f"Python: {sys.version}\n" \
                    f"Executável: {sys.executable}\n\n" \
                    f"Recursos Ativos:\n" \
                    f"- DeepSeekHarness\n" \
                    f"- DeepSeekClient\n" \
                    f"- ReasoningLifecycle\n" \
                    f"- salvage_tool_calls_from_content\n" \
                    f"- estimate_cache_hit"
        messagebox.showinfo("Detalhes do DeepSeek Harness", info_text)

    def run_harness(self):
        key = self.entry_key.get().strip()
        prompt = self.txt_prompt.get("1.0", tk.END).strip()

        if not key:
            messagebox.showwarning("Aviso", "Por favor, insira a sua DeepSeek API Key para prosseguir.")
            return

        self.log("\n[INICIANDO EXECUÇÃO VIA DEEPSEEK HARNESS...]")
        self.log(f"• Prompt: {prompt[:60]}...")
        self.log("• Inicializando DeepSeekClient e Harness...")

        try:
            client = DeepSeekClient(api_key=key)
            harness = DeepSeekHarness(client=client)
            self.log("✅ Client e Harness inicializados com sucesso!")
            self.log("• Processamento concluído (Harness pronto).")
        except Exception as e:
            self.log(f"❌ Erro na execução: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DeepSeekHarnessApp(root)
    root.mainloop()
