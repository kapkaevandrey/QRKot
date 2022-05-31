from datetime import datetime
from typing import Optional

from pydantic import BaseModel, PositiveInt, Extra, Field, validator, root_validator


class ProjectCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str
    full_amount: PositiveInt

    class Config:
        extra = Extra.forbid


class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None)
    full_amount: Optional[PositiveInt]

    @validator('name', 'full_amount')
    def value_cannot_be_none(cls, value):
        if value is None:
            raise ValueError(
                'value cannot be None'
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
