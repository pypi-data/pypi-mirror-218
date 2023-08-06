import pytest

from work_yapi import WorkYapi
from pprint import pprint




def test_register(yapi):
    username,email,password = 'wp7', 'wp7@126.com', '123456'
    data = yapi.register(username,email,password
    )
    pprint(data)
    assert data['username'] == username
    assert data['email'] == email

def test_login(yapi):
    username,email,password = 'wp7', 'wp7@126.com', '123456'
    data = yapi.login(email,password)
    pprint(data)
    assert data['username'] == username
    assert data['email'] == email
