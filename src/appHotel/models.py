from .database import db
from datetime import datetime


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(75), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    bookings = db.relationship('Booking', backref='client', lazy="dynamic")


class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False, unique=True)
    type = db.Column(db.String(60), nullable=False)
    price = db.Column(db.Float, nullable=False)
    bookings = db.relationship('Booking', backref='room', lazy="dynamic")


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_client = db.Column(db.Integer, db.ForeignKey('client.id'))
    id_room = db.Column(db.Integer, db.ForeignKey('room.id'))
    arrival_date = db.Column(db.DateTime, default=datetime.utcnow)
    departure_date = db.Column(db.DateTime, default=datetime.utcnow)
    statut = db.Column(db.String(50), nullable=True)
