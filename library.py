from flask import Flask, request, jsonify

app = Flask(__name__)

users = {
    "alice": "1234",
    "bob": "4321"
}


def authenticate(token):
    return token if token in users else None


# get all books
@app.route("/books", methods=["GET"])
def get_books():
    return jsonify(books), 200


# get one book by id
@app.route("/books/<int:id>", methods=["GET"])
def get_book(id):
    book = next((b for b in books if b["id"] == id), None)
    if book:
        return jsonify(book), 200
    return jsonify({"error": "Book not found"}), 404


# add a new book
@app.route("/books", methods=["POST"])
def add_book():
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


# update a book
@app.route("/books/<int:id>", methods=["PUT"])
def update_book(id):
    book = next((b for b in books if b["id"] == id), None)
    if not book:
        return jsonify({"error": "Book not found"}), 404

    data = request.get_json()
    for key in ["title", "author", "year", "publisher", "genre", "isbn", "available"]:
        if key in data:
            book[key] = data[key]

    return jsonify(book)


# delete a book
@app.route("/books/<int:id>", methods=["DELETE"])
def delete_book(id):
    global books
    books = [b for b in books if b["id"] != id]
    return jsonify({"message": "Book deleted successfully"})


# Borrow a book
@app.route("/books/<int:id>/borrow", methods=["POST"])
def borrow_book(id):
    token = request.headers.get('Authorization')
    user = authenticate(token)
    if not user:
        return jsonify({"error": "Invalid or missing token"}), 401

    book = next((b for b in books if b["id"] == id), None)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    if not book["available"]:
        return jsonify({"error": "Book is already borrowed"}), 400

    book["available"] = False
    return jsonify({"message": f"{user} borrowed '{book['title']}'", "book": book})


# Return a book
@app.route("/books/<int:id>/return", methods=["POST"])
def return_book(id):
    token = request.headers.get('Authorization')
    user = authenticate(token)
    if not user:
        return jsonify({"error": "Invalid or missing token"}), 401
    
    book = next((b for b in books if b["id"] == id), None)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    if book["available"]:
        return jsonify({"error": "Book was not borrowed"}), 400

    book["available"] = True
    return jsonify({"message": f"{user} returned '{book['title']}'", "book": book})


if __name__ == "__main__":
    app.run(debug=True)
