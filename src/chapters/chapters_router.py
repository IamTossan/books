from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from . import chapters_service as service
from . import chapters_schema as schemas
from src.database import get_db


router = APIRouter()


@router.get("")
async def get_chapters(db: Session = Depends(get_db)):
    return service.get_chapters(db)


@router.get("/{chapter_id}", response_model=schemas.Chapter)
async def get_chapter(chapter_id: str, db: Session = Depends(get_db)):
    chapter = service.get_chapter(db, chapter_id=chapter_id)
    if chapter is None:
        raise HTTPException(status_code=404, detail="User not found")
    return chapter


@router.post("")
async def create_chapter(
    chapter: schemas.CreateChapterDTO, db: Session = Depends(get_db)
):
    return service.create_chapter(db, chapter)
