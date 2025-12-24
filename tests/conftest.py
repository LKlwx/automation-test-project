import pytest
from core import ConfigManager, DataReader, APIClient

@pytest.fixture(scope="session")
def config():
    return ConfigManager()


@pytest.fixture(scope="session")
def data_reader():
    return DataReader()


@pytest.fixture(scope="session")
def api_client():
    return APIClient()