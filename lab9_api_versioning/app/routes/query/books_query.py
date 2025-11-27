from flask import Blueprint, request
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['library_db']
books_collection = db['books']

VERSION_QUERY_PARAM = 'version'

books_query = Blueprint('books_query', __name__, url_prefix='/books-query')

def get_api_version_from_query(request):
    version = request.args.get(VERSION_QUERY_PARAM, 'v1')
    print(f"API version from query parameter: {version}")
    return version

def get_book_data(book, version):
    if version == 'v2':
        return {
            "id": book.get("id"),
            "title": book.get("title"),
            "author": book.get("author"),
            "published_date": book.get("published_date"),
            "publisher": book.get("publisher"),
            "genre": book.get("genre"),
            "isbn": book.get("isbn"),
            "available": book.get("available", True),
            "version": "v2"
        }
    else:  # default to v1
        return {
            "id": book.get("id"),
            "title": book.get("title"),
            "author": book.get("author"),
            "published_date": book.get("published_date"),
            "publisher": book.get("publisher"),
            "genre": book.get("genre"),
            "isbn": book.get("isbn"),
            "available": book.get("available", True),
            "version": "v1"
        }
    
@books_query.route('/', methods=['GET'])
def get_books():
    version = get_api_version_from_query(request)
    books = books_collection.find()
    result = [get_book_data(book, version) for book in books]
    return {"books": result}, 200