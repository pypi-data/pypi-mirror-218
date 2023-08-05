"""Main module."""
from test_yapi1.group import GroupMixIn
from test_yapi1.project import ProjectMixIn
from test_yapi1.user import UserMixIn


class YApiClient(UserMixIn, GroupMixIn, ProjectMixIn):
    pass
