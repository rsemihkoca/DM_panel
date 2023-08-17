import uvicorn
from database import models
from database.db import engine
from factory import create_app

models.Base.metadata.create_all(bind=engine)

app = create_app()

@app.get("/health")
async def healthy():
    return {"status": "healthy"}

if __name__ == "__main__":
    app.controller.start()
    # uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)