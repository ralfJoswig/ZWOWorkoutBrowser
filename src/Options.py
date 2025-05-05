import json
from pathlib import Path

class Options:
    __instance = None
    __root = None
    
    def __new__(cls):
        raise TypeError("Benutzen Sie get_instance() zum Erstellen einer Instanz.")
    
    @classmethod
    def get_instanz(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__load_from_file()
        return cls.__instance

    def set_root(self, root):
        Options.__root = root
    
    def save_to_file(self):
        #winfo_width = 
        #winfo_height = 
        meine_daten = {
            "ftp": self.ftp,
            "minWatt4Grafic": self.minWatt4Grafic,
            "language": self.language,
            "winfo_width": Options.__root.winfo_width(),
            "winfo_height": Options.__root.winfo_height(),
            "winfo_x": Options.__root.winfo_x(),
            "winfo_y": Options.__root.winfo_y(),
            }
        """ Saves the options to a file """
        with open(self.initFile, "w", encoding="utf-8") as datei:
            json.dump(meine_daten, datei, ensure_ascii=False, indent=4)
            
    def __load_from_file(self):
        localedir = Path(__file__).parent.resolve().absolute()
        self.initFile = localedir / 'ZWOWorkoutBrowser.ini'
        """ Loads the options from a file """
        try:
            with open(self.initFile, "r", encoding="utf-8") as datei:
                meine_daten = json.load(datei)
                self.ftp = int(meine_daten.get("ftp", 230))
                self.minWatt4Grafic = int(meine_daten.get("minWatt4Grafic", 300))
                self.language = meine_daten.get("language", 'de')
                self.winfo_width = int(meine_daten.get("winfo_width", 800))
                self.winfo_height = int(meine_daten.get("winfo_height", 600))
                self.winfo_x = int(meine_daten.get("winfo_x", 0))
                self.winfo_y = int(meine_daten.get("winfo_y", 0))   
        except FileNotFoundError:
            self.ftp = 230
            self.minWatt4Grafic = 300
            self.language = 'de'
            self.winfo_width = 800
            self.winfo_height = 600
            self.winfo_x = 0
            self.winfo_y = 0

    def get_ftp(self):
        return self.ftp
    
    def get_winfo_x(self):
        return self.winfo_x 
    
    def get_winfo_y(self):
        return self.winfo_y
    
    def get_minWatt4Grafic(self):
        return self.minWatt4Grafic
    
    def get_language(self):
        return self.language
    
    def get_winfo_width(self):
        return self.winfo_width
    
    def get_winfo_height(self):
        return self.winfo_height
    
    def set_language(self, language):
        self.language = language
        
    def set_ftp(self, ftp):
        self.ftp = ftp  
        
    def set_minWatt4Grafic(self, minWatt4Grafic):
        self.minWatt4Grafic = minWatt4Grafic    