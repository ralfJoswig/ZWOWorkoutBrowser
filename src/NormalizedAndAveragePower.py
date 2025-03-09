import numpy as np
from ZwoWorkout import ZwoWorkout
from EnumSegmentType import SegmentType

class NormalizedAndAveragePower:
    def __init__(self, workout: ZwoWorkout):
        self.workout = workout
        
    def calculate(self,ftp: int):
        """
        Berechnet die Normalized Power aus einer Liste von (Leistung, Dauer)-Paaren.
    
        Schritte zur Berechnung der Normalized Power:
        1. Konvertiere die Daten in eine Sekunden-für-Sekunden-Zeitreihe
        2. Berechne den rollenden 30-Sekunden-Durchschnitt der Leistungswerte
        3. Nehme die vierte Potenz jedes geglätteten Leistungswerts
        4. Berechne den Durchschnitt dieser Werte
        5. Nehme die vierte Wurzel dieses Durchschnitts
    
        Returns:
            normalized_power: Die normalisierte Leistung in Watt
            average_power: Die durchschnittliche Leistung in Watt
        """
        # Schritt 1: Konvertiere Daten in Sekunden-für-Sekunden-Zeitreihe
        power_series = []
    
        for segment in self.workout.segments:
            match segment.get_segment_type():
                case SegmentType.STEADYSTATE:
                    power_series.extend([segment.get_power().get_start_power_for_ftp(ftp)] * segment.get_duration())
                case SegmentType.WARMUP | SegmentType.RAMP | SegmentType.COOLDOWN:
                    anzahlStufen = int(abs(segment.get_power().get_start_power_for_ftp(ftp) - segment.get_power().get_end_power_for_ftp(ftp)) / 5 + 1)
                    startZahl = min(segment.get_power().get_start_power_for_ftp(ftp), segment.get_power().get_end_power_for_ftp(ftp))
                    dauer = int(segment.get_duration() / anzahlStufen)
                    for i in range(anzahlStufen + 1):  # +1 weil wir auch den Startwert benötigen
                        aktueller_wert = startZahl + i * 5
                        power_series.extend([aktueller_wert] * dauer)
                #case SegmentType.FREE, :
                case SegmentType.INTERVALST:
                    for interval in range(segment.get_repeat()):
                        power_series.extend([segment.get_power().get_start_power_for_ftp(ftp)] * segment.get_duration())
                        power_series.extend([segment.get_power().get_end_power_for_ftp(ftp)] * segment.get_duration())
    
        power_array = np.array(power_series)
    
        # Berechne durchschnittliche Leistung
        average_power = np.mean(power_array)
    
        # Schritt 2: Berechne rollenden 30-Sekunden-Durchschnitt
        window_size = 30
        rolling_avg = np.convolve(power_array, np.ones(window_size)/window_size, mode='valid')
    
        # Schritt 3 & 4: Nehme die vierte Potenz und berechne den Durchschnitt
        fourth_power_avg = np.mean(rolling_avg ** 4)
    
        # Schritt 5: Nehme die vierte Wurzel
        normalized_power = np.power(fourth_power_avg, 0.25)
        normalized_power = round(normalized_power)
        average_power = round(average_power)
    
        return normalized_power, average_power