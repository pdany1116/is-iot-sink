from enum import Enum

class IrrigationMode(Enum):
    MANUAL = 0
    AUTO = 1

    @classmethod
    def mode_to_str(self, mode):
        if mode == self.MANUAL:
            return "MANUAL"
        elif mode == self.AUTO:
            return "AUTO"
        else:
            return None

    @classmethod
    def str_to_mode(self, str):
        str = str.upper()

        if str == "MANUAL":
            return self.MANUAL
        elif str == "AUTO":
            return self.AUTO
        else:
            return None
