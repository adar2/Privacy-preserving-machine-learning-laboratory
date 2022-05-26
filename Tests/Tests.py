import json

from Client.DataServerClient import DataServerClient
from Common.Utils import deserialize, serialize

if __name__ == '__main__':
    client = DataServerClient('https://127.0.0.1:5000')
    status, uid, public_key = client.send_new_experiment_request('ExperimentName')
    m1 = public_key.encrypt(17)
    m2 = public_key.encrypt(13)
    client.send_data_upload_request(uid,m1,m2)
    print(status, uid, public_key)