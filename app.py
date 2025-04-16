import streamlit as st
from database import Seating, Reservation, get_session, reserve_time_slot, delete_reservation, update_reservation, count_weakly_reservations
import datetime
from data_visualization import create_reservation_dataframe
import plotly.express as px
from mailing import sende_bestaetigungsmail
from api_client import authenticate_user
st.set_page_config(layout="wide")
#Github Copilot für die Kommentierung des Codes.


# 🔐 Login-System
if "user_email" not in st.session_state:
    st.title("🔐 Login zur Sitzplatzreservierung")

    email = st.text_input("📧 E-Mail")
    password = st.text_input("🔑 Passwort", type="password")

    if st.button("Login"):
        if authenticate_user(email, password):
            st.session_state["user_email"] = email
            st.success("✅ Login erfolgreich!")
            st.rerun()
        else:
            st.error("❌ E-Mail oder Passwort ist falsch.")
    st.stop()

if "user_email" not in st.session_state:
    st.stop()

st.title("📚 Sitzplatz-Reservierung – HSG Bibliothek")

session = get_session()
seats = session.query(Seating).all()

#Filterung der Sitzplätze nach Stock
alle_stocks = sorted(list(set([s.Stock for s in seats])))
ausgewaehlter_stock = st.selectbox("📍 Stock auswählen", ["Alle"] + alle_stocks)

if ausgewaehlter_stock != "Alle":
    seats = [s for s in seats if s.Stock == ausgewaehlter_stock]

# Adminmodus
st.sidebar.title("🔐 Adminbereich")
is_admin = st.sidebar.checkbox("Adminmodus aktivieren")

# Bestehende Reservierungen anzeigen
reservierungen = session.query(Reservation).all()

st.subheader("📅 Aktuelle Zeitreservierungen")
for r in reservierungen:
    st.write(f"🪑 Platz {r.sitznummer} | 📅 {r.datum} | ⏰ {r.startzeit} – {r.endzeit}")

    if is_admin: #Kommentar hinzufügen
        col1, col2 = st.columns(2)
        with col1:
            if st.button(f"❌ Löschen", key=f"del_{r.id}"):
                delete_reservation(r.id)
                st.rerun()
        with col2:
            neue_startzeit = st.time_input(f"Neue Startzeit (ID {r.id})",
                                           value=datetime.datetime.strptime(r.startzeit, "%H:%M").time(),
                                           key=f"new_start_{r.id}")
            neue_endzeit = st.time_input(f"Neue Endzeit (ID {r.id})",
                                         value=datetime.datetime.strptime(r.endzeit, "%H:%M").time(),
                                         key=f"new_end_{r.id}")
            neues_datum = st.date_input(f"Neues Datum (ID {r.id})", value=r.datum, key=f"new_date_{r.id}")
            if st.button(f"🔄 Aktualisieren", key=f"update_{r.id}"):
                update_reservation(r.id, neues_datum, neue_startzeit.strftime("%H:%M"), neue_endzeit.strftime("%H:%M"))
                st.rerun()

st.markdown("---")

# Sitzplätze mit Zeitfenster-Reservierung anzeigen
st.subheader("🪑 Neue Zeitfenster-Reservierung")
ausgewähltes_datum = st.date_input("📅 Datum", datetime.date.today())
ausgewählte_zeit = st.time_input("⏰ Uhrzeit", datetime.datetime.now().time())

for index, platz in enumerate(seats):
    col1, col2 = st.columns([3, 2])

    with col1:
        # Startzeit = ausgewählte Zeit, Endzeit = 2 Stunden später
        vorgeschlagene_startzeit = ausgewählte_zeit
        vorgeschlagene_endzeit = (
                    datetime.datetime.combine(datetime.date.today(), ausgewählte_zeit) + datetime.timedelta(
                hours=2)).time()

        start = st.time_input(f"Startzeit für Platz {platz.Platznummer}", vorgeschlagene_startzeit,
                              key=f"start_{platz.Platznummer}")
        end = st.time_input(f"Endzeit für Platz {platz.Platznummer}", vorgeschlagene_endzeit,
                            key=f"end_{platz.Platznummer}")

        belegt = any(
            r.sitznummer == platz.Platznummer and
            r.datum == ausgewähltes_datum and
            (
                datetime.datetime.strptime(r.startzeit, "%H:%M").time() < end and
                datetime.datetime.strptime(r.endzeit, "%H:%M").time() > start
            )
            for r in reservierungen
        )

        farbe = "🔴 Belegt" if belegt else "🟢 Frei"
        st.markdown(f"**Platz {platz.Platznummer} | Stock: {platz.Stock} → {farbe}**")

    with col2:
        if st.button("Reservieren", key=f"timebtn_{platz.Platznummer}_{index}"):
            start_str = start.strftime("%H:%M")
            end_str = end.strftime("%H:%M")
            anzahl_reservierungen = count_weakly_reservations(session, st.session_state["user_email"], ausgewähltes_datum)
            if anzahl_reservierungen >= 2:
                st.warning("Du hast bereits 2 Reservierungen in dieser Woche vorgenommen.")
                continue #Überspringt diese Reservierung
            success = reserve_time_slot(platz.Platznummer, start_str, end_str, ausgewähltes_datum, st.session_state["user_email"])
            if success:
                st.success(f"✅ Reservierung erfolgreich: {start_str} – {end_str} am {ausgewähltes_datum}")
                st.rerun()
                sende_bestaetigungsmail(
                    empfaenger_email=st.session_state["user_email"],
                    platznummer=platz.Platznummer,
                    datum=ausgewähltes_datum,
                    startzeit=start_str,
                    endzeit=end_str
                )
                st.info("📧 Bestätigung wurde per Mail gesendet.")
                st.rerun()
            else:
                st.error("⚠️ Zeitraum bereits reserviert!")



# Visualisierung der Auslastung
st.subheader("📊 Auslastung der Bibliothek")
df = create_reservation_dataframe()
fig = px.bar(df, x="Uhrzeit", y="Anzahl Reservationen", color="Stock", barmode="group")
st.plotly_chart(fig, use_container_width=True)





























