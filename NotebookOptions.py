import tkinter as tk
from tkinter import ttk

class NotebookOptions:

    def __init__(self, root, master=None):
        self.__notebook = ttk.Frame(root)
        
        self.__frame = ttk.Frame(self.__notebook)
        self.__frame.pack(fill=tk.BOTH, expand=True)

        # FTP
        ttk.Label(self.__frame, 
                  text="FTP:").grid(row=0, 
                                    column=0, 
                                    sticky='w', 
                                    padx=10, 
                                    pady=5)
        
        # Validierung für nur Ganzzahlen
        vcmd = (self.__frame.register(self._validate_integer),
                '%P')
        self.__ftp_var = tk.StringVar(value="230")
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
        
        # Min. Watt für Graphen 
        ttk.Label(self.__frame, 
                  text="min. Watt Grafik:").grid(row=1, 
                                                 column=0, 
                                                 sticky='w', 
                                                 padx=10, 
                                                 pady=5)
        self.__min_watt_var = tk.StringVar(value="300")
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

    def get_notebook(self):
        return self.__notebook
    
    def get_ftp(self):
        return int(self.__ftp_var.get().strip())
    
    def get_min_watt(self):
        return int(self.__min_watt_var.get().strip())
    
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