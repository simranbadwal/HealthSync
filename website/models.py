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
    speciality = db.Column(db.String(150))
    isDoctor = db.Column(db.Boolean, default=False)
    notes = db.relationship('Note')
    primary_id = db.Column(db.Integer)

class HealthForm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    allergies = db.Column(db.String(2000))
    disease = db.Column(db.String(2000))
    symptoms = db.Column(db.String(2000))
    medication = db.Column(db.String(2000))
    drugs = db.Column(db.String(2000))
    extrainfo = db.Column(db.String(2000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
