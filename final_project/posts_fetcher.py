import vk
import time
from post import Post
from conf import *


session = vk.Session(access_token=ACCESS_TOKEN)
vk_api = vk.API(session)

response = vk_api.wall.get(owner_id=OWNER_ID, v=VERSION, count=100, offset=0)
raw_posts = response['items']

for i in range(response['count'] // 100 + 1):
    curr_response = vk_api.wall.get(owner_id=OWNER_ID, v=VERSION, count=100,
                                    offset=100 * (i + 1))
    time.sleep(0.3)
    raw_posts += curr_response['items']

posts = []
for raw_post in raw_posts:
    if 'attachments' not in raw_post:
        posts.append(Post(raw_post['id'], raw_post['date'], raw_post['text'],
                     raw_post['likes']['count']))
