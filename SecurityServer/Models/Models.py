from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime, func

from Common.Constants import KEY_SIZE
from Common.Utils import is_valid_uuid, serialize, generate_uuid
from SecurityServer.EncryptionModule import generate_public_private_keys

db = SQLAlchemy()


class Experiment(db.Model):
    id = db.Column(db.Text(length=36), default=generate_uuid, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    timestamp = db.Column(DateTime(timezone=True), server_default=func.now())
    public_key = db.Column(db.String(KEY_SIZE), nullable=False)
    private_key = db.Column(db.String(KEY_SIZE), nullable=False)


def add_experiment(experiment: Experiment) -> None:
    db.session.add(experiment)
    db.session.commit()


def create_experiment(uid, name):
    if uid is None or name is None or not is_valid_uuid(uid):
        raise Exception('Invalid Arguments')
    public_key, private_key = generate_public_private_keys()
    storable_public_key = serialize(public_key)
    storable_private_key = serialize(private_key)
    new_experiment = Experiment(id=uid, name=name, public_key=storable_public_key, private_key=storable_private_key)
    add_experiment(new_experiment)


def get_public_key_by_experiment_id(uid):
    experiment = get_experiment_by_id(uid)
    if experiment is None:
        return None
    return experiment.public_key


def get_private_key_by_experiment_id(uid):
    experiment = get_experiment_by_id(uid)
    if experiment is None:
        return None
    return experiment.private_key


def get_experiment_by_id(uid) -> Experiment:
    return Experiment.query.filter_by(id=uid).first()
