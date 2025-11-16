from flask import Blueprint, request

from server import globals


from .services import conversation_bp
from .services import database_bp

service_bp = Blueprint("service", __name__)

service_bp.register_blueprint(conversation_bp, url_prefix="/conversation")
service_bp.register_blueprint(database_bp, url_prefix="/database")


@service_bp.route("/", methods=["GET"])
def serviceMain():
    return "<h1>This is service api! /conversation, /database</h1>"


