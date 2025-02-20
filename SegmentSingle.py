from dataclasses import dataclass
from TextEvent import TextEvent
from Power import Power
from EnumSegmentType import SegmentType

@dataclass
class SegmentSingle:
    __duration: int
    __power: Power
    __textevents: list[TextEvent]
    __type: SegmentType
    __cadence: int

    def add_text_event(self, timeoffset, message):
        if self.__textevents is None:
            self.__textevents = []

        self.__textevents.append(TextEvent(timeoffset, message))

    def get_power(self):
        return self.__power
    
    def get_segment_type(self):
        return self.__type
    
    def get_duration(self):
        return self.__duration
    
    def get_cadence(self):
        return self.__cadence
    
    def get_text_count(self):
        return len(self.__textevents) if self.__textevents is not None else 0
    
    def get_duration_as_text(self):
        mins, secs = divmod(self.__duration, 60)
        return f"{mins:02d}:{secs:02d}"