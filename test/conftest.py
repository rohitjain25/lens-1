import pytest
from setup.requests import Requests
from setup.log import Log



@pytest.fixture
def requests():
    return Requests()

@pytest.fixture
def log():
    return Log()