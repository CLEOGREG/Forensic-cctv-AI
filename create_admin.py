import sqlite3
from werkzeug.security import generate_password_hash

DATABASE = "database/forensiciq.db"

username = "admin"
password = "admin123"
role = "admin"

# Use PBKDF2-SHA256 for compatibility with Python 3.9
password_hash = generate_password_hash(
    password,
    method="pbkdf2:sha256"
)

connection = sqlite3.connect(DATABASE)

cursor = connection.cursor()

# Avoid crashing with "UNIQUE constraint failed" if this is run twice
existing = cursor.execute(
    "SELECT id FROM users WHERE username = ?",
    (username,)
).fetchone()

if existing:
    print(f"User '{username}' already exists. No changes made.")
else:
    cursor.execute("""
        INSERT INTO users (
            username,
            password_hash,
            role
        )
        VALUES (?, ?, ?)
    """, (
        username,
        password_hash,
        role
    ))

    connection.commit()

    print("================================")
    print("ADMIN ACCOUNT CREATED")
    print("================================")
    print("Username:", username)
    print("Password:", password)
    print("Role:", role)
    print("================================")

connection.close()