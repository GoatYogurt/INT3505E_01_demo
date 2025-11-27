from flask import Flask
import os


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('JWT_SECRET','dev_secret')

    from app.routes.auth import auth_bp
    from app.routes.v1.books import books_v1
    from app.routes.v2.books import books_v2
    from app.routes.header.books_header import books_header
    from app.routes.query.books_query import books_query
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(books_v1)
    app.register_blueprint(books_v2)
    app.register_blueprint(books_header)
    app.register_blueprint(books_query)
    return app