from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.configs.database_settings import initialize
from app.routers.address_router import router as address_router
from app.routers.category_router import router as category_router
from app.routers.chat_router import router as chat_router
from app.routers.inspector_router import router as inspector_router
from app.routers.product_router import router as product_router
from app.routers.term_agreement_router import router as term_agreement_router
from app.routers.term_router import router as term_router
from app.routers.user_router import router as user_router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(product_router)
app.include_router(term_router)
app.include_router(user_router)
app.include_router(inspector_router)
app.include_router(term_agreement_router)
app.include_router(address_router)
app.include_router(category_router)
app.include_router(chat_router)
initialize(app)
