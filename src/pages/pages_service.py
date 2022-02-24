import uuid
from sqlalchemy.orm import Session

from . import pages_schema as schemas
from . import pages_model as models


def get_page(db: Session, page_id: str):
    return (
        db.query(models.Page)
        .filter(models.Page.uuid == page_id)
        .order_by(models.Page.updated_at.desc(), models.Page.id.desc())
        .first()
    )


def get_pages(db: Session):
    return db.query(models.Page).all()


def create_page(db: Session, page: schemas.CreatePageDTO):
    new_page = models.Page(name=page.name, uuid=str(uuid.uuid4()))
    db.add(new_page)
    db.commit()
    db.refresh(new_page)
    return new_page


def publish_page(db: Session, page_id: str):
    published_page = (
        db.query(models.Page)
        .filter(models.Page.uuid == page_id, models.Page.status == "DRAFT")
        .first()
    )
    published_page.status = models.PublicationStatus.PUBLISHED
    db.add(published_page)
    db.commit()
    db.refresh(published_page)
    return published_page


def update_page(db: Session, page_id: str, page: schemas.UpdatePageDTO):
    current_page = get_page(db, page_id)
    if current_page.status == models.PublicationStatus.PUBLISHED:
        new_draft = models.Page(
            uuid=current_page.uuid,
            name=page.name,
            version=current_page.version + 1,
        )
        db.add(new_draft)
        db.commit()
        db.refresh(new_draft)
        return new_draft
    else:
        db.query(models.Page).filter(models.Page.id == current_page.id).update(
            page.dict()
        )
        db.commit()
        db.refresh(current_page)
        return current_page


def create_contribution(
    db: Session, page_id: str, payload: schemas.CreatePageContributionDTO
):
    page = (
        db.query(models.Page)
        .filter(
            models.Page.uuid == page_id,
            models.Page.status == models.PublicationStatus.PUBLISHED,
        )
        .order_by(models.Page.updated_at.desc(), models.Page.id.desc())
        .first()
    )
    new_contribution = models.PageContribution(
        author=payload.author, comment=payload.comment, page_id=page.id
    )
    db.add(new_contribution)
    db.commit()
    db.refresh(new_contribution)
    return new_contribution


def get_page_contribution(db: Session, page_id: str):
    pages = (
        db.query(models.Page)
        .filter(
            models.Page.uuid == page_id,
            models.Page.status == models.PublicationStatus.PUBLISHED,
        )
        .all()
    )
    return (
        db.query(models.PageContribution)
        .filter(models.PageContribution.page_id.in_([p.id for p in pages]))
        .first()
    )
