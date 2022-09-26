import pytest
from is_iot_sink.mongodb.mongodb_client import MongoClient
from is_iot_sink.sink import Sink
from test.helper import TestHelper
from test.mocks.collector_mock import CollectorMock
import time

def setup_module():
    TestHelper.suite_setup()

def teardown_module():
    TestHelper.suite_teardown()

def test_smoke_test():
    settings = TestHelper.default_test_settings()
    sink = Sink(settings)

    sink.start()
    assert sink.status() == True

    sink.stop()
    assert sink.status() == False

def test_saves_collector_data_in_db():
    # Arrange
    settings = TestHelper.default_test_settings()
    TestHelper.cleanup_database(settings)
    collector_id = '0000'
    collector = CollectorMock(collector_id, settings)
    sink = Sink(settings)
    mongo_client = MongoClient(settings)

    # Act
    sink.start()
    collector.register(settings.get('mqtt/topics/collector/registration'))
    collector.send_dummy_data(settings.get('mqtt/topics/collector/data'))
    time.sleep(1)

    # Assert
    assert sink.status() == True
    assert mongo_client.db[settings.get('mongo/collections/readings')].count_documents({'collectorId': collector_id}) == 1
