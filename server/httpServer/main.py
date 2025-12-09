from fastapi import FastAPI, APIRouter, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .routes import *
import uvicorn, os
import server.globals as globals
from server.db import setup_db
from server.eventPool import setupEventPool
from contextlib import asynccontextmanager

@asynccontextmanager
async def app_lifespan(app: FastAPI):
    #startup
    await setup_db()
    setupEventPool() # setup events

    yield

    #shutdown
    await globals.connPool.close()

def run_http_server() -> None:
    app = FastAPI(lifespan=app_lifespan)
    origins = [
        "http://localhost:3000",
        "https://bunnid-app.onrender.com"
    ]
    app_url = os.getenv("BUNNID_APP_URL", "")
    if app_url:
        origins.append(app_url)
    else:
        print("No app url found")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins, 
        allow_credentials=True,
        allow_methods=["*"],   
        allow_headers=["*"],   
    )
    

    @app.get("/healthz")
    async def healthz() -> dict[str, str]:
        
        return {"status": "OK"}
    
    @app.middleware("http")
    async def block_ips(request: Request, call_next):
        client_ip = request.client.host

        if client_ip == "83.25.221.83":
            return JSONResponse(
                status_code=403,
                content={"detail": "Forbidden"},
            )

        return await call_next(request)
    

    api = APIRouter(prefix="/api")
    
    api.include_router(auth_router)
    api.include_router(service_router)
    api.include_router(websocket_router)


    app.include_router(api)
    
    uvicorn.run(app, host="localhost", port=os.environ.get("PORT", 8000))