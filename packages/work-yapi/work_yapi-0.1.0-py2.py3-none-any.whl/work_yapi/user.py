from .base import YapiBase

class UserMixIn(YapiBase):
    """
    :param username: 用户名
    :param email:邮箱（不能重复）
    :param password:密码
    :return: 响应中的data
        eg:{'add_time': 1688802196,
             'email': 'wp5',
             'role': 'member',
             'study': False,
             'type': 'site',
             'uid': 74,
             'up_time': 1688802196,
             'username': 'wp5@126.com'}
    """
    def register(self,username,email,password):
        url = "/api/user/reg"
        payload = {"username":username,
                   "email":email,
                   "password":password
                   }
        return self.post(url,payload)

    def login(self, email, password):
        """
        登录
        :param email: 用户邮箱
        :param password: 用户密码
        :return: 响应的data
            eg：{'add_time': 1688802888,
                 'email': 'wp7@126.com',
                 'role': 'member',
                 'study': False,
                 'type': 'site',
                 'uid': 92,
                 'up_time': 1688802888,
                 'username': 'wp7'}
        """
        url = '/api/user/login'
        payload = {"email": email, "password": password}
        return self.post(url, payload)

