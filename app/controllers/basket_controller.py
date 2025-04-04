import sqlite3

def get_db_connection2():
    """Connects to the SQLite database and returns the connection."""
    conn = sqlite3.connect('books_data.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_basket_items(user_id):
    """Fetches all basket items for a user and returns as a list of dictionaries."""
    conn = get_db_connection2()
    rows = conn.execute("""
        SELECT 
            u.username,
            b.book_id,
            b.book_title,
            b.book_price,
            ba.quantity,
            b.book_category
        FROM basket AS ba
        JOIN users AS u ON ba.user_id = u.user_id
        JOIN books AS b ON ba.book_id = b.book_id
        WHERE u.user_id = ?
        ORDER BY b.book_title;
    """, (user_id,)).fetchall()
    conn.close()
    return [dict(row) for row in rows]

def add_item_to_basket(user_id, book_id, quantity):
    """Adds an item to the basket."""
    conn = get_db_connection2()
    basket_id = conn.execute(
        "INSERT INTO basket (user_id, book_id, quantity) VALUES (?, ?, ?)",
        (user_id, book_id, quantity)
    ).lastrowid
    conn.commit()
    conn.close()
    return basket_id if basket_id else None

def remove_item_from_basket(user_id, book_id):
    """Removes an item from the basket using user_id and book_id."""
    conn = get_db_connection2()
    conn.execute(
        "DELETE FROM basket WHERE user_id = ? AND book_id = ?",
        (user_id, book_id)
    )
    conn.commit()
    conn.close()
    return True