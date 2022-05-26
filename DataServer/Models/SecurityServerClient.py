import json

import requests


class SecurityServerClient:
    def __init__(self, url='https://127.0.0.1:5051'):
        self.url = url
        self.session = requests.session()
        self.headers = {'Content-Type': 'application/json'}
        self.paths = {'create': '/create'}

    def get_public_key(self, name, uid):
        url = self.url + self.paths['create']
        payload = json.dumps({'name': name, 'uid': uid})
        response = self.session.post(headers=self.headers, url=url, data=payload, verify=False)
        return response.json()['public_key']
