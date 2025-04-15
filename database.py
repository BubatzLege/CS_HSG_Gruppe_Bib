from sqlalchemy import create_engine, Column, Integer, String, Time, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import timedelta


Base = declarative_base()

class Seating(Base):
    __tablename__ = "seating"
    Platznummer = Column(Integer, primary_key=True)
    Stock = Column(String)
    Zustand = Column(String)

class Reservation(Base):
    __tablename__ = "reservations"
    id = Column(Integer, primary_key=True)
    sitznummer = Column(Integer)
    startzeit = Column(String)
    endzeit = Column(String)
    datum = Column(Date)
    user_email = Column(String)

engine = create_engine("sqlite:///database_HSG.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def get_session():
    return Session()


def reserve_time_slot(sitznummer, startzeit, endzeit, datum, user_email):
    session = get_session()
    bestehende = session.query(Reservation).filter_by(sitznummer=sitznummer, datum=datum).all()

    for r in bestehende:
        if not (endzeit <= r.startzeit or startzeit >= r.endzeit):
            return False

    neue_reservierung = Reservation(sitznummer=sitznummer, startzeit=startzeit, endzeit=endzeit, datum=datum, user_email=user_email)
    session.add(neue_reservierung)
    session.commit()
    return True

def delete_reservation(res_id):
    session = get_session()
    res = session.query(Reservation).get(res_id)
    if res:
        session.delete(res)
        session.commit()

def update_reservation(res_id, neues_datum, neue_startzeit, neue_endzeit):
    session = get_session()
    res = session.query(Reservation).get(res_id)
    if res:
        res.datum = neues_datum
        res.startzeit = neue_startzeit
        res.endzeit = neue_endzeit
        session.commit()

def count_weakly_reservations(session, user_email, target_date):
    start_of_week = target_date - timedelta(days=target_date.weekday())
    end_of_week = start_of_week + timedelta(days=6)

    return session.query(Reservation).filter(
        Reservation.user_email == user_email,
        Reservation.datum >= start_of_week,
        Reservation.datum <= end_of_week
    ).count()






















