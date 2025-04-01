import sqlite3

def get_db_connection2():
    """Ansluter till SQLite-databasen och returnerar anslutningen."""
    conn = sqlite3.connect('books_data.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_basket_items(user_id):
    """Hämtar allt i varukorgen från databasen och returnerar som JSON."""
    conn = get_db_connection2()
    basket = conn.execute("""
        SELECT 
            u.user_id,
            u.username,
            b.book_title AS book_title,
            ba.quantity,
            b.book_price
        FROM basket AS ba
        JOIN users AS u ON ba.user_id = u.user_id
        JOIN books AS b ON ba.book_id = b.book_id
        WHERE u.user_id = ?
        ORDER BY u.username, b.book_title;
        """, (user_id,)).fetchone()
    conn.close()
    
    return [dict(row) for row in basket]

def add_item_to_basket(user_id, book_id, quantity):
    """Adds an item to the basket."""
    conn = get_db_connection2()
    basket = conn.execute("INSERT INTO basket (user_id, book_id, quantity) VALUES (?, ?, ?)", (user_id, book_id, quantity)).lastrowid
    conn.commit()
    conn.close()
    
    return basket if basket else None

def remove_item_from_basket(basket_id):
    """Removes an item from the basket."""
    conn = get_db_connection2()
    basket = conn.execute("DELETE FROM basket WHERE basket_id = ?", (basket_id,)).fetchone()
    conn.commit()
    conn.close()

    return dict(basket) if basket else None