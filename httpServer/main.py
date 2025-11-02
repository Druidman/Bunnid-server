from flask import Flask
from flask_cors import CORS
from .blueprints import *



def run_http_server():
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(session_bp, url_prefix="/api/session")
    app.register_blueprint(docs_bp, url_prefix="/api/docs")
    app.register_blueprint(service_bp, url_prefix="/api/service")
    app.run(host="0.0.0.0", port=5000)

