import os.path
import secrets

from flask import Flask, request, abort

from Common.Utils import deserialize
from SecurityServer.EncryptionModule import decrypt, encrypt
from SecurityServer.Models.Models import *
from Common.Constants import DEFAULT_FAILURE_STATUS_CODE, SECURITY_SERVER_DB_CS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SECURITY_SERVER_DB_CS
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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
    return abort(DEFAULT_FAILURE_STATUS_CODE)


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
    return abort(DEFAULT_FAILURE_STATUS_CODE)


@app.route('/encrypt', methods=['GET'])
def data_encryption():
    if request.data:
        try:
            data = request.json
            uid = data['uid']
            plain_text_data = data['data']
            public_key = get_public_key_by_experiment_id(uid)
            if public_key is None:
                raise Exception('Could not find public key for the given UID')
            public_key_object = deserialize(public_key)
            encrypted_data = encrypt(public_key_object, plain_text_data)
            response = {'encrypted_data': serialize(encrypted_data)}
            return response
        except Exception as e:
            print(e)
    return abort(DEFAULT_FAILURE_STATUS_CODE)


@app.route('/decrypt', methods=['GET'])
def data_decryption():
    if request.data:
        try:
            data = request.json
            uid = data['uid']
            encrypted_data = deserialize(data['data'])
            private_key = get_private_key_by_experiment_id(uid)
            if private_key is None:
                raise Exception('Could not find private key for the given UID')
            private_key_object = deserialize(private_key)
            decrypted_data = decrypt(private_key_object, encrypted_data)
            response = {'decrypted_data': decrypted_data}
            return response
        except Exception as e:
            print(e)
    return abort(DEFAULT_FAILURE_STATUS_CODE)


if __name__ == "__main__":
    from configparser import ConfigParser

    config_file = 'config.ini'
    config = ConfigParser()
    config.read(config_file)
    if not os.path.exists(config_file):
        config.add_section('main')
        config.set('main', 'port', '5051')
        config.set('main', 'debug', 'False')
        config.set('main', 'ssl_context', 'adhoc')
        with open('config.ini', 'w') as f:
            config.write(f)

    port = int(config.get('main', 'port'))
    debug = bool(config.get('main', 'debug'))
    ssl_context = config.get('main', 'ssl_context')

    app.run(port=port, debug=debug, ssl_context=ssl_context)
