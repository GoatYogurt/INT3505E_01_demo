# app/routes/books.py
from flask import Blueprint, jsonify, request
from app.utils.jwt_utils import token_required
from app.data.sample_books import books

books_bp = Blueprint('books', __name__)

@books_bp.route('/', methods=['GET'])
def get_books():
    return jsonify(books)

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