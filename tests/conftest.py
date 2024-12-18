from datetime import datetime

import pytest

from main import create_app, db as _db
from model import Client, Parking, ClientParking
import datetime
import sys
sys.path.append("../hw")

@pytest.fixture
def app():
    _app = create_app()
    _app.config["TESTING"] = True
    _app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"

    with _app.app_context():
        _db.create_all()
        user = Client(id=1,
                      name="name1",
                      surname="surname1",
                      credit_card='54133',
                      car_number='s777sd')
        parking = Parking(id=1,
                          address="ufa, parhmenko, 24",
                          opened=True,
                          count_places=5,
                          count_available_places=5)
        _db.session.add(user)
        _db.session.add(parking)

        user = Client(id=999,
                    name="name",
                    surname="surname",
                    credit_card='12345',
                    car_number='s777ss')
        parking = Parking(id=999,
                          address="ufa, parhmenko, 23",
                          opened=True,
                          count_places=5,
                          count_available_places=5)
        _db.session.add(user)
        _db.session.add(parking)

        _db.session.commit()

        yield _app
        _db.session.close()
        _db.drop_all()


@pytest.fixture
def client(app):
    client = app.test_client()
    yield client


@pytest.fixture
def db(app):
    with app.app_context():
        yield _db