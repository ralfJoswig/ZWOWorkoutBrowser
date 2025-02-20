from enum import Enum

class SegmentType(Enum):
    WARMUP = "Warmup"
    STEADYSTATE = "SteadyState"
    RAMP = "Ramp"
    FREERIDE = "Freeride"
    COOLDOWN = "Cooldown"
    UNKNOWN = "Unknown"
    INTERVALST = "Intervalst"