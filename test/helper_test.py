import pytest
import subprocess
from test.helper import TestHelper

STARTED_RETURN_CODE = 0
STOPPED_RETURN_CODE = 3

def test_suite_setup_starts_mqtt_broker():
    TestHelper.suite_setup()

    result = subprocess.run('sudo service mosquitto status'.split())

    assert result.returncode == STARTED_RETURN_CODE

def test_suite_setup_stops_mqtt_broker():
    TestHelper.suite_teardown()

    result = subprocess.run('sudo service mosquitto status'.split())

    assert result.returncode == STOPPED_RETURN_CODE
