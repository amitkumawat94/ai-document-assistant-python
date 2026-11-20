import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.chat import router as chat_router
from app.routes.documents import router as documents_router
from app.services.vector_service import vector_service


app = FastAPI(
    title="AI Document Assistant",
    description="RAG backend built with FastAPI, Qdrant and Groq",
    version="1.0.0",
)

allowed_origins = os.getenv(
    "FRONTEND_ORIGINS",
    "http://localhost:3000,http://127.0.0.1:3000",
).split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in allowed_origins if origin.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    vector_service.create_collection()


app.include_router(chat_router)
app.include_router(documents_router)


@app.get("/health")
async def health():
    return {"status": "ok"}
