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
        Group members via 'groups.getMembers'
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

    # set operations
    def __eq__(self, other):
        if isinstance(other, UsersSet):
            return self.s.__eq__(other.s)
        else:
            raise TypeError('Other should be UsersSet type')

    def __contains__(self, item):
        if isinstance(item, UsersSet):
            return self.s.__contains__(item.s)
        elif isinstance(item, User):
            return self.s.__contains__(User)
        else:
            raise TypeError('in operator is not defined for this type')

    def __or__(self, other):
        if isinstance(other, UsersSet):
            return self.s.__or__(other.s)
        else:
            raise TypeError('')

    def __and__(self, other):
        if isinstance(other, UsersSet):
            return self.s.__and__(other.s)
        else:
            raise TypeError('not defined for this type')

    def __sub__(self, other):
        if isinstance(other, UsersSet):
            return self.s.__sub__(other.s)
        else:
            raise TypeError('not defined for this type')

    def filter(self, func):
        return set(filter(func, self.s))
