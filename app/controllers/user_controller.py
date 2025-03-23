import sqlite3

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
