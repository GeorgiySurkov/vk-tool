from vk_api import VkApi
from pprint import pprint

vk = VkApi(token='5833f0eb5833f0eb5833f0eba1585e000f558335833f0eb05fa7d5b8ea1893583b51fdb')
fields = ['photo_50', 'city', 'verified', 'can_post', 'counters']
user_ids = ['aklwfnaswnfas']
result = vk.method('users.get', values={
    'fields': ','.join(fields),
    'name_case': 'Nom',
    'user_ids': ','.join(user_ids),
})

pprint(result)
