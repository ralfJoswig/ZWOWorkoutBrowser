import tkinter as tk
from tkinter import ttk
from LanguageSwitcher import LanguageSwitcher
from Options import Options

class NotebookOptions:

    def __init__(self, root, master=None):
        options = Options.get_instanz()
                
        self.__notebook = ttk.Frame(root)
        
        self.__frame = ttk.Frame(self.__notebook)
        self.__frame.pack(fill=tk.BOTH, expand=True)

        # FTP
        ttk.Label(self.__frame, 
                  text=_("FTP")).grid(row=0, 
                                      column=0, 
                                      sticky='w', 
                                      padx=10, 
                                      pady=5)
        
        # Validierung für nur Ganzzahlen
        vcmd = (self.__frame.register(self._validate_integer),
                '%P')
        self.__ftp_var = tk.StringVar(value=options.get_ftp())
        self.__ftp_entry = ttk.Entry(self.__frame, 
                                     textvariable=self.__ftp_var, 
                                     validate='key', 
                                     validatecommand=vcmd,
                                     width=10)
        self.__ftp_entry.grid(row=0, 
                              column=1, 
                              sticky='w', 
                              padx=10, 
                              pady=5)
        self.__ftp_entry.bind("<FocusOut>", self._on_focus_out_ftp)
        
        # Min. Watt für Graphen 
        ttk.Label(self.__frame, 
                  text=_("min. Watt Grafik")).grid(row=1, 
                                                   column=0, 
                                                   sticky='w', 
                                                   padx=10, 
                                                   pady=5)
        self.__min_watt_var = tk.StringVar(value=options.get_minWatt4Grafic())
        self.__min_watt_entry = ttk.Entry(self.__frame, 
                                          textvariable=self.__min_watt_var, 
                                          validate='key', 
                                          validatecommand=vcmd,
                                          width=10)
        self.__min_watt_entry.grid(row=1, 
                                   column=1, 
                                   sticky='w', 
                                   padx=10, 
                                   pady=5)
        self.__min_watt_entry.bind("<FocusOut>", self._on_focus_out_min_watt)

        # Sprache
        ttk.Label(self.__frame, 
                  text=_("Sprache")).grid(row=2, 
                                          column=0, 
                                          sticky='w', 
                                          padx=10, 
                                          pady=5)
        # Liste der Sprachen
        sprachen = ["de", "en"]

        # Combobox (Dropdownbox) erstellen
        sprache_combobox = ttk.Combobox(self.__frame,
                                        values=sprachen, 
                                        state="readonly")
        sprache_combobox.set(options.get_language())  # Standardwert setzen
        sprache_combobox.grid(row=2,
                              column=1, 
                              sticky='w', 
                              padx=10, 
                              pady=5)

                
        # Funktion, die bei Auswahl einer Sprache aufgerufen wird
        def sprache_gewaehlt(event):
            ausgewaehlte_sprache = sprache_combobox.get()
            language_switcher = LanguageSwitcher()
            language_switcher.set_language(ausgewaehlte_sprache)
            options.set_language(ausgewaehlte_sprache)  # Sprache speichern
        
        # Event-Handler für die Auswahl
        sprache_combobox.bind("<<ComboboxSelected>>", sprache_gewaehlt)
        
    def get_notebook(self):
        return self.__notebook
    
    def _validate_integer(self, value):
        """111
        Validiert, dass nur Ganzzahlen eingegeben werden können.
        
        Args:
            value (str): Der zu prüfende Wert.
        
        Returns:
            bool: True, wenn der Wert eine gültige Ganzzahl ist.
        """
        if value == "":
            return True
        try:
            int(value)
            return True
        except ValueError:
            return False
        
    def _on_focus_out_min_watt(self, event):
        """
        Handler for the focus out event of the min watt entry.
        Updates the minimum watt value in the options.
        """
        options = Options.get_instanz()
        options.set_minWatt4Grafic(self.__min_watt_var.get())
    
    def _on_focus_out_ftp(self, event):
        options = Options.get_instanz()
        options.set_ftp(self.__ftp_var.get())