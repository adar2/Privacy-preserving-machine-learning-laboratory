import json

import requests

import Client.Common
import Client.Common as clientCommon
from Common.Utils import serialize, deserialize


class DataServerClient:
    def __init__(self, url=Client.Common.DATA_SERVER_URL):
        self.url = url
        self.headers = {'Content-Type': 'application/json'}
        self.paths = {'create': '/create', 'submit_results': '/submitResults'}

    def send_new_experiment_request(self, experiment_name: ""):
        url = self.url + self.paths['create']
        payload = json.dumps({'name': experiment_name})
        response = requests.post(headers=self.headers, url=url, data=payload, verify=False)
        if response.status_code == 200:
            response_json = response.json()
            return clientCommon.SUCCESS, response_json["uid"], deserialize(response_json["public_key"])
        else:
            return clientCommon.FAILURE, None, None

    def send_data_upload_request(self, uid, m1, m2):
        url = self.url + self.paths['submit_results']
        payload = json.dumps({"m1": serialize(m1), "m2": serialize(m2), "uid": uid})
        response = requests.post(headers=self.headers, url=url, data=payload, verify=False)
        if response:
            return clientCommon.SUCCESS
        else:
            return clientCommon.FAILURE
