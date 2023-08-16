from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from routers import db_router

origins = ["*"]

def create_app():
    app = FastAPI()
    # app.logger
    # app.controller
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(db_router.router, prefix="/db", tags=["database"])

    return app
