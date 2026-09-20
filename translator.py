import sys
import os
from pathlib import Path
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

SDK_PATHS = [
    Path.home() / "AppData" / "Roaming" / "npm" / "node_modules" / "@qvac" / "sdk",
    Path(r"C:\Users\kavya\AppData\Roaming\npm\node_modules\@qvac\sdk"),
]

for sdk_path in SDK_PATHS:
    if sdk_path.exists():
        os.environ["QVAC_SDK_DIR"] = str(sdk_path)
        break

try:
    from tetherto.qvac_sdk import Client, load_model, completion
    from tetherto.qvac_sdk.models import LLAMA_3_2_1B_INST_Q4_0
except ImportError as e:
    messagebox.showerror("Error", f"Cannot import QVAC SDK: {e}\n\nPlease install: npm install -g @qvac/sdk@0.19.1")
    sys.exit(1)

PROF_COLORS = {
    'bg': '#F5F7FA',
    'fg': '#2D3748',
    'accent': '#4C51BF',
    'input_bg': '#EDF2F7',
    'output_bg': '#EBF8FF',
    'text_muted': '#718096',
    'success': '#48BB78',
    'error': '#F56565'
}

class TranslatorApp:
    def __init__(self, root):
        self.root = root
        root.title("Translator - AI Translation Tool")
        root.geometry("800x600")
        root.configure(bg=PROF_COLORS['bg'])
        
        self._create_header()
        self._create_main_content()
        self._create_footer()
        
        self.client = None
        self.model_id = None
        self.loaded = False
        
    def _create_header(self):
        header = tk.Frame(self.root, bg=PROF_COLORS['bg'], pady=20, padx=30)
        header.pack(fill=tk.X)
        
        tk.Label(header, text="Translator", font=("Segoe UI", 28, "bold"), 
                 fg=PROF_COLORS['fg'], bg=PROF_COLORS['bg']).pack()
        tk.Label(header, text="Powered by QVAC | Local AI Translation", 
                 font=("Segoe UI", 10), fg=PROF_COLORS['text_muted'], 
                 bg=PROF_COLORS['bg']).pack(pady=(5, 0))
    
    def _create_main_content(self):
        main = tk.Frame(self.root, bg=PROF_COLORS['bg'], padx=30, pady=20)
        main.pack(fill=tk.BOTH, expand=True)
        
        panel = ttk.LabelFrame(main, padding=15)
        panel.pack(fill=tk.X, padx=10)
        
        input_label = tk.Label(panel, text="English Input", 
                               font=("Segoe UI", 11, "bold"), fg=PROF_COLORS['fg'])
        input_label.pack(anchor="w", pady=(0, 8))
        
        self.input_text = scrolledtext.ScrolledText(panel, height=5,
            font=("Segoe UI", 11), bg=PROF_COLORS['input_bg'], fg=PROF_COLORS['fg'],
            highlightthickness=2, highlightbackground=PROF_COLORS['text_muted'], padx=12, pady=12)
        self.input_text.pack(fill=tk.X, pady=(0, 8))
        
        self.translate_btn = tk.Button(panel, text="Translate", font=("Segoe UI", 10, "bold"),
            bg=PROF_COLORS['accent'], fg="#FFFFFF", padx=30, pady=10, cursor="hand2", command=self.translate)
        self.translate_btn.pack()
        
        output_label = tk.Label(panel, text="Japanese Output", 
                                font=("Segoe UI", 11, "bold"), fg=PROF_COLORS['fg'])
        output_label.pack(anchor="w", pady=(20, 8))
        
        self.output_text = scrolledtext.ScrolledText(panel, height=5,
            font=("Segoe UI", 11), bg=PROF_COLORS['output_bg'], fg=PROF_COLORS['fg'],
            state=tk.DISABLED, highlightthickness=2, highlightbackground=PROF_COLORS['text_muted'], padx=12, pady=12)
        self.output_text.pack(fill=tk.X)
        
        self.status = tk.Label(panel, text="Loading model...", font=("Segoe UI", 10), 
                               fg=PROF_COLORS['text_muted'], bg=PROF_COLORS['bg'])
        self.status.pack(pady=(15, 0))
    
    def _create_footer(self):
        footer = ttk.Frame(self.root, padding=15)
        footer.pack(fill=tk.X, side=tk.BOTTOM)
        ttk.Separator(footer, orient="horizontal").pack(fill="x")
        tk.Label(footer, text="Built with QVAC SDK | On-device AI | No Cloud Calls",
                 font=("Segoe UI", 9), fg=PROF_COLORS['text_muted'], bg=PROF_COLORS['bg']).pack(pady=(8, 0))
    
    def load_model(self):
        self.status.config(text="Loading AI model... Please wait...")
        self.translate_btn.config(state=tk.DISABLED)
        self.root.update()
        
        try:
            self.client = Client()
            import asyncio
            self.model_id = asyncio.run(load_model(
                self.client.transport, 
                model_src=LLAMA_3_2_1B_INST_Q4_0
            ))
            self.loaded = True
            self.status.config(text="Model loaded! Ready to translate.", fg=PROF_COLORS['success'])
            self.translate_btn.config(state=tk.NORMAL)
        except Exception as e:
            self.status.config(text=f"Error: {e}", fg=PROF_COLORS['error'])
            messagebox.showerror("Model Load Error", str(e))
    
    def translate(self):
        english = self.input_text.get("1.0", tk.END).strip()
        
        if not english:
            messagebox.showwarning("Input Required", "Please enter some text to translate.")
            return
        
        if not self.loaded:
            messagebox.showerror("Not Ready", "Model not loaded. Please wait.")
            return
        
        self.translate_btn.config(state=tk.DISABLED)
        self.status.config(text="Translating...", fg=PROF_COLORS['text_muted'])
        
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        self.output_text.config(state=tk.DISABLED)
        
        prompt = f"""Translate to Japanese. ONLY output the translation.

Examples:
- hello → こんにちは
- thank you → ありがとう

Text: {english}
Translation:"""
        
        try:
            import asyncio
            result = completion(
                self.client.transport, 
                model_id=self.model_id, 
                history=[{"role": "user", "content": prompt}]
            )
            translation = asyncio.run(result.text())
            self.output_text.config(state=tk.NORMAL)
            self.output_text.insert(tk.END, translation)
            self.output_text.config(state=tk.DISABLED)
            self.status.config(text="Translation complete!", fg=PROF_COLORS['success'])
        except Exception as e:
            self.status.config(text=f"Error: {e}", fg=PROF_COLORS['error'])
            messagebox.showerror("Translation Error", str(e))
        
        self.translate_btn.config(state=tk.NORMAL)


def main():
    root = tk.Tk()
    app = TranslatorApp(root)
    root.protocol("WM_DELETE_WINDOW", root.destroy)
    
    root.after(500, app.load_model)
    root.mainloop()


if __name__ == "__main__":
    main()
