class Book:
    def __init__(self, id, title, author, year, publisher, genre, isbn, available=True):
        self.id = id
        self.title = title
        self.author = author
        self.year = year
        self.publisher = publisher
        self.genre = genre
        self.isbn = isbn
        self.available = available

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "publisher": self.publisher,
            "genre": self.genre,
            "isbn": self.isbn,
            "available": self.available
        }
    

class User:
    def __init__(self, username, password, role='user'):
        self.username = username
        self.password = password
        self.role = role

    def to_dict(self):
        return {
            "username": self.username,
            "password": self.password,
            "role": self.role
        }