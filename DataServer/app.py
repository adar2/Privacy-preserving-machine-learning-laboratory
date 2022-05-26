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
            name = data['name']
            experiment = create_experiment(name)
            add_experiment(experiment)
            response = {'uid': experiment.id, 'public_key': experiment.public_key}
            return response
        except Exception as e:
            print(e)
    return abort(400)


if __name__ == "__main__":
    app.run(debug=True, ssl_context='adhoc')
    db.create_all()
