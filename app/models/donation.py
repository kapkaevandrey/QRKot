from fastapi_users_db_sqlalchemy.guid import GUID
from sqlalchemy import Column, ForeignKey, Text

from .abstract_base import ProjectDonation


class Donation(ProjectDonation):
    user_id = Column(GUID, ForeignKey('user.id'), nullable=False)
    comment = Column(Text, nullable=True)

    def __repr__(self):
        return (
            f'Donation №{self.id} - {self.full_amount}, '
            f'invested - {self.invested_amount}'
        )
