from pprint import pprint


def test_add_project(yapi_login):
    group_id = yapi_login.get_may_group()['_id']
    data = yapi_login.add_project(
        name="测试项目1",
        basepath='/project',
        desc='描述1',
        group_id = group_id,
    )
    pprint(data)
