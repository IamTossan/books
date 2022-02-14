import uuid
from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()


class CreatePageDTO(BaseModel):
    name: str


class Page(BaseModel):
    id: str = str(uuid.uuid4())
    name: str
    status: str = "DRAFT"


pages = {}


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/health")
async def health():
    return {"status": "RUNNING"}


@app.get("/pages")
async def get_pages():
    return list(pages.values())


@app.get("/pages/{page_id}")
async def get_page(page_id: str):
    return pages[page_id]


@app.post("/pages")
async def create_page(page: CreatePageDTO):
    new_page = Page(**page.dict())
    pages[new_page.id] = new_page.dict()
    return {"id": new_page.id}


@app.post("/pages/publish/{page_id}")
async def publish_page(page_id: str):
    pages[page_id]["status"] = "PUBLISHED"
    return pages[page_id]
