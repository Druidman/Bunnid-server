from flask import Blueprint, request

from server import globals

docs_bp = Blueprint("docs", __name__)


@docs_bp.route("/getWs", methods=["GET"])
def getWsDocs():
    return "Under construction..."


