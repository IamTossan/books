import uuid
from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()


class CreatePageDTO(BaseModel):
    name: str


class UpdatePageDTO(BaseModel):
    name: str


class Comment(BaseModel):
    author: str
    comment: str


class Page(BaseModel):
    id: str
    name: str
    version: int = 1
    status: str = "DRAFT"
    comments: list[Comment] = []


class CreateChapterDTO(BaseModel):
    name: str
    pages: list[str]


class Chapter(BaseModel):
    id: str
    name: str
    version: int = 1
    status: str = "DRAFT"
    pages: list[str]


pages = []
chapters = []


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


@app.post("/pages/comment/{page_id}")
async def comment_page(page_id: str, payload: Comment):
    page = [p for p in pages if p["id"] == page_id and p["status"] == "PUBLISHED"][-1]
    page["comments"].append(payload.dict())
    return page


@app.get("/chapters")
async def get_chapters():
    return chapters


@app.get("/chapters/{chapter_id}")
async def get_chapters(chapter_id: str):
    chapter = [c for c in chapters if c["id"] == chapter_id][-1].copy()
    chapter["pages"] = list(
        map(
            lambda page_id: [p for p in pages if p["id"] == page_id][-1],
            chapter["pages"],
        )
    )
    return chapter


@app.post("/chapters")
async def create_chapter(chapter: CreateChapterDTO):
    new_chapter = Chapter(
        id=str(uuid.uuid4()), name=chapter.dict()["name"], pages=chapter.dict()["pages"]
    )
    chapters.append(new_chapter.dict())
    return {"id": new_chapter.id}
