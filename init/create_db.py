import sqlite3
import os
import sys

# Add the parent directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import Config

#print("Absolute DB path:", os.path.abspath(Config.DB_PATH))

class Database:

    # SQLite database, skapa tabell books
    def create_table_books(self):
        conn = sqlite3.connect(Config.DB_PATH)        
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                book_id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_title TEXT,
                book_price TEXT,
                book_rating TEXT,
                book_availability TEXT,
                book_image_url TEXT,
                book_category TEXT
            )
        """)
        conn.commit()
        return conn
    
    # SQLite database, skapa tabell users
    def create_table_users(self):
        conn = sqlite3.connect(Config.DB_PATH)        
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT,
                email TEXT
            )
        """)
        conn.commit()
        return conn

    # SQLite database, skapa kopplingstabell basket
    def create_table_basket(self):
        conn = sqlite3.connect(Config.DB_PATH)        
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS basket (
                basket_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                book_id INTEGER NOT NULL,
                quantity INTEGER DEFAULT 1,
                added_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id),
                FOREIGN KEY (book_id) REFERENCES books(book_id)
            )
        """)
        conn.commit()
        return conn
    
    # SQLite database, skapa kopplingstabell favorites
    def create_table_favorites(self):
        conn = sqlite3.connect(Config.DB_PATH)        
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS favorites (
                favorite_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                book_id INTEGER NOT NULL,
                added_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id),
                FOREIGN KEY (book_id) REFERENCES books(book_id)
            )
        """)
        conn.commit()
        return conn

    # SQLite database, ta bort tabell
    def delete_table(self):
        conn = sqlite3.connect(Config.DB_PATH)        
        cursor = conn.cursor()
        cursor.execute("DROP TABLE users;")
        conn.commit()
        return conn
    
db=Database()
# db.create_table_books()
# db.create_table_users()
# db.create_table_basket()
db.create_table_favorites()
# db.delete_table()