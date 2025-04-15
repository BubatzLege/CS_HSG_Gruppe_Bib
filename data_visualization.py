import pandas as pd
from database import get_session, Reservation, Seating

def create_reservation_dataframe():
    session = get_session()
    reservations = session.query(Reservation).all()
    seating = session.query(Seating).all()

    data = []
    for r in reservations:
        seat = next((s for s in seating if s.Platznummer == r.sitznummer), None)
        if seat:
            data.append({
                "Datum": r.datum,
                "Uhrzeit": r.startzeit,  # <--- stellt sicher, dass "Uhrzeit" existiert
                "Stock": seat.Stock
            })

    df = pd.DataFrame(data)

    # Sicherstellen, dass die Spalte "Uhrzeit" vorhanden ist:
    if "Uhrzeit" not in df.columns:
        raise ValueError("Spalte 'Uhrzeit' fehlt im DataFrame!")

    df = df.groupby(["Uhrzeit", "Stock"]).size().reset_index(name="Anzahl Reservationen")
    return df





