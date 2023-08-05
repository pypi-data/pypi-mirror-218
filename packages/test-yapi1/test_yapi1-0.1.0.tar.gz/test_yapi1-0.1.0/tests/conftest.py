import pytest

from test_yapi1 import YApiClient


@pytest.fixture
def base_url():
    return 'http://localhost:3001'

@pytest.fixture
def user():
    return 'kevin2@126.com', 'abc123'

@pytest.fixture
def yapi(base_url):
    return YApiClient(base_url)

@pytest.fixture
def yapi_login(yapi, user):
    yapi.login(*user)
    return yapi
