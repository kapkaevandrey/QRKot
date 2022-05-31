import uuid
from datetime import datetime
from typing import Optional
from uuid import uuid4

from pydantic import BaseModel, Field, PositiveInt, UUID4


class DonationCreate(BaseModel):
    full_amount: PositiveInt
    comment: Optional[str]


class DonationUpdate(BaseModel):
    pass


class DonationRead(DonationCreate):
    id: int
    create_date: datetime
    close_date: Optional[datetime]
    user_id: UUID4 = Field(default_factory=uuid.uuid4)
    invested_amount: int
    fully_invested: bool

    class Config:
        orm_mode = True
