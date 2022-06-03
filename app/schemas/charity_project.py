from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt, validator


class ProjectBase(BaseModel):
    class Config:
        extra = Extra.forbid
        min_anystr_length = 1


class ProjectCreate(ProjectBase):
    name: str = Field(..., max_length=100)
    description: str
    full_amount: PositiveInt


class ProjectUpdate(ProjectBase):
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str]
    full_amount: Optional[PositiveInt]

    @validator('name', 'full_amount')
    def value_cannot_be_none(cls, value):
        if not value or value is None:
            raise ValueError(
                'Значение не может быть равно null'
            )
        return value

    class Config:
        extra = Extra.forbid


class ProjectRead(ProjectCreate):
    id: int
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]
    create_date: datetime

    class Config:
        orm_mode = True
