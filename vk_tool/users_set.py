from typing import Set
from vk_tool import User


class UsersSet:
    def __init__(self, s: Set[User]):
        self.s = s

    @staticmethod
    def new_from_user_friends(user):
        pass

    @staticmethod
    def new_from_public_subscribers(public):
        pass
