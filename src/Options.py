import json
from pathlib import Path

class Options:
    __instance = None
    
    def __new__(cls):
        raise TypeError("Benutzen Sie get_instance() zum Erstellen einer Instanz.")
    
    @classmethod
    def get_instanz(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__load_from_file()
        return cls.__instance

    
    def save_to_file(self):
        meine_daten = {
            "ftp": self.ftp,
            "minWatt4Grafic": self.minWatt4Grafic,
            "language": self.language
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
        except FileNotFoundError:
            self.ftp = 230
            self.minWatt4Grafic = 300
            self.language = 'de'

    def get_ftp(self):
        return self.ftp
    
    def get_minWatt4Grafic(self):
        return self.minWatt4Grafic
    
    def get_language(self):
        return self.language
    
    def set_language(self, language):
        self.language = language
        
    def set_ftp(self, ftp):
        self.ftp = ftp  
        
    def set_minWatt4Grafic(self, minWatt4Grafic):
        self.minWatt4Grafic = minWatt4Grafic    