from typing import Dict, Union
from vk_tool import vk, USER_FIELDS
from copy import deepcopy


class User:
    def __init__(self, properties_dict: Dict):
        self.id = properties_dict['id']
        del properties_dict['id']
        self.properties = deepcopy(properties_dict)

    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        if isinstance(other, User):
            return self.id == other.id
        else:
            return False

    def __repr__(self):
        return f'<User: {self.id}, {self.properties["first_name"]} {self.properties["second_name"]}>'

    @staticmethod
    def new_from_id(user_id: Union[str, int]):
        if isinstance(user_id, str):
            if user_id.count(',') > 0:
                raise ValueError('One user id expected, More than one received instead.')
        values = {
            'fields': USER_FIELDS,
            'name_case': 'Nom',
            'user_ids': user_id,
        }
        user_dict = vk.method('users.get', values=values)[0]
        return User(user_dict)
