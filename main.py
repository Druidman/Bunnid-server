from flask import Flask
from .blueprints import *
from .db import connectDb

dbConn = connectDb()
if not dbConn:
    print("Error when connecting to db!")
    exit()

app = Flask(__name__)
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(session_bp, url_prefix="/api/session")
