import pytest
from work_yapi import WorkYapi


@pytest.fixture()
def base_url():
    return 'http://localhost:3000'

@pytest.fixture()
def user():
    return 'wp7@126.com','123456'

@pytest.fixture
def yapi(base_url):
    return WorkYapi(base_url)


@pytest.fixture
def yapi_login(yapi,user):
    yapi.login(*user)
    return yapi

