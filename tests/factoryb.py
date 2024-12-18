import sys

import factory
import factory.fuzzy as fuzzy
from faker import Faker

from main import db
from model import Client, Parking

sys.path.append("../hw")


class ClientFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Client
        sqlalchemy_session = db.session

    name: factory.Faker = factory.Faker("first_name")
    surname: factory.Faker = factory.Faker("last_name")
    credit_card: fuzzy.FuzzyChoice = fuzzy.FuzzyChoice(choices=(None, "some_card"))
    car_number: fuzzy.FuzzyText = fuzzy.FuzzyText(length=5)


class ParkingFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Parking
        sqlalchemy_session = db.session

    address: factory.LazyAttribute = factory.LazyAttribute(lambda x: Faker().street_address())
    opened: fuzzy.FuzzyChoice = fuzzy.FuzzyChoice(choices=(True, False))
    count_places: factory.Faker = factory.Faker("pyint", min_value=0, max_value=5)
    count_available_places: factory.LazyAttribute = factory.LazyAttribute(lambda x: x.count_places)
