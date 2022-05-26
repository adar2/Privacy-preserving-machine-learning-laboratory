import requests
import Client.Common as clientCommon
from Common.Utils import serialize, deserialize


def send_new_experiment_request(experiment_name: ""):
    response = requests.post(clientCommon.DATA_SERVER_URL, headers={"Content-Type": "application/json"},
                             data={"name": experiment_name})
    if response.status_code == 200:
        response_json = response.json()
        return clientCommon.SUCCESS, response_json["guid"], deserialize(response_json["publickey"])
    else:
        return clientCommon.FAILURE, None, None


def send_data_upload_request(guid, m1, m2):
    response = requests.post(clientCommon.DATA_SERVER_URL, headers={"Content-Type": "application/json"},
                             data={"m1": serialize(m1), "m2": serialize(m2), "guid": guid})
    if response:
        return clientCommon.SUCCESS
    else:
        return clientCommon.FAILURE
