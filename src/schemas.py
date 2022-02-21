from typing import Optional
from datetime import datetime

from pydantic import BaseModel

from .models import PublicationStatus


class CreatePageDTO(BaseModel):
    name: str

    class Config:
        orm_mode = True


class UpdatePageDTO(BaseModel):
    name: str

    class Config:
        orm_mode = True


class CreateChapterDTO(BaseModel):
    name: str
    pages: list[str]


class Page(BaseModel):
    uuid: str
    name: str
    version: int
    status: PublicationStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class Chapter(BaseModel):
    uuid: str
    version: int
    name: str
    status: PublicationStatus
    pages: list[Page] = []

    class Config:
        orm_mode = True


class CreatePageContributionDTO(BaseModel):
    author: str
    comment: str

    class Config:
        orm_mode = True
