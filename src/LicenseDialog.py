import tkinter as tk
from tkhtmlview import HTMLScrolledText
from pathlib import Path
import gettext

class LicenseDialog:
    def __init__(self):
        self.root = tk.Toplevel()
        self.root.title(_("Lizenz"))
        
        # Fenstergröße und Position
        window_width = 800
        window_height = 600
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        
        self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        
        # Hauptframe
        main_frame = tk.Frame(self.root)
        main_frame.pack(expand=True, 
                        fill='both', 
                        padx=10, 
                        pady=10)
        
        # HTML-Viewer
        self.html_viewer = HTMLScrolledText(main_frame,
                                            width=80,
                                            height=30)
        self.html_viewer.pack(expand=True, 
                              fill='both')
        
        # Schließen-Button
        close_button = tk.Button(main_frame,
                                 text=_("Schließen"),
                                 command=self.root.destroy,
                                 width=20)
        close_button.pack(pady=10)
        
        # Lizenztext laden
        self.load_license()
        
    def load_license(self):
        """Lädt und zeigt den Inhalt der HTML-Lizenzdatei"""
        try:
            license_path = Path('gpl-3.0.en.html')
            with open(license_path, 'r', encoding='utf-8') as file:
                html_content = file.read()
            self.html_viewer.set_html(html_content)
            
        except FileNotFoundError:
            error_msg = "<h1>Fehler</h1><p>Die Datei 'gpl-3.0.en.html' wurde nicht gefunden.</p>"
            self.html_viewer.set_html(error_msg)
            
        except Exception as e:
            error_msg = f"<h1>Fehler</h1><p>Ein Fehler ist aufgetreten: {str(e)}</p>"
            self.html_viewer.set_html(error_msg)