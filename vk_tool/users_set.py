from typing import Set, Union
from vk_tool import vk, USER_FIELDS
from vk_tool.user import User


class UsersSet:
    def __init__(self, s: Set[User]):
        self.s = s

    def __repr__(self):
        return f'<UsersSet:{len(self.s)}>'

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
        friends = set()
        friends |= UsersSet._get_users(response['items'])
        n = -(-response['count'] // 1000) * 1000
        for offset in range(1000, n + 1, 1000):
            response = vk.method('friends.get', values={
                'user_id': user.id,
                'offset': offset
            })
            friends |= UsersSet._get_users(response['items'])
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
        members = set()
        members |= UsersSet._get_users(response['items'])
        n = -(-response['count'] // 1000) * 1000 + 1
        for offset in range(1000, n, 1000):
            response = vk.method('groups.getMembers', values={
                'group_id': group_id,
                'offset': offset
            })
            members |= UsersSet._get_users(response['items'])
        return UsersSet(members)

    @staticmethod
    def _get_users(users_ids):
        members = set()

        # split request in 2 parts because vk sometimes can't handle request for 1000 users
        if len(users_ids) <= 500:
            members |= set(
                map(
                    lambda user_dict: User(user_dict),
                    vk.method('users.get', values={
                        'user_ids': ','.join(map(str, users_ids)),
                        'fields': USER_FIELDS,
                        'name_case': 'Nom',
                    })
                )
            )
        else:
            members |= set(
                map(
                    lambda user_dict: User(user_dict),
                    vk.method('users.get', values={
                        'user_ids': ','.join(map(str, users_ids[:500])),
                        'fields': USER_FIELDS,
                        'name_case': 'Nom',
                    })
                )
            )
            members |= set(
                map(
                    lambda user_dict: User(user_dict),
                    vk.method('users.get', values={
                        'user_ids': ','.join(map(str, users_ids[500:])),
                        'fields': USER_FIELDS,
                        'name_case': 'Nom',
                    })
                )
            )
        return members

    # set operations
    def __eq__(self, other):
        if isinstance(other, UsersSet):
            return self.s.__eq__(other.s)
        else:
            raise TypeError('Other should be UsersSet type')

    def __contains__(self, item):
        if isinstance(item, UsersSet):
            return item.s in self.s
        elif isinstance(item, User):
            return item in self.s
        else:
            raise TypeError('in operator is not defined for this type')

    def __or__(self, other):
        if isinstance(other, UsersSet):
            return UsersSet(self.s.__or__(other.s))
        else:
            raise TypeError('')

    def __and__(self, other):
        if isinstance(other, UsersSet):
            return UsersSet(self.s.__and__(other.s))
        else:
            raise TypeError('not defined for this type')

    def __sub__(self, other):
        if isinstance(other, UsersSet):
            return UsersSet(self.s.__sub__(other.s))
        else:
            raise TypeError('not defined for this type')

    def filter(self, func):
        return UsersSet(set(filter(func, self.s)))
