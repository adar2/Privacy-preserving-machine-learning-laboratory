from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    param_1 = db.Column(db.String(200), nullable=False)
    param_2 = db.Column(db.String(200), nullable=False)
    experiment = db.relationship('Experiment', backref=db.backref('messages', lazy=True))
    experiment_id = db.Column(db.Integer, db.ForeignKey('experiment.id',nullable=False))


class Experiment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    # messages = db.relationship('Message', backref='experiment', lazy='dynamic')


@app.route('/', methods=['POST', 'GET'])
def index():
    try:
        ex = Experiment(id=1, name='fuck this shit')
        m = Message(experiment=ex, param_1='daaa', param_2='dddd')
        # ex.messages.add(m)
        db.session.add(ex)
        db.session.add(m)
        db.session.commit()
        return 'Ok'
    except Exception as e:
        print(e)
        return 'There was an issue adding your task'


if __name__ == "__main__":
    app.run()
