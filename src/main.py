import uuid
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel

from sqlalchemy.orm import Session

from . import service, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/health")
async def health():
    return {"status": "RUNNING"}


@app.get("/pages", response_model=list[schemas.Page])
async def get_pages(db: Session = Depends(get_db)):
    pages = service.get_pages(db)
    return pages


@app.get("/pages/{page_id}", response_model=schemas.Page)
async def get_page(page_id: str, db: Session = Depends(get_db)):
    page = service.get_page(db, page_id=page_id)
    if page is None:
        raise HTTPException(status_code=404, detail="User not found")
    return page


@app.post("/pages", response_model=schemas.Page)
async def create_page(page: schemas.CreatePageDTO, db: Session = Depends(get_db)):
    return service.create_page(db, page=page)


@app.put("/pages/{page_id}", response_model=schemas.Page)
async def update_page(
    page_id: str, payload: schemas.UpdatePageDTO, db: Session = Depends(get_db)
):
    return service.update_page(db, page_id, payload)


@app.post("/pages/publish/{page_id}", response_model=schemas.Page)
async def publish_page(page_id: str, db: Session = Depends(get_db)):
    return service.publish_page(db, page_id=page_id)


@app.post("/pages/comment/{page_id}")
async def comment_page(
    page_id: str,
    payload: schemas.CreatePageContributionDTO,
    db: Session = Depends(get_db),
):
    return service.create_contribution(db, page_id, payload)


@app.get("/pages/contributions/{page_id}")
async def get_page_contribution(page_id: str, db: Session = Depends(get_db)):
    return service.get_page_contribution(db, page_id)


@app.get("/chapters")
async def get_chapters(db: Session = Depends(get_db)):
    return service.get_chapters(db)


@app.get("/chapters/{chapter_id}", response_model=schemas.Chapter)
async def get_chapter(chapter_id: str, db: Session = Depends(get_db)):
    chapter = service.get_chapter(db, chapter_id=chapter_id)
    if chapter is None:
        raise HTTPException(status_code=404, detail="User not found")
    return chapter


@app.post("/chapters")
async def create_chapter(
    chapter: schemas.CreateChapterDTO, db: Session = Depends(get_db)
):
    return service.create_chapter(db, chapter)
