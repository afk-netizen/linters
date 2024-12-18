import datetime
from model import db, Client, Parking, ClientParking
from flask import Flask, jsonify, request


def create_app(test_config="config.py"):
    app = Flask(__name__)

    app.config.from_pyfile(test_config)

    @app.before_request
    def before_request_func():
        db.create_all()

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    @app.route("/clients", methods=["GET", "POST"])
    def clients():
        if request.method == "GET":
            clients_list = [
                client.to_json() for client in db.session.query(Client).all()
            ]
            return {"All Clients": clients_list}

        elif request.method == "POST":
            name = request.form.get("name")
            surname = request.form.get("surname")
            credit_card = request.form.get("credit_card")
            car_number = request.form.get("car_number")
            print(name, surname, credit_card, car_number)
            client = Client(
                name=name,
                surname=surname,
                credit_card=credit_card,
                car_number=car_number,
            )
            db.session.add(client)
            db.session.commit()
            return client.to_json(), 201

    @app.route("/clients/<int:client_id>", methods=["GET"])
    def one_client(client_id):
        client: Client = db.session.query(Client).get(client_id)
        if client:
            return jsonify(client.to_json()), 200
        return "client is not found"

    @app.route("/parkings", methods=["GET", "POST"])
    def parkings():
        if request.method == "GET":
            parkings_list = [
                parking.to_json() for parking in db.session.query(Parking).all()
            ]
            return {"All parkings": parkings_list}
        elif request.method == "POST":
            address = request.form.get("address")
            opened = request.form.get("opened", type=bool)
            # if opened in ('True', 'true'): opened = True
            # else: opened = False

            count_places = request.form.get("count_places")
            count_available_places = request.form.get("count_available_places")
            parking = Parking(
                address=address,
                opened=opened,
                count_places=count_places,
                count_available_places=count_available_places,
            )
            db.session.add(parking)
            db.session.commit()
            return parking.to_json(), 201

    @app.route("/client_parking", methods=["POST", "DELETE", "GET"])
    def client_parking():

        client_id = request.form.get("client_id", type=int)
        parking_id = request.form.get("parking_id", type=int)
        if request.method == "POST":
            parking = db.session.query(Parking).get(parking_id)
            if parking:
                opened = parking.opened
                count_available_places = parking.count_available_places
                if not opened:
                    return "parking is closed"
                elif count_available_places <= 0:
                    return "parking is not have available places"
                else:
                    time_in = datetime.datetime.now()
                    client_parking = ClientParking(
                        client_id=client_id, parking_id=parking_id, time_in=time_in
                    )
                    db.session.add(client_parking)

                    parking.count_available_places -= 1
                    db.session.commit()
                    return client_parking.to_json(), 201

            else:
                return "parking is not found", 404
        elif request.method == "DELETE":
            client_parking = (
                db.session.query(ClientParking)
                .where(
                    ClientParking.client_id == client_id,
                    ClientParking.parking_id == parking_id,
                )
                .first()
            )
            if client_parking:
                client = db.session.query(Client).get(client_id)
                if not client.credit_card:
                    return "credit card is not found, please try again"
                parking = db.session.query(Parking).get(parking_id)
                parking.count_available_places += 1
                client_parking.time_out = datetime.datetime.now()
                db.session.commit()
                return "", 204
            else:
                return "client or parking is not found", 404

        elif request.method == "GET":
            client_parkings_list = [
                client_parking.to_json()
                for client_parking in db.session.query(ClientParking).all()
            ]
            return {"All client_parkings": client_parkings_list}

    db.init_app(app)

    return app
