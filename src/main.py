from fastapi import FastAPI

from . import models
from .database import engine

from src.pages import pages_router
from src.chapters import chapters_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(pages_router.router, prefix="/pages")
app.include_router(chapters_router.router, prefix="/chapters")


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/health")
async def health():
    return {"status": "RUNNING"}
