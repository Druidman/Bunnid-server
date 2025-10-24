from flask import Flask

from blueprints import auth_bp


app = Flask(__name__)
app.register_blueprint(auth_bp, url_prefix="/api")







