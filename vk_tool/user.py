from typing import Dict
from vk_tool import vk, USER_FIELDS
from copy import deepcopy


class User:
    def __init__(self, dict: Dict):
        self.id = int(dict['id'])
        del dict['id']
        self.properties = deepcopy(dict)

    def __hash__(self):
        return hash(self.id)

    @staticmethod
    def new_from_id(id: str):
        response = vk.method('users.get', values={
            'fields': USER_FIELDS,
            'name_case': 'Nom',
            'user_id': id,
        })
        return User(response)

