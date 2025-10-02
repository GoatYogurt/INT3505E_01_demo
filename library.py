from flask import Flask, request, jsonify

app = Flask(__name__)

books = [
    {
        "id": 1,
        "title": "Cấu trúc dữ liệu và Giải thuật",
        "author": "Nguyễn Văn A",
        "year": 2021,
        "publisher": "NXB Giáo dục",
        "genre": "Computer Science",
        "isbn": "978-604-123-456-7",
        "available": True
    },
    {
        "id": 2,
        "title": "Đại số tuyến tính",
        "author": "Trần Thị B",
        "year": 2020,
        "publisher": "NXB Đại học Quốc gia",
        "genre": "Mathematics",
        "isbn": "978-604-234-567-8",
        "available": False
    },
    {
        "id": 3,
        "title": "Hệ điều hành",
        "author": "Lê Văn C",
        "year": 2019,
        "publisher": "NXB Khoa học và Kỹ thuật",
        "genre": "Computer Science",
        "isbn": "978-604-345-678-9",
        "available": True
    },
    {
        "id": 4,
        "title": "Nguyên lý Máy học",
        "author": "Phạm Duy D",
        "year": 2022,
        "publisher": "NXB Thông tin và Truyền thông",
        "genre": "Artificial Intelligence",
        "isbn": "978-604-456-789-0",
        "available": True
    },
    {
        "id": 5,
        "title": "Mạng máy tính",
        "author": "Ngô Văn E",
        "year": 2018,
        "publisher": "NXB Lao động",
        "genre": "Networking",
        "isbn": "978-604-567-890-1",
        "available": False
    }
]

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
    book = next((b for b in books if b["id"] == id), None)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    if not book["available"]:
        return jsonify({"error": "Book is already borrowed"}), 400
    
    book["available"] = False
    return jsonify({"message": f"You borrowed '{book['title']}'", "book": book})

# Return a book
@app.route("/books/<int:id>/return", methods=["POST"])
def return_book(id):
    book = next((b for b in books if b["id"] == id), None)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    if book["available"]:
        return jsonify({"error": "Book was not borrowed"}), 400
    
    book["available"] = True
    return jsonify({"message": f"You returned '{book['title']}'", "book": book})

if __name__ == "__main__":
    app.run(debug=True)