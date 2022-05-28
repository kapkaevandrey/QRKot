from datetime import datetime

from sqlalchemy import (
    Boolean, CheckConstraint, Column, DateTime,
    Integer,
)

from app.core.db import Base


class ProjectDonation(Base):
    __abstract__ = True

    full_amount = Column(Integer, nullable=False, )
    invested_amount = Column(Integer, nullable=False, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, server_default=datetime.now())
    close_data = Column(
        DateTime,
        server_onupdate=datetime.now(),
        nullable=True,
        default=None
    )

    __table_args__ = [CheckConstraint(full_amount > 0, 'full_amount_greater_than_zero'), ]
