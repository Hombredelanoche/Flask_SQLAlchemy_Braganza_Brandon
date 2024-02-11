from flask import Blueprint, render_template, request, jsonify
from .database import db
from .models import Client, Room, Booking
from datetime import datetime


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
    return jsonify({'message': 'Des utilisateurs ont bien été enregistrés en base de données.'})


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

    db.session.add_all(basicRoom, prestigeRoom, deluxeRoom)
    db.session.commit()
    return jsonify({'message': 'Les chambres ont bien été crééés'})


@main.route('/api/rooms/reserved')
def roomReserved():
    invalaibleRoom = [
        Booking(id_client=1, id_room=6, arrival_date='2024-02-11 14:00:00',
                departure_date='2024-02-14 11:00:00', statut='Payed & Reserved'),
        Booking(id_client=2, id_room=15, arrival_date='2024-02-13 14:00:00',
                departure_date='2024-02-15 11:00:00', statut='Reserved'),
        Booking(id_client=3, id_room=10, arrival_date='2024-03-1 14:00:00',
                departure_date='2024-03-10 11:00:00', statut='Reserved'),
        Booking(id_client=4, id_room=2, arrival_date='2024-03-20 14:00:00',
                departure_date='2024-03-24 11:00:00', statut='Waitlist'),
        Booking(id_client=5, id_room=8, arrival_date='2024-04-15 14:00:00',
                departure_date='2024-04-30 11:00:00', statut='Payed & Reserved')
    ]

    db.session.add_all(invalaibleRoom)
    db.session.commit()
    return jsonify({'message': 'Ces chambres ne sont plus disponibles.'})


# N'hésitez pas à changer les dates dans les paramétres de l'adresse URL.
# ?arrival_date=2024-02-11&departure_date=2024-02-14
@main.route('/api/rooms/available')
def roomsAvailable():
    arrival_date_str = request.args.get('arrival_date')
    departure_date_str = request.args.get('departure_date')

    if arrival_date_str is None or departure_date_str is None:
        return jsonify({'error': 'Les dates d\'arrivée et de départ doivent être fournies'}), 400

    arrival_date = datetime.strptime(arrival_date_str, '%Y-%m-%d')
    departure_date = datetime.strptime(departure_date_str, '%Y-%m-%d')

    available_rooms = []

    rooms = Room.query.all()

    for room in rooms:
        is_available = True
        for booking in room.bookings:
            if arrival_date < booking.departure_date and departure_date > booking.arrival_date:
                is_available = False
                break
        if is_available:
            available_rooms.append(
                {'room_number': room.number, 'room_type': room.type, 'price': room.price})

    return jsonify({'available_rooms': available_rooms})


# Exemple de requête json pour ajouter une réservation
# {"id_client": 1, "id_room": 4, "arrival_date": "2024-06-19", "departure_date": "2024-06-30", "statut": "Confirmée"}
# A ajouter dans le body de la requête json
@main.route('/api/bookingRoom', methods=['POST'])
def bookingRoom():
    data = request.json
    id_client = data.get('id_client')
    arrival_date = datetime.strptime(
        data.get('arrival_date'), '%Y-%m-%d').date()
    departure_date = datetime.strptime(
        data.get('departure_date'), '%Y-%m-%d').date()

    available_room = Room.query.filter(
        ~Room.bookings.any(
            (Booking.arrival_date <= departure_date) & (
                Booking.departure_date >= arrival_date)
        )
    ).first()

    if available_room:
        reservation = Booking(
            id_client=id_client,
            id_room=available_room.id,
            arrival_date=arrival_date,
            departure_date=departure_date,
            statut="Confirmé"
        )
    db.session.add(reservation)
    db.session.commit()
    return jsonify({"message": "Réservation créée avec succès"}), 201
# else:
#             return jsonify({"message": "La chambre n'est pas disponible à cette date"}), 400


# Annulation de Réservation
@main.route('/api/reserved/<int:reservation_id>', methods=["DELETE"])
def cancel_reservation(reservation_id):
    try:
        reservation = Booking.query.get(reservation_id)
        if reservation is None:
            return jsonify({'message': 'Réservation introuvable'}), 404

        db.session.delete(reservation)
        db.session.commit()

        return jsonify({'message': 'Réservation annulée avec succès'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500


# Gestionnaire des chambres "Créer"
@main.route('/api/chambres', methods=['POST'])
def add_room():
    try:
        data = request.json
        number = data.get('numero')
        room_type = data.get('type')
        price = data.get('prix')

        if not number or not room_type or not price:
            return jsonify({'message': 'Tous les champs (numero, type, prix) sont obligatoires'}), 400

        new_room = Room(number=number, type=room_type, price=price)
        db.session.add(new_room)
        db.session.commit()

        return jsonify({'message': 'Chambre ajoutée avec succès'}), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 500


# Gestionnaire des chambres "Modifier"
@main.route('/api/chambres/<int:room_id>', methods=['PUT'])
def update_room(room_id):
    try:
        data = request.json
        number = data.get('numero')
        room_type = data.get('type')
        price = data.get('prix')

        if not number or not room_type or not price:
            return jsonify({'message': 'Tous les champs (numero, type, prix) sont obligatoires'}), 400

        room = Room.query.get(room_id)
        if room is None:
            return jsonify({'message': 'Chambre introuvable'}), 404

        room.number = number
        room.type = room_type
        room.price = price

        db.session.commit()

        return jsonify({'message': 'Chambre modifiée avec succès'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500


# Gestionnaire des chambres "Supprimer"
@main.route('/api/chambres/<int:room_id>', methods=['DELETE'])
def delete_room(room_id):
    try:
        room = Room.query.get(room_id)
        if room is None:
            return jsonify({'message': 'Chambre introuvable'}), 404

        db.session.delete(room)
        db.session.commit()

        return jsonify({'message': 'Chambre supprimée avec succès'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500
