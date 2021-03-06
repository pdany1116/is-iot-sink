from is_iot_sink.irrigation.mode import *
from is_iot_sink.logger import LOG

class ManualIrrigation:
    def __init__(self):
        super().__init__()
        self.mode = Mode.MANUAL

    def start(self):
        LOG.info("Manual Irrigation process started.")
        pass

    def stop(self):
        LOG.info("Manual Irrigation process stopped.")
        pass
