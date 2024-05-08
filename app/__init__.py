from fastapi import FastAPI

from app.configs.database_settings import initialize

app = FastAPI()
initialize(app)
