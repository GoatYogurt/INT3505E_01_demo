from flask import Blueprint, jsonify, request
from app.models import Book
from app.utils.jwt_utils import token_required, requires_role
from app.data.sample_data import books

books_bp = Blueprint('books', __name__)

# --- Reusable Schema Snippets ---
# (You can't do this in YAML, but I'm showing it here for clarity.
# I've pasted the full schema into the docstrings below.)
#
# Book Schema Properties:
#   id: { type: integer, example: 1 }
#   title: { type: string, example: "The Great Gatsby" }
#   author: { type: string, example: "F. Scott Fitzgerald" }
#   year: { type: integer, example: 1925 }
#   publisher: { type: string, example: "Scribner" }
#   genre: { type: string, example: "Fiction" }
#   isbn: { type: string, example: "978-0743273565" }
#   available: { type: boolean, example: true }
#
# Error Schema:
#   type: object
#   properties:
#     error: { type: string }
#
# ---------------------------------


@books_bp.route('/', methods=['GET'])
def get_books():
    """
    Get a list of all books
    Returns a complete list of all books in the library.
    ---
    tags:
      - Books
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
    return jsonify([book.to_dict() for book in books])


@books_bp.route('/<int:id>', methods=['GET'])
def get_book(id):
    """
    Get a single book by ID
    Returns details for a specific book.
    ---
    tags:
      - Books
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
    book = next((b for b in books if b.id == id), None)
    if book:
        return jsonify(book.to_dict())
    return jsonify({"error": "Book not found"}), 404


@books_bp.route('/', methods=['POST'])
@token_required
@requires_role('admin')
def add_book():
    """
    Add a new book (Admin only)
    Creates a new book and adds it to the library. Requires admin privileges.
    ---
    tags:
      - Books
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
    """
    Borrow an available book
    Marks a book as 'unavailable' (borrowed). Requires 'user' or 'admin' role.
    ---
    tags:
      - Books
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
    """
    Return a borrowed book
    Marks a book as 'available' (returned). Requires 'user' or 'admin' role.
    ---
    tags:
      - Books
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
    book = next((b for b in books if b.id == id), None)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    if book.available:
        return jsonify({"error": "Book is not borrowed"}), 400
    book.available = True
    return jsonify({"message": f"Returned '{book.title}'", "book": book.to_dict()})