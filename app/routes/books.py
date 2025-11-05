# app/routes/books.py
from flask import Blueprint, jsonify, request
from app.models import Book
from app.utils.jwt_utils import token_required, requires_role
from app.data.sample_data import books

books_bp = Blueprint('books', __name__)


@books_bp.route('/', methods=['GET'])
def get_books():
    return jsonify([book.to_dict() for book in books])


@books_bp.route('/<int:id>', methods=['GET'])
def get_book(id):
    book = next((b for b in books if b.id == id), None)
    if book:
        return jsonify(book.to_dict())
    return jsonify({"error": "Book not found"}), 404


@books_bp.route('/', methods=['POST'])
@token_required
@requires_role('admin')
def add_book():
    data = request.get_json()
    new_book = Book(
        id=len(books) + 1,
        title=data.get("title"),
        author=data.get("author"),
        year=data.get("year"),
        publisher=data.get("publisher"),
        genre=data.get("genre"),
        isbn=data.get("isbn"),
        available=True
    )
    books.append(new_book)
    return jsonify(new_book.to_dict()), 201


@books_bp.route('/<int:id>/borrow', methods=['POST'])
@token_required
@requires_role('user', 'admin')
def borrow_book(id):
    book = next((b for b in books if b.id == id), None)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    if not book.available:
        return jsonify({"error": "Book is already borrowed"}), 400
    book.available = False
    return jsonify({"message": f"Borrowed '{book.title}'", "book": book.to_dict()})


@books_bp.route('/<int:id>/return', methods=['POST'])
@token_required
@requires_role('user', 'admin')
def return_book(id):
    book = next((b for b in books if b.id == id), None)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    if book.available:
        return jsonify({"error": "Book is not borrowed"}), 400
    book.available = True
    return jsonify({"message": f"Returned '{book.title}'", "book": book.to_dict()})