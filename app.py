import asyncio
import sys
import os
from pathlib import Path
import tkinter as tk
from tkinter import ttk, scrolledtext

# Try to find QVAC SDK automatically
SDK_PATHS = [
    Path.home() / "AppData" / "Roaming" / "npm" / "node_modules" / "@qvac" / "sdk",
    Path(r"C:\Users\kavya\AppData\Roaming\npm\node_modules\@qvac\sdk"),
]

for sdk_path in SDK_PATHS:
    if sdk_path.exists():
        os.environ["QVAC_SDK_DIR"] = str(sdk_path)
        break

from tetherto.qvac_sdk import Client, load_model, completion
from tetherto.qvac_sdk.models import LLAMA_3_2_1B_INST_Q4_0

class TranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Translator - QVAC")
        self.root.geometry("700x500")
        self.root.minsize(600, 400)
        
        # Set dark theme
        self.root.configure(bg="#1e1e2e")
        
        # Title
        title_frame = tk.Frame(root, bg="#1e1e2e")
        title_frame.pack(pady=10)
        
        title_label = tk.Label(
            title_frame, 
            text="🔤 Translator", 
            font=("Segoe UI", 20, "bold"),
            fg="#89b4fa", 
            bg="#1e1e2e"
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            title_frame,
            text="English → Japanese (Powered by QVAC)",
            font=("Segoe UI", 10),
            fg="#a6adc8",
            bg="#1e1e2e"
        )
        subtitle_label.pack()
        
        # Create main frame with padding
        main_frame = tk.Frame(root, bg="#1e1e2e", padx=20, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Input frame
        input_frame = tk.LabelFrame(
            main_frame, 
            text=" English Input ", 
            font=("Segoe UI", 10, "bold"),
            fg="#a6e3a1",
            bg="#1e1e2e",
            padx=10,
            pady=10
        )
        input_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.input_text = scrolledtext.ScrolledText(
            input_frame, 
            height=6,
            font=("Segoe UI", 11),
            bg="#313244",
            fg="#cdd6f4",
            insertbackground="#cdd6f4",
            relief=tk.FLAT,
            padx=10,
            pady=10
        )
        self.input_text.pack(fill=tk.BOTH, expand=True)
        
        # Button frame
        btn_frame = tk.Frame(main_frame, bg="#1e1e2e", pady=10)
        btn_frame.pack(fill=tk.X)
        
        self.translate_btn = tk.Button(
            btn_frame,
            text="🌏 Translate",
            font=("Segoe UI", 12, "bold"),
            bg="#89b4fa",
            fg="#11111b",
            activebackground="#b4befe",
            activeforeground="#11111b",
            relief=tk.FLAT,
            padx=20,
            pady=8,
            cursor="hand2",
            command=self.translate
        )
        self.translate_btn.pack()
        
        # Output frame
        output_frame = tk.LabelFrame(
            main_frame, 
            text=" 🎌 Japanese Output ", 
            font=("Segoe UI", 10, "bold"),
            fg="#f38ba8",
            bg="#1e1e2e",
            padx=10,
            pady=10
        )
        output_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.output_text = scrolledtext.ScrolledText(
            output_frame, 
            height=6,
            font=("Segoe UI", 11),
            bg="#313244",
            fg="#cdd6f4",
            state=tk.DISABLED,
            relief=tk.FLAT,
            padx=10,
            pady=10
        )
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        # Status bar
        self.status = tk.Label(
            root, 
            text="Ready - Type English above and click Translate", 
            font=("Segoe UI", 9),
            fg="#9399b2",
            bg="#11111b",
            anchor=tk.W,
            padx=10
        )
        self.status.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.client = None
        self.model_id = None
        self.loaded = False
        
    def load_model(self):
        self.status.config(text="Loading model... Please wait...")
        self.root.update()
        
        async def async_load():
            try:
                self.client = Client()
                await self.client.__aenter__()
                self.model_id = await load_model(
                    self.client.transport, 
                    model_src=LLAMA_3_2_1B_INST_Q4_0
                )
                self.loaded = True
                self.status.config(text="Model loaded! Ready to translate.")
                self.root.after(0, lambda: self.translate_btn.config(state=tk.NORMAL))
            except Exception as e:
                self.status.config(text=f"Error loading model: {e}")
                self.root.after(0, lambda: self.translate_btn.config(state=tk.NORMAL))
        
        asyncio.run(async_load())
    
    def translate(self):
        english = self.input_text.get("1.0", tk.END).strip()
        
        if not english:
            self.status.config(text="Please enter some text to translate")
            return
        
        self.translate_btn.config(state=tk.DISABLED)
        self.status.config(text="Translating...")
        
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        self.output_text.config(state=tk.DISABLED)
        
        prompt = f"""Translate English to Japanese naturally. Output ONLY the Japanese translation.

Examples:
- hello → こんにちは
- thank you → ありがとう

Text: {english}
Translation:"""
        
        async def async_translate():
            try:
                result = completion(
                    self.client.transport, 
                    model_id=self.model_id, 
                    history=[{"role": "user", "content": prompt}]
                )
                translation = await result.text()
                self.root.after(0, lambda: self.show_output(translation))
            except Exception as e:
                self.root.after(0, lambda: self.status.config(text=f"Error: {e}"))
            finally:
                self.root.after(0, lambda: self.translate_btn.config(state=tk.NORMAL))
        
        asyncio.run(async_translate())
    
    def show_output(self, text):
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, text)
        self.output_text.config(state=tk.DISABLED)
        self.status.config(text="Translation complete!")


def main():
    root = tk.Tk()
    app = TranslatorApp(root)
    
    def on_closing():
        if app.client:
            app.client.__aexit__(None, None, None)
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    app.load_model()
    root.mainloop()


if __name__ == "__main__":
    main()
