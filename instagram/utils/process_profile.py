from datetime import datetime
import json

path = 'instagram/users'


def process_profile(self, request):
    response = request.response()
    data = response.json()
    now = datetime.strftime(datetime.now(), '%Y-%m-%d=%H:%M:%S')
    with open(f'{path}/{self._username}/{now}-profile.json', 'w') as f:
        json.dump(data, f)

    if data['status'] != 'ok':
        raise Exception(
            f'Error al cargar los datos del usuario {self.username}')

    user = data['data']['user']
    self._fullname = user['full_name']
    self._followers = user['edge_followed_by']['count']
    self._following = user['edge_follow']['count']

    for post in user['edge_owner_to_timeline_media']['edges']:
        _type = post['node']['__typename']
        if _type == 'GraphImage':
            self._posts.append(post['node']['display_url'])
        elif _type == 'GraphVideo':
            self._posts.append(post['node']['video_url'])

    self._is_friend = user['blocked_by_viewer']
