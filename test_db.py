from database import get_session, Seating

session = get_session()
results = session.query(Seating).all()

for row in results:
    print(row.Platznummer, row.Zustand, row.Stock)
