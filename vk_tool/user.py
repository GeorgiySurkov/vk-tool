from typing import Dict, Union
from vk_tool import vk, USER_FIELDS
from copy import deepcopy


class User:
    def __init__(self, dict: Dict):
        self.id = dict['id']
        del dict['id']
        self.properties = deepcopy(dict)

    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        if isinstance(other, User):
            return self.id == other.id
        else:
            return False

    @staticmethod
    def new_from_id(id: Union[str, int]):
        if isinstance(id, str):
            if id.count(',') > 0:
                raise ValueError('One user id expected, More than one received instead.')
        values = {
            'fields': USER_FIELDS,
            'name_case': 'Nom',
            'user_ids': id,
        }
        user_dict = vk.method('users.get', values=values)[0]
        return User(user_dict)

