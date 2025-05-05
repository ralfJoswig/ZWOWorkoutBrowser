class Version:
    """Klasse für die Version des Programms"""
    
    __version = '0.4'
    
    @classmethod
    def get_version(cls):
        """Gibt die Version der Anwendung zurück"""
        return cls.__version