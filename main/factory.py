from fastapi import FastAPI, Depends, Request
from lib.utils.controller import Controller

def create_app():
    app = FastAPI()
    app.controller = Controller()

    return app
