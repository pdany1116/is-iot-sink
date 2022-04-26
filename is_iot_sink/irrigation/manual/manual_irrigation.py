from is_iot_sink.irrigation.irrigation import *
from is_iot_sink.irrigation.mode import *

class ManualIrrigation(Irrigation):
    def __init__(self):
        super().__init__()
        self.mode = Mode.MANUAL

    def run(self):
        pass
