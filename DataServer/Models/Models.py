import uuid

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime, func

from Common.Constants import KEY_SIZE
from DataServer.Models.SecurityServerClient import SecurityServerClient

db = SQLAlchemy()
client = SecurityServerClient()


class Experiment(db.Model):
    id = db.Column(db.Text(length=36), default=lambda: str(uuid.uuid4()), primary_key=True)
    timestamp = db.Column(DateTime(timezone=True), server_default=func.now())
    name = db.Column(db.String(200), nullable=False)
    public_key = db.Column(db.String(KEY_SIZE), nullable=True)
    cumulative_sum = db.Column(db.String(KEY_SIZE), nullable=True)


def add_experiment(experiment: Experiment) -> None:
    db.session.add(experiment)
    db.session.commit()


def get_experiment_by_id(uid) -> Experiment:
    return Experiment.query.filter_by(id=uid).first()


def create_experiment(name):
    new_experiment = Experiment(name=name)
    public_key = client.get_public_key(name, new_experiment.id)
    new_experiment.public_key = public_key
    add_experiment(new_experiment)
