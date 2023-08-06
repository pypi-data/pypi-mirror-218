from .base import YapiBase

class GroupMixIn(YapiBase):
    def get_may_group(self):
        """
        获取用户默认组
        :return:影响data
        eg：{'_id': 59,
             'add_time': 1688802888,
             'custom_field1': {'enable': False},
             'group_name': 'User-92',
             'type': 'private',
             'up_time': 1688802888}
        """
        url = '/api/group/get_mygroup'
        return self.get(url)
