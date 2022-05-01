import secrets
from flask import Flask, render_template, request, abort,session,url_for
from Models.Models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.secret_key = secrets.token_bytes(32)
db.init_app(app)


def is_valid_uuid(uuid_to_test):
    try:
        uuid_obj = UUID(uuid_to_test)
    except ValueError:
        return False
    return uuid_obj.as_uuid == uuid_to_test


@app.route('/submit-results',methods=['POST'])
def submit_results():
    try:
        experiment_id = session["eid"]
        print(request.data)
        return render_template('index.html')
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
                    return render_template('experiment.html', name=ex.name, id=ex.id)
                return "Id doesn't exists"
            if action == 'create_experiment':
                ex = Experiment(name=request.form['experiment_name'])
                add_experiment(ex)
                session["eid"] = ex.id
                return render_template('experiment.html',name=ex.name,id=ex.id)
        return render_template('index.html')
    except Exception as e:
        print(e)
        return 'There was an issue adding your task'


if __name__ == "__main__":
    app.run(debug=True)
