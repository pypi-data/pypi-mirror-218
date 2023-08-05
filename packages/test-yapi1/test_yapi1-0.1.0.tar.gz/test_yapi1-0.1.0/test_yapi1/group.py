from test_yapi1.base import YApiBase


class GroupMixIn(YApiBase):
    def get_my_group(self):
        """
        获取用户默认值
        :return: 响应data
            eg: {
                '_id': 44,
                'add_time': 1682637364,
                'custom_field1': {'enable': False},
                'group_name': 'User-16',
                'up_time': 16827623636
            }

        """
        url = '/api/group/get_mygroup'
        return self.get(url)
