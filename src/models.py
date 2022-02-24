import enum
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    DateTime,
    dialects,
    Table,
)
from sqlalchemy.sql import func

from .database import Base


class BaseColumns:
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(
        DateTime(timezone=True).with_variant(
            dialects.sqlite.DATETIME(truncate_microseconds=False), "sqlite"
        ),
        server_default=func.now(),
    )
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


Chapter_Page = Table(
    "chapter_page",
    Base.metadata,
    Column("chapter_id", ForeignKey("chapters.id")),
    Column("page_id", ForeignKey("pages.id")),
)


class PublicationStatus(enum.Enum):
    DRAFT = "DRAFT"
    PUBLISHED = "PUBLISHED"
