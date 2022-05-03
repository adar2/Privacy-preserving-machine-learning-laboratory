import uuid
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime, func

db = SQLAlchemy()


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    param_1 = db.Column(db.String(200), nullable=False)
    param_2 = db.Column(db.String(200), nullable=False)
    experiment = db.relationship('Experiment', backref=db.backref('messages', lazy=True))
    experiment_id = db.Column(db.Text(length=36), db.ForeignKey('experiment.id'), nullable=False)


class Experiment(db.Model):
    id = db.Column(db.Text(length=36), default=lambda: str(uuid.uuid4()), primary_key=True)
    timestamp = db.Column(DateTime(timezone=True), server_default=func.now())
    name = db.Column(db.String(200), nullable=False)


def add_experiment(experiment: Experiment) -> None:
    db.session.add(experiment)
    db.session.commit()


def get_experiment_by_id(uid) -> Experiment:
    return Experiment.query.filter_by(id=uid).first()


def add_message(message: Message) -> None:
    db.session.add(message)
    db.session.commit()
