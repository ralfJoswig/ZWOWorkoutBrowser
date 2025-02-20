from dataclasses import dataclass

@dataclass
class Power:
    """ A simple class to represent min and max power targets """
    start_power: float
    end_power: float

    def get_as_text(self, ftp :int):
        """ Returns the power targets as a string """
        if self.start_power != 0 and self.end_power != 0 and self.start_power != self.end_power: 
            result = f"{int(float(self.start_power) * float(ftp))} - {int(float(self.end_power) * float(ftp))}"
        elif self.start_power != 0:
            result = f"{int(float(self.start_power) * float(ftp))}"    
        elif self.end_power != 0:
            result = f"{int(float(self.end_power) * float(ftp))}"
        else:
            result = ""
        return result