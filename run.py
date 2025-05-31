from flask import Flask
from app.routes import api
from app.config import Config
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    CORS(app, supports_credentials=True, origins=["http://localhost:3000"])
    app.config.from_object(Config)
    app.register_blueprint(api, url_prefix='/api')
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
