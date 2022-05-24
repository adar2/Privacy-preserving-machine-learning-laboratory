import secrets

from flask import Flask, render_template, request, abort, session, redirect

from Common.Utils import is_valid_uuid
from Models.Models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.secret_key = secrets.token_bytes(32)
db.app = app
db.init_app(app)
db.create_all()


@app.route('/submit-results', methods=['POST'])
def submit_results():
    try:
        return redirect("/")
    except Exception as e:
        print(e)
        abort(400)


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


@app.route('/', methods=['POST', 'GET'])
def index():
    try:
        if request.method == 'POST':
            if request.form['action'] is None:
                abort(404)
            action = request.form['action']
            if action == 'join_experiment':
                uid = request.form['experiment_id']
                if not is_valid_uuid(uid):
                    return 'id is not valid'
                ex = Experiment.query.filter_by(id=uid).first()
                if ex is not None:
                    return render_template('templates/experiment.html', name=ex.name, id=ex.id)
                return "Id doesn't exists"
            if action == 'create_experiment':
                ex = Experiment(name=request.form['experiment_name'])
                add_experiment(ex)
                session["eid"] = ex.id
                return render_template('templates/experiment.html', name=ex.name, id=ex.id)
        return render_template('templates/index.html')
    except Exception as e:
        print(e)
        return 'There was an issue adding your task'


if __name__ == "__main__":
    app.run(debug=True)
    db.create_all()
