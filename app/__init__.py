from fastapi import FastAPI

from app.configs.database_settings import initialize
from app.routers.term_router import router as term_router

app = FastAPI()
app.include_router(term_router)
initialize(app)
