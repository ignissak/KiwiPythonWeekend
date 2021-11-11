import datetime
from typing import Iterator

from sqlalchemy import create_engine, Column, Integer, TEXT, TIMESTAMP, FLOAT, VARCHAR, Sequence
from sqlalchemy.dialects.mysql import ENUM
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, aliased

import config
from slugify import slugify


Base = declarative_base()


class Journey(Base):
    __tablename__ = 'journeys_bordas'
    id = Column(Integer, Sequence("journeys_bordas_id"), primary_key=True)
    origin = Column(TEXT, nullable=False)
    destination = Column(TEXT, nullable=False)
    departure_datetime = Column(TIMESTAMP)
    arrival_datetime = Column(TIMESTAMP)
    carrier = Column(TEXT, index=True)
    vehicle_type = Column(ENUM("airplane", "bus", "train", name="vehicle_type_enum"))
    price = Column(FLOAT)
    currency = Column(VARCHAR(3))


class Database:
    engine = create_engine(config.DATABASE_URL, echo=False)
    SessionMaker = sessionmaker(engine)

    def __init__(self):
        Base.metadata.create_all(bind=self.engine)
        pass

    def create_session(self) -> Iterator[Session]:
        db = self.SessionMaker()
        try:
            yield db
        finally:
            db.close()

    def put_in_dummy(self):
        for session in self.create_session():
            journey = Journey(
                origin="Bratislava",
                destination="Prague",
                departure_datetime=datetime.datetime(2021, 8, 30, 8, 0),
                arrival_datetime=datetime.datetime(2021, 8, 30, 16, 0),
                carrier="REGIOJET",
                vehicle_type="train",
                price="13",
                currency="EUR"
            )
            session.add(journey)

            journey = Journey(
                origin="Prague",
                destination="Zagreb",
                departure_datetime=datetime.datetime(2021, 8, 30, 18, 0),
                arrival_datetime=datetime.datetime(2021, 8, 31, 8, 0),
                carrier="REGIOJET",
                vehicle_type="train",
                price="400",
                currency="CZK"
            )
            session.add(journey)

            session.commit()

    def get_journeys_by_destination(self, destination):
        for session in self.create_session():
            return session.query(Journey).filter(Journey, Journey.destination == destination).all()

    def insert_journey(self, origin, destination, departure_datetime, arrival_datetime, carrier, vehicle_type, price,
                       currency):
        for session in self.create_session():
            session.add(Journey(origin, destination,
                                departure_datetime, arrival_datetime, carrier, vehicle_type, price, currency))
            session.commit()

    def find_journeys(self, origin: str, destination: str, from_date: datetime, to_date: datetime):
        for session in self.create_session():
            return session.query(Journey).filter(Journey.origin == slugify(origin), Journey.destination == slugify(destination),
                                                 Journey.departure_datetime > from_date,
                                                 Journey.arrival_datetime < to_date).all()

    def find_combinations(self, origin, destination, date):
        for session in self.create_session():
            Journey2 = aliased(Journey)
            for segment1, segment2 in (
                    session.query(Journey, Journey2)
                            .filter(Journey.origin == origin and Journey2.destination == destination
                                    and Journey.departure_datetime > date)
                            .join(Journey2, Journey.destination == Journey2.origin)
                            .all()):
                combination = {
                    "origin": segment1.origin,
                    "stopover": segment1.destination,
                    "destination": segment2.destination,
                    "origin_departure": segment1.departure_datetime.isoformat(),
                    "layover_arrival": segment1.arrival_datetime.isoformat(),
                    "layover_departure": segment2.departure_datetime.isoformat(),
                    "destination_arrival": segment2.arrival_datetime.isoformat()
                }
                return combination
