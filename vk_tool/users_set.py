from typing import Set, Union
from vk_tool import vk, USER_FIELDS
from vk_tool.user import User
import multiprocessing as mp


def _get_group_members_proc(_offset, _group_id, _q, _response=None):
    if _response is None:
        _response = vk.method('groups.getMembers', values={
            'group_id': _group_id,
            'offset': _offset
        })
    members = get_users(_response['items'])
    _q.put(members)


def _get_user_friends_proc(_offset, _user_id, _q, _response=None):
    if _response is None:
        _response = vk.method('friends.get', values={
            'user_id': _user_id,
            'offset': _offset
        })
    members = get_users(_response['items'])
    _q.put(members)


def get_users(users_ids):
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
        users_packs_expected = -(-response['count'] // 1000)
        q = mp.Queue()
        p = mp.Process(target=_get_user_friends_proc, args=(0, user.id, q, response))
        p.start()
        processes = [p]
        for offset in range(1000, response['count'], 1000):
            p = mp.Process(target=_get_user_friends_proc, args=(offset, user.id, q, None))
            p.start()
            processes.append(p)
        friends = set()
        users_packs_received = 0
        while users_packs_received < users_packs_expected:
            while not q.empty():
                friends |= q.get()
                users_packs_received += 1
        # friends |= UsersSet._get_users(response['items'])
        # n = -(-response['count'] // 1000) * 1000
        # for offset in range(1000, n + 1, 1000):
        #     response = vk.method('friends.get', values={
        #         'user_id': user.id,
        #         'offset': offset
        #     })
        #     friends |= UsersSet._get_users(response['items'])
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
        users_packs_expected = -(-response['count'] // 1000)
        q = mp.Queue()
        p = mp.Process(target=_get_group_members_proc, args=(0, group_id, q, response))
        p.start()
        processes = [p]
        for offset in range(1000, response['count'], 1000):
            p = mp.Process(target=_get_group_members_proc, args=(offset, group_id, q, None))
            p.start()
            processes.append(p)
        members = set()
        users_packs_received = 0
        while users_packs_received < users_packs_expected:
            while not q.empty():
                members |= q.get()
                users_packs_received += 1
        return UsersSet(members)

    def __iter__(self):
        return iter(self.s)

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
