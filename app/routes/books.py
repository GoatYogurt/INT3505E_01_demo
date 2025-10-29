# app/routes/books.py
from flask import Blueprint, jsonify, request
from app.utils.jwt_utils import token_required
from app.data.sample_data import books

books_bp = Blueprint('books', __name__)


@books_bp.route('/', methods=['GET'])
def get_books():
    return jsonify(books)


@books_bp.route('/<int:id>', methods=['GET'])
def get_book(id):
    book = next((b for b in books if b["id"] == id), None)
    if book:
        return jsonify(book)
    return jsonify({"error": "Book not found"}), 404


@books_bp.route('/', methods=['POST'])
@token_required
def add_book(current_user):
    data = request.get_json()
    new_book = {
        "id": len(books) + 1,
        "title": data.get("title"),
        "author": data.get("author"),
        "year": data.get("year"),
        "publisher": data.get("publisher"),
        "genre": data.get("genre"),
        "isbn": data.get("isbn"),
        "available": True
    }
    books.append(new_book)
    return jsonify(new_book), 201


@books_bp.route('/<int:id>/borrow', methods=['POST'])
@token_required
def borrow_book(current_user, id):
    book = next((b for b in books if b["id"] == id), None)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    if not book["available"]:
        return jsonify({"error": "Book is already borrowed"}), 400
    book["available"] = False
    return jsonify({"message": f"{current_user} borrowed '{book['title']}'", "book": book})

@books_bp.route('/<int:id>/return', methods=['POST'])
@token_required
def return_book(current_user, id):
    book = next((b for b in books if b["id"] == id), None)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    if book["available"]:
        return jsonify({"error": "Book is not borrowed"}), 400
    book["available"] = True
    return jsonify({"message": f"{current_user} returned '{book['title']}'", "book": book})