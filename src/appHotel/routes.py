from flask import Blueprint, render_template, request, jsonify
from .database import db
from .models import Client, Room, Booking


main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/api/inscription')
def inscription():

    newClients = [
        Client(name='Richard', email='CoeurDeLion@gmail.com'),
        Client(name='Mangue', email='DeBol@gmail.com'),
        Client(name='Gare', email='Atwa@gmail.com'),
        Client(name='Assassin', email='Sensible@gmail.com'),
        Client(name='JackLondon', email='MartinEden@gmail.com')
    ]

    db.session.add_all(newClients)
    db.session.commit()


@main.route('/api/createRoom')
def createRooms():
    basicRoom = [
        Room(number=10, type='basic', price=79.99),
        Room(number=11, type='basic', price=79.99),
        Room(number=12, type='basic', price=79.99),
        Room(number=13, type='basic', price=79.99),
        Room(number=14, type='basic', price=79.99),
        Room(number=15, type='basic', price=79.99),
    ]

    prestigeRoom = [
        Room(number=100, type='prestige', price=129.99),
        Room(number=101, type='prestige', price=129.99),
        Room(number=102, type='prestige', price=129.99),
        Room(number=103, type='prestige', price=129.99),
        Room(number=104, type='prestige', price=129.99),
        Room(number=105, type='prestige', price=129.99),
    ]

    deluxeRoom = [
        Room(number=200, type='luxury', price=229.99),
        Room(number=201, type='luxury', price=229.99),
        Room(number=202, type='luxury', price=229.99),
        Room(number=203, type='luxury', price=229.99),
        Room(number=204, type='luxury', price=229.99),
        Room(number=205, type='luxury', price=229.99),
    ]

    db.session.add_all(basicRoom)
    db.session.add_all(prestigeRoom)
    db.session.add_all(deluxeRoom)
    db.session.commit()


@main.route('/api/chambres/disponibles', methodes=['GET'])
def roomAvailable():
    arrival_date = request.args.get('arrival_date')
    departure_date = request.args.get('departure_date')

    if not (arrival_date and departure_date):
        return jsonify({'message': 'Les dates de recherche sont nécessaires'})
