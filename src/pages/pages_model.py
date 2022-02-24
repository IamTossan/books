from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Enum,
)
from sqlalchemy.orm import relationship

from src.models import Base, BaseColumns, PublicationStatus


class Page(Base, BaseColumns):
    __tablename__ = "pages"

    uuid = Column(String)
    name = Column(String)
    version = Column(Integer, default=1)
    status = Column(Enum(PublicationStatus), default=PublicationStatus.DRAFT)

    contributions = relationship("PageContribution")

    def __repr__(self):
        return f"<Page {self.uuid} {self.name} {self.version} {self.status} {self.created_at} {self.updated_at}>"


class PageContribution(Base, BaseColumns):
    __tablename__ = "page_contributions"

    author = Column(String)
    comment = Column(String)

    page_id = Column(Integer, ForeignKey("pages.id"))
