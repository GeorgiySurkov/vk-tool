from typing import Set, Union
from vk_tool import vk, USER_FIELDS
from vk_tool.user import User


class UsersSet:
    def __init__(self, s: Set[User]):
        self.s = s

    @staticmethod
    def new_from_user_friends(user: User):
        """
        Create UsersSet instance from 
        User friends via 'friends.get'
        vk api method
        """
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
    def new_from_group_members(group_id: Union[int, str]):
        """
        Create UsersSet instance from
        Group members via 'grups.getMembers'
        vk api method
        """
        response = vk.method('groups.getMembers', values={
            'group_id': group_id
        })
        members = set(
            map(
                lambda user_dict: User(user_dict),
                vk.method('users.get', values={
                    'user_ids': ','.join(map(str, response['items'])),
                    'fields': USER_FIELDS,
                    'name_case': 'Nom',
                })
            )
        )
        return UsersSet(members)

