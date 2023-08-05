from .base import YApiBase

class UserMixIn(YApiBase):

    def register(self, username, email, password):
        '''
        注册用户
        :param username:用户名
        :param email：邮箱
        :param password: 密码
        :return: 响应中的data
            eg: {
            'add_time': 168829213,
            'email': 'kevin2@126.com',
            'role': 'member',
            'study': False,
            'uid': 17,
            'up_time': 18273733,
            'username': 'kevin'}
        '''
        url = '/api/user/reg'
        payload = {
            "email": email,
            "password": password,
            "username": username
        }
        return self.post(url, payload)

    def login(self, email, password):
        '''
        登录
        :param email: 用户邮箱
        :param password: 用户密码
        :return: 响应data
            eg: {
                'add_time': 127374744,
                'email': 'kevin@126.com',
                'role': 'member',
                'study': False,
                'type': 'site',
                'uid': 16,
                'up_time': 138383838,
                'username': 'kevin'
            }
        '''

        url = '/api/user/login'
        payload = {"email": email, "password": password}
        return self.post(url, payload)


























































