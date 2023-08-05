from pprint import pprint

import pytest

from test_yapi1 import YApiClient

def test_register(yapi):
    username, email, password = 'Kevin','kevin3@126.com','abc123'
    data = yapi.register(username, email, password)
    pprint(data)
    assert data['username'] == username
    assert data['email'] == email


def test_login(yapi, user):
    username, email, password = 'Kevin','kevin3@126.com','abc123'
    data = yapi.login(email, password)
    assert data['username'] == username
    assert data['email'] == email
