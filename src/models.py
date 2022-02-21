import enum
from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    Enum,
    DateTime,
    dialects,
    Table,
)
from sqlalchemy.orm import relationship
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


class Page(Base, BaseColumns):
    __tablename__ = "pages"

    uuid = Column(String)
    name = Column(String)
    version = Column(Integer, default=1)
    status = Column(Enum(PublicationStatus), default=PublicationStatus.DRAFT)

    contributions = relationship("PageContribution")
    # chapters = relationship(
    #     "Chapter", secondary=Chapter_Page, back_populates="chapters"
    # )

    def __repr__(self):
        return f"<Page {self.uuid} {self.name} {self.version} {self.status} {self.created_at} {self.updated_at}>"


class Chapter(Base, BaseColumns):
    __tablename__ = "chapters"

    uuid = Column(String)
    name = Column(String)
    version = Column(Integer, default=1)
    status = Column(Enum(PublicationStatus), default=PublicationStatus.DRAFT)

    pages = relationship("Page", secondary=Chapter_Page)


class PageContribution(Base, BaseColumns):
    __tablename__ = "page_contributions"

    author = Column(String)
    comment = Column(String)

    page_id = Column(Integer, ForeignKey("pages.id"))
