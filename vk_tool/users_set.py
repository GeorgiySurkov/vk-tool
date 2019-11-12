from typing import Set
from vk_tool import User, vk


class UsersSet:
    def __init__(self, s: Set[User]):
        self.s = s

    @staticmethod
    def new_from_user_friends(user: User):
        response = vk.method('friends.get', values={
            'user_id': user.id,
        })
        friends = set()
        for user in response:
            friends.add(User(user))
        return UsersSet(friends)

    @staticmethod
    def new_from_public_subscribers(public):
        pass
