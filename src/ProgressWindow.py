import tkinter as tk
from tkinter import ttk

class ProgressWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title(_("Fortschritt"))
        self.geometry("300x100")
        
        # Fenster in der Mitte des Hauptfensters platzieren
        self.transient(parent)
        self.grab_set()
        
        # Progressbar erstellen
        self.progress = ttk.Progressbar(
            self,
            orient="horizontal",
            length=250,
            mode="determinate"
        )
        self.progress.pack(pady=20)
        
        # Label für den Text
        self.label = ttk.Label(self, text="0%")
        self.label.pack()

    def update_progress(self, value, text):
        self.progress['value'] = value
        self.label['text'] = text
        self.update_idletasks()