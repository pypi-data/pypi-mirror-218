from pprint import pprint

def test_get_my_group(yapi_login):
    data = yapi_login.get_my_group()
    pprint(data)
