from sqlalchemy import (
    Column,
    Integer,
    String,
    Enum,
)
from sqlalchemy.orm import relationship

from src.models import Base, BaseColumns, PublicationStatus, Chapter_Page


class Chapter(Base, BaseColumns):
    __tablename__ = "chapters"

    uuid = Column(String)
    name = Column(String)
    version = Column(Integer, default=1)
    status = Column(Enum(PublicationStatus), default=PublicationStatus.DRAFT)

    pages = relationship("Page", secondary=Chapter_Page)
