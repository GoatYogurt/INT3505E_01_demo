from flask import Flask
import os
import logging
import sys

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('JWT_SECRET','dev_secret')

    # logging configuration
    log_level = logging.DEBUG
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - **%(name)s** - %(message)s'
    )
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.encoding = 'utf-8'

    file_handler = logging.FileHandler('app.log', encoding='utf-8')
    file_handler.setFormatter(formatter)

    app.logger.setLevel(log_level)
    app.logger.addHandler(console_handler)
    app.logger.addHandler(file_handler)

    # import and register blueprints
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