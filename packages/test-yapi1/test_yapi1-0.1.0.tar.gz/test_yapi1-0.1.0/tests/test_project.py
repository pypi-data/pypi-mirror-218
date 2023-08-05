from pprint import pprint

def test_add_project(yapi_login):
    group_id = yapi_login.get_my_group()['_id']
    data = yapi_login.add_project(
        name='示例项目3',
        basepath= '/proj3',
        desc='示例项目3描述',
        group_id=group_id
    )
    pprint(data)

def test_add_project02(yapi_login):
    data = yapi_login.add_project(name="示例项目4")
    pprint(data)
