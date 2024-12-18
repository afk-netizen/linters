from typing import Dict, Any

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint

db = SQLAlchemy()


class ClientParking(db.Model):
    __tablename__ = "client_parking"
    id = db.Column(db.Integer, nullable=True, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey("clients.id"), nullable=False)
    parking_id = db.Column(db.Integer, db.ForeignKey("parking.id"), nullable=False)
    time_in = db.Column(db.DateTime)
    time_out = db.Column(db.DateTime)

    __table_args__ = (
        UniqueConstraint("client_id", "parking_id", name="uix_client_parking"),
    )

    def __repr__(self):
        return f"<user  {self.client_id} - parking {self.parking_id}>"

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Parking(db.Model):
    __tablename__ = "parking"
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    address = db.Column(db.String, nullable=False)
    opened = db.Column(db.Boolean)
    count_places = db.Column(db.Integer, nullable=False)
    count_available_places = db.Column(db.Integer, nullable=False)
    clients = db.relationship(
        "Client", secondary="client_parking", back_populates="parking"
    )

    def __repr__(self):
        return f"<parking  {self.id}>"

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Client(db.Model):
    __tablename__ = "clients"

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    name = db.Column(db.String, nullable=False)
    surname = db.Column(db.String, nullable=False)
    credit_card = db.Column(db.String)
    car_number = db.Column(db.String)
    parking = db.relationship(
        "Parking", secondary="client_parking", back_populates="clients"
    )

    def __repr__(self):
        return f"<client  {self.name}>"

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
