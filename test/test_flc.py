import pytest
from is_iot_sink.irrigation.flc import *

instance = FLC()

def test_init():
    assert isinstance(instance, FLC) == True
