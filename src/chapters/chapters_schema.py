from pydantic import BaseModel

from src.models import PublicationStatus
from src.pages.pages_schema import Page


class CreateChapterDTO(BaseModel):
    name: str
    pages: list[str]


class Chapter(BaseModel):
    uuid: str
    version: int
    name: str
    status: PublicationStatus
    pages: list[Page] = []

    class Config:
        orm_mode = True
