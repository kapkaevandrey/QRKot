from datetime import datetime
from typing import Optional

from pydantic import BaseModel, PositiveInt, UUID4


class DonationCreate(BaseModel):
    full_amount: PositiveInt
    comment: Optional[str]


class DonationUpdate(BaseModel):
    pass


class DonationRead(DonationCreate):
    id: int
    create_date: datetime


class DonationReadFull(DonationRead):
    user_id: UUID4
    invested_amount: PositiveInt
    fully_invested: bool
    close_data: datetime

    class Config:
        orm_mode = True
