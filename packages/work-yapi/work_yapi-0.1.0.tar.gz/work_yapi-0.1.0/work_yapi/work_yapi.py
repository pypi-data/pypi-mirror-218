"""Main module."""
from work_yapi.group import GroupMixIn
from work_yapi.projec import ProjectMixIn
from work_yapi.user import UserMixIn


class WorkYapi(GroupMixIn,UserMixIn,ProjectMixIn):
    pass

