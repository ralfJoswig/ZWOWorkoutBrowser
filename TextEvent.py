from dataclasses import dataclass

@dataclass
class TextEvent:
    """ A simple class to represent a text event with timeoffset and message.
    timeoffset is seconds from the beginning of the workout.
    timeoffset_relative is seconds form the beginning of the segment in which the
    textmessage appears (useful for auto-hotkey timings)"""
    timeoffset: int
    #timeoffset_relative: int
    message: str