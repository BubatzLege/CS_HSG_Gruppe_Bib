from datetime import date
from apscheduler.schedulers.background import BackgroundScheduler
from database import get_session, Reservation  # dein bestehendes DB-Modul

def clean_old_reservations():
    session = get_session()
    today = date.today()

    # Verwende 'datum' statt 'date' als Spaltenname
    old_reservations = session.query(Reservation).filter(Reservation.datum < today).all()

    if old_reservations:
        for res in old_reservations:
            session.delete(res)
        session.commit()
        print(f"{len(old_reservations)} veraltete Reservation(en) gelöscht.")
    else:
        print("Keine veralteten Reservationen gefunden.")

    session.close()

# Scheduler initialisieren
scheduler = BackgroundScheduler()
scheduler.add_job(clean_old_reservations, 'cron', hour=0, minute=0)
scheduler.start()

# Beim Programmende den Scheduler sauber beenden
import atexit
atexit.register(lambda: scheduler.shutdown())

