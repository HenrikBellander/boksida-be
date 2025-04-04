import sqlite3
from flask import Blueprint, request, jsonify
from config import Config   

def get_db_connection():
    return sqlite3.connect(Config.DB_PATH)
favorites_bp = Blueprint('favorites', __name__)

@favorites_bp.route('/api/favorites', methods=['POST'])
def add_favorite():
    user_id = request.json.get('user_id')
    book_id = request.json.get('book_id')

    if not user_id:
        return jsonify({"error": "user_id is required"}), 400
    if not book_id:
        return jsonify({"error": "book_id is required"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT OR REPLACE INTO favorites (user_id, book_id) VALUES (?, ?)",
            (user_id, book_id)
        )
        conn.commit()
        conn.close()
        return jsonify({"message": "Book added to favorites"}), 201

    except sqlite3.IntegrityError as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500


@favorites_bp.route('/api/favorites', methods=['DELETE'])
def remove_favorite():
    user_id = request.json.get('user_id')
    book_id = request.json.get('book_id')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM favorites WHERE user_id = ? AND book_id = ?",
        (user_id, book_id)
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Book removed from favorites"}), 200

@favorites_bp.route('/api/favorites/<int:user_id>', methods=['GET'])
def get_favorites(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT book_id FROM favorites WHERE user_id = ?", (user_id,))
    favorite_books = cursor.fetchall()

    if not favorite_books:
        conn.close()
        return jsonify({"message": "No favorites found"}), 404

    book_ids = [fav[0] for fav in favorite_books]

    placeholders = ','.join('?' * len(book_ids))
    cursor.execute(f"SELECT book_title, book_image_url FROM books WHERE book_id IN ({placeholders})", book_ids)
    
    books = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    
    conn.close()

    books_list = [dict(zip(columns, book)) for book in books]

    return jsonify(books_list)






