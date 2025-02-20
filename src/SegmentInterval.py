from dataclasses import dataclass
from TextEvent import TextEvent
from Power import Power
from EnumSegmentType import SegmentType

@dataclass
class SegmentInterval:
    __repeat: int
    __on_duration: int
    __off_duration: int
    __power: Power
    __textevents: list[TextEvent]
    __type: SegmentType
    __cadence: int

    @property
    def on_duration(self):
        return self.__on_duration
    
    @property
    def off_duration(self):
        return self.__off_duration
    
    def add_text_event(self, timeoffset, message):
        if self.__textevents is None:
            self.__textevents = []

        self.__textevents.append(TextEvent(timeoffset, message))

    def get_power(self):
        return self.__power
    
    def get_segment_type(self):
        return self.__type
    
    def get_duration(self):
        return ( self.__on_duration + self.__off_duration ) * self.__repeat
    
    def get_cadence(self):
        return self.__cadence
    
    def get_text_count(self):
        return len(self.__textevents) if self.__textevents is not None else 0
    
    def get_repeat(self):
        return self.__repeat
    
    def get_duration_as_text(self):
        on_mins, on_secs = divmod(self.__on_duration, 60)
        off_mins, off_secs = divmod(self.__off_duration, 60)
        return f"{on_mins:02d}:{on_secs:02d}/{off_mins:02d}:{off_secs:02d}"
    
    def get_on_duration_as_text(self):
        mins, secs = divmod(self.__on_duration, 60)
        return f"{mins:02d}:{secs:02d}"
    
    def get_off_duration_as_text(self):
        mins, secs = divmod(self.__off_duration, 60)
        return f"{mins:02d}:{secs:02d}"