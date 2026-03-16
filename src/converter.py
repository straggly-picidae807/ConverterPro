import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os

# --- PERCORSI ---
INKSCAPE_PATH = r"C:\Program Files\Inkscape\bin\inkscape.exe"
MAGICK_PATH = "magick"

class ConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Converter Pro")
        self.root.geometry("550x600")
        self.root.configure(bg="#121212")
        
        self.files_to_convert = []
        
        tk.Label(root, text="IMAGE CONVERTER PRO", fg="#00FFA3", bg="#121212", font=("Arial", 18, "bold")).pack(pady=10)

        btn_frame = tk.Frame(root, bg="#121212")
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="AGGIUNGI FILE", command=self.add_files, width=20, height=2, bg="#252526", fg="white", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="AGGIUNGI CARTELLA", command=self.add_folder, width=20, height=2, bg="#252526", fg="white", font=("Arial", 10, "bold")).grid(row=0, column=1, padx=5)

        self.listbox = tk.Listbox(root, bg="#0A0A0A", fg="#00FFA3", font=("Arial", 10), borderwidth=0, highlightthickness=1)
        self.listbox.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

        self.format_var = tk.StringVar(value="png")
        fmt_frame = tk.Frame(root, bg="#121212")
        fmt_frame.pack(pady=5)
        for fmt in [("PNG", "png"), ("ICO", "ico")]:
            tk.Radiobutton(fmt_frame, text=fmt[0], variable=self.format_var, value=fmt[1], indicatoron=0, width=12, height=2, font=("Arial", 12, "bold"), selectcolor="#00FFA3", bg="#252526", fg="white").pack(side=tk.LEFT, padx=10)

        size_frame = tk.Frame(root, bg="#121212")
        size_frame.pack(pady=10)
        tk.Label(size_frame, text="LARGHEZZA (PX):", fg="#888", bg="#121212", font=("Arial", 10, "bold")).pack(side=tk.LEFT)
        self.size_entry = tk.Entry(size_frame, width=8, font=("Arial", 14), justify='center')
        self.size_entry.insert(0, "512")
        self.size_entry.pack(side=tk.LEFT, padx=10)

        tk.Button(root, text="AVVIA CONVERSIONE", command=self.process_conversion, bg="#00FFA3", fg="black", font=("Arial", 14, "bold"), height=2).pack(pady=20, padx=20, fill=tk.X)

    def add_files(self):
        files = filedialog.askopenfilenames(filetypes=[("Immagini", "*.svg *.png *.jpg")])
        for f in files:
            self.files_to_convert.append(os.path.abspath(f))
            self.listbox.insert(tk.END, os.path.basename(f))

    def add_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            for r, d, f_list in os.walk(folder):
                for f in f_list:
                    if f.lower().endswith(('.svg', '.png', '.jpg')):
                        self.files_to_convert.append(os.path.abspath(os.path.join(r, f)))
                        self.listbox.insert(tk.END, f)

    def process_conversion(self):
        if not self.files_to_convert: return
        target = filedialog.askdirectory()
        if not target: return
        
        fmt = self.format_var.get()
        size = self.size_entry.get()
        
        for f in self.files_to_convert:
            nome_file = os.path.splitext(os.path.basename(f))[0]
            # Usiamo percorsi assoluti e normalizzati per Windows
            out_final = os.path.normpath(os.path.join(target, f"{nome_file}.{fmt}"))
            temp_png = os.path.normpath(os.path.join(os.environ['TEMP'], "temp_output.png"))

            try:
                if fmt == "png":
                    # COMANDO RINFORZATO PER INKSCAPE
                    subprocess.run([INKSCAPE_PATH, f, "--export-type=png", f"--export-width={size}", f"--export-filename={out_final}"], shell=True)
                else:
                    # PROCESSO PER ICO
                    subprocess.run([INKSCAPE_PATH, f, "--export-type=png", f"--export-width={size}", f"--export-filename={temp_png}"], shell=True)
                    subprocess.run([MAGICK_PATH, "convert", temp_png, "-define", "icon:auto-resize=256,128,64,48,32,16", out_final], shell=True)
                    if os.path.exists(temp_png): os.remove(temp_png)
            except Exception as e:
                print(f"Errore: {e}")

        if messagebox.askyesno("Fatto", "Conversione completata!\nVuoi aprire la cartella?"):
            os.startfile(target)
        
        self.files_to_convert = []
        self.listbox.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = ConverterApp(root)
    root.mainloop()