import os
import secrets

from flask import Flask, request, abort

from Common.Constants import DEFAULT_FAILURE_STATUS_CODE, DATA_SERVER_DB_CS
from DataServer.Models.Models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATA_SERVER_DB_CS
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = secrets.token_bytes(32)
db.app = app
db.init_app(app)
db.create_all()


@app.route('/submitResults', methods=['POST'])
def submit_results():
    if request.data:
        try:
            data = request.json
            m1 = data['m1']
            m2 = data['m2']
            uid = data['uid']
            update_experiment_results(uid, m1, m2)
            return 'Success'
        except Exception as e:
            print(e)
    return abort(DEFAULT_FAILURE_STATUS_CODE)


@app.route('/getResults', methods=['GET'])
def get_results():
    if request.data:
        try:
            data = request.json
            uid = data['uid']
            decrypted_data = get_decrypted_data(uid)
            name = get_experiment_name(uid)
            creation_date = get_experiment_creation_date(uid)
            return {'name': name, 'creation_date': creation_date, 'D': decrypted_data[0], 'U': decrypted_data[1]}
        except Exception as e:
            print(e)
    return abort(DEFAULT_FAILURE_STATUS_CODE)


@app.route('/create', methods=['POST'])
def create():
    if request.data:
        try:
            data = request.json
            name = data['name']
            experiment = create_experiment(name)
            add_experiment(experiment)
            response = {'uid': experiment.id, 'public_key': experiment.public_key}
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
            public_key = get_public_key_by_uid(uid)
            if public_key is None:
                raise Exception('Could not find public key for the given UID')
            response = {'public_key': public_key}
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
        config.set('main', 'port', '8080')
        config.set('main', 'debug', 'False')
        config.set('main', 'ssl_context', 'adhoc')
        config.set('main', 'security_server_url', 'https://127.0.0.1:5051')
        with open('config.ini', 'w') as f:
            config.write(f)

    port = int(config.get('main', 'port'))
    debug = bool(config.get('main', 'debug'))
    ssl_context = config.get('main', 'ssl_context')
    url = config.get('main', 'security_server_url')

    init_security_client(url)
    app.run(port=port, debug=debug, ssl_context=ssl_context)
