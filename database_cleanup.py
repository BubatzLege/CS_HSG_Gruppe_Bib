import sqlite3

conn = sqlite3.connect("database_HSG.db")
cursor = conn.cursor()

cursor.execute("SELECT id, email FROM users")
rows = cursor.fetchall()

for user_id, email in rows:
    cleaned_email = email.strip()
    if email != cleaned_email:
        cursor.execute("UPDATE users SET email = ? WHERE id = ?", (cleaned_email, user_id))

conn.commit()
conn.close()
print("✅ Alle E-Mail-Adressen bereinigt!")
