from is_iot_sink.irrigation.manual.manual_irrigation import ManualIrrigation
from is_iot_sink.irrigation.automated.automted_irrigation import AutomatedIrrigation
from is_iot_sink.irrigation.mode import *

class IrrigationFactory:
    def __init__(self):
        pass

    def create(self, mode):
        if (mode == Mode.MANUAL):
            return ManualIrrigation()
        elif (mode == Mode.AUTO):
            return AutomatedIrrigation()
        else:
            return None
