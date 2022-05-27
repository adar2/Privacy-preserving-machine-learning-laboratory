from flask_sqlalchemy import SQLAlchemy
from phe import EncryptedNumber, PaillierPublicKey
from sqlalchemy import DateTime, func

from Common.Utils import generate_uuid, deserialize, serialize
from DataServer.Models.SecurityServerClient import SecurityServerClient

db = SQLAlchemy()
client = SecurityServerClient()


class Experiment(db.Model):
    id = db.Column(db.Text(length=36), default=generate_uuid, primary_key=True)
    timestamp = db.Column(DateTime(timezone=True), server_default=func.now())
    name = db.Column(db.String(), nullable=False)
    public_key = db.Column(db.String(), nullable=True)
    D_cumulative_sum = db.Column(db.String(), nullable=True)
    U_cumulative_sum = db.Column(db.String(), nullable=True)


def add_experiment(experiment: Experiment) -> None:
    db.session.add(experiment)
    db.session.commit()


def get_experiment_by_id(uid) -> Experiment:
    return Experiment.query.filter_by(id=uid).first()


def get_default_encrypted_number(public_key):
    public_key_obj = deserialize(public_key)
    if not isinstance(public_key_obj, PaillierPublicKey):
        raise Exception('Invalid object type')
    return public_key_obj.encrypt(0)


def get_public_key_by_uid(uid):
    return client.get_public_key(uid)


def create_experiment(name) -> Experiment:
    new_experiment = Experiment(id=generate_uuid(), name=name)
    public_key = client.create(name, new_experiment.id)
    new_experiment.public_key = public_key
    default_number = get_default_encrypted_number(public_key)
    new_experiment.D_cumulative_sum = serialize(default_number)
    new_experiment.U_cumulative_sum = serialize(default_number)
    return new_experiment


def get_decrypted_data(uid):
    experiment = get_experiment_by_id(uid)
    if experiment is None:
        raise Exception(f'Could not find experiment with uid={uid}')
    D = experiment.D_cumulative_sum
    U = experiment.U_cumulative_sum
    decrypted_D = client.decrypt(uid, D)
    decrypted_U = client.decrypt(uid, U)
    return decrypted_D, decrypted_U


def update_experiment_results(uid, m1, m2) -> None:
    experiment = get_experiment_by_id(uid)
    if experiment is None:
        raise Exception(f'Could not find experiment with uid={uid}')
    D = deserialize(experiment.D_cumulative_sum)
    U = deserialize(experiment.U_cumulative_sum)
    m1 = deserialize(m1)
    m2 = deserialize(m2)
    D += m1
    U += m2
    experiment.D_cumulative_sum = serialize(D)
    experiment.U_cumulative_sum = serialize(U)
    db.session.commit()
