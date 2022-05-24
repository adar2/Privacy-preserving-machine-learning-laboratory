import requests


class SecurityServerClient:
    def __init__(self):
        self.url = ''
        self.session = requests.session()

    def get_public_key(self, name, uid):
        payload = {'name': name, 'uid': uid}
        response = self.session.post(headers={'Content-Type': 'application/json'}, url='someurl', data=payload)
        return response.json()['public_key']
