import gettext
import locale
import os
from pathlib import Path

class LanguageSwitcher:    
    def __init__(self):
        """
        Initialisiert den LanguageSwitcher für Übersetzungen.
        
        :param domain: Name des Übersetzungsbereichs
        :param localedir: Verzeichnis mit Übersetzungsdateien
        """
        self.domain = 'ZWOBroser'
        self.localedir = Path(__file__).parent.resolve() / 'locales'
        self.current_language = 'de'
        
    def set_language(self, language_code):
        """
        Wechselt die Sprache dynamisch während der Laufzeit.
        
        :param language_code: Sprachcode (z.B. 'de', 'en', 'fr')
        """
        try:
            # Setze Locale für die ausgewählte Sprache
            locale.setlocale(locale.LC_ALL, language_code)
            
            # Initialisiere Übersetzung
            translation = gettext.translation(
                self.domain, 
                localedir=self.localedir, 
                languages=[language_code], 
                fallback=False
            )
            translation.install()
            
            self.current_language = language_code
            
            self._ = translation.gettext
        
        except Exception as e:
            print(f"Fehler beim Sprachwechsel: {e}")
    
    def get_current_language(self):
        """
        Gibt die aktuell eingestellte Sprache zurück.
        
        :return: Aktueller Sprachcode
        """
        return self.current_language