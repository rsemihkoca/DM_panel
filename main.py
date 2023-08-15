import uvicorn
from fastapi import FastAPI
from database import models
from database.db import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/health")
async def healthy():
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)