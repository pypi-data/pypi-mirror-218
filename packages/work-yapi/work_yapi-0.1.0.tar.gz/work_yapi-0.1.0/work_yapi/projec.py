from work_yapi.base import YapiBase


class ProjectMixIn(YapiBase):
    def add_project(self,name,basepath,desc,group_id,icon="code-o",color="purple",project_type ='private' ):
        """
        添加项目
        :param name:项目名称
        :param basepath:项目路径
        :param desc:项目描述
        :param group_id:所属项目组id
        :param icon:项目图标
        :param color:项目颜色
        :param project_type:
        :return:响应data
        eg:{'__v': 0,
             '_id': 30,
             'add_time': 1688920812,
             'basepath': '/project',
             'color': 'purple',
             'desc': '描述1',
             'env': [{'_id': '64aae2ec497c231db8cee70c',
                      'domain': 'http://127.0.0.1',
                      'global': [],
                      'header': [],
                      'name': 'local'}],
             'group_id': 59,
             'icon': 'code-o',
             'is_json5': False,
             'is_mock_open': False,
             'members': [],
             'name': '测试项目1',
             'project_type': 'private',
             'strice': False,
             'switch_notice': True,
             'tag': [],
             'uid': 92,
             'up_time': 1688920812}
        """
        url = '/api/project/add'
        payload = {"name":name,
                   "basepath":basepath,
                   "desc":desc,
                   "group_id":str(group_id),
                   "icon":icon,
                   "color":color,
                   "project_type":project_type}
        return self.post(url,payload)
