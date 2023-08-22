import uvicorn
from database import models
from database.db import engine
from factory import create_app
models.Base.metadata.create_all(bind=engine)
app = create_app()

if __name__ == "__main__":
    app.controller.start()
