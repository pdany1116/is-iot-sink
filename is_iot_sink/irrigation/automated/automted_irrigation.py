from is_iot_sink.irrigation.irrigation import *
from is_iot_sink.irrigation.mode import *

class AutomatedIrrigation(Irrigation):
    def __init__(self):
        super().__init__()
        self.mode = Mode.AUTO

    def run(self):
        pass
