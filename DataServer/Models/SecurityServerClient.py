import json

import requests


class SecurityServerClient:
    def __init__(self, url):
        self.url = url
        self.headers = {'Content-Type': 'application/json'}
        self.paths = {'create': '/create', 'public_key': '/publicKey', 'encrypt': '/encrypt', 'decrypt': '/decrypt'}

    def create(self, name, uid):
        url = self.url + self.paths['create']
        payload = json.dumps({'name': name, 'uid': uid})
        response = requests.post(headers=self.headers, url=url, data=payload, verify=False)
        if response.status_code != 200:
            return None
        return response.json()['public_key']

    def get_public_key(self, uid):
        url = self.url + self.paths['public_key']
        payload = json.dumps({'uid': uid})
        response = requests.get(headers=self.headers, url=url, data=payload, verify=False)
        if response.status_code != 200:
            return None
        return response.json()['public_key']

    def encrypt(self, uid, data):
        url = self.url + self.paths['encrypt']
        payload = json.dumps({'uid': uid, 'data': data})
        response = requests.get(headers=self.headers, url=url, data=payload, verify=False)
        if response.status_code != 200:
            return None
        return response.json()['encrypted_data']

    def decrypt(self, uid, encrypted_data):
        url = self.url + self.paths['decrypt']
        payload = json.dumps({'uid': uid, 'data': encrypted_data})
        response = requests.get(headers=self.headers, url=url, data=payload, verify=False)
        if response.status_code != 200:
            return None
        return response.json()['decrypted_data']
