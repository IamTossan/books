import uuid
from sqlalchemy.orm import Session

from . import chapters_model as models
from . import chapters_schema as schemas
from src.pages.pages_service import get_page


def get_chapter(db: Session, chapter_id: str):
    return (
        db.query(models.Chapter)
        .filter(models.Chapter.uuid == chapter_id)
        .order_by(models.Chapter.updated_at.desc(), models.Chapter.id.desc())
        .first()
    )


def get_chapters(db: Session):
    return db.query(models.Chapter).all()


def create_chapter(db: Session, chapter: schemas.CreateChapterDTO):
    pages = [get_page(db, page_id) for page_id in chapter.pages]
    new_chapter = models.Chapter(name=chapter.name, uuid=str(uuid.uuid4()), pages=pages)
    db.add(new_chapter)
    db.commit()
    db.refresh(new_chapter)
    return new_chapter
