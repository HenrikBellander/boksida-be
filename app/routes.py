from flask import Blueprint, jsonify, request
from .controllers.book_controller import get_categories, get_books_by_category, search_books, get_book_detail

books = Blueprint('books', __name__, url_prefix='/api')

@books.route('/', methods=['GET'])
def get_categories_route():
    """Hämtar alla bokkategorier från databasen och returnerar som JSON."""
    categories = get_categories()
    return jsonify(categories)

@books.route('/category/<category>', methods=['GET'])
def show_books_by_category_route(category):
    """Visar böcker från en specifik kategori."""
    books = get_books_by_category(category)
    return jsonify(books)

@books.route('/search', methods=['GET'])
def search_route():
    """Söker böcker baserat på användarens sökfråga."""
    query = request.args.get('q', '')
    books = search_books(query)
    return jsonify(books)

@books.route('/book/<int:book_id>', methods=['GET'])
def book_detail_route(book_id):
    """Visar detaljer om en bok baserat på dess ID."""
    book = get_book_detail(book_id)
    if book is None:
        return jsonify({"error": "Boken hittades inte"}), 404
    return jsonify(book)






