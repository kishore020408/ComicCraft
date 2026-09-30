from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import router
import os
os.makedirs("app/static", exist_ok=True)
app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(router)