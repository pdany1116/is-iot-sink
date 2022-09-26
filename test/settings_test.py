import pytest
import os
from is_iot_sink.settings import Settings
from threading import Lock

def filepath():
    return os.getenv('PROJECT_PATH') + '/test/fixtures/settings_test_setup.yml'

def test_get_simple_text_setting():
    settings = Settings(filepath = filepath(), mutex = Lock())

    assert settings.get('name') == 'SinkTest'

def test_get_array_setting():
    settings = Settings(filepath = filepath(), mutex = Lock())

    assert settings.get('array') == [1,2,3]

def test_get_nested_text_setting():
    settings = Settings(filepath = filepath(), mutex = Lock())

    assert settings.get('location/latitude') == 42

def test_set_setting():
    settings = Settings(filepath = filepath(), mutex = Lock())
    value = 'SinkChanged'

    settings.set('name', value) 

    assert settings.get('name') == value
