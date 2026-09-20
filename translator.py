import asyncio
import sys
import os
from pathlib import Path
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

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

# Professional color scheme
PROF_COLORS = {
    'bg': '#F5F7FA',
    'fg': '#2D3748',
    'accent': '#4C51BF',
    'accent_hover': '#434190',
    'input_bg': '#EDF2F7',
    'input_fg': '#1A202C',
    'output_bg': '#EBF8FF',
    'output_fg': '#2B6CB0',
    'success': '#48BB78',
    'warning': '#ED8936',
    'error': '#F56565',
    'border': '#E2E8F0',
    'text_muted': '#718096'
}

class TranslatorApp:
    def __init__(self, root):
        self.root = root
        
        # Main window
        root.title("Translator - AI Translation Tool")
        root.geometry("800x600")
        root.configure(bg=PROF_COLORS['bg'])
        root.resizable(True, True)
        
        # Apply professional theme
        self._create_header()
        self._create_main_content()
        self._create_footer()
        
        # State
        self.client = None
        self.model_id = None
        self.loaded = False
        self.is_translating = False
        
    def _create_header(self):
        """Create professional header."""
        header = tk.Frame(self.root, bg=PROF_COLORS['bg'], pady=20, padx=30)
        header.pack(fill=tk.X)
        
        # Title
        title = tk.Label(
            header,
            text="Translator",
            font=("Segoe UI", 28, "bold"),
            fg=PROF_COLORS['fg'],
            bg=PROF_COLORS['bg']
        )
        title.pack()
        
        # Subtitle
        subtitle = tk.Label(
            header,
            text="Powered by QVAC | Local AI Translation",
            font=("Segoe UI", 10),
            fg=PROF_COLORS['text_muted'],
            bg=PROF_COLORS['bg']
        )
        subtitle.pack(pady=(5, 0))
    
    def _create_main_content(self):
        """Create main content area with input/output panels."""
        main = tk.Frame(self.root, bg=PROF_COLORS['bg'], padx=30, pady=20)
        main.pack(fill=tk.BOTH, expand=True)
        
        # Create canvas for scrollable area
        canvas = tk.Canvas(main, bg=PROF_COLORS['bg'], highlightthickness=0)
        scroll_y = ttk.Scrollbar(main, orient="vertical", command=canvas.yview)
        scrollable = ttk.Frame(canvas)
        
        scrollable.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable, anchor="nw")
        canvas.configure(yscrollcommand=scroll_y.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scroll_y.pack(side="right", fill="y")
        
        # Translation panel
        panel = ttk.LabelFrame(scrollable, padding=15)
        panel.pack(fill=tk.X, padx=10)
        
        # Input section
        input_frame = ttk.Frame(panel)
        input_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(
            input_frame,
            text="English Input",
            font=("Segoe UI", 11, "bold"),
            foreground=PROF_COLORS['fg']
        ).pack(anchor="w", pady=(0, 8))
        
        self.input_text = scrolledtext.ScrolledText(
            input_frame,
            height=5,
            font=("Segoe UI", 11),
            bg=PROF_COLORS['input_bg'],
            fg=PROF_COLORS['input_fg'],
            insertbackground=PROF_COLORS['input_fg'],
            relief=tk.FLAT,
            highlightthickness=2,
            highlightbackground=PROF_COLORS['border'],
            highlightcolor=PROF_COLORS['accent'],
            padx=12,
            pady=12
        )
        self.input_text.pack(fill=tk.X, pady=(0, 8))
        
        # Action buttons
        btn_frame = ttk.Frame(panel)
        btn_frame.pack(pady=5)
        
        self.translate_btn = tk.Button(
            btn_frame,
            text="Translate",
            font=("Segoe UI", 10, "bold"),
            bg=PROF_COLORS['accent'],
            fg="#FFFFFF",
            activebackground=PROF_COLORS['accent_hover'],
            activeforeground="#FFFFFF",
            relief=tk.FLAT,
            padx=30,
            pady=10,
            cursor="hand2",
            command=self.translate
        )
        self.translate_btn.pack()
        
        # Output section
        output_frame = ttk.Frame(panel)
        output_frame.pack(fill=tk.X, pady=(20, 0))
        
        ttk.Label(
            output_frame,
            text="Japanese Output",
            font=("Segoe UI", 11, "bold"),
            foreground=PROF_COLORS['fg']
        ).pack(anchor="w", pady=(0, 8))
        
        self.output_text = scrolledtext.ScrolledText(
            output_frame,
            height=5,
            font=("Segoe UI", 11),
            bg=PROF_COLORS['output_bg'],
            fg=PROF_COLORS['output_fg'],
            state=tk.DISABLED,
            relief=tk.FLAT,
            highlightthickness=2,
            highlightbackground=PROF_COLORS['border'],
            highlightcolor=PROF_COLORS['accent'],
            padx=12,
            pady=12
        )
        self.output_text.pack(fill=tk.X)
        
        # Status indicator
        self.status_frame = tk.Frame(panel, bg=PROF_COLORS['bg'])
        self.status_frame.pack(fill=tk.X, pady=(15, 0))
        
        self.status_icon = tk.Label(
            self.status_frame,
            text="⏱️",
            font=("Segoe UI", 12),
            bg=PROF_COLORS['bg']
        )
        self.status_icon.pack(side="left")
        
        self.status_text = tk.Label(
            self.status_frame,
            text="Ready - Type your text above",
            font=("Segoe UI", 10),
            fg=PROF_COLORS['text_muted'],
            bg=PROF_COLORS['bg']
        )
        self.status_text.pack(side="left", padx=(10, 0))
    
    def _create_footer(self):
        """Create professional footer."""
        footer = ttk.Frame(self.root, padding=15)
        footer.pack(fill=tk.X, side=tk.BOTTOM)
        
        ttk.Separator(footer, orient="horizontal").pack(fill="x")
        
        credits = tk.Label(
            footer,
            text="Built with QVAC SDK | On-device AI | No Cloud Calls",
            font=("Segoe UI", 9),
            fg=PROF_COLORS['text_muted'],
            bg=PROF_COLORS['bg']
        )
        credits.pack(pady=(8, 0))
    
    def _set_status(self, text, icon, color):
        """Update status indicator."""
        self.status_icon.config(text=icon)
        self.status_text.config(text=text, fg=color)
    
    def load_model(self):
        """Load the QVAC model."""
        self._set_status("Loading AI model...", "⏳", PROF_COLORS['text_muted'])
        self.translate_btn.config(state=tk.DISABLED)
        self.root.update()
        
        async def async_load():
            try:
                self._set_status("Loading AI model...", "⏳", PROF_COLORS['text_muted'])
                self.client = Client()
                await self.client.__aenter__()
                self.model_id = await load_model(
                    self.client.transport, 
                    model_src=LLAMA_3_2_1B_INST_Q4_0
                )
                self.loaded = True
                self._set_status("AI model loaded successfully! ✅", "✅", PROF_COLORS['success'])
                self.root.after(0, lambda: self.translate_btn.config(state=tk.NORMAL))
            except Exception as e:
                self._set_status(f"Error loading model: {e}", "❌", PROF_COLORS['error'])
                self.root.after(0, lambda: self.translate_btn.config(state=tk.NORMAL))
        
        asyncio.run(async_load())
    
    def translate(self):
        """Perform translation."""
        english = self.input_text.get("1.0", tk.END).strip()
        
        if not english:
            messagebox.showwarning("Input Required", "Please enter some text to translate.")
            return
        
        if self.is_translating:
            return
        
        self.is_translating = True
        self._set_status("Translating...", "⏳", PROF_COLORS['text_muted'])
        self.translate_btn.config(state=tk.DISABLED)
        
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        self.output_text.config(state=tk.DISABLED)
        
        prompt = f"""Translate the following English text to Japanese naturally and accurately.

Output ONLY the Japanese translation. Do not add any explanations, romanization, or extra text.

English text:
{english}

Japanese translation:"""
        
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
                self.root.after(0, lambda: self._set_status(f"Translation error: {e}", "❌", PROF_COLORS['error']))
            finally:
                self.is_translating = False
                self.root.after(0, lambda: self.translate_btn.config(state=tk.NORMAL))
        
        asyncio.run(async_translate())
    
    def show_output(self, text):
        """Display translation output."""
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, text)
        self.output_text.config(state=tk.DISABLED)
        self._set_status("Translation complete! ✅", "✅", PROF_COLORS['success'])
    
    def on_closing(self):
        """Handle window close."""
        if self.client:
            self.client.__aexit__(None, None, None)
        self.root.destroy()


def main():
    root = tk.Tk()
    app = TranslatorApp(root)
    
    # Setup cleanup
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    # Load model after GUI is ready
    root.after(500, app.load_model)
    
    # Start the app
    root.mainloop()


if __name__ == "__main__":
    main()
