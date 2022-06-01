from fastapi_users_db_sqlalchemy.guid import GUID
from sqlalchemy import Column, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from .abstract_base import ProjectDonation
from .user import UserTable


class Donation(ProjectDonation):
    user_id = Column(GUID, ForeignKey('user.id'), nullable=False)
    comment = Column(Text, nullable=True)

    def __repr__(self):
        return (
            f'Donation №{self.id} - {self.full_amount}, '
            f'invested - {self.invested_amount}'
        )
