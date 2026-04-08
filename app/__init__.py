from flask import Flask

def create_app():
    app = Flask(__name__)
    app.secret_key = "your_secret_key_here"

    from . import routes
    routes.init_app(app)

    return app