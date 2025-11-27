from flask import Blueprint, jsonify, request
from app.models import Book
from app.utils.jwt_utils import token_required, requires_role
from app.data.sample_data import books
from pymongo import MongoClient
from bson import ObjectId

books_v2 = Blueprint('books_v2', __name__, url_prefix='/v2/books')
client = MongoClient('mongodb://localhost:27017/')
db = client['library_db']
books_collection = db['books']

def serialize_book(book):
    """Convert MongoDB book document to JSON serializable dict"""
    return {
        "id": str(book["_id"]),
        "title": book.get("title"),
        "author": book.get("author"),
        "year": book.get("year"),
        "publisher": book.get("publisher"),
        "genre": book.get("genre"),
        "isbn": book.get("isbn"),
        "available": book.get("available", True)
    }

@books_v2.route('/', methods=['GET'])
def get_books():
    """
    Get a list of all books
    Returns a complete list of all books in the library.
    ---
    tags:
      - Books_v2
    produces:
      - application/json
    responses:
      200:
        description: A list of books.
        schema:
          type: array
          items:
            type: object
            properties:
              id: { type: integer, example: 1 }
              title: { type: string, example: "The Great Gatsby" }
              author: { type: string, example: "F. Scott Fitzgerald" }
              year: { type: integer, example: 1925 }
              publisher: { type: string, example: "Scribner" }
              genre: { type: string, example: "Fiction" }
              isbn: { type: string, example: "978-0743273565" }
              available: { type: boolean, example: true }
    """
    books = list(books_collection.find())
    return jsonify([serialize_book(b) for b in books])


@books_v2.route('/<string:id>', methods=['GET'])
def get_book(id):
    """
    Get a single book by ID
    Returns details for a specific book.
    ---
    tags:
      - Books_v2
    produces:
      - application/json
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: The ID of the book to retrieve.
    responses:
      200:
        description: The requested book.
        schema:
          type: object
          properties:
            id: { type: integer, example: 1 }
            title: { type: string, example: "The Great Gatsby" }
            author: { type: string, example: "F. Scott Fitzgerald" }
            year: { type: integer, example: 1925 }
            publisher: { type: string, example: "Scribner" }
            genre: { type: string, example: "Fiction" }
            isbn: { type: string, example: "978-0743273565" }
            available: { type: boolean, example: true }
      404:
        description: Book not found.
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Book not found"
    """
    try:
        book = books_collection.find_one({"_id": ObjectId(id)})
    except:
        return jsonify({"error": "Invalid book ID"}), 400

    if not book:
        return jsonify({"error": "Book not found"}), 404

    return jsonify(serialize_book(book))


@books_v2.route('/', methods=['POST'])
@token_required
@requires_role('admin')
def add_book():
    """
    Add a new book (Admin only)
    Creates a new book and adds it to the library. Requires admin privileges.
    ---
    tags:
      - Books_v2
    consumes:
      - application/json
    produces:
      - application/json
    securityDefinitions:
      ApiKeyAuth:
        type: apiKey
        in: header
        name: Authorization
        description: "JWT Token, typically 'Bearer &lt;token&gt;'. The @token_required decorator handles parsing."
    security:
      - ApiKeyAuth: []
    parameters:
      - in: body
        name: body
        required: true
        description: The book to create.
        schema:
          type: object
          required:
            - title
            - author
          properties:
            title: { type: string, example: "1984" }
            author: { type: string, example: "George Orwell" }
            year: { type: integer, example: 1949 }
            publisher: { type: string, example: "Secker & Warburg" }
            genre: { type: string, example: "Dystopian" }
            isbn: { type: string, example: "978-0451524935" }
    responses:
      201:
        description: Book created successfully.
        schema:
          type: object
          properties:
            id: { type: integer, example: 1 }
            title: { type: string, example: "1984" }
            author: { type: string, example: "George Orwell" }
            year: { type: integer, example: 1949 }
            publisher: { type: string, example: "Secker & Warburg" }
            genre: { type: string, example: "Dystopian" }
            isbn: { type: string, example: "978-0451524935" }
            available: { type: boolean, example: true }
      401:
        description: Unauthorized (Token is missing or invalid)
      403:
        description: Forbidden (User is not an admin)
    """
    data = request.get_json()

    new_book = {
        "title": data.get("title"),
        "author": data.get("author"),
        "year": data.get("year"),
        "publisher": data.get("publisher"),
        "genre": data.get("genre"),
        "isbn": data.get("isbn"),
        "available": True
    }

    result = books_collection.insert_one(new_book)
    new_book["_id"] = result.inserted_id

    return jsonify(serialize_book(new_book)), 201


@books_v2.route('/<string:id>', methods=['PUT'])
@token_required
@requires_role('admin')
def update_book(id):
    """
    Update an existing book (Admin only)
    Updates details of an existing book. Requires admin privileges.
    ---
    tags:
      - Books_v2
    consumes:
      - application/json
    produces:
      - application/json
    security:
      - ApiKeyAuth: []
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: The ID of the book to update.
      - in: body
        name: body
        required: true
        description: The updated book details.
        schema:
          type: object
          properties:
            title: { type: string, example: "1984" }
            author: { type: string, example: "George Orwell" }
            year: { type: integer, example: 1949 }
            publisher: { type: string, example: "Secker & Warburg" }
            genre: { type: string, example: "Dystopian" }
            isbn: { type: string, example: "978-0451524935" }
    responses:
      200:
        description: Book updated successfully.
        schema:
          type: object
          properties:
            id: { type: integer, example: 1 }
            title: { type: string, example: "1984" }
            author: { type: string, example: "George Orwell" }
            year: { type: integer, example: 1949 }
            publisher: { type: string, example: "Secker & Warburg" }
            genre: { type: string, example: "Dystopian" }
            isbn: { type: string, example: "978-0451524935" }
            available: { type: boolean, example: true }
      404:
        description: Book not found.
        schema:
          type: object
          properties:
            error: { type: string, example: "Book not found" }
      401:
        description: Unauthorized (Token is missing or invalid)
      403:
        description: Forbidden (User is not an admin)
    """
    data = request.get_json()
    try:
        book = books_collection.find_one({"_id": ObjectId(id)})
    except:
        return jsonify({"error": "Invalid book ID"}), 400

    if not book:
        return jsonify({"error": "Book not found"}), 404

    updated_fields = {k: v for k, v in data.items() if v is not None}
    books_collection.update_one({"_id": ObjectId(id)}, {"$set": updated_fields})

    book.update(updated_fields)
    return jsonify(serialize_book(book))

@books_v2.route('/<string:id>', methods=['DELETE'])
@token_required
@requires_role('admin')
def delete_book(id):
    """
    Delete a book (Admin only)
    Deletes a book from the library. Requires admin privileges.
    ---
    tags:
      - Books_v2
    produces:
      - application/json
    security:
      - ApiKeyAuth: []
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: The ID of the book to delete.
    responses:
      200:
        description: Book deleted successfully.
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Book deleted successfully"
      404:
        description: Book not found.
        schema:
          type: object
          properties:
            error: { type: string, example: "Book not found" }
      401:
        description: Unauthorized (Token is missing or invalid)
      403:
        description: Forbidden (User is not an admin)
    """
    try:
        book = books_collection.find_one({"_id": ObjectId(id)})
    except:
        return jsonify({"error": "Invalid book ID"}), 400

    if not book:
        return jsonify({"error": "Book not found"}), 404

    books_collection.delete_one({"_id": ObjectId(id)})
    return jsonify({"message": "Book deleted successfully"})


@books_v2.route('/<string:id>/borrow', methods=['POST'])
@token_required
@requires_role('user', 'admin')
def borrow_book(id):
    """
    Borrow an available book
    Marks a book as 'unavailable' (borrowed). Requires 'user' or 'admin' role.
    ---
    tags:
      - Books_v2
    produces:
      - application/json
    security:
      - ApiKeyAuth: []
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: The ID of the book to borrow.
    responses:
      200:
        description: Book borrowed successfully.
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Borrowed '1984'"
            book:
              type: object
              properties:
                id: { type: integer, example: 1 }
                title: { type: string, example: "1984" }
                author: { type: string, example: "George Orwell" }
                year: { type: integer, example: 1949 }
                publisher: { type: string, example: "Secker & Warburg" }
                genre: { type: string, example: "Dystopian" }
                isbn: { type: string, example: "978-0451524935" }
                available: { type: boolean, example: false }
      400:
        description: Book is already borrowed.
        schema:
          type: object
          properties:
            error: { type: string, example: "Book is already borrowed" }
      404:
        description: Book not found.
        schema:
          type: object
          properties:
            error: { type: string, example: "Book not found" }
      401:
        description: Unauthorized (Token is missing or invalid)
      403:
        description: Forbidden (User role is incorrect)
    """
    try:
        book = books_collection.find_one({"_id": ObjectId(id)})
    except:
        return jsonify({"error": "Invalid book ID"}), 400

    if not book:
        return jsonify({"error": "Book not found"}), 404

    if not book.get("available", True):
        return jsonify({"error": "Book is already borrowed"}), 400

    books_collection.update_one({"_id": ObjectId(id)}, {"$set": {"available": False}})
    book["available"] = False

    return jsonify({"message": f"Borrowed '{book['title']}'", "book": serialize_book(book)})


@books_v2.route('/<string:id>/return', methods=['POST'])
@token_required
@requires_role('user', 'admin')
def return_book(id):
    """
    Return a borrowed book
    Marks a book as 'available' (returned). Requires 'user' or 'admin' role.
    ---
    tags:
      - Books_v2
    produces:
      - application/json
    security:
      - ApiKeyAuth: []
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: The ID of the book to return.
    responses:
      200:
        description: Book returned successfully.
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Returned '1984'"
            book:
              type: object
              properties:
                id: { type: integer, example: 1 }
                title: { type: string, example: "1984" }
                author: { type: string, example: "George Orwell" }
                year: { type: integer, example: 1949 }
                publisher: { type: string, example: "Secker & Warburg" }
                genre: { type: string, example:Z "Dystopian" }
                isbn: { type: string, example: "978-0451524935" }
                available: { type: boolean, example: true }
      400:
        description: Book is not borrowed.
        schema:
          type: object
          properties:
            error: { type: string, example: "Book is not borrowed" }
      404:
        description: Book not found.
        schema:
          type: object
          properties:
            error: { type: string, example: "Book not found" }
      401:
        description: Unauthorized (Token is missing or invalid)
      403:
        description: Forbidden (User role is incorrect)
    """
    try:
        book = books_collection.find_one({"_id": ObjectId(id)})
    except:
        return jsonify({"error": "Invalid book ID"}), 400

    if not book:
        return jsonify({"error": "Book not found"}), 404

    if book.get("available", True):
        return jsonify({"error": "Book is not borrowed"}), 400

    books_collection.update_one({"_id": ObjectId(id)}, {"$set": {"available": True}})
    book["available"] = True

    return jsonify({"message": f"Returned '{book['title']}'", "book": serialize_book(book)})