from fastapi import FastAPI

from routes import router

app = FastAPI(title="Test billing api")
app.include_router(router)
