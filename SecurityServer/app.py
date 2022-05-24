import secrets

from flask import Flask, request, abort

from EncryptionModule import decrypt
from Models.Models import *
from Common.Utils import bytes_to_string, deserialize

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///security.db'
app.secret_key = secrets.token_bytes(32)
db.app = app
db.init_app(app)
db.create_all()


@app.route('/create', methods=['POST'])
def create():
    if request.data:
        try:
            data = request.json
            uid = data['uid']
            name = data['name']
            create_experiment(uid, name)
            public_key = get_public_key_by_experiment_id(uid)
            if public_key is None:
                raise Exception('Could not find public key for the given UID')
            response = {'public_key': public_key}
            return response
        except Exception as e:
            print(e)
    return abort(400)


@app.route('/publicKey', methods=['GET'])
def get_public_key():
    if request.data:
        try:
            data = request.json
            uid = data['uid']
            public_key = get_public_key_by_experiment_id(uid)
            if public_key is None:
                raise Exception('Could not find public key for the given UID')
            response = {'public_key': public_key}
            return response
        except Exception as e:
            print(e)
    return abort(400)


@app.route('/decrypt', methods=['GET'])
def data_decryption():
    if request.data:
        try:
            data = request.json
            uid = data['uid']
            encrypted_data = data['data']
            private_key = get_private_key_by_experiment_id(uid)
            if private_key is None:
                raise Exception('Could not find private key for the given UID')
            private_key_object = deserialize(private_key)
            decrypted_data = decrypt(private_key_object, encrypted_data)
            return decrypted_data
        except Exception as e:
            print(e)
    return abort(400)


if __name__ == "__main__":
    app.run(debug=True)
    db.create_all()
