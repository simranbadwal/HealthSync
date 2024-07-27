from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    notes = db.relationship('Note')

class HealthForm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    allergies = db.Column(db.String(2000), unique=True)
    disease = db.Column(db.String(2000), unique=True)
    symptoms = db.Column(db.String(2000), unique=True)
    medication = db.Column(db.String(2000), unique=True)
    drugs = db.Column(db.String(2000), unique=True)
    extrainfo = db.Column(db.String(2000), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
