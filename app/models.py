from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import MetaData

naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)   
    phone_no = db.Column(db.String(15), unique=True)
    created_at =db.Column(db.DateTime, default=datetime.utcnow)

    attempts = db.relationship('Attempt', backref='user', cascade='all, delete-orphan')

problem_pattern = db.Table('problem_pattern',                     #association table
    db.Column('problem_id', db.Integer, db.ForeignKey('problem.problem_id'), primary_key=True),
    db.Column('pattern_id', db.Integer, db.ForeignKey('pattern.id'), primary_key=True)
)

class Pattern(db.Model):
    __tablename__ = 'pattern'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    pattern_name = db.Column(db.String(250), unique=True, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Problem(db.Model):
    __tablename__ = 'problem'
    problem_id = db.Column(db.Integer, primary_key=True)
    problem_number = db.Column(db.Integer, unique=True)
    title = db.Column(db.String(250), unique=True)
    difficulty = db.Column(db.String(10))
    link = db.Column(db.Text)

    patterns = db.relationship('Pattern', secondary=problem_pattern,backref='problems')
    attempts = db.relationship('Attempt', backref='problem', cascade='all, delete-orphan')


class Attempt(db.Model):
    __tablename__ = 'attempt'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    problem_id = db.Column(db.Integer, db.ForeignKey('problem.problem_id', ondelete='CASCADE'), nullable=False)
    confidence = db.Column(db.Integer)
    time_taken_mins = db.Column(db.Integer)
    solved = db.Column(db.Boolean)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)