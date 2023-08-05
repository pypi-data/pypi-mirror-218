import random
from typing import Callable

from test_yapi1.base import YApiBase

PROJECT_COLORS = [
    'blue',
    'green',
    'yellow',
    'red',
    'pink',
    'cyan',
    'gray',
    'purple'
]

PROJECT_ICONS =[
    'code-o',
    'swap',
    'clock-circle-o',
    'unlock',
    'calendar',
    'play-circle-o',
    'file-text',
    'desktop',
    'hdd',
    'appstore-o',
    'line-chart',
    'mail',
    'mobile',
    'notification',
    'picture',
    'poweroff',
    'search',
    'setting',
    'share-alt',
    'shopping-cart',
    'tag-o',
    'video-camera',
    'cloud-o',
    'star-o',
    'environment-o',
    'camera-o',
    'team',
    'customer-service',
    'pay-circle-o',
    'rocket',
    'database',
    'tool',
    'wifi',
    'idcard',
    'medicine-box',
    'coffee',
    'safety',
    'global',
    'api',
    'fork',
    'android-o',
    'apple-o'
]

class ProjectMixIn(YApiBase):
    get_my_group: Callable

    def add_project(self, name,
                    basepath=None,
                    group_id=None,
                    desc='',
                    icon=None,
                    color=None,
                    project_type='private'):
        """
        添加项目
        :param name: 项目名称
        :param basepath: 项目路径（不能重复
        :param desc: 项目描述
        :param group_id: 所属项目组ID
        :param icon: 项目图标, PORJECT_ICONS中随意一个 (默认随机图标)
        :param color: 项目颜色，PROJECT_COLORS中任意一个（默认随机颜色）
        :param project_type: 项目类型，默认为private
        :return: 响应data
            eg: {'__v': 0,
                 '_id': 58,
                 'add_time': 1688292619,
                 'basepath': '/proj2',
                 'color': 'purple',
                 'desc': '示例项目2描述',
                 'env': [{'_id': '64a14d0ba534ee9cf4b71394',
                          'domain': 'http://127.0.0.1',
                          'global': [],
                          'header': [],
                          'name': 'local'}],
                 'group_id': 44,
                 'icon': 'code-o',
                 'is_json5': False,
                 'is_mock_open': False,
                 'members': [],
                 'name': '示例项目2',
                 'project_type': 'private',
                 'strice': False,
                 'switch_notice': True,
                 'tag': [],
                 'uid': 16,
                 'up_time': 1688292619}
        """
        url = '/api/project/add'
        if color is None:
            color = random.choice(PROJECT_COLORS)
        if icon is None:
            icon = random.choice(PROJECT_ICONS)
        if basepath is None:
            from slugify import slugify
            basepath = slugify(name)
        if group_id is None:
            group_id = self.get_my_group()['_id']

        payload = {"name": name,
                   "basepath": basepath,
                   "desc": desc,
                   "group_id": str(group_id),
                   "icon": icon,
                   "color": color,
                   "project_type": project_type}
        return self.post(url, payload)






























