from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Page(BaseModel):
    name: str


pages = {}


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/pages")
async def get_pages():
    def parse_output(i):
        return {"id": i[0], "name": i[1].name}
    return list(map(parse_output, pages.items()))


@app.get("/pages/{page_id}")
async def get_page(page_id: int):
    return pages[page_id]


@app.post("/pages")
async def create_page(page: Page):
    id = len(pages) + 1
    pages[id] = page
    return {"id": id}
