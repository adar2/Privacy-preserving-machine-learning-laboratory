import secrets

from flask import Flask, request, abort, redirect

from Common.Constants import DEFAULT_FAILURE_STATUS_CODE, DATA_SERVER_DB_CS
from Models.Models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATA_SERVER_DB_CS
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
            return redirect('/')
            # add_experiment(experiment)
            # response = {'uid': experiment.id, 'public_key': experiment.public_key}
            # return response
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


if __name__ == "__main__":
    app.run(debug=True, ssl_context='adhoc')
