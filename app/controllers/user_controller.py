import sqlite3
from werkzeug.security import generate_password_hash

def get_db_connection():
    """Ansluter till SQLite-databasen och returnerar anslutningen."""
    conn = sqlite3.connect('books_data.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_users():
    """Hämtar alla användare från databasen och returnerar som JSON."""
    conn = get_db_connection()
    users = conn.execute('SELECT user_id, username FROM users').fetchall()
    conn.close()
    
    return [dict(row) for row in users]

def get_single_user(user_id):
    """Hämtar en användare baserat på dess ID."""
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchone()
    conn.close()

    return dict(user) if user else None

def delete_user(user_id):
    """Ta bort användare med hjälp av ID."""
    conn = get_db_connection()
    user = conn.execute("DELETE FROM users WHERE user_id = ?", (user_id,)).fetchone()
    conn.commit()
    conn.close()

    return dict(user) if user else None

def add_user(username, password, email):
    print(username)
    """Lägg till användare i databasen."""
    conn = get_db_connection()
    user = conn.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", (username, generate_password_hash(password), email)).lastrowid
    conn.commit()
    conn.close()

    return user if user else None

def update_user(user_id, username, password, email):
    """Uppdatera användare med hjälp av ID."""
    conn = get_db_connection()
    user = conn.execute("UPDATE users SET username = ?, password = ?, email = ? WHERE user_id = ?", (username, generate_password_hash(password), email, user_id,)).fetchone()
    conn.commit()
    conn.close()

    return dict(user) if user else None