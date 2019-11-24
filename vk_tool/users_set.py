from typing import Set
from vk_tool import vk, USER_FIELDS
from vk_tool.user import User


class UsersSet:
    def __init__(self, s: Set[User]):
        self.s = s

    @staticmethod
    def new_from_user_friends(user: User):
        response = vk.method('friends.get', values={
            'user_id': user.id,
        })
        friends = set(
            map(
                lambda user_dict: User(user_dict), 
                vk.method('users.get', values={
                    'user_ids': ','.join(map(str, response['items'])),
                    'fields': USER_FIELDS,
                    'name_case': 'Nom',
                }),
            )
        )
        return UsersSet(friends)

    @staticmethod
    def new_from_community_subscribers(public):
        pass

    def __repr__(self):
        return self.s.__repr__()
