from flask import Flask
import os


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('JWT_SECRET','dev_secret')

    from app.routes.auth import auth_bp
    from app.routes.books import books_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(books_bp, url_prefix='/books')

    return app