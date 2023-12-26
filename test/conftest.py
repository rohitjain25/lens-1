import pytest
from setup.requests import Requests


@pytest.fixture
def requests():
    return Requests()