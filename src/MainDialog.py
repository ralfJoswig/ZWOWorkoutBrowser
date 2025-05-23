import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from ZwoWorkout import ZwoWorkout
from LicenseDialog import LicenseDialog
from AboutDialog import AboutDialog
from NotebookOptions import NotebookOptions
from NotebookWorkoutDetails import NotebookWorkoutDetails
from NotebookWorkoutSegments import NotebookWorkoutSegments
from NotebookWorkoutGraph import NotebookWorkoutGraph
from pathlib import Path
from ProgressWindow import ProgressWindow
from LanguageSwitcher import LanguageSwitcher
from Options import Options
from Version import Version
from tkinter import messagebox

class MainDialog:
    
    def __init__(self, root):
        self.data_notebook_list = []
        self.workout = None
        
        self.programm_titel = "ZWO-Workout-Browser"

        self.programm_titel = self.programm_titel + " " + Version.get_version()

        self.root = root
        self.root.title(self.programm_titel)
        
        self.options = Options.get_instanz()
        
        self.root.geometry('' + str(self.options.get_winfo_width()) + 'x' + str(self.options.get_winfo_height()) + '+' + str(self.options.get_winfo_x()) + '+' + str(self.options.get_winfo_y()))
        
        language_switcher = LanguageSwitcher()
        language_switcher.set_language(self.options.get_language())

        # Menüleiste hinzufügen
        self.add_menu(self.root)

        # Notebook (Tabs-Container) erstellen
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, 
                           fill='both')

        # Tab-Seite für die Segmente
        self.notebook_details = NotebookWorkoutDetails(self.notebook)
        self.notebook.add(self.notebook_details.get_notebook(), 
                          text=_("Details"))
        self.data_notebook_list.append(self.notebook_details)

        # Tab-Seite für Workoutdetails
        self.notebook_segments = NotebookWorkoutSegments(self.notebook)
        self.notebook.add(self.notebook_segments.get_notebook(), 
                          text=_("Segmente"))
        self.data_notebook_list.append(self.notebook_segments)
        
        # Tab-Seite für Grafik
        self.notebook_graphic = NotebookWorkoutGraph(self.notebook)
        self.notebook.add(self.notebook_graphic.get_notebook(),
                          text=_("Grafik"))
        self.data_notebook_list.append(self.notebook_graphic)   

        # Tab-Seite für Einstellungen
        self.notebook_options = NotebookOptions(self.notebook)
        self.notebook.add(self.notebook_options.get_notebook(), 
                          text=_("Einstellungen"))
        
        # Binding für Tab-Wechsel
        self.notebook.bind('<<NotebookTabChanged>>', 
                           self.on_tab_change)
        
    def on_tab_change(self, event):
        if self.workout is None:
            return
        for notebook in self.data_notebook_list:
            notebook.set_workout(self.workout)

    def add_menu(self, root):
        # Create menubar
        menubar = tk.Menu(root)
        root.config(menu=menubar)

        # Create File menu
        file_menu = tk.Menu(menubar, 
                            tearoff=0)
        menubar.add_cascade(label=_("Datei"), 
                            menu=file_menu)
        file_menu.add_command(label=_("Öffnen"), 
                              command=self.open_file, 
                              accelerator="Ctrl+O", 
                              underline=0)
        file_menu.add_separator()
        file_menu.add_command(label=_("Beenden"), 
                              command=self.quit)

        # Create Help menu
        help_menu = tk.Menu(menubar, 
                            tearoff=0)
        menubar.add_cascade(label=_("Hilfe"), 
                            menu=help_menu)
        help_menu.add_command(label=_("Über"),
                              command=self.show_about)
        help_menu.add_command(label=_("Lizenz anzeigen"),
                              command=self.show_license)
        
    def quit(self):
        """Beendet die Anwendung"""
        if messagebox.askokcancel(_("Beenden"), 
                              _("Möchten Sie die Anwendung wirklich schließen?")):
            Options.get_instanz().save_to_file()
            self.root.quit()

    def show_about(self):
        """Zeigt den Über-Dialog an"""
        app = AboutDialog()

    def show_license(self):
        """Zeigt die Lizenz im HTML-Viewer an"""
        app = LicenseDialog()

    def open_file(self):
        """Öffnet den Datei-Auswahl-Dialog"""
        filename = filedialog.askopenfilename(title=_("Datei auswählen"),
                                              filetypes=[(_("ZWO Files"), 
                                                          "*.zwo"),
                                                         (_("All Files"), "*.*")])
        if not filename:
            return

        p = Path(filename)
        self.root.title(f"{self.programm_titel} / {p.name}")

        progress_window = ProgressWindow(self.root)
        progress_window.update_progress(10,
                                        _("Lese Datei ein...."))

        input_file = open(filename, 'r')
        xmlstring = input_file.read()

        progress_window.update_progress(20,
                                        _("parse Datei...."))
        
        self.workout = ZwoWorkout()
        self.workout.parse(xmlstring)

        progress_window.update_progress(30,
                                        _("leite Workout weiter...."))
        # Workout an die Notebooks übergeben
        for notebook in self.data_notebook_list:
            notebook.set_workout(self.workout)
            
        progress_window.destroy()