from enum import Enum
from is_iot_sink import utils

class Mode(Enum):
    MANUAL = 0
    AUTO = 1

def mode_to_str(mode):
    if mode == Mode.MANUAL:
        return "MANUAL"
    elif mode == Mode.AUTO:
        return "AUTO"
    else:
        return None

def str_to_mode(str):
    str = str.upper()

    if str == "MANUAL":
        return Mode.MANUAL
    elif str == "AUTO":
        return Mode.AUTO
    else:
        return None

def initial_mode():
    return str_to_mode(utils.get_setting("irrigation/initialMode").upper())
