import xml.etree.ElementTree as ET
from Power import Power
from SegmentSingle import SegmentSingle
from SegmentInterval import SegmentInterval
from EnumSegmentType import SegmentType
from EnumSportType import SportType

class ZwoWorkout:
    def __init__(self):
        self.__uniqueId = ""
        self.__legacyIdHash = ""
        self.__author = ""
        self.__categoryOverride = ""
        self.__name = ""
        self.__description = ""
        self.__sportType = SportType.UNKNOWN
        self.__category = ""
        self.__overrideHash = ""
        self.__visibleOutsidePlan = ""
        self.__subcategory = ""
        self.__activitySaveName = ""
        self.__visibleAfterTime = ""
        self.__tags = []
        self.__segments = []
        self.__duration = 0
        self.__max_power = 0

    @property
    def max_power(self):
        return self.__max_power

    @property
    def duration(self):
        return self.__duration
    
    @property
    def segments(self):
        return self.__segments
    
    @property
    def tags(self):
        return self.__tags

    @property
    def visibleAfterTime(self):
        return self.__visibleAfterTime
    
    @property
    def activitySaveName(self):
        return self.__activitySaveName
    
    @property
    def subcategory(self):
        return self.__subcategory   
    
    @property
    def visibleOutsidePlan(self):
        return self.__visibleOutsidePlan
    
    @property
    def overrideHash(self):
        return self.__overrideHash

    @property
    def category(self):
        return self.__category
    
    @property
    def uniqueId(self):
        return self.__uniqueId
    
    @property
    def legacyIdHash(self):
        return self.__legacyIdHash

    @property
    def author(self):
        return self.__author
    
    @property
    def categoryOverride(self):
        return self.__categoryOverride
    
    @property
    def name(self):
        return self.__name
    
    @property
    def description(self):
        return self.__description
    
    @property
    def sportType(self):
        return self.__sportType

    @staticmethod
    def round_to_nearest_second(value):
        """ takes a floating point number of seconds as a string and returns
        the number of seconds as an integer """
        return int(round(float(value)))
    
    @staticmethod
    def parse_cadence(node, suffix=""):
        if node.tag == "FreeRide":
            return None

        return node.get("Cadence" + suffix) if node.get("Cadence") is not None else 0
       
    @staticmethod
    def parse_textevents(node, segment):
        for textevent in node.iter("textevent"):
            timeoffset = int(textevent.get("timeoffset"))
            message = textevent.get("message")
            segment.add_text_event(timeoffset, message)

        return segment
    
    @staticmethod
    def parse_power(node, segment_type):
        target_intensity = float(node.get("Power")) if node.get("Power") is not None else 0.0
        power_low = float(node.get("PowerLow")) if node.get("PowerLow") is not None else target_intensity
        power_high = float(node.get("PowerHigh")) if node.get("PowerHigh") is not None else 0.0

        match segment_type:
            case SegmentType.WARMUP:
                return Power(power_low, power_high)
            case SegmentType.STEADYSTATE:
                return Power(target_intensity, target_intensity)
            case SegmentType.FREERIDE:
                return Power(0, 0)
            case SegmentType.COOLDOWN:
                if power_low < power_high:
                    return Power(power_high, power_low)
                else:
                    return Power(power_low, power_high)
            case SegmentType.RAMP:  
                return Power(power_low, power_high)
            case _:
                return Power(999, 999)
    
    def parse(self, xmlstring, minduration=0):
        segments = []
        tree = ET.ElementTree(ET.fromstring(xmlstring))
        root = tree.getroot()
    
        self.__uniqueId = root.find("uniqueId").text if root.find("uniqueId") is not None else ""
        self.__legacyIdHash = root.find("legacyIdHash").text if root.find("legacyIdHash") is not None else ""
        self.__author = root.find("author").text if root.find("author") is not None else ""
        self.__categoryOverride = root.find("categoryOverride").text if root.find("categoryOverride") is not None else ""
        self.__name = root.find("name").text if root.find("name") is not None else ""
        self.__description = root.find("description").text if root.find("description") is not None else ""
        self.__sportType = ZwoWorkout.parse_sport_type(root)
        self.__category = root.find("category").text if root.find("category") is not None else ""
        self.__overrideHash = root.find("overrideHash").text if root.find("overrideHash") is not None else ""
        self.__visibleOutsidePlan = root.find("visibleOutsidePlan").text if root.find("visibleOutsidePlan") is not None else ""
        self.__subcategory = root.find("subcategory").text if root.find("subcategory") is not None else ""
        self.__activitySaveName = root.find("activitySaveName").text if root.find("activitySaveName") is not None else ""
        self.__visibleAfterTime = root.find("visibleAfterTime").text if root.find("visibleAfterTime") is not None else ""

        tag_list = root.find("tags")
        for node in tag_list:
            tag = node.get("name")
            self.__tags.append(tag)

        workout = root.find("workout")
        for node in workout:
            
            segment_type = ZwoWorkout.det_segement_type(node)
            match segment_type:
                case SegmentType.WARMUP |  SegmentType.STEADYSTATE | SegmentType.RAMP | SegmentType.FREERIDE | SegmentType.COOLDOWN:
                    duration = int(float(node.get("Duration")))
                    cadence = int(ZwoWorkout.parse_cadence(node))
                    power = ZwoWorkout.parse_power(node, segment_type)
                    workout = SegmentSingle(duration, 
                                            power, 
                                            None,
                                            segment_type,
                                            cadence)
                case SegmentType.INTERVALST:
                    repeat = int(node.get("Repeat"))
                    on_duration = int(node.get("OnDuration"))
                    off_duration = int(node.get("OffDuration"))
                    power = ZwoWorkout.parse_interval_power(node)
                    cadence_work = int(ZwoWorkout.parse_cadence(node))
                    cadence_rest = int(ZwoWorkout.parse_cadence(node, "Resting"))
                    workout = SegmentInterval(repeat,
                                              on_duration,
                                              off_duration,
                                              power,
                                              None,
                                              segment_type,
                                              cadence_work)              
                case _:
                    power = Power(0, 0)
                    workout = SegmentSingle(0, 
                                            power, 
                                            None,
                                            segment_type,
                                            "")
                    #self.__segments.append(workout_segment)
            ZwoWorkout.parse_textevents(node, workout)
            self.__segments.append(workout)  
            self.__duration += workout.get_duration()
            if power.end_power > self.__max_power:
                self.__max_power = power.end_power 
            if power.start_power > self.__max_power:
                self.__max_power = power.start_power

    def parse_sport_type(node):
        match node.find("sportType").text:
            case "bike" | "ride":
                return SportType.BIKE
            case _:
                return SportType.UNKNOWN
              
    def det_segement_type(node):
        lowerTag = node.tag.lower()
        match node.tag.lower():
            case "warmup":
                return SegmentType.WARMUP
            case "steadystate":
                return SegmentType.STEADYSTATE
            case "ramp":
                return SegmentType.RAMP
            case "freeride":
                return SegmentType.FREERIDE
            case "cooldown":
                return SegmentType.COOLDOWN
            case "intervalst":
                return SegmentType.INTERVALST
            case _:
                return SegmentType.UNKNOWN
    
    def parse_interval_power(node):
        on_power = float(node.get("OnPower")) if node.get("OnPower") is not None else 0.0
        off_power = float(node.get("OffPower")) if node.get("OffPower") is not None else 0.0
        return Power(on_power, off_power)
    
    def get_duration_as_text(self):
        mins, secs = divmod(self.__duration, 60)
        hours, mins = divmod(mins, 60)
        return f"{hours:02d}:{mins:02d}:{secs:02d}"
    
    def get_max_power(self):
        max_power = 0
        for segment in self.__segments:
            if segment.power.max_intensity > max_power:
                max_power = segment.power.max_intensity
            if segment.power.min_intensity > max_power:
                max_power = segment.power.min_intensity
        return max_power
    
    def get_max_cadence(self):
        max_cadence = 0
        for segment in self.__segments:
            if segment.get_cadence() > max_cadence:
                max_cadence = segment.get_cadence()
        return max_cadence