from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from config import Config

def get_db_connection():
    return sqlite3.connect(Config.DB_PATH)

def get_all_users():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, username FROM users")
        users = cursor.fetchall()
        return [{"id": user[0], "username": user[1]} for user in users], None
    except Exception as e:
        return None, f"Database error: {str(e)}"
    finally:
        conn.close()

def create_user(username, password, email=None):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
        if cursor.fetchone():
            return None, "Username already exists"
        
        password_hash = generate_password_hash(password)
        
        cursor.execute(
            "INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
            (username, password, email),
        )
        conn.commit()

        user_id = cursor.lastrowid
        return {"id": user_id, "username": username}, None
    except Exception as e:
        conn.rollback()
        return None, f"Database error: {str(e)}"
    finally:
        conn.close()

def verify_user(username, password):
    """Helper function to verify a user's password during login."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT user_id, username, password FROM users WHERE username = ?",
            (username,)
        )
        user = cursor.fetchone()
        if not user:
            return None, 'User not found'
        
        if check_password_hash(user[2], password):  # user[2] = password_hash
            return {'id': user[0], 'username': user[1]}, None
        else:
            return None, 'Incorrect password'
    except Exception as e:
        return None, f'Database error: {str(e)}'
    finally:
        conn.close()

def get_user_by_id_or_username(user_id=None, username=None):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        if user_id:
            cursor.execute(
                "SELECT user_id, username, password FROM users WHERE user_id = ?",
                (user_id,),
            )
        elif username:
            cursor.execute(
                "SELECT user_id, username, password FROM users WHERE username = ?",
                (username,),
            )
        else:
            return None, "User not found"

        user = cursor.fetchone()
        if user:
            return {"id": user[0], "username": user[1], "password_hash": user[2]}, None
        else:
            return None, "User not found"
    except Exception as e:
        return None, f"Database error: {str(e)}"
    finally:
        conn.close()

def delete_user(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
        if not cursor.fetchone():
            return None, "User not found"

        cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
        conn.commit()
        return {"message": f"User {user_id} deleted successfully"}, None
    except Exception as e:
        conn.rollback()
        return None, f"Database error: {str(e)}"
    finally:
        conn.close()

def update_user(user_id, new_data):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
        if not cursor.fetchone():
            return None, "User not found"

        if "username" in new_data:
            cursor.execute(
                "SELECT user_id FROM users WHERE username = ? AND user_id != ?",
                (new_data["username"], user_id),
            )
            if cursor.fetchone():
                return None, "Username already exists"
            cursor.execute(
                "UPDATE users SET username = ? WHERE user_id = ?",
                (new_data["username"], user_id),
            )

        if 'password' in new_data:
            password_hash = generate_password_hash(new_data['password'])
            cursor.execute(
                "UPDATE users SET password = ? WHERE user_id = ?",
                (password_hash, user_id)
            )

        conn.commit()
        return {"message": "User updated successfully"}, None
    except Exception as e:
        conn.rollback()
        return None, f"Database error: {str(e)}"
    finally:
        conn.close()

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


def add_user(username, password, email):
    if (any(user['username'] == username for user in get_users())):
        return 'Username already exists'
    else:
        """Lägg till användare i databasen."""
        conn = get_db_connection()
        user = conn.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", (username, generate_password_hash(password), email)).lastrowid
        conn.commit()
        conn.close()

        return user if user else None