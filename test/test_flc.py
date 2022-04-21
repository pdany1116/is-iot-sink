import pytest
from is_iot_sink.irrigation.automated.flc import *

instance = FLC()

def test_init():
    assert isinstance(instance, FLC) == True

@pytest.mark.skip(reason="Not implemented yet!")
def test_solve_worst_env_case():
    sm = 0
    temp = 40
    hum = 0
    light = 100
    irrig_time = 10
    assert instance.solve(sm, temp, hum, light) == irrig_time

@pytest.mark.skip(reason="Not implemented yet!")
def test_solve_best_env_case():
    sm = 100
    temp = -10
    hum = 100
    light = 0
    irrig_time = 0
    assert instance.solve(sm, temp, hum, light) == irrig_time
