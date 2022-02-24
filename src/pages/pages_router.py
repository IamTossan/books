from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from . import pages_service as service
from . import pages_schema as schemas
from src.database import get_db


router = APIRouter()


@router.get("", response_model=list[schemas.Page])
async def get_pages(db: Session = Depends(get_db)):
    pages = service.get_pages(db)
    return pages


@router.get("/{page_id}", response_model=schemas.Page)
async def get_page(page_id: str, db: Session = Depends(get_db)):
    page = service.get_page(db, page_id=page_id)
    if page is None:
        raise HTTPException(status_code=404, detail="User not found")
    return page


@router.post("", response_model=schemas.Page)
async def create_page(page: schemas.CreatePageDTO, db: Session = Depends(get_db)):
    return service.create_page(db, page=page)


@router.put("/{page_id}", response_model=schemas.Page)
async def update_page(
    page_id: str, payload: schemas.UpdatePageDTO, db: Session = Depends(get_db)
):
    return service.update_page(db, page_id, payload)


@router.post("/publish/{page_id}", response_model=schemas.Page)
async def publish_page(page_id: str, db: Session = Depends(get_db)):
    return service.publish_page(db, page_id=page_id)


@router.post("/comment/{page_id}")
async def comment_page(
    page_id: str,
    payload: schemas.CreatePageContributionDTO,
    db: Session = Depends(get_db),
):
    return service.create_contribution(db, page_id, payload)


@router.get("/contributions/{page_id}")
async def get_page_contribution(page_id: str, db: Session = Depends(get_db)):
    return service.get_page_contribution(db, page_id)
