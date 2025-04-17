import tkinter as tk
from tkhtmlview import HTMLScrolledText
from pathlib import Path

import gettext

appname = 'ZWOBroser'
localedir = Path(__file__).parent.resolve() / 'locales'
en_i18n = gettext.translation(appname, localedir, fallback=False, languages=['de'])
en_i18n.install()
_ = en_i18n.gettext

class AboutDialog:
    def __init__(self):
        self.root = tk.Toplevel()
        self.root.title(_("Über") + " ZWO-Workout-Browser")
        
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
        
        # Dialogtext setzen
        self.html_viewer.set_html("<h1>ZWO-Workout-Browser</h1><p>Version 1.0</p>")