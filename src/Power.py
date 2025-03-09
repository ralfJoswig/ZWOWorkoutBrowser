from dataclasses import dataclass

@dataclass
class Power:
    """ A simple class to represent min and max power targets """
    start_power: float
    end_power: float

    def get_as_text(self, ftp :int):
        """ Returns the power targets as a string """
        if self.start_power != 0 and self.end_power != 0 and self.start_power != self.end_power: 
            #result = f"{int(float(self.start_power) * float(ftp))} - {int(float(self.end_power) * float(ftp))}"
            result = f"{Power.round_to_five(float(self.start_power) * float(ftp))} - {Power.round_to_five(float(self.end_power) * float(ftp))}"
        elif self.start_power != 0:
            result = f"{Power.round_to_five(float(self.start_power) * float(ftp))}"    
        elif self.end_power != 0:
            result = f"{Power.round_to_five(float(self.end_power) * float(ftp))}"
        else:
            result = ""
        return result
    
    def round_to_five(zahl):
        """
        Rundet eine Fließkommazahl kaufmännisch auf ein Vielfaches von 5.
        
        Args:
            zahl (float): Die zu rundende Fließkommazahl
        
        Returns:
            int: Die kaufmännisch auf ein Vielfaches von 5 gerundete Ganzzahl
        """
        # Division durch 5, um das Problem auf Rundung auf Ganzzahlen zu reduzieren
        quotient = zahl / 5
        
        # Kaufmännische Rundung (round() in Python verwendet Banker's Rounding)
        gerundeter_quotient = round(quotient)
        
        # Zurückmultiplizieren mit 5
        ergebnis = gerundeter_quotient * 5
        
        return int(ergebnis)
    
    def get_start_power_for_ftp(self, ftp :int):
        """ Returns the start power target as a percentage of FTP """
        return Power.round_to_five(float(self.start_power) * float(ftp))
    
    def get_end_power_for_ftp(self, ftp :int):
        """ Returns the end power target as a percentage of FTP """
        return Power.round_to_five(float(self.end_power) * float(ftp))