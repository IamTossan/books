from datetime import datetime
from pydantic import BaseModel

from src.models import PublicationStatus


class CreatePageDTO(BaseModel):
    name: str

    class Config:
        orm_mode = True


class UpdatePageDTO(BaseModel):
    name: str

    class Config:
        orm_mode = True


class Page(BaseModel):
    uuid: str
    name: str
    version: int
    status: PublicationStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class CreatePageContributionDTO(BaseModel):
    author: str
    comment: str

    class Config:
        orm_mode = True
