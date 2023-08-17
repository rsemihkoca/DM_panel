from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from routers import db_router
from lib.utils.controller import Controller
origins = ["*"]

def create_app():
    app = FastAPI()
    # app.loggeri
    app.controller = Controller()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(db_router.router, prefix="/db", tags=["database"])

    return app
