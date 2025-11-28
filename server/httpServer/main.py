from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from .routes import *
import uvicorn
import server.globals as globals
from server.db import setup_db
from server.eventPool import setupEventPool



def run_http_server() -> None:
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
    @app.on_event("startup")
    async def startup():
        await setup_db()
        setupEventPool() # setup events

    @app.get("/healthz")
    async def healthz() -> dict[str, str]:
        
        return {"status": "OK"}
    

    api = APIRouter(prefix="/api")
    
    api.include_router(auth_router)
    api.include_router(service_router)
    api.include_router(websocket_router)


    app.include_router(api)
    
    uvicorn.run(app, host="0.0.0.0", port=5000)

