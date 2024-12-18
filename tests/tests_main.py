import pytest

from .conftest import client
from main import db
from model import Parking
import sys

from model import ClientParking, Client

from .factoryb import ClientFactory, ParkingFactory

sys.path.append("../hw")


@pytest.mark.parametrize(
    "url",
    [
        "/clients",
        "/clients/1",
        "/parkings",
        "/client_parking",
    ],
)
def test_route_status(client, url):
    response = client.get(url)
    assert response.status_code == 200


def test_create_client(client):
    response = client.post(
        "/clients",
        data={
            "name": "name",
            "surname": "surname",
            "credit_card": "12345",
            "car_number": "s777ss",
        },
    )
    assert response.status_code == 201


def test_create_parking(client):
    response = client.post(
        "/parkings",
        data={
            "address": "ufa, parhmenko, 23",
            "opened": True,
            "count_places": 5,
            "count_available_places": 5,
        },
    )

    assert response.status_code == 201


@pytest.mark.parking
def test_client_parking_in(client, db):
    response = client.post("/client_parking", data={"client_id": 1, "parking_id": 1})

    parking = db.session.query(Parking).where(Parking.id == 1).one()
    opened = parking.opened
    assert parking.count_places == parking.count_available_places + 1
    assert opened == True
    assert response.status_code == 201


@pytest.mark.parking
def test_client_parking_out(client, db):
    client.post("/client_parking", data={"client_id": 999, "parking_id": 999})
    parking = db.session.query(Parking).where(Parking.id == 999).one()
    assert parking.count_available_places == 4
    response = client.delete(
        "/client_parking", data={"client_id": 999, "parking_id": 999}
    )
    parking_after = db.session.query(Parking).where(Parking.id == 999).one()
    client = db.session.query(Client).where(Client.id == 999).one()
    client_parking = (
        db.session.query(ClientParking)
        .where(ClientParking.client_id == 999, ClientParking.parking_id == 999)
        .one()
    )
    assert parking_after.count_available_places == 5
    assert client.credit_card
    assert client_parking.time_in < client_parking.time_out
    assert parking.count_places == parking.count_available_places
    assert response.status_code == 204


def test_create_parking_factory(client, db):
    places_before = db.session.query(Parking).count()
    parking = ParkingFactory()
    db.session.commit()
    places_after = db.session.query(Parking).count()
    assert places_before + 1 == places_after
    assert parking.id is not None


def test_create_client_factory(client, db):
    clients_before = db.session.query(Client).count()
    client = ClientFactory()
    db.session.commit()
    clients_after = db.session.query(Client).count()
    assert clients_before + 1 == clients_after
    assert client.id is not None
