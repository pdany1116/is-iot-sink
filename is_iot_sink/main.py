from is_iot_sink.sink import Sink
from is_iot_sink.logger import LOG
from pathlib import Path
from dotenv import Dotenv
import os
import time
import sys
import signal

sink = Sink()

def set_env_variables():
    env_file_path = Path(os.getenv('PROJECT_PATH') + '/.env')
    dotenv = Dotenv(env_file_path)
    os.environ.update(dotenv)

def signal_handler(sig, frame):
    LOG.info("SIGINT received!")
    sink.stop()
    sys.exit(0)

def main():
    signal.signal(signal.SIGINT, signal_handler)
    set_env_variables()
    sink.start()
    while sink.status() == True:
        time.sleep(1)
    
if __name__ == "__main__":
    main()
