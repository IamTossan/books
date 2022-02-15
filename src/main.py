import uuid
from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()


class CreatePageDTO(BaseModel):
    name: str


class UpdatePageDTO(BaseModel):
    name: str


class Page(BaseModel):
    id: str
    name: str
    version: int = 1
    status: str = "DRAFT"


pages = []


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/health")
async def health():
    return {"status": "RUNNING"}


@app.get("/pages")
async def get_pages():
    return pages


@app.get("/pages/{page_id}")
async def get_page(page_id: str):
    page = [p for p in pages if p["id"] == page_id][-1]
    return page


@app.post("/pages")
async def create_page(page: CreatePageDTO):
    new_page = Page(id=str(uuid.uuid4()), name=page.dict()["name"])
    pages.append(new_page.dict())
    return {"id": new_page.id}


@app.put("/pages/{page_id}")
async def get_page(page_id: str, payload: UpdatePageDTO):
    page = [p for p in pages if p["id"] == page_id][-1]
    if page["status"] == "PUBLISHED":
        new_page = Page(
            id=page_id, name=payload.dict()["name"], version=page["version"] + 1
        )
        pages.append(new_page.dict())
        return new_page
    page["name"] = payload.dict()["name"]
    return page


@app.post("/pages/publish/{page_id}")
async def publish_page(page_id: str):
    page = [p for p in pages if p["id"] == page_id][-1]
    page["status"] = "PUBLISHED"
    return page
