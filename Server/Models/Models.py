from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    param_1 = db.Column(db.String(200), nullable=False)
    param_2 = db.Column(db.String(200), nullable=False)
    # experiment_id = db.Column(db.String, db.ForeignKey('experiments.id'))
    experiment = db.relationship('Category', backref=db.backref('messages', lazy=True))
    experiment_id = db.Column(db.String, db.ForeignKey('experiment.id'), nullable=False)


class Experiment(db.Model):
    # __tablename__ = 'experiments'
    id = db.Column(db.String(200), primary_key=True, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    # messages = db.relationship('Message', backref='experiment', lazy='dynamic')
