import sqlite3
import bcrypt

conn = sqlite3.connect("/database_HSG.db")

cursor = conn.cursor()

cursor.execute("SELECT id, password_hash FROM users")
users = cursor.fetchall()

for user_id, plain_password in users:
    # Nur Klartext-Passwörter updaten (nicht doppelt hashen)
    if not plain_password.startswith("$2b$"):
        hashed = bcrypt.hashpw(plain_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        cursor.execute("UPDATE users SET password_hash = ? WHERE id = ?", (hashed, user_id))

conn.commit()
conn.close()
print("✅ Alle Klartext-Passwörter wurden sicher gehashed.")
