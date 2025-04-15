import sqlite3
import bcrypt

import sqlite3
import bcrypt

def authenticate_user(email, password):
    try:
        conn = sqlite3.connect("database_HSG.db")
        cursor = conn.cursor()

        cursor.execute("SELECT password_hash FROM users WHERE email = ?", (email,))
        result = cursor.fetchone()

        if result:
            stored_hash = result[0]
            print("💾 Hash aus DB:", stored_hash)
            print("🔑 Eingegebenes Passwort:", password)

            if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
                print("✅ Passwort korrekt")
                return True
            else:
                print("❌ Passwort falsch")
        else:
            print("⚠️ Benutzer nicht gefunden")

        return False

    except Exception as e:
        print("Fehler bei der Authentifizierung:", e)
        return False

    finally:
        if 'conn' in locals():
            conn.close()






