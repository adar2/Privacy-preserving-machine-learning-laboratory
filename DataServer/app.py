import secrets
import threading

from flask import Flask, render_template, request, abort, session, url_for, redirect
from Models.Models import *
from sqlalchemy.dialects.postgresql import UUID

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.secret_key = secrets.token_bytes(32)
db.app = app
db.init_app(app)
db.create_all()


def is_valid_uuid(uuid_to_test):
    try:
        uuid_obj = UUID(uuid_to_test)
    except ValueError:
        return False
    return uuid_obj.as_uuid == uuid_to_test

# def execute_experiment(experiment:Experiment)->None:
#     creation_date = experiment.timestamp
#     execution_date = threading.Timer()


@app.route('/submit-results', methods=['POST'])
def submit_results():
    try:
        data_dict = eval(request.data.decode())
        experiment_id = session["eid"]
        experiment = Experiment.query.filter_by(id=experiment_id).first()
        message = Message(experiment=experiment,param_1=data_dict['message1'],param_2=data_dict['message2'])
        add_message(message)
        return redirect("/")
    except Exception as e:
        print(e)
        abort(400)


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
