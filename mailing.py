import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
# -*- coding: utf-8 -*-

def sende_bestaetigungsmail(empfaenger_email, platznummer, datum, startzeit, endzeit):
    absender_email = "Deine E-Mail für die Bestätigungsmail"
    app_passwort = "DEIN_APP_PASSWORT"

    nachricht = MIMEMultipart("alternative")
    nachricht["Subject"] = "📚 Deine Sitzplatz-Reservierung – HSG Bibliothek"
    nachricht["From"] = absender_email
    nachricht["To"] = empfaenger_email

    text = f"""
    Hallo!

    Deine Reservierung wurde erfolgreich gebucht:

    🪑 Platz: {platznummer}
    📅 Datum: {datum}
    ⏰ Zeit: {startzeit} – {endzeit}

    Viel Erfolg beim Lernen!
    """
    nachricht.attach(MIMEText(text, "plain"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(str(absender_email), str(app_passwort))
        server.sendmail(absender_email, empfaenger_email, nachricht.as_string()
        )

