from datetime import datetime

from sqlalchemy import (
    Boolean, CheckConstraint, Column, DateTime,
    Integer,
)

from app.core.db import Base


class ProjectDonation(Base):
    __abstract__ = True
    __table_args__ = (CheckConstraint('full_amount > 0', 'full_amount_greater_than_zero'),)

    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(
        DateTime,
        nullable=True
    )

    @property
    def is_active(self) -> bool:
        return not self.fully_invested

    @property
    def remain(self) -> int:
        return self.full_amount - self.invested_amount

    def deactivate(self):
        self.invested_amount = self.full_amount
        self.fully_invested = True
        self.close_date = datetime.now()
