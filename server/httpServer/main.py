from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .blueprints import *
import os



def run_http_server():
    app = FastAPI()
    origins = [
        "http://localhost:5173"
    ]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins, 
        allow_credentials=True,
        allow_methods=["*"],   
        allow_headers=["*"],   
    )

    @app.route("/healthz", methods=["GET", "HEAD"])
    async def healthz():
        return "OK", 200
    
    # app.register_blueprint(auth_bp, url_prefix="/api/auth")
    # app.register_blueprint(session_bp, url_prefix="/api/session")
    # app.register_blueprint(docs_bp, url_prefix="/api/docs")
    # app.register_blueprint(service_bp, url_prefix="/api/service")
    # app.run(host="0.0.0.0", port=5000)

