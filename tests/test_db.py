import pytest
import sqlite3
from app.controllers.book_controller import get_categories, get_books_by_category

@pytest.fixture(scope='module')
def test_db():
    conn = sqlite3.connect(':memory:')
    conn.row_factory = sqlite3.Row
    
    conn.execute('''
    CREATE TABLE books (
        book_id INTEGER PRIMARY KEY,
        book_title TEXT,
        book_availability TEXT,
        book_image_url TEXT,
        book_description TEXT,
        book_price REAL,
        book_rating INTEGER,
        book_category TEXT
    )''')
    
    conn.execute('''
    INSERT INTO books VALUES
        (1, "It's Only the Himalayas", "In stock", "url1.jpg", 
         "En reseskildring", 199.99, 4, "Travel"),
        (2, "Most Wanted", "Out of stock", "url2.jpg",
         "En thriller", 249.99, 5, "Fiction"),
        (3, "Philosophy 101", "In stock", "url3.jpg",
         "Filosofi introduktion", 159.99, 3, "Philosophy")
    ''')
    conn.commit()
    yield conn
    conn.close()

def test_get_categories():
    """Testar att kategori-funktionen returnerar rätt typ"""
    result = get_categories()
    assert isinstance(result, list), "Should return a list of categories"
    assert all(
        isinstance(item, dict) and "book_category" in item 
        for item in result
    ), "Each item should be a dict with 'book_category' key"
    
    categories = [item["book_category"] for item in result]
    assert "Travel" in categories
    assert "Fiction" in categories

def test_get_books_by_category():
    """Testar boklistning per kategori"""
    books = get_books_by_category("Fiction")
    assert isinstance(books, list)
    if len(books) > 0:
        assert books[0]["book_category"] == "Fiction"